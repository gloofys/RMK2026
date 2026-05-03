import calendar
import math
from dataclasses import dataclass

import pandas as pd

from probability_scale.config import BIRTHS_DEATHS_RAW_PATH


@dataclass
class PopulationStats:
    year: int
    births: int
    deaths: int
    intervals_per_year: int
    birth_probability_10_min: float
    death_probability_10_min: float

    @property
    def birth_one_in_x(self) -> float:
        return 1 / self.birth_probability_10_min

    @property
    def death_one_in_x(self) -> float:
        return 1 / self.death_probability_10_min


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


def read_births_deaths_data() -> pd.DataFrame:
    """
    Read Statistics Estonia RV030 births/deaths CSV data.
    """

    if not BIRTHS_DEATHS_RAW_PATH.exists():
        raise FileNotFoundError(
            "Missing births/deaths raw data. Run "
            "`python scripts/fetch_data.py` first."
        )

    encodings = ["utf-8-sig", "utf-8", "cp1257"]

    for encoding in encodings:
        try:
            return pd.read_csv(
                BIRTHS_DEATHS_RAW_PATH,
                sep=None,
                engine="python",
                encoding=encoding,
            )
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "Could not read births/deaths CSV with supported encodings."
    )


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


def calculate_population_stats() -> PopulationStats:
    """
    Calculate birth and death probabilities from Statistics Estonia RV030.

    RV030 is read as a wide table with columns like:
    Aasta, Elussünnid, Surmad, Loomulik iive.

    The probabilities are calculated for a randomly selected 10-minute interval.
    """

    df = read_births_deaths_data()

    year_column = find_column_by_keywords(df, ["aasta", "year"])
    births_column = find_column_by_keywords(df, ["elussunnid", "birth"])
    deaths_column = find_column_by_keywords(df, ["surmad", "death"])

    df = df.copy()

    df["year_numeric"] = pd.to_numeric(df[year_column], errors="coerce")
    df["births_numeric"] = df[births_column].map(clean_numeric_value)
    df["deaths_numeric"] = df[deaths_column].map(clean_numeric_value)

    df = df.dropna(
        subset=[
            "year_numeric",
            "births_numeric",
            "deaths_numeric",
        ]
    )

    if df.empty:
        raise ValueError("No valid birth/death rows found in RV030 data.")

    df["year_numeric"] = df["year_numeric"].astype(int)

    latest_year = int(df["year_numeric"].max())
    latest_row = df[df["year_numeric"] == latest_year].iloc[0]

    births = int(latest_row["births_numeric"])
    deaths = int(latest_row["deaths_numeric"])

    days_in_year = 366 if calendar.isleap(latest_year) else 365
    intervals_per_year = days_in_year * 24 * 6

    birth_probability = poisson_probability_at_least_one(
        event_count=births,
        interval_count=intervals_per_year,
    )

    death_probability = poisson_probability_at_least_one(
        event_count=deaths,
        interval_count=intervals_per_year,
    )

    return PopulationStats(
        year=latest_year,
        births=births,
        deaths=deaths,
        intervals_per_year=intervals_per_year,
        birth_probability_10_min=birth_probability,
        death_probability_10_min=death_probability,
    )