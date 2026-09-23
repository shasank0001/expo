---
subject: dwdm
unit: 1
topic: data-preprocessing
syllabus_ref: CSM3101 Unit-I
status: draft
---
# Data Quality and Preprocessing

## Overview

Raw data is rarely ready for reliable data mining. It may contain missing values, errors, duplicates, incompatible units, unusual observations, irrelevant features, and relationships that are difficult to analyze. Preprocessing is the controlled process of assessing, cleaning, integrating, reducing, transforming, discretizing, and organizing data before mining.

The complete treatment in this note follows Han, Kamber, and Pei: **data quality, cleaning, integration, reduction, transformation, discretization, and concept hierarchy generation**. It also follows Tan, Steinbach, and Kumar's emphasis on measurable data quality, attribute types, outliers, and the difference between an original value and a derived representation.

Preprocessing does not change the underlying reality. It changes the representation and the evidence available to an algorithm. Every operation should have a reason, a documented rule, an audit trail, and a validation check. Aggressive cleaning can remove rare but valid events; integration can create false matches; reduction can discard a minority pattern; discretization can lose information. Good preprocessing improves the quality of a result while keeping its limitations visible.

## Explanation

### 1. The role of preprocessing

A typical pipeline is:

```text
raw sources
  -> quality assessment
  -> cleaning
  -> integration
  -> reduction
  -> transformation
  -> discretization and concept hierarchy generation (when appropriate)
  -> mining and evaluation
```

The order is a guide, not a rigid rule. A preliminary integration may reveal duplicates that require cleaning. Transformation may expose values that need validation. Discretization may be followed by reduction, or a feature may be aggregated before integration. The important point is to make each dependency explicit.

Preprocessing has three broad purposes:

- **Quality:** make values accurate, complete, consistent, valid, timely, and identifiable.
- **Efficiency:** reduce storage, computation, and search space.
- **Compatibility:** convert data into forms that an algorithm or user can interpret.

The transformed dataset must be accompanied by metadata describing the original source, transformation time, parameters, affected records, and validation result. A clean-looking table without provenance can be less trustworthy than a table that exposes its cleaning decisions.

### 2. Data quality dimensions

A data-quality assessment should be systematic rather than a single yes/no judgment.

#### Accuracy

Accuracy means that a value correctly represents the real-world fact or the intended source. It cannot always be checked without an external reference. Possible checks include reconciliation with an authoritative system, range rules, transaction totals, duplicate invoices, and domain review.

#### Completeness

A dataset is complete when the required attributes and records are present. Missingness can occur because:

- the field was not collected;
- collection failed;
- the value was deleted;
- the value does not apply to the record;
- the source uses a null or sentinel code;
- a join failed.

Completeness should be measured by field, row, group, and time period. A dataset with 99% complete customer IDs can still have a serious problem if all missing IDs belong to a particular branch or customer type.

#### Consistency

Consistency means that the same fact is represented and interpreted consistently across fields, records, sources, and time. Examples include:

- `M` in one source and `Male` in another;
- temperature in Celsius in one table and Fahrenheit in another;
- two systems using different customer identifiers;
- a total that does not equal the sum of its parts.

#### Timeliness

Timeliness measures whether data is sufficiently current for the decision. A perfect balance from yesterday may be useless for a high-frequency trading decision, while a yearly historical record may be perfectly appropriate for a long-term climate study.

#### Validity

Validity means that a value satisfies the permitted domain, format, type, and business rules. Examples include a grade outside the allowed set, a date that cannot exist, a negative quantity where only positive values are allowed, or a string in a numeric field.

#### Uniqueness

Uniqueness means that records are not unnecessarily duplicated and that keys identify the intended entity. Duplicate records can inflate counts and totals, distort frequencies, and create false associations.

#### Redundancy

Redundancy is unnecessary repetition of the same fact. It increases storage and update effort and can create inconsistency. Redundancy can sometimes be intentional for performance, but its source and maintenance rule should be documented.

#### Other practical dimensions

- **Consistency of units and metadata:** all fields need compatible definitions.
- **Lineage:** the source and transformation history should be known.
- **Accessibility:** authorized users should be able to find and use the data.
- **Security and privacy:** sensitive values should be protected and used according to policy.
- **Interpretability:** a value or feature should have a meaningful domain description.

### 3. Quality assessment procedure

A useful audit proceeds in this order:

1. Define the data grain, purpose, required attributes, units, and acceptable rules.
2. Profile row counts, distinct counts, ranges, missingness, duplicates, and distributions.
3. Check referential integrity and joins.
4. Compare source totals with control totals and independent records.
5. Inspect temporal freshness and coverage by subgroup.
6. Investigate anomalies and outliers with the source owner.
7. Record severity, likely cause, proposed treatment, and responsible person.
8. Apply approved rules, retain the original data, and rerun the checks.
9. Publish residual limitations with the analytical dataset.

A quality score can summarize dimensions, but a single average can hide a critical failure. For example, a dataset may score well on accuracy but be unusable if its target labels are 80% missing.

### 4. Data cleaning

Data cleaning detects and corrects or handles errors, missing values, noise, duplicates, and inconsistent representations. A cleaning decision depends on the error mechanism and the analysis goal.

#### 4.1 Missing values

A missing value is different from a measured zero. It may mean unknown, not applicable, not collected, suppressed, or failed. Nulls should be recognized using the source's documented codes, not by guessing from a number such as 0, -1, or 9999.

Common treatments include:

- **Delete the record:** appropriate when the missing field is essential and deletion is unlikely to introduce serious bias.
- **Delete the attribute:** appropriate when it is mostly missing, has no useful definition, or is not needed for the task.
- **Ignore the value:** some algorithms or pairwise calculations can omit it, but the reduction in information must be understood.
- **Impute a constant:** replace missing values with the mean, median, mode, domain value, or a labeled unknown category.
- **Impute from neighbors:** use a nearest-neighbor, interpolation, or carry-forward method when temporal or spatial order makes it defensible.
- **Predict the missing value:** use a model or regression, while avoiding leakage and reporting uncertainty.
- **Add a missingness indicator:** retain the fact that the value was absent, which may itself predict an outcome.

The choice between mean and median depends on distribution. A mean is sensitive to outliers; a median is more robust. A mode is useful for categories but can conceal uncertainty. A missingness indicator can be important when missingness is related to a class or subgroup.

#### 4.2 Noise and measurement error

Noise is variation or corruption that is not part of the meaningful signal. It can arise from sensors, manual entry, inconsistent units, rounding, or changing definitions.

Common methods include:

- **Binning:** sort values into intervals and replace them with a bin representative or smooth boundary.
- **Regression smoothing:** fit a local or global regression and use the fitted value to smooth a noisy measurement.
- **Clustering:** group similar records and replace a noisy value with a cluster summary or identify the outlier.
- **Ensemble or consensus checks:** compare independent sources and investigate disagreement.
- **Range and pattern rules:** reject or flag values outside valid physical or business limits.

Smoothing should not erase a genuine rare event. For example, a sudden temperature spike may be a sensor fault or a real event; the decision requires domain evidence.

#### 4.3 Outliers

An outlier may be an error, an unusual valid observation, or a member of a different population. A useful process is:

1. detect it with a histogram, box plot, IQR rule, z-score, or domain rule;
2. verify the source and measurement conditions;
3. classify it as invalid, valid rare, or uncertain;
4. correct an error only with evidence;
5. retain a valid rare value or analyze it separately;
6. document any exclusion and its effect on the result.

A fraud detector or disease study may need outliers more than an ordinary average model does. “Remove every extreme value” is not a valid general rule.

#### 4.4 Duplicates and inconsistent formatting

Duplicates can be exact copies, repeated business events, or different records for the same entity. Deduplication requires a definition of “same” and usually uses:

- a primary key;
- a composite key;
- fuzzy matching of names and addresses;
- time proximity and transaction amount;
- domain-specific entity resolution.

Formatting cleanup can standardize case, punctuation, dates, currency, units, and category labels. Standardization must not destroy meaningful distinctions. For example, a data dictionary should specify whether “Dr.” is a title, an abbreviation, or a different person category.

### 5. Data integration

Data integration combines data from multiple databases, files, warehouses, APIs, or sensors into a coherent analytical collection. It involves more than appending files.

#### 5.1 Schema matching

A schema describes fields, types, relationships, and constraints. Schema matching determines that fields such as `cust_id`, `customerID`, and `CUSTOMER_KEY` may refer to the same concept. It can use:

- exact names and descriptions;
- data types and formats;
- keys and relationships;
- value distributions;
- metadata and business rules;
- sample matching and user review.

A field-name match alone is not proof. A field called `status` may mean payment status in one system and account status in another.

#### 5.2 Entity resolution and deduplication

Entity resolution decides whether records from different sources describe the same person, product, customer, or event. A record-linkage process can use:

- exact identifiers, such as a verified customer ID;
- blocking by shared attributes to reduce comparisons;
- normalized names, addresses, and phone numbers;
- fuzzy similarity scores;
- transaction, time, or relationship evidence;
- human review for uncertain matches.

False merges create fabricated histories. False non-merges leave duplicate entities. The threshold should reflect the cost of each error and should be monitored.

#### 5.3 Unit and code conversion

Integration often requires conversion between compatible units:

\[
\text{value}_{m} = \text{value}_{cm}/100
\]

Temperature requires an affine conversion, for example:

\[
F = \left(\frac{9}{5}\right)C + 32
\]

A currency conversion requires a rate with a date and source. Converting all monetary values to one currency without retaining the original value, rate, and timestamp can make later reconciliation difficult.

#### 5.4 Conflicting values and data fusion

If two sources disagree, do not silently choose one. Compare timestamps, source authority, measurement uncertainty, and definitions. Possible policies are:

- retain both values and a quality flag;
- choose the authoritative source and record the rejection;
- reconcile the values with a business rule;
- create a conflict queue for review.

Data fusion can combine measurements from multiple sensors, but the fusion rule must reflect uncertainty. A simple average is not appropriate when one sensor is known to be unreliable.

#### 5.5 Integrity after integration

After integration, verify:

- key uniqueness;
- foreign-key validity;
- row counts and totals;
- duplicate rates;
- missingness by source;
- units and ranges;
- temporal alignment;
- referential integrity;
- coverage of intended groups.

A transformed data lake is not integrated merely because its files are in one location.

### 6. Data reduction

Data reduction obtains a smaller or more compact representation while retaining enough information for the intended analysis. It can reduce the number of records, attributes, or levels of detail.

#### 6.1 Sampling

Sampling selects a subset of the population. Important choices include:

- **Simple random sampling:** every record has a known chance of selection.
- **Stratified sampling:** divide the population into meaningful groups and sample within each group.
- **Systematic sampling:** choose every \(k\)-th record after a random starting point.
- **Cluster sampling:** sample groups and then study all or part of the selected groups.
- **Progressive or reservoir sampling:** select records when the full population cannot fit in memory.

A sample must preserve important rare classes and subgroups. If fraud is only 0.1%, a uniform random sample may contain too few fraud cases. Stratified sampling or a carefully designed rare-case sample is needed. Sampling error and the seed or inclusion probability should be recorded.

#### 6.2 Feature selection

Feature selection reduces the number of attributes.

- **Filter methods:** score attributes using correlation, information gain, mutual information, chi-square, or statistical tests. They are fast and do not use the final model.
- **Wrapper methods:** evaluate subsets with a model, such as forward selection, backward elimination, or recursive feature elimination. They can account for interactions but are expensive and may overfit.
- **Embedded methods:** selection occurs during training, for example with L1 regularization or a decision tree.

A useful feature-selection report includes the selected attributes, the selection criterion, validation method, stability across samples, and the reason each feature matters. High correlation does not by itself prove a feature is useless; a correlated variable may be useful as an alternative when one is missing.

#### 6.3 Dimensionality reduction

Dimensionality reduction creates new attributes from combinations or transformations of existing attributes.

**Principal component analysis (PCA)** finds directions of maximum variance. For centered numeric data, compute the covariance or correlation matrix, find its eigenvectors and eigenvalues, and retain the leading components. If the data covariance matrix is \(S\), an eigenvector satisfies

\[
S\mathbf{v}=\lambda\mathbf{v}
\]

The total variance is the sum of eigenvalues. The proportion explained by a component is

\[
\frac{\lambda_j}{\sum_j \lambda_j}
\]

PCA is useful for compression and removing correlated redundancy, but components are combinations and may be difficult to interpret. Standardization is normally important when variables have different units or variances.

Other methods include independent component analysis, nonlinear dimension reduction, and supervised projections. The method should be fit on training data and applied consistently to new data.

#### 6.4 Aggregation and data cubes

Aggregation replaces detailed values with summaries such as daily totals, monthly averages, or counts by category. It can reduce volume greatly:

\[
\text{daily sales}=\sum_{j=1}^{m}\text{sales of transaction }j
\]

A data cube organizes measures by multiple dimensions, such as time, product, and region. Drill-down restores detail, while roll-up increases aggregation. Aggregation is lossy: a monthly total cannot recover individual transaction-level patterns.

### 7. Data transformation

Data transformation changes a representation so that it is more suitable for analysis or modeling. It may preserve, combine, smooth, or generalize values.

#### 7.1 Smoothing

A moving average smooths a noisy numeric sequence:

\[
\hat{x}_t=\frac{1}{2k+1}\sum_{j=-k}^{k}x_{t+j}
\]

For example, the sequence 10, 12, 30, 14, 16 has a central three-term moving average of 18.67 for the middle value when \(k=1\):

\[
(12+30+14)/3=18.67
\]

The smoothed value is not an observation; the original sequence should be retained.

#### 7.2 Aggregation and generalization

Aggregation combines detailed records. Generalization replaces a specific value with a more general concept:

```text
Exact date: 2026-09-24 -> month: 2026-09 -> year: 2026
Exact product: A17-X -> product family: A17 -> category: A
```

Generalization can improve summaries and privacy, but it can hide important differences.

#### 7.3 Normalization and scaling

**Min-max normalization**

\[
x'=\frac{x-\min(x)}{\max(x)-\min(x)}
\]

**Z-score standardization**

\[
z=\frac{x-\mu}{\sigma}
\]

**Decimal scaling**

\[
x'=\frac{x}{10^j}
\]

where \(j\) makes the largest absolute value less than 1.

**Logarithmic transformation**

\[
x'=\log_b(x)
\]

for positive skewed values. It reduces right skew and can make multiplicative relationships more visible. It cannot directly handle zero or negative values without a justified offset or other treatment.

The choice depends on the algorithm and the desired interpretation. A tree may not need min-max scaling, while a distance-based or gradient-based method often benefits from it. Scale parameters must be learned from training data.

#### 7.4 Attribute construction

New features can be derived from existing attributes:

\[
\text{profit}=\text{revenue}-\text{cost}
\]

\[
\text{profit margin}=\frac{\text{profit}}{\text{revenue}}
\]

\[
\text{attendance rate}=\frac{\text{classes attended}}{\text{classes held}}
\]

Derived features should be documented, checked for division by zero and missing inputs, and evaluated for leakage. A feature containing future information cannot be used during historical prediction.

#### 7.5 Transformation validation

After transformation, compare distributions, ranges, missingness, group effects, and correlations with the original data. Check that totals, identities, units, and timestamps still make sense. A transformation can improve a model's numerical behavior while harming interpretability or fairness.

### 8. Discretization

Discretization converts a continuous numerical attribute into intervals or categories. It can reduce the number of possible values, make rules easier to read, support concept hierarchies, and help methods that work well with categorical data.

#### 8.1 Equal-width bins

Divide the numeric range into intervals of equal width:

\[
\text{width}=\frac{x_{\max}-x_{\min}}{k}
\]

#### 8.2 Equal-frequency bins

Divide the data into \(k\) bins so that approximately the same number of records falls in each bin. This can be better for skewed data, but repeated values can make exact equal frequencies difficult.

#### 8.3 Data-driven or optimal discretization

Methods such as histograms, decision trees, clustering, correlation analysis, and information gain choose boundaries according to the data distribution or task. The method should be fit on training data if the resulting categories are used by a predictive model.

#### 8.4 Binning and smoothing

Binning maps values to intervals or representative values. A histogram can be smoothed by:

- averaging neighboring bins;
- merging sparse adjacent bins;
- using a fitted curve or density estimate;
- removing very small bins and reporting them as an “other” group.

Smoothing may hide rare but important regions. An “other” category should retain a count and domain interpretation.

#### 8.5 Information and loss

A discretized value \(t\) is associated with an interval \(I_t\). The information gain of a split \(T\) is

\[
IG(T)=Entropy(S)-\sum_{t\in T}\frac{|S_t|}{|S|}Entropy(S_t)
\]

where \(S_t\) is the subset in interval \(I_t\). In a supervised task, boundaries should be evaluated using the target; in an unsupervised task, they may be chosen to preserve density or cluster structure.

Discretization is lossy. A high-value outlier may be placed in the same interval as ordinary values, and two nearby values can be separated by a boundary. Boundaries, inclusion rules, and treatment of missing values must be recorded.

### 9. Concept hierarchy generation

A **concept hierarchy** organizes specific concepts into increasingly general concepts. It supports abstraction, multidimensional summaries, and queries at different levels.

Example:

```text
Specific: red mobile phone
Level 1:  mobile phone
Level 2:  electronic product
Level 3:  retail product
```

A time hierarchy is:

```text
2026-09-24 -> September 2026 -> Q3 2026 -> 2026
```

#### 9.1 Sources of concept hierarchy

- **Background knowledge:** an expert states that a city belongs to a state and a state belongs to a country.
- **Taxonomy or schema:** an enterprise system already provides product or organization categories.
- **Attribute discretization:** continuous age, income, or time values are grouped into meaningful levels.
- **Data-driven induction:** frequent patterns, clustering, or association analysis reveal groups and abstractions.
- **Data cubes:** precomputed hierarchies support roll-up and drill-down.

#### 9.2 Total and partial orders

A **total ordering** gives a strict sequence from specific to general, such as a date hierarchy. A **partial ordering** allows branches: a product may belong to one category, and a city may belong to a region through a different hierarchy. A concept hierarchy can therefore be a tree, DAG, or other structure rather than one linear list.

#### 9.3 Step-by-step generation

1. List distinct values and their frequencies.
2. Define the intended question and level of abstraction.
3. Identify shared properties or domain relationships.
4. Group values with a justified rule.
5. Name each group so its meaning is clear.
6. Check coverage, overlap, and consistency.
7. Repeat the process to create higher levels if needed.
8. Validate the hierarchy with domain experts and representative data.
9. Store the mapping and version used for each transformed dataset.

#### 9.4 Example hierarchy generation

Raw product values:

```text
A17-R, A17-B, A19-R, B10-X, B10-B, C05-R
```

A domain rule might group them by first-level product family:

```text
A17: A17-R, A17-B
A19: A19-R
B10: B10-X, B10-B
C05: C05-R
```

A higher level might group A17 and A19 under `A-series`, B10 under `B-series`, and C05 under `C-series`. The grouping is not forced by the codes; it is supported by product metadata. If the suffix is a color, the hierarchy should not accidentally treat color as a product family.

#### 9.5 Privacy and granularity

More detailed hierarchies can identify individuals or rare combinations. Generalization can protect privacy but reduce analysis value. Before publishing a hierarchy, test rare combinations, small cells, and re-identification risk. A hierarchy should not be chosen only because it makes a chart look simpler.

### 10. End-to-end preprocessing principles

Preprocessing should be:

- **purpose-driven:** linked to a task and decision;
- **documented:** every rule and parameter is recorded;
- **repeatable:** the same process produces the same result;
- **validated:** checks compare output with input and control totals;
- **provenance-aware:** the original data and transformation lineage remain accessible;
- **privacy-aware:** detail is shared only when appropriate;
- **reversible where possible:** transformations can be audited or reversed;
- **evaluated:** preprocessing is judged by data quality and downstream performance, not by how many operations were performed.

## Worked examples

### Example 1: A quality audit

A student table contains:

```text
Roll | Name  | Branch | Age | Marks | Timestamp
1    | Asha  | CSE    | 21  | 78    | 2026-09-01
2    | Bilal | ECE    | -1  | 64    | 2026-09-01
3    | Asha  | CSE    | 21  | 78    | 2026-09-01
4    | Divya | ME     | 22  | 999   | 2026-09-02
5    | Raj   | CSE    | 20  | 72    | 2026-09-02
6    | Asha  | CSE    | 21  | 78    | 2026-09-01
```

The audit finds:

- Age `-1` is a missing-value code, not a real age.
- Roll 1, 3, and 6 are likely duplicates.
- Marks 999 violates a 0–100 rule.
- One source may use a different branch code; verify the code list before integration.
- The timestamp range and expected row count should be checked.

A responsible treatment is to recover the duplicate key, replace the sentinel with a missing marker, investigate 999 with the source, and retain an audit record. The analyst should not simply change 999 to 78 because it looks plausible.

### Example 2: Missing-value imputation

A small training set of marks is:

```text
50, 60, 70, 80, 100
```

The mean is

\[
\bar{x}=\frac{360}{5}=72
\]

If a sixth value is missing, mean imputation gives 72. A median-based rule gives 70. If the missing value is more common among high-performing students, mean or median imputation may understate the group. A missingness indicator can preserve the fact that the observation was incomplete.

For a time series of daily sales:

```text
100, 110, 105, 108
```

a missing value on day 4 could be linearly interpolated between 105 and the following observed value, but only if the value is genuinely unavailable rather than a business event that produced zero sales. The chosen rule should be recorded.

### Example 3: Binning and smoothing noisy measurements

A sensor reports:

```text
10, 12, 11, 40, 13, 12, 11
```

A three-bin method could group nearby values, but first verify whether 40 is a sensor fault. If it is confirmed as a real spike, binning it together with 10–13 would hide a meaningful event. If it is a fault, replace or flag it using the source's calibration rule. A histogram can suggest the grouping, but domain validation decides the treatment.

### Example 4: Integration of two customer sources

Source A:

```text
C001 | Asha | CSE | Pune
C002 | Bilal | ECE | Delhi
```

Source B:

```text
customer_key | full_name | city
K01           | Asha      | Pune
K02           | Bilal     | New Delhi
```

A mapping table can connect `C001` to `K01` and `C002` to `K02`. Before joining, standardize city labels: `Delhi` and `New Delhi` may be aliases, but this must be verified. A name-only match could incorrectly merge two people. The join should retain both original identifiers and a confidence or review flag.

### Example 5: Unit conversion and control total

One sales system stores weight in kilograms and another in grams.

```text
2 kg = 2000 g
```

If 500 records have average weight 2 kg, the total is

\[
500\times2=1000\text{ kg}=1{,}000{,}000\text{ g}
\]

After conversion, compare the integrated total with the source control total. Do not convert a value twice or mix kilograms and grams in the same field.

### Example 6: Sampling a rare class

A fraud dataset has 1,000,000 transactions and only 1,000 frauds, a prevalence of 0.1%. A simple random sample of 10,000 would be expected to contain about 10 fraud cases, but the count can vary. Stratified sampling can preserve the 1,000-fraud group and sample a controlled number from the non-fraud group. The resulting prevalence is intentionally changed for model development, so evaluation must restore the real class prevalence or use appropriate weighting.

### Example 7: Feature selection

Suppose a loan model has:

```text
income, debt_ratio, age, number_of_address_changes, customer_id, random_comment
```

Correlation and missingness checks may identify `customer_id` and `random_comment` as unstable or irrelevant. A wrapper method can test whether removing them improves validation performance without harming interpretability. The final model should be tested on a new sample because repeated feature search can overfit the validation data.

### Example 8: PCA calculation outline

Consider two centered numeric features with a covariance matrix:

```text
       Feature1 Feature2
F1        2.0      1.0
F2        1.0      2.0
```

The characteristic equation is

\[
\det(S-\lambda I)=(2-\lambda)^2-1=0
\]

so the eigenvalues are \(\lambda_1=3\) and \(\lambda_2=1\). The total variance is 4, so retaining the leading component preserves

\[
\frac{3}{4}=0.75
\]

or 75% of the total variance. The second component preserves 25%. The first component is the direction in which the two correlated features vary together most strongly. This calculation is valid because the supplied matrix is positive semidefinite; every covariance matrix should be checked for valid eigenvalues before components are interpreted.

### Example 9: Min-max and z-score transformation

Marks are \(40, 50, 60, 70, 80\).

- Minimum = 40; maximum = 80.
- Mean = 60.
- Sample standard deviation = \(\sqrt{1000/4}\approx15.81\).

Min-max values:

```text
40 -> 0.00
50 -> 0.25
60 -> 0.50
70 -> 0.75
80 -> 1.00
```

Z-scores:

```text
40 -> -1.26
50 -> -0.63
60 ->  0.00
70 ->  0.63
80 ->  1.26
```

Min-max preserves the ordering and gives a fixed [0,1] range for this sample. Z-scores express each value in training-standard-deviation units and are not bounded by 1.

### Example 10: Attribute construction

A retailer has:

```text
revenue = 500
cost = 350
returns = 20
```

Derived features are:

\[
\text{gross profit}=500-350=150
\]

\[
\text{profit margin}=150/500=0.30
\]

\[
\text{return rate}=20/500=0.04
\]

The definitions, denominator safeguards, currency, and time period must be documented. A future return amount must not be included when predicting a customer's current behavior.

### Example 11: Equal-width discretization

Attendance values range from 40% to 100%, and three equal-width bins are requested.

\[
\text{width}=\frac{100-40}{3}=20
\]

Using a documented boundary convention:

```text
40–59.999... : low
60–79.999... : medium
80–100       : high
```

The interval at the exact boundary must be assigned once, not to two bins. A student with 60% is medium in this scheme; a different convention must be reported if the analyst chooses different boundaries.

### Example 12: Equal-frequency discretization

Suppose ten sorted attendance values are:

```text
41, 45, 49, 52, 58, 63, 68, 75, 84, 97
```

For three approximately equal-frequency groups, one possible grouping is:

```text
low:  41, 45, 49
mid:  52, 58, 63
high: 68, 75, 84, 97
```

Repeated values can make exact equal counts difficult, and the grouping is a representation change. The high group still contains a very wide range, so it should not be treated as more precise than the original data.

### Example 13: A concept hierarchy from age

Raw ages:

```text
6, 18, 40
```

Using one documented domain hierarchy:

```text
6   -> child -> person
18  -> adult -> person
40  -> senior -> person
```

A different study might combine 6 and 18 into `young person` and leave 40 as `older person`, but that rule must be stated explicitly. The labels are not forced by the numeric values; they are domain definitions, and every level should have a clear meaning.

### Example 14: A complete preprocessing pipeline

A retailer wants to predict repeat purchases.

1. **Define grain and target:** one customer-month record; target is a purchase in the next 30 days.
2. **Quality:** check customer ID completeness, timestamp validity, duplicate orders, currency, and label delay.
3. **Clean:** remove duplicate event keys, flag impossible quantities, impute or model missing spend carefully, and add a missingness indicator.
4. **Integrate:** map customer IDs across orders and web events, convert currency using dated rates, and resolve duplicates.
5. **Reduce:** use stratified sampling for development, remove unstable identifiers, and select useful behavioral features.
6. **Transform:** derive spend per visit, days since last purchase, and average basket value; standardize numeric features for a distance-sensitive model.
7. **Discretize:** create recency bands if interpretable rules are important, while retaining continuous features for a model that needs them.
8. **Build hierarchies:** organize product categories and time for roll-up reports.
9. **Validate:** check totals, distributions, subgroup performance, leakage, and a time-based test set.
10. **Deploy with monitoring:** detect drift in customer behavior and changes in missingness.

This sequence makes clear that reduction, transformation, and discretization are choices tied to the task, not mandatory steps that must destroy information.

## Key terms & formulas

- **Data preprocessing:** preparation of data for mining through quality assessment, cleaning, integration, reduction, transformation, discretization, and hierarchy organization.
- **Data quality:** the degree to which data is fit for its intended use.
- **Accuracy:** correctness of a value relative to reality or an authoritative source.
- **Completeness:** presence of required records and attributes.
- **Consistency:** agreement of representation and meaning across records and sources.
- **Timeliness:** currency of data relative to its use.
- **Validity:** conformance to permitted types, formats, and domain rules.
- **Uniqueness:** absence of unintended duplicate entities or records.
- **Redundancy:** unnecessary repetition of information.
- **Missing value:** a value that is unavailable, unknown, not applicable, or not recorded; it is not automatically zero.
- **Imputation:** replacement of a missing value with an estimated or domain value.
- **Noise:** erroneous or irrelevant variation in data.
- **Outlier:** an unusually distant observation that may be erroneous or valid.
- **Binning:** grouping values into intervals.
- **Regression smoothing:** replacing or adjusting a value using a fitted regression.
- **Clustering-based cleaning:** identifying noisy records or imputing values using similar groups.
- **Data integration:** combining data from multiple sources into a coherent representation.
- **Schema matching:** identifying corresponding fields or concepts across schemas.
- **Entity resolution:** determining whether records represent the same real-world entity.
- **Data fusion:** combining measurements or records using a defined conflict and uncertainty policy.
- **Data reduction:** obtaining a smaller representation while preserving useful information.
- **Sampling:** selecting a subset of records.
- **Stratified sampling:** sampling within defined subgroups.
- **Feature selection:** choosing a subset of attributes.
- **Filter method:** feature ranking independent of the final model.
- **Wrapper method:** feature subset evaluation with a chosen model.
- **Embedded method:** feature selection during model training.
- **Dimensionality reduction:** transformation to fewer attributes.
- **PCA:** orthogonal directions of maximum variance; eigenvectors satisfy \(S\mathbf v=\lambda\mathbf v\).
- **Aggregation:** combining detailed values into summaries.
- **Data transformation:** changing a representation for analysis.
- **Smoothing:** reducing short-term variation.
- **Generalization:** replacing a detailed concept with a broader concept.
- **Normalization:** mapping values using a chosen range or scale.
- **Min-max normalization:** \(x'=(x-\min)/(\max-\min)\).
- **Z-score standardization:** \(z=(x-\mu)/\sigma\).
- **Decimal scaling:** \(x'=x/10^j\).
- **Log transformation:** \(x'=\log_b(x)\), for valid positive values.
- **Discretization:** conversion of continuous values into intervals or categories.
- **Equal-width discretization:** bins with approximately equal numeric width.
- **Equal-frequency discretization:** bins with approximately equal numbers of records.
- **Concept hierarchy:** an organization of specific concepts into more general concepts.
- **Total order:** one ordered chain of abstraction levels.
- **Partial order:** branching abstraction relationships.
- **Roll-up:** movement from detail to a more general summary.
- **Drill-down:** movement from a general summary to detail.
- **Provenance:** information about the source and transformation history of data.
- **Entropy:** uncertainty in a set; for a target distribution \(p_i\),

\[
H=-\sum_i p_i\log p_i
\]

- **Information gain for a split:**

\[
IG(T)=H(S)-\sum_{t\in T}\frac{|S_t|}{|S|}H(S_t)
\]

## Common mistakes

1. **Cleaning before understanding the data.** A value such as `-1` may be a missing code, not a negative age. First consult the data dictionary and business rules.
2. **Treating all missing values as zero.** Unknown, not applicable, and observed zero have different meanings.
3. **Choosing mean imputation without checking skewness and missingness mechanism.** A median or model-based method may be safer.
4. **Deleting all outliers.** An outlier may be an error, a rare event, or the most important observation. Investigate and document.
5. **Replacing a value with a plausible guess without provenance.** The analyst must know that it was imputed and why.
6. **Joining files without matching units and keys.** A text join can create false records or incorrect totals.
7. **Using a name alone to resolve entities.** Two people can share a name, and one person can change a name.
8. **Sampling without preserving rare classes or important subgroups.** The sample may be fast but statistically useless for the target task.
9. **Selecting features using the test set.** Feature selection must use training and validation information only.
10. **Applying min-max or z-score to the whole dataset before splitting.** This leaks test information.
11. **Using dimensionality reduction without reporting explained variance and interpretability.** A smaller representation may discard a minority pattern.
12. **Assuming aggregation is reversible.** A monthly total cannot recover the original transactions.
13. **Choosing discretization boundaries only for a tidy chart.** Boundaries should reflect data, domain meaning, and the task.
14. **Calling arbitrary value grouping a concept hierarchy.** A valid hierarchy needs meaningful levels and a documented relationship.
15. **Using a log transformation on zero or negative data without a justified rule.** The logarithm is undefined there.
16. **Assuming preprocessing improves every downstream result.** Evaluate quality, task performance, subgroup effects, and cost.
17. **Forgetting leakage checks.** A feature containing future information can make validation and deployment results invalid.
18. **Discarding raw data.** Retain a protected, access-controlled original so transformations can be audited or repeated.

## Exam prep

### Likely 2-mark questions

1. **What is data preprocessing?**  
   *Hint:* The process of assessing and preparing data for mining through cleaning, integration, reduction, transformation, discretization, and hierarchy generation.

2. **Name six data-quality dimensions.**  
   *Hint:* Accuracy, completeness, consistency, timeliness, validity, uniqueness, and possibly redundancy.

3. **What is a missing value?**  
   *Hint:* A value that is unavailable, unknown, not applicable, or not recorded; it is not automatically zero.

4. **Give three missing-value treatments.**  
   *Hint:* Delete the record or attribute, impute the mean/median/mode, use neighbors or a model, or add a missingness indicator.

5. **Define an outlier and one handling method.**  
   *Hint:* An unusually distant value; investigate it and use binning, regression, clustering, correction, or separate analysis depending on the cause.

6. **What is data integration?**  
   *Hint:* Combining data from multiple sources while reconciling schemas, identifiers, units, formats, duplicates, and conflicts.

7. **Define entity resolution.**  
   *Hint:* Determining whether records from different sources represent the same real-world entity.

8. **What is data reduction?**  
   *Hint:* Obtaining a smaller representation using sampling, feature selection, dimensionality reduction, or aggregation.

9. **Differentiate filter and wrapper feature selection.**  
   *Hint:* Filter methods rank features independently; wrapper methods evaluate subsets using a model.

10. **What is PCA?**  
    *Hint:* A dimensionality-reduction method that creates orthogonal linear combinations of numeric attributes with maximum variance.

11. **What is data transformation?**  
    *Hint:* Changing a representation using smoothing, aggregation, generalization, normalization, scaling, or attribute construction.

12. **Write the min-max normalization formula.**  
    *Hint:* \(x'=(x-\min(x))/(\max(x)-\min(x))\).

13. **Define discretization.**  
    *Hint:* Converting continuous numerical values into intervals or categories.

14. **Differentiate equal-width and equal-frequency discretization.**  
    *Hint:* Equal width divides the numeric range; equal frequency aims for similar record counts per bin.

15. **What is a concept hierarchy?**  
    *Hint:* A structure that organizes detailed concepts into more general levels.

16. **Give two sources of a concept hierarchy.**  
    *Hint:* Background knowledge, taxonomy, discretization, data-driven induction, or a data cube.

17. **What is provenance?**  
    *Hint:* Information about a value's source and transformation history.

18. **Why is leakage a preprocessing problem?**  
    *Hint:* Future or test-only information can enter scaling, feature selection, or imputation and make evaluation overly optimistic.

### Likely long-answer questions

1. **Explain data quality dimensions and how they are assessed.**  
   **Answer hint:** Define accuracy, completeness, consistency, timeliness, validity, uniqueness, and redundancy. Describe profiling, control totals, constraints, subgroup checks, lineage, and why a single average quality score is insufficient.

2. **Explain missing data, noise, outliers, and cleaning methods.**  
   **Answer hint:** Distinguish missingness codes from zero, discuss missingness mechanisms, deletion and imputation, binning, regression and clustering, outlier investigation, duplicate removal, and preservation of the original values and audit trail.

3. **Describe data integration and entity resolution with a concrete example.**  
   **Answer hint:** Cover schema matching, key and value mapping, unit conversion, blocking, fuzzy or exact entity resolution, conflict policies, false merges and misses, and post-integration integrity checks.

4. **Explain sampling, feature selection, and dimensionality reduction for data reduction.**  
   **Answer hint:** Compare simple, stratified, systematic, and cluster sampling; filter, wrapper, and embedded selection; PCA equations and explained variance; aggregation and data cubes; and the information lost by each method.

5. **Explain data transformation with formulas and examples.**  
   **Answer hint:** Cover smoothing, aggregation, generalization, min-max, z-score, decimal scaling, logarithm, and derived attributes. Explain how training data, units, zeros, leakage, and interpretability affect the choice.

6. **Explain discretization methods and their limitations.**  
   **Answer hint:** Give equal-width and equal-frequency steps, compare data-driven methods, explain bin boundaries and repeated values, show information gain, and discuss lost resolution, rare values, and target leakage.

7. **Explain concept hierarchy generation with a step-by-step example.**  
   **Answer hint:** Define the specific concept, generalize values, create levels, distinguish total from partial order, use background knowledge or data-driven induction, validate coverage and meaning, and discuss privacy.

8. **Design an end-to-end preprocessing pipeline for a real problem.**  
   **Answer hint:** State the task and grain, list quality checks, cleaning and integration rules, reduction and transformation choices, discretization or hierarchy decisions, validation metrics, provenance, leakage controls, and monitoring.

9. **Compare a raw dataset with a preprocessed dataset and evaluate the trade-offs.**  
   **Answer hint:** Quantify missingness, duplicates, scale, dimensionality, runtime, and downstream accuracy or interpretability. Explain which information was preserved, discarded, or made less certain and how this should be reported.

10. **Discuss why preprocessing can introduce bias and harm.**  
    **Answer hint:** Explain nonrepresentative sampling, differential imputation, incorrect entity merges, overgeneralization, lossy discretization, proxy features, unequal error costs, privacy risk, and the need for subgroup validation and documentation.
