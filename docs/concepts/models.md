# Models

## The _tag attribute

The [_tag](#asdf_pydantic.model.AsdfPydanticModel._tag) attribute is used to define the ASDF tag for the model given it a language-agnostic version and a name. It is a string that follows the ASDF URI format or an ASDF `TagDefinition` object.

```python
class MyModel(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/mymodel-1.0.0"

print(MyModel.get_tag_definition())
# TagDefinition(
#     tag="asdf://asdf-pydantic/examples/tags/mymodel-1.0.0",
#     schema_uri="asdf://asdf-pydantic/examples/schemas/mymodel-1.0.0",
# )
```

Notice the schema URI is also defined alongside the tag. If you wish to overwrite this, define your tag with a `TagDefinition` instead.

```python
from asdf.extension import TagDefinition

class MyModel(AsdfPydanticModel):
    _tag = TagDefinition(
        tag=f"asdf://asdf-pydantic/examples/tags/mymodel-1.0.0",
        schema_uri=f"asdf://asdf-pydantic/examples/schemas/foobar-1.0.0",
    )

print(MyModel.get_tag_definition())
# TagDefinition(
#     tag="asdf://asdf-pydantic/examples/tags/mymodel-1.0.0",
#     schema_uri="asdf://asdf-pydantic/examples/schemas/foobar-1.0.0",
# )
```

## ASDF Schema

All [AsdfPydanticModel](#asdf_pydantic.model.AsdfPydanticModel) models have an ASDF schema. Its schema definition (a YAML string) can be obtained by calling [model_asdf_schema()](#asdf_pydantic.model.AsdfPydanticModel.model_asdf_schema) and its URI [get_tag_definition()](#asdf_pydantic.model.AsdfPydanticModel.get_tag_definition).

### Validation
The ASDF schema is used for validation when loading an ASDF file.

## JSON Schema

All [AsdfPydanticModel](#asdf_pydantic.model.AsdfPydanticModel) models have a JSON schema. Its schema definition (a JSON string) can be obtained by calling [model_json_schema()](#asdf_pydantic.model.AsdfPydanticModel).

### JSON Validation
The JSON schema is not used for validation neither in ASDF nor in Pydantic.

## Model Validation

asdf-pydantic provides validation on both directions of serialization and deserialization.

### Validation during deserialization

Deserialization happens when loading an ASDF file into a Python object (e.g., `af.open()`). If the ASDF file contains a tagged object associated with an `AsdfPydanticModel` the validation performed are:


1. ASDF field validation

    All tagged fields in ASDF are validated against its associated ASDF schema.

    :::tip
    To disable this, see [disabling ASDF validation](https://www.asdf-format.org/projects/asdf/en/4.1.0/asdf/config.html#validate-on-read).
    :::

2. Pydantic model validation


    All fields with tag associated with an `AsdfPydanticModel` subtype are validated using Pydantic.

    :::tip
    To disable this, see [disabling Pydantic model validation](https://docs.pydantic.dev/latest/concepts/models/#creating-models-without-validation).
    :::

:::{admonition} ASDF whole file validation
Although not common, some ASDF file may have a schema to validate its whole file and not just the tagged fields contained. File-level validation is performed if a schema is explicitly provided while opening the ASDF file. See [ASDF docs](https://www.asdf-format.org/projects/asdf/en/latest/asdf/features.html#custom-schemas) for more information.
:::

### Validation during serialization

Serialization happens when writing a Python object to an ASDF file (e.g., `af.write_to()`).

Typically, ASDF will not validate the data being written to the ASDF file, but with [AsdfPydanticModel](#asdf_pydantic.model.AsdfPydanticModel) models, Pydantic validation will be performed when upon creating the model instance.

```python
af = AsdfFile({
    "data": MyModel(width=1.0, height=2.0)  # Pydantic validation here
})
af.write_to("data.asdf")  # No ASDF validation here
```

:::tip
To disable Pydantic validation, see [disabling Pydantic model validation](https://docs.pydantic.dev/latest/concepts/models/#creating-models-without-validation).
:::

ASDF does provide a way to validate all tagged fields in the ASDF tree with [AsdfFile.validate()](https://www.asdf-format.org/projects/asdf/en/4.1.0/api/asdf.AsdfFile.html#asdf.AsdfFile.validate)

```python
af = AsdfFile({
    "data": MyModel(width=1.0, height=2.0)  # Pydantic validation here
})
af.validate() # ASDF validation here
af.write_to("data.asdf")  # No ASDF validation here
```


:::{admonition} ASDF whole file validation
Like with deserialization, the whole tree isn't validated by ASDF, just the tagged fields. You may pass in a schema to `AsdfFile.validate()` to validate the whole file.

See [ASDF docs](https://www.asdf-format.org/projects/asdf/en/4.1.0/asdf/extending/schemas.html#testing-validation) for more information.
:::

## A note on modeling ASDF files

asdf-pydantic focuses on modeling fields you'd populate an ASDF file with, but it does not model the entire file itself. This can be illustrated by when attempting to create an ASDF file, the [AsdfPydanticModel](#asdf_pydantic.model.AsdfPydanticModel) describes a key in the tree and not the tree itself.

```python
tree: dict = {
    "data": MyModel(width=1.0, height=2.0),
    "meta": MyMetaModel(author="John Doe", sw_version="1.0.0")
}
af = AsdfFile(tree)
```

*What if you want to model the entire tree with Pydantic?*

It's a very reasonable request to want to mandate your ASDF file must have the fields `data` and `meta` in the root of the ASDF file and those fields. However due to ASDF lacking a method to associate an ASDF file to a specific schema (i.e., all ASDF files are validated against the [core/asdf](https://www.asdf-format.org/projects/asdf-standard/en/latest/schemas/core.html#core-schema) schema), the call to validation and association must be done manually.

```python
import asdf.schema

class MyAsdfFileModel(AsdfPydanticModel):
    # NOTE: This tag will not replace the core/asdf schema tag
    # It is only used if the model is used as a tagged field.
    _tag = "asdf://asdf-pydantic/examples/tags/my-asdf-file-1.0.0"

    data: MyModel
    meta: MyMetaModel

tree: dict = MyAsdfFileModel(                                # Pydantic validates the entire tree here
    data=MyModel(width=1.0, height=2.0),                     # Pydantic validates the field here
    meta=MyMetaModel(author="John Doe", sw_version="1.0.0")  # Pydantic validates the field here
).model_dump()                                               # For type checking, we keep the tree a dict.

af = AsdfFile(tree)
# At this point, ASDF has not done any validation.
# We must explicitly ask it to...

asdf.schema.validate(af.tree)                                # ASDF validates the tree here

# Notice we didn't pass any schema to `validate()`, that's because
# AsdfPydanticModel has a schema associated with its tag..
# You may explicitly pass in the model schema.
asdf.schema.validate(af.tree, schema=MyAsdfFileModel.model_asdf_schema()) # ASDF validates the tree here
```
