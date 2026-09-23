---
subject: ml
unit: 2
topic: data-remediation
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Data Remediation

## Overview

Data remediation is the process of correcting, supplementing, standardising, or safely removing data problems so that it becomes fit for an intended ML task. It is more than deleting bad rows. Remediation may involve fixing a source system, resolving contradictory records, imputing a value, merging mappings, collecting new data, or documenting why an error cannot be repaired.

The central rule is to preserve evidence. Keep the original data, record the problem and rule applied, and test the effect of each repair. Aggressive remediation can create a clean-looking data set that is less truthful than the original.

## Explanation

### A remediation workflow

1. **Define rules and scope:** state the purpose, source, allowable values, and severity of each issue.
2. **Profile the issue:** count, locate, and characterise errors; determine whether they are random or systematic.
3. **Trace the source:** identify whether the problem arose during collection, transfer, storage, join, or annotation.
4. **Choose a response:** correct, impute, exclude, recode, quarantine, or collect again.
5. **Apply reproducibly:** use versioned code or a documented mapping table.
6. **Validate:** rerun schema, range, consistency, and representativeness checks.
7. **Assess impact:** compare model and subgroup results with and without the repair.
8. **Document and monitor:** record assumptions, exclusions, and unresolved uncertainty.

### Correcting values and formats

Typical corrections include trimming accidental whitespace, normalising case and units, mapping aliases to canonical categories, fixing date formats, and correcting impossible values. A rule such as “convert ‘M’ to ‘male’” is unsafe unless the source definition is known; `M` could mean something else.

Use validation after correction:

\[
\text{valid}(x)=
\begin{cases}
1,&\text{if }x\text{ satisfies the documented rule},\\
0,&\text{otherwise}.
\end{cases}
\]

For numeric ranges, define the unit and allowed uncertainty. Do not clip a value merely because it is extreme; first determine whether it is a unit error, a legitimate rare case, or a failed sensor.

### Handling missing data

Options include:

- **complete-case deletion:** simple but can bias results if missingness is systematic;
- **mean/median/mode imputation:** fills a value with a summary, reducing variance and ignoring uncertainty;
- **model-based imputation:** predicts missing values from other features and may be useful when assumptions hold;
- **missing indicators:** tells the model that a value was absent;
- **special missing categories:** sometimes valid for categorical fields;
- **collect more data:** often the best remedy for important missingness.

For numerical feature \(x_j\), mean imputation is

\[
\hat x_{ij}=\bar x_j
\]

for missing values, optionally with \(m_{ij}=1\) when \(x_{ij}\) is missing. Imputation parameters must be estimated on training data only. For prediction-time missingness, the production system must apply the same policy.

### Duplicates and entity resolution

Exact duplicate keys can be detected with a hash or group-by. Near duplicates require matching on stable fields and tolerances. A merge can create false links when people share a name or a sensor reports identical values. Keep provenance, compare confidence, and avoid automatically collapsing records when the event granularity is unknown.

### Outliers and anomalies

An outlier is context-dependent. Use robust rules such as the interquartile range,

\[
IQR=Q_3-Q_1,
\]

or median absolute deviation, but treat a flagged value as a question:

- Is it a data-entry or unit error?
- Is it a valid rare event?
- Does it represent a failure of the sensor or process?
- Is it important for the decision?

Correct, retain, cap, or exclude only with a documented rationale. Removing difficult cases can make a model look better while making it less useful.

### Inconsistent categories and schema

Canonical mappings can reconcile “USA,” “US,” and “United States” only when the source definitions agree. Keep an unknown category for new values and monitor its frequency. Schema changes—renamed fields, new units, altered codes—should be versioned and tested against existing pipelines.

### Label remediation

Labels require special care. Establish a definition, obtain expert adjudication for disagreements, preserve uncertainty, and measure inter-annotator agreement. If the target is inherently ambiguous, use soft labels or a “review” category instead of forcing false precision. Correcting only examples that the current model gets wrong creates label leakage.

### Missing or broken remediation for high-stakes data

When a source is untrustworthy, quarantining records is safer than guessing. A bank may route uncertain identity records to manual review; a hospital may refuse a model update until a critical feature is validated. No imputation can recover an observation that was never collected.

### Remediation and model fairness

A repair rule can affect groups differently. Mean imputation may erase a missingness signal for one group but not another. Duplicate removal may disproportionately delete low-volume records. Check missingness, errors, and model performance by subgroup before and after remediation. A rule is not neutral merely because it is automated.

## Worked examples

### Example 1: unit correction

Temperatures are stored in Celsius for one source and Fahrenheit for another. The team confirms the source definition, converts Fahrenheit to Celsius,

\[
C=(F-32)\times \frac{5}{9},
\]

and stores the original value plus a source flag. It validates physically plausible ranges and checks that the distribution no longer contains impossible values.

### Example 2: missing income

A loan application has missing income. The team keeps an `income_missing` indicator, uses the training-set median within each documented broad category, and checks whether a model relying on the indicator has worse subgroup calibration. It does not use a value calculated from the test set.

### Example 3: outlier decision

A network sensor reports 5 requests per second in every normal period and 5,000 in one period. The team checks whether a maintenance job caused it. It keeps the raw record, marks it as a sensor/event status, and prevents a corrupted status field from training an ordinary normal-operation model.

### Example 4: conflicting labels

Two reviewers disagree on 30 borderline images. The lead reviewer adjudicates according to a written rubric, records both original decisions, and reports performance separately on the uncertain subset. The model is not rewarded for guessing a label that has no agreed meaning.

## Key terms & formulas

- **Remediation:** actions that make data fit for use.
- **Data cleansing:** correcting or removing errors and inconsistencies.
- **Imputation:** replacing a missing value with an estimate.
- **Complete-case deletion:** retaining rows with no missing required field.
- **Missing indicator:** binary feature marking imputation.
- **Canonical mapping:** agreed representation for equivalent labels.
- **Entity resolution:** identifying records that refer to the same entity.
- **IQR outlier rule:** flag values below \(Q_1-1.5IQR\) or above \(Q_3+1.5IQR\).
- **Median absolute deviation:** robust spread based on absolute deviations from the median.
- **Quarantine:** isolate questionable records for review.
- **Label adjudication:** expert resolution of disagreement.
- **Remediation log:** record of issue, rule, affected rows, and result.
- **Data provenance:** source and history of the data.

## Common mistakes

1. **Deleting rows instead of investigating the source.** The error will return in production.
2. **Imputing using the full data.** This leaks validation/test statistics.
3. **Treating all outliers as errors.** A valid rare event can be essential.
4. **Merging categories by spelling alone.** Similar strings can represent different concepts.
5. **Changing labels to match model predictions.** That hides disagreement and leaks test information.
6. **Ignoring remediation's effect on subgroups.** Automated rules can amplify inequity.
7. **Failing to document exclusions and assumptions.** Results become impossible to audit.

## Exam prep

### Likely 2-mark questions

- **Define data remediation.** Correcting, supplementing, standardising, or safely excluding data problems to make data fit for use.
- **Name three remediation actions.** Imputation, deduplication, recoding, correction, quarantine, or new data collection.
- **What is an outlier?** An observation unusual relative to a defined context; it may be valid or erroneous.
- **Why preserve an audit log?** To reproduce decisions and understand data impact.

### Long-answer prompts

- **Explain how missing data should be handled.** Compare deletion, imputation, missing indicators, model-based methods, and additional collection.
- **How would you investigate an extreme value?** Check source, units, sensor status, context, subgroup, and decision importance before changing it.
- **Describe a data-remediation plan for a customer database.** Cover profiling, rules, mappings, duplicates, validation, documentation, and monitoring.
- **Why can remediation create bias?** Give examples involving missingness, duplicate removal, unit conversion, or label correction.
