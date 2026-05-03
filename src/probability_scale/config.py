from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"

PROBABILITY_TABLE_PATH = PROCESSED_DATA_DIR / "probability_scale.csv"
PROBABILITY_FIGURE_PATH = FIGURES_DIR / "probability_scale.png"