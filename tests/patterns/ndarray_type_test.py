import asdf
import numpy as np
from asdf.extension import Extension

from asdf_pydantic import AsdfPydanticConverter, AsdfPydanticModel


class Data(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/data-1.0.0"
    array: np.ndarray


def setup_module():
    AsdfPydanticConverter.add_models(Data)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [AsdfPydanticConverter()]  # type: ignore
        tags = [*AsdfPydanticConverter().tags]  # type: ignore

    asdf.get_config().add_extension(TestExtension())


def test_can_write_with_subclass_model(tmp_path):
    data = Data(array=np.array([1, 2, 3]))

    af = asdf.AsdfFile({"data": data})
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf", lazy_load=False) as af:
        assert isinstance(af["data"], Data)
