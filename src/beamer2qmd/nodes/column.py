from dataclasses import dataclass

from .node import Node


@dataclass
class Column:

    width: float | None
    contents: list[Node]
    skip: int = 0

    def to_md(self):
        width_specifier = f'width="{self.width:g}%"' if self.width is not None else ""
        lines = []
        lines.append(f"::: {{.column {width_specifier}}}\n")
        for line in self.contents:
            lines.append(str(line).rstrip().replace(r"\\", "\n"))
        lines.append("\n:::\n")
        return "".join(lines)

    def __str__(self):
        return self.to_md()
