from dataclasses import dataclass
from probability_scale.forest_fire import calculate_forest_fire_stats
from probability_scale.population import calculate_population_stats
from probability_scale.traffic import calculate_traffic_accident_stats
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

def build_forest_fire_event() -> ProbabilityEvent:
    """
    Build a probability event from real forest and landscape fire data.
    """

    stats = calculate_forest_fire_stats()

    return ProbabilityEvent(
        event="A randomly selected day has a forest or landscape fire",
        category="Nature",
        probability=stats.probability,
        probability_type="daily_event_probability",
        interpretation=f"About 1 in {stats.one_in_x:.1f} days",
        source_name="Forest and landscape fires",
        source_url="https://andmed.eesti.ee/datasets/metsa-ja-maastikutulekahjud",
        notes=(
            "Calculated from downloaded forest and landscape fire data. "
            f"Observed period: {stats.start_date} to {stats.end_date}. "
            f"Days with at least one event: {stats.days_with_event}. "
            f"Total observed days: {stats.total_days_observed}. "
            f"Total event records: {stats.event_count}."
        ),
    )

def build_birth_event() -> ProbabilityEvent:
    """
    Build a probability event from real Statistics Estonia birth data.
    """

    stats = calculate_population_stats()

    return ProbabilityEvent(
        event="A randomly selected 10-minute interval has at least one birth in Estonia",
        category="Population",
        probability=stats.birth_probability_10_min,
        probability_type="interval_event_probability",
        interpretation=f"About 1 in {stats.birth_one_in_x:.1f} ten-minute intervals",
        source_name="Statistics Estonia RV030 births/deaths data",
        source_url="https://andmed.stat.ee/et/stat/RV030",
        notes=(
            "Calculated from Statistics Estonia RV030. "
            f"Year: {stats.year}. "
            f"Annual births: {stats.births}. "
            "Probability estimated with a simple Poisson approximation."
        ),
    )


def build_death_event() -> ProbabilityEvent:
    """
    Build a probability event from real Statistics Estonia death data.
    """

    stats = calculate_population_stats()

    return ProbabilityEvent(
        event="A randomly selected 10-minute interval has at least one death in Estonia",
        category="Population",
        probability=stats.death_probability_10_min,
        probability_type="interval_event_probability",
        interpretation=f"About 1 in {stats.death_one_in_x:.1f} ten-minute intervals",
        source_name="Statistics Estonia RV030 births/deaths data",
        source_url="https://andmed.stat.ee/et/stat/RV030",
        notes=(
            "Calculated from Statistics Estonia RV030. "
            f"Year: {stats.year}. "
            f"Annual deaths: {stats.deaths}. "
            "Probability estimated with a simple Poisson approximation."
        ),
    )

def build_traffic_accident_event() -> ProbabilityEvent:
    """
    Build a probability event from real Statistics Estonia traffic accident data.
    """

    stats = calculate_traffic_accident_stats()

    return ProbabilityEvent(
        event="A randomly selected day has at least one traffic accident with injured people",
        category="Traffic",
        probability=stats.probability,
        probability_type="daily_event_probability",
        interpretation=f"About 1 in {stats.one_in_x:.2f} days",
        source_name="Statistics Estonia TS093 traffic accidents data",
        source_url="https://andmed.stat.ee/et/stat/TS093",
        notes=(
            "Calculated from Statistics Estonia TS093. "
            f"Year: {stats.year}. "
            f"Annual traffic accidents with injured people: {stats.accident_count}. "
            "Daily probability estimated with a simple Poisson approximation."
        ),
    )

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
            build_death_event(),
            build_birth_event(),
        build_traffic_accident_event(),

        build_forest_fire_event(),

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
    
