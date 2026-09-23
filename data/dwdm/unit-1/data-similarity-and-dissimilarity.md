---
subject: dwdm
unit: 1
topic: data-similarity-and-dissimilarity
syllabus_ref: CSM3101 Unit-I
status: draft
---
# Estimating Data Similarity and Dissimilarity

## Overview

A similarity measure quantifies how alike two data objects are. A dissimilarity measure, often called a distance, quantifies how different they are. Both are needed by clustering, nearest-neighbor classification, recommendation, duplicate detection, anomaly detection, and comparison of measurements.

The correct measure depends on the attribute types and their scales. Euclidean distance is suitable for suitably scaled numerical data, mismatch distance is suitable for nominal data, ranks are needed for ordinal data, and cosine or Jaccard similarity handles vectors or binary sets. A small raw distance is not necessarily meaningful when one attribute uses a much larger range or different unit.

This topic combines the introductory similarity treatment in Han, Kamber, and Pei with the measurement-scale and distance discussion in Tan, Steinbach, and Kumar. The central habit is to state the data representation, scale, direction, and assumptions before calculating a distance.

## Explanation

### 1. Data objects as vectors

Let two objects be

\[
\mathbf{x}=(x_1,x_2,\ldots,x_d),\qquad
\mathbf{y}=(y_1,y_2,\ldots,y_d)
\]

where each coordinate is an attribute value. A dissimilarity function should return zero for identical objects under the chosen representation and should become larger as objects become more different. A similarity function should generally be larger for more alike objects.

The terms “close” and “far” are meaningful only relative to a feature space and a task. Two students with the same total marks may be far apart if one has very high attendance and the other very low attendance. A representation that omits an important variable can make genuinely different objects appear identical.

### 2. Euclidean distance

For numerical attributes, the \(L_2\) or Euclidean distance is

\[
d_E(\mathbf{x},\mathbf{y})=
\sqrt{\sum_{j=1}^{d}(x_j-y_j)^2}
\]

It is the straight-line distance in the coordinate space. A small distance means the objects are numerically close, but the result depends on scale.

A weighted Euclidean distance is

\[
d_w(\mathbf{x},\mathbf{y})=
\sqrt{\sum_{j=1}^{d}w_j(x_j-y_j)^2}
\]

where \(w_j\ge 0\) reflects the importance of attribute \(j\). A zero weight removes an attribute; a large weight makes a difference on that attribute count more.

### 3. Manhattan or city-block distance

The \(L_1\) distance is

\[
d_1(\mathbf{x},\mathbf{y})=\sum_{j=1}^{d}|x_j-y_j|
\]

It adds absolute differences. It is useful when movement along each coordinate is considered separately, when differences should not be squared, or when the representation has an \(L_1\) geometry. Like Euclidean distance, it is affected by units and scale.

### 4. Chebyshev and Minkowski distances

The Chebyshev or maximum-coordinate distance is

\[
d_\infty(\mathbf{x},\mathbf{y})=\max_j |x_j-y_j|
\]

It reports the largest single-coordinate difference.

The Minkowski distance is

\[
d_p(\mathbf{x},\mathbf{y})=
\left(\sum_{j=1}^{d}|x_j-y_j|^p\right)^{1/p},
\qquad p\ge 1
\]

For \(p=1\), it is Manhattan distance. For \(p=2\), it is Euclidean distance. As \(p\) increases, the largest coordinate differences have greater influence. For \(p\to\infty\), the measure approaches Chebyshev distance.

### 5. Attribute scaling

Suppose age is measured in years and income in rupees. Income differences may be numerically much larger, so an unnormalized distance can be dominated by income even when age is equally important.

#### Min-max normalization

For an attribute with observed minimum \(a\) and maximum \(b\),

\[
x'=\frac{x-a}{b-a}
\]

For marks with minimum 40 and maximum 100:

\[
x'=\frac{x-40}{100-40}
\]

Marks 70 become

\[
\frac{70-40}{60}=0.5
\]

This maps the observed range to \([0,1]\). New values outside the training range may fall outside this interval; the original training bounds should be reused for consistency.

#### Z-score standardization

\[
z=\frac{x-\mu}{\sigma}
\]

where \(\mu\) and \(\sigma\) are estimated from the training data. A z-score of -1 means one standard deviation below the training mean. It preserves relative differences in units of standard deviation and is useful when attributes have different spreads.

Scaling parameters should be estimated on training data and applied consistently to validation, test, and production data. Fitting a scaler separately on the test set leaks information.

### 6. Similarity and distance for nominal data

For nominal attributes, calculate a mismatch indicator:

\[
\delta(x_j,y_j)=
\begin{cases}
0, & x_j=y_j\\
1, & x_j\ne y_j
\end{cases}
\]

A simple mismatch dissimilarity is

\[
d(\mathbf{x},\mathbf{y})=\frac{1}{d}\sum_{j=1}^{d}\delta(x_j,y_j)
\]

if every attribute is counted equally. A weighted version is

\[
d(\mathbf{x},\mathbf{y})=
\frac{\sum_j w_j\delta(x_j,y_j)}{\sum_j w_j}
\]

This treats a mismatch as a cost, but it does not claim that all category pairs are equally different. If that distinction matters, define a category-distance matrix.

### 7. Ordinal attributes

For an ordinal attribute with ordered ranks \(r(x_j)\) and \(r(y_j)\), a common mismatch is

\[
\delta_j=\frac{|r(x_j)-r(y_j)|}{R-1}
\]

where \(R\) is the number of ordered levels. The rank difference is normalized to keep it comparable with other attribute distances. This is useful when the order matters, but the exact conversion still involves a modeling choice about the gaps.

### 8. Cosine similarity

For vectors \(\mathbf{x}\) and \(\mathbf{y}\),

\[
\operatorname{cos}(\mathbf{x},\mathbf{y})=
\frac{\mathbf{x}\cdot\mathbf{y}}
{\|\mathbf{x}\|\|\mathbf{y}\|}
\]

Cosine similarity compares direction, not magnitude. It is widely used for text term-frequency vectors and recommendations. A related cosine distance is

\[
d_{\cos}=1-\cos(\mathbf{x},\mathbf{y})
\]

Zero vectors have undefined cosine similarity and must be handled separately.

### 9. Binary similarity

For a binary attribute, there are four counts:

- \(a\): both have 1;
- \(b\): first has 1 and second has 0;
- \(c\): first has 0 and second has 1;
- \(d\): both have 0.

The **Jaccard similarity** is

\[
J=\frac{a}{a+b+c}
\]

and its dissimilarity is

\[
d_J=1-J=\frac{b+c}{a+b+c}
\]

Jaccard ignores the joint zeros. It is useful when zeros mean “not present” and there are many such entries, as in document-term or item-indicator data.

A simple mismatch similarity is

\[
s_{\text{match}}=\frac{a+d}{a+b+c+d}
\]

This treats agreement on zeros as evidence of similarity. The choice between Jaccard and matching similarity depends on what a zero means.

### 10. Correlation distance and shape

When overall scale and offset are unimportant but the pattern of variation matters, correlation similarity can be used. The Pearson correlation between two vectors is

\[
s_{\text{corr}}=
\frac{\sum_j(x_j-\bar{x})(y_j-\bar{y})}
{\sqrt{\sum_j(x_j-\bar{x})^2\sum_j(y_j-\bar{y})^2}}
\]

A related distance is

\[
d_{\text{corr}}=1-s_{\text{corr}}
\]

Correlation distance is useful for comparing shapes or time-series profiles, but it is not appropriate for a single constant vector and can hide a constant offset.

### 11. Mixed and weighted distances

For objects with nominal, ordinal, interval, and ratio attributes, first compute a meaningful component for each type and then combine them. A general form is

\[
d(\mathbf{x},\mathbf{y})=
\frac{\sum_j w_jd_j(x_j,y_j)}{\sum_j w_j}
\]

For example, a weighted Euclidean component can be combined with normalized nominal mismatch. The weights express application priorities, not universal facts. They should be validated and documented.

### 12. Properties of a distance

A true metric often satisfies:

- **Identity of indiscernibles:** \(d(x,y)=0\) if and only if \(x=y\);
- **Non-negativity:** \(d(x,y)\ge 0\);
- **Symmetry:** \(d(x,y)=d(y,x)\);
- **Triangle inequality:** \(d(x,z)\le d(x,y)+d(y,z)\).

Many practical dissimilarity measures are useful but do not satisfy every metric property, especially after thresholding or one-to-one matching. Do not assume that a similarity score is a metric simply because it is called a distance.

## Worked examples

### Example 1: Euclidean, Manhattan, and Chebyshev distances

Objects:

\[
\mathbf{x}=(1,2),\qquad \mathbf{y}=(4,6)
\]

Differences are \((3,4)\).

\[
d_E=\sqrt{3^2+4^2}=5
\]

\[
d_1=|3|+|4|=7
\]

\[
d_\infty=\max(3,4)=4
\]

The same pair has different distances because the measures encode different geometries. Neither value tells us whether the two students are similar until the attributes and their importance are known.

### Example 2: Minkowski distance

For \(\mathbf{x}=(1,2)\), \(\mathbf{y}=(4,6)\), and \(p=3\):

\[
d_3=(|3|^3+|4|^3)^{1/3}
=(27+64)^{1/3}
\approx4.50
\]

The result lies between the Manhattan and Chebyshev values for these differences, illustrating the role of \(p\).

### Example 3: Weighted distance and scaling

Suppose two applicants have:

```text
           Test score (0–100)   Interview rating (1–5)
A                 80                  4
B                 90                  5
```

Raw differences are 10 and 1, so raw Euclidean distance is

\[
\sqrt{10^2+1^2}=\sqrt{101}\approx10.05
\]

The test difference dominates because its range is larger. If **both** attributes are min-max normalized using training ranges test \(0\)–\(100\) and interview \(1\)–\(5\), the vectors become

```text
A = (80/100, (4-1)/(5-1)) = (0.80, 0.75)
B = (90/100, (5-1)/(5-1)) = (0.90, 1.00)
```

The coordinate differences are 0.10 and 0.25, so the normalized Euclidean distance is

\[
\sqrt{0.10^2+0.25^2}
=\sqrt{0.0725}
\approx0.269
\]

Scaling has made the two attributes' ranges comparable; it has not made their differences equal or declared them equally important. Weights or a z-score representation may be preferable when the domain gives the measures different priorities. Scaling is a modeling decision, not a cosmetic step.

### Example 4: Nominal mismatch

Customers:

```text
x = (CSE, red, Mumbai)
y = (ECE, red, Delhi)
```

For three equally weighted nominal attributes, the mismatches are branch and city, while color matches. Thus:

\[
d(\mathbf{x},\mathbf{y})=\frac{2}{3}\approx0.667
\]

If location is more important than color, use weights and a different normalized total.

### Example 5: Ordinal distance

Customer satisfaction levels use:

```text
poor = 1, fair = 2, good = 3, excellent = 4
```

For `fair` and `excellent', \(R=4\):

\[
d=\frac{|2-4|}{4-1}=\frac{2}{3}\approx0.667
\]

For `poor` and `fair`:

\[
d=\frac{|1-2|}{3}=\frac{1}{3}\approx0.333
\]

The order is respected. The values are rank-based, so a real measurement-scale interpretation should be justified.

### Example 6: Cosine similarity

Text-document vectors are:

```text
x = (3, 4)
y = (6, 8)
```

They point in the same direction. Thus:

\[
\cos(\mathbf{x},\mathbf{y})
=\frac{3(6)+4(8)}{\sqrt{3^2+4^2}\sqrt{6^2+8^2}}
=\frac{50}{5\cdot10}=1
\]

Even though the magnitudes differ, the direction is identical. Compare \(\mathbf{x}=(1,0)\) with \((0,1)\):

\[
\cos=\frac{0}{1\cdot1}=0
\]

The documents have no shared direction in this representation. Cosine is therefore useful for term-frequency or feature-direction comparison, not for every notion of numeric closeness.

### Example 7: Jaccard similarity

Two users have binary preferences for five items:

```text
item       1 2 3 4 5
user A     1 1 0 0 0
user B     1 0 1 0 0
```

Counts are \(a=1\) (both have item 1), \(b=1\) (only A has item 2), \(c=1\) (only B has item 3), and joint zeros \(d=2\).

\[
J=\frac{1}{1+1+1}=\frac{1}{3}\approx0.333
\]

They share one of the three items either selected. Jaccard ignores the two joint absences; matching similarity would include them and give \((1+2)/5=0.6\).

### Example 8: A mixed-distance pipeline

A patient record contains:

- age (ratio);
- systolic blood pressure (ratio);
- region (nominal);
- risk level (ordinal).

A practical pipeline is:

1. normalize or standardize the numeric variables;
2. compute weighted numeric Euclidean distance;
3. compute normalized mismatch for region;
4. compute rank-based distance for risk level;
5. combine components with documented weights.

This is more meaningful than applying one raw distance to all four fields. The final score is still a model choice and should be tested against the intended task.

## Key terms & formulas

- **Similarity:** a score indicating how alike two objects are.
- **Dissimilarity or distance:** a score indicating how different two objects are.
- **Data vector:** an object represented by one coordinate per attribute.
- **Euclidean distance:** \(d_2=\sqrt{\sum_j(x_j-y_j)^2}\).
- **Manhattan distance:** \(d_1=\sum_j|x_j-y_j|\).
- **Chebyshev distance:** \(d_\infty=\max_j|x_j-y_j|\).
- **Minkowski distance:** \(d_p=(\sum_j|x_j-y_j|^p)^{1/p}\).
- **Weighted distance:** a distance in which selected attributes have larger coefficients.
- **Min-max normalization:** \(x'=(x-\min)/(\max-\min)\).
- **Z-score standardization:** \(z=(x-\mu)/\sigma\).
- **Nominal mismatch:** \(0\) for equal categories and \(1\) for different categories.
- **Ordinal rank distance:** normalized difference between ordered ranks.
- **Cosine similarity:** \(\frac{\mathbf{x}\cdot\mathbf{y}}{\|\mathbf{x}\|\|\mathbf{y}\|}\).
- **Cosine distance:** \(1-\) cosine similarity.
- **Jaccard similarity:** \(\frac{a}{a+b+c}\) for binary objects.
- **Matching similarity:** \(\frac{a+d}{a+b+c+d}\).
- **Correlation distance:** \(1-r\) when a shape-based distance is wanted.
- **Metric identity:** zero distance for identical points and positive distance for different points.
- **Triangle inequality:** \(d(x,z)\le d(x,y)+d(y,z)\).
- **Scale dependence:** the fact that distances change when attributes are measured on different scales.

## Common mistakes

1. **Using Euclidean distance on raw nominal codes.** Numeric codes are arbitrary and have no geometric meaning.
2. **Forgetting to scale numeric attributes.** A large-range variable can dominate the distance.
3. **Mixing units within one calculation.** Convert units and record the conversion.
4. **Using cosine similarity for a zero vector.** Its denominator is zero, so define a special policy.
5. **Treating cosine similarity as magnitude distance.** Cosine ignores overall magnitude.
6. **Ignoring joint zeros in binary data.** Jaccard and matching similarity answer different questions.
7. **Assuming a weighted distance is objective.** Weights encode domain priorities and must be justified.
8. **Calculating a distance using test-set scaling parameters.** This leaks information and makes evaluation optimistic.
9. **Confusing similarity direction.** A larger similarity usually means closer, while a larger distance means farther.
10. **Assuming every dissimilarity is a metric.** Thresholded or matching-based measures may violate the triangle inequality.
11. **Comparing an ordinal rank as if its gaps are equal.** The rank conversion is an assumption.
12. **Ignoring zero values in a document-term vector.** Whether a zero means absence or missing data changes the measure.

## Exam prep

### Likely 2-mark questions

1. **Differentiate similarity and dissimilarity.**  
   *Hint:* Similarity is larger for more alike objects; dissimilarity or distance is larger for more different objects.

2. **Write the Euclidean distance formula.**  
   *Hint:* \(d_2=\sqrt{\sum_j(x_j-y_j)^2}\).

3. **When is Manhattan distance used?**  
   *Hint:* For numerical data where absolute coordinate differences are summed, often for an \(L_1\) geometry or robust linear differences.

4. **Why is scaling needed before distance calculation?**  
   *Hint:* Attributes with larger numeric ranges can otherwise dominate; scaling makes the intended contributions comparable.

5. **Give the min-max normalization formula.**  
   *Hint:* \(x'=(x-\min)/(\max-\min)\).

6. **What is cosine similarity used for?**  
   *Hint:* Comparing vector direction, especially text term-frequency or feature vectors; it is not sensitive to overall magnitude.

7. **Define Jaccard similarity.**  
   *Hint:* For binary data, \(a/(a+b+c)\), counting shared 1s over the union of 1s.

8. **What type of distance suits nominal attributes?**  
   *Hint:* A mismatch count or proportion, possibly with weights or a category-distance matrix.

### Likely long-answer questions

1. **Explain the main numerical dissimilarity measures and compare them.**  
   *Answer hint:* Give Euclidean, Manhattan, Chebyshev, and Minkowski formulas; use the same two points; interpret \(p\) and discuss sensitivity to scale, outliers, and geometry.

2. **Explain how attribute type affects similarity measurement.**  
   *Answer hint:* Compare nominal mismatch, ordinal rank distance, interval/ratio numerical distance, temporal and spatial considerations, and why a single universal measure is unsafe.

3. **Explain min-max normalization, z-score standardization, and weighted distance with an example.**  
   *Answer hint:* Calculate both scaling methods on a small dataset, show how the distance changes, explain training-data leakage, and discuss when each representation is preferable.

4. **Explain cosine and Jaccard similarity for different data representations.**  
   *Answer hint:* Derive or state the formulas, calculate a numerical example, discuss zero vectors and joint zeros, and connect each measure to text or binary-item data.

5. **Design a mixed-data similarity measure for a real dataset.**  
   *Answer hint:* State the object and attributes, choose a component measure for each type, scale numeric features, assign defensible weights, discuss properties, and evaluate the result on a real task.
