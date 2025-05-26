from dataclasses import dataclass

from .node import Node


@dataclass
class Centering:
    contents: list[Node]
    pass

    def to_md(self):
        lines = []
        for line in self.contents:
            lines.append(str(line).rstrip().replace(r"\\", "\n"))
        return "".join(lines)

    def __str__(self):
        return self.to_md()
