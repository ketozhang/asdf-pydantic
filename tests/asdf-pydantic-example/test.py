import logging

import asdf
from asdf import AsdfFile
from astropy import units as u

from shapes.circle import Circle


def test_write_asdf(tmp_path):
    af = AsdfFile({"data": Circle(radius=1 * u.m)})
    af.write_to(tmp_path / "circle.asdf")

    with asdf.open("circle.asdf") as af:
        af.info()
        logging.info(af.tree["data"])
