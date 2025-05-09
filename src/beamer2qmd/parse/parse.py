from beamer2qmd.nodes import *

def parse_columns(root):
    columns: list[Column] = []
    for child in root.children:
        assert child.name == "column"
        idx = child.args[0].string.find("\\textwidth")
        skip = 0
        if idx != -1:
            width_str = child.args[0].string[:idx]
            width = float(width_str)
            width_pct = width * 100
            skip = 2
        columns.append(Column(width_pct, child.contents, skip))
    return Columns(columns)