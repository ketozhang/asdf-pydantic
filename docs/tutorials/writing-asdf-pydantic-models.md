```{currentmodule} asdf_pydantic
```
# Writing ASDF Pydantic models to define tagged objects

The [AsdfPydanticModel](#asdf_pydantic.AsdfPydanticModel) is a class that combines the features of [`pydantic.BaseModel`](https://docs.pydantic.dev/usage/models/) and ASDF to be readily serializable as tagged objects in an ASDF file.

```py
class Rectangle(AsdfPydanticModel):
  _tag = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"

  width: float
  height: float
```

This `Rectangle` model will be referenced in ASDF's YAML file as `!rectangle-1.0.0` specified by the `_tag` field. The `_tag` should be globally unique ASDF tag (see [naming best practices](https://asdf.readthedocs.io/en/stable/asdf/extending/uris.html#tags)) and should uniquely identify which ASDF Pydantic model it corresponds to. This model contains two fields: `width` and `height` and their field type are both `float`.

## Field Types

### ASDF field type
An ASDF field type is a Python type that can be serialized to a YAML file. These include Python types that are...

- Already implemented in [ASDF's standard schema definitions](https://asdf-standard.readthedocs.io/en/latest/schemas/index.html#asdf-standard-schema-definitions).

  ```py
  class Employees(AsdfPydanticModel):
      _tag = "asdf://asdf-pydantic/examples/tags/employees-1.0.0"
      last_updated: datetime.datetime
      names: list[str]
  ```


  ```yaml
  example: !<asdf://asdf-pydantic/examples/tags/employees-1.0.0>
    last_updated: !time/time-1.2.0 "2000-12-31T13:05:27.737"
    names: ["alice", "bob", "charlie"]
  ```

- Provided by installed 3rd party ASDF extensions.

  ```py
  from astropy import units as u

  class Rectangle(AsdfPydanticModel):
      _tag = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"

      # Astropy provides u.Quantity and schema
      width: u.Quantity[u.m]
      height: u.Quantity[u.m]
  ```


  ```yaml
  rect: !<asdf://asdf-pydantic/examples/tags/rectangle-1.0.0>
    width: {datatype: float64, unit: !unit/unit-1.0.0 m, value: 1.0}
    height: {datatype: float64, unit: !unit/unit-1.0.0 m, value: 2.0}
  ```

  Here, if `asdf-astropy` is installed, then the `Quantity` type is a valid ASDF tagged.

- Any subtype of [AsdfPydanticModel](#asdf_pydantic.AsdfPydanticModel):

  ```py
  class Employees(AsdfPydanticModel):
      _tag = "asdf://asdf-pydantic/examples/tags/employees-1.0.0"
      names: list[str]

  class Office(AsdfPydanticModel):
      _tag = "asdf://asdf-pydantic/examples/tags/office-1.0.0"

      employees: Employees
  ```


  ```yaml
  office: !<asdf://asdf-pydantic/examples/tags/office-1.0.0>
    employees: !<asdf://asdf-pydantic/examples/tags/employees-1.0.0>
      names: ["alice", "bob", "charlie"]
  ```
  Because both `Office` and `Employees` are [`AsdfPydanticModel`](#asdf_pydantic.AsdfPydanticModel), both fields are tagged.

- A subtype of [`pydantic.BaseModel`](https://docs.pydantic.dev/usage/models/):

  ```py
  from pydantic import BaseModel

  class Employees(BaseModel):
    names: list[str]

  class Office(AsdfPydanticModel):
      _tag = "asdf://asdf-pydantic/examples/tags/office-1.0.0"

      employees: Employees
  ```


  ```yaml
  office: !<asdf://asdf-pydantic/examples/tags/office-1.0.0>
    employees:
      names: ["alice", "bob", "charlie"]
  ```
  Because `Employees` is not an [`AsdfPydanticModel`](#asdf_pydantic.AsdfPydanticModel), its field is not tagged. If it's fields are all recursively serializable, then it becomes an untagged ASDF object.

### Custom field type

You can define your own custom types in any way so that they would satisfy a
[ASDF field type](#asdf-field-type). Here list a few options:

1. Create a tagged ASDF type classically (involves defining a custom ASDF Converter
and extension).
2. Create a tagged ASDF type for composite types (e.g., dict-like, `dataclass`, `TypeDict`, `NamedTuple`), define a [`AsdfPydanticModel`](#asdf_pydantic.model.AsdfPydanticModel) subclass.
3. Create untagged type is not yet supported.
