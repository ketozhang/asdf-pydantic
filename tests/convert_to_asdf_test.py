from __future__ import annotations

from tempfile import NamedTemporaryFile

import asdf

from asdf_pydantic.examples.extensions import ExampleExtension
from asdf_pydantic.examples.tree import AsdfNode, Node


def setup_module():
    asdf.get_config().add_extension(ExampleExtension())


def test_asdf_node_root_is_AsdfNode():
    node = AsdfNode()
    af = asdf.AsdfFile({"node": node})
    with NamedTemporaryFile() as tempfile:
        af.write_to(tempfile.name)
        with asdf.open(tempfile.name) as ff:
            assert isinstance(ff["node"], AsdfNode)


def test_asdf_node_child_is_AsdfNode():
    node = AsdfNode(child=AsdfNode())
    af = asdf.AsdfFile({"node": node})
    with NamedTemporaryFile() as tempfile:
        af.write_to(tempfile.name)

        with asdf.open(tempfile.name) as ff:
            assert isinstance(ff["node"].child, AsdfNode)


def test_regular_node_child_is_dict():
    node = AsdfNode(child=Node())
    af = asdf.AsdfFile({"node": node})
    with NamedTemporaryFile() as tempfile:
        af.write_to(tempfile.name)

        with asdf.open(tempfile.name) as ff:
            assert isinstance(ff["node"].child, Node)
