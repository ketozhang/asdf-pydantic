import pytest

from asdf_pydantic.converter import AsdfPydanticConverter
from asdf_pydantic.model import AsdfPydanticModel


class TestModel(AsdfPydanticModel):
    _tag = "https://example.org/test_model"


@pytest.mark.parametrize("args", [tuple(), (TestModel,)])
def test_converter_is_unscoped_by_default(args):
    assert AsdfPydanticConverter(*args) is not AsdfPydanticConverter(*args)
