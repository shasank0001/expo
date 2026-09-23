---
subject: dwdm
unit: 2
topic: olap-technology-and-operations
syllabus_ref: CSM3101 Unit-II
status: draft
---
# OLAP Technology and Operations

## Overview

OLAP means **Online Analytical Processing**. It supports fast, interactive analysis of multidimensional warehouse data. Users slice, dice, drill, roll up, pivot, and calculate measures across dimension hierarchies. OLAP is a serving approach: a warehouse supplies integrated historical data, while an OLAP engine organizes it for aggregation and navigation. The main technologies are ROLAP, MOLAP, and hybrid OLAP.

## Explanation

### 1. OLAP characteristics

OLAP is designed for analysis by many users over integrated and historical data. Typical features include:

- multidimensional views;
- fast aggregation and precomputation;
- complex calculations and time comparisons;
- drill-down and roll-up through hierarchies;
- interactive response and exploratory analysis;
- security, metadata, and what-if calculations.

OLTP remains better for recording individual transactions. An OLAP response should still be based on a consistent data snapshot, even when it appears interactive.

### 2. Core operations

A cube has dimensions, members, hierarchies, and measures. A **slice** fixes one dimension member. A **dice** selects several members from one or more dimensions. **Drill-down** follows a hierarchy from coarse to fine; **roll-up** moves fine to coarse. A **pivot** changes the displayed axes. A **rank** sorts members, and a **calculation** creates a derived measure such as margin percentage.

For sales:

- slice: `year = 2024`;
- dice: `region in {North, South}` and `quarter in {Q1,Q2}`;
- drill: year → quarter → month → day;
- roll: store → region → all;
- calculate: `revenue - cost` for margin.

The operation is not just a visual change. A drill to day may require a new precomputed cuboid or a scan of base facts.

### 3. ROLAP

**ROLAP** stores relational tables and uses SQL or an SQL-like engine to aggregate. It is flexible, handles large and detailed data well, and avoids duplicating every cuboid, but complex queries can be slower and require careful indexing and partitioning. A materialized view or aggregate table can provide speed.

### 4. MOLAP

**MOLAP** stores preaggregated multidimensional arrays in an optimized engine. It provides fast slicing, drilling, and calculations for common cubes. Its weakness is the cost and space of computing many cuboids, plus the need to refresh the cube when facts change. Sparse representation is important when many combinations are empty.

### 5. HOLAP

**HOLAP** stores detailed data relationally and stores or computes aggregates in a multidimensional engine. It combines MOLAP speed for frequent summaries with ROLAP detail and scalability. Refresh and consistency between the two layers must be managed.

### 6. Aggregation functions and derived measures

A simple measure can use `sum`, `count`, `min`, or `max`. Averages and ratios require stored numerator and denominator. For example:

\[
\text{gross\ margin\ rate}
=\frac{\sum\text{revenue}-\sum\text{cost}}{\sum\text{revenue}}.
\]

Do not average regional margin rates without weighting them by revenue; the result is not the overall rate.

### 7. Performance design

Precompute common cuboids, partition by date or other filters, use columnar storage for scans, compress sparse cells, and cache metadata and frequently used aggregates. Query latency depends on number of dimensions, selected granularity, filters, calculation complexity, concurrency, and storage. Benchmark real queries instead of relying on a synthetic average.

### 8. Security and governance

Roles can limit dimensions, measures, rows, or members. A user may see aggregate sales but not individual customer details. Metadata should define calculations, filters, refresh, and permissions. A fast but unauthorized or stale response is not a successful OLAP system.

## Worked examples

### Example 1: Slice and dice

A cube has year, quarter, region, and product. `year=2024` is a slice. Adding `quarter in {Q1,Q4}` and `region in {South,West}` is a dice. The result is a subcube with selected members, not a new physical fact table.

### Example 2: Roll-up and drill-down

Daily sales are 100, 120, and 80 for three days. The week total is 300. Rolling from city to country sums city totals; drilling from country to city reveals each city's contribution. A roll-up is not valid for an average balance by adding daily balances unless the business rule says so.

### Example 3: ROLAP versus MOLAP

A rare query for an unusual region/product combination may be easiest in ROLAP because it can scan the base fact. A common monthly category total may be faster in MOLAP because it is precomputed. HOLAP is a design choice, not an automatic guarantee of correctness.

### Example 4: MDX-style measure

A conceptual expression `Sales / (Sales + Returns)` for a selected period requires both sums before division. The calculation is reproducible in the semantic model and avoids confusing the ratio with an average of row-level percentages.

## Key terms & formulas

- **OLAP:** interactive multidimensional analytical processing.
- **Slice:** one dimension member fixed.
- **Dice:** several members selected.
- **Drill-down:** finer hierarchy levels.
- **Roll-up:** coarser hierarchy levels.
- **Pivot:** rearrange displayed dimensions.
- **ROLAP:** relational storage and aggregation.
- **MOLAP:** multidimensional preaggregated storage.
- **HOLAP:** hybrid relational detail plus multidimensional aggregates.
- **Derived measure:** calculated from stored measures.

## Common mistakes

1. **Confusing OLAP with OLTP:** analysis versus transaction processing.
2. **Averaging a ratio across regions:** aggregate numerator and denominator first.
3. **Assuming every drill level is precomputed:** some levels are computed on demand.
4. **Ignoring security in a cube:** row and measure access can differ.
5. **Reporting a cache value without refresh status:** it may be stale.
6. **Choosing MOLAP without storage planning:** full cuboids can explode.

## Exam prep

**Likely 2-mark questions**
1. Define slice and dice. *Hint: one selected member versus several selected members.*
2. Differentiate ROLAP and MOLAP. *Hint: relational aggregation versus preaggregated multidimensional storage.*
3. What is a derived measure? *Hint: a calculation from other measures.*

**Likely long-answer questions**
1. Explain OLAP operations with a sales cube. *Hint: slice, dice, drill, roll, pivot, calculate, and storage effects.*
2. Compare ROLAP, MOLAP, and HOLAP. *Hint: storage, flexibility, speed, refresh, and scalability.*
3. Design an OLAP performance and security plan. *Hint: cuboids, partitions, caching, roles, metadata, and monitoring.*
