from .notes import Notes


class Slide:

    def __init__(self, title: str, contents: list, notes: Notes):
        self.title = title
        self.contents = contents
        self.notes = notes

    def to_md(self):
        self._ensure_at_least_one_newline_follows_title()
        return "\n".join(
            [
                f"## {self.title}",
                "\n".join([str(x) for x in self.contents]),
                self.notes.to_md(),
            ]
        )

    def _ensure_at_least_one_newline_follows_title(self):
        if len(self.contents) == 0:
            self.contents.append("")
            return
        if isinstance(self.contents[0], str):
            self.contents[0] = self.contents[0].lstrip()
        else:
            self.contents.insert(0, "")
