---
subject: ml
unit: 2
topic: exploring-data-structure
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Exploring the Structure of Data

## Overview

Exploring data structure means understanding what the observations look like, how variables vary, how they relate, and where the data may be unreliable. It is the bridge between collecting a table and deciding how to model it. EDA uses statistics and visualisations to generate hypotheses, expose quality problems, and check whether the available data can support the intended task.

A good exploration is both quantitative and domain-aware. A high average may hide a bimodal distribution; a strong correlation may be caused by time; a rare category may be a data-entry error or the most important case. The purpose is not to produce decorative charts but to make defensible modelling decisions.

## Explanation

### Understand the unit of observation

Start by asking what one row represents: a person, transaction, visit, sensor reading, image, or time interval. Check the grain, key, and relationship to the target. Duplicate keys may be valid for event data but not for a customer table. Repeated measurements of the same subject create dependence and can leak information if they are split across train and test.

### Descriptive statistics

For a numerical feature, calculate count, missing count, mean, median, standard deviation, quartiles, minimum, maximum, and skewness. For a categorical feature, count frequencies, proportions, rare levels, and unknown strings. Report these both overall and by important groups and time periods. A median can be more informative than a mean for a skewed income or latency feature; a count can be more useful than a mean for categorical data.

### Distributions and shapes

Visualise histograms, density plots, box plots, violin plots, and empirical cumulative distributions. Look for:

- centre, spread, skew, heavy tails, and multimodality;
- impossible negatives or values beyond a valid range;
- changes across time or locations;
- mixture of populations that may need a feature or segment;
- rare but important tails.

A box plot's five-number summary is useful, but the visual can hide multimodality. Use domain limits rather than automatically deleting every statistical outlier.

### Relationships among variables

Use scatter plots for numerical pairs, grouped/box plots for numerical–categorical pairs, correlation matrices for linear associations, and mosaic plots for categorical pairs. For nonlinear relationships, add smooth curves or transformations. Correlation is a measure of association, not causation. A correlation may arise from a common time trend or selection effect.

### Target and class structure

For supervised learning, inspect the target distribution and its relationship with features. A class with only 20 examples may need a different metric or data-collection plan. Check whether the target has impossible values, inconsistent definitions, or label leakage. For regression, inspect residuals and whether errors vary across feature ranges.

### Missingness and anomalies

Calculate missingness by column and subgroup. Determine whether missing values are random or systematic. Inspect duplicate rows, contradictory values, schema violations, and impossible combinations. Anomaly detection can suggest a problem, but a domain expert must decide whether to correct, retain, or investigate it.

### Time and groups

Plot trends and seasonal patterns. Use chronological, group-aware splits when appropriate. If multiple rows belong to one person, customer, machine, or hospital, all relevant rows should be grouped in the same partition. Time and group structure are often more important than a random train/test split.

### Dimensionality and redundancy

A wide table may contain duplicate columns, highly correlated features, or identifiers that are not useful. Correlation filtering, variance thresholds, domain review, principal component analysis, and feature selection can reduce noise. Dimensionality reduction may improve visualisation or regularise a model, but discarded variation can contain the target.

### Sampling and representativeness

Compare the sample with the intended deployment population. Check coverage of regions, devices, demographics, time periods, rare outcomes, and difficult cases. A dataset collected at one hospital or one promotion period is not automatically representative of all hospitals or seasons.

## Worked examples

### Example 1: discovering a missingness pattern

A loan field is missing 2% overall but 30% for one application channel. A generic imputation may erase the fact that the channel is different. The team adds a missing indicator, investigates collection failure, and checks performance by channel.

### Example 2: nonlinear relationship

Plotting study hours against score shows a curved pattern. A straight-line model is underfitting. A quadratic term, spline, or tree may capture the trend, but the team checks validation performance and avoids extrapolating beyond observed hours.

### Example 3: duplicates and leakage

A customer has several rows per month. Random splitting could put one month in training and another in test, making the model remember the customer. Grouped splitting keeps all months for a customer together. A feature such as “account closure date” is removed if it is only known after prediction.

### Example 4: rare categories

The product category has 20,000 rows with “other” and one row with a misspelled rare label. Spell normalisation may combine legitimate values, so the team checks the source and creates a validated “unknown” category rather than blindly replacing it.

## Key terms & formulas

- **EDA:** exploratory data analysis.
- **Mean:** \(\bar x=\frac1n\sum_i x_i\).
- **Median:** middle value of the ordered sample.
- **Variance:** \(s^2=\frac{1}{n-1}\sum_i(x_i-\bar x)^2\).
- **Standard deviation:** square root of variance.
- **Pearson correlation:**
  \[
  r=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}
  {\sqrt{\sum_i(x_i-\bar x)^2\sum_i(y_i-\bar y)^2}}.
  \]
- **Histogram:** binned frequency plot.
- **Box plot:** five-number distribution summary.
- **Multimodality:** multiple peaks in a distribution.
- **Data granularity:** the level represented by one row.
- **Group leakage:** information shared through a group crossing a split.
- **Representativeness:** similarity between the sample and target population.
- **Inlier/outlier:** ordinary versus unusual observation; context determines whether it is an error.
- **Residual:** \(y-\hat y\) in regression.

## Common mistakes

1. **Starting to model without inspecting missingness and target balance.** A basic profile may prevent a major failure.
2. **Deleting all outliers automatically.** Some extremes are valid and important.
3. **Using correlation as a causal explanation.** Explore relationships, not causal conclusions.
4. **Randomly splitting grouped or temporal data.** This causes leakage and optimistic scores.
5. **Treating a rare category as a typo.** Verify the source before merging it.
6. **Ignoring data collected at a different time or place.** Deployment may not resemble the sample.
7. **Using EDA conclusions from the test set.** Exploration should inform training choices without consuming final evaluation data.

## Exam prep

### Likely 2-mark questions

- **What is EDA?** Analysing data to understand distributions, relationships, missingness, and quality before modelling.
- **Name two ways to inspect a numerical distribution.** Histogram, box plot, density plot, or summary statistics.
- **Why inspect class balance?** Unequal classes can make accuracy misleading and affect training.
- **What is a data grain?** The meaning of one observation or row.

### Long-answer prompts

- **Describe how you would explore a new data set.** Cover unit of observation, types, distributions, missingness, relationships, target, time/groups, and representativeness.
- **How can exploratory analysis detect leakage?** Give temporal, target, duplicate, and grouped-record examples.
- **Explain the importance of visual and statistical exploration.** Use an example of a skewed, multimodal, or rare-category feature.
- **How would you investigate missing values?** Compare missingness across groups and time, identify causes, choose an imputation strategy, and retain uncertainty.
