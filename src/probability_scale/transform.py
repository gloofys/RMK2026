from dataclasses import dataclass

import pandas as pd


@dataclass
class ProbabilityEvent:
    """
    Represents one event on the probability scale.
    """

    event: str
    category: str
    probability: float
    probability_type: str
    interpretation: str
    source_name: str
    source_url: str
    notes: str

    @property
    def one_in_x(self) -> float:
        """
        Convert probability to a '1 in X' value.
        """

        if self.probability <= 0:
            raise ValueError("Probability must be greater than zero.")

        return 1 / self.probability


def build_example_events() -> list[ProbabilityEvent]:
    """
    Build the first MVP probability events.

    These values are example values for the first working version.
    Later, they should be replaced with values calculated from source data.
    """

    return [
        ProbabilityEvent(
            event="A randomly selected forest stand has pine as dominant tree species",
            category="Nature",
            probability=0.30,
            probability_type="record_share",
            interpretation="About 1 in 3 forest stands",
            source_name="Forest inventory / SMI",
            source_url="https://andmed.eesti.ee/datasets/smi-statistilise-metsainventeerimise-andmestik",
            notes="Example value for first MVP plot",
        ),
        ProbabilityEvent(
            event="A randomly selected forest stand has birch as dominant tree species",
            category="Nature",
            probability=0.30,
            probability_type="record_share",
            interpretation="About 1 in 3 forest stands",
            source_name="Forest inventory / SMI",
            source_url="https://andmed.eesti.ee/datasets/smi-statistilise-metsainventeerimise-andmestik",
            notes="Example value for first MVP plot",
        ),
        ProbabilityEvent(
            event="A randomly selected resident dies within a year",
            category="Population",
            probability=0.012,
            probability_type="individual_probability",
            interpretation="About 1 in 83 residents per year",
            source_name="Statistics Estonia births and deaths",
            source_url="https://andmed.eesti.ee/datasets/sunnid-surmad-ja-loomulik-iive",
            notes="Example value for first MVP plot",
        ),
        ProbabilityEvent(
            event="A randomly selected resident is born during a year",
            category="Population",
            probability=0.007,
            probability_type="individual_probability",
            interpretation="About 1 in 143 residents per year",
            source_name="Statistics Estonia births and deaths",
            source_url="https://andmed.eesti.ee/datasets/sunnid-surmad-ja-loomulik-iive",
            notes="Example value for first MVP plot",
        ),
        ProbabilityEvent(
            event="A randomly selected day has a traffic accident with injured people",
            category="Traffic",
            probability=0.75,
            probability_type="daily_event_probability",
            interpretation="About 1 in 1.3 days",
            source_name="Traffic accidents with injured people",
            source_url="https://andmed.eesti.ee/datasets/inimkannatanutega-liiklusonnetuste-andmed",
            notes="Example value for first MVP plot",
        ),
        ProbabilityEvent(
            event="A randomly selected day has a forest or landscape fire",
            category="Nature",
            probability=0.08,
            probability_type="daily_event_probability",
            interpretation="About 1 in 12.5 days",
            source_name="Forest and landscape fires",
            source_url="https://andmed.eesti.ee/datasets/metsa-ja-maastikutulekahjud",
            notes="Example value for first MVP plot",
        ),
        ProbabilityEvent(
            event="A randomly selected day has an EE-ALARM crisis alert",
            category="Crisis",
            probability=0.01,
            probability_type="daily_event_probability",
            interpretation="About 1 in 100 days",
            source_name="EE-ALARM crisis alerts",
            source_url="https://andmed.eesti.ee/datasets/ulevaade-kriisiinfoteenuse-%28krit%29-sundmustest-ja-nende-raames-valja-saadetud-ohuteavitussonumitest-ee-alarm-%282025%29",
            notes="Example value for first MVP plot",
        ),
    ]


def build_probability_table() -> pd.DataFrame:
    """
    Convert probability events into a processed probability table.
    """

    events = build_example_events()

    rows = []

    for item in events:
        rows.append(
            {
                "event": item.event,
                "category": item.category,
                "probability": item.probability,
                "one_in_x": round(item.one_in_x, 2),
                "probability_type": item.probability_type,
                "interpretation": item.interpretation,
                "source_name": item.source_name,
                "source_url": item.source_url,
                "notes": item.notes,
            }
        )

    df = pd.DataFrame(rows)
    df = df.sort_values("probability", ascending=False)

    return df
    
