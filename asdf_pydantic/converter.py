from typing import Type

from asdf.extension import Converter, TagDefinition

from asdf_pydantic.model import AsdfPydanticModel


class AsdfPydanticConverter(Converter):
    _model_class: Type[AsdfPydanticModel]
    _tags: list[str]
    _types: list[str]

    @property
    def tags(self) -> list[str]:
        return self._tags

    @property
    def types(self) -> list[str]:
        return self._types

    def to_yaml_tree(self, obj: AsdfPydanticModel, tag, ctx):
        return obj.asdf_yaml_tree()

    def from_yaml_tree(self, node, tag, ctx):
        return self._model_class.parse_obj(node)


# class AsdfPydanticConverterFactory:
#     def __call__(self, *args: Any, **kwds: Any) -> Any:
#         pass


def create_converter(
    model_class: Type[AsdfPydanticModel],
    *,
    tags: list[str | TagDefinition] | None = None,
    types: list[str]
) -> Converter:
    converter = AsdfPydanticConverter()
    converter._model_class = model_class
    converter._tags = tags or [model_class.tag_uri]  # type: ignore
    converter._types = types  # type: ignore
    return converter
