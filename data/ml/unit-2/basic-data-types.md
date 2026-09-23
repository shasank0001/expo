---
subject: ml
unit: 2
topic: basic-data-types
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Basic Types of Data in Machine Learning

## Overview

Data types determine how a value should be measured, stored, compared, visualised, and modelled. A model can fail when a nominal category is treated as an ordered number, a timestamp is split carelessly, or a missing value is silently treated as zero. Choosing the right representation is the first step in data preparation.

The same business field can have several representations. Age may be numerical, a satisfaction label may be ordinal, and free-text feedback is text. We describe the measurement type and the modelling role separately.

## Explanation

### Numerical data

Numerical variables represent quantities that support meaningful arithmetic.

- **Continuous:** height, temperature, income, time; values lie on a continuum.
- **Discrete:** number of children, number of clicks, count of defects; values come from a countable set.
- **Ratio-scale variables** have a meaningful zero, so ratios are meaningful: 10 kg is twice 5 kg.
- **Interval-scale variables** have equal intervals but an arbitrary zero: 20 °C is not “twice as hot” as 10 °C in a ratio sense.

A numerical variable may be skewed, contain outliers, or have a distribution that changes over time. Mean, median, standard deviation, and quantiles describe it, but the correct summary depends on the distribution and use.

### Categorical data

Categorical variables identify groups rather than quantities.

- **Nominal:** red, blue, green; department, country, payment method. There is no natural order.
- **Ordinal:** low, medium, high; small, medium, large; poor, fair, good. The order is meaningful, but the gaps need not be equal.
- **Binary:** yes/no, fraud/not fraud, positive/negative. Binary variables are often encoded as 0 and 1, but the labels remain categorical.
- **Multi-class:** several unordered categories.
- **Multi-label:** one observation can have several independent categories.

For nominal data, one-hot encoding is usually safer than assigning arbitrary integer codes. For ordinal data, integer encoding can preserve order, but only if the model uses the order appropriately. A category with rare levels needs grouping or a robust unknown-category policy.

### Time and sequence data

A timestamp has an absolute time and often a calendar structure. Year, month, weekday, holiday, hour, and “days since event” can be engineered from it. Time series has an order and usually dependencies between nearby observations. Randomly splitting it can train on the future to predict the past. Lagged variables are useful only when the value would be available at prediction time.

Sequences such as speech, text, sensor traces, and video contain order information. A sequence model should preserve or deliberately summarise that order.

### Text data

Text is symbolic but not a collection of ordinary independent numbers. A document can be represented by raw tokens, counts, TF–IDF, embeddings, or a language-model representation. Vocabulary choice, stop-word handling, normalisation, tokenisation, and sequence length affect the result. Text often contains protected or sensitive information, so data governance is part of the type definition.

### Image and audio data

Images are arrays of pixels or learned feature maps. Colour channels, resolution, orientation, lighting, and class balance matter. Audio is a time series of amplitudes, often represented by spectrograms or learned features; sample rate, noise, and speaker variation matter. Raw data are high-dimensional and normally need transformations or a suitable architecture.

### Graph and relational data

A graph represents entities as nodes and relationships as edges. Features can be attached to nodes and edges, while the graph structure itself is information. Splitting edges randomly can leak connected information, so a graph task requires group- or time-aware splitting.

### Missing, unknown, and sentinel values

Missingness is informative or not depending on why it is missing. “Not recorded” may mean “not applicable,” “unknown,” or “declined.” Keep a missing indicator when the distinction matters. Do not replace missing values indiscriminately with the mean or zero. A sentinel such as `-1` must not accidentally be accepted as a real measurement.

### Measurement levels versus model roles

A feature may be categorical in its measurement but used to calculate a count, or text in its raw form but represented by an embedding. State both:

- **Measured type:** nominal, ordinal, interval, ratio, time, text, image, graph.
- **Model role:** input feature, target, identifier, grouping variable, timestamp, or derived feature.

Identifiers should usually not be used as numeric predictors: an ID 10,000 is not automatically larger or more informative than ID 9,999. Some IDs are useful only for joining or grouping.

## Worked examples

### Example 1: encoding a nominal variable

A colour field has values `red`, `blue`, and `green`. One-hot encoding gives

\[
[\mathbf1(\text{red}),\mathbf1(\text{blue}),\mathbf1(\text{green})].
\]

Using `red=1, blue=2, green=3` invents a false order and makes a distance between blue and green appear meaningful.

### Example 2: ordinal encoding

Satisfaction levels `low < medium < high` can be represented as 0, 1, and 2. The difference between low and medium is not guaranteed to equal the difference between medium and high, so the model should not assume equal intervals.

### Example 3: time-aware features

For a demand forecast at 6 a.m. on 5 January, features might include day of week, holiday flag, recent demand, and weather known at 6 a.m. Actual demand for the day or a future promotion settlement is not available and would be leakage.

### Example 4: missingness

A survey's income field is blank for some respondents. Blank may mean high income or refusal, not a random zero. A median imputation plus a missing indicator preserves the model input while making the uncertainty visible. The team documents the assumption and checks subgroup effects.

## Key terms & formulas

- **Nominal variable:** unordered category.
- **Ordinal variable:** ordered category with unspecified spacing.
- **Interval scale:** equal intervals, arbitrary zero.
- **Ratio scale:** equal intervals and meaningful zero.
- **Binary variable:** two-category variable.
- **Discrete variable:** countable value.
- **Continuous variable:** measurement on a continuum.
- **One-hot encoding:**
  \[
  x_{ij}=\mathbf1(\text{row }i\text{ has category }j).
  \]
- **Standardisation:**
  \[
  z_{ij}=\frac{x_{ij}-\mu_j}{\sigma_j}.
  \]
- **Min–max scaling:** \(x'=(x-\min x)/(\max x-\min x)\).
- **Time-series feature:** a value derived from position, calendar, lag, or rolling history.
- **Missingness indicator:** \(m_{ij}=\mathbf1(x_{ij}\text{ is missing})\).
- **Data type:** the structure and measurement meaning used for representation and processing.

## Common mistakes

1. **Encoding nominal categories as arbitrary integers.** This creates a false order.
2. **Treating an identifier as a quantity.** Large IDs are not automatically more valuable.
3. **Ignoring the measurement scale.** Averaging calendar temperatures or class IDs can be meaningless.
4. **Randomly splitting a time series.** This lets future information influence the past.
5. **Throwing away all text or image order.** Sequence and spatial relationships may be the signal.
6. **Using a missing-value code as a real measurement.** Filter or interpret it explicitly.
7. **Ignoring rare and unseen categories.** Keep an “other/unknown” policy and validate it.

## Exam prep

### Likely 2-mark questions

- **Define nominal and ordinal data.** Nominal has unordered categories; ordinal has a meaningful order.
- **Why is one-hot encoding useful for colours?** It avoids inventing an order among unrelated categories.
- **What is a timestamp feature?** A numeric or categorical value derived from date/time, such as hour or holiday.
- **Why must time-series splits be chronological?** To prevent future information leaking into training.

### Long-answer prompts

- **Explain the main data types used in machine learning.** Cover numerical, categorical, temporal, text, image, graph, and missing data with examples.
- **Choose suitable representations for five fields.** Justify scaling, one-hot, ordinal encoding, tokenisation, or sequence treatment.
- **Explain measurement levels and give two examples of each.** Include interval/ratio distinctions and the implications for arithmetic.
- **How can data type affect model choice?** Discuss distance, loss, encodings, time dependence, and dimensionality.
