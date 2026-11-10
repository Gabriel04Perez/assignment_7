import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return mo, pd, plt


@app.cell
def _(mo):
    mo.md("""
    # Event duration report

    This notebook reads `data/features/events.csv`, the output of the
    `features` stage of the DVC pipeline. Run `uv run dvc repro` first
    if that file doesn't exist yet.
    """)
    return


@app.cell
def _(mo, pd):
    # Resolve the path from the notebook's own location, so it works no
    # matter which directory marimo was started from.
    features_path = mo.notebook_dir() / ".." / "data" / "features" / "events.csv"
    events = pd.read_csv(features_path, dtype={"user_id": str})
    events.head()
    return (events,)


@app.cell
def _(events):
    events["duration_minutes"].describe()
    return


@app.cell
def _(events, plt):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(events["duration_minutes"], bins=40, edgecolor="white")
    ax.set_title(f"Distribution of event durations (n = {len(events)})")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of events")
    fig.tight_layout()
    fig
    return


if __name__ == "__main__":
    app.run()
