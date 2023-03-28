# asdf-pydantic


[![PyPI - Version](https://img.shields.io/pypi/v/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)
[![Documentation Status](https://readthedocs.org/projects/asdf-pydantic/badge/?version=latest)](https://asdf-pydantic.readthedocs.io/en/latest/?badge=latest)

Create ASDF tags with *pydantic* models.

<div style="width: 66vw; margin:auto;">

```py
from asdf_pydantic import AsdfPydanticModel

class Rectangle(AsdfPydanticModel):
    width: float
    height: float

# After creating extension and install ...

af = asdf.AsdfFile()
af["rect"] = Rectangle(width=1, height=1)
```

```yaml
#ASDF 1.0.0
#ASDF_STANDARD 1.5.0
%YAML 1.1
%TAG ! tag:stsci.edu:asdf/
--- !core/asdf-1.1.0
asdf_library: !core/software-1.0.0 {
    author: The ASDF Developers,
    homepage: 'http://github.com/asdf-format/asdf',
    name: asdf,
    version: 2.14.3}
history:
  extensions:
  - !core/extension_metadata-1.0.0
    extension_class: asdf.extension.BuiltinExtension
    software: !core/software-1.0.0 {
        name: asdf,
        version: 2.14.3}
  - !core/extension_metadata-1.0.0 {
    extension_class: mypackage.shapes.ShapesExtension,
    extension_uri: 'asdf://asdf-pydantic/shapes/extensions/shapes-1.0.0'}
rect: !<asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0> {
    height: 1.0,
    width: 1.0}
...
```
</div>

## Features

- [x] Create ASDF tag from your *pydantic* models with batteries ([converters](https://asdf.readthedocs.io/en/stable/asdf/extending/converters.html)) included.
- [x] Validates data models as you create them and not only when reading and writing ASDF files.
- [x] All the cool things that comes with *pydantic* (e.g., JSON encoder, Pydantic types)
- [ ] <span style="color: #736f73">Comes with schemas.</span>

## Installation

```console
pip install asdf-pydantic
```

## Usage

Define your data model
```py
# mypackage/shapes.py
from asdf_pydantic import AsdfPydanticModel

class Rectangle(AsdfPydanticModel):
    width: float
    height: float
```

Then create an extension with the converter included with *asdf-pydantic*:
```py
# mypackage/extensions.py
from asdf.extension import Extension
from asdf_pydantic.converter import AsdfPydanticConverter
from mypackage.shapes import Rectangle

AsdfPydanticConverter.register_models(Rectangle)

class ShapesExtension(Extension):
    extension_uri = "asdf://asdf-pydantic/examples/extensions/shapes-1.0.0"
    converters = [AsdfPydanticConverter()]
    tags = [*AsdfPydanticConverter().tags]
```

Install the extension either by entry point specification or add it to
`asdf.get_config()`:

```py
import asdf
from mypackage.extensions import ShapeExtension

asdf.get_config().register_extension(ShapeExtension)

af = asdf.AsdfFile()
af["rect"] = Rectangle(width=1, height=1)
```

---

```{toctree}
:maxdepth: 1
autoapi
```
