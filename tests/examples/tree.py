from __future__ import annotations

from pydantic import BaseModel

from asdf_pydantic import AsdfPydanticModel


class Node(BaseModel):
    child: Node | None = None


class AsdfTreeNode(Node, AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/tree-node-1.0.0"

    child: AsdfTreeNode | Node | None = None
