import textwrap
from typing import ClassVar

from pydantic import BaseModel


class AsdfBaseModel(BaseModel):
    """

    ASDF Serialization and Deserialization:
        Serialize to ASDF yaml tree is done with the
        py:classmethod`AsdfBaseModel.asdf_yaml_tree()` and deserialize to an
        AsdfBaseModel object with py:meth`AsdfBaseModel.parse_obj()`.
    """

    tag_uri: ClassVar[str]

    def asdf_yaml_tree(self) -> dict:
        d = {}
        for field_key, v in self.__dict__.items():
            if field_key not in self.__fields__:
                continue

            if isinstance(v, AsdfBaseModel):
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
    def schema_asdf(
        cls, *, metaschema="http://stsci.edu/schemas/asdf/asdf-schema-1.0.0"
    ) -> str:
        # TODO: Function signature should follow BaseModel.schema() or
        # BaseModel.schema_json()
        import yaml

        header = textwrap.dedent(
            f"""
            %YAML 1.1
            ---
            $schema: {metaschema}
            id: {cls.tag_uri}

            """
        )

        body = yaml.dump(cls.schema())

        return header + body
