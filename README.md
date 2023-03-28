# asdf-pydantic


[![PyPI - Version](https://img.shields.io/pypi/v/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)

Create ASDF tags with *pydantic* models.

<table>
<tr>
<td>

```py
# mypackage/shapes.py
from asdf_pydantic import AsdfPydanticModel

class Rectangle(AsdfPydanticModel):
    width: float
    height: float

# After creating extension and install ...

af = asdf.AsdfFile(
    {
        "toybox": [
            Rectangle(width=1, height=1),
            Rectangle(width=2, height=3),
        ]
    }
)
```

</td>
<td>

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
toybox:
- !<asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0> {
    height: 1.0,
    width: 1.0}
- !<asdf://asdf-pydantic/shapes/tags/rectangle-1.0.0> {
    height: 3.0,
    width: 2.0}
...
```

</td>
</tr>
</table>

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




Let's take a look at how fast you can create an extension with converters
already included with *asdf-pydantic*.
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

## License

`asdf-pydantic` is distributed under the terms of the [BSD-3-Clause](./LICENSE) license.
