class Image:

    def __init__(self, path: str, caption=""):
        self.caption = caption
        self.path = path

    def to_md(self):
        return f"![{self.caption}]({self.path})"

    def __str__(self):
        return self.to_md()
