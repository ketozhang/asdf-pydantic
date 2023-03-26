from asdf_pydantic import AsdfBaseModel


class AsdfPydanticRectangle(AsdfBaseModel):
    tag_uri = "asdf://asdf-pydantic.com/shapes/tags/rectangle-1.0.0"
    width: float
    height: float

    @property
    def area(self):
        return self.width * self.height
