import calendar
import math
from dataclasses import dataclass

import pandas as pd

from probability_scale.config import TRAFFIC_ACCIDENTS_RAW_PATH


@dataclass
class TrafficAccidentStats:
    year: int
    accident_count: int
    days_in_year: int
    probability: float

    @property
    def one_in_x(self) -> float:
        return 1 / self.probability


def normalize_text(value: str) -> str:
    """
    Normalize Estonian text for easier matching.
    """

    return (
        str(value)
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


def read_traffic_accidents_data() -> pd.DataFrame:
    """
    Read Statistics Estonia TS093 traffic accidents CSV data.
    """

    if not TRAFFIC_ACCIDENTS_RAW_PATH.exists():
        raise FileNotFoundError(
            "Missing traffic accidents raw data. Run "
            "`python scripts/fetch_data.py` first."
        )

    encodings = ["utf-8-sig", "utf-8", "cp1257"]

    for encoding in encodings:
        try:
            return pd.read_csv(
                TRAFFIC_ACCIDENTS_RAW_PATH,
                sep=None,
                engine="python",
                encoding=encoding,
            )
        except UnicodeDecodeError:
            continue

    raise ValueError("Could not read traffic accidents CSV with supported encodings.")


def find_column_by_keywords(df: pd.DataFrame, keywords: list[str]) -> str:
    """
    Find a column where the normalized column name contains one of the keywords.
    """

    for column in df.columns:
        normalized = normalize_text(column)

        if any(keyword in normalized for keyword in keywords):
            return column

    raise ValueError(
        f"Could not find column with keywords {keywords}. "
        f"Available columns: {list(df.columns)}"
    )


def find_year_columns(df: pd.DataFrame) -> list[str]:
    """
    Find year columns in a wide Statistics Estonia table.

    Example columns:
    1990, 1991, ..., 2024
    """

    year_columns = []

    for column in df.columns:
        column_text = str(column).strip()

        if column_text.isdigit() and len(column_text) == 4:
            year_columns.append(column)

    if not year_columns:
        raise ValueError(
            "Could not find year columns. "
            f"Available columns: {list(df.columns)}"
        )

    return sorted(year_columns, key=lambda value: int(str(value)))


def clean_numeric_value(value) -> float:
    """
    Convert a Statistics Estonia CSV value to float.
    """

    if pd.isna(value):
        return math.nan

    text = str(value).replace(" ", "").replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return math.nan


def poisson_probability_at_least_one(
    event_count: int,
    interval_count: int,
) -> float:
    """
    Estimate probability that at least one event occurs in a random interval.

    P(at least one event) = 1 - exp(-lambda)
    """

    event_rate = event_count / interval_count

    return 1 - math.exp(-event_rate)


def calculate_traffic_accident_stats() -> TrafficAccidentStats:
    """
    Calculate the probability that a randomly selected day has at least one
    traffic accident with injured people.

    TS093 is read as a wide table with columns like:
    Näitaja, Kuu, 1990, 1991, ..., 2024.

    The calculation uses the latest available year and the annual total row.
    """

    df = read_traffic_accidents_data()

    indicator_column = find_column_by_keywords(df, ["naitaja", "indicator"])
    month_column = find_column_by_keywords(df, ["kuu", "month"])
    year_columns = find_year_columns(df)

    latest_year_column = year_columns[-1]
    latest_year = int(str(latest_year_column))

    df = df.copy()

    df["normalized_indicator"] = df[indicator_column].map(normalize_text)
    df["normalized_month"] = df[month_column].map(normalize_text)
    df["latest_year_value"] = df[latest_year_column].map(clean_numeric_value)

    accident_rows = df[
        df["normalized_indicator"].str.contains("liiklusonnetused", na=False)
    ]

    if accident_rows.empty:
        raise ValueError("Could not find traffic accident rows in TS093 data.")

    annual_total_rows = accident_rows[
        accident_rows["normalized_month"].str.contains("kokku", na=False)
    ]

    if not annual_total_rows.empty:
        accident_count = int(annual_total_rows["latest_year_value"].iloc[0])
    else:
        monthly_rows = accident_rows.dropna(subset=["latest_year_value"])
        accident_count = int(monthly_rows["latest_year_value"].sum())

    if accident_count <= 0:
        raise ValueError(
            "Traffic accident count is zero or missing for latest year "
            f"{latest_year}."
        )

    days_in_year = 366 if calendar.isleap(latest_year) else 365

    probability = poisson_probability_at_least_one(
        event_count=accident_count,
        interval_count=days_in_year,
    )

    return TrafficAccidentStats(
        year=latest_year,
        accident_count=accident_count,
        days_in_year=days_in_year,
        probability=probability,
    )