import textwrap
from unittest.mock import MagicMock, patch

import asdf
import asdf.schema
import pytest
import yaml
from asdf.extension import Extension

from asdf_pydantic import AsdfPydanticConverter
from tests.examples.shapes import AsdfRectangle


@pytest.fixture()
def asdf_extension():
    """Registers an ASDF extension containing models for this test."""
    converter = AsdfPydanticConverter()
    converter.add_models(AsdfRectangle)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [converter]  # type: ignore
        tags = [AsdfRectangle.get_tag_definition()]  # type: ignore

    with asdf.config_context() as asdf_config:
        asdf_config.add_resource_mapping(
            {
                yaml.safe_load(AsdfRectangle.model_asdf_schema())[
                    "id"
                ]: AsdfRectangle.model_asdf_schema()
            }
        )
        asdf_config.add_extension(TestExtension())
        yield asdf_config


@pytest.mark.usefixtures("asdf_extension")
def test_check_schema():
    """Tests the model schema is correct."""
    schema = yaml.safe_load(AsdfRectangle.model_asdf_schema())
    asdf.schema.check_schema(schema)


@pytest.mark.usefixtures("asdf_extension")
def test_can_write_valid_asdf_file(tmp_path):
    """Tests using the model to write an ASDF file validates its own schema."""
    af = asdf.AsdfFile()
    af["root"] = AsdfRectangle(width=42, height=10)
    af.validate()
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert af.tree


@pytest.mark.usefixtures("asdf_extension")
@patch.object(
    AsdfRectangle, "model_validate", MagicMock()
)  # Ignore pydantic validation
def test_errors_reading_invalid_asdf_file(tmp_path):
    """Tests validation fails when ASDF file does not match the schema."""
    content = """\
        #ASDF 1.0.0
        #ASDF_STANDARD 1.5.0
        %YAML 1.1
        %TAG ! tag:stsci.edu:asdf/
        --- !core/asdf-1.1.0
        asdf_library: !core/software-1.0.0 {
            author: The ASDF Developers,
            homepage: 'http://github.com/asdf-format/asdf',
            name: asdf,
            version: 2.14.3}
        history:
        extensions:
        - !core/extension_metadata-1.0.0
            extension_class: asdf.extension.BuiltinExtension
            software: !core/software-1.0.0 {
                name: asdf,
                version: 2.14.3}
        - !core/extension_metadata-1.0.0 {
            extension_class: mypackage.shapes.ShapesExtension,
            extension_uri: 'asdf://asdf-pydantic/shapes/extensions/shapes-1.0.0'}
        rect: !<asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0>
            height: "10"
            width: "42"
        ...
    """
    with open(tmp_path / "test.asdf", "w") as f:
        f.write(textwrap.dedent(content))

    with pytest.raises(asdf.exceptions.ValidationError):
        with asdf.open(tmp_path / "test.asdf") as af:
            assert af.tree
