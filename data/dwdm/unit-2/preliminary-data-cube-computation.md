---
subject: dwdm
unit: 2
topic: preliminary-data-cube-computation
syllabus_ref: CSM3101 Unit-II
status: draft
---
# Preliminary Concepts of Data Cube Computation

## Overview

Data-cube computation builds a multidimensional collection of measures from detailed facts. A **base cuboid** holds the least summarized combination; **aggregate cuboids** combine dimension members or levels. A **full cube** contains every valid combination, while a partial cube stores only useful views. The computation can be expensive because the number of cuboids grows rapidly, so sparsity, aggregation order, storage, and query requirements matter.

## Explanation

### 1. Multidimensional array view

Suppose a cube has dimensions time \(D_1\), product \(P_1\), and region \(R_1\), with measure `sales`. A cell is addressed by a tuple of members, for example `(2024-Q1, Tea, South)`. The logical value is

\[
V[d,p,r]=\sum_{\text{facts matching }(d,p,r)}\text{sales}.
\]

A cube is not necessarily a physical three-dimensional shape. Four or more dimensions are represented as an n-dimensional array or an equivalent relational structure.

### 2. Base and aggregate cuboids

A **base cuboid** uses the finest selected levels, such as day, product, and store. If dimensions have hierarchies, roll-up cuboids use week, month, or category. A full cube includes every combination of the selected levels. A **lattice** describes the set of cuboids and their relationships. Cuboids can be materialized, partially materialized, or computed on demand.

### 3. Aggregation functions

A cell can store a sum, count, minimum, maximum, or average. Sum and count are naturally additive. An average must be derived from the corresponding sum and count, not obtained by averaging already averaged cells. A non-additive ratio similarly needs its numerator and denominator.

### 4. Full versus partial computation

A full cube is useful when users query many combinations and data is dense. It requires more memory and refresh work. A partial cube stores common combinations, such as daily product-region and monthly total, and calculates rare views from the base cuboid. Query workload, sparsity, storage budget, and update frequency determine the trade-off.

### 5. Sparsity

A dense cell has data in most combinations. A **sparse cube** has many empty cells, especially with high-cardinality dimensions. Store only nonzero cells, or use a chunk/bitmap representation. A small number of facts can still require a huge logical cube because every combination is possible.

### 6. Computation and optimization

The computation order is important. If a higher-level aggregate can be derived from lower-level aggregates, intermediate work can be reduced. Common techniques include chunking dimensions, using array operations, selecting dimension order, reusing partial aggregates, processing partitions, and materializing high-value cells. A dimension with low cardinality or a frequently filtered level can be handled first.

### 7. Query-driven view selection

Start with actual questions. If users mostly ask for region-month-category sales, materialize that cuboid rather than every day-by-product-by-store combination. A view-selection algorithm estimates benefit from query frequency, computation cost, and storage. The result should be revisited as usage changes.

## Worked examples

### Example 1: Three-dimensional cells

Let dimensions be day, product, and region. The base cells could be:

| Day | Product | Region | Sales |
|---|---|---|---:|
| 1 | Tea | South | 10 |
| 1 | Tea | North | 20 |
| 2 | Coffee | South | 15 |

A `(day, product, region)` cell is direct. A `(month, category, region)` cell aggregates many base cells. The cube must define how day maps to month and product maps to category.

### Example 2: Average cannot be averaged

If South has total sales 100 over 4 transactions, its average is 25. North has total sales 300 over 6 transactions, average 50. The combined average is

\[
(100+300)/(4+6)=40,
\]

not \((25+50)/2=37.5\). Store count and sum if the cube must answer average queries.

### Example 3: Sparse size

Three dimensions with 365 days, 10,000 products, and 100 regions have

\[
365\times10{,}000\times100=365{,}000{,}000
\]

logical cells. If only 50,000 cells have facts, a dense allocation wastes most memory. A sparse cell list or chunk representation stores the occupied combinations and computes the rest as needed.

### Example 4: Materialized view choice

Suppose monthly total and product-category-month are frequent, while day-product-store-region is rarely queried. Materialize the first two and leave the detailed base fact available for drill-through. This reduces cuboid count while preserving rare detail.

## Key terms & formulas

- **Data cube:** n-dimensional collection of measures and dimension members.
- **Base cuboid:** least summarized level.
- **Aggregate cuboid:** summarized dimension levels.
- **Full cube:** all selected cuboid combinations.
- **Partial cube:** selected/materialized cuboids.
- **Lattice:** organization of cuboids and hierarchies.
- **Dense/sparse cube:** mostly occupied versus mostly empty.
- **Chunk:** a block of the multidimensional array.
- **Aggregate function:** sum, count, min, max, or derived average.
- **View selection:** choose cuboids according to workload and cost.

## Common mistakes

1. **Calling a data cube only three-dimensional:** dimensions can be many.
2. **Averaging cell averages:** sum and count must be recomputed.
3. **Assuming a full cube is always best:** storage and refresh can be excessive.
4. **Ignoring sparsity:** dense allocation wastes space.
5. **Confusing base fact granularity with the cube's logical array:** a missing combination is not automatically zero.
6. **Materializing views without query evidence:** unused cuboids waste resources.

## Exam prep

**Likely 2-mark questions**
1. Define base cuboid and full cube. *Hint: least summarized levels versus all combinations.*
2. Why is sparsity important in cube computation? *Hint: many combinations have no facts.*
3. How is an overall average derived from cells? *Hint: total sum divided by total count.*

**Likely long-answer questions**
1. Explain cube computation from base facts to aggregate cuboids. *Hint: dimensions, measures, hierarchies, aggregation, and views.*
2. Compare full and partial cube materialization. *Hint: query coverage, storage, refresh, and sparsity.*
3. Design a cube-view selection strategy for a retailer. *Hint: workload, frequency, cost, storage, and refresh.*
