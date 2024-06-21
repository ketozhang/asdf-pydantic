from __future__ import annotations

from asdf_pydantic.examples.tree import AsdfNode, Node


def test_sanity():
    AsdfNode().asdf_yaml_tree() == {"child": None}


def test_should_not_convert_given_child_is_AsdfNode():
    AsdfNode(child=AsdfNode()).asdf_yaml_tree() == {"child": AsdfNode()}


def test_should_convert_given_child_is_Node():
    AsdfNode(child=Node()).asdf_yaml_tree() == {"child": {"child": None}}


def test_given_mix_child_is_mix_of_AsdfNode_and_Node():
    assert AsdfNode(child=AsdfNode(child=Node())).asdf_yaml_tree() == {
        "child": AsdfNode(child=Node())
    }

    assert AsdfNode(child=Node(child=AsdfNode())).asdf_yaml_tree() == {
        "child": {"child": {"child": None}}
    }
