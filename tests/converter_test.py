from tempfile import NamedTemporaryFile

import asdf
from asdf.extension import Extension

from asdf_pydantic.converter import create_converter
from asdf_pydantic.examples.shapes import Rectangle


class ShapesExtension(Extension):
    extension_uri = "asdf://example.com/shapes/extensions/shapes-1.0.0"  # type: ignore
    converters = [
        create_converter(
            Rectangle,
            tags=["asdf://example.com/shapes/tags/rectangle-1.0.0"],
            types=["asdf_pydantic.examples.shapes.Rectangle"],
        )
    ]  # type: ignore
    tags = ["asdf://example.com/shapes/tags/rectangle-1.0.0"]  # type: ignore


def setup_module():
    asdf.get_config().add_extension(ShapesExtension())


def test_create_asdf_file():
    with NamedTemporaryFile() as tempfile:
        af = asdf.AsdfFile({"rect": Rectangle(width=42, height=10)})
        af.write_to(tempfile.name)
