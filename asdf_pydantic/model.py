from typing import ClassVar

import yaml
from pydantic import BaseModel, ConfigDict
from typing_extensions import deprecated

from asdf_pydantic.schema import DEFAULT_ASDF_SCHEMA_REF_TEMPLATE, GenerateAsdfSchema


class AsdfPydanticModel(BaseModel):
    """

    ASDF Serialization and Deserialization:
        Serialize to ASDF yaml tree is done with the
        py:classmethod`AsdfPydanticModel.asdf_yaml_tree()` and deserialize to an
        AsdfPydanticModel object with py:meth`AsdfPydanticModel.parse_obj()`.
    """

    _tag: ClassVar[str]
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def asdf_yaml_tree(self) -> dict:
        d = {}
        for field_key, v in self.__dict__.items():
            if field_key not in self.__fields__:
                continue

            if isinstance(v, AsdfPydanticModel):
                d[field_key] = v
            else:
                d[field_key] = self._get_value(
                    v,
                    to_dict=True,
                    by_alias=False,
                    include=None,
                    exclude=None,
                    exclude_unset=False,
                    exclude_defaults=False,
                    exclude_none=False,
                )

        return d

    @classmethod
    def model_asdf_schema(
        cls,
        by_alias: bool = True,
        ref_template: str = DEFAULT_ASDF_SCHEMA_REF_TEMPLATE,
        schema_generator: type[GenerateAsdfSchema] = GenerateAsdfSchema,
    ):
        """Get the ASDF schema definition for this model."""
        # Implementation follows closely with the `BaseModel.model_json_schema`
        schema_generator_instance = schema_generator(
            by_alias=by_alias,
            ref_template=ref_template,
            tag=cls._tag,
        )
        json_schema = schema_generator_instance.generate(cls.__pydantic_core_schema__)

        return f"%YAML 1.1\n---\n{yaml.safe_dump(json_schema)}"

    @classmethod
    @deprecated(
        "The `schema_asdf` method is deprecated; use `model_asdf_schema` instead."
    )
    def schema_asdf(
        cls,
        *,
        metaschema: str = GenerateAsdfSchema.schema_dialect,
        **kwargs,
    ) -> str:
        """Get the ASDF schema definition for this model.

        Parameters
        ----------
        metaschema, optional
            A metaschema URI
        """  # noqa: E501
        if metaschema != GenerateAsdfSchema.schema_dialect:
            raise NotImplementedError(
                f"Only {GenerateAsdfSchema.schema_dialect} is supported as metaschema."
            )

        return cls.model_asdf_schema(**kwargs)
