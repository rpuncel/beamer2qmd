import os
from pathlib import Path
import pytest


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
