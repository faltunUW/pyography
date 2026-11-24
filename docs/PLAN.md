# Project 01 — `pyography`: Python Geospatial Utility Package

> **Status:** Building. Step 1 (Scaffold) is done (2026-11-23); see `JOURNAL.md` for the current step.
> Source: `Industry_Portfolio_12_Projects_Learning_Order.pdf`, page 1 of 12 (in the portfolio folder, two levels up from this file).

---

## 1. What this project is

A small, installable Python library that later projects import for common spatial and movement operations.
It **wraps proven libraries** (PyProj, Shapely, GeoPandas) behind a consistent, well-tested API with consistent
CRS handling, units and error messages. It does **not** invent new geometry or projection math.

- **Format:** Reusable open-source package, a bounded MVP with 5 public functions plus 1 written by you.
- **Time budget:** 10–15 hours (about one week at roughly 12 h/week).
- **Roles it targets:** Python Developer, GIS Developer, Geospatial Software Engineer.
- **Reused later by:** Project 4 (hotspots: `utm_crs_for` for distances in meters), Project 9 (routing),
  and Project 12 (integrated app, installed from GitHub/PyPI, not copied).

---

## 2. Settled decisions (2026-11-23)

| # | Decision | Answer |
|---|---|---|
| Scope | Which projects | Only the 12 in the Learning Order PDF. The Catalog PDF ideas are a separate track. |
| Pacing | How we work | **One project at a time.** The user decides when to move on. |
| Who codes | Learning mode | **Claude writes the code; the user studies it** to learn and to prepare for interviews. |
| Repos | Structure | One public GitHub repo per project, plus a hub repo that indexes all 12. |
| Docs | Per-repo documentation | `README.md`, `docs/PLAN.md`, `docs/DECISIONS.md`, `docs/JOURNAL.md` (includes STAR interview stories and 5 likely interview Q&As). |
| Pace | Schedule | About 12 h/week, one project per week, in PDF order. |
| Tooling | Shared stack | `uv`, `ruff`, `pytest`, GitHub Actions CI. Later projects require Python ≥3.12; develop on the local Python 3.13. |
| GitHub | Publishing | Public from the first commit, with small commits as you go. Data stays out of git (download scripts instead). `gh` CLI installed and logged in (verified 2026-11-23). |
| Target role | Emphasis | Geospatial Data Scientist / GeoAI, with data engineering as the backup. |
| Geography | Default city | Seattle, open to revisit later. |
| Name | Package name | **`pyography`**. Checked free on PyPI and TestPyPI on 2026-11-23. (`pytography` and `geomove` are taken.) |
| API | Public functions | The 5 functions in §3 |
| Inputs | Accepted types | Floats, NumPy arrays and pandas DataFrames. GeoDataFrame only in `to_crs`. |
| Validation | How correctness is proven | `geodesic_distance` vs a subset of GeographicLib's published geodesic test set (≤1 mm); `to_crs` vs direct PyProj (≤1e-6 m). CI matrix on Python 3.11–3.14 (settled Q31). |
| Release | Distribution | GitHub release `v0.1.0`; publish to TestPyPI first, then PyPI via GitHub Actions **trusted publishing** (no API tokens). |
| Docs site | API reference | `mkdocs-material` + `mkdocstrings`, hosted on GitHub Pages. |
| Q17 | Build rhythm | One step at a time. Claude stops after each step; the user studies it, takes the quiz, and says "next". |
| Q18 | Study materials | `docs/WALKTHROUGH.md`, one section per module: design reasons, key lines, concepts, official doc links. |
| Q19 | Comprehension checks | 3–5 interview-style questions per step, answered in `JOURNAL.md` with feedback from Claude. The user also writes one function themselves. |
| Q20 | AI disclosure | README line: "Developed with AI pair-programming (Claude Code); design decisions documented in docs/". |
| Q21 | User's own function | `initial_bearing(a, b)`, built on `pyproj.Geod.inv`. The user writes it with guidance. |
| Q22 | Messy data in `trajectory_stats` | Sort by time; drop exact duplicates (same time and place) with a warning; raise on same time with a different place; raise on missing time or coordinates; SI units (m, s, m/s). |
| Q23 | Repo, license, location | GitHub repo `pyography` (matches PyPI), MIT license, built locally in `01-pyography`. |
| Q24 | Example notebook | Seattle Neighborhood Map Atlas: centroid distances, UTM zone pick (10N, EPSG:32610) + `to_crs`, synthetic Capitol Hill → Pike Place walk through `trajectory_stats`. Data fetched by script, never committed. |
| Q25 | Hub repo | Create `geoai-portfolio` at Project 1's first push: a README listing all 12 projects, Project 1 linked, the rest "coming soon". |
| Q26 | Argument order | Always lat, lon as separate arguments (no tuples). Fixes the original `utm_crs_for(lon, lat)` clash. |
| Q27 | Bearing range | 0–360°, clockwise from true north. |
| Q28 | Bearing, identical points | Returns NaN, documented in the docstring. |
| Q29 | Trajectory input | Default columns `lat`, `lon`, `time`; overridable via `lat_col=`, `lon_col=`, `time_col=`; time must be datetime. |
| Q30 | Trajectory output | Frozen `TrajectoryStats` dataclass with unit-suffixed fields and `.to_dict()`. |
| Q31 | Python versions | Support and test 3.11–3.14 (`requires-python = ">=3.11"`). 3.10 reached end of life in Oct 2026. |
| Q32 | GeoPandas | A required dependency, not an optional extra. |

---

## 3. Public API (settled)

| Function | Purpose | Wraps | Key edge cases to test |
|---|---|---|---|
| `validate_coords(lat, lon)` | Reject NaN, None and out-of-range values with clear messages | NumPy | lat = ±90.0001, lon = 180.5, NaN, mixed scalar/array |
| `to_crs(geoms, src, dst)` | Reproject coordinates or a GeoDataFrame | PyProj / GeoPandas | missing source CRS (must raise), axis order (lat/lon vs lon/lat) |
| `geodesic_distance(lat1, lon1, lat2, lon2)` | True distance on the WGS84 ellipsoid, in meters | `pyproj.Geod.inv` | antimeridian (179.9° ↔ -179.9°), poles, identical points, antipodal points |
| `utm_crs_for(lat, lon)` | Choose the correct UTM zone EPSG code for a location | PyProj CRS database | Norway/Svalbard zone exceptions, southern hemisphere, zone boundaries |
| `trajectory_stats(df, lat_col="lat", lon_col="lon", time_col="time")` | Returns a frozen `TrajectoryStats` dataclass: `total_distance_m`, `duration_s`, `mean_speed_mps`, `max_speed_mps`, `n_points`, plus `.to_dict()` | `geodesic_distance` | unsorted times, repeated timestamps, single point, missing values, non-datetime time column |
| *(yours)* `initial_bearing(lat1, lon1, lat2, lon2)` | Compass direction A→B, 0–360° clockwise from true north; NaN for identical points | `pyproj.Geod.inv` + `% 360` | north/south/east/west, identical points |

**Conventions (settled Q26–Q30):**
- Coordinates are always passed **lat, lon**, as separate scalar-or-array arguments (no point tuples). The package
  swaps to lon, lat internally, in one place, before calling PyProj.
- All outputs are in SI units (meters, seconds, m/s); bearings are in degrees.
- `trajectory_stats` requires a real datetime time column and raises a clear error otherwise.

---

## 4. Data

No large data is needed.

- **Synthetic fixtures:** hand-built coordinates and trajectories, including deliberately invalid ones.
- **Reference values:** a small subset of GeographicLib's published geodesic test data, stored in `tests/data/`.
- **One real sample, for the example notebook:** Seattle *Neighborhood Map Atlas Neighborhoods*.
  - 94 polygons, about 2 MB, public domain (ODC PDDL).
  - GeoJSON query:
    `https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/nma_nhoods_sub/FeatureServer/0/query?where=1=1&outFields=*&f=geojson`
  - Download it with a script. Do not commit it.

Full verified source list for all 12 projects: `../../_planning/data-sources-verified-2026-11-23.md`.

---

## 5. Implementation steps (learning order)

Each step follows the same loop (settled, Q17–Q19): **Claude builds → the user reads the code and the
`WALKTHROUGH.md` section → the user asks questions → short interview-style quiz answered in `JOURNAL.md` → next step.**

1. **Scaffold.** `uv init --lib`, `pyproject.toml`, `src/pyography/` layout, ruff, pytest, `.gitignore`, MIT license.
   First commit, then create the GitHub repo.
2. **Contracts.** Write type-hinted signatures and docstrings (inputs, outputs, units, errors) for all functions
   *before* implementing them.
3. **`validate_coords` + tests.**
4. **`geodesic_distance` + `utm_crs_for` + tests**, including the antimeridian and GeographicLib reference tests.
5. **`to_crs` + tests**, covering CRS mismatch and missing-CRS errors.
6. **`trajectory_stats` + tests**, covering the messy-data rules (settled Q22).
7. **User's own feature** (`initial_bearing`, settled Q21): the user writes it with guidance.
8. **CI.** A GitHub Actions matrix (3.11–3.14) that runs lint and tests on every push.
9. **Example notebook** on Seattle data (settled Q24).
10. **Docs site.** mkdocs-material + mkdocstrings deployed to GitHub Pages.
11. **Release.** Clean-venv install check → TestPyPI → tag `v0.1.0` → PyPI (trusted publishing).
12. **Wrap-up.** README polish, `JOURNAL.md` interview section, entry in the hub repo.

---

## 6. Validation and definition of done

- [ ] `pip install pyography` (or install from the wheel) works in a **fresh** virtual environment.
- [ ] All tests pass locally and in CI on Python 3.11–3.14.
- [ ] Geodesic distances match the GeographicLib reference values within 1 mm. Reprojections match PyProj within 1e-6 m.
- [ ] Every invalid input produces a clear, tested error message.
- [ ] API docs are live on GitHub Pages; the example notebook runs top to bottom.
- [ ] `v0.1.0` is tagged and released.
- [ ] `README`, `DECISIONS.md`, `JOURNAL.md` and `WALKTHROUGH.md` are complete; the user has answered every quiz.

---

## 7. Planned repo layout

```
01-pyography/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/pyography/
│   ├── __init__.py
│   ├── validate.py
│   ├── crs.py
│   ├── distance.py
│   └── trajectory.py
├── tests/
│   ├── data/            # GeographicLib reference subset
│   └── test_*.py
├── examples/seattle_demo.ipynb
├── scripts/download_sample.py
├── docs/
│   ├── PLAN.md          # this file, moved here at scaffold time
│   ├── DECISIONS.md
│   ├── JOURNAL.md
│   ├── WALKTHROUGH.md
│   └── api/             # mkdocs pages
└── .github/workflows/   # ci.yml, docs.yml, release.yml
```

---

## 8. Open questions

Ask these **one at a time or in small rounds** in the new chat, before building. The recommended answer comes after each ➡️.

- ~~Q17–Q19~~ ✅ Settled 2026-11-23 (all yes). See §2.
- ~~Q20–Q22~~ ✅ Settled 2026-11-23 (all yes). See §2.
- ~~Q23–Q25~~ ✅ Settled 2026-11-23 (all yes). See §2.
- ~~Q26–Q30~~ ✅ Settled 2026-11-23 (all yes): lat, lon argument order everywhere; bearing 0–360°; NaN bearing
  for identical points; `lat`/`lon`/`time` default columns; frozen `TrajectoryStats` dataclass. See §2–§3.

**No open questions remain.** Finer details (exact error types and messages) are reviewed in build step 2 (Contracts).

**Prerequisite done:** `gh auth status` confirmed the user is logged in to github.com over HTTPS (2026-11-23).

---

## 9. Out of scope

- Custom projection math, or reimplementing geodesic algorithms
- A GeoPandas replacement
- A routing engine
- More than 6 public functions in v0.1.0

---

## 10. Environment facts (checked 2026-11-23)

- Windows 11, Python 3.13.13, `uv` installed, `git` installed (identity already configured), `gh` 2.105.0
  installed and logged in (HTTPS; scopes include `repo` and `workflow`).
- GPU: RTX 2070 Super, 8 GB. Not needed for this project.
