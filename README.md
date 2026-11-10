# Assignment 7: Reproducible Data Pipelines

A DVC pipeline that cleans `data/raw/events.csv` and adds features, plus a
Marimo notebook that plots the result.

## Pipeline

| Stage       | Script              | Output                        |
|-------------|---------------------|-------------------------------|
| `clean`     | `src/clean.py`      | `data/clean/events.csv`       |
| `transform` | `src/transform.py`  | `data/transformed/events.csv` |
| `features`  | `src/features.py`   | `data/features/events.csv`    |

- **clean** drops rows with a missing field, an `event_type` other than
  `click`, `login`, `purchase`, `scroll` or `view`, or a non-positive
  `duration_seconds`. It also rewrites every timestamp as
  `YYYY-MM-DDTHH:MM:SS`.
- **transform** adds a `date` column (`YYYY-MM-DD`).
- **features** adds `duration_minutes` (`duration_seconds / 60`) and
  `weekday` (`Monday` through `Sunday`).

## Usage

```sh
uv sync
uv run dvc repro                          # build data/clean, data/transformed, data/features
uv run marimo edit notebooks/report.py    # histogram of duration_minutes
```

The raw data is committed to git. DVC tracks every derived file, so they
are not in git.
