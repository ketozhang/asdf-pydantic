import asdf
import pytest
from asdf.extension import Extension
from pydantic import BaseModel

from asdf_pydantic import AsdfPydanticConverter, AsdfPydanticModel


class Dog(BaseModel):
    name: str


class DogAsdfBySubclass(Dog, AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/dog-1.0.0"


def setup_module():
    AsdfPydanticConverter.add_models(DogAsdfBySubclass)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [AsdfPydanticConverter()]  # type: ignore
        tags = [*AsdfPydanticConverter().tags]  # type: ignore

    asdf.get_config().add_extension(TestExtension())


def test_can_write_with_subclass_model(tmp_path):
    fido = DogAsdfBySubclass(name="Fido")

    af = asdf.AsdfFile({"dog": fido})
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af["dog"], Dog)
        assert isinstance(af["dog"], DogAsdfBySubclass)
        assert af["dog"] == fido


def test_cannot_write_with_original_model(tmp_path):
    fido = Dog(name="Fido")
    af = asdf.AsdfFile({"dog": fido})

    with pytest.raises(
        # ASDF will raise RepresenterError (subclass of YAMLError).
        # HACK: Catching general exception to avoid depending on YAMLError
        Exception
    ):
        af.write_to(tmp_path / "test.asdf")


def test_can_write_with_cast_to_subclass_model(tmp_path):
    fido = Dog(name="Fido")
    fido_asdf = DogAsdfBySubclass.model_validate(fido.model_dump())
    af = asdf.AsdfFile({"dog": fido_asdf})
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        msg = "Read object should be the same object written"
        assert af["dog"] == fido_asdf, msg

        msg = "Read object should be the same as non-ASDF object when casted back"
        assert Dog.model_validate(af["dog"]) == fido_asdf, msg
