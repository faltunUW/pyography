"""Smoke test: the package installs, imports, and reports the version from pyproject.toml."""

from importlib.metadata import version

import pyography


def test_version_matches_metadata() -> None:
    assert pyography.__version__ == version("pyography")
