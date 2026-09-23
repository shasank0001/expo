---
subject: dwdm
unit: 1
topic: motivation-for-data-warehousing-and-data-mining
syllabus_ref: CSM3101 Unit-I
status: draft
---
# Motivation for Data Warehousing and Data Mining

## Overview

Organizations collect data far faster than they can interpret it. Daily systems record millions of transactions, web events, sensor readings, student records, and customer interactions. Much of this data is historical, detailed, and stored across incompatible systems. Simple operational databases answer current tasks, but they are not designed to reveal multi-year trends or relationships among many variables.

A **data warehouse** makes large collections of data available in an integrated, consistent, historical form for analysis. **Data mining** then searches that form for useful patterns, models, and knowledge. Together, they support decisions such as inventory planning, customer targeting, fraud detection, medical diagnosis, and scientific discovery.

The treatment here follows Han, Kamber, and Pei's distinction between data warehousing, data mining, and analytical decision support, together with Tan, Steinbach, and Kumar's emphasis on data quality, types, and analysis. For examination purposes, learn the four defining characteristics of a data warehouse, the difference between OLTP and OLAP, and the reasons that integration and pattern discovery are necessary.

## Explanation

### 1. The growth of organizational data

Data growth comes from several directions:

- transactional systems record purchases, payments, bookings, and stock changes;
- websites record searches, clicks, page visits, and responses;
- mobile and IoT devices continuously produce sensor measurements;
- scientific instruments and simulations create large result sets;
- customer-service, communication, and billing systems retain histories;
- regulations and business policies require records to be preserved.

If a value grows at a constant annual rate \(r\), then after \(n\) years its approximate size is

\[
V_n = V_0(1+r)^n
\]

For example, a company starting with 1 million events per day and growing by 20% per year will process approximately

\[
1.0 \times 1.2^5 = 2.488 \text{ million events per day}
\]

after five years. Volume alone is a problem, but organization is also necessary. More data is useful only when it is complete, consistent, correctly defined, and available at the right time and level of detail.

### 2. Why an operational DBMS is not enough

Operational systems, also called OLTP systems, are optimized for short transactions such as recording an order, changing a balance, or registering a student. Their goals include high concurrency, rapid updates, constraint enforcement, and recovery.

They usually have the following characteristics:

- detailed current data;
- rapid insert, update, and delete operations;
- normalized structures designed for application transactions;
- limited historical analysis;
- data optimized for individual departments;
- many small queries.

Analytical users have different needs. A manager may ask:

- Which product families have grown for six consecutive quarters?
- How do customers differ in profitability and retention?
- Which branches have unusual complaint patterns?
- What combinations of treatments lead to better medical outcomes?
- How will next month's demand change under different promotions?

These queries inspect many records, many months, and many attributes. Running them directly on many OLTP databases can be slow and can disrupt daily operations. Analytical processing is therefore separated from routine transactions.

### 3. Data warehousing

In Han, Kamber, and Pei, a data warehouse is a **subject-oriented, integrated, time-variant, and nonvolatile collection of data** that provides support for management's decision-making process. This is often remembered as the SITS properties.

1. **Subject-oriented:** data is organized around major business or analytical subjects—customer, product, sales, student, or event—rather than around one application.
2. **Integrated:** data from different sources is reconciled to common formats, names, codes, and units.
3. **Time-variant:** data is retained with explicit time periods so that history and change can be analyzed.
4. **Nonvolatile:** analytical data is normally loaded and maintained as history; ordinary users do not continually overwrite old records.

These properties distinguish a warehouse from an ordinary departmental database.

### 4. Facts, dimensions, and granularity

A warehouse commonly contains:

- **Fact table:** records quantitative measures or events, such as sales amount, quantity, marks, visit count, or cost.
- **Dimension table:** descriptive context such as date, product, customer, branch, course, or location.
- **Grain:** the level of detail represented by one fact record.

Example grain: **one sales transaction line for one product on one day in one store**.

A useful fact table for a retailer might contain:

```text
FACT_SALES(DateKey, StoreKey, ProductKey, Units, Revenue, Discount)
```

Dimension tables might contain:

```text
DIM_DATE(DateKey, Day, Month, Quarter, Year)
DIM_PRODUCT(ProductKey, Category, Subcategory, Product)
DIM_STORE(StoreKey, City, Region)
```

The grain must be stated clearly. If a table contains one row per invoice line, it should not silently be treated as one row per customer. Incorrect grain can double-count measures or create invalid totals.

### 5. ETL and ELT

Sources do not automatically become a usable warehouse. Data passes through extraction, transformation, and loading:

- **Extract:** obtain data from operational databases, files, APIs, sensors, and external sources.
- **Transform:** clean values, reconcile codes and units, join records, derive measures, and detect errors.
- **Load:** insert validated data into the warehouse at the correct grain and time.

Some systems use **ELT**, where raw data is loaded first and transformation occurs within the analytical platform. Either approach requires lineage, validation, security, and quality checks.

### 6. OLAP and analytical processing

Online Analytical Processing (OLAP) organizes data for multidimensional views such as time, geography, product, and customer. Common operations include:

- **Roll-up:** move from month to quarter or day to year.
- **Drill-down:** move from year to quarter, month, or day.
- **Dice:** select particular values or ranges across several dimensions.
- **Slice:** select one dimension value, such as only the North region.
- **Pivot:** rearrange a selected measure across dimensions.

For example, the measure `SUM(Revenue)` can be displayed by rows = month and columns = product category. A drill-down may split a yearly total into quarters and months.

### 7. Why data mining is needed

A warehouse supplies high-quality analytical data, but managers still need methods that go beyond simple summaries. Data mining searches large data for patterns that are difficult to notice manually. It can:

- classify records into known categories;
- predict a likely outcome;
- find items or events that occur together;
- group similar objects without a predefined label;
- identify unusual observations;
- summarize groups and reveal trends.

The result is a **pattern** that satisfies a usefulness condition, often expressed as support, confidence, a prediction accuracy, or another domain-specific threshold.

### 8. Business, scientific, and social motivations

Organizations may mine data to:

- improve marketing and customer retention;
- reduce cost and optimize supply chains;
- detect fraud and manage risk;
- improve clinical diagnosis and treatment planning;
- predict maintenance needs;
- monitor public health, transport, and education;
- study scientific phenomena in biology, astronomy, climate, and engineering.

A valid data-mining solution must improve a real decision process, not merely produce a high score. Its output must be explainable enough for the intended user, legally and ethically usable, and supported by reliable data.

## Worked examples

### Example 1: Separating daily operations from historical analysis

A supermarket's operational database records every sale for billing. During a busy hour, an analyst's query joins five large tables and scans years of data. This can slow checkout operations.

A warehouse stores a daily summarized fact:

```text
Date       | ProductCategory | Units | Revenue | Profit
2026-01-01 | Bread            | 420   | 25200   | 6300
2026-01-01 | Milk             | 510   | 30600   | 7650
2026-01-01 | Soap             | 180   | 14400   | 4320
```

Now the analyst can answer questions across many dates without placing a heavy analytical query on the billing system. New sales are usually appended as time passes; old analytical records are not routinely modified.

### Example 2: Verifying the four warehouse properties

A hospital warehouse contains a **patient** table with age, district, diagnosis, and treatment history, not separate tables named after each department: this is **subject-oriented**. It maps sex codes, blood-pressure units, and district codes to shared definitions: this is **integrated**. It stores treatment years from 2019 through 2026: this is **time-variant**. Historical treatment records are stable and are normally corrected through controlled updates rather than continually overwritten: this is **nonvolatile**.

### Example 3: Basket analysis and decision improvement

A store analyzes 100 transactions. Bread and milk occur together in 20 transactions.

\[
\text{Support}(\{\text{bread, milk}\}) = 20/100 = 0.20
\]

Suppose 20 of the 25 bread purchases include milk:

\[
\text{Confidence}(\text{bread} \rightarrow \text{milk}) = 20/25 = 0.80
\]

The retailer can test nearby placement or a bundle offer. The mining output alone does not guarantee higher profit; an experiment or careful evaluation is still needed.

### Example 4: Growth calculation

An online service begins with 500 GB of logs per month and grows by 35% each year.

After three years:

\[
V_3 = 500(1.35)^3 \approx 500(2.460375) \approx 1230.19 \text{ GB}
\]

Thus the service manages more than twice its original monthly volume. This motivates distributed storage, integration, automated pipelines, and analytical processing.

### Example 5: Turning a historical pattern into a prediction

A training set contains past purchases. A model finds that customers who renew within 30 days are more likely to buy an insurance product later. After validation on a separate period, the organization may use the score to target a campaign. It must still check false positives, consent, fairness, and whether the historical population represents future customers.

## Key terms & formulas

- **Data warehousing:** collecting, organizing, and managing data for analytical and decision-support use.
- **SITS:** Subject-oriented, Integrated, Time-variant, and Nonvolatile—the four defining warehouse properties.
- **OLTP:** Online Transaction Processing, optimized for routine operational updates.
- **OLAP:** Online Analytical Processing, optimized for multidimensional analysis of aggregated data.
- **ETL:** Extract, Transform, Load.
- **ELT:** Extract, Load, Transform.
- **Fact:** a measured event or quantitative observation in a warehouse.
- **Dimension:** descriptive context for a fact, such as time, product, or location.
- **Grain:** the detail represented by one warehouse record.
- **Data warehouse metadata:** definitions, sources, transformations, loading times, and lineage.
- **Decision support:** systems and analyses that help managers choose actions.
- **Data mining:** discovery of useful patterns, relationships, models, and knowledge from data.
- **Pattern:** a repeatable and interesting relationship or structure supported by data.
- **Business understanding:** defining the decision or problem before selecting a mining method.
- **Analytical dataset:** a collection selected and prepared for a particular question.
- **Data growth formula:** \(V_n = V_0(1+r)^n\).
- **Support:** \(\operatorname{support}(A) = \frac{\text{transactions containing } A}{\text{all transactions}}\).
- **Confidence:** \(\operatorname{confidence}(A \rightarrow B) = \frac{\text{transactions containing } A \text{ and } B}{\text{transactions containing } A}\).
- **Lift:** \(\operatorname{lift}(A \rightarrow B) = \frac{\text{confidence}(A \rightarrow B)}{\operatorname{support}(B)}\). Lift greater than 1 indicates positive association.

## Common mistakes

1. **Calling a warehouse merely a very large database.** A warehouse is designed around analytical subjects, integrated history, and decision support.
2. **Forgetting one SITS property.** Exam answers should explicitly state subject-oriented, integrated, time-variant, and nonvolatile.
3. **Confusing OLTP with OLAP.** OLTP handles current transactions; OLAP explores summarized, multidimensional data.
4. **Treating integration as copying files.** Names, codes, units, identifiers, and meanings must be reconciled.
5. **Ignoring grain.** A statement such as “revenue is ₹2 million” is ambiguous until the fact level is known.
6. **Assuming nonvolatile means incorrectable.** Corrections and controlled updates are possible; ordinary analytical loading does not continuously overwrite history.
7. **Confusing data warehousing with data mining.** Warehousing prepares and stores analytical data; mining discovers patterns from it.
8. **Assuming a statistically strong rule should be deployed immediately.** Business cost, risk, fairness, and an actual evaluation are necessary.
9. **Ignoring data volume growth.** Storage, access time, and processing cost must be planned for future volume, not only today's data.

## Exam prep

### Likely 2-mark questions

1. **Define a data warehouse.**  
   *Hint:* Give the Han–Kamber–Pei definition and list subject-oriented, integrated, time-variant, and nonvolatile.

2. **Differentiate DBMS and data warehouse.**  
   *Hint:* Compare operational current transactions with subject-oriented historical analytical data and SITS properties.

3. **What is ETL?**  
   *Hint:* Explain extraction from sources, transformation and reconciliation, and loading into the analytical store.

4. **What is data mining?**  
   *Hint:* A process that searches data for useful patterns and knowledge to support decisions.

5. **Define fact and dimension with an example.**  
   *Hint:* A fact records a measure or event; a dimension gives context such as date, product, or customer.

6. **What is the grain of a fact table?**  
   *Hint:* The level of detail represented by one fact record, such as one sale line per product per day.

7. **State two reasons organizations build warehouses.**  
   *Hint:* Give historical analysis and reduced impact on OLTP, or integrated decision support and long-term trends.

8. **What is a roll-up operation?**  
   *Hint:* Summarize detailed values along a dimension, for example month to quarter to year.

### Likely long-answer questions

1. **Explain the four defining characteristics of a data warehouse with examples.**  
   *Answer hint:* Define each SITS characteristic and use a hospital or retail warehouse to show how it is satisfied. Mention how the properties improve historical analytical work.

2. **Compare OLTP, OLAP, data warehousing, and data mining.**  
   *Answer hint:* Explain the purpose, data orientation, time range, update pattern, and main users of each. Include a case where transactions feed an integrated warehouse and mined patterns support action.

3. **Describe facts, dimensions, and grain in a star-schema design.**  
   *Answer hint:* State one explicit grain, identify a fact table, name several dimensions, explain keys and measures, and show how drill-down or roll-up changes the view without changing grain.

4. **Explain why data integration and quality control are necessary before mining.**  
   *Answer hint:* Discuss duplicate identifiers, inconsistent units and codes, missing values, timestamps, entity resolution, validation, metadata, and their effect on the reliability of discovered patterns.

5. **Describe the motivation for data mining in a real organization or scientific field.**  
   *Answer hint:* Identify the decision, data sources, business or scientific value, pattern type, evaluation measure, possible deployment, and privacy or bias concerns.
