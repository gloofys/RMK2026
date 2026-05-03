from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"

PROBABILITY_TABLE_PATH = PROCESSED_DATA_DIR / "probability_scale.csv"
PROBABILITY_FIGURE_PATH = FIGURES_DIR / "probability_scale.png"

FOREST_FIRE_CURRENT_YEAR_URL = (
    "https://opendata.smit.ee/paa/csv/"
    "metsa_ja_maastikutulekahjud_jooksev_aasta.csv"
)

FOREST_FIRE_HISTORY_URL = (
    "https://opendata.smit.ee/paa/csv/"
    "metsa_ja_maastikutulekahjud_2014_kuni_2025.csv"
)

FOREST_FIRE_CURRENT_YEAR_RAW_PATH = (
    RAW_DATA_DIR / "metsa_ja_maastikutulekahjud_jooksev_aasta.csv"
)

FOREST_FIRE_HISTORY_RAW_PATH = (
    RAW_DATA_DIR / "metsa_ja_maastikutulekahjud_2014_kuni_2025.csv"
)

STATISTICS_ESTONIA_RV030_API_URL = (
    "https://andmed.stat.ee/api/v1/et/stat/RV030"
)

BIRTHS_DEATHS_RAW_PATH = RAW_DATA_DIR / "rv030_births_deaths.csv"

BIRTHS_DEATHS_RAW_PATH = RAW_DATA_DIR / "rv030_births_deaths.csv"

STATISTICS_ESTONIA_TS093_API_URL = (
    "https://andmed.stat.ee/api/v1/et/stat/TS093"
)

TRAFFIC_ACCIDENTS_RAW_PATH = RAW_DATA_DIR / "ts093_traffic_accidents.csv"