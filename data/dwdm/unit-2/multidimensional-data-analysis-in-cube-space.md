---
subject: dwdm
unit: 2
topic: multidimensional-data-analysis-in-cube-space
syllabus_ref: CSM3101 Unit-II
status: draft
---
# Multidimensional Data Analysis in Cube Space

## Overview

A data cube turns a fact table into navigable analytical space. Multidimensional analysis uses the cube to compare measures across dimensions, identify patterns, find exceptions, and move from summary to detail. It includes characterization (what is typical), discrimination (what distinguishes a selected member), selection (where a target condition holds), and drill-oriented analysis. The same measure can look different at different levels, so grain, filters, and time alignment must always be stated.

## Explanation

### 1. Cube coordinates

A cell is a combination of dimension members. A measure can be queried with one or more dimensions fixed. In a cube with year, quarter, product, and region, `(2024, Q1, Tea, South)` identifies one cell; a slice or dice selects many such cells. A cube operation is meaningful only when the selected cells share the required grain.

### 2. Characterization

Characterization asks what is typical of a selected cell, dimension member, or class. A manager can inspect a region and see its sales total, average basket, product mix, and comparison with other regions. Characterization may use distributions, top-k members, averages, or deviations from the overall mean. It is descriptive, not causal.

### 3. Discrimination

Discrimination asks what makes a selected member different. Compare South with North by the same period and measure, calculate the difference or ratio, and drill into the dimensions that account for it. A large difference can be driven by population size, missing data, or a small denominator. Use aligned filters and state whether the comparison is absolute or relative.

### 4. Selection and exception analysis

Selection finds members meeting a condition, such as sales below target or error rate above 5%. Cube analysis can filter or rank cells, then drill to details. Exceptions should have a threshold, a reference period, and a follow-up action. A statistical outlier in a stable process may be different from a business exception caused by a new campaign.

### 5. Drill, slice, dice, and roll

A **slice** fixes a member; a **dice** selects several; **drill-down** moves to finer members; **roll-up** aggregates to broader members. Pivot changes the visual arrangement but not the value. A drill to transaction detail can expose the base fact grain; stop at the level authorized for the user.

### 6. Other cube-space analyses

Cube data supports ranking, contribution analysis, period-over-period change, share of total, correlation across measures, and what-if recalculation. A derived share should use the same total as the denominator. Correlation across aggregate cells can be misleading because aggregation can induce a relationship; it is not a causal model.

### 7. Analytical integrity

Check time completeness, duplicate facts, measure nulls, and consistent filters. A total can be correct for a selected cube but misleading if a dimension member was silently excluded. Keep the query, filter, version, and refresh timestamp with the result. Use drill-through to representative detail, not as a substitute for a statistical sample.

## Worked examples

### Example 1: Characterization

South 2024 sales are ₹1.2 million over 120,000 transactions; average basket is ₹10. North is ₹1.5 million over 75,000 transactions; average basket is ₹20. South has a higher transaction count but lower total revenue. The cube characterization shows the pattern; it does not explain the cause.

### Example 2: Discrimination

A region's revenue is 15% below the average. The analyst slices by product and finds that one category contributes most of the gap. The correct statement is “the gap is concentrated in category X under the selected filters,” not “category X causes low revenue.”

### Example 3: Selection and exception

Target monthly sales is ₹100,000. Cells below 80% of target are selected:

\[
\text{exception}: \text{sales}<0.8(100{,}000)=80{,}000.
\]

The cube returns three regions. Drill-through shows their detailed products and dates, while the selection rule remains in the report so a reader knows why they appeared.

### Example 4: Share and average

A cube shows regions A and B with 60 and 40 units. A's share is \(60/(60+40)=60\%\). If a third region is later included, the denominator changes to 100 and A's share becomes 50%. Always label the scope of a share.

## Key terms & formulas

- **Characterization:** description of typical cube cells or members.
- **Discrimination:** comparison showing what distinguishes a member.
- **Selection:** filtering cells by a condition.
- **Exception analysis:** finding cells outside an expected range.
- **Slice/dice:** fix or select dimension members.
- **Drill-down/roll-up:** finer/coarser hierarchy movement.
- **Pivot:** rearrange axes without changing the data.
- **Share of total:** member measure divided by the selected total.
- **Cube-space ranking:** ordering members by a measure.
- **Drill-through:** retrieve detailed supporting rows.

## Common mistakes

1. **Comparing members with different filters or time periods:** the difference is not interpretable.
2. **Using a changing denominator for a share:** trends become artificial.
3. **Treating a selected exception as a proven cause:** it is a flag for investigation.
4. **Confusing pivot with drill-down:** pivot changes layout, not granularity.
5. **Drilling to data beyond the user's access:** security must follow navigation.
6. **Ignoring aggregate-level correlation:** aggregation can create or hide relationships.

## Exam prep

**Likely 2-mark questions**
1. Differentiate characterization and discrimination in cube analysis. *Hint: typical description versus distinguishing comparison.*
2. What is selection analysis? *Hint: filter cube cells using conditions.*
3. What is drill-through? *Hint: retrieve detailed records supporting an aggregate.*

**Likely long-answer questions**
1. Explain characterization, discrimination, selection, and exception analysis with a retail cube. *Hint: question, operation, example, interpretation.*
2. Demonstrate slice, dice, drill-down, roll-up, and pivot on one sales cube. *Hint: identify dimensions and levels for each.*
3. Discuss analytical pitfalls in multidimensional analysis. *Hint: grain, scope, time, aggregation, security, and causation.*
