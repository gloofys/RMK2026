# Approach

## Project idea

The goal of this project is to create a probability scale for events in Estonia.

The final result should help readers understand probability by comparing familiar real-world events on the same visual scale.

The current title is:

```text
Probability Scale of Estonia
Real events from public datasets
```

I chose events that are understandable to everyday readers and also relevant to environmental and public-sector data work.

## Why this topic?

People usually understand distances better than probabilities.

For example:

- a few centimetres can be held in one hand
- a few metres is the scale of a room
- kilometres are used for distances between cities

Probabilities are harder to understand intuitively.

A probability such as `0.01` or `0.0001` is mathematically simple, but it is not immediately obvious whether this is common or rare.

This project tries to make probabilities easier to understand by converting public Estonian data into “1 in X” statements.

For example:

```text
1 in 6.2 random 10-minute intervals
```

is easier to understand than:

```text
0.161
```

## Current focus

The current main visualisation focuses on one comparable probability type:

```text
Probability that at least one event happens in a random 10-minute interval.
```

This keeps the visual comparison fair and easier to understand.

The current main probability scale includes:

1. Birth in Estonia in a random 10-minute interval
2. Death in Estonia in a random 10-minute interval
3. Traffic accident with injuries in a random 10-minute interval
4. Forest or landscape fire in a random 10-minute interval

These events are calculated from public datasets and processed programmatically.

## Why 10-minute intervals?

At first, some event probabilities were calculated per random day.

However, this made some events appear almost certain. For example, traffic accidents with injuries and forest or landscape fires can happen on many days, so a daily scale made them look close to `1 in 1`.

A 10-minute interval gives a more useful comparison.

It makes common events and less common events fit better on one scale.

The interval is also easy to understand:

```text
1 day = 24 hours
1 hour = 6 ten-minute intervals
1 day = 144 ten-minute intervals
```

For a normal year:

```text
365 * 144 = 52,560 ten-minute intervals
```

For a leap year:

```text
366 * 144 = 52,704 ten-minute intervals
```

## Data sources used

The current implementation uses three public data sources.

### 1. Statistics Estonia RV030

Used for:

- births
- deaths

Source:

```text
https://andmed.stat.ee/et/stat/RV030
```

This data is downloaded programmatically through the Statistics Estonia PxWeb API.

### 2. Statistics Estonia TS093

Used for:

- traffic accidents with injured people

Source:

```text
https://andmed.stat.ee/et/stat/TS093
```

This data is downloaded programmatically through the Statistics Estonia PxWeb API.

### 3. Forest and landscape fires

Used for:

- forest and landscape fire events

Source:

```text
https://andmed.eesti.ee/datasets/metsa-ja-maastikutulekahjud
```

The CSV files are downloaded programmatically from the public open data source.

## Important distinction: probability type

One challenge in this project is that not all probabilities answer the same type of question.

For example, this question:

```text
What is the probability that at least one death happens in Estonia during a random 10-minute interval?
```

is different from this question:

```text
If we randomly select one traffic accident record, what is the probability that it happened in summer?
```

Both are probabilities, but they have different meanings.

Because of this, the processed dataset includes a column named:

```text
probability_type
```

The most important current probability type is:

```text
interval_event_probability
```

This is used for the main visualisation.

The project also contains logic for:

```text
record_share
```

Record-share probabilities are useful, but they are not shown in the main scale if the goal is to keep the visual comparison focused on one probability type.

## Main calculation pattern

For the main probability scale, I estimate the probability that at least one event happens in a randomly selected 10-minute interval.

The calculation uses a simple Poisson approximation.

First, calculate the event rate:

```text
event_rate = event_count / number_of_intervals
```

Then calculate the probability that at least one event happens in a random interval:

```text
P(at least one event) = 1 - exp(-event_rate)
```

This is useful for count-based events such as:

- annual births
- annual deaths
- annual traffic accidents
- forest and landscape fire records

## Example calculation idea

If there are 10,000 events in one year, and the year has 52,560 ten-minute intervals, then:

```text
event_rate = 10000 / 52560
```

Then:

```text
P(at least one event in a random 10-minute interval) = 1 - exp(-event_rate)
```

The result is then converted into a “1 in X” value:

```text
one_in_x = 1 / probability
```

This makes the output easier to understand for readers.

## Output table

The processed output table contains these columns:

```text
event
category
probability
one_in_x
probability_type
interpretation
source_name
source_url
notes
```

Example row structure:

```text
event: Birth in Estonia in a random 10-minute interval
category: Population
probability: calculated value
one_in_x: calculated value
probability_type: interval_event_probability
interpretation: About 1 in X ten-minute intervals
source_name: Statistics Estonia RV030 births/deaths data
source_url: https://andmed.stat.ee/et/stat/RV030
notes: Calculation details and source period
```

## Visualisation approach

The main output is a horizontal probability scale.

The x-axis uses:

```text
one_in_x
```

instead of raw probability.

This is because “1 in X” is more intuitive for readers than decimal probabilities.

The x-axis uses a logarithmic scale.

This is needed because the selected events can differ by large factors.

For example:

```text
1 in 4
1 in 6
1 in 28
1 in 52
```

A logarithmic scale makes these differences easier to compare visually.

The graph is sorted from more common events to rarer events.

In the final plot:

```text
farther right means rarer
```

## Why not mix all probability types in one graph?

Earlier versions of the project mixed interval probabilities and record-share probabilities in the same graph.

For example:

```text
Death in Estonia in a random 10-minute interval
```

and:

```text
Traffic accident with injuries happened in summer
```

These are both valid probabilities, but they answer different questions.

Mixing them in one visual scale can confuse readers.

Because of this, the main graph focuses on interval event probabilities only.

Record-share probabilities can still be calculated and documented separately, but they should not be interpreted as personal risk or directly compared with interval probabilities.

## Reproducible workflow

The project workflow is:

```text
download raw data
        ↓
process public datasets
        ↓
calculate probabilities
        ↓
save processed CSV
        ↓
create probability scale plot
        ↓
run smoke tests
```

The workflow can be run with:

```bash
python scripts/run_all.py
```

Or step by step:

```bash
python scripts/fetch_data.py
python scripts/run_pipeline.py
python -m pytest
```

## First MVP and later improvements

The first MVP used manually prepared example values to quickly test the idea and create the first plot.

That version was useful for checking the structure of the project.

The current version improves on that by calculating the main probability values from real public data sources.

The project now includes:

- programmatic data download
- data processing scripts
- probability calculations
- generated processed CSV
- generated plot
- smoke tests
- documentation

## Limitations

The probabilities in the main scale are event-frequency probabilities.

They are not personal risk probabilities.

For example, the traffic accident probability does not mean that one person has that exact chance of being in an accident during a 10-minute interval.

Personal risk depends on many factors, including:

- location
- age
- behaviour
- season
- weather
- time spent in traffic
- exposure to risk

The goal of this project is not to calculate personal risk.

The goal is to create an intuitive probability scale from public data.

Another limitation is that the datasets have different definitions, formats and update frequencies.

For example:

- Statistics Estonia tables are downloaded through the PxWeb API
- forest and landscape fire data is downloaded as CSV files
- some datasets are yearly
- some datasets contain event records
- some datasets may be updated more often than others

These differences are documented in the source notes and in the processed output table.

## Future improvements

Possible future improvements:

- add more RMK-specific forest indicators
- add EE-ALARM crisis alert probabilities
- add a separate graph for record-share probabilities
- add county-level or regional comparisons
- add uncertainty intervals
- compare seasonal differences more carefully
- add Bayesian reasoning for rare events
- create a small Power BI or Streamlit version
- improve the visual design further