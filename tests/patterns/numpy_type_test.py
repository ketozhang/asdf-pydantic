import asdf
import numpy as np
from asdf.extension import Extension
from numpy.typing import NDArray

from asdf_pydantic import AsdfPydanticConverter, AsdfPydanticModel


class ArrayContainer(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/array-container-1.0.0"

    array: NDArray  # Equivalently np.ndarray


def setup_module():
    """Register the ArrayContainer model with the AsdfPydanticConverter.

    Pytest will run this function before the tests in this module.
    """
    AsdfPydanticConverter.add_models(ArrayContainer)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-pydantic/examples/extensions/test-1.0.0"

        converters = [AsdfPydanticConverter()]  # type: ignore
        tags = [*AsdfPydanticConverter().tags]  # type: ignore

    asdf.get_config().add_extension(TestExtension())


########################################################################################
# Test Cases
########################################################################################


def test_convert_ArrayContainer_to_asdf(tmp_path):
    """When writing ArrayContainer to an ASDF file, the array field should be
    serialized to the original numpy array.
    """
    data = ArrayContainer(array=np.array([1, 2, 3]))
    af = asdf.AsdfFile({"data": data})
    af.write_to(tmp_path / "test.asdf")

    with asdf.open(tmp_path / "test.asdf") as af:
        breakpoint()
        assert isinstance(af.tree["data"], np.ndarray), (
            f"Expected {type(np.ndarray)}, " f"got {type(af.tree['data'])}"
        )
        assert np.all(af.tree["data"] == np.array([1, 2, 3]))
