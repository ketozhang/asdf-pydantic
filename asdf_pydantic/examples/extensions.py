from asdf.extension import Extension

from asdf_pydantic.converter import create_converter
from asdf_pydantic.examples.shapes import AsdfRectangle
from asdf_pydantic.examples.tree import AsdfNode


class ExampleExtension(Extension):
    extension_uri = "asdf://asdf-pydantic/examples/extensions/examples-1.0.0"  # type: ignore
    converters = [
        create_converter(
            AsdfRectangle,
            types=[
                "asdf_pydantic.examples.shapes.AsdfRectangle",
            ],
        ),
        create_converter(
            AsdfNode,
            types=[
                "asdf_pydantic.examples.tree.AsdfNode",
            ],
        ),
    ]  # type: ignore
    tags = [AsdfRectangle.tag_uri, AsdfNode.tag_uri]  # type: ignore


def get_extensions() -> list[Extension]:
    return [ExampleExtension()]
