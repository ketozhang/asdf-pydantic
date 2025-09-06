# Fields

Fields are the attributes of your model. asdf-pydantic focuses on implementing fields that are compatible with ASDF. A compatible field is one that can be serialized to ASDF file and deserialized back to original data type.


- ASDF standard fields

  A standard ASDF type from the [ASDF's standard schema definitions](https://asdf-standard.readthedocs.io/en/latest/schemas/index.html#asdf-standard-schema-definitions).

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

  These include many Python standard types such as `int`, `float`, `str`, `bool`, `list`, `dict`, and more complex types like `datetime.datetime`, `numpy.ndarray`, etc.

- 3rd party ASDF fields

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

  Here, the astropy `u.Quantity` data type is compatible with ASDF if the package `asdf-astropy` is installed.

- A subtype of [`AsdfPydanticModel`](#asdf_pydantic.model.AsdfPydanticModel):

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
  Because both `Office` and `Employees` are [`AsdfPydanticModel`](#asdf_pydantic.model.AsdfPydanticModel), both fields are tagged.

- A subtype of [`pydantic.BaseModel`](https://docs.pydantic.dev/usage/models/)

  If all fields of the Pydantic model are ASDF-compatible, then the model itself is also ASDF-compatible.

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
    employees:         # NOTE: ASDF tag is not present here
      names: ["alice", "bob", "charlie"]
  ```
  Notice the `.office.employees` field is not a tagged because `Employees`, but it is still ASDF-compatible because all its fields are ASDF-compatible.

## ASDF Field Schema

All tagged fields in ASDF must have a schema associated for ASDF to perform validation when loading the file. asdf-pydantic can figure out the correct schema for all ASDF standard fields and [`AsdfPydanticModel`](#asdf_pydantic.model.AsdfPydanticModel) fields, but 3rd party fields may need a direct reference to associate with the correct schema.

### Associating a schema to a field

Any field may be have a schema associated or overwritten by type annotating the field with an [`AsdfTag`](#asdf_pydantic.schema.AsdfTag) or [`withAsdfSchema`](#asdf_pydantic.schema.WithAsdfSchema).

```{autodoc2-object} asdf_pydantic.schema.AsdfTag
render_plugin = "myst"
no_index = true
```

```{autodoc2-object} asdf_pydantic.schema.WithAsdfSchema
render_plugin = "myst"
no_index = true
```

```python
from astropy.units import Quantity
from astropy.time import Time

class PositionInTime(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/position-in-time-1.0.0"

    time: Annotated[Time, AsdfTag("http://stsci.edu/schemas/asdf/time/time-1.2.0")]
    x: Annotated[Quantity[u.m], AsdfTag("http://stsci.edu/schemas/asdf/quantity/quantity-1.0.0")]
    y: Annotated[Quantity[u.m], AsdfTag("http://stsci.edu/schemas/asdf/quantity/quantity-1.0.0")]
```
