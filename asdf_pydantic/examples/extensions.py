from asdf.extension import Extension

from asdf_pydantic.converter import AsdfPydanticConverter
from asdf_pydantic.examples.shapes import AsdfRectangle
from asdf_pydantic.examples.tree import AsdfNode
from asdf_pydantic.examples.with_units import AsdfTimeEntry

AsdfPydanticConverter.add_models(AsdfRectangle, AsdfNode, AsdfTimeEntry)

class ExampleExtension(Extension):
    extension_uri = "asdf://asdf-pydantic/examples/extensions/examples-1.0.0"
    converters = [
        AsdfPydanticConverter()
    ]  # type: ignore
    tags = [*AsdfPydanticConverter().tags]  # type: ignore

def get_extensions() -> list[Extension]:
    return [ExampleExtension()]
