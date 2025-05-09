from dataclasses import dataclass
import os
from typing import TypedDict
import yaml
from TexSoup import TexSoup
from TexSoup.data import TexNode, TexCmd, TexExpr

from .nodes import *
from beamer2qmd.parse import *

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


def open_tex():
    # Read the LaTeX file
    with open(input_file, "r") as file:
        tex_content = file.read()

    # Parse the LaTeX content using text2py
    parsed_content = TexSoup(tex_content)
    return parsed_content


def main():

    # Start writing the Quarto markdown content

    parsed_content = open_tex()
    doc = parsed_content
    metadata = get_doc_metadata(doc)
    qmd_content = "---\ntitle: 'Unit 01 Presentation'\nformat: revealjs\n---\n\n"
    qmd_content = convert_doc(parsed_content).to_md()

    # Write the Quarto markdown file
    with open(output_file, "w") as file:
        file.write("---\n")
        yaml.dump(metadata, file)
        file.write("---\n\n")
        file.write(qmd_content)


def parse_orig(parse_content):

    # Process each parsed element
    for element in parsed_content:
        if element["type"] == "frame":
            frame_content = element["content"]

            # Extract notes
            notes = [note["content"] for note in element.get("notes", [])]

            # Extract images and check their existence
            for image in element.get("images", []):
                image_path = find_image_file(image["path"])
                if image_path:
                    frame_content = frame_content.replace(
                        image["raw"], f"![]({image_path})"
                    )
                else:
                    frame_content = frame_content.replace(image["raw"], "")

            # Replace LaTeX-specific syntax with Markdown/Quarto syntax
            frame_content = frame_content.replace(
                "\\", ""
            )  # Remove remaining LaTeX backslashes

            # Add slide content
            qmd_content += "---\n\n"  # Slide separator
            qmd_content += frame_content + "\n\n"

            # Add notes if present
            if notes:
                qmd_content += "::: {.notes}\n"
                for note in notes:
                    qmd_content += f"- {note.strip()}\n"
                qmd_content += ":::\n\n"


if __name__ == "__main__":
    main()
