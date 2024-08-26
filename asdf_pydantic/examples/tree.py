from __future__ import annotations

from typing import Optional, Union

from pydantic import BaseModel

from asdf_pydantic import AsdfPydanticModel


class Node(BaseModel):
    child: Optional[Node] = None


class AsdfTreeNode(Node, AsdfPydanticModel):
    _tag = "asdf://asdf-pydantic/examples/tags/tree-node-1.0.0"

    child: Optional[Union[AsdfTreeNode, Node]] = None
