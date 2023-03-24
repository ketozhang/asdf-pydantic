# asdf-pydantic


[![PyPI - Version](https://img.shields.io/pypi/v/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)
-----

Create ASDF tags and schemas with *pydantic* models

## Features

- Automatically create [ASDF Converters](https://asdf.readthedocs.io/en/stable/asdf/extending/converters.html)
and [schemas](https://asdf.readthedocs.io/en/stable/asdf/extending/extensions.html#additional-tags) for your tags.
- Serialize custom objects using pydantic's JSON encoder configs.

## Installation

```console
pip install asdf-pydantic
```

## Usage

Define your data model
```py
# mypackage/shapes.py
from asdf_pydantic import AsdfBaseModel


class Rectangle(AsdfBaseModel):
    width: float
    height: float
```

Create your extension specification
```py
# mypackage/extension
from asdf.extension import Extension

from asdf_pydantic.converter import create_converter

class ShapesExtension(Extension):
    extension_uri = "asdf://asdf-pydantic/shapes/extensions/shapes-1.0.0"
    converters = [
        create_converter(
            Rectangle,
            tags=["asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0"],
            types=["mypackage.shapes.Rectangle"],
        )
    ]
    tags = ["asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0"]
```

Install

```py
# main.py
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
