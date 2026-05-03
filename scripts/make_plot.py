from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "probability_scale.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "figures" / "probability_scale.png"


def format_one_in_x(value: float) -> str:
    if value >= 100:
        return f"1 in {value:,.0f}"

    if value >= 10:
        return f"1 in {value:.1f}"

    return f"1 in {value:.2f}"


def make_probability_plot(input_path: Path, output_path: Path) -> None:
    df = pd.read_csv(input_path)

    required_columns = {
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

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

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


def main() -> None:
    make_probability_plot(INPUT_PATH, OUTPUT_PATH)
    print(f"Saved plot to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()