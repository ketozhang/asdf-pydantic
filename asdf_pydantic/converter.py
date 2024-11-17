from __future__ import annotations

from typing import Type

from asdf.extension import Converter

from asdf_pydantic.model import AsdfPydanticModel


class AsdfPydanticConverter(Converter):
    """Implements a converter compatible with all subclass of AsdfPydanticModel."""

    _tag_to_class: dict[str, Type[AsdfPydanticModel]]

    def __init__(self, *model_classes: Type[AsdfPydanticModel]) -> None:
        self._tag_to_class = {}
        self.add_models(*model_classes)
        super().__init__()

    def add_models(
        self, *model_classes: Type[AsdfPydanticModel]
    ) -> "AsdfPydanticConverter":
        for model_class in model_classes:
            self._tag_to_class[model_class.get_tag_uri()] = model_class

        return self

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
