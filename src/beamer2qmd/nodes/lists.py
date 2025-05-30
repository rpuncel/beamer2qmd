class UnorderedList:

    def __init__(self, items: list[str]):
        self.items = items

    def to_md(self):
        return "\n".join([f"- {item.lstrip()}" for item in self.items]) + "\n"

    def __str__(self):
        return self.to_md()


class OrderedList:

    def __init__(self, items: list[str]):
        self.items = items

    def to_md(self):
        return (
            "\n".join([f"{i+1}. {item.lstrip()}" for i, item in enumerate(self.items)])
            + "\n"
        )

    def __str__(self):
        return self.to_md()
