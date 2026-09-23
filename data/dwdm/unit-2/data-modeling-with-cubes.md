---
subject: dwdm
unit: 2
topic: data-modeling-with-cubes
syllabus_ref: CSM3101 Unit-II
status: draft
---
# Data Modeling Using Cubes and OLAP

## Overview

Multidimensional modeling organizes facts around the questions users ask. A **star schema** has a central fact table and denormalized dimension tables. A **snowflake schema** normalizes some dimensions into related tables. A cube represents the same facts as a multidimensional array or logical structure, with dimension hierarchies and aggregated measures. The model is the foundation for fast, understandable OLAP.

## Explanation

### 1. Fact table design

Choose a business process, such as sales, and a grain, such as one product line per order. The fact table stores measures and foreign keys. Common measures include quantity, sales amount, discount, and cost. Store the base value at the finest supported grain and aggregate upward; do not store a precomputed total that cannot be reconciled to its components.

A **degenerate dimension** is a fact attribute such as an order number that has no separate dimension table. A **factless fact table** records the occurrence of an event, such as a student taking a course, with no numeric measure.

### 2. Dimension tables

A dimension table gives meaning to a key. `Date` can contain day, month, quarter, year, holiday, and fiscal period. `Product` can contain category, brand, and package size. Dimension attributes should be descriptive at the grain and slowly changing attributes need a chosen history policy. Surrogate keys can be compact, stable warehouse keys, while natural keys should be retained when useful for traceability.

### 3. Star schema

A star has one fact table connected directly to each dimension:

```text
             Product
                |
Store -- Sales -- Date
                |
             Customer
```

Denormalized dimension tables make joins short and queries readable. A fact table can be large, but dimension tables are comparatively small. Star schemas are the usual choice for OLAP because they simplify browsing and aggregation.

### 4. Snowflake schema

A snowflake normalizes a dimension, for example splitting product into category, brand, and product. It reduces redundancy and can support shared reference data, but adds joins and can make ad hoc queries harder. Use it when normalization or reuse is more important than the simplest star.

### 5. Fact constellation and multiple grains

A fact constellation (galaxy schema) contains multiple fact tables sharing conformed dimensions, such as sales fact and inventory fact both using date, product, and store. Keep the grain of each fact table distinct. Do not combine unrelated grains in one row because it creates double counting or an invalid many-to-many relationship.

### 6. Cubes and cuboids

A cube is a logical multidimensional collection of measures indexed by dimension members. A **base cuboid** contains the least summarized combination. An **aggregate cuboid** combines hierarchy levels, such as month and year. A full cube contains all cuboids needed by the chosen dimensions, while a sparse or partial cube stores selected combinations. OLAP tools can navigate these levels with slice, dice, roll-up, and drill-down.

### 7. SQL and OLAP correspondence

```sql
SELECT p.category, t.quarter, SUM(s.amount)
FROM sales s
JOIN product p ON p.product_key=s.product_key
JOIN date t ON t.date_key=s.date_key
GROUP BY p.category, t.quarter;
```

This is a two-dimensional slice. A cube engine stores or computes this aggregate and can pivot the result across categories, quarters, and measures. The SQL grouping must preserve the fact grain.

## Worked examples

### Example 1: Star rows

Sales fact:

| date_key | product_key | store_key | amount |
|---|---|---|---:|
| D01 | P10 | S1 | 500 |
| D01 | P20 | S1 | 300 |

Product dimension:

| product_key | product | category |
|---|---|---|
| P10 | Tea | Beverages |
| P20 | Coffee | Beverages |

Query by category gives 800 for Beverages. Querying by individual products gives 500 and 300. A cube can precompute both views.

### Example 2: Snowflake join

Product P10 belongs to brand B1. A normalized model might have `product(product_key, brand_key, name)` and `brand(brand_key, name)`. The query needs an additional join. The model is still valid, but response time and dimensional browsing should be tested.

### Example 3: Double counting warning

A sales fact with one row per order line and a shipment fact with one row per shipment may both contain the same product and date. Joining them on product and date can create a many-to-many result and multiply revenue. A fact constellation keeps the facts separate or uses a shared conformed dimension without pretending their grains are identical.

## Key terms & formulas

- **Star schema:** denormalized dimension tables around a fact table.
- **Snowflake schema:** normalized dimension tables.
- **Fact constellation:** multiple facts sharing conformed dimensions.
- **Grain:** one fact row's detail.
- **Base cuboid:** least summarized cube level.
- **Aggregate cuboid:** summarized hierarchy levels.
- **Cube:** multidimensional measure/dimension structure.
- **Conformed dimension:** same meaning, keys, and hierarchy across facts.
- **Degenerate dimension:** fact attribute without a dimension table.
- **Factless fact:** event table with no ordinary numeric measure.

## Common mistakes

1. **Leaving grain undefined:** it controls valid measures and joins.
2. **Putting descriptive product text in the fact table repeatedly:** use dimensions.
3. **Using a snowflake unnecessarily:** joins and complexity increase.
4. **Combining fact tables at different grains:** it double counts.
5. **Treating a cube as only three dimensions:** n-dimensional arrays are common.
6. **Confusing a dimension member with a measure:** categories are descriptors; amounts are usually measures.

## Exam prep

**Likely 2-mark questions**
1. Differentiate star and snowflake schemas. *Hint: denormalized dimensions versus normalized dimensions.*
2. What is a fact constellation? *Hint: multiple fact tables sharing conformed dimensions.*
3. Define a base cuboid. *Hint: least summarized cuboid.*

**Likely long-answer questions**
1. Design a star schema for retail sales and explain every table. *Hint: process, grain, measures, dimensions, keys, hierarchies.*
2. Explain how a relational model maps to a cube and OLAP navigation. *Hint: facts become measures, dimensions become axes, GROUP BY becomes aggregation.*
3. Compare star, snowflake, and fact-constellation designs. *Hint: redundancy, joins, shared dimensions, grain, and use cases.*
