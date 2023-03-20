from abc import ABC, abstractmethod

from asdf import AsdfFile
from pydantic import BaseModel


class AsdfBaseModel(ABC, BaseModel):
    # @abstractmethod
    # def to_yaml(self):
    #     pass

    # @abstractmethod
    # def from_yaml(self):
    #     pass

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
