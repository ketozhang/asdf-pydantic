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

    tag_uri: ClassVar[str]

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
    def schema_asdf(
        cls, *, metaschema: str = "http://stsci.edu/schemas/asdf/asdf-schema-1.0.0"
    ) -> str:
        """Get the ASDF schema definition for this model.

        Parameters
        ----------
        metaschema, optional
            A metaschema URI, by default "http://stsci.edu/schemas/asdf/asdf-schema-1.0.0".
            See https://asdf.readthedocs.io/en/stable/asdf/extending/schemas.html#anatomy-of-a-schema
            for more options.
        """
        # TODO: Function signature should follow BaseModel.schema() or
        # BaseModel.schema_json()
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
