from asdf_pydantic import AsdfPydanticModel


class AsdfRectangle(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"
    width: float
    height: float
