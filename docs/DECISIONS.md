# Decisions

A record of each design decision: what we chose, why, and what we rejected. Newest decisions go at the bottom.
Questions Q17–Q32 refer to the planning rounds in [`PLAN.md`](PLAN.md).

---

### D-01 · Wrap proven libraries; don't reimplement the math (2026-11-23)
- **Decision:** Every function delegates the real computation to PyProj, Shapely or GeoPandas.
- **Why:** Geodesy is full of subtle edge cases (antimeridian, poles, nearly antipodal points). PyProj wraps PROJ
  and GeographicLib, which are tested far more thoroughly than anything we could write in a week. Our value is a
  consistent API, clear errors and tests.
- **Rejected:** Haversine by hand. It assumes a spherical Earth and is off by up to ~0.5% compared with the
  WGS84 ellipsoid.

### D-02 · A bounded API of 6 public functions (2026-11-23)
- **Decision:** `validate_coords`, `to_crs`, `geodesic_distance`, `utm_crs_for`, `trajectory_stats`, plus
  `initial_bearing`, which the user writes.
- **Why:** A small, finished, tested library is a stronger portfolio piece than a large, half-done one. It fits
  the 10–15 hour budget.

### D-03 · Always `lat, lon`, as separate arguments (Q26, 2026-11-23)
- **Decision:** Every function takes `lat, lon` (or `lat1, lon1, lat2, lon2`) as separate scalar-or-array
  arguments. There are no point tuples. The package swaps to `lon, lat` in one place before calling PyProj.
- **Why:** The first draft mixed `validate_coords(lat, lon)` with `utm_crs_for(lon, lat)`, which invites the
  most common GIS bug of all. A tuple like `(47.6, -122.3)` doesn't say which order it's in. Separate arguments
  also vectorize with NumPy for free.
- **Rejected:** `(lon, lat)` order to match GeoJSON and Shapely. That's correct for x/y geometry, but GPS data
  and people say "lat, lon".

### D-04 · SI units everywhere (2026-11-23)
- **Decision:** Meters, seconds and m/s, with the unit written in field names (`total_distance_m`). Bearings are
  in degrees.
- **Why:** One unit system removes a whole class of conversion bugs. Unit suffixes make results
  self-documenting.

### D-05 · Accepted input types (2026-11-23)
- **Decision:** Floats, NumPy arrays and pandas objects. GeoDataFrames are accepted only by `to_crs`.

### D-06 · Messy GPS data in `trajectory_stats` (Q22, 2026-11-23)
- **Decision:** Sort by time. Drop exact duplicates (same time and place) with a warning. Raise on the same time
  at a different place. Raise on missing time or coordinates.
- **Why:** Same time at a different place means infinite speed, so the data is wrong and must not be averaged
  away. Silently dropping missing values hides data problems from the user.

### D-07 · `initial_bearing` returns 0–360°, and NaN for identical points (Q27–Q28, 2026-11-23)
- **Why:** 0–360° clockwise from north matches a compass. Identical points have no direction. NaN keeps a
  million-point array calculation running, where raising would stop it because of one stationary point.

### D-08 · `trajectory_stats` returns a frozen dataclass (Q29–Q30, 2026-11-23)
- **Decision:** `TrajectoryStats(total_distance_m, duration_s, mean_speed_mps, max_speed_mps, n_points)` plus
  `.to_dict()`. Input columns default to `lat`/`lon`/`time` and can be overridden.
- **Rejected:** A plain dict. A typo in a key fails silently or late, and there's no autocomplete.

### D-09 · Prove correctness against external references (2026-11-23)
- **Decision:** `geodesic_distance` is checked against GeographicLib's published test set (≤ 1 mm). `to_crs` is
  checked against direct PyProj calls (≤ 1e-6 m).
- **Why:** Tests that compare our code with our own expectations can share our misunderstanding. An external
  reference can't.

### D-10 · Tooling: uv, ruff, pytest, GitHub Actions (2026-11-23)
- **Why:** These are the current standard Python tools. `uv` replaces pip, venv and pip-tools in one fast tool.
  `ruff` replaces flake8, isort and pyupgrade.

### D-11 · `src/` layout with the `uv_build` backend (step 1, 2026-11-23)
- **Decision:** The code lives in `src/pyography/`, built by `uv_build`, which is uv's default backend.
- **Why:** With a `src/` layout, tests can't accidentally import the local folder instead of the installed
  package. That catches packaging mistakes (a missing file, wrong metadata) before users hit them.
- **Rejected:** `hatchling` or `setuptools`. Both are fine, but `uv_build` needs no extra configuration for a
  pure-Python package.

### D-12 · Support Python 3.11–3.14 (Q31, 2026-11-23)
- **Decision:** `requires-python = ">=3.11"`, and CI tests 3.11, 3.12, 3.13 and 3.14.
- **Why:** Python 3.10 reached end of life in October 2026, and new NumPy releases already require 3.11 or
  newer. 3.14 is the current release.
- **Changed from:** the original plan of 3.10–3.13.

### D-13 · GeoPandas is a required dependency (Q32, 2026-11-23)
- **Why:** It's simpler to install and to explain. Every later portfolio project uses GeoPandas anyway, and it
  installs from prebuilt wheels on Windows.
- **Rejected:** An optional `pyography[geo]` extra. It's lighter, but it adds an import-guard code path that
  needs its own tests.

### D-14 · Lower-bound dependencies, with an exact lockfile committed (step 1, 2026-11-23)
- **Decision:** `pyproject.toml` lists minimums only (`numpy>=1.26`). `uv.lock` pins the exact versions we test
  with, and it's committed.
- **Why:** A library is installed alongside other packages. Upper caps or exact pins would block users'
  environments. The lockfile gives us, and CI, a reproducible development environment.

### D-15 · Releases through TestPyPI, then PyPI with trusted publishing (2026-11-23)
- **Why:** A rehearsal on TestPyPI catches metadata mistakes. Trusted publishing (OIDC from GitHub Actions)
  means no long-lived API token exists that could leak.

### D-16 · A public repo from the first commit, with data never committed (2026-11-23)
- **Decision:** MIT license. Small commits as we go. `data/` is in `.gitignore`, and download scripts fetch the
  data instead.
- **Why:** Commit history shows how the work progressed. Data files bloat git history permanently.

### D-17 · Disclose AI pair-programming (Q20, 2026-11-23)
- **Decision:** The README says the project was developed with Claude Code, and `docs/` documents the
  reasoning.
- **Why:** Being honest up front, plus showing understanding through this file and `JOURNAL.md`, comes across
  better than being asked about it later.

### D-18 · Commit with the GitHub noreply email (step 1, 2026-11-23)
- **Decision:** This repo's git config uses `<id>+faltunUW@users.noreply.github.com`. The first commit was
  re-authored before the first push.
- **Why:** Commit metadata is public forever, and scrapers collect emails from it. GitHub still credits
  noreply commits to the profile.

### D-19 · A hands-on learning loop for every step (Q33, 2026-11-23)
- **Decision:** Besides studying and quizzes, each step now has the user predict the approach first, write
  some of the tests, run the commands themselves, find a planted bug, and explain one key line in their own
  words.
- **Why:** Reading good code builds understanding, but not the ability to write it. Writing tests and fixing
  a real failing test build that skill at low risk, and they fit the 10–15 hour budget.
- **Changed from:** the original loop, where Claude builds and the user studies and takes a quiz.
