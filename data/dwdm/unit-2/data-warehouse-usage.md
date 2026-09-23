---
subject: dwdm
unit: 2
topic: data-warehouse-usage
syllabus_ref: CSM3101 Unit-II
status: draft
---
# Data Warehouse Usage

## Overview

A warehouse is useful when it supports decisions rather than merely storing history. Common uses include standard reports, dashboards, ad hoc analysis, trend and comparison studies, forecasting, and what-if planning. The warehouse's integrated historical view gives context, but correct usage depends on agreed metric definitions, suitable refresh timing, data quality, and interpretation by domain users.

## Explanation

### 1. Reporting and dashboards

A report presents a repeatable question, such as monthly revenue by region. A dashboard places several related measures together, often with a date filter and KPI indicators. It should show definitions, units, update time, and drill paths. A dashboard that is attractive but hides freshness or incomplete periods can mislead users.

### 2. Ad hoc analysis

Ad hoc questions are not known in advance: “Which stores lost sales after a promotion?” Users need flexible dimensions, filters, and drill-down. The warehouse should retain detail and metadata rather than only a few prebuilt summaries. A query should be reproducible so another user can understand its filters and time range.

### 3. Trends and comparisons

A trend compares a measure over time; a comparison contrasts regions, products, segments, or periods. Useful comparisons align grain and calendar. Compare like with like, use the same currency, and distinguish a percentage change from a percentage-point change. Year-over-year comparison should use a time dimension with a consistent fiscal calendar.

### 4. Key performance indicators

A KPI is a defined measure used to track an objective, such as gross margin or on-time delivery. A KPI needs a formula, target, period, owner, and data lineage. A percentage can be misleading if its denominator is very small. Dashboard design should show context and uncertainty, not just a red/green icon.

### 5. Forecasting and planning

Forecasting uses historical warehouse values to estimate a future measure, subject to assumptions about trend, seasonality, and external events. A what-if analysis changes an input—price, promotion, inventory, or capacity—and estimates the response. The model and assumptions should be visible. Historical association does not by itself prove that changing a business lever will cause the predicted effect.

### 6. Business intelligence workflow

BI combines data preparation, semantic definitions, dashboards, ad hoc exploration, alerts, and decisions. A useful workflow is: identify a decision, find the relevant measures and dimensions, explore the data, validate the result, act, and monitor the outcome. The warehouse is an input to this workflow, not a substitute for asking a clear question.

### 7. Trust and governance

Users need data dictionary entries, ownership, refresh timestamp, quality status, and access controls. Definitions such as “active customer” must be consistent across reports. If only one team knows how a metric is calculated, a warehouse can multiply confusion. Training and documentation are part of usage.

## Worked examples

### Example 1: Festival stock decision

A retailer wants to know which stores need extra stock before a festival. The user slices sales by store, product category, and week, then compares the same weeks in prior years and checks promotion calendars. The decision is not based on a single total. The warehouse supplies consistent history; a planner applies stock policy and uncertainty.

### Example 2: Year-over-year revenue

Revenue is ₹1.2 million this year and ₹1.0 million last year. Relative growth is

\[
(1.2-1.0)/1.0=20\%.
\]

The absolute increase is 0.2 million and the relative growth is 20%. The term “20 percentage points” should be used only when the original metric itself is a percentage. The report must use the same product scope, currency, and calendar.

### Example 3: KPI definition

A dashboard defines on-time delivery as deliveries arriving by the promised date divided by all completed deliveries. If 920 of 1,000 deliveries are on time, the KPI is 92%. If a month is still loading, a provisional label and data timestamp prevent a false comparison.

## Key terms & formulas

- **Report:** repeatable presentation of a defined question.
- **Dashboard:** coordinated set of measures and filters.
- **Ad hoc analysis:** exploratory query not predefined in advance.
- **KPI:** defined measure tied to an objective.
- **Trend:** change over time.
- **Forecast:** estimate of a future measure.
- **What-if analysis:** evaluate a hypothetical input change.
- **Semantic layer:** consistent business definitions and calculations.
- **Data freshness:** time since the latest valid warehouse load.
- **Lineage:** path from source to published measure.

## Common mistakes

1. **Using a dashboard without checking its refresh status:** a number can be stale.
2. **Comparing different definitions or currencies:** the result is not a valid comparison.
3. **Calling a model forecast a fact:** assumptions and uncertainty matter.
4. **Using correlation as proof that a what-if change will work:** causal evidence is needed.
5. **Allowing every team to define a KPI differently:** trust collapses.
6. **Ignoring seasonal or incomplete periods:** comparisons can be misleading.

## Exam prep

**Likely 2-mark questions**
1. List four warehouse uses. *Hint: reports, dashboards, ad hoc analysis, trends, forecasting, and decision support.*
2. What is a KPI? *Hint: a defined measure linked to an objective.*
3. Why are data definitions important to BI users? *Hint: consistent, trusted measures across reports.*

**Likely long-answer questions**
1. Explain how a warehouse supports trend and comparison analysis. *Hint: time dimensions, aligned scope, formulas, quality.*
2. Describe reporting, dashboards, and ad hoc analysis with a retail example. *Hint: repeatable, overview, exploratory uses.*
3. Explain why forecasting and what-if analysis need assumptions and metadata. *Hint: model uncertainty, causal limits, lineage, and auditability.*
