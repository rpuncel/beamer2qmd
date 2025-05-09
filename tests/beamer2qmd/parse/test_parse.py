from TexSoup import TexSoup
from beamer2qmd.parse import *

def test_parse_block():
    text = r"""\begin{block}{Definition 1.1.12: \textit{partition}}
    A set of sets $A_{1}, A_{2}, \dots, A_{n}$ is a \textit{partition} of set $S$, if $A_{1}, A_{2}, \dots, A_{n}$ are nonempty and
    pairwise disjoint, and if $S = A_{1} \cup A_{2} 
    \cup \cdots \cup A_{n}$.

  \end{block}
    """
    expect = """::: {.callout-note title="Definition 1.1.12:  _partition_ "}

A set of sets $A_{1}, A_{2}, \dots, A_{n}$ is a _partition_ of set $S$, if $A_{1}, A_{2}, \dots, A_{n}$ are nonempty and
pairwise disjoint, and if $S = A_{1} \cup A_{2} 
\cup \cdots \cup A_{n}$.
  
:::"""
    soup = TexSoup(text)
    parsed = parse_block(list(soup.children)[0])
    assert parsed.to_md() == expect


def test_parse_columns():
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
        \includegraphics[width=\textwidth]{figures/Laplace}
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

::::\
"""
    soup = TexSoup(text)
    parsed = parse_columns(list(soup.children)[0])
    assert parsed.to_md() == expect