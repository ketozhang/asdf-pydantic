from __future__ import annotations

from asdf_pydantic.examples.tree import AsdfTreeNode, Node


def test_sanity():
    AsdfTreeNode().asdf_yaml_tree() == {"child": None}


def test_should_not_convert_given_child_is_AsdfNode():
    AsdfTreeNode(child=AsdfTreeNode()).asdf_yaml_tree() == {"child": AsdfTreeNode()}


def test_should_convert_given_child_is_Node():
    AsdfTreeNode(child=Node()).asdf_yaml_tree() == {"child": {"child": None}}


def test_given_mix_child_is_mix_of_AsdfNode_and_Node():
    assert AsdfTreeNode(child=AsdfTreeNode(child=Node())).asdf_yaml_tree() == {
        "child": AsdfTreeNode(child=Node())
    }

    assert AsdfTreeNode(child=Node(child=AsdfTreeNode())).asdf_yaml_tree() == {
        "child": {"child": {"child": None}}
    }
