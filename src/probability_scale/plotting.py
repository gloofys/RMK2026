from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


REQUIRED_COLUMNS = {
    "event",
    "category",
    "probability",
    "one_in_x",
    "probability_type",
    "interpretation",
    "source_name",
    "source_url",
    "notes",
}


def format_one_in_x(value: float) -> str:
    """
    Format the one_in_x value for plot labels.

    Examples:
    - 3.33 becomes "1 in 3.33"
    - 12.5 becomes "1 in 12.5"
    - 100 becomes "1 in 100"
    """

    if value >= 100:
        return f"1 in {value:,.0f}"

    if value >= 10:
        return f"1 in {value:.1f}"

    return f"1 in {value:.2f}"


def validate_probability_table(df: pd.DataFrame) -> None:
    """
    Validate that the probability table contains all required columns.
    """

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def create_probability_scale_plot(df: pd.DataFrame, output_path: Path) -> None:
    """
    Create a horizontal log-scale probability plot.

    Parameters
    ----------
    df:
        Processed probability table.
    output_path:
        Path where the generated plot will be saved.
    """

    validate_probability_table(df)

    df = df.sort_values("probability", ascending=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.scatter(df["probability"], df["event"])

    for _, row in df.iterrows():
        label = format_one_in_x(row["one_in_x"])

        ax.text(
            row["probability"],
            row["event"],
            f"  {label}",
            va="center",
            fontsize=8,
        )

    ax.set_xscale("log")
    ax.set_xlabel("Probability, log scale")
    ax.set_ylabel("")
    ax.set_title(
        "Probability Scale of Estonia:\n"
        "From daily births to rare crisis alerts and forest fires"
    )

    ax.grid(True, axis="x", linestyle="--", linewidth=0.5)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def create_probability_scale_plot_from_csv(
    input_path: Path,
    output_path: Path,
) -> None:
    """
    Read a processed probability CSV file and create the probability scale plot.
    """

    df = pd.read_csv(input_path)
    create_probability_scale_plot(df, output_path)