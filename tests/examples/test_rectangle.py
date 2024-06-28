import asdf
from asdf.extension import Extension
from asdf.schema import check_schema, load_schema

from asdf_pydantic import AsdfPydanticConverter
from asdf_pydantic.examples.shapes import AsdfRectangle


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
                AsdfRectangle.schema_asdf().encode("utf-8")
            )
        }
    )
    asdf.get_config().add_extension(TestExtension())


def test_schema():
    schema = load_schema("asdf://asdf-pydantic/shapes/schemas/rectangle-1.0.0")

    check_schema(schema)

    assert schema["$schema"] == "http://stsci.edu/schemas/asdf/asdf-schema-1.0.0"
    assert schema["title"] == "AsdfRectangle"
    assert schema["id"] == "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"
    assert schema["tag"] == "tag:asdf-pydantic/examples/tags/rectangle-1.0.0"
    assert schema["type"] == "object"
    assert schema["properties"] == {
        "width": {
            "type": "number",
            "title": "Width",
        },
        "height": {
            "type": "number",
            "title": "Height",
        },
    }

    assert schema["required"] == ["width", "height"]
