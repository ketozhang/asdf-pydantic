# asdf-pydantic

[![PyPI - Version](https://img.shields.io/pypi/v/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asdf-pydantic.svg)](https://pypi.org/project/asdf-pydantic)
[![Documentation Status](https://readthedocs.org/projects/asdf-pydantic/badge/?version=latest)](https://asdf-pydantic.readthedocs.io/en/latest/?badge=latest)

:::{tip}
For v1, see [https://asdf-pydantic.readthedocs.io/en/v1/](https://asdf-pydantic.readthedocs.io/en/v1/)
:::

<div style="width: 33vw; min-width: 50em; max-width: 70em; margin:auto;">

Type-validated scientific data serialization with [*ASDF*](https://asdf.readthedocs.io/en/stable/) and [*Pydantic*](https://pydantic-docs.helpmanual.io/) models

```py
import asdf
from asdf_pydantic import AsdfPydanticModel

class Rectangle(AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"

    width: float
    height: float

# After creating extension and install ...

af = asdf.AsdfFile()
af["rect"] = Rectangle(width=1, height=1)
```


<details>
<summary><b>ASDF File</b></summary>

```py
print(af.dumps())
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

</details>

<details>
<summary><b>ASDF Schema</b></summary>

```py
print(af["rect"].model_asdf_schema())
```


```yaml
%YAML 1.1
---
$schema: http://stsci.edu/schemas/asdf/asdf-schema-1.0.0
id: asdf://asdf-pydantic/examples/tags/rectangle-1.0.0/schema
title: Rectangle
type: object
properties:
  width:
    title: Width
    type: number
  height:
    title: Height
    type: number
required:
- width
- height
```




</details>

<details>
<summary><b>JSON Schema</b></summary>

```py
print(af["rect"].model_json_schema())
```

```yaml
{
    "properties": {
        "width": {
            "title": "Width",
            "type": "number"
        },
        "height": {
            "title": "Height",
            "type": "number"
        }
    },
    "required": [
        "width",
        "height"
    ],
    "title": "Rectangle",
    "type": "object"
}
```

</details>

</div>

## Features

- [x] Create ASDF tag from your *pydantic* models with batteries ([converters](https://asdf.readthedocs.io/en/stable/asdf/extending/converters.html)) included
- [x] Automatically generate ASDF schemas-- [x] Validate data models as you create them, and not only when reading and writing ASDF files
- [x] Preserve Python types when deserializing ASDF filesA- [x] All the benefits of *pydantic* (e.g., JSON encoder, JSON schema, Pydantic types).llation

```sh
pip install asdf-pydantic
```

## Usage

Define youDefine your data model with `AsdfPydanticModel`. For *pydantic* fans, this haseall the features of *pydantic's* BaseModel.mypackage/shapes.py
from asdf_from asdf_pydantic import AsdfPydanticModelctclass Rectangle(AsdfPydanticModel):=    _tag = "asdf://asdf-pydantic/examples/tags/rectangle-1.0.0"h:    width: Annotated[.        u.Quantity[u.m], AsdfTag("tag:stsci.edu:asdf/core/unit/quantity-1.*")     ]t    height: Annotated[.        u.Quantity[u.m], AsdfTag("tag:stsci.edu:asdf/core/unit/quantity-1.*")
    ] ```atThen create an extension with the converter included with *asdf-pydantic*:my```pyg# mypackage/extensions.py.from asdf.extension import Extension_from asdf_pydantic.converter import AsdfPydanticConvertercfrom mypackage.shapes import Rectangler converter = AsdfPydanticConverter().converter.add_models(Rectangle)apclass ShapesExtension(Extension):s    extension_uri = "asdf://asdf-pydantic/examples/extensions/shapes-1.0.0"r    converters = [converter]=    tags = [*converter.tags]r```urAfter your extension is installed with either the entrypoint method or temporarilyfwith `asdf.get_config()`:po```pydimport asdfcfrom mypackage.extensions import ShapeExtension_casdf.get_config().add_extension(ShapesExtension())f.af = asdf.AsdfFile()]af["rect"] = Rectangle(width=1, height=1)n
# Write(af.write_to("shapes.asdf")

# Read back and validate
with asdf.open("shapes.asdf", "rb") as af:
    print(af["rect"])
```sh---ax```sh::maxdepth: 1omodel:autoapio
