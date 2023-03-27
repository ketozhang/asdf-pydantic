from tempfile import NamedTemporaryFile

import asdf

from asdf_pydantic.examples.shapes import AsdfRectangle


def test_create_asdf_file():
    with NamedTemporaryFile() as tempfile:
        af = asdf.AsdfFile({"rect": AsdfRectangle(width=42, height=10)})
        af.write_to(tempfile.name)
