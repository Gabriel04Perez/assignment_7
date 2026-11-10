"""Add a date column (YYYY-MM-DD) taken from each event's timestamp.

Usage: python src/transform.py <clean csv> <output csv>
"""

import sys
from pathlib import Path

import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with a `date` column added."""
    df = df.copy()
    timestamp = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M:%S")
    df["date"] = timestamp.dt.strftime("%Y-%m-%d")
    return df


def main() -> None:
    in_path, out_path = sys.argv[1], sys.argv[2]

    df = pd.read_csv(in_path, dtype={"user_id": str})
    transformed = transform(df)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    transformed.to_csv(out_path, index=False)
    print(f"transform: wrote {len(transformed)} rows -> {out_path}")


if __name__ == "__main__":
    main()
