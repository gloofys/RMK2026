from probability_scale.plotting import (
    REQUIRED_COLUMNS,
    create_probability_scale_plot,
)
from probability_scale.transform import build_probability_table


def test_probability_table_has_required_columns() -> None:
    """
    Check that the generated probability table has all required columns.
    """

    df = build_probability_table()

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    assert not missing_columns


def test_probability_values_are_valid() -> None:
    """
    Check that probability values are between 0 and 1.
    """

    df = build_probability_table()

    assert (df["probability"] > 0).all()
    assert (df["probability"] <= 1).all()


def test_one_in_x_values_are_positive() -> None:
    """
    Check that one_in_x values are positive.
    """

    df = build_probability_table()

    assert (df["one_in_x"] > 0).all()


def test_probability_plot_can_be_created(tmp_path) -> None:
    """
    Check that the plot function creates an output image file.
    """

    df = build_probability_table()
    output_path = tmp_path / "probability_scale.png"

    create_probability_scale_plot(df, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0