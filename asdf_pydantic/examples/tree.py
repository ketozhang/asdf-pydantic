from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from asdf_pydantic import AsdfBaseModel


class Node(BaseModel):
    child: Optional[Node] = None


class AsdfNode(Node, AsdfBaseModel):
    tag_uri = "asdf://asdf-pydantic/examples/tags/node-1.0.0"
    child: Optional[Node | AsdfNode] = None
