
class Block:
    def __init__(self, title, content: list):
        self.title = title
        self.content = content
    
    def to_md(self):
        content = [ str(c).lstrip() for c in self.content ]
        return '\n'.join([
            f'::: {{.callout-note title="{self.title}"}}',
           '\n'.join(content),
            ':::',
        ])
        
    def __str__(self):
        return self.to_md()
        