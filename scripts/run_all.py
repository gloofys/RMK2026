from probability_scale.ingest import download_raw_data
from probability_scale.pipeline import run_pipeline


def main() -> None:
    """
    Run the full project workflow.

    Steps:
    1. Download raw data.
    2. Build the processed probability table.
    3. Create the probability scale plot.
    """

    print("Downloading raw data...")
    download_raw_data()

    print("Running probability scale pipeline...")
    run_pipeline()

    print("Done.")


if __name__ == "__main__":
    main()