from tempfile import NamedTemporaryFile

import asdf
import astropy.units as u
from asdf.extension import Extension
from astropy.time import Time
from astropy.units import Quantity

from asdf_pydantic import AsdfPydanticConverter, AsdfPydanticModel


class DataPoint(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/datapoint-1.0.0"

    time: Time
    distance: Quantity[u.m]


def setup_module():
    AsdfPydanticConverter.add_models(DataPoint)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [AsdfPydanticConverter()]  # type: ignore
        tags = [*AsdfPydanticConverter().tags]  # type: ignore

    asdf.get_config().add_extension(TestExtension())


def test_convert_to_asdf():
    af = asdf.AsdfFile(
        {
            "positions": [
                DataPoint(
                    time=Time("2023-01-01T00:00:00"),
                    distance=0 * u.m,
                ),
                DataPoint(
                    time=Time("2023-01-01T01:00:00"),
                    distance=1 * u.m,
                ),
            ]
        }
    )

    with NamedTemporaryFile() as fp:
        af.write_to(fp)
