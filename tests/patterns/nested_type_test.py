import asdf
from asdf.extension import Extension

from asdf_pydantic import AsdfPydanticConverter, AsdfPydanticModel


class Dog(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/dog-1.0.0"
    name: str


class DogPark(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/dog-park-1.0.0"
    pets: list[Dog] = []  # Pydantic will create new list instance

    def add(self, dog: Dog) -> None:
        self.pets.append(dog)


def setup_module():
    AsdfPydanticConverter.add_models(
        Dog,
        DogPark,
    )

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [AsdfPydanticConverter()]  # type: ignore
        tags = [*AsdfPydanticConverter().tags]  # type: ignore

    asdf.get_config().add_extension(TestExtension())


def test_sanity(tmp_path):
    fido = Dog(name="Fido")
    park = DogPark()
    park.add(fido)

    af = asdf.AsdfFile({"park": park})
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        assert isinstance(af["park"], DogPark)
        assert isinstance(af["park"].pets[0], Dog)
