from pathlib import Path

from probability_scale.plotting import create_probability_scale_plot_from_csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "probability_scale.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "figures" / "probability_scale.png"


def main() -> None:
    """
    Create the probability scale plot from the processed CSV file.
    """

    create_probability_scale_plot_from_csv(INPUT_PATH, OUTPUT_PATH)

    print(f"Saved plot to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()