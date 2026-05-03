from probability_scale.config import (
    PROBABILITY_TABLE_PATH,
    PROBABILITY_FIGURE_PATH,
)
from probability_scale.plotting import create_probability_scale_plot
from probability_scale.transform import build_probability_table


def run_pipeline() -> None:
    """
    Run the current MVP pipeline.

    The pipeline:
    1. Builds the probability table.
    2. Saves it as a processed CSV file.
    3. Creates the probability scale figure.
    """

    PROBABILITY_TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROBABILITY_FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = build_probability_table()

    df.to_csv(PROBABILITY_TABLE_PATH, index=False)

    create_probability_scale_plot(
        df=df,
        output_path=PROBABILITY_FIGURE_PATH,
    )

    print(f"Saved probability table to: {PROBABILITY_TABLE_PATH}")
    print(f"Saved probability figure to: {PROBABILITY_FIGURE_PATH}")