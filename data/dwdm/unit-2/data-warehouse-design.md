---
subject: dwdm
unit: 2
topic: data-warehouse-design
syllabus_ref: CSM3101 Unit-II
status: draft
---
# Data Warehouse Design

## Overview

Warehouse design converts business questions into a stable, testable analytical model. The design process begins with requirements and data sources, chooses a process and grain, defines facts, dimensions, hierarchies, and measures, then designs loading, storage, security, and refresh. A good design preserves meaning and makes common queries fast without losing the detail needed for new questions.

## Explanation

### 1. Requirements and sources

Interview users and list recurring questions: “What were sales by region and month?”, “Which products are running out?”, and “How does this year compare with last year?” Identify the business process, users, decisions, required history, refresh expectations, security rules, and acceptable latency. Inventory source systems, update frequency, keys, formats, and data owners.

### 2. Business process and grain

Choose one subject area and process at a time. A process is “sales,” not “all company data.” Define grain in a sentence: one fact row represents one product line in a completed sale. If an order can be cancelled or returned, decide whether transactions, status events, or adjustments are separate facts. Grain must be consistent across every measure in the table.

### 3. Dimensions and hierarchies

Typical dimensions include date/time, product, customer, store, promotion, and currency. Define hierarchy levels, members, unknown/not-applicable values, and slowly changing policies. A date dimension can include day, week, month, quarter, fiscal year, and holiday flags. Categories should be mutually understandable and stable enough for reporting.

### 4. Measures and facts

Choose additive, semi-additive, or non-additive measures. Sales amount is usually additive across time and dimensions. Account balance is semi-additive across time. A ratio such as margin percentage is non-additive; store numerator and denominator and calculate the ratio after aggregation. Store source precision and units. Avoid adding a measure whose definition changes silently.

### 5. Physical and logical design

Choose column types, partitions, indexes, compression, distribution, and materialized aggregates based on query patterns. Partition a large fact table by date or another common filter. Use columnar storage for analytical scans where appropriate. Indexes help particular filters or joins but add load and storage cost. A physical design should be tested with real query workloads.

### 6. ETL and refresh

Extract from sources, stage data, validate keys and totals, transform names/units, load facts and dimensions, and publish only after checks pass. Choose full or incremental refresh. A nightly batch can have a clear consistency point; near-real-time loads need late-arriving updates and versioning. Record source timestamp, load timestamp, and batch ID.

### 7. Quality, governance, and security

Test uniqueness of dimension keys, referential integrity, nonnull rules, valid ranges, and reconciliation to source totals. Metadata should define each measure, owner, source, transformation, refresh, and security classification. Apply least privilege and row/column controls where needed.

### 8. Kimball and Inmon perspectives

Kimball's dimensional approach emphasizes the business process, grain, star schemas, and fact tables. Inmon's approach emphasizes a normalized enterprise data warehouse and dependent data marts. The labels are less important than the design facts: declared grain, conformed dimensions, consistent definitions, and tested loading.

## Worked examples

### Example 1: Requirements to model

Question: “Show quarterly sales by product category and store.” Process: sales. Grain: one product line per order. Measures: quantity and net amount. Dimensions: date (quarter), product (category), and store. The model does not need customer unless another requirement does; adding unused dimensions increases complexity.

### Example 2: Semi-additive measure

Suppose monthly account balances are 100, 120, and 130. Do not sum them to claim a total balance over time. Use the ending balance 130 for a period-end report, or average them if the question is average balance. The measure definition must state the time behavior.

### Example 3: Incremental load check

Yesterday's source sales total is ₹1,000,000 and the warehouse contains ₹995,000. One late order of ₹5,000 is found. A reliable load adds the missing order, logs the correction, and refreshes affected daily/monthly aggregates. Simply accepting the batch without reconciliation would propagate an error.

### Example 4: Slowly changing product name

If “Green Tea” is renamed “Organic Green Tea,” Type 2 creates a new product version and maps historical facts to the old version; Type 1 changes the display for all history. The choice is a reporting policy and must be documented, not an implementation accident.

## Key terms & formulas

- **Grain:** detail of one fact row.
- **Business process:** activity being modeled.
- **Additive measure:** safely summed across relevant dimensions/time.
- **Semi-additive:** not safely summed across every time level.
- **Non-additive:** ratio or average that should be recomputed.
- **Conformed dimension:** consistent dimension shared by facts.
- **Slowly changing dimension:** policy for historical attribute changes.
- **Staging area:** temporary landing/validation area.
- **Increment load:** add only new or changed source data.
- **Reconciliation:** compare warehouse totals with trusted source totals.

## Common mistakes

1. **Designing tables before fixing grain:** the model cannot be validated.
2. **Using one “sales” fact for multiple grains:** measures double count.
3. **Summing non-additive ratios:** aggregate numerator and denominator first.
4. **Ignoring late-arriving data:** monthly totals can remain wrong.
5. **Adding every available dimension:** cost and confusion increase.
6. **No reconciliation or ownership:** quality failures are hard to diagnose.

## Exam prep

**Likely 2-mark questions**
1. What is fact-table grain? *Hint: the detail represented by one row.*
2. Differentiate additive and semi-additive measures. *Hint: safe sum across all dimensions versus not safe across time.*
3. Why use a staging area? *Hint: landing, cleaning, validation, and controlled loading.*

**Likely long-answer questions**
1. Design a warehouse for an online retailer step by step. *Hint: requirements, process, grain, schema, ETL, quality, security, refresh.*
2. Discuss dimensional versus enterprise-normalized design choices. *Hint: query simplicity and shared models versus normalization and reuse.*
3. Explain a slowly changing dimension and its effect on historical reports. *Hint: Type 1/2/3, version keys, time validity.*
