from datetime import datetime
from tempfile import NamedTemporaryFile

import asdf

from asdf_pydantic.examples.extensions import ExampleExtension
from asdf_pydantic.examples.with_units import AsdfTimeEntry


def setup_module():
    asdf.get_config().add_extension(ExampleExtension())


def test_sanity():
    import astropy.units as u

    entry = AsdfTimeEntry(
        time=datetime(2023, 1, 1),
        speed=u.Quantity(10, u.m / u.s),
        distance=u.Quantity(1, u.m),
    )
    af = asdf.AsdfFile({"entries": [entry]})

    with NamedTemporaryFile() as tempfile:
        af.write_to(tempfile.name)
        asdf.open(tempfile.name)
