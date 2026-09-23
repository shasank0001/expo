---
subject: dwdm
unit: 2
topic: data-generalization-with-aoi
syllabus_ref: CSM3101 Unit-II
status: draft
---
# Data Generalization with AOI

## Overview

AOI means **Attribute-Oriented Induction**. It summarizes many records by replacing detailed attribute values with higher-level categories, then describes a target class with the resulting generalized tuples. The technique is useful when the original database is not already arranged in a convenient multidimensional relation. AOI can produce a **characteristic description** of one class and a **contrastive description** showing how it differs from other classes.

## Explanation

### 1. Why generalization is needed

Detailed values such as every city, product code, and timestamp make comparison difficult. A concept hierarchy maps details to broader concepts:

```text
Mumbai, Pune, Delhi → India
Tea, Coffee         → Beverage
```

The hierarchy is domain knowledge. Generalization replaces a value by an ancestor while preserving a meaningful comparison. It is not arbitrary rounding, and it does not simply delete detail.

### 2. Attribute-oriented induction

AOI examines tuples, selects target and comparison classes, and progressively generalizes attributes that are not useful for discrimination. A typical process is:

1. Choose a target class, such as `fraud = yes`.
2. Select tuples from that class and from comparison tuples.
3. Generalize attribute values using concept hierarchies.
4. Prune rare or uninformative values.
5. Find the smallest generalized tuple set that covers the target class.
6. Derive characteristic and contrastive descriptions.

A generalized tuple is a pattern such as `(occupation = employee, amount = high, region = urban)`. A **cover** is a set of generalized tuples that matches the target records under the hierarchy.

### 3. Characteristic description

A characteristic description summarizes common properties of target records. It answers: “What is typical of the target class?” For example, if most approved loans have `income=high` and `occupation=employed`, the description may be `occupation = employed AND income = high`.

### 4. Contrastive description

A contrastive description compares the target class with non-target classes. It answers: “What distinguishes the target from the other classes?” If fraudulent transactions often occur at `night` and have `online = yes`, the contrastive rule might be:

```text
IF channel = online AND time_period = night
THEN fraud more likely than non-fraud.
```

The rule is descriptive, not a causal claim. It must be evaluated on held-out data and with the class distribution.

### 5. Generalization choices

A value can be generalized upward by a concept hierarchy, binned into numeric intervals, or replaced with a domain category. Excessive generalization can make every record match and destroy discrimination. Too little generalization leaves many rules and does not reveal structure. The stopping point should balance coverage, simplicity, and validation performance.

### 6. Pruning and relevance

A value or tuple can be pruned if it covers too few target records, is equally common in the comparison class, or adds no distinction. A generalized value that covers the whole database is too broad to be useful. Attribute relevance can be assessed by how much a value separates target from comparison tuples. AOI may be integrated with decision trees, rule induction, or association mining.

### 7. Example of a multidimensional view

If the warehouse has facts and dimension hierarchies, a general query can slice by `country=India`, roll up from day to year, and group by product category. AOI supplies the conceptual idea of replacing detailed dimension members with ancestors; it does not require a special cube engine.

## Worked examples

### Example 1: Characteristic generalization

Target tuples:

| Occupation | Income | Region |
|---|---|---|
| teacher | 80,000 | urban |
| nurse | 75,000 | urban |
| teacher | 90,000 | semi-urban |

Use `low < 50,000`, `medium 50,000–100,000`, `high > 100,000`, and `urban` as a region category. The generalized target descriptions are `(teacher, medium, urban)`, `(nurse, medium, urban)`, and `(teacher, medium, semi-urban)`. A compact cover might be `income = medium AND occupation in {teacher, nurse}`. It covers all three target records but may also cover non-target records, so it is not a perfect classifier.

### Example 2: Contrastive description

Suppose non-fraud records are mostly daytime, in-store transactions. Fraud records are mostly online at night. After generalization, the contrastive tuple is

```text
channel = online AND time = night
```

It covers 80 of 100 fraud records and only 20 of 1,000 non-fraud records. In all 1,100 records, pattern prevalence is \(100/1100=0.0909\), while fraud prevalence is also \(100/1100=0.0909\). Therefore

\[
\operatorname{lift}=\frac{0.80}{0.0909}\approx8.8.
\]

The contrast is strong, but the pattern occurs in only about 9% of all records. Coverage, prevalence, and lift should be read together.

### Example 3: Numeric bins

Ages 6, 18, 40, and 65 can be generalized to `child`, `young adult`, `adult`, and `senior`, or grouped into broader bands such as `<18`, `18–39`, and `>=40`. The choice depends on the task. A broad band can increase coverage but hide useful variation; a narrow band preserves detail but creates more tuples.

## Key terms & formulas

- **AOI:** Attribute-Oriented Induction.
- **Concept hierarchy:** detail-to-general categories.
- **Generalization:** replace a value with an ancestor or interval.
- **Target class:** class being described.
- **Comparison class:** other classes used for contrast.
- **Characteristic description:** properties common to the target class.
- **Contrastive description:** properties that distinguish target from others.
- **Generalized tuple:** pattern after replacing values.
- **Cover:** generalized tuples that cover target records.
- **Pruning:** remove irrelevant or overly general patterns.

## Common mistakes

1. **Equating generalization with deletion:** it replaces detail with a meaningful level.
2. **Using a hierarchy without domain meaning:** labels must be valid for the task.
3. **Calling a characteristic description causal:** it summarizes association.
4. **Generalizing so far that every record matches:** the description loses discrimination.
5. **Ignoring class prevalence:** many target records can still be a small fraction of all data.
6. **Failing to validate generalized rules:** they may not generalize to new data.

## Exam prep

**Likely 2-mark questions**
1. What does AOI stand for and what does it do? *Hint: Attribute-Oriented Induction; generalizes attributes and induces descriptions.*
2. Differentiate characteristic and contrastive descriptions. *Hint: common target properties versus target-versus-other distinctions.*
3. What is a concept hierarchy? *Hint: a tree of detailed and general concepts.*

**Likely long-answer questions**
1. Explain the AOI process from target selection to contrastive rule. *Hint: generalize, prune, cover, characterize, contrast, validate.*
2. Use a supplied table to construct a hierarchy and derive a characteristic description. *Hint: show ancestor mappings and generalized tuples.*
3. Discuss the effect of overgeneralization in AOI. *Hint: coverage versus discrimination and validation.*
