"""pyography: well-tested helpers for coordinates, CRS, geodesic distance and GPS tracks.

The public functions are added one build step at a time (see docs/PLAN.md, section 5).
"""

from importlib.metadata import version

# Read the version from the installed package metadata, so pyproject.toml stays
# the single place where the version number is written.
__version__ = version("pyography")

__all__ = ["__version__"]
