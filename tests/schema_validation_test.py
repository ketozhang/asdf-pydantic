from tempfile import NamedTemporaryFile

import asdf
import pydantic
import pytest
import yaml
from asdf.extension import Extension
from asdf_pydantic import AsdfPydanticConverter

from asdf_pydantic.examples.shapes import AsdfRectangle
from asdf_pydantic.examples.tree import AsdfNode


def setup_module():
    AsdfPydanticConverter.add_models(AsdfRectangle)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"  # type: ignore

        tags = [*AsdfPydanticConverter().tags]  # type: ignore
        converters = [AsdfPydanticConverter()]  # type: ignore

    # HACK: The schema URI should be referenced from `AsdfRectangle._schema`.
    # Then there should be a way to automatically add the schema to ASDF
    # resources perhaps during AsdfPydanticConverter.add_models(). Further
    # abstracting can be done later, perhaps defining a
    # AsdfPydanticExtension.
    asdf.get_config().add_resource_mapping(
        {
            "asdf://asdf-pydantic/shapes/schemas/rectangle-1.0.0": (
                AsdfRectangle.model_asdf_schema().encode("utf-8")
            )
        }
    )
    asdf.get_config().add_extension(TestExtension())


def test_schema_exists_and_valid():
    from asdf.schema import check_schema, load_schema

    check_schema(load_schema("asdf://asdf-pydantic/shapes/schemas/rectangle-1.0.0"))


def test_create_asdf_file():
    with NamedTemporaryFile() as tempfile:
        af = asdf.AsdfFile({"rect": AsdfRectangle(width=10, height=10)})
        af.write_to(tempfile.name)


def test_validate_pass_on_good_yaml_file():
    """Given a YAML file that follows the schema, when loading the file with
    asdf, then validation should pass.
    """
    with NamedTemporaryFile() as tempfile:
        tempfile.write(
            (
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
        extension_uri: asdf://asdf-pydantic/examples/extensions/examples-1.0.0
        software: !core/software-1.0.0 {name: asdf-pydantic, version: 0.1.0}
rect: !<asdf://asdf-pydantic/examples/tags/rectangle-1.0.0> {height: 10.0, width: 10.0}
...
    """  # noqa: E501
            )
            .strip()
            .encode("utf-8")
        )
        tempfile.seek(0)

        asdf.open(tempfile.name)


def test_validate_fail_on_bad_yaml_file():
    """Given a YAML file with the wrong type on the rectangle width, when
    loading the file with asdf, then the asdf schema validation error should be raised.

    """
    with NamedTemporaryFile() as tempfile:
        tempfile.write(
            (
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
        extension_uri: asdf://asdf-pydantic/examples/extensions/examples-1.0.0
        software: !core/software-1.0.0 {name: asdf-pydantic, version: 0.1.0}
rect: !<asdf://asdf-pydantic/examples/tags/rectangle-1.0.0> {height: 1.0, width: "somestr"}
...
    """  # noqa: E501
            )
            .strip()
            .encode("utf-8")
        )
        tempfile.seek(0)

        # HACK: It is better that the ASDF's schema validation fails before
        # the pydantic's. However, it seems ASDF deserialize first then do their
        # validation.
        with pytest.raises((asdf.ValidationError, pydantic.ValidationError)):
            asdf.open(tempfile.name)


@pytest.mark.xfail(
    reason="Until schema replaces `$ref` with `tag` for tagged Asdf objects"
)
def test_given_child_field_contains_asdf_object_then_schema_has_child_tag():
    from asdf.schema import check_schema

    schema = yaml.safe_load(AsdfNode.model_asdf_schema())  # type: ignore
    check_schema(schema)

    child_schema = schema["definitions"]["AsdfNode"]["properties"]["child"]

    assert {"tag": AsdfNode._tag} in child_schema["anyOf"]
