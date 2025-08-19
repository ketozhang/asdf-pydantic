from typing import Any, ClassVar

import yaml
from asdf.extension import TagDefinition
from asdf.tagged import TaggedDict
from pydantic import BaseModel, ConfigDict, model_validator
from typing_extensions import deprecated

from asdf_pydantic.schema import DEFAULT_ASDF_SCHEMA_REF_TEMPLATE, GenerateAsdfSchema


class AsdfPydanticModel(BaseModel):
    """

    ASDF Serialization and Deserialization:
        Serialize to ASDF yaml tree is done with the
        {meth}`asdf_yaml_tree` and deserialize to an
        AsdfPydanticModel object with {meth}`model_validate`.
    """

    _tag: ClassVar[str | TagDefinition]
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def asdf_yaml_tree(self) -> dict:
        """Converts the model to an ASDF-compatible YAML tree (dict).

        :::{note}
        Any fields that are normal Pydantic `BaseModel` will be converted to
        dict. See conversion table.
        :::

        Conversion Table:

        | Value type in field       | Value type in dict                             |
        |---------------------------|------------------------------------------------|
        | AsdfPydanticModel         | No conversion                                  |
        | BaseModel                 | Converted to dict using BaseModel.model_dump() |
        | Other types               | No conversion                                  |
        """
        tree = {}
        for k, v in dict(self).items():
            if isinstance(v, AsdfPydanticModel):
                tree[k] = v
            elif isinstance(v, BaseModel):
                tree[k] = v.model_dump()
            else:
                tree[k] = v

        return tree

    @model_validator(mode="before")
    @classmethod
    def handle_asdf_tagged_dict_compat(cls, data: Any) -> dict:
        return dict(data) if isinstance(data, TaggedDict) else data

    @classmethod
    def get_tag_definition(cls):
        if isinstance(cls._tag, str):
            return TagDefinition(  # TODO: Add title and description
                cls._tag,
                schema_uris=[f"{cls._tag}/schema"],
            )
        return cls._tag

    @classmethod
    def get_tag_uri(cls):
        if isinstance(cls._tag, TagDefinition):
            return cls._tag.tag_uri
        else:
            return cls._tag

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
            by_alias=by_alias, ref_template=ref_template, tag_uri=cls.get_tag_uri()
        )
        json_schema = schema_generator_instance.generate(cls.__pydantic_core_schema__)

        return f"%YAML 1.1\n---\n{yaml.safe_dump(json_schema, sort_keys=False)}"

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
