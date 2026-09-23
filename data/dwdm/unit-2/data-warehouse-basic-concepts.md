---
subject: dwdm
unit: 2
topic: data-warehouse-basic-concepts
syllabus_ref: CSM3101 Unit-II
status: draft
---
# Basic Concepts of a Data Warehouse

## Overview

A **data warehouse** is a large collection of integrated, historical data organized for analysis rather than day-to-day transaction processing. Operational databases answer current tasks such as recording an order. A warehouse answers questions across years, products, customers, and locations. It is the foundation for OLAP, data cubes, dashboards, reporting, forecasting, and data mining.

## Explanation

### 1. OLTP versus OLAP

An **operational DBMS** is optimized for OLTP: many short inserts, updates, deletes, and point lookups. Concurrency, recovery, and fast updates are central. OLAP is optimized for analysis: aggregations, slices, grouping, and multidimensional queries. Warehouses commonly support OLAP, but the terms are not identical: a warehouse stores and organizes data; OLAP is a way of querying and analyzing it.

### 2. Four defining characteristics

A warehouse is:

- **Subject-oriented:** organized around business subjects such as sales, customer, inventory, or finance, not around application screens.
- **Integrated:** values from many sources use common names, codes, units, and time conventions.
- **Time-variant:** historical snapshots are retained, often with a time key and slowly changing dimension handling.
- **Nonvolatile:** data is loaded and mainly read; routine analyst queries do not overwrite historical facts.

“Nonvolatile” does not mean a warehouse never changes. New facts and corrected historical values are loaded through controlled processes.

### 3. Architecture

A common flow is:

```text
Operational sources
        ↓ extract
Staging area (clean, reconcile)
        ↓ transform and load
Warehouse: fact + dimension tables
        ↓
OLAP server / data cube / analytical reports
```

**Extract, Transform, Load (ETL)** moves data, converts formats and units, joins keys, removes duplicates, and applies quality rules. ELT loads raw data first and transforms it in the analytical platform; CDC, batch loads, and streaming are possible sources. Metadata records definitions, lineage, transformations, refresh time, and ownership.

### 4. Facts, dimensions, and measures

A **fact table** stores numeric business events or measurements. A fact row has foreign keys into dimension tables and measure values such as quantity, amount, or duration. A **dimension table** describes the “who, what, when, where, why” of a fact. A measure is a numeric value that is usually aggregated by sum, average, min, max, or count.

The **grain** is the level of detail represented by one fact row, such as one line item per order, not vaguely “sales.” Grain determines what joins and aggregates are valid.

### 5. Time and history

A warehouse has a time dimension with levels such as day, week, month, quarter, and year. Slowly changing dimensions handle a changing descriptive attribute: Type 1 overwrites the old value, Type 2 adds a version row, and Type 3 stores selected historical values. Without a deliberate policy, historical reports can silently change meaning.

### 6. Users and benefits

Analysts perform ad hoc investigations, managers use dashboards, and operational decision teams use trends and forecasts. Benefits include consistent historical reporting, faster complex queries, cross-functional integration, and a stable analytical model. A warehouse also adds storage, refresh, governance, and security costs.

## Worked examples

### Example 1: Daily sales fact

Fact table `SALES`:

| order_id | date_key | product_key | store_key | quantity | amount |
|---|---|---|---|---:|---:|
| 101 | 2024-01-01 | P1 | S1 | 2 | 300 |

The grain is one order line. The amount is not a dimension; it is a measure. `date_key`, `product_key`, and `store_key` connect to descriptive tables.

### Example 2: Monthly aggregation

If ten daily facts each have amount 100, the month total is 1,000. A query at month grain is:

```sql
SELECT d.month, SUM(f.amount) AS revenue
FROM sales f
JOIN date_dim d ON d.date_key = f.date_key
GROUP BY d.month;
```

Averaging daily amounts before summing them would answer a different question.

### Example 3: Integrated units

The POS system records price in dollars and another system in rupees. Integration requires a documented exchange rate and currency date; simply renaming both to `price` creates a mixed-unit error. The warehouse should retain currency or a converted measure with metadata.

## Key terms & formulas

- **Data warehouse:** subject-oriented, integrated, time-variant, nonvolatile analytical data.
- **OLTP:** operational transaction processing.
- **OLAP:** online analytical processing.
- **ETL:** extract, transform, load.
- **Fact:** stored business event or measurement.
- **Dimension:** descriptive context for facts.
- **Measure:** numeric value used in aggregation.
- **Grain:** detail represented by one fact row.
- **Metadata:** definitions, lineage, ownership, and refresh information.
- **Slowly changing dimension:** dimension attribute whose history needs deliberate handling.

## Common mistakes

1. **Calling a warehouse an ordinary large database:** its model and query purpose differ.
2. **Saying nonvolatile means data never changes:** new loads and corrections occur.
3. **Mixing fact and dimension concepts:** measures are not dimensions.
4. **Leaving grain unstated:** every fact design must state it explicitly.
5. **Converting units without metadata:** the result can be numerically wrong.
6. **Confusing ETL and data mining:** ETL prepares data; mining searches it for patterns.

## Exam prep

**Likely 2-mark questions**
1. State the four characteristics of a data warehouse. *Hint: subject-oriented, integrated, time-variant, nonvolatile.*
2. Define grain. *Hint: detail represented by one fact record.*
3. What is ETL? *Hint: extract, transform, load.*

**Likely long-answer questions**
1. Compare OLTP and an analytical warehouse. *Hint: workload, schema, updates, queries, and users.*
2. Explain the warehouse architecture and role of metadata. *Hint: sources, staging, transformation, load, serving, lineage.*
3. Explain facts, dimensions, measures, and grain with a sales schema. *Hint: give a concrete row and valid aggregation.*
