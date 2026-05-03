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
    Format '1 in X' nicely for labels.
    """

    if value >= 100:
        return f"1 in {value:,.0f}"
    if value >= 10:
        return f"1 in {value:.1f}"
    return f"1 in {value:.2f}"


def wrap_event_label(text: str, width: int = 34) -> str:
    """
    Wrap long event labels onto multiple lines.
    """
    return fill(text, width=width)


def validate_probability_table(df: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def create_probability_scale_plot(df: pd.DataFrame, output_path: Path) -> None:
    """
    Create a more readable horizontal probability plot.
    """

    validate_probability_table(df)

    df = df.copy()
    df = df.sort_values("probability", ascending=False).reset_index(drop=True)

    df["wrapped_event"] = df["event"].apply(wrap_event_label)
    df["color"] = df["category"].map(CATEGORY_COLORS).fillna("#333333")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig_height = max(6, len(df) * 1.1)
    fig, ax = plt.subplots(figsize=(13, fig_height))

    y_positions = list(range(len(df)))

    # Lollipop lines
    for i, row in df.iterrows():
        ax.hlines(
            y=i,
            xmin=df["probability"].min() * 0.9,
            xmax=row["probability"],
            color="#cccccc",
            linewidth=1.2,
            zorder=1,
        )

    # Points
    ax.scatter(
        df["probability"],
        y_positions,
        s=90,
        c=df["color"],
        zorder=3,
    )

    # Labels next to points
    for i, row in df.iterrows():
        label = format_one_in_x(row["one_in_x"])
        ax.annotate(
            label,
            (row["probability"], i),
            xytext=(8, 0),
            textcoords="offset points",
            va="center",
            fontsize=10,
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["wrapped_event"], fontsize=10)
    ax.invert_yaxis()

    ax.set_xscale("log")
    ax.set_xlabel("Probability (log scale)", fontsize=11)

    ax.set_title(
        "Probability Scale of Estonia\n"
        "Real events from public datasets",
        fontsize=14,
        pad=16,
    )

    # Friendlier major ticks
    tick_values = [1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.001]
    visible_ticks = [
        tick for tick in tick_values
        if df["probability"].min() * 0.8 <= tick <= df["probability"].max() * 1.2
    ]

    if visible_ticks:
        ax.set_xticks(visible_ticks)
        ax.set_xticklabels([str(tick) for tick in visible_ticks])

    ax.grid(True, axis="x", linestyle="--", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)

    # Clean spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend
    categories_present = df["category"].dropna().unique().tolist()
    handles = []
    for category in categories_present:
        handles.append(
            plt.Line2D(
                [0],
                [0],
                marker="o",
                linestyle="",
                markersize=8,
                label=category,
                markerfacecolor=CATEGORY_COLORS.get(category, "#333333"),
                markeredgecolor=CATEGORY_COLORS.get(category, "#333333"),
            )
        )

    if handles:
        ax.legend(handles=handles, title="Category", loc="lower right")

    plt.subplots_adjust(left=0.38, right=0.95, top=0.88, bottom=0.12)

    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def create_probability_scale_plot_from_csv(
    input_path: Path,
    output_path: Path,
) -> None:
    df = pd.read_csv(input_path)
    create_probability_scale_plot(df, output_path)