from typing import Type

from asdf.extension import Converter, TagDefinition

from asdf_pydantic.model import AsdfBaseModel


class AsdfPydanticConverter(Converter):
    _model_class: Type[AsdfBaseModel]
    tags = None
    types = None

    def to_yaml_tree(self, obj: AsdfBaseModel, tag, ctx):
        return obj.asdf_yaml_tree()

    def from_yaml_tree(self, node, tag, ctx):
        return self._model_class.parse_obj(node)


# class AsdfPydanticConverterFactory:
#     def __call__(self, *args: Any, **kwds: Any) -> Any:
#         pass


def create_converter(
    model_class: Type[AsdfBaseModel],
    *,
    tags: list[str | TagDefinition] | None = None,
    types: list[str]
) -> Converter:
    converter = AsdfPydanticConverter()
    converter._model_class = model_class
    converter.tags = tags or [model_class.tag_uri]  # type: ignore
    converter.types = types  # type: ignore
    return converter
