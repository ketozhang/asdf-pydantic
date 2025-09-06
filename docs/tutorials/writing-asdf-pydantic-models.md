```{currentmodule} asdf_pydantic
```
# Writing ASDF Pydantic models to define tagged objects

The [AsdfPydanticModel](#asdf_pydantic.model.AsdfPydanticModel) is a class that combines the features of [`pydantic.BaseModel`](https://docs.pydantic.dev/usage/models/) and ASDF to be readily serializable as tagged objects in an ASDF file.

```py
class Rectangle(AsdfPydanticModel):
  _tag = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"

  width: float
  height: float
```

This `Rectangle` model will be referenced in ASDF's YAML file as `!rectangle-1.0.0` specified by the `_tag` field. The `_tag` should be globally unique ASDF tag (see [naming best practices](https://asdf.readthedocs.io/en/stable/asdf/extending/uris.html#tags)) and should uniquely identify which ASDF Pydantic model it corresponds to. This model contains two fields: `width` and `height` and their field type are both `float`.

## Field Types

See [fields](../concepts/fields).
