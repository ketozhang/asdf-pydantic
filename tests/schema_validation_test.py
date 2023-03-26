from tempfile import NamedTemporaryFile

import asdf
import jsonschema
import pytest
import yaml
from asdf.extension import Extension, TagDefinition

from asdf_pydantic.converter import create_converter
from asdf_pydantic.examples.shapes import AsdfPydanticRectangle


class ShapesExtension(Extension):
    extension_uri = "asdf://asdf-pydantic/shapes/extensions/shapes-1.0.0"  # type: ignore
    converters = [
        create_converter(
            AsdfPydanticRectangle,
            tags="asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0",  # type: ignore
            types=["asdf_pydantic.examples.shapes.AsdfPydanticRectangle"],
        )
    ]
    tags = [  # type: ignore
        TagDefinition(
            "asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0",
            schema_uris="asdf://asdf-pydantic/shapes/schemas/rectangle-1.0.0",
        )
    ]


rectangle_schema_yaml = """
%YAML 1.1
---
$schema: http://stsci.edu/schemas/asdf/asdf-schema-1.0.0
id: asdf://asdf-pydantic/shapes/schemas/rectangle-1.0.0

title: AsdfPydanticRectangle
description: ""
type: object

properties:
  height:
    # title: Height
    type: number
  width:
    # title: Width
    type: number
required:
- width
- height
"""

resource_mapping = {
    "asdf://asdf-pydantic/shapes/schemas/rectangle-1.0.0": rectangle_schema_yaml.encode(
        "utf-8"
    )
}


def setup_module():
    asdf.get_config().add_extension(ShapesExtension())
    asdf.get_config().add_resource_mapping(resource_mapping)


def test_schema_exists_and_valid():
    from asdf.schema import check_schema, load_schema

    check_schema(load_schema("asdf://asdf-pydantic/shapes/schemas/rectangle-1.0.0"))


def test_create_asdf_file():
    with NamedTemporaryFile() as tempfile:
        af = asdf.AsdfFile({"rect": AsdfPydanticRectangle(width=10, height=10)})
        af.write_to(tempfile.name)


def test_validate_pass_on_good_yaml_file():
    """Given a YAML file that follows the schema, when loading the file with
    asdf, then validation should pass.
    """
    with NamedTemporaryFile() as tempfile:

        tempfile.write(
            """\
#ASDF 1.0.0
#ASDF_STANDARD 1.5.0
%YAML 1.1
%TAG ! tag:stsci.edu:asdf/
--- !core/asdf-1.1.0
asdf_library: !core/software-1.0.0 {author: The ASDF Developers, homepage: 'http://github.com/asdf-format/asdf',
name: asdf, version: 2.11.2}
history:
    extensions:
    - !core/extension_metadata-1.0.0
        extension_class: asdf.extension.BuiltinExtension
        software: !core/software-1.0.0 {name: asdf, version: 2.11.2}
    - !core/extension_metadata-1.0.0
        extension_class: asdf_pydantic.examples.extensions.AsdfPydanticShapesExtension
        extension_uri: asdf://asdf-pydantic/shapes/extensions/shapes-1.0.0
        software: !core/software-1.0.0 {name: asdf-pydantic, version: 0.1.0}
rect: !<asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0> {height: 10.0, width: 10.0}
...
    """.rstrip().encode(
                "utf-8"
            )
        )
        tempfile.seek(0)

        asdf.open(tempfile.name)


def test_validate_fail_on_bad_yaml_file():
    """Given a YAML file with the wrong type on the rectangle width, when
    loading the file with asdf, then the asdf schema validation error should be raised.

    It is important that the ASDF's schema validation fails before the pydantic's.
    """
    with NamedTemporaryFile() as tempfile:
        tempfile.write(
            """
#ASDF 1.0.0
#ASDF_STANDARD 1.5.0
%YAML 1.1
%TAG ! tag:stsci.edu:asdf/
--- !core/asdf-1.1.0
asdf_library: !core/software-1.0.0 {author: The ASDF Developers, homepage: 'http://github.com/asdf-format/asdf',
name: asdf, version: 2.11.2}
history:
    extensions:
    - !core/extension_metadata-1.0.0
        extension_class: asdf.extension.BuiltinExtension
        software: !core/software-1.0.0 {name: asdf, version: 2.11.2}
    - !core/extension_metadata-1.0.0
        extension_class: asdf_pydantic.examples.extensions.AsdfPydanticShapesExtension
        extension_uri: asdf://asdf-pydantic/shapes/extensions/shapes-1.0.0
        software: !core/software-1.0.0 {name: asdf-pydantic, version: 0.1.0}
rect: !<asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0> {height: 1.0, width: "somestr"}
...
    """.strip().encode(
                "utf-8"
            )
        )
        tempfile.seek(0)

        with pytest.raises(jsonschema.ValidationError):
            asdf.open(tempfile.name)
