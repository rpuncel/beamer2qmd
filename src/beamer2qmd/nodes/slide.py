from .notes import Notes

class Slide:

    def __init__(self, title: str, contents, notes: Notes):
        self.title = title
        self.contents = contents
        self.notes = notes
    
    def to_md(self):
        return ('\n'.join([
            f'## {self.title}',
            '\n'.join([str(x) for x in self.contents]),
            '',
            self.notes.to_md(),  
        ]))
