from dataclasses import dataclass

from .node import Node


@dataclass
class Text(Node):
    text: str
