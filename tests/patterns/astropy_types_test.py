from __future__ import annotations

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


class DataContainer(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/datacontainer-1.0.0"

    positions: list[DataPoint]


def setup_module():
    AsdfPydanticConverter.add_models(DataPoint, DataContainer)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [AsdfPydanticConverter()]  # type: ignore
        tags = [*AsdfPydanticConverter().tags]  # type: ignore

    asdf.get_config().add_extension(TestExtension())


def test_convert_DataPoint_to_asdf(tmp_path):
    asdf.AsdfFile(
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
    ).write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af.tree["positions"], list)
        for position in af.tree["positions"]:
            assert isinstance(position, DataPoint)


def test_convert_DataContainer_to_asdf(tmp_path):
    asdf.AsdfFile(
        {
            "container": DataContainer(
                positions=[
                    DataPoint(
                        time=Time("2023-01-01T00:00:00"),
                        distance=0 * u.m,
                    ),
                    DataPoint(
                        time=Time("2023-01-01T01:00:00"),
                        distance=1 * u.m,
                    ),
                ]
            )
        }
    ).write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af["container"], DataContainer)
