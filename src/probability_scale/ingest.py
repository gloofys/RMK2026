from pathlib import Path
from probability_scale.config import (
    BIRTHS_DEATHS_RAW_PATH,
    STATISTICS_ESTONIA_RV030_API_URL,
)
import requests

from probability_scale.config import (
    FOREST_FIRE_CURRENT_YEAR_RAW_PATH,
    FOREST_FIRE_CURRENT_YEAR_URL,
    FOREST_FIRE_HISTORY_RAW_PATH,
    FOREST_FIRE_HISTORY_URL,
    RAW_DATA_DIR,
)


def download_file(url: str, output_path: Path) -> None:
    """
    Download one file from a URL and save it locally.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    output_path.write_bytes(response.content)


def download_forest_fire_data() -> None:
    """
    Download forest and landscape fire CSV files from the public source.
    """

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    download_file(
        url=FOREST_FIRE_HISTORY_URL,
        output_path=FOREST_FIRE_HISTORY_RAW_PATH,
    )

    download_file(
        url=FOREST_FIRE_CURRENT_YEAR_URL,
        output_path=FOREST_FIRE_CURRENT_YEAR_RAW_PATH,
    )


def download_raw_data() -> None:
    """
    Download all raw data files used by the project.

    Currently this only downloads forest and landscape fire data.
    More sources will be added later.
    """

    download_forest_fire_data()
    download_births_deaths_data()

def build_pxweb_all_values_query(metadata: dict) -> dict:
    """
    Build a PxWeb query that requests all values from all dimensions.
    """

    query = []

    for variable in metadata["variables"]:
        query.append(
            {
                "code": variable["code"],
                "selection": {
                    "filter": "item",
                    "values": variable["values"],
                },
            }
        )

    return {
        "query": query,
        "response": {
            "format": "csv",
        },
    }

    return {
        "query": query,
        "response": {
            "format": "CSV",
        },
    }


def download_pxweb_csv(api_url: str, output_path: Path) -> None:
    """
    Download a complete PxWeb table as CSV.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    metadata_response = requests.get(api_url, timeout=30)
    metadata_response.raise_for_status()
    metadata = metadata_response.json()

    query = build_pxweb_all_values_query(metadata)

    data_response = requests.post(api_url, json=query, timeout=30)
    data_response.raise_for_status()

    output_path.write_text(data_response.text, encoding="utf-8")


def download_births_deaths_data() -> None:
    """
    Download Statistics Estonia RV030 births/deaths data.
    """

    download_pxweb_csv(
        api_url=STATISTICS_ESTONIA_RV030_API_URL,
        output_path=BIRTHS_DEATHS_RAW_PATH,
    )