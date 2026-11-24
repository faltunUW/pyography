# Journal

A log of the build, step by step: what happened, what I learned, and my quiz answers. The end of this file
collects interview material (STAR stories and likely Q&As).

---

## 2026-11-23 · Planning

- Settled every open question (Q17–Q30) in four short rounds. The full answers are in [`PLAN.md`](PLAN.md) §2–§3.
- **Catch during planning:** the draft API mixed `validate_coords(lat, lon)` with `utm_crs_for(lon, lat)`.
  We standardized on `lat, lon` everywhere (DECISIONS D-03). This is exactly the kind of inconsistency that
  causes the most common GIS bug.
- Logged in to GitHub with `gh auth login`.

## 2026-11-23 · Step 1: Scaffold

**What was built:** `uv init --lib` skeleton, a hand-written `pyproject.toml` (metadata, dependencies, ruff,
pytest), MIT license, `.gitignore`, a smoke test, and the four docs files. `PLAN.md` moved into `docs/`.

**Decisions made during this step:**
- Q31 → Python **3.11–3.14**, because 3.10 reached end of life in Oct 2026 (D-12).
- Q32 → GeoPandas is **required**, not optional (D-13).
- Dependencies use lower bounds only; `uv.lock` is committed (D-14).
- Commits use the GitHub noreply email, so no personal email is exposed in public history (D-18).

**Published:** [github.com/faltunUW/pyography](https://github.com/faltunUW/pyography) and the hub
[github.com/faltunUW/geoai-portfolio](https://github.com/faltunUW/geoai-portfolio), both public.

**Study:** [`WALKTHROUGH.md` → Step 1](WALKTHROUGH.md#step-1--scaffold)

### Hands-on: Step 1

Step 1 was built before the hands-on loop existed, so there's no prediction for it. Do these in your own
terminal, from the `01-pyography` folder.

**A. Run the commands.** Run each one and note what it prints.

```powershell
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

> *What did you see?*

**B. Break it, read the error, fix it.** Make each change, run the command, read the error, then undo the change.

1. In `src/pyography/__init__.py`, change `version("pyography")` to `version("pyograpy")` (a typo). Run
   `uv run pytest`. Which exception do you get, and on which line?
2. In `tests/test_package.py`, swap the order of the two `import` lines. Run `uv run ruff check .`. Which rule
   code complains? Then run `uv run ruff check . --fix` and see what it does.

> *What did you find?*

**C. Write a test.** Add a second test to `tests/test_package.py`:

> `pyography.__version__` should look like a release number: three whole numbers separated by dots, like `0.1.0`.

Hint: `"0.1.0".split(".")` gives `["0", "1", "0"]`, and `"7".isdigit()` is `True`. Run `uv run pytest` until
both tests pass. Then commit it yourself:

```powershell
git add tests/test_package.py
git commit -m "test: check version format"
git push
```

### Quiz: Step 1

Answer in your own words, below each question. Short answers are fine.

1. Why does pyography put its code in `src/pyography/` instead of `pyography/` at the top level? Describe the
   bug this prevents.

   > *Your answer:*

2. `pyproject.toml` says `numpy>=1.26`, but `uv.lock` pins `numpy==2.5.5`. Why have both, and who uses each one?

   > *Your answer:*

3. Where is the version number `0.1.0` written, and how does `pyography.__version__` get it? Why not just
   write `__version__ = "0.1.0"` in `__init__.py`?

   > *Your answer:*

4. What's the difference between `dependencies` and the `dev` dependency group? What would go wrong if
   `pytest` were listed under `dependencies`?

   > *Your answer:*

5. Someone on Python 3.10 runs `pip install pyography`. What happens, and which line causes it?

   > *Your answer:*

6. **Explain this line in your own words**, as you would to an interviewer. What does each of the three
   options do, and why would a project want them?

   ```toml
   addopts = ["-ra", "--strict-markers", "--strict-config"]
   ```

   > *Your answer:*

**Feedback:** *(Claude fills this in after you answer)*

---

## Interview material

### STAR stories
*(Written at wrap-up, step 12.)*

### Likely interview questions
*(Five questions with answers, written at wrap-up.)*
