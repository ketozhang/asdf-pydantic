from asdf.extension import Extension

import asdf_pydantic.schema
from asdf_pydantic import AsdfPydanticConverter
from asdf_pydantic_example.circle import Circle

converter = AsdfPydanticConverter()
converter.add_models(Circle)


class ShapesExtension(Extension):
    extension_uri = "asdf://asdf-pydantic/examples/extensions/shapes-1.0.0"  # type: ignore
    converters = [converter]  # type: ignore
    tags = [*converter.tags]  # type: ignore


def get_extensions():
    return [ShapesExtension()]


def get_resource_mappings():
    schema_mapping = asdf_pydantic.schema.generate_resource_mapping(
        "mypackage.schemas", "generated/"
    )

    return [schema_mapping]
