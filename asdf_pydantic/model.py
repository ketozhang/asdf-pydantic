import textwrap
from typing import ClassVar

import yaml
from pydantic import BaseModel


class AsdfPydanticModel(BaseModel):
    """

    ASDF Serialization and Deserialization:
        Serialize to ASDF yaml tree is done with the
        py:classmethod`AsdfPydanticModel.asdf_yaml_tree()` and deserialize to an
        AsdfPydanticModel object with py:meth`AsdfPydanticModel.parse_obj()`.
    """

    _tag: ClassVar[str]

    class Config:
        arbitrary_types_allowed = True

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

        header = "%YAML 1.1\n---\n"

        return f"{header}\n{yaml.safe_dump(json_schema)}"
    def schema_asdf(
        cls,
        *,
        metaschema: str = "http://stsci.edu/schemas/asdf/asdf-schema-1.0.0",
        **kwargs,
    ) -> str:
        """Get the ASDF schema definition for this model.

        Parameters
        ----------
        metaschema, optional
            A metaschema URI, by default "http://stsci.edu/schemas/asdf/asdf-schema-1.0.0".
            See https://asdf.readthedocs.io/en/stable/asdf/extending/schemas.html#anatomy-of-a-schema
            for more options.
        """  # noqa: E501
        header = textwrap.dedent(
            f"""
            %YAML 1.1
            ---
            $schema: {metaschema}
            id: {cls._tag}
            tag: tag:{cls._tag.split('://', maxsplit=2)[-1]}

            """
        )
        body = yaml.safe_dump(cls.model_json_schema())
        return header + body
