from asdf.extension import Extension

from asdf_pydantic.converter import create_converter
from asdf_pydantic.examples.shapes import AsdfPydanticRectangle


class AsdfPydanticShapesExtension(Extension):
    extension_uri = "asdf://asdf-pydantic/shapes/extensions/shapes-1.0.0"  # type: ignore
    converters = [
        create_converter(
            AsdfPydanticRectangle,
            tags=["asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0"],
            types=["asdf_pydantic.examples.shapes.AsdfPydanticRectangle"],
        )
    ]  # type: ignore
    tags = ["asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0"]  # type: ignore


def get_extensions() -> list[Extension]:
    return [AsdfPydanticShapesExtension()]
