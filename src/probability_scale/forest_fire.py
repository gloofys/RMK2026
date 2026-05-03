from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from probability_scale.config import (
    FOREST_FIRE_CURRENT_YEAR_RAW_PATH,
    FOREST_FIRE_HISTORY_RAW_PATH,
)


@dataclass
class ForestFireStats:
    event_count: int
    days_with_event: int
    total_days_observed: int
    start_date: str
    end_date: str
    probability: float

    @property
    def one_in_x(self) -> float:
        return 1 / self.probability


@dataclass
class ForestFireShareStats:
    matching_records: int
    total_records: int
    start_date: str
    end_date: str
    probability: float

    @property
    def one_in_x(self) -> float:
        return 1 / self.probability


def read_forest_fire_csv(path: Path) -> pd.DataFrame:
    """
    Read one forest fire CSV file.

    The separator and encoding are handled flexibly because public CSV files
    may use different formats.
    """

    try:
        return pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(path, sep=None, engine="python", encoding="cp1257")


def normalize_column_name(column_name: str) -> str:
    """
    Normalize Estonian column names for easier matching.
    """

    return (
        column_name.lower()
        .replace("ä", "a")
        .replace("ö", "o")
        .replace("ü", "u")
        .replace("õ", "o")
        .replace(" ", "_")
    )


def find_date_column(df: pd.DataFrame) -> str:
    """
    Find the most likely date column in the forest fire dataset.
    """

    normalized_columns = {
        column: normalize_column_name(column)
        for column in df.columns
    }

    date_keywords = [
        "kuupaev",
        "kuup",
        "aeg",
        "date",
        "algus",
        "toimumis",
        "syndmus",
        "sundmus",
    ]

    for original_column, normalized_column in normalized_columns.items():
        if any(keyword in normalized_column for keyword in date_keywords):
            return original_column

    raise ValueError(
        "Could not detect date column. Available columns: "
        f"{list(df.columns)}"
    )


def load_forest_fire_data() -> pd.DataFrame:
    """
    Load and combine forest and landscape fire raw CSV files.
    """

    paths = [
        FOREST_FIRE_HISTORY_RAW_PATH,
        FOREST_FIRE_CURRENT_YEAR_RAW_PATH,
    ]

    missing_paths = [path for path in paths if not path.exists()]

    if missing_paths:
        raise FileNotFoundError(
            "Missing forest fire raw data files. Run "
            "`python scripts/fetch_data.py` first. Missing files: "
            f"{missing_paths}"
        )

    frames = [read_forest_fire_csv(path) for path in paths]

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates()

    return df


def calculate_forest_fire_stats() -> ForestFireStats:
    """
    Calculate the probability that a randomly selected observed day has
    at least one forest or landscape fire.
    """

    df = load_forest_fire_data()

    date_column = find_date_column(df)

    dates = pd.to_datetime(
        df[date_column],
        errors="coerce",
        dayfirst=True,
    ).dt.date

    dates = dates.dropna()

    if dates.empty:
        raise ValueError("No valid dates found in forest fire data.")

    start_date = dates.min()
    end_date = dates.max()

    total_days_observed = (end_date - start_date).days + 1
    days_with_event = dates.nunique()
    event_count = len(dates)

    probability = days_with_event / total_days_observed

    return ForestFireStats(
        event_count=event_count,
        days_with_event=days_with_event,
        total_days_observed=total_days_observed,
        start_date=str(start_date),
        end_date=str(end_date),
        probability=probability,
    )


def calculate_forest_fire_summer_share() -> ForestFireShareStats:
    """
    Calculate the share of forest and landscape fire records that happened in summer.

    Summer is defined as June, July and August.
    """

    df = load_forest_fire_data()

    date_column = find_date_column(df)

    dates = pd.to_datetime(
        df[date_column],
        errors="coerce",
        dayfirst=True,
    ).dropna()

    if dates.empty:
        raise ValueError("No valid dates found in forest fire data.")

    start_date = dates.dt.date.min()
    end_date = dates.dt.date.max()

    total_records = len(dates)
    summer_records = dates.dt.month.isin([6, 7, 8]).sum()

    probability = summer_records / total_records

    return ForestFireShareStats(
        matching_records=int(summer_records),
        total_records=int(total_records),
        start_date=str(start_date),
        end_date=str(end_date),
        probability=probability,
    )