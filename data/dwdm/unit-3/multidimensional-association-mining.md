---
subject: dwdm
unit: 3
topic: multidimensional-association-mining
syllabus_ref: CSM3101 Unit-III
status: draft
---
# Multidimensional Association Mining

## Overview

Multidimensional association mining adds conditions from other data dimensions—such as time, location, customer segment, or device—to an association rule. A multidimensional rule can say that a product pair is popular in one region or during one season. The same items may have different associations in different slices, so mining only the full database can hide important context.

## Explanation

### 1. Multidimensional data

Transactions can carry attributes beyond their items. A transaction might contain `tea`, `biscuit`, location `Mumbai`, season `winter`, and customer type `student`. A **multidimensional itemset** selects items and dimensions together. A **multidimensional association rule** constrains the antecedent, consequent, or both with dimension predicates.

Examples include:

- `winter ∧ Mumbai -> tea -> biscuit`;
- `tea -> biscuit [Mumbai, 2024]`;
- `student ∧ low price -> tea ∧ biscuit`.

The notation in brackets commonly records dimension restrictions, but the exact placement of predicates should be stated rather than guessed.

### 2. Single versus multiple dimensions

A **single-dimensional** rule uses only transaction items. A multidimensional rule uses at least one external dimension. Multiple dimensions are often correlated: a high-value customer may also be in a particular region and season. A rule that is strong globally may be negative in one segment.

### 3. Categorical and numerical dimensions

Categorical dimensions have levels such as `North`, `South`, `urban`, or `student`. Numerical or temporal dimensions can be discretized into intervals such as age `20–29`, price `$10–19`, time `9–12`, or quarter `Q1`. Discretization makes transactions and cube cells comparable, but bin boundaries should reflect domain meaning and should be reported.

### 4. Support and confidence with constraints

For a rule with dimension condition \(D\),

\[
\operatorname{supp}(A\cup B\mid D)
=\frac{\#\{T:A\subseteq T,\ B\subseteq T,\ D(T)\text{ holds}\}}
{\#\{T:D(T)\text{ holds}\}},
\]

when support is defined within the selected slice. Confidence is then the joint count within \(D\) divided by the count containing \(A\) within \(D\). State the denominator: “support in all transactions” and “support within Mumbai winter transactions” are different tasks.

### 5. Mining strategies

**Top-down refinement:** start with a broad cube cell such as all locations and periods, find strong patterns, and drill into dimensions. **Constraint-based mining:** use user predicates to restrict the search, for example `location = South` or `time between 10 and 17`. **Query-based mining:** interactively select slices and ask for patterns. **Data-cube and OLAP integration:** precompute or materialize aggregated cells, then drill through to fine data. **Shared multi-level mining:** mine related rules with a common frequent itemset or dimension prefix efficiently.

A multidimensional Apriori must prune only when a rule's relevant slice cannot meet its threshold. A set can be infrequent globally and frequent in a narrow region, so global pruning alone is unsafe for slice-specific tasks.

### 6. Evaluation and deployment

Segment-specific rules should be checked for sample size, lift, significance, and stability across time. A rule supported by only two regional transactions is not a reliable regional pattern. Multidimensional results also need privacy and fairness review when location or customer attributes could cause inappropriate targeting.

## Worked examples

### Example 1: Seasonal rule

Database has 1,000 winter transactions. Tea appears in 400, biscuit in 500, and both in 300.

Within winter:

\[
\operatorname{supp}(tea)=\frac{400}{1000}=0.40,
\quad \operatorname{supp}(biscuit)=0.50,
\quad \operatorname{supp}(tea,biscuit)=0.30,
\]
\[
\operatorname{conf}(tea\rightarrow biscuit)=0.30/0.40=0.75,
\]
\[
\operatorname{lift}=0.30/(0.40\cdot0.50)=1.50.
\]

The same items might have lower association in summer. Reporting the result as `winter -> tea -> biscuit` preserves the context.

### Example 2: Location slice and support denominator

There are 200 South-region transactions. A appears in 100, B in 80, and A with B in 50. If the query restricts to South:

\[
\operatorname{supp}(A\mid South)=0.50,\quad
\operatorname{supp}(B\mid South)=0.40,\quad
\operatorname{supp}(A,B\mid South)=0.25.
\]

Confidence is \(0.25/0.50=0.50\), and lift is \(0.25/(0.50\cdot0.40)=1.25\). If a user instead asks for the rule without a location predicate, the denominator becomes the total database size and the result is a different, global rule.

### Example 3: Drilling a cube

Suppose a cube shows `Q1: lift 0.8`, `Q2: lift 1.1`, and `Q3: lift 1.6` for the same item pair. A top-down method may drill from year to quarter and then region. It should not discard the pair at the year level merely because annual lift is near 1; the Q3 slice may be the actionable pattern. The final report must state the granularity and sample size.

### Example 4: Safe pruning

A 2-itemset occurs in 20 of 10,000 transactions, so it is globally infrequent with a 5% threshold. If all 20 occur in a region that has 300 transactions, its regional support is \(20/300=6.67\%\), above 5%. A global-only Apriori pruning rule would miss it. A multidimensional method must postpone or relax global pruning for the selected region.

## Key terms & formulas

- **Dimension:** an attribute used to describe a transaction, such as time or location.
- **Multidimensional itemset:** items plus dimension conditions.
- **Dimension constraint:** predicate such as `time = Q3` or `region = South`.
- **Slice:** the transactions/cells selected by a dimension condition.
- **Conditional support:** support among transactions satisfying dimension \(D\).
- **Top-down refinement:** mine coarse slices then drill down.
- **Query-based mining:** interactive constrained mining.
- **Drill-through:** move from an aggregate slice to detailed transactions.
- **Slice-specific pruning:** test support in the selected dimensions, not only globally.

## Common mistakes

1. **Using the wrong support denominator:** slice support and global support are not interchangeable.
2. **Pruning a globally infrequent set before checking a valid slice:** local patterns can be strong.
3. **Treating a time attribute as a transaction item:** it is a dimension unless the task explicitly models sequence.
4. **Ignoring binning choices:** arbitrary temporal or age intervals can change discovered patterns.
5. **Reporting a segmented rule without its segment:** the location/time condition is part of the claim.
6. **Overfitting small slices:** apply a minimum count and validate across periods.

## Exam prep

**Likely 2-mark questions**
1. Differentiate single-dimensional and multidimensional association rules. *Hint: ordinary items versus items with time/location/other predicates.*
2. What is a constraint in multidimensional mining? *Hint: a user predicate that limits the relevant transactions or cells.*
3. What is top-down refinement? *Hint: mine broad dimensions first, then drill into promising slices.*

**Likely long-answer questions**
1. Mine and evaluate an association in a given multidimensional slice. *Hint: define denominator, count cells, compute support/confidence/lift, and state the constraint.*
2. Compare query-based, top-down, and cube-based multidimensional mining. *Hint: interaction, refinement, aggregation, pruning, and cost.*
3. Explain why global Apriori pruning can lose local patterns and how to avoid it. *Hint: regional support may exceed global support; use slice-aware or delayed pruning.*
