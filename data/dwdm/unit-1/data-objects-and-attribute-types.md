---
subject: dwdm
unit: 1
topic: data-objects-and-attribute-types
syllabus_ref: CSM3101 Unit-I
status: draft
---
# Data Objects and Attribute Types

## Overview

A **data object** is a record, tuple, row, or item representing one case: a student, customer, product, transaction, sensor reading, or document. Its properties are **attributes**, also called fields, variables, or features. For example, a student object might have attributes `RollNo`, `Name`, `Branch`, `Attendance`, `Marks`, and `PassStatus`.

The attribute type determines which comparisons and operations are meaningful. Nominal attributes name categories, ordinal attributes have meaningful order, interval attributes support differences but not ratios, and ratio attributes have a meaningful zero. Binary, temporal, spatial, structural, and text attributes require additional care.

This topic is foundational because preprocessing, similarity measures, visualization, and mining algorithms all depend on the semantics of the data object and its attributes. The distinctions follow the introductory data representation treatment in Han, Kamber, and Pei and the measurement-scale and distance discussion in Tan, Steinbach, and Kumar.

## Explanation

### 1. Data objects, attributes, and tuples

A data object can be represented as a vector:

\[
\mathbf{x} = (x_1, x_2, \ldots, x_d)
\]

where \(d\) is the number of attributes and \(x_j\) is the value of attribute \(j\).

For student Asha, an object might be:

```text
(RollNo=101, Name=Asha, Branch=CSE, Attendance=86, Marks=78)
```

The same object is often called:

- a **record** in database terminology;
- a **tuple** in relational terminology;
- an **instance** in machine learning;
- an **item** or **case** in data-mining terminology.

A **data matrix** contains objects as rows and attributes as columns:

```text
RollNo | Name | Branch | Attendance | Marks
101    | Asha | CSE    | 86         | 78
102    | Bilal| ECE    | 72         | 64
```

A **data object set** is a collection of such objects. The object may represent a real entity, an event, an observation, or a document, depending on the task.

### 2. Attribute properties

An attribute has several properties beyond its type:

- **Name:** for example, `Attendance`.
- **Alias:** a second name used by a source system.
- **Position:** its location in the data object.
- **Type:** nominal, ordinal, interval, ratio, and so on.
- **Domain:** its permitted values, such as `{0,1,2,3,4,5}`.
- **Physical type:** integer, floating point, string, date, or image.
- **Logical type:** the meaning used by the application.
- **Missing-value rule:** how absent or unknown values are represented.
- **Security and privacy level:** whether access is restricted.
- **Provenance:** where the value came from and when it was updated.

A physical type alone is not enough. A value such as `2` can be a count, a category code, a rank, or a year. The meaning and measurement scale must be known.

### 3. Nominal attributes

A **nominal** attribute, also called a categorical or unordered attribute, identifies a category. Nominal values have names but no meaningful distance or order.

Examples:

- branch: CSE, ECE, ME;
- color: red, blue, green;
- material: wood, metal, plastic;
- marital status: single, married, divorced;
- yes/no answers.

Two nominal values can be said to be different, but one cannot normally be said to be twice the other. The mean of branch codes is meaningless even if the codes are 1, 2, and 3.

A nominal variable with \(k\) categories can be encoded using indicator variables, for example:

```text
Branch_CSE, Branch_ECE, Branch_ME
```

for three branches. This encoding allows numerical algorithms to process the categories without inventing an order.

### 4. Binary attributes

A **binary** attribute has only two states, usually represented as 0 and 1.

Examples:

- pass/fail;
- fraud/not fraud;
- yes/no;
- present/absent;
- approved/rejected;
- default/no default.

The coding convention must be documented. If `1 = fraud`, a row of 0 and 1 can be represented as:

```text
Transaction | Fraud
T001        | 0
T002        | 1
```

Some binary variables are symmetric because neither state should be considered the normal or preferred one. Other variables are asymmetric, such as disease present versus absent. A distance or error cost may need to treat the two states differently.

### 5. Ordinal attributes

An **ordinal** attribute has categories with a meaningful order, but the gaps between adjacent categories need not be equal.

Examples:

- satisfaction: poor, fair, good, excellent;
- size: small, medium, large;
- education level: school, diploma, bachelor's, master's;
- class rank categories;
- age categories: child, adult, senior.

It is meaningful to say that `good` is above `fair`, but it is not generally meaningful to say that the numerical difference between good and fair equals the difference between fair and poor.

A common rank encoding is:

\[
\operatorname{rank}(\text{poor})=1,\quad
\operatorname{rank}(\text{fair})=2,\quad
\operatorname{rank}(\text{good})=3,\quad
\operatorname{rank}(\text{excellent})=4
\]

This is useful when a method requires numerical values, but the chosen distances still require a defensible assumption.

### 6. Interval attributes

An **interval** attribute is numeric, and differences are meaningful, but ratios are not because zero is not a true absence of the quantity.

Examples:

- temperature in Celsius;
- temperature in Fahrenheit;
- calendar dates under a conventional numerical coding.

It is meaningful to say that 20°C is 5°C warmer than 15°C because the difference is \(20-15=5\). It is not meaningful to say that 20°C is twice as hot as 10°C. A ratio such as

\[
20/10=2
\]

does not represent a true doubling of temperature on the Celsius scale.

The Kelvin scale is ratio-scaled because zero kelvin represents absolute zero, but Celsius and Fahrenheit are interval-scaled.

### 7. Ratio attributes

A **ratio** attribute is numeric with a meaningful zero and meaningful ratios. Differences and ratios are interpretable.

Examples:

- age in years;
- height in centimeters;
- mass in kilograms;
- income in a stated currency;
- distance;
- duration;
- counts such as number of purchases.

If a person's height is 20 cm and another is 40 cm, 40 cm is twice the height. A value of zero age or zero duration means none of the measured amount. The unit must still be specified: height in centimeters and height in meters differ by a scale factor.

### 8. Temporal attributes

**Temporal attributes** represent time, date, duration, or an event order. Examples include:

- date of birth;
- transaction timestamp;
- duration between visits;
- month of a sale;
- age at diagnosis.

Time has special properties: it has direction and often cycles, and time-zone or daylight-saving conventions can affect calculations. A timestamp should not be treated as an ordinary number without preserving its calendar meaning.

### 9. Spatial and structural attributes

**Spatial attributes** describe location or shape: latitude, longitude, polygon, image, map, or geographic region. Euclidean distance in degrees is not automatically a ground distance near the poles or across a map projection.

**Structural attributes** describe relationships among objects, such as nodes and links in a graph, parent-child relationships, or positions in a hierarchy. A graph object may have adjacency and degree attributes in addition to numeric properties.

Text and documents are also structured or semi-structured objects. A document may have terms, counts, positions, and metadata, but individual word counts are usually sparse.

### 10. Keys, identifiers, and measurement attributes

An **identifier** distinguishes objects, such as a student roll number or customer ID. An identifier is useful for joining, uniqueness checks, and referencing, but it may carry no useful ordinal or numeric meaning.

A **descriptive or measurement attribute** represents a property used for analysis. For example, roll number identifies Asha, while attendance and marks describe her academic performance. Treating an ID as a continuous measurement can create meaningless distances and distorted averages.

A **key attribute** uniquely identifies a record in a relation. A foreign key connects records across relations. A composite key uses two or more attributes, such as `(courseID, semester)`, when one attribute alone is not unique.

### 11. Cardinality, sparsity, and missing values

The **cardinality** of an attribute is the number of distinct values it can take. A customer ID may have high cardinality; a yes/no field has cardinality two. High-cardinality attributes can cause overfitting, large indexes, and unstable models.

A **sparse** object has many missing or zero attributes, common in document-term matrices. A missing value may mean:

- the value is not available;
- the value is unknown;
- the field is not applicable;
- collection failed;
- zero was observed;
- the value was suppressed for privacy.

These meanings are not interchangeable. Treating every missing marker as zero can create false observations.

### 12. Choosing a representation

The attribute type guides:

- allowed operations (`<` is meaningful for ratio but usually not for nominal);
- summary statistics (a mean is meaningful for ratio, not for branch names);
- visual encodings (bars for categories, histograms for numeric distributions);
- distance functions (Euclidean for suitable numeric data, mismatch for nominal data);
- modeling and preprocessing choices.

A data dictionary should document each attribute's name, type, unit, domain, missing values, source, and permitted transformations.

## Worked examples

### Example 1: Classifying student attributes

A student record is:

```text
RollNo = 101
Name = Asha
Branch = CSE
Attendance = 86%
Average = 78
Pass = yes
```

The attributes are interpreted as follows:

- `RollNo`: nominal identifier; it distinguishes records but is not a useful numeric measurement.
- `Name`: nominal identifier or label.
- `Branch`: nominal attribute.
- `Attendance`: ratio percentage, assuming zero attendance is meaningful.
- `Average`: ratio or interval depending on whether zero is a meaningful score origin; it is commonly treated as a numeric score.
- `Pass`: binary attribute.

The record is not meaningfully summarized by averaging RollNo, Name, and Branch.

### Example 2: Nominal mismatch distance

Three customers have colors red, blue, and red.

Using a simple nominal mismatch measure, the number of mismatched attributes between customer 1 and customer 2 is 1; between customers 1 and 3 it is 0. The distance matrix is:

```text
       R1 R2 R3
R1      0  1  0
R2      1  0  1
R3      0  1  0
```

Although the mismatch count is useful for this simple case, it assumes that every color mismatch is equally important. Domain knowledge may require a different cost.

### Example 3: Ordinal ranks

Survey responses are mapped as:

```text
poor = 1
fair = 2
good = 3
excellent = 4
```

The average of two `good` responses is 3. This is a convenient rank summary. However, it assumes the step from fair to good is comparable to the step from good to excellent. If that assumption is inappropriate, report category proportions or use a more carefully designed scale.

### Example 4: Interval temperature

Temperatures are 15°C and 20°C.

The difference is meaningful:

\[
20-15=5^\circ C
\]

The ratio is not meaningful as a statement of physical heat:

\[
20/15=1.33
\]

does not mean the object is “1.33 times as hot.” Convert to Kelvin before using a ratio interpretation if that is scientifically valid.

### Example 5: Ratio income

Annual incomes are ₹200,000 and ₹500,000. The first is 40% of the second, not half of it:

\[
200{,}000/500{,}000=0.4
\]

The person with the lower income earns 40% of the higher income, because zero income is a meaningful absence of income. A geometric mean is more appropriate than an arithmetic mean for very skewed income data.

### Example 6: Missing values in a document-term vector

A document has 20,000 possible terms, but only 40 occur. If zero is used for every nonoccurring term, the vector is highly sparse.

```text
terms: 20000
nonzero: 40
sparsity = 1 - 40/20000 = 0.998
```

A zero here may mean “term not observed,” not that the term has a measured numeric value of zero. Missing-value handling must follow the representation.

## Key terms & formulas

- **Data object:** one case represented by a record, tuple, row, item, or vector.
- **Attribute:** a property or field of a data object.
- **Data matrix:** a collection of objects and attributes.
- **Nominal attribute:** a category with no natural order.
- **Binary attribute:** an attribute with two states, often 0 and 1.
- **Ordinal attribute:** a category with meaningful order but not necessarily equal intervals.
- **Interval attribute:** a numeric attribute with meaningful differences and no meaningful ratio.
- **Ratio attribute:** a numeric attribute with meaningful differences, ratios, and a true zero.
- **Nominal mismatch distance:** the number or proportion of nominal attributes that differ.
- **Temporal attribute:** an attribute involving date, time, duration, or event order.
- **Spatial attribute:** an attribute describing geographic position, shape, or space.
- **Identifier:** a value used to identify or distinguish an object.
- **Key:** an attribute or set of attributes that uniquely identifies records.
- **Cardinality:** the number of distinct values in an attribute.
- **Sparsity:** the proportion of zero or missing entries in a representation.
- **Missing value:** an unavailable or unknown value; its reason must be recorded.
- **Rank encoding:** assigning ordered integers to ordinal categories.
- **Indicator encoding:** creating one binary variable for each category of a nominal attribute.
- **Sparsity formula:** \(1-\frac{\text{nonzero entries}}{\text{all entries}}\).
- **Cardinality:** \(\left|\{x:x\in\mathcal D\}\right|\), the number of distinct values in domain \(\mathcal D\).

## Common mistakes

1. **Treating an identifier as a continuous measurement.** Roll numbers and customer IDs usually have no meaningful arithmetic.
2. **Averaging nominal values.** Branch codes `1,2,3` are labels, not quantities.
3. **Using a ratio on Celsius temperature.** Celsius has meaningful differences but no true zero.
4. **Assuming ordinal gaps are equal.** The difference between poor and fair need not equal that between good and excellent.
5. **Confusing missing with zero.** “Not recorded,” “not applicable,” and an observed zero are different facts.
6. **Using a different unit without recording it.** A value of 1000 in grams is not the same measurement as 1000 in kilograms.
7. **Encoding a nominal attribute with arbitrary numeric ranks.** Doing so makes `ECE` appear between `CSE` and `ME`, which may be false.
8. **Ignoring metadata.** A field's unit, source, update time, and missing-value code are essential.
9. **Treating a document's unobserved terms as measured zeros.** The vector is usually sparse and zero has a representation-specific meaning.
10. **Using the same distance for every attribute type.** The measure must respect nominal, ordinal, interval, and ratio semantics.

## Exam prep

### Likely 2-mark questions

1. **Define a data object and attribute.**  
   *Hint:* An object is one case; an attribute is a property measured or described for that case.

2. **Differentiate nominal and ordinal attributes with examples.**  
   *Hint:* Nominal categories have names; ordinal categories also have a meaningful order.

3. **Why is Celsius an interval attribute?**  
   *Hint:* Temperature differences are meaningful, but ratios are not because zero Celsius is not absence of heat.

4. **Give two ratio attributes.**  
   *Hint:* Age, height, mass, income, duration, or count, with the unit and meaningful zero stated.

5. **What is a binary attribute?**  
   *Hint:* An attribute with two states, such as yes/no or pass/fail.

6. **Why should an identifier not be averaged?**  
   *Hint:* Its numerical code identifies records and usually has no meaningful arithmetic order or magnitude.

7. **What is a temporal attribute?**  
   *Hint:* An attribute representing date, time, duration, or event order.

8. **Define cardinality.**  
   *Hint:* The number of distinct values an attribute can take.

### Likely long-answer questions

1. **Explain data objects, attributes, and their properties with examples.**  
   *Answer hint:* Define the terms, describe a data matrix, and discuss name, alias, position, type, domain, physical/logical type, missing values, security, and provenance.

2. **Explain nominal, ordinal, interval, and ratio attribute types.**  
   *Answer hint:* Compare order, differences, ratios, meaningful zero, and valid operations. Give separate examples and show why arbitrary numeric codes can be misleading.

3. **Discuss binary, temporal, spatial, and identifier attributes.**  
   *Answer hint:* Explain their representations, symmetry or directionality, time semantics, geometric limitations, and why identifiers should not be treated as measurements.

4. **Why are metadata and missing-value meanings important?**  
   *Answer hint:* Explain units, source, domain, update time, null codes, not-applicable values, and how incorrect assumptions corrupt summaries, distances, and mined patterns.

5. **Choose appropriate representations for a student, transaction, and document dataset.**  
   *Answer hint:* Identify object grain, attributes, types, identifiers, binary fields, temporal fields, sparsity, and the operations each representation can safely support.
