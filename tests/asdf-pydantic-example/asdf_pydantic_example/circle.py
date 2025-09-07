from typing import Annotated

from asdf_pydantic import AsdfPydanticModel
from asdf_pydantic.schema import AsdfTag
from astropy import units as u


class Circle(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/circle-1.0.0"
    radius: Annotated[
        u.Quantity[u.m], AsdfTag("http://stsci.edu/schemas/asdf/unit/quantity-1.2.0")
    ]
