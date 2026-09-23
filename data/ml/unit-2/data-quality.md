---
subject: ml
unit: 2
topic: data-quality
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Data Quality

## Overview

Data quality asks whether data is fit for the purpose of a particular ML task. Quality is not an absolute property of a table: a value may be adequate for a broad trend and inadequate for an individual medical decision. A high-quality data set is accurate enough, complete enough, consistent, valid, timely, representative, and documented for its intended use.

The main idea is **fitness for purpose**. Before deleting or repairing anything, define the required meaning, population, time, and tolerance for error. The same missing value may be harmless for a descriptive chart and unacceptable for a regulated decision.

## Explanation

### Dimensions of data quality

1. **Accuracy:** values represent the real-world facts they claim to represent. Accuracy may be checked against trusted sources or known process rules.
2. **Completeness:** required fields and relevant cases are present. Completeness includes coverage of important groups and time periods, not only a high row count.
3. **Consistency:** the same concept is represented consistently across tables, systems, and records. Examples include a country code changing from ISO to a local abbreviation without a mapping.
4. **Uniqueness:** records are not duplicated unless repeated events are meaningful. A unique key is a tool for checking, not proof that every field is correct.
5. **Validity:** values obey the permitted type, format, range, and business rules. A negative age or a percentage of 250% may be invalid.
6. **Accuracy of labels:** targets are defined consistently and reflect the intended concept, not a careless proxy.
7. **Timeliness:** data is current enough for the decision and available when needed.
8. **Representativeness:** the sample covers the intended population and operating conditions.
9. **Traceability:** source, transformations, version, and access history are known.
10. **Security and privacy:** unauthorised disclosure or misuse is prevented.

### Detecting quality problems

Use schema checks, type and range validation, uniqueness tests, cross-field rules, duplicate detection, missingness profiles, distribution comparisons, and source reconciliation. Compare training data with the live production stream. A sudden change in a feature may be a quality problem, a real event, or both.

**Cross-field example:** if `end_date < start_date`, the record is invalid. If `status = completed` but `completion_date` is missing, the record may be incomplete. A customer ID found in one table but not another is not necessarily bad; the relationship must be defined.

### Labels and target quality

Label quality has several layers:

- **Definition:** what exactly is the target?
- **Measurement:** how was it observed or annotated?
- **Consistency:** do different annotators use the same standard?
- **Coverage:** are all important cases eligible for the label?
- **Timing:** is the label available at the intended training cutoff?
- **Noise:** how often is it wrong or uncertain?

For weak labels, measure the relationship between the proxy and the true target. If “click” stands for “purchase”, a click is noisy and exposure-biased. For medical labels, compare expert agreement and clinical outcomes. A high volume of labels does not remove systematic bias.

### Missing data

Missingness may be:

- **MCAR (missing completely at random):** unrelated to observed or unobserved values.
- **MAR (missing at random):** related to observed variables but not the unobserved value, conditional on those variables.
- **MNAR (missing not at random):** related to the missing value itself.

These descriptions help choose an analysis strategy but are assumptions, not labels that can be proven from a table alone. Add a missing indicator when missingness itself is meaningful. Compare model results with and without missing rows; report the number and reason for exclusion.

### Duplicates and inconsistent records

Exact duplicates may be repeated exports; near duplicates may be different people with similar attributes. Deduplication rules need a key or domain knowledge. Removing a duplicate can alter class balance and time order. Keep an audit trail of rows removed and why.

### Data quality and fairness

A group missing from a dataset is invisible to average quality statistics. Report completeness, error, and coverage by relevant subgroup. A model can be technically accurate because the difficult cases were not recorded. Quality assessment therefore includes whose experiences are represented and whose are absent.

### Data quality versus cleaning

Cleaning is a set of actions, not a definition of quality. Over-cleaning can delete minority cases, smooth away legitimate variation, or impose a preferred answer. Every rule should have a purpose, an owner, and a record. If the source system is wrong, repairing a local copy only hides the problem.

### A quality scorecard

A team can define:

- required-field completeness and validated range;
- duplicate rate per entity/time;
- label agreement and delayed-label rate;
- source-to-target reconciliation difference;
- freshness and ingestion delay;
- subgroup coverage and error disparities;
- percentage of records with unknown or imputed values.

The scorecard should be tracked over time, not checked once. Quality is a property of the data pipeline and the application.

### Measuring quality over the lifecycle

Data quality should be assessed continuously, not only before the first training run. At ingestion, validate schema, ranges, units, and freshness. During transformation, monitor row counts, join multiplicity, missingness, and category drift. Before release, compare the evaluation data with production data and check subgroup coverage. After deployment, track the rate of missing, invalid, out-of-range, unknown-category, and late-arriving values.

A quality incident should have a clear response: pause a pipeline, quarantine records, repair the source, rerun validation, notify affected owners, and document which model versions were trained on bad data. Remediation is not complete merely because the table loads. The repaired data must be compared with the original to ensure that a fix did not create a new bias or remove a legitimate rare case.

## Worked examples

### Example 1: customer table

Customer age is stored as text, with values `"25"`, `"25.0"`, `"unknown"`, and `"-"`. Converting blindly produces a spurious zero or a parsing error. The team normalises valid values, maps explicit unknowns to missing, validates age range, and reports how many records changed. A missing indicator is retained because unknown age may relate to a customer segment.

### Example 2: transaction duplicates

A retried payment request appears twice with the same transaction ID. The business system says one is a retry, so it is marked as a duplicate event. Dropping every repeated row would remove valid split payments; the key and event semantics are required.

### Example 3: label noise

Two doctors label the same scan differently for borderline cases. The team creates an explicit uncertain label, measures agreement, and reports performance separately for clear and difficult cases. Hiding the disagreement would make a classifier look falsely precise.

### Example 4: freshness

A product recommendation model uses inventory values that refresh once a day, but the service requests predictions every minute. The model is accurate for demand but receives stale stock features. The quality issue is timeliness, not the classifier.

## Key terms & formulas

- **Data quality:** fitness of data for a defined purpose.
- **Accuracy:** closeness of a value to the truth.
- **Completeness:** presence of required fields and relevant cases.
- **Consistency:** compatible meaning and format across records.
- **Validity:** conformance to type, range, and business rules.
- **Uniqueness:** absence of unintended duplicate records.
- **Timeliness:** currency and availability of data for the decision.
- **Representativeness:** coverage of the intended population.
- **Provenance:** origin and lineage of data.
- **Data dictionary:** documented field definitions and rules.
- **Schema:** structure, types, and constraints.
- **Target quality:** correctness and meaningfulness of labels.
- **MCAR/MAR/MNAR:** standard descriptions of missingness mechanisms.
- **Data quality scorecard:** tracked measures of quality dimensions.
- **Audit trail:** record of changes and exclusions.

## Common mistakes

1. **Equating a complete table with high quality.** A full table can be biased, stale, or incorrectly labelled.
2. **Deleting every outlier.** An unusual value may be the important case.
3. **Imputing without recording the imputation.** Analysts cannot reproduce the result.
4. **Using row counts alone.** Coverage and subgroup representation matter.
5. **Fixing errors without preserving the raw source.** Remediation becomes opaque and irreversible.
6. **Ignoring label agreement.** A target can be consistently wrong.
7. **Cleaning until validation looks good.** This is selection bias if the rules use test information.

## Exam prep

### Likely 2-mark questions

- **Define data quality.** The degree to which data is fit for a specified purpose.
- **Name four quality dimensions.** Accuracy, completeness, consistency, validity, timeliness, representativeness, or uniqueness.
- **What is a data dictionary?** A document defining fields, types, units, meanings, and allowed values.
- **Why is label quality important?** Incorrect or inconsistent targets make the model learn the wrong concept.

### Long-answer prompts

- **Explain the dimensions of data quality.** Use examples from healthcare, retail, or finance and state how each is assessed.
- **How would you diagnose missing data?** Compare missingness across groups, identify its mechanism, compare imputation strategies, and document limitations.
- **Distinguish data quality from data preprocessing.** Quality assessment diagnoses fitness; preprocessing transforms usable data.
- **Design a data-quality scorecard for a hospital model.** Include completeness, validity, label agreement, timeliness, subgroup coverage, and monitoring.
