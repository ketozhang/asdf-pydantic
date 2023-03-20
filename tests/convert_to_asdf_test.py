from __future__ import annotations

from tempfile import NamedTemporaryFile
from typing import Optional

import asdf
import pydantic
from asdf.extension import Converter, Extension

from asdf_pydantic import AsdfBaseModel


class Node(pydantic.BaseModel):
    child: Optional[Node] = None


class AsdfNode(Node, AsdfBaseModel):
    child: Optional[Node | AsdfNode] = None


class AsdfNodeConverter(Converter):
    tags = ["asdf://example.com/tags/node-1.0.0"]
    types = ["tests.convert_to_asdf_test.AsdfNode"]

    def to_yaml_tree(self, obj: AsdfNode, tag, ctx):
        return obj.asdf_yaml_tree()

    def from_yaml_tree(self, node, tag, ctx):
        return AsdfNode.parse_obj(node)


class MyExtension(Extension):
    extension_uri = "asdf://example.com/extensions/node-1.0.0"
    converters = [AsdfNodeConverter()]
    tags = ["asdf://example.com/tags/node-1.0.0"]


def setup_module():
    asdf.get_config().add_extension(MyExtension())


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
