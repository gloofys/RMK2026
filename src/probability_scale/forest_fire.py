from dataclasses import dataclass
from pathlib import Path

import math
import pandas as pd

from probability_scale.config import (
    FOREST_FIRE_CURRENT_YEAR_RAW_PATH,
    FOREST_FIRE_HISTORY_RAW_PATH,
)


@dataclass
class ForestFireStats:
    event_count: int
    days_observed: int
    intervals_observed: int
    start_date: str
    end_date: str
    probability_10_min: float

    @property
    def one_in_x(self) -> float:
        return 1 / self.probability_10_min


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
        str(column_name)
        .strip()
        .lower()
        .replace("\ufeff", "")
        .replace('"', "")
        .replace("ä", "a")
        .replace("ö", "o")
        .replace("ü", "u")
        .replace("õ", "o")
        .replace(" ", "_")
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


def parse_possible_date_column(series: pd.Series) -> pd.Series:
    """
    Try to parse a dataframe column as dates.

    ISO-like dates are parsed with year-first logic.
    Other dates are parsed with Estonian/European day-first logic.
    This avoids pandas warnings when ISO dates are parsed with dayfirst=True.
    """

    text_values = series.astype(str).str.strip()

    iso_like_mask = text_values.str.match(r"^\d{4}-\d{2}-\d{2}")

    parsed_iso = pd.to_datetime(
        text_values.where(iso_like_mask),
        errors="coerce",
    )

    parsed_dayfirst = pd.to_datetime(
        text_values.where(~iso_like_mask),
        errors="coerce",
        dayfirst=True,
    )

    return parsed_iso.fillna(parsed_dayfirst)


def find_date_column(df: pd.DataFrame) -> str:
    """
    Find the most likely date column by checking actual parseable date values.

    This is safer than only matching column names, because some columns may
    contain words like 'sündmus' without being date columns.
    """

    preferred_keywords = [
        "kuupaev",
        "kuup",
        "algus",
        "aeg",
        "date",
        "toimumis",
    ]

    best_column = None
    best_valid_count = 0

    for column in df.columns:
        normalized = normalize_column_name(column)

        if not any(keyword in normalized for keyword in preferred_keywords):
            continue

        parsed_dates = parse_possible_date_column(df[column])
        valid_count = parsed_dates.notna().sum()

        if valid_count > best_valid_count:
            best_column = column
            best_valid_count = valid_count

    if best_column is not None and best_valid_count > 0:
        return best_column

    # Fallback: try all columns and choose the one with most parseable dates.
    for column in df.columns:
        parsed_dates = parse_possible_date_column(df[column])
        valid_count = parsed_dates.notna().sum()

        if valid_count > best_valid_count:
            best_column = column
            best_valid_count = valid_count

    if best_column is None or best_valid_count == 0:
        raise ValueError(
            "Could not detect date column. Available columns: "
            f"{list(df.columns)}"
        )

    return best_column


def get_forest_fire_dates() -> pd.Series:
    """
    Load forest fire data and return parsed event dates.
    """

    df = load_forest_fire_data()
    date_column = find_date_column(df)

    dates = parse_possible_date_column(df[date_column]).dropna()

    if dates.empty:
        raise ValueError(
            "No valid dates found in forest fire data. "
            f"Detected date column: {date_column}. "
            f"Available columns: {list(df.columns)}"
        )

    return dates


def poisson_probability_at_least_one(
    event_count: int,
    interval_count: int,
) -> float:
    """
    Estimate probability that at least one event occurs in a random interval.
    """

    event_rate = event_count / interval_count

    return 1 - math.exp(-event_rate)


def calculate_forest_fire_stats() -> ForestFireStats:
    """
    Calculate the probability that a randomly selected 10-minute interval has
    at least one forest or landscape fire.
    """

    dates = get_forest_fire_dates()

    start_date = dates.dt.date.min()
    end_date = dates.dt.date.max()

    days_observed = (end_date - start_date).days + 1
    intervals_observed = days_observed * 24 * 6
    event_count = len(dates)

    probability_10_min = poisson_probability_at_least_one(
        event_count=event_count,
        interval_count=intervals_observed,
    )

    return ForestFireStats(
        event_count=event_count,
        days_observed=days_observed,
        intervals_observed=intervals_observed,
        start_date=str(start_date),
        end_date=str(end_date),
        probability_10_min=probability_10_min,
    )


def calculate_forest_fire_summer_share() -> ForestFireShareStats:
    """
    Calculate the share of forest and landscape fire records that happened in summer.

    Summer is defined as June, July and August.
    """

    dates = get_forest_fire_dates()

    start_date = dates.dt.date.min()
    end_date = dates.dt.date.max()

    total_records = len(dates)
    summer_records = dates.dt.month.isin([6, 7, 8]).sum()

    if total_records <= 0:
        raise ValueError("Forest fire data has no valid records.")

    if summer_records <= 0:
        raise ValueError(
            "Forest fire summer record count is zero. "
            "Check whether the correct date column was detected."
        )

    probability = summer_records / total_records

    return ForestFireShareStats(
        matching_records=int(summer_records),
        total_records=int(total_records),
        start_date=str(start_date),
        end_date=str(end_date),
        probability=probability,
    )