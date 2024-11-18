import asdf
import pytest
import yaml
from asdf.extension import Extension

from asdf_pydantic import AsdfPydanticConverter, AsdfPydanticModel


class MetaModel(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/meta-model-1.0.0"
    author: str


class DataModel(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/data-model-1.0.0"
    value: int


class MainModel(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/main-model-1.0.0"
    meta: MetaModel
    data: DataModel


@pytest.fixture()
def asdf_extension():
    """Registers an ASDF extension containing models for this test."""

    converter = AsdfPydanticConverter()
    converter.add_models(MainModel, DataModel, MetaModel)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [converter]  # type: ignore
        tags = [MainModel.get_tag_definition()]  # type: ignore

    with asdf.config_context() as asdf_config:
        asdf_config.add_resource_mapping(
            {
                yaml.safe_load(MainModel.model_asdf_schema())[
                    "id"
                ]: MainModel.model_asdf_schema()
            }
        )
        asdf_config.add_extension(TestExtension())
        yield asdf_config


@pytest.mark.usefixtures("asdf_extension")
def test_can_write_valid_asdf_file(tmp_path):
    """Tests using the model to write an ASDF file validates its own schema."""
    af = asdf.AsdfFile()
    af["root"] = MainModel(data=DataModel(value=1), meta=MetaModel(author="foobar"))
    af.validate()
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert af.tree
