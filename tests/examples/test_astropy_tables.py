from __future__ import annotations
from typing import Annotated, TypeVar

import asdf
import astropy.units as u
from asdf.extension import Extension
from astropy.table import Table
from astropy.units import Quantity
from pydantic import WithJsonSchema
import pytest
import yaml

from asdf_pydantic import AsdfPydanticConverter, AsdfPydanticModel

T = TypeVar("T", bound=Table)

AsdfAstropyTable = Annotated[
    T,
    WithJsonSchema(
        {
            "type": "object",
            "$ref": "http://stsci.edu/schemas/asdf.org/table/table-1.1.0",
        }
    ),
]


class Database(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/database-1.0.0"
    positions: AsdfAstropyTable[Table]


@pytest.fixture()
def asdf_extension():
    """Registers an ASDF extension containing models for this test."""
    AsdfPydanticConverter.add_models(Database)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [AsdfPydanticConverter()]  # type: ignore
        tags = [*AsdfPydanticConverter().tags]  # type: ignore

    asdf.get_config().add_extension(TestExtension())

    with asdf.config_context() as asdf_config:
        asdf_config.add_resource_mapping(
            {
                yaml.safe_load(Database.model_asdf_schema())[
                    "id"
                ]: Database.model_asdf_schema()
            }
        )
        print(Database.model_asdf_schema())
        asdf_config.add_extension(TestExtension())
        yield asdf_config


@pytest.mark.usefixtures("asdf_extension")
def test_convert_to_asdf(tmp_path):
    database = Database(
        positions=Table(
            {
                "x": Quantity([1, 2, 3], u.m),
                "y": Quantity([4, 5, 6], u.m),
            }
        )
    )
    asdf.AsdfFile({"data": database}).write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af.tree["data"], Database)
        assert isinstance(af.tree["data"].positions, Table)


@pytest.mark.usefixtures("asdf_extension")
def test_check_schema():
    """Tests the model schema is correct."""
    schema = yaml.safe_load(Database.model_asdf_schema())
    asdf.schema.check_schema(schema)
