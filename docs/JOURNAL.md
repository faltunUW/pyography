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

**Feedback:** *(Claude fills this in after you answer)*

---

## Interview material

### STAR stories
*(Written at wrap-up, step 12.)*

### Likely interview questions
*(Five questions with answers, written at wrap-up.)*
