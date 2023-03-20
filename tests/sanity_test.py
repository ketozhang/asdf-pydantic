from tempfile import NamedTemporaryFile

import asdf
from asdf.extension import Converter, Extension

from asdf_pydantic import AsdfBaseModel


class Rectangle(AsdfBaseModel):
    width: float
    height: float

    @property
    def area(self):
        return self.width * self.height


class RectangleConverter(Converter):
    tags = ["asdf://example.com/shapes/tags/rectangle-1.0.0"]
    types = ["tests.sanity_test.Rectangle"]

    def to_yaml_tree(self, obj, tag, ctx):
        return obj.asdf_yaml_tree()

    def from_yaml_tree(self, node, tag, ctx):
        return Rectangle.parse_obj(node)


class ShapesExtension(Extension):
    extension_uri = "asdf://example.com/shapes/extensions/shapes-1.0.0"
    converters = [RectangleConverter()]
    tags = ["asdf://example.com/shapes/tags/rectangle-1.0.0"]


def setup_module():
    asdf.get_config().add_extension(ShapesExtension())


def test_sanity_create_rectangle():
    rect = Rectangle(width=42, height=10)
    assert rect.width == 42
    assert rect.height == 10


def test_sanity_create_rectangle_from_dict():
    rect = Rectangle.parse_obj({"width": 42, "height": 10})
    assert rect.width == 42
    assert rect.height == 10


def test_create_asdf_file():
    with NamedTemporaryFile() as tempfile:
        af = asdf.AsdfFile({"rect": Rectangle(width=42, height=10)})
        af.write_to(tempfile.name)
