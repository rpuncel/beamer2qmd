from typing import Iterator

from TexSoup import TexNode
from TexSoup.data import BracketGroup, TexCmd, TexEnv

from beamer2qmd.nodes import *
from beamer2qmd.nodes.centering import Centering
from beamer2qmd.nodes.node import Node
from beamer2qmd.util.util import find_image_file


def _parse_item(child) -> str:
    result = []
    for i, text in enumerate(child.contents):
        x = parse(text)
        s = str(x).strip()
        result.append(s)
    return " ".join(result).strip()


def parse_list(root: TexNode) -> list[TexNode | str]:
    result: list[TexNode | str] = list()
    for child in root.children:
        if child.name == "itemize":
            result.append(UnorderedList(parse_list(child)))
        elif child.name == "item":
            result.append(_parse_item(child))
    return result


def parse_include_graphics(root):
    filename = root.args[1].string
    path = find_image_file(filename)
    if path is None:
        raise ValueError(f"could not find file path: {filename}")
    return Image(path)


def parse_math(root):
    content_str = ""
    contents = list(root.contents)
    for i, x in enumerate(contents):
        to_add = str(x)
        if i == 0:
            to_add = to_add.lstrip()
        if i == len(contents) - 1:
            to_add = to_add.rstrip()
        if i + 1 < len(contents):
            if isinstance(contents[i], TexNode) and isinstance(
                contents[i + 1], TexNode
            ):
                to_add += " "
        content_str += to_add

    return "".join(
        [
            "$",
            content_str,
            "$",
        ]
    )


def parse_simple(root):
    contents = list()
    if isinstance(root, str):
        return root
    for child in root.contents:
        if hasattr(child, "name"):
            if child.name == "textit":
                contents.append(f"_{str(child.args[0].string)}_")
            elif child.name == "$":
                contents.append(parse_math(child))
            else:
                contents.append(str(child))
        else:
            contents.append(child)
    return " ".join(contents)


parse_line = parse_simple


def parse_centering(root):
    contents = list()
    for i, content in enumerate(root.contents):
        if isinstance(content, str):
            contents.append(content)
        else:
            contents.append(parse_texnode(content))
    return Centering(contents)


ignore_these = {
    "vspace": 0,
}


def parse_texnode(root):
    if root.name == "itemize":
        return UnorderedList(parse_list(root))
    elif root.name == "enumerate":
        return OrderedList(parse_list(root))
    elif root.name == "item":
        return parse_line(root)
    elif root.name == "includegraphics":
        previous_image = parse_include_graphics(root)
        return previous_image
    elif root.name == "textit":
        return f"_{str(root.args[0].string)}_"
    elif root.name == "textbf":
        return f"__{str(root.args[0].string)}__"
    elif root.name == "block":
        return parse_block(root)
    elif root.name == "columns":
        return parse_columns(root)
    elif root.name in ["$", "$$"]:
        return parse_math(root)
    elif root.name in ["\\"]:
        return root
    elif root.name in ["center", "centering"]:
        return parse_centering(root)
    elif root.name in ["footnotesize"]:
        return ""
    elif root.name == "BraceGroup":
        if len(root.contents) > 0:
            return parse(root.contents[0])
    elif root.name in ["paul"]:
        print("paul")
        return root.string
    elif root.name in ignore_these:
        ignore_these[root.name] += 1
        return ""
    else:
        return root


def parse_column_width(root) -> tuple[float, int]:
    assert root.name == "column"
    skip = 0
    width_pct = 100.0
    for cmd in ["\\textwidth", "\\linewidth"]:
        # Not going to worry about translating different commands exactly right
        idx = root.args[0].string.find(cmd)
        if idx != -1:
            width_str = root.args[0].string[:idx]
            width = float(width_str)
            width_pct = width * 100
            skip = 2
            break
    return width_pct, skip


def parse_column_env(root):
    assert root.name == "column"
    width_pct, skip = parse_column_width(root)
    contents = list()
    for i, content in enumerate(root.contents):
        if i < skip:
            continue
        if isinstance(content, str):
            contents.append(content)
        else:
            contents.append(parse_texnode(content))
    return Column(width_pct, contents, skip)


def slurp_column(col: TexCmd, start: int, contents) -> tuple[int, Column]:
    ret_contents = list()
    idx = start
    width_pct, skip = parse_column_width(col)
    while idx < len(contents):
        next = contents[idx]
        if isinstance(next, TexNode) and next.name == "column":
            break
        ret_contents.append(parse(contents[idx]))
        idx += 1
    return (idx - start, Column(width_pct, ret_contents, skip))


def parse_columns(root):
    columns: list[Column] = []
    skip = 0
    if len(root.args) > 0:
        assert len(root.args) == 1
        assert root.args[0] == "[t]", f"it was actually {root.args[0]}"
        skip = 1
    for i in range(len(root.contents)):
        child = root.contents[i]
        if skip > 0:
            skip -= 1
            continue
        if isinstance(child, TexNode):
            if child.name == "column":
                if isinstance(child.expr, TexEnv):
                    columns.append(parse_column_env(child))
                elif isinstance(child.expr, TexCmd) and child.name == "column":
                    skip, col = slurp_column(child, i + 1, root.contents)
                    columns.append(col)
                    continue
        else:
            raise RuntimeError("wat")

    return Columns(columns)


def parse_block(root):
    block_title_expr = root.args[0]
    title = parse_simple(block_title_expr)
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


def parse_note(note):
    match note.args[0]:
        case BracketGroup():
            return parse(note.args[1])
        case _:
            return parse(note.args[0])


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
                note_items.append(parse_note(child))
            else:
                contents.append(parse_texnode(child))
        else:
            if str(child) == "t":
                continue
            if r"\\" in str(child):
                continue
            elif str(child).startswith("%"):
                continue
            else:
                contents.append(str(child))

    return Slide(title=slide_title, contents=contents, notes=Notes(note_items))


def parse(root):
    if hasattr(root, "name"):
        return parse_texnode(root)
    else:
        return str(root)
