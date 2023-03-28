from datetime import datetime
from typing import Any, Optional

import asdf
import pytest
from asdf.extension import Extension
from astropy.time import Time

from asdf_pydantic import AsdfPydanticConverter, AsdfPydanticModel


class UnionObject(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/unionobject-1.0.0"

    # Order of type matters
    int_or_str: int | str = 0
    datetime_or_time: datetime | Time = datetime(2023, 1, 1)
    anything: Optional[Any] = None


def setup_module():
    AsdfPydanticConverter.add_models(UnionObject)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [AsdfPydanticConverter()]  # type: ignore
        tags = [*AsdfPydanticConverter().tags]  # type: ignore

    asdf.get_config().add_extension(TestExtension())


def test_str_converts_to_str(tmp_path):
    af = asdf.AsdfFile(
        {
            "obj": UnionObject(
                int_or_str="test",
            )
        }
    )
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af["obj"].int_or_str, str)


def test_integer_converts_to_int(tmp_path):
    asdf.AsdfFile(
        {
            "obj": UnionObject(
                int_or_str=0,
            )
        }
    ).write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af["obj"].int_or_str, int)


def test_datetime_converts_to_datetime(tmp_path):
    af = asdf.AsdfFile(
        {
            "obj": UnionObject(
                datetime_or_time=datetime(2023, 1, 1, 0),
            )
        }
    )
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af["obj"].datetime_or_time, datetime)


def test_Time_converts_to_Time(tmp_path):
    af = asdf.AsdfFile(
        {
            "obj": UnionObject(
                datetime_or_time=Time(
                    "2023-01-01T01:00:00", format="isot", scale="utc"
                ),
            )
        }
    )
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af["obj"].datetime_or_time, Time)


@pytest.mark.parametrize(
    "value",
    [
        0,
        1.0,
        "asdf",
        dict(key="value"),
        # (1, 2, 3),  # Tuples are returned as list in ASDF
        [1, 2, 3],
        {1, 2, 3},
        Time("2023-01-01T00:00:00", format="isot", scale="utc"),
        datetime(2023, 1, 1, 1, 0, 0),
    ],
)
def test_Any_converts_back_to_itself(value, tmp_path):
    af = asdf.AsdfFile({"obj": UnionObject(anything=value)})
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af["obj"].anything, type(value))
