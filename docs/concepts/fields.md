# Fields

Fields are the attributes of your model. An ASDF-compatible field is one that can be serialized to an ASDF file and deserialized back to its original Python type.

## Supported Field Types

### ASDF Standard Fields

The [ASDF standard](https://asdf-standard.readthedocs.io/en/latest/schemas/index.html#asdf-standard-schema-definitions) defines schemas for many common Python types. Any field whose type has an ASDF standard schema works out of the box. This includes primitive types (`int`, `float`, `str`, `bool`), collections (`list`, `dict`), and richer types like `datetime.datetime` and `numpy.ndarray`.

```python
import datetime
import numpy as np
from asdf_pydantic import AsdfPydanticModel

class Image(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/image-1.0.0"

    data: np.ndarray
    time: datetime.datetime
    metadata: dict[str, str]

print(
  Image(
    data=np.zeros(100, 100),
    time=datetime.datetime(1970, 1, 1, 0, 0, 0),
    metadata={"filter": "r"},
  )
)
```

```yaml
image: !<asdf://asdf-pydantic/examples/tags/image-1.0.0>
  data: !numpy/ndarray-1.0.0
    datatype: float64
    shape: [100, 100]
  time: !time/time-1.2.0 "1970-01-01T00:00:00"
  metadata: {filter: r}
```

### Third-Party ASDF Fields

Some packages extend ASDF with their own types and schemas. For example, installing [`asdf-astropy`](https://asdf-astropy.readthedocs.io/) adds support for `astropy` types such as `Quantity` and `Time`. Fields using these types are serialized using the schema provided by the third-party package.

```python
from astropy import units as u
from asdf_pydantic import AsdfPydanticModel

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

If asdf-pydantic cannot automatically determine the schema for a third-party type or you want to use a specific ASDF schema, see [Associating a schema to a field](#associating-a-schema-to-a-field).

### AsdfPydanticModel Fields

All types created with this package using [`AsdfPydanticModel`](#asdf_pydantic.model.AsdfPydanticModel) are automatically ASDF-compatible. Both models are written as tagged objects in the ASDF file.

```python
from asdf_pydantic import AsdfPydanticModel

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

Both `Office` and `Employees` carry their own ASDF tags, so each is independently tagged in the serialized file.

### Pydantic BaseModel Fields

A field whose type is a plain [`pydantic.BaseModel`](https://docs.pydantic.dev/usage/models/) subclass (not an `AsdfPydanticModel`) is ASDF-compatible as long as all of its own fields are also ASDF-compatible. The model is serialized as an untagged mapping.

```python
from pydantic import BaseModel
from asdf_pydantic import AsdfPydanticModel

class Employees(BaseModel):
    names: list[str]

class Office(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/office-1.0.0"

    employees: Employees
```

```yaml
office: !<asdf://asdf-pydantic/examples/tags/office-1.0.0>
  employees:  # no ASDF tag — Employees is a plain BaseModel
    names: ["alice", "bob", "charlie"]
```

Because `Employees` is not an `AsdfPydanticModel`, it has no ASDF tag and is written as a plain mapping. Its fields are still serialized correctly because `list[str]` is an ASDF standard type.

## ASDF Field Schema

All tagged fields in ASDF must have a schema associated for ASDF to perform validation when loading the file. asdf-pydantic can figure out the correct schema for all ASDF standard fields and [`AsdfPydanticModel`](#asdf_pydantic.model.AsdfPydanticModel) fields, but 3rd party fields may need a direct reference to associate with the correct schema.

### Associating a schema to a field

Any field may be have a schema associated or overwritten by type annotating the field with an [`AsdfTag`](#asdf_pydantic.schema.AsdfTag) or [`WithAsdfSchema`](#asdf_pydantic.schema.WithAsdfSchema).

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
