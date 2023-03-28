from __future__ import annotations

from datetime import datetime
from typing import Optional

import astropy.units as u

from asdf_pydantic import AsdfPydanticModel


class AsdfTimeEntry(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/time-entry-1.0.0"
    time: Optional[datetime] = None
    speed: u.Quantity[u.m / u.s]
    distance: u.Quantity[u.m]

    class Config:
        arbitrary_types_allowed = True
