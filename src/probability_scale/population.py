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


def read_births_deaths_data() -> pd.DataFrame:
    """
    Read Statistics Estonia RV030 births/deaths CSV data.
    """

    if not BIRTHS_DEATHS_RAW_PATH.exists():
        raise FileNotFoundError(
            "Missing births/deaths raw data. Run "
            "`python scripts/fetch_data.py` first."
        )

    return pd.read_csv(
        BIRTHS_DEATHS_RAW_PATH,
        sep=None,
        engine="python",
        encoding="utf-8-sig",
    )


def find_column_by_keywords(df: pd.DataFrame, keywords: list[str]) -> str:
    """
    Find a column where the normalized name contains one of the given keywords.
    """

    for column in df.columns:
        normalized = normalize_column_name(column)

        if any(keyword in normalized for keyword in keywords):
            return column

    raise ValueError(
        f"Could not find column with keywords {keywords}. "
        f"Available columns: {list(df.columns)}"
    )


def find_value_column(df: pd.DataFrame) -> str:
    """
    Find the numeric value column in a PxWeb CSV output.
    """

    possible_names = ["value", "obsvalue", "obs_value", "väärtus", "vaartus"]

    for column in df.columns:
        normalized = normalize_column_name(column)

        if normalized in possible_names:
            return column

    # Fallback: use the last column, which is commonly the value column.
    return df.columns[-1]


def clean_numeric_value(value) -> float:
    """
    Convert a value from Statistics Estonia CSV to float.
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

    This uses a simple Poisson approximation:

    P(at least one event) = 1 - exp(-lambda)
    """

    event_rate = event_count / interval_count

    return 1 - math.exp(-event_rate)


def calculate_population_stats() -> PopulationStats:
    """
    Calculate birth and death probabilities from Statistics Estonia RV030.

    The probabilities are calculated for a randomly selected 10-minute interval.
    """

    df = read_births_deaths_data()

    year_column = find_column_by_keywords(df, ["aasta", "year"])
    indicator_column = find_column_by_keywords(df, ["naitaja", "indicator"])
    value_column = find_value_column(df)

    df = df.copy()
    df["normalized_indicator"] = df[indicator_column].map(normalize_column_name)
    df["numeric_value"] = df[value_column].map(clean_numeric_value)

    df = df.dropna(subset=["numeric_value"])

    df[year_column] = pd.to_numeric(df[year_column], errors="coerce")
    df = df.dropna(subset=[year_column])
    df[year_column] = df[year_column].astype(int)

    births_df = df[df["normalized_indicator"].str.contains("elussunnid")]
    deaths_df = df[df["normalized_indicator"].str.fullmatch("surmad")]

    if births_df.empty:
        raise ValueError("Could not find births row in RV030 data.")

    if deaths_df.empty:
        raise ValueError("Could not find deaths row in RV030 data.")

    common_years = sorted(
        set(births_df[year_column]).intersection(set(deaths_df[year_column])),
        reverse=True,
    )

    if not common_years:
        raise ValueError("Could not find a year with both births and deaths.")

    latest_year = common_years[0]

    births = int(
        births_df.loc[births_df[year_column] == latest_year, "numeric_value"].iloc[0]
    )
    deaths = int(
        deaths_df.loc[deaths_df[year_column] == latest_year, "numeric_value"].iloc[0]
    )

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