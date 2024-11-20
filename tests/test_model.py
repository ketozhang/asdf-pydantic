import pytest
import yaml
from asdf.extension import TagDefinition
from pydantic import BaseModel

from asdf_pydantic import AsdfPydanticModel


########################################################################################
# ASDF Tree
########################################################################################
def test_asdf_yaml_tree_sanity():
    class TestModel(AsdfPydanticModel):
        foo: str

    model = TestModel(foo="bar")
    assert model.asdf_yaml_tree() == {"foo": "bar"}


def test_asdf_yaml_tree_nested_dict():
    class NestedTestModel(AsdfPydanticModel):
        nested: dict

    model = NestedTestModel(nested={"foo": "bar"})
    assert model.asdf_yaml_tree() == {"nested": {"foo": "bar"}}


def test_asdf_yaml_tree_nested_basemodel():
    class TestModel(BaseModel):
        foo: str

    class NestedTestModel(AsdfPydanticModel):
        nested: TestModel

    model = NestedTestModel(nested=TestModel(foo="bar"))
    assert model.asdf_yaml_tree() == {"nested": {"foo": "bar"}}


def test_asdf_yaml_tree_nested_asdf_pydantic_model():
    class TestModel(AsdfPydanticModel):
        foo: str

    class NestedTestModel(AsdfPydanticModel):
        nested: TestModel

    model = NestedTestModel(nested=TestModel(foo="bar"))
    assert model.asdf_yaml_tree() == {"nested": TestModel(foo="bar")}


########################################################################################
# TAGS
########################################################################################
@pytest.mark.parametrize(
    "tag",
    (
        "asdf://asdf-pydantic/test/tags/",
        pytest.param(
            TagDefinition("asdf://asdf-pydantic/tags/test-0.0.1"),
            marks=pytest.mark.xfail(
                reason="Tag definition without schema URIs not supported"
            ),
        ),
        TagDefinition(
            "asdf://asdf-pydantic/tags/test-0.0.1",
            schema_uris=["asdf://asdf-pydantic/test/schemas/test-0.0.1"],
        ),
    ),
)
def test_can_get_tag_definition(tag):
    class TestModel(AsdfPydanticModel):
        _tag = tag

    tag_definition = TestModel.get_tag_definition()
    assert isinstance(tag_definition, TagDefinition)
    assert tag_definition.schema_uris


@pytest.mark.parametrize(
    "tag",
    (
        "asdf://asdf-pydantic/test/tags/",
        TagDefinition("asdf://asdf-pydantic/tags/test-0.0.1"),
        TagDefinition(
            "asdf://asdf-pydantic/tags/test-0.0.1",
            schema_uris=["asdf://asdf-pydantic/test/schemas/test-0.0.1"],
        ),
    ),
)
def test_can_get_tag_uris(tag):
    class TestModel(AsdfPydanticModel):
        _tag = tag

    assert TestModel.get_tag_uri()


########################################################################################
# GENERATED SCHEMA
########################################################################################
def test_generated_schema_keys_in_order():
    class TestModel(AsdfPydanticModel):
        _tag = "asdf://asdf-pydantic/tags/test-0.0.1"
        foo: str

    assert list(yaml.safe_load(TestModel.model_asdf_schema()).keys()) == [
        "$schema",
        "id",
        "title",
        "type",
        "properties",
        "required",
    ]


def test_generated_schema_id_uses_tag_in_pattern():
    class TestModel(AsdfPydanticModel):
        _tag = "asdf://asdf-pydantic/tags/test-0.0.1"

    assert (
        yaml.safe_load(TestModel.model_asdf_schema())["id"]
        == "asdf://asdf-pydantic/tags/test-0.0.1/schema"
    )
