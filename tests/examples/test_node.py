"""Tests example asdf-pydantic model for nodes of a graph/tree."""

from __future__ import annotations

import textwrap
from unittest.mock import MagicMock, patch

import asdf
import asdf.exceptions
import asdf.schema
import pytest
import yaml
from asdf.extension import Extension

from asdf_pydantic import AsdfPydanticConverter, AsdfPydanticModel


class AsdfNode(AsdfPydanticModel):
    """Model for a node in a graph/tree.

    Nodes introduce self-referential types. Notice the type of the `child`
    attribute it the node type itself. The ASDF schema for this model will require
    self-referencing syntax. We assumes this form is valid for ASDF schemas:

    ```yaml
    ---
    type: object
    anyOf:
      - $ref: "#/definitions/AsdfNode"
    definitions:
        AsdfNode:
            type: object
            properties:
            name:
                type: string
            child:
                anyOf:
                - $ref: "#/definitions/AsdfNode"
                - type: null
    ```

    The self-reference happens in ``definitions[AsdfNode].properties.child.anyOf[0]``
    where the `$ref` is a special JSONSchema syntax that referes to the value,
    `#/definitions/AsdfNode`. This value is a json path where `#` denotes "this
    schema".
    """

    _tag = "asdf://asdf-pydantic/examples/tags/node-1.0.0"

    name: str
    child: AsdfNode | None = None


@pytest.fixture()
def asdf_extension():
    """Registers an ASDF extension containing models for this test."""
    AsdfPydanticConverter.add_models(AsdfNode)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [AsdfPydanticConverter()]  # type: ignore
        tags = [AsdfNode.get_tag_definition()]  # type: ignore

    with asdf.config_context() as asdf_config:
        asdf_config.add_resource_mapping(
            {
                yaml.safe_load(AsdfNode.model_asdf_schema())[
                    "id"
                ]: AsdfNode.model_asdf_schema()
            }
        )
        asdf_config.add_extension(TestExtension())
        yield asdf_config


@pytest.mark.usefixtures("asdf_extension")
def test_can_write_valid_asdf_file(tmp_path):
    """Tests using the model to write an ASDF file validates its own schema."""
    af = asdf.AsdfFile()
    af["root"] = AsdfNode(name="foo", child=None)
    af.validate()
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert af.tree


@pytest.mark.usefixtures("asdf_extension")
@patch.object(AsdfNode, "model_validate", MagicMock())  # Ignore pydantic validation
def test_errors_reading_invalid_asdf_file(tmp_path):
    """Tests ASDF validation fails when ASDF file does not match the schema."""
    content = """\
        #ASDF 1.0.0
        #ASDF_STANDARD 1.5.0
        %YAML 1.1
        %TAG ! tag:stsci.edu:asdf/
        --- !core/asdf-1.1.0
        asdf_library: !core/software-1.0.0 {author: The ASDF Developers, homepage: 'http://github.com/asdf-format/asdf',
            name: asdf, version: 3.4.0}
        history:
            extensions:
            - !core/extension_metadata-1.0.0
                extension_class: asdf.extension._manifest.ManifestExtension
                extension_uri: asdf://asdf-format.org/core/extensions/core-1.5.0
                manifest_software: !core/software-1.0.0 {name: asdf_standard, version: 1.1.1}
                software: !core/software-1.0.0 {name: asdf, version: 3.4.0}
            - !core/extension_metadata-1.0.0 {extension_class: tests.examples.test_node.setup_module.<locals>.TestExtension,
                extension_uri: 'asdf://asdf-pydantic/examples/extensions/test-1.0.0'}
        root: !<asdf://asdf-pydantic/examples/tags/node-1.0.0>
            child: None
        ...
    """
    with open(tmp_path / "test.asdf", "w") as f:
        f.write(textwrap.dedent(content))

    with pytest.raises(asdf.exceptions.ValidationError):
        with asdf.open(tmp_path / "test.asdf") as af:
            assert af.tree
