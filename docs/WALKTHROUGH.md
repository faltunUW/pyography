# Walkthrough

A study guide to the code, one section per build step. Each section explains **why** things are built the
way they are, which lines matter most, the concepts behind them, and where to read more.

---

## Step 1 · Scaffold

**Goal:** an empty but real Python package. It can be installed, imported, linted and tested, so every later
step only adds code and never fights setup problems.

### The files

```
01-pyography/
├── pyproject.toml        # the one config file: metadata, dependencies, build, ruff, pytest
├── uv.lock               # exact versions of every package we develop with (generated; committed)
├── .python-version       # tells uv which Python to use locally (3.13)
├── .gitignore            # what git must never track
├── LICENSE               # MIT
├── README.md             # the front page on GitHub and PyPI
├── src/pyography/
│   ├── __init__.py       # makes the folder a package; defines __version__
│   └── py.typed          # empty marker: "this package ships type hints"
├── tests/
│   └── test_package.py   # smoke test
└── docs/                 # PLAN, DECISIONS, JOURNAL, this file
```

### Concept 1: the `src/` layout

The package lives in `src/pyography/`, not in `pyography/` at the top level. Why?

When you run Python from the project folder, the current directory is on the import path. With a flat layout,
`import pyography` in a test would pick up the **local folder**, even if the installed package is broken, for
example because a file is missing from the build. Tests would pass on your machine and fail for users.

With `src/`, the only way to import `pyography` is to **install it**. `uv sync` installs it in editable mode,
so your edits show up immediately. Tests therefore always exercise the package the way users get it.

📖 [Python Packaging Guide: src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

### Concept 2: `pyproject.toml`, section by section

| Section | What it controls |
|---|---|
| `[project]` | Package metadata: name, version, description, license, Python range, **runtime dependencies**. PyPI shows this. |
| `[project.urls]` | Links shown in the PyPI sidebar |
| `[dependency-groups]` | **Developer-only** tools (pytest, ruff). Users who `pip install pyography` never get these. |
| `[build-system]` | Which tool turns the source into a wheel (`uv_build`) |
| `[tool.ruff]`, `[tool.pytest.ini_options]` | Settings for each tool, kept in the same file |

Key lines to understand:

```toml
requires-python = ">=3.11"
```
pip and uv read this **before** installing. Someone on Python 3.10 gets a resolver error, or an older
compatible release of pyography if one exists, instead of a broken install. See DECISIONS D-12.

```toml
dependencies = ["numpy>=1.26", "pandas>=2.2", ...]
```
These are **lower bounds only**. A library shares an environment with the user's other packages. If we wrote
`numpy==2.5.5`, nobody could install pyography next to a package that needs a different NumPy. See D-14.

📖 [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

### Concept 3: `uv.lock` vs `pyproject.toml`

They answer two different questions:

- `pyproject.toml`: *which versions does pyography work with?* (a range, for users)
- `uv.lock`: *which exact versions did we test with?* (a snapshot, for us and CI)

`uv sync` reads the lockfile, so your laptop and CI get exactly the same environment. The lockfile is **not**
included when users install the package from PyPI.

📖 [uv: Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)

### Concept 4: one place for the version number

```python
from importlib.metadata import version

__version__ = version("pyography")
```

The version is written **only** in `pyproject.toml`. At import time, `importlib.metadata` reads it from the
installed package's metadata. If it were hard-coded in two places, the two copies would eventually disagree.
The smoke test in `tests/test_package.py` checks exactly this connection.

📖 [importlib.metadata](https://docs.python.org/3/library/importlib.metadata.html)

### Concept 5: `py.typed`

This is an empty file, but it matters. [PEP 561](https://peps.python.org/pep-0561/) says type checkers (mypy,
Pyright, your editor) should only trust a package's type hints if this marker exists. Because we write type
hints on every function, users get autocomplete and type checking for free.

### Concept 6: ruff and pytest configuration

**ruff** runs one linter with many rule sets. We enable:
- `E`/`W`/`F`: classic errors (unused imports, undefined names)
- `I`: sorted imports
- `B`: bugbear, which catches likely bugs
- `UP`: modern syntax for Python 3.11+
- `D` with the **Google docstring convention**: every public function must document its arguments, return
  value and errors. This fits step 2 (Contracts), where docstrings come before code.
- `NPY`: NumPy-specific pitfalls
- `RUF`: ruff's own rules

**pytest** options:
- `-ra`: print a summary of skipped and failed tests at the end
- `--strict-markers`: a typo like `@pytest.mark.slwo` fails instead of being silently ignored
- `--strict-config`: same idea for config typos

📖 [Ruff rules](https://docs.astral.sh/ruff/rules/) · [pytest configuration](https://docs.pytest.org/en/stable/reference/customize.html)

### Commands you'll use every step

```powershell
uv sync                  # install or refresh the environment from uv.lock
uv run pytest            # run the tests inside that environment
uv run ruff check .      # lint
uv run ruff format .     # auto-format
```

`uv run` always uses the project's `.venv`, so you never need to "activate" anything.
