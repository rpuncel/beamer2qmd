from TexSoup import TexNode

from beamer2qmd.nodes import *
from beamer2qmd.util.util import find_image_file


def parse_list(root):
    result = list()
    for child in root.children:
        if child.name == "itemize":
            result.append(UnorderedList(parse_list(child)))
        elif child.name == "item":
            result.append("".join([text for text in child.text]))
    return result


def parse_include_graphics(root):
    filename = root.args[1].string
    path = find_image_file(filename)
    if path is None:
        raise ValueError(f"could not find file path: {filename}")
    return Image(path)


def parse_simple(root):
    contents = list()
    for child in root.contents:
        if hasattr(child, "name"):
            if child.name == "textit":
                contents.append(f"_{str(child.args[0].string)}_")
            if child.name == "$":
                contents.append(child.string)
            else:
                contents.append(child.string)
        else:
            contents.append(child)
    return contents


def parse_texnode(root):
    if root.name == "itemize":
        return UnorderedList(parse_list(root))
    elif root.name == "enumerate":
        return OrderedList(parse_list(root))
    elif root.name == "includegraphics":
        previous_image = parse_include_graphics(root)
        return previous_image
    elif root.name == "textit":
        return f"_{str(root.args[0].string)}_"
    elif root.name == "block":
        return parse_block(root)
    elif root.name == "columns":
        return parse_columns(root)
    elif root.name in ["$", "$$", "\\"]:
        return root
    elif root.name in ["centering", "footnotesize"]:
        return ""

    else:
        return root


def parse_column(root):
    assert root.name == "column"
    idx = root.args[0].string.find("\\textwidth")
    skip = 0
    if idx != -1:
        width_str = root.args[0].string[:idx]
        width = float(width_str)
        width_pct = width * 100
        skip = 2
    contents = list()
    for i, content in enumerate(root.contents):
        if i < skip:
            continue
        if isinstance(content, str):
            contents.append(content)
        else:
            contents.append(parse_texnode(content))
    return Column(width_pct, contents, skip)


def parse_columns(root):
    columns: list[Column] = []
    for child in root.children:
        columns.append(parse_column(child))
    return Columns(columns)


def parse_block(root):
    block_title_expr = root.args[0]
    title = " ".join(parse_simple(block_title_expr))
    skip = len(list(block_title_expr.contents))
    contents = list()
    for i, content in enumerate(root.contents):
        if i < skip:
            continue
        if isinstance(content, str):
            contents.append(content)
        else:
            contents.append(parse_texnode(content))

    return Block(title, contents)


def parse_slide(frame_root):
    slide_title = ""
    if frame_root.frametitle is not None:
        slide_title = frame_root.frametitle.string
    contents = list()
    note_items = list()
    alls = frame_root.contents
    previous_image = None
    for child in alls:
        if isinstance(child, TexNode):
            if child.name == "frametitle":
                slide_title = child.string
            elif child.name == "note":
                note_items.append(child.args[1].string)
            else:
                contents.append(parse_texnode(child))
        else:
            if r"\\" in str(child):
                continue
            elif str(child).startswith("%"):
                continue
            else:
                contents.append(str(child))

    return Slide(title=slide_title, contents=contents, notes=Notes(note_items))
