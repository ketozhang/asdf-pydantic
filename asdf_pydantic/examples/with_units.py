from __future__ import annotations

from datetime import datetime

import astropy.units as u

from asdf_pydantic import AsdfBaseModel


class TimeEntry(AsdfBaseModel):
    tag_uri = "asdf://asdf-pydantic/examples/tags/time-entry-1.0.0"
    time: datetime
    speed: u.Quantity[u.m / u.s]
    distance: u.Quantity[u.m]