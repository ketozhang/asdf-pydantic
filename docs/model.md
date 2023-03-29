```{currentmodule} asdf_pydantic
```
# ASDF Pydantic Model

The {py:class}`AsdfPydanticModel` is a data model
[`pydantic.BaseModel`](https://docs.pydantic.dev/usage/models/) that is readily
serializable to ASDF.


```py
class Rectangle(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"

    width: float
    height: float
```

`_tag` is a globally unique **ASDF tag** (see [naming best
practices](https://asdf.readthedocs.io/en/stable/asdf/extending/uris.html#tags))
that identifies the data model. This model contains two **fields**: `width` and
`height` and their **field type** are both `float`.

## Field Types

### ASDF field type
An ASDF field type is a Python type that can be serialized to a YAML file. These include Python types that are

- Compatible with [ASDF Standard Schema](https://asdf-standard.readthedocs.io/en/1.0.3/schemas/index.html#asdf-standard-schema-definitions):
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
- ASDF tagged types from ASDF extensions:
  ```py
  from astropy import units as u

  class Rectangle(AsdfPydanticModel):
      _tag = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"

      width: u.Quantity[u.m]
      height: u.Quantity[u.m]
  ```
  ```yaml
  rect: !<asdf://asdf-pydantic/examples/tags/rectangle-1.0.0>
    width: {datatype: float64, unit: !unit/unit-1.0.0 m, value: 1.0}
    height: {datatype: float64, unit: !unit/unit-1.0.0 m, value: 2.0}
  ```
  Here, if `asdf-astropy` is installed, then the `Quantity` type is a valid ASDF tagged.

- A subtype of {py:class}`AsdfPydanticModel`:
  ```py
  class Office(AsdfPydanticModel):
      _tag = "asdf://asdf-pydantic/examples/tags/office-1.0.0"

      employees: Employees
  ```
  ```yaml
  office: !<asdf://asdf-pydantic/examples/tags/office-1.0.0>
    employees: !<asdf://asdf-pydantic/examples/tags/employees-1.0.0>
      names: ["alice", "bob", "charlie"]
  ```
  Because both `Office` and `Employees` are `AsdfPydanticModel`, both are
  referenced by their tags.
- A subtype of `pydantic.BaseModel`:
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
  Because `Employees` is not an `AsdfPydanticModel`, it is not reference by tag.
  If it's fields are all recursively serializable, then it becomes an untagged
  ASDF object.

### Custom field type

You can define your own custom types so that they may satisfy any criteria defined the above section.
You have a few options depending on your type

1. Create a tagged ASDF type classically (involves defining a custom ASDF Converter
and extension).
2. Create a tagged ASDF type for composite types (e.g., dict-like, `dataclass`, `TypeDict`, `NamedTuple`), define a `AsdfPydanticModel`
3. Create untagged type is not yet supported.
