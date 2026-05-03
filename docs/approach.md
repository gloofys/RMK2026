# Approach

## Project idea

The goal of this project is to create a probability scale for events in
Estonia.

The working title is:

```text
Probability Scale of Estonia:
From daily births to rare crisis alerts and forest fires
```

The final result should help readers understand probability by comparing
familiar and less familiar events on the same visual scale.

I chose events that are understandable to everyday readers and also relevant to
environmental and public-sector data work.

## Why this topic?

People usually understand distances better than probabilities.

For example:

- a few centimetres can be held in one hand
- a few metres is the scale of a room
- kilometres are used for distances between cities

Probabilities are harder to understand intuitively.

A probability such as `0.01` or `0.0001` is mathematically simple, but it is
not immediately obvious whether this is common or rare.

This project tries to make probabilities easier to understand by placing
different Estonian events on one scale.

## Selected theme

The selected theme combines four areas:

```text
people + traffic + nature + crisis events
```

This gives the project a wider story than using only one dataset.

The planned event groups are:

- Population events: births and deaths
- Traffic events: traffic accidents with injured people
- Nature and forest events: forest and landscape fires, forest inventory
  properties
- Rare crisis events: EE-ALARM crisis alerts

This combination is useful because some events are very common, while others
are rare. That makes the probability scale more interesting.

## Important distinction: probability vs frequency

One challenge in this project is that not all values mean the same thing.

For example, these are different concepts:

> A randomly selected resident dies within a year.

and

> A traffic accident with injured people happens on a randomly selected day.

The first one can be interpreted as an individual probability.

The second one is better interpreted as an event frequency or daily occurrence
probability.

Because of this, the final dataset includes a column named `probability_type`.

Possible values:

```text
individual_probability
daily_event_probability
record_share
area_share
event_frequency
```

This makes the final result more honest and easier to understand.

## General calculation patterns

### 1. Individual probability

Used when the denominator is a population.

Example:

```text
probability = number_of_deaths / population
```

Possible interpretation:

> A randomly selected resident dies within a year.

### 2. Daily event probability

Used when the question is about whether an event happens on a randomly selected
day.

Example:

```text
probability = days_with_event / total_days_observed
```

Possible interpretation:

> A randomly selected day has at least one forest or landscape fire.

### 3. Record share

Used when the denominator is the number of records in a dataset.

Example:

```text
probability = forest_stands_with_pine / all_forest_stands
```

Possible interpretation:

> A randomly selected forest stand has pine as the dominant tree species.

### 4. Area share

Used when the denominator is total area.

Example:

```text
probability = pine_forest_area / total_forest_area
```

Possible interpretation:

> A randomly selected hectare of forest belongs to a certain forest type.

## Planned output table

The processed output table should contain at least these columns:

- `event`
- `category`
- `probability`
- `one_in_x`
- `probability_type`
- `interpretation`
- `source_name`
- `source_url`
- `notes`

Example:

```text
event: A randomly selected day has a forest or landscape fire
category: Nature
probability: 0.08
one_in_x: 12.5
probability_type: daily_event_probability
interpretation: About 1 in 12.5 days
source_name: Metsa- ja maastikutulekahjud
notes: Calculated from days with at least one event
```

## Planned visualisation

The main output will be a horizontal probability scale.

The x-axis will use a logarithmic scale because the selected probabilities can
differ by orders of magnitude.

The y-axis will contain event descriptions.

The plot should make it easy to compare common and rare events.

Possible visual idea:

```text
Common events                                     Rare events
|-----------------------------------------------------------|
0.5        0.1        0.01        0.001        0.0001
```

## Why logarithmic scale?

A normal linear scale would make rare events almost invisible.

For example:

```text
0.5
0.05
0.005
0.0005
```

These values are very different, but on a normal axis the smaller values would
be squeezed together.

A log scale makes differences between orders of magnitude easier to see.

## First MVP version

The first version of the project will not try to solve everything.

The MVP steps are:

1. Create a manually prepared example probability table.
2. Build a plot from that table.
3. Document the selected data sources.
4. Explain assumptions and limitations.
5. Replace manual example values with programmatically processed source data.

This approach makes it possible to quickly create a working end-to-end pipeline
before spending too much time on data ingestion details.

