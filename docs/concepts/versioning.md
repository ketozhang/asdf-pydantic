# Versioning

asdf-pydantic provides a few tools and recommendations to help propagate versions of your models to ASDF extensions, tags, schemas, etc. following the guidelines in the ASDF documentation on [versioning extensions](
https://www.asdf-format.org/projects/asdf/en/stable/asdf/extending/extensions.html#versioning-extensions).

## Use the package version

asdf-pydantic recommends maintainers to use the versioning scheme of their Python package for all versioned resources in ASDF.

```python
__version__ = ...

class MyModel(AsdfPydanticModel):
    _tag = f"asdf://asdf-pydantic/examples/tags/mymodel-{__version__}"


class MyModel(AsdfPydanticModel):
    _tag = TagDefinition(
        tag=f"asdf://asdf-pydantic/examples/tags/mymodel-{__version__}",
        schema_uri=f"asdf://asdf-pydantic/examples/schemas/mymodel-{__version__}",
    )


class MyExtension(Extension):
    extension_uri = f"asdf://asdf-pydantic/examples/extensions/test-extension-{__version__}"
```

:::{admonition} Ways to construct `__version__`
:class: dropdown

### Version from a version module
A version module is a de-facto standard for Python packages to define their version in a single location. This can be done by creating a `version.py` file in your package that contains the version in the variable, `__version__`.

Certain tools like [setuptools-scm](https://github.com/pypa/setuptools-scm) or [hatch-vcs](https://github.com/pypa/setuptools-scm) can automatically generate this module.

```python
# mypackage/model.py
from mypackage.version import __version__
```

### Version from the package metadata
Using `importlib` the version of the distribution package can be obtained. Here we use the magic variable `__package__` inside its package module to get the package name and then retrieve the version from the package metadata.

```python
# mypackage/model.py
import importlib

__version__ = importlib.import_module(__package__).__version__
```
:::
