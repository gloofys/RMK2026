from pathlib import Path

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