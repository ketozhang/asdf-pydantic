from typing import ClassVar

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
