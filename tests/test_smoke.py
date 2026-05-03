from probability_scale.config import FIGURE_DIR, RAW_DATA_DIR


def test_expected_directory_names() -> None:
    assert RAW_DATA_DIR.name == "raw"
    assert FIGURE_DIR.name == "figures"
