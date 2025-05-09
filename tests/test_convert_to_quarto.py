from pathlib import Path

import pytest

from TexSoup import TexSoup
from beamer2qmd.convert_to_quarto import *


@pytest.fixture
def tmp_wrkdir(tmp_path):
  orig = os.getcwd()
  os.chdir(tmp_path)
  yield
  os.chdir(orig)


@pytest.fixture
def figure_png(tmp_wrkdir):
    dir = Path("figures")
    dir.mkdir()
    fig = dir / "figure.png"
    fig.write_text("")
    yield fig.with_suffix("")

def test_parse_include_graphics(figure_png):
    tex = r"""\includegraphics[width=.8\textwidth]{""" + f'{figure_png}' + r"}"
    soup = TexSoup(tex)
    parse_include_graphics(list(soup.children)[0])


def test_parse_slide_notes_only():
    tex = r"""
    \begin{frame}
  \frametitle{First Models}
  \note[item]{They will be brittle - with no flexibility to make them look like the real world}
  \note[item]{Actually, just like this tower of legos, they may be very rectangle.}
  \note[item]{The answer is we made it up!  and we just want to build
    something simple to understand how the bricks fit together}
\end{frame}
    """
    soup = TexSoup(tex)
    expect = """## First Models


::: {.notes}
- They will be brittle - with no flexibility to make them look like the real world
- Actually, just like this tower of legos, they may be very rectangle.
- The answer is we made it up!  and we just want to build
    something simple to understand how the bricks fit together
:::
"""
    assert parse_slide(list(soup.children)[0]).to_md() == expect

def test_parse_slide_single_figure(figure_png):
    tex = r"""
    \begin{frame}
  \frametitle{First Models}
  \note[item]{When we start out, our models are not going to resemble the world at all}
  \note[item]{They will be brittle - with no flexibility to make them look like the real world}
  \note[item]{Actually, just like this tower of legos, they may be very rectangle.}
  \note[item]{You may ask, where did this rectangular distribution come from?}
  \note[item]{The answer is we made it up!  and we just want to build
    something simple to understand how the bricks fit together}
  \centering 
  \includegraphics[width=.8\textwidth]{figures/figure} \\ 
  \footnotesize Image: Hans Schou (CC BY-SA 3.0)
\end{frame}
    """
    soup = TexSoup(tex)
    expect = """## First Models

![](figures/figure.png)


 Image: Hans Schou (CC BY-SA 3.0)


::: {.notes}
- When we start out, our models are not going to resemble the world at all
- They will be brittle - with no flexibility to make them look like the real world
- Actually, just like this tower of legos, they may be very rectangle.
- You may ask, where did this rectangular distribution come from?
- The answer is we made it up!  and we just want to build
    something simple to understand how the bricks fit together
:::
"""
    assert parse_slide(list(soup.children)[0]).to_md() == expect

