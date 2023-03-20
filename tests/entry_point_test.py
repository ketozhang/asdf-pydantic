from tempfile import NamedTemporaryFile

import asdf

from asdf_pydantic.examples.shapes import AsdfPydanticRectangle


def test_create_asdf_file():
    with NamedTemporaryFile() as tempfile:
        af = asdf.AsdfFile({"rect": AsdfPydanticRectangle(width=42, height=10)})
        af.write_to(tempfile.name)
