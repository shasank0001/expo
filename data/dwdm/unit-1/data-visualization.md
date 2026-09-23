---
subject: dwdm
unit: 1
topic: data-visualization
syllabus_ref: CSM3101 Unit-I
status: draft
---
# Data Visualization

## Overview

Data visualization represents values graphically so that people can detect distributions, trends, relationships, clusters, gaps, and anomalies quickly. It is both an exploratory tool, used before and during mining, and a communication tool, used to explain a result to a decision-maker. Visualization is not a substitute for data inspection: axes, scales, filters, missing values, and aggregation choices can create or hide apparent patterns.

Han, Kamber, and Pei include visualization among the core data-mining technologies. Tan, Steinbach, and Kumar use visualizations to understand distributions, outliers, and relationships before applying data-mining methods. This note follows that progression: select a visual encoding for the attribute type and question, read the chart carefully, and validate any apparent pattern quantitatively.

## Explanation

### 1. Purpose of visualization

Visualization can:

- reveal a distribution and its skewness;
- compare categories or groups;
- show change over time;
- expose relationships between two or more variables;
- identify clusters and outliers;
- show missing data and coverage gaps;
- inspect the result of cleaning, scaling, reduction, or discretization;
- communicate uncertainty and model performance;
- allow users to interact with a large dataset.

A good visualization answers a question. “Make a chart” is not enough. For example:

- Question: Are monthly sales increasing? → line chart.
- Question: How are ages distributed? → histogram.
- Question: Which category has the largest count? → bar chart.
- Question: Is there a relationship between height and weight? → scatter plot.
- Question: How does the median and spread vary by department? → box plot.
- Question: Where are high values across a two-dimensional grid? → heat map.

### 2. Visual encodings and perceptual effectiveness

Common visual channels include position, length, angle, area, color, shape, and connection. Position and length on a common scale are often easier to compare accurately than area or color intensity. A useful design principle is to encode the most important variable by the most accurately perceived channel.

A chart should include:

- a descriptive title;
- labeled axes with units;
- a readable scale;
- a legend when colors or shapes encode categories;
- a sample size or denominator;
- uncertainty intervals when relevant;
- a note about missing data and aggregation.

Color should not be the only way to convey a distinction. Use labels, shapes, or patterns as well for accessibility and grayscale printing.

### 3. Histograms and frequency distributions

A **histogram** displays the frequency of values in intervals for one numerical attribute. It is used to inspect center, spread, skewness, modality, gaps, and possible outliers.

For bin \(j\),

\[
\text{relative frequency}_j=\frac{n_j}{n}
\]

and, if bin width is \(\Delta_j\),

\[
\text{density}_j=\frac{n_j}{n\Delta_j}
\]

For equal-width bins, the area of a bar is proportional to its count. Bar width and bin origin can change the apparent shape, so a histogram should not be interpreted without its bin specification.

A histogram is different from a categorical bar chart. Adjacent numeric bins touch because they are intervals on a continuous scale; category bars usually have gaps.

### 4. Bar charts

A **bar chart** compares values across discrete categories such as departments, products, branches, or diagnosis groups. Length or height should begin at a meaningful zero when absolute quantities are compared.

Examples include:

- units sold by product category;
- number of students per branch;
- complaint rate by service type;
- accuracy by model version.

A sorted bar chart makes ranking easy, but sorting can hide the original natural order. A time-ordered bar chart may be less suitable than a line chart for a trend.

### 5. Line charts and time series

A **line chart** places observations on an ordered horizontal axis, usually time, and connects them. It is useful for trends, seasonality, changes, and turning points.

A line chart should show:

- the time unit and timezone if relevant;
- missing periods;
- irregular sampling intervals;
- uncertainty or forecast intervals;
- whether a smoothing method was used.

A smooth line can suggest values between observations that were never measured. Do not interpret the curve as observed data unless the underlying method and sampling support that interpretation.

### 6. Scatter plots

A **scatter plot** shows pairs \((x,y)\) as points. It helps reveal:

- linear or nonlinear relationships;
- clusters;
- gaps;
- heteroscedasticity;
- isolated points;
- subgroup differences.

Trend lines should state their method, uncertainty, and domain assumptions. A fitted line summarizes a relationship but does not prove causation. Overplotting can hide density; transparency, sampling, hexbinning, or density plots may help.

When values span several orders of magnitude, a logarithmic axis may reveal structure. A log axis cannot display zero or negative values without an explicit treatment.

### 7. Box plots and distribution comparison

A box plot summarizes a numeric distribution using the minimum, quartiles, median, maximum or whiskers, and possible outliers. Several box plots can compare groups on a common scale.

A box plot is compact but hides multimodality and the positions of individual values. Pair it with a jittered scatter plot or violin/density plot when individual observations matter.

### 8. Heat maps and multidimensional views

A **heat map** represents values using color in a grid or matrix. Rows and columns can represent dates, products, locations, classes, or features. It is effective for:

- seasonal patterns;
- correlation or similarity matrices;
- confusion matrices;
- geographic grids;
- sensor coverage;
- missingness and density.

Color scales should be perceptually uniform. A truncated color scale can exaggerate small differences; a sequential scale is normally used for magnitude, while a diverging scale is used for values around a meaningful midpoint.

### 9. Other useful views

- **Pie or donut charts:** part-to-whole comparisons for a small number of categories; angles and areas are harder to compare than lengths.
- **Violin plots:** distribution density and multimodality.
- **Parallel-coordinate plots:** many attributes across many objects; line crossings can quickly become cluttered.
- **Bubble charts:** three or more variables using position, size, and color; bubble area is difficult to compare precisely.
- **Network graphs:** relationships and clusters, but not ideal for precise numerical comparison.
- **Choropleth maps:** regional values, with care for area bias and geographic aggregation.

### 10. Interactive visualization

Interactive tools allow users to:

- filter by time, group, or category;
- zoom and pan;
- brush a region and inspect details;
- link several coordinated charts;
- change chart type or measure;
- show tooltips and record-level values.

Interaction helps exploration, but it can also encourage cherry-picking. The filter state, excluded records, and exact values should be visible and exportable.

### 11. Visualization before and after mining

Before mining, visualization can identify:

- data-entry errors and impossible values;
- class imbalance;
- skewness and heavy tails;
- clusters and outliers;
- missingness patterns;
- possible confounding variables.

After mining, it can show:

- confusion matrices and error types;
- residual plots;
- feature importance with uncertainty;
- decision boundaries;
- model drift over time;
- whether a discovered pattern agrees with the data distribution.

A visualization can suggest a hypothesis, but statistical testing, domain review, and an independent evaluation are needed before treating it as a reliable pattern.

## Worked examples

### Example 1: Histogram from a frequency distribution

Marks in a class are grouped as follows:

```text
Marks interval | Count
0–19           | 0
20–39          | 2
40–59          | 8
60–79          | 15
80–99          | 5
100             | 0
```

Total \(n=30\). Relative frequencies are:

```text
0–19: 0/30 = 0.000
20–39: 2/30 = 0.067
40–59: 8/30 = 0.267
60–79: 15/30 = 0.500
80–99: 5/30 = 0.167
100: 0/30 = 0.000
```

The histogram has its highest bar at 60–79. A reader should still check the bin definition, the number of observations, and whether zero marks are encoded separately from missing marks.

If the middle interval were 20 marks wide and the sample represented a population, its density would be

\[
\frac{8/30}{20} = 0.0133 \text{ per mark}
\]

but density is not usually needed when all bins have equal width.

### Example 2: Choosing a bar chart rather than a histogram

A shop compares units sold:

```text
Tea    120
Coffee 85
Juice  40
```

A bar chart shows the categories clearly. A histogram would imply a continuous ordered scale and adjacent intervals, which is misleading because the products are nominal categories. A zero baseline is needed for an honest magnitude comparison.

### Example 3: Detecting a trend

Monthly sales are:

```text
Month   Sales
Jan     100
Feb     108
Mar     107
Apr     120
May     135
Jun     132
```

A line chart reveals an overall rise with a small dip in March and June. The slope between January and June is

\[
\frac{132-100}{5}=6.4 \text{ units per month}
\]

This is an average slope, not proof of a constant increase. A forecast should account for the observed variation and possible seasonality.

### Example 4: Scatter plot and an apparent relationship

Study hours and marks are:

```text
Hours: 1, 2, 3, 4, 5, 6
Marks: 52, 61, 65, 73, 78, 85
```

A scatter plot shows an upward trend. A fitted line might be used to summarize it, but the plot should still show individual points. A high correlation would not prove that more study hours caused every observed increase; ability, prior preparation, and motivation may also vary.

### Example 5: Comparing groups with box plots

Two departments have test scores:

```text
Department A: 55, 60, 62, 64, 65, 67, 70, 95
Department B: 40, 45, 50, 55, 60, 65, 70, 75
```

The two box plots can compare medians and spreads. Department A's value 95 may appear as an outlier and should be checked. A box plot alone does not establish that Department A teaches better; the groups may differ in prior preparation, course difficulty, or sample selection.

### Example 6: Heat map of monthly demand

A retailer has a grid of categories by month. A heat map can reveal a high-demand band in one month and a low-demand gap in another. If colors are not labeled and the scale is not shown, a reader cannot tell whether a small numerical difference is large or trivial. Include the numeric range, missing cells, and the aggregation rule.

### Example 7: Visualizing a confusion matrix

A classifier has:

```text
                    Predicted negative  Predicted positive
Actual negative              90                 10
Actual positive                5                 15
```

A heat map makes the 5 false negatives and 10 false positives visible. Overall accuracy is

\[
\frac{90+15}{120}=0.875
\]

but the chart also shows that 5 of 20 actual positives were missed. The visual and the metric tell a more complete story.

## Key terms & formulas

- **Data visualization:** graphical representation of data for exploration, analysis, and communication.
- **Histogram:** a graph of frequencies across numerical intervals.
- **Bar chart:** a chart comparing values across categories.
- **Line chart:** a chart of values connected over an ordered axis, commonly time.
- **Scatter plot:** points representing pairs of numeric attributes.
- **Box plot:** a summary using median, quartiles, whiskers, and possible outliers.
- **Heat map:** a matrix encoded with color intensity.
- **Visual channel:** position, length, angle, area, color, shape, or connection used to encode a variable.
- **Relative frequency:** \(n_j/n\).
- **Histogram density:** \(n_j/(n\Delta_j)\).
- **Range:** \(x_{\max}-x_{\min}\).
- **IQR:** \(Q_3-Q_1\).
- **Correlation:** \(r=s_{XY}/(s_Xs_Y)\), a measure of linear association.
- **Residual:** \(y_i-\hat y_i\), the difference between observed and predicted values.
- **Confusion matrix:** a table of predicted classes against actual classes.
- **Visualization literacy:** the ability to read scales, encodings, uncertainty, and design choices critically.
- **Perceptual effectiveness:** how accurately a visual encoding supports comparisons.
- **Interactive visualization:** a display that responds to filtering, zooming, brushing, or linking.

## Common mistakes

1. **Using a histogram for nominal categories.** Use a bar chart for unordered categories.
2. **Using a bar chart for a continuous distribution.** A histogram shows intervals and their frequencies.
3. **Starting a magnitude bar chart at a nonzero baseline.** This can exaggerate differences.
4. **Omitting units, time periods, or sample sizes.** The viewer cannot interpret the scale or generalization.
5. **Using a log scale with zero or negative values without explanation.** The axis is undefined for nonpositive values.
6. **Treating a trend line as causal evidence.** A fitted line summarizes association.
7. **Trusting a smoothed line as if every point were observed.** Smoothing estimates between observations.
8. **Ignoring overplotting in a scatter plot.** Use transparency, density, sampling, or hexbinning when appropriate.
9. **Using color as the only distinction.** This reduces accessibility and may fail in grayscale.
10. **Hiding outliers in a summary chart.** Show individual or extreme observations where they matter.
11. **Changing bin boundaries without reporting them.** A histogram's apparent shape may change substantially.
12. **Interpreting an interactive filtered view as the whole population.** Display the active filter and excluded data.

## Exam prep

### Likely 2-mark questions

1. **What is data visualization?**  
   *Hint:* Graphical representation of data used to reveal distributions, relationships, trends, and anomalies.

2. **Differentiate a histogram and a bar chart.**  
   *Hint:* Histogram for numerical intervals; bar chart for discrete categories.

3. **What is a scatter plot used for?**  
   *Hint:* Showing the relationship between two numeric variables and identifying clusters, trends, and outliers.

4. **What does a box plot show?**  
   *Hint:* Median, quartiles, spread, whiskers, and possible outliers.

5. **What is a heat map?**  
   *Hint:* A matrix of values represented by color intensity.

6. **Why are units and axes important?**  
   *Hint:* They define the meaning, scale, and valid interpretation of the plotted values.

7. **What is interactive visualization?**  
   *Hint:* A visualization that responds to actions such as filtering, zooming, brushing, or linking views.

8. **What is a confusion matrix?**  
   *Hint:* A table comparing actual classes with predicted classes to show error types.

### Likely long-answer questions

1. **Explain the role of visualization in the data-mining process.**  
   *Answer hint:* Cover exploratory profiling, quality checks, pattern discovery, model evaluation, communication, interaction, and the need to verify visual suggestions quantitatively.

2. **Choose suitable visualizations for different data types and questions.**  
   *Answer hint:* Match histograms to numerical distributions, bar charts to categories, line charts to time, scatter plots to pairs, box plots to group distributions, and heat maps to matrices or spatial grids.

3. **Explain how to read a histogram and discuss bin-width effects.**  
   *Answer hint:* Define bins, counts, relative frequency, and density. Show how changing bin width can hide or create apparent peaks and why the bin convention must be reported.

4. **Discuss good visualization design and common errors.**  
   *Answer hint:* Address truthful axes, units, labels, accessible encodings, uncertainty, sample size, color scale, overplotting, aggregation, and misleading 3D or truncated scales.

5. **Explain how visualization supports model evaluation.**  
   *Answer hint:* Use residual plots, confusion matrices, ROC-like views when appropriate, calibration or error displays, and time monitoring, while noting that visuals do not replace formal metrics.
