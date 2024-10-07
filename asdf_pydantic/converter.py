from __future__ import annotations

from typing import Optional, Type

from asdf.extension import Converter

from asdf_pydantic.model import AsdfPydanticModel

_ASDF_PYDANTIC_SINGLETON_CONVERTER: Optional[AsdfPydanticConverter] = None


class AsdfPydanticConverter(Converter):
    """Implements a converter compatible with all subclass of AsdfPydanticModel.

    The instance is a singleton.
    """

    _tag_to_class: dict[str, Type[AsdfPydanticModel]] = {}

    def __init__(self) -> None:
        global _ASDF_PYDANTIC_SINGLETON_CONVERTER

        if _ASDF_PYDANTIC_SINGLETON_CONVERTER is None:
            _ASDF_PYDANTIC_SINGLETON_CONVERTER = self

        self = _ASDF_PYDANTIC_SINGLETON_CONVERTER

    @classmethod
    def add_models(
        cls, *model_classes: Type[AsdfPydanticModel]
    ) -> "AsdfPydanticConverter":
        for model_class in model_classes:
            cls._tag_to_class[model_class.get_tag_uri()] = model_class
        return cls()

    @property
    def tags(self) -> tuple[str]:
        return tuple(self._tag_to_class.keys())

    @property
    def types(self) -> tuple[str | Type]:
        return tuple(self._tag_to_class.values())

    def select_tag(self, obj, tags, ctx):
        return obj._tag

    def to_yaml_tree(self, obj: AsdfPydanticModel, tag, ctx):
        return obj.asdf_yaml_tree()

    def from_yaml_tree(self, node, tag, ctx):
        return self._tag_to_class[tag].parse_obj(node)
