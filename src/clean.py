"""Clean the raw events data.

Drops rows that have a missing field, an invalid event_type, or a
non-positive duration_seconds, and normalizes timestamps to ISO 8601
(YYYY-MM-DDTHH:MM:SS).

Usage: python src/clean.py <raw csv> <output csv>
"""

import sys
from pathlib import Path

import pandas as pd

VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}

# Timestamp formats that appear in the raw data. Slash dates are
# month/day/year. Fractional seconds are dropped during normalization.
TIMESTAMP_FORMATS = [
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
]

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"


def parse_timestamps(raw: pd.Series) -> pd.Series:
    """Parse timestamps written in any of TIMESTAMP_FORMATS.

    Values that match none of the formats become NaT.
    """
    parsed = pd.Series(pd.NaT, index=raw.index, dtype="datetime64[us]")
    for fmt in TIMESTAMP_FORMATS:
        attempt = pd.to_datetime(raw, format=fmt, errors="coerce")
        parsed = parsed.fillna(attempt)
    return parsed


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Return the valid rows of df, with timestamps normalized."""
    df = df.dropna()

    df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

    duration = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df[(duration > 0) & (duration % 1 == 0)].copy()
    df["duration_seconds"] = duration[df.index].astype(int)

    timestamp = parse_timestamps(df["timestamp"])
    df = df[timestamp.notna()].copy()
    df["timestamp"] = timestamp[df.index].dt.strftime(ISO_FORMAT)

    return df


def main() -> None:
    raw_path, out_path = sys.argv[1], sys.argv[2]

    df = pd.read_csv(raw_path, dtype=str)
    cleaned = clean(df)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(out_path, index=False)
    print(f"clean: kept {len(cleaned)} of {len(df)} rows -> {out_path}")


if __name__ == "__main__":
    main()
