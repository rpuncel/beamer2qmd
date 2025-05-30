from TexSoup import TexSoup
import pytest

from beamer2qmd.parse.parse import parse


def test_parsing_math_eliminates_whitespace_inside_delimiters():
    text = r"$ ( A \cap B ) $"
    expect = r"$( A \cap B )$"
    soup = TexSoup(text)
    contents = list(soup.contents)[0]
    parsed = parse(contents)
    assert expect == parsed


def test_parse_block():
    text = r"""\begin{block}{Definition 1.1.12: \textit{partition}}
    A set of sets $A_{1}, A_{2}, \dots, A_{n}$ is a \textit{partition} of set $S$, if $A_{1}, A_{2}, \dots, A_{n}$ are nonempty and
    pairwise disjoint, and if $S = A_{1} \cup A_{2} 
    \cup \cdots \cup A_{n}$.

  \end{block}
    """
    expect = """::: {.callout-note title="Definition 1.1.12:  _partition_"}

    A set of sets $A_{1}, A_{2}, \dots, A_{n}$ is a _partition_ of set $S$, if $A_{1}, A_{2}, \dots, A_{n}$ are nonempty and
    pairwise disjoint, and if $S = A_{1} \cup A_{2} \cup \cdots \cup A_{n}$.

  
:::"""
    soup = TexSoup(text)
    parsed = parse(list(soup.children)[0])
    assert parsed.to_md() == expect


def test_parse_columns(figure_png):
    text = r"""
      \begin{columns}
    \begin{column}{0.6\textwidth}
      "Essentially, the theory of probability is nothing but good common
      sense reduced to mathematics. It provides an exact appreciation of
      what sound minds feel with a kind of instinct, frequently without
      being able to account for it.”\\
      - Pierre-Simon Laplace
    \end{column}
    \begin{column}{0.4\textwidth}
      \begin{center}
        \includegraphics[width=\textwidth]{figures/figure}
      \end{center}
    \end{column}
  \end{columns}
  """

    expect = """\
:::: {.columns}

::: {.column width="60%"}

      "Essentially, the theory of probability is nothing but good common
      sense reduced to mathematics. It provides an exact appreciation of
      what sound minds feel with a kind of instinct, frequently without
      being able to account for it.”

      - Pierre-Simon Laplace
:::

::: {.column width="40%"}
![](figures/figure.png)
:::

::::\
"""
    soup = TexSoup(text)
    parsed = parse(list(soup.children)[0])
    assert parsed.to_md() == expect


def test_parse_enumerate():
    text = r"""\begin{enumerate}
\item Putting together statistical models
\item Fitting models to data
\end{enumerate}"""
    expect = r"""1. Putting together statistical models
2. Fitting models to data
"""

    soup = TexSoup(text)
    parsed = parse(list(soup.children)[0])
    assert parsed.to_md() == expect


def test_parse_itemize():

    text = r"""\begin{itemize}
\item  A precise definition of probability
\item  How mathematicians build from a set of axioms to useful properties
\end{itemize}"""
    expect = r"""- A precise definition of probability
- How mathematicians build from a set of axioms to useful properties
"""

    soup = TexSoup(text)
    parsed = parse(list(soup.children)[0])
    assert parsed.to_md() == expect
