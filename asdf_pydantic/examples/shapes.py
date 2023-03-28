from asdf_pydantic import AsdfPydanticModel


class AsdfRectangle(AsdfPydanticModel):
    tag_uri = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"
    width: float
    height: float
