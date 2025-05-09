from dataclasses import dataclass

from . import Column


@dataclass
class Columns:
    columns: list[Column]

    def to_md(self):
        content = "\n".join(c.to_md() for c in self.columns)
        return "\n".join([":::: {.columns}\n", content, "::::"])

    def __str__(self):
        return self.to_md()
