---
subject: dwdm
unit: 5
topic: types-of-data-in-cluster-analysis
syllabus_ref: CSM3101 Unit-V
status: draft
---
# Types of Data in Cluster Analysis

## Overview

Clustering depends on how the data represents objects and attributes. Numeric, binary, categorical, ordinal, mixed, and high-dimensional data require different similarities and transformations. Choosing the wrong measure can produce formally correct but meaningless groups. This topic explains data types, normalization, distance and similarity measures, and their use in clustering.

## Explanation

### 1. Data matrix

An \(n\times p\) data matrix has \(n\) objects and \(p\) attributes. Rows are objects such as customers, documents, or sensors; columns are measured properties. Some attributes are continuous, some categorical, and some are derived. A mixed matrix may need a composite dissimilarity.

### 2. Numeric data

For numeric attributes, differences and ratios can be meaningful. **Min–max normalization** maps a value to

\[
x'=\frac{x-\min}{\max-\min}.
\]

**Z-score standardization** gives

\[
z=\frac{x-\mu}{\sigma}.
\]

Min–max preserves relative position in the observed range but is sensitive to outliers; z-score handles scale and is common in k-means. Robust scaling using the median and interquartile range can be preferable with skewed data.

Euclidean distance is

\[
d(\mathbf{x},\mathbf{y})=\sqrt{\sum_{j=1}^{p}(x_j-y_j)^2},
\]

while Manhattan distance is robust to a few large differences. Mahalanobis distance accounts for correlations and variances:

\[
d_M(\mathbf{x},\mathbf{y})
=\sqrt{(\mathbf{x}-\mathbf{y})^T\Sigma^{-1}(\mathbf{x}-\mathbf{y})}.
\]

Its covariance estimate must be reliable; in high dimensions it may be unstable.

### 3. Binary data

For binary vectors, simple matching disagreement is the fraction of differing attributes:

\[
d_{sm}=\frac{a+b}{m},
\]

where \(a\) counts 1–0, \(b\) counts 0–1, and \(m\) is the number of attributes. Jaccard distance compares shared 1s with the union of 1s:

\[
d_J=1-\frac{|\mathbf{x}\cap\mathbf{y}|}{|\mathbf{x}\cup\mathbf{y}|}.
\]

Jaccard is useful when many positions are zero and a shared feature matters. Hamming distance can treat every disagreement equally, which may not fit asymmetric data.

### 4. Nominal categorical data

Categories are labels without an inherent order, such as color `red`, `blue`, or payment method `card`, `cash`, `wallet`. A mismatch of two attributes has no natural magnitude. One-hot encoding can be used with appropriate distance, but many high-cardinality categories create sparse vectors and can overweight one category's multiple indicators. A category-specific mismatch matrix is often better.

### 5. Ordinal data

Categories have a meaningful order, such as `low < medium < high` or education levels. Numeric ranks can be used, but the spacing between levels may not be equal. If the intervals are not comparable, a rank-based or custom ordinal distance is safer.

### 6. Text and cosine similarity

A document can be a vector of word counts. Cosine similarity is

\[
\cos(\mathbf{x},\mathbf{y})
=\frac{\mathbf{x}\cdot\mathbf{y}}
{\|\mathbf{x}\|\|\mathbf{y}\|}.
\]

It measures direction rather than document length. Common words may dominate, so TF–IDF and stop-word removal are common preprocessing choices. Cosine distance is \(1-\cos\).

### 7. Mixed data and weighted Gower

Gower similarity combines a similarity for each attribute:

\[
s_G(x_i,x_j)=\frac{\sum_{j=1}^{p}w_j s_{ij}}{\sum_{j=1}^{p}w_j},
\]

using range similarity for numeric values, equality for nominal values, and a rank-based score for ordinal values. A composite distance is \(1-s_G\). Feature weights express which attributes matter more, but they introduce a modeling decision.

### 8. Correlation distance

For variables or standardized feature vectors, correlation measures similarity of pattern rather than level. Correlation distance is

\[
d_{\rho}=1-\rho,
\]

but it can be unstable with short series, constant values, or nonlinear relationships. It is not interchangeable with Euclidean distance.

### 9. Missing, noisy, and high-dimensional data

Missing values prevent direct distance calculation. Impute using training information, use a missingness-aware measure, or omit the attribute for that pair. Duplicate and noisy records can distort centroids. In high dimensions, distances concentrate; feature selection, weighting, or domain reduction may be needed before clustering.

## Worked examples

### Example 1: Min–max normalization

Income values are 20,000, 30,000, and 60,000. Min–max maps them to 0, 0.25, and 1. A value of 45,000 maps to

\[
(45{,}000-20{,}000)/(60{,}000-20{,}000)=0.625.
\]

A new value outside the training range can fall outside [0,1], so the training range should be stored and applied consistently.

### Example 2: Binary Jaccard

Two customer activity sets are:

- \(x=\{\text{web},\text{app},\text{email}\}\)
- \(y=\{\text{web},\text{app},\text{sms}\}\)

Intersection size is 2 and union size is 4:

\[
s_J=2/4=0.50,\quad d_J=0.50.
\]

Simple mismatch would be 2/4=0.50 here too, but the measures differ when one object has many features and the other few.

### Example 3: Cosine similarity

Document vectors are \(x=(1,2)\), \(y=(2,4)\). Dot product is 10 and norms are \(\sqrt5\) and \(\sqrt{20}\), so

\[
\cos=10/\sqrt{100}=1.
\]

They have the same direction even though \(y\) is twice as long. Euclidean distance is \(\sqrt5\), so cosine would be the better choice if length is irrelevant.

### Example 4: Mixed Gower similarity

Assume numeric similarity is 0.8, nominal equality is 1, and ordinal rank similarity is 0.5, all equally weighted:

\[
s_G=(0.8+1+0.5)/3=0.7667,
\quad d_G=0.2333.
\]

The weights should be justified by the application rather than selected only to produce attractive clusters.

## Key terms & formulas

- **Data matrix:** objects by attributes.
- **Min–max normalization:** \((x-\min)/(\max-\min)\).
- **Z-score:** \((x-\mu)/\sigma\).
- **Euclidean distance:** square root of squared differences.
- **Manhattan distance:** sum of absolute differences.
- **Mahalanobis distance:** covariance-weighted squared distance.
- **Jaccard similarity:** intersection divided by union.
- **Cosine similarity:** normalized dot product.
- **Gower similarity:** weighted average of per-attribute similarities.
- **Correlation distance:** \(1-\rho\).

## Common mistakes

1. **Using Euclidean distance on unnormalized nominal data:** category codes are arbitrary.
2. **Treating ordinal ranks as exact equal intervals:** order does not guarantee equal spacing.
3. **Using Jaccard on unordered features when length matters:** the measure ignores shared absences and length differently.
4. **Forgetting missing-value policy:** every distance needs a defined treatment.
5. **Using correlation distance on constant variables:** correlation is undefined.
6. **Interpreting a composite similarity as objective truth:** weights and definitions are choices.

## Exam prep

**Likely 2-mark questions**
1. Differentiate nominal and ordinal attributes. *Hint: labels only versus labels with order.*
2. State Euclidean and Jaccard similarity. *Hint: squared numeric differences versus intersection over union.*
3. Why use Gower similarity? *Hint: combine heterogeneous attribute types in one dissimilarity.*

**Likely long-answer questions**
1. Select an appropriate distance for numeric, binary, nominal, ordinal, and text data. *Hint: justify each choice.*
2. Compare z-score and min–max normalization, including outlier effects. *Hint: center/variance versus observed range.*
3. Explain cosine similarity for text clustering and a preprocessing pipeline. *Hint: term vectors, TF–IDF, direction, stop words, sparsity.*
