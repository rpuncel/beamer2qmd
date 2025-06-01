import os
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

import rich_click as click
import yaml
from TexSoup import TexSoup
from TexSoup.data import TexCmd, TexExpr, TexNode

from beamer2qmd.parse import *

from .nodes import *

# Define the input and output file paths
input_file = "/Users/rpuncel/Workspaces/slides/unit_01/unit_01.tex"
output_file = "/Users/rpuncel/Workspaces/slides/unit_01/unit_01_converted.qmd"


class QmdHeader(TypedDict):
    title: str
    subtitle: str
    author: str
    institute: str
    format: dict


def get_doc_metadata(doc):
    print(doc.title.string)
    return QmdHeader(
        title=str(doc.title.string),
        subtitle=str(doc.subtitle.string),
        author=str(doc.author.string),
        institute=str(doc.institute.string),
        format={"revealjs": {"show-notes": True}},
    )


class Section:

    def __init__(self, title: str):
        self.title = title

    def to_md(self):
        return f"# {self.title}"


class Slideshow:

    def __init__(self):
        self.title = ""
        self.subtitle = ""
        self.authors = list()
        self.sections_and_slides = list()

    def to_md(self):
        return "\n\n".join(
            [f"# {self.title}", *[s.to_md() for s in self.sections_and_slides]]
        )


def convert_doc(doc):
    root = doc.find("document")
    slideshow = Slideshow()
    for child in root.children:
        if child.name == "section":
            slideshow.sections_and_slides.append(Section(child.string))
        elif child.name == "frame":
            slide = parse_slide(child)
            if slide is None:
                continue
            slideshow.sections_and_slides.append(slide)
    return slideshow


def open_tex(input_file):
    # Read the LaTeX file
    tex_content = input_file.read()

    # Parse the LaTeX content using text2py
    parsed_content = TexSoup(tex_content)
    return parsed_content


def write_qmd(qmd_content, metadata, output_path):
    with open(output_path, "w") as file:
        file.write("---\n")
        yaml.dump(metadata, file)
        file.write("---\n\n")
        file.write(qmd_content)


def inpath_to_output(path):
    inpath = Path(path)
    return inpath.with_suffix(".qmd")


@click.command()
@click.argument("beamer_file", type=click.File(), required=True)
def main(beamer_file):

    # Start writing the Quarto markdown content
    parsed_content = open_tex(beamer_file)
    doc = parsed_content
    metadata = get_doc_metadata(doc)
    qmd_content = convert_doc(parsed_content).to_md()

    outpath = inpath_to_output(beamer_file.name)

    # Write the Quarto markdown file
    write_qmd(qmd_content, metadata, outpath)
    print(f"wrote out {outpath}")


if __name__ == "__main__":

    main()
