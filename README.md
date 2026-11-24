# pyography

Small, well-tested Python helpers for coordinates, coordinate reference systems (CRS), geodesic distance
and GPS trajectories.

pyography wraps proven libraries (PyProj, Shapely, GeoPandas) behind one consistent API: coordinates
are always passed as `lat, lon`, results are always in SI units (meters, seconds, m/s), and bad input
fails with a clear message. It doesn't invent any new geometry or projection math.

> **Status:** early development (v0.1.0 in progress). The functions below are planned, not yet available.

## Planned API (v0.1.0)

| Function | What it does |
|---|---|
| `validate_coords(lat, lon)` | Reject NaN, None and out-of-range coordinates with clear messages |
| `to_crs(geoms, src, dst)` | Reproject coordinates or a GeoDataFrame |
| `geodesic_distance(lat1, lon1, lat2, lon2)` | True distance on the WGS84 ellipsoid, in meters |
| `utm_crs_for(lat, lon)` | The correct UTM zone (EPSG code) for a location |
| `trajectory_stats(df)` | Distance, duration, mean and max speed of a GPS track |
| `initial_bearing(lat1, lon1, lat2, lon2)` | Compass direction from A to B, 0–360° |

## Development

Requires [uv](https://docs.astral.sh/uv/) and Python 3.11 or newer.

```bash
uv sync                 # create .venv and install the package plus dev tools
uv run pytest           # run the tests
uv run ruff check .     # lint
uv run ruff format .    # format
```

## How this was built

Developed with AI pair-programming (Claude Code); design decisions documented in [`docs/`](docs/).
See [`docs/DECISIONS.md`](docs/DECISIONS.md) for the reasoning behind each choice and
[`docs/PLAN.md`](docs/PLAN.md) for the full project plan.

## License

[MIT](LICENSE)
