from asdf_pydantic import AsdfBaseModel


class AsdfPydanticRectangle(AsdfBaseModel):
    width: float
    height: float

    @property
    def area(self):
        return self.width * self.height
