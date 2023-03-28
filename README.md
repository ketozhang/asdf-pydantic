# asdf-pydantic


[![PyPI - Version](https://img.shields.io/pypi/v/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)
-----

Create ASDF tags with *pydantic* models.

## Features

- [x] Create ASDF tag from your *pydantic* models with batteries ([converters](https://asdf.readthedocs.io/en/stable/asdf/extending/converters.html)) included.
- [x] Validates data models as you create them and not only when reading and writing ASDF files.
- [x] All the cool things that comes with *pydantic* (e.g., JSON encoder, Pydantic types)
- <span style="color: #736f73">Comes with schemas.</span>

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

Create your extension specification
```py
# mypackage/extensions.py
from asdf.extension import Extension

from asdf_pydantic.converter import register_models_to_converter

AsdfPydanticConverter.register_models(AsdfRectangle)

class ShapesExtension(Extension):
    extension_uri = "asdf://asdf-pydantic/examples/extensions/shapes-1.0.0"
    converters = [AsdfPydanticConverter()]
    tags = [*AsdfPydanticConverter().tags]
```

Install

```py
# main.py
import asdf
from mypackage.shapes import Rectangle
from mypackage.extensions import ShapeExtension

asdf.get_config().add_extension(ShapeExtension())

af = asdf.AsdfFile(
    {
        "toybox": [
            Rectangle(width=1, height=1),
            Rectangle(width=2, height=3),
        ]
    }
)

with open("shape.asdf") as f:
    af.write_to(f)

```

```yaml
#ASDF 1.0.0
#ASDF_STANDARD 1.5.0
%YAML 1.1
%TAG ! tag:stsci.edu:asdf/
--- !core/asdf-1.1.0
asdf_library: !core/software-1.0.0 {author: The ASDF Developers, homepage: 'http://github.com/asdf-format/asdf',
  name: asdf, version: 2.14.3}
history:
  extensions:
  - !core/extension_metadata-1.0.0
    extension_class: asdf.extension.BuiltinExtension
    software: !core/software-1.0.0 {name: asdf, version: 2.14.3}
  - !core/extension_metadata-1.0.0 {extension_class: mypackage.shapes.ShapesExtension,
    extension_uri: 'asdf://asdf-pydantic/shapes/extensions/shapes-1.0.0'}
toybox:
- !<asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0> {height: 2.0, width: 1.0}
- !<asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0> {height: 4.0, width: 3.0}
...
```

## License

`asdf-pydantic` is distributed under the terms of the [BSD-3-Clause](./LICENSE) license.
