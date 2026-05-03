from pathlib import Path
from textwrap import fill

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


CATEGORY_COLORS = {
    "Population": "#1f77b4",
    "Traffic": "#d62728",
    "Nature": "#2ca02c",
    "Crisis": "#9467bd",
}


def format_one_in_x(value: float) -> str:
    """
    Format the one_in_x value for plot labels.
    """

    if value >= 100:
        return f"1 in {value:,.0f}"

    if value >= 10:
        return f"1 in {value:.1f}"

    return f"1 in {value:.2f}"


def format_point_label(row: pd.Series) -> str:
    """
    Format point labels.
    """

    return format_one_in_x(row["one_in_x"])


def wrap_event_label(text: str, width: int = 34) -> str:
    """
    Wrap long event labels onto multiple lines.
    """

    return fill(text, width=width)


def validate_probability_table(df: pd.DataFrame) -> None:
    """
    Validate that the probability table contains all required columns.
    """

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def create_probability_scale_plot(df: pd.DataFrame, output_path: Path) -> None:
    """
    Create a readable horizontal probability scale plot.

    The x-axis uses one_in_x instead of raw probability because it is easier
    for readers to understand: larger values mean rarer events.
    """

    validate_probability_table(df)

    df = df.copy()
    df = df.sort_values("one_in_x", ascending=True).reset_index(drop=True)

    df["wrapped_event"] = df["event"].apply(wrap_event_label)
    df["color"] = df["category"].map(CATEGORY_COLORS).fillna("#333333")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig_height = max(6, len(df) * 1.05)
    fig, ax = plt.subplots(figsize=(13, fig_height))

    y_positions = list(range(len(df)))

    min_x = max(df["one_in_x"].min() * 0.8, 1)

    for i, row in df.iterrows():
        ax.hlines(
            y=i,
            xmin=min_x,
            xmax=row["one_in_x"],
            color="#cccccc",
            linewidth=1.2,
            zorder=1,
        )

    ax.scatter(
        df["one_in_x"],
        y_positions,
        s=90,
        c=df["color"],
        zorder=3,
    )

    for i, row in df.iterrows():
        label = format_point_label(row)

        ax.annotate(
            label,
            (row["one_in_x"], i),
            xytext=(8, 0),
            textcoords="offset points",
            va="center",
            fontsize=10,
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["wrapped_event"], fontsize=10)
    ax.invert_yaxis()

    ax.set_xscale("log")
    ax.set_xlim(
    left=max(df["one_in_x"].min() * 0.75, 1),
    right=df["one_in_x"].max() * 1.8,
)
    ax.set_xlabel("Rarity: 1 in X, log scale — farther right means rarer", fontsize=11)

    fig.suptitle(
    "Probability Scale of Estonia\n"
    "Real events from public datasets",
    fontsize=15,
    y=0.96,
)

    tick_values = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    visible_ticks = [
        tick
        for tick in tick_values
        if df["one_in_x"].min() * 0.8 <= tick <= df["one_in_x"].max() * 1.4
    ]

    if visible_ticks:
        ax.set_xticks(visible_ticks)
        ax.set_xticklabels([f"1 in {tick}" for tick in visible_ticks])

    ax.grid(True, axis="x", linestyle="-", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    categories_present = df["category"].dropna().unique().tolist()

    handles = []
    for category in categories_present:
        color = CATEGORY_COLORS.get(category, "#333333")

        handles.append(
            plt.Line2D(
                [0],
                [0],
                marker="o",
                linestyle="",
                markersize=8,
                label=category,
                markerfacecolor=color,
                markeredgecolor=color,
            )
        )

    if handles:
        ax.legend(
            handles=handles,
            title="Category",
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            frameon=True,
        )

    plt.subplots_adjust(left=0.30, right=0.78, top=0.82, bottom=0.12)

    fig.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.25)
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