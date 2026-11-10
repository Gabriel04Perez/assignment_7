"""Add duration_minutes and weekday feature columns.

duration_minutes is duration_seconds / 60. weekday is the full English
day name of the event's date (Monday, ..., Sunday).

Usage: python src/features.py <transformed csv> <output csv>
"""

import sys
from pathlib import Path

import pandas as pd

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with `duration_minutes` and `weekday` columns added."""
    df = df.copy()
    df["duration_minutes"] = df["duration_seconds"] / 60
    date = pd.to_datetime(df["date"], format="%Y-%m-%d")
    # Map weekday numbers to names directly so the output doesn't depend
    # on the system locale.
    df["weekday"] = date.dt.day_of_week.map(lambda i: WEEKDAYS[i])
    return df


def main() -> None:
    in_path, out_path = sys.argv[1], sys.argv[2]

    df = pd.read_csv(in_path, dtype={"user_id": str})
    features = add_features(df)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(out_path, index=False)
    print(f"features: wrote {len(features)} rows -> {out_path}")


if __name__ == "__main__":
    main()
