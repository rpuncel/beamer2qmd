class Notes:
    def __init__(self, items: list):
        self.items = items

    def to_md(self):
        if len(self.items) == 0:
            return ""
        bullets = [f"- {item}" for item in self.items]

        return "\n".join(["::: {.notes}\n", *bullets, ":::", ""])
