from typing import Type

from asdf.extension import Converter

from asdf_pydantic.model import AsdfPydanticModel


class AsdfPydanticConverter(Converter):
    _tag_to_class: dict[str, Type[AsdfPydanticModel]] = {}

    @property
    def tags(self) -> tuple[str]:
        return tuple(self._tag_to_class.keys())

    @property
    def types(self) -> tuple[str | Type]:
        return tuple(self._tag_to_class.values())

    def to_yaml_tree(self, obj: AsdfPydanticModel, tag, ctx):
        return obj.asdf_yaml_tree()

    def from_yaml_tree(self, node, tag, ctx):
        return self._tag_to_class[tag].parse_obj(node)


def create_converter(model_class: Type[AsdfPydanticModel]) -> AsdfPydanticConverter:
    converter = AsdfPydanticConverter()
    converter._tag_to_class[model_class._tag] = model_class
    return converter


def register_models_to_converter(
    *model_classes: Type[AsdfPydanticModel],
) -> None:
    for model_class in model_classes:
        AsdfPydanticConverter._tag_to_class[model_class._tag] = model_class
