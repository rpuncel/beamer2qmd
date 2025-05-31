from .node import Node


class UnorderedList:

    def __init__(self, items: list[str | Node], depth=0):
        self.items = items
        self.depth = depth

    def set_depth(self, depth):
        self.depth = depth

    def to_md(self) -> str:
        lines: list[str] = list()
        for item in self.items:
            match item:
                case UnorderedList():
                    item.set_depth(self.depth + 1)
                    lines.append(item.to_md())
                case _:
                    lines.append("  " * self.depth + "- " + str(item))
                    pass

        return "\n".join(lines) + "\n"

    def __str__(self):
        return self.to_md()


class OrderedList:

    def __init__(self, items: list[str]):
        self.items = items

    def to_md(self):
        return (
            "\n".join(
                [f"{i+1}. {str(item).lstrip()}" for i, item in enumerate(self.items)]
            )
            + "\n"
        )

    def __str__(self):
        return self.to_md()
