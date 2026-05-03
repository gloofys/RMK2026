# Data sources

This project uses public Estonian datasets to build a probability scale of
everyday, environmental and rare public-sector events.

The goal is not only to collect interesting numbers, but to convert them into
comparable probability statements.

## 1. Births, deaths and natural increase

**Dataset:** Sünnid, surmad ja loomulik iive  
**Source:** Estonian Open Data Portal / Statistics Estonia  
**Link:** https://andmed.eesti.ee/datasets/sunnid-surmad-ja-loomulik-iive

### Planned use in this project

This dataset can be used to calculate population-related probabilities, for
example:

- probability that a randomly selected resident dies within a year
- average number of births per day
- average number of deaths per day

### Probability idea

```text
annual_deaths / population

or:

annual_births / 365
```

### Notes

Daily birth and death values are event frequencies, not individual risk
probabilities. This distinction is explained in `docs/approach.md`.

## 2. Traffic accidents with injured people

**Dataset:** Inimkannatanutega liiklusõnnetuste andmed  
**Source:** Estonian Open Data Portal / Police and Border Guard Board /
Transport Administration  
**Link:** https://andmed.eesti.ee/datasets/inimkannatanutega-liiklusonnetuste-andmed

### Planned use in this project

This dataset can be used to calculate how often traffic accidents with injured
people occur in Estonia.

### Probability idea

```text
number_of_accident_days / number_of_days_observed

or, as event frequency:

number_of_accidents / number_of_days_observed
```

### Notes

A traffic accident probability is not the same as personal traffic risk,
because exposure differs between people.

## 3. Forest and landscape fires

**Dataset:** Metsa- ja maastikutulekahjud  
**Source:** Estonian Open Data Portal / Rescue Board  
**Link:** https://andmed.eesti.ee/datasets/metsa-ja-maastikutulekahjud

### Planned use in this project

This dataset is useful for an RMK-related nature event in the probability
scale.

Possible probability statements:

- probability that a randomly selected day has at least one forest or landscape
  fire
- average number of forest or landscape fires per year
- average waiting time between registered forest or landscape fires

### Probability idea

```text
days_with_forest_or_landscape_fire / total_days_observed
```

## 4. Forest inventory data

**Dataset:** Metsa inventeerimisandmed  
**Source:** Estonian Open Data Portal  
**Link:** https://andmed.eesti.ee/datasets/metsa-inventeerimisandmed

### Planned use in this project

This dataset can be used to calculate probabilities related to forest stands.

Possible probability statements:

- probability that a randomly selected forest stand has pine as the dominant
  tree species
- probability that a randomly selected forest stand belongs to a certain age
  group
- probability that a randomly selected forest stand is in a certain forest
  category

### Probability idea

```text
number_of_matching_forest_stands / total_number_of_forest_stands
```

### Notes

This is different from event frequency. Here the probability is based on
randomly selecting one record or forest stand from the dataset.

## 5. Statistical forest inventory data

**Dataset:** SMI - Statistilise metsainventeerimise andmestik  
**Source:** Estonian Open Data Portal / Environmental Agency  
**Link:** https://andmed.eesti.ee/datasets/smi-statistilise-metsainventeerimise-andmestik

### Planned use in this project

This dataset can be used to add broader forest-level probabilities, such as
forest type, tree species or forest land proportions.

### Probability idea

```text
area_of_category / total_forest_area
```

### Notes

SMI data is useful because it describes forest patterns at the country level,
not only individual records.

## 6. EE-ALARM crisis alerts

**Dataset:** Ülevaade kriisiinfoteenuse sündmustest ja nende raames välja
saadetud ohuteavitussõnumitest EE-ALARM  
**Source:** Estonian Open Data Portal / Emergency Response Centre  
**Link:** https://andmed.eesti.ee/datasets/ulevaade-kriisiinfoteenuse-%28krit%29-sundmustest-ja-nende-raames-valja-saadetud-ohuteavitussonumitest-ee-alarm-%282025%29

### Planned use in this project

This dataset can represent rare public-sector warning events.

Possible probability statements:

- probability that a randomly selected day has an EE-ALARM message
- average waiting time between crisis alert messages
- share of alert events by event type

### Probability idea

```text
days_with_ee_alarm / total_days_observed
```

### Notes

This is expected to be one of the rarer events on the final probability scale.

## Source selection logic

I selected datasets where the numerator and denominator can be explained
clearly.

Good examples:

- number of deaths / population
- days with forest fire / total observed days
- forest stands with pine / all forest stands

Less clear examples were avoided or marked as event frequencies, because not
every count can be interpreted as personal risk.
