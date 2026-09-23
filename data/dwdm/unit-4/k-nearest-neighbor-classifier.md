---
subject: dwdm
unit: 4
topic: k-nearest-neighbor-classifier
syllabus_ref: CSM3101 Unit-IV
status: draft
---
# k-Nearest Neighbor Classifier

## Overview

A k-nearest neighbor (k-NN) classifier predicts an object by looking at the \(k\) training objects closest to it. It stores the training data rather than learning a compact parameter model, so it is often called a **lazy learner**. k-NN is simple, can model nonlinear boundaries, and works well when examples are dense and features are scaled consistently. Its main challenges are choosing \(k\), measuring distance, controlling computation, and avoiding the curse of dimensionality.

## Explanation

### 1. Prediction rule

For a new object \(x\), compute its distance to every labeled training object, sort the distances, take the \(k\) closest, and assign:

- the majority class for ordinary k-NN;
- a distance-weighted vote for weighted k-NN;
- a numeric average or local model for k-NN regression.

A tie requires a declared policy: majority class, distance weighting, or a random tie-break. The prediction is local and can be explained by listing the neighbors.

### 2. Distance measures

For numeric vectors, Euclidean distance is

\[
d(\mathbf{x},\mathbf{y})=
\sqrt{\sum_j(x_j-y_j)^2}.
\]

Manhattan distance is

\[
d_1(\mathbf{x},\mathbf{y})=\sum_j|x_j-y_j|.
\]

Minkowski distance is

\[
d_p=(\sum_j|x_j-y_j|^p)^{1/p}.
\]

For binary vectors, the number of positions in which they differ gives Hamming distance; the Jaccard similarity compares intersecting and union features. For text, cosine or TF–IDF-based distance may be more appropriate. The measure must reflect the feature type and the application.

### 3. Feature scaling

Distance-based methods are affected by units. If age ranges from 20 to 70 and income from 20,000 to 200,000, raw Euclidean distance is dominated by income. Standardize or normalize each feature using training-set statistics. The transformation parameters must be fitted only on training data and then applied unchanged to validation and test data.

### 4. Choosing \(k\)

A very small \(k\) follows local noise and has high variance. A very large \(k\) approaches a global majority and has high bias. Try odd \(k\) for binary classification to reduce ties, but oddness is not a universal rule. Select \(k\) by cross-validation using the same metric as deployment. A value that works for two numeric features may not work for fifty.

### 5. Distance weighting

Instead of counting votes equally, use

\[
w_i=\frac{1}{d(x,x_i)}
\]

or \(w_i=1/d(x,x_i)^2\), avoiding zero distance. The predicted score for class \(C\) is \(\sum_{i:y_i=C}w_i\), and the class with the largest score wins. Weighting can help a very close neighbor dominate, but it can also make noise highly influential.

### 6. Efficiency and indexing

Brute-force k-NN compares the query with all \(n\) training points, costing \(O(nd)\) before sorting/searching. Trees, grid indexes, hashing, locality-sensitive hashing, and approximate nearest-neighbor methods can reduce query time, at the cost of memory, build time, or exactness. Standardization and dimensionality reduction must be validated because they can change neighborhoods.

### 7. Missing values and categorical data

A missing feature can make Euclidean distance undefined. Strategies include omitting that feature in the distance, imputing from training data, adding a missingness indicator, or using a distance suited to the data. One-hot encoding may make nominal categories sparse; domain-aware dissimilarity can be better. Imputation should be considered part of the model.

### 8. Strengths and limitations

**Strengths:** simple, nonparametric, naturally nonlinear, little model training, and easy local explanations.

**Limitations:** prediction is costly, sensitive to scaling and irrelevant features, affected by outliers, and prone to the curse of dimensionality. It does not naturally model causal relationships. Class imbalance and class probabilities need careful distance and voting rules.

## Worked examples

### Example 1: k=3 vote

Training points:

| Point | \(x_1\) | \(x_2\) | Class |
|---|---:|---:|---|
| A | 1 | 1 | A |
| B | 2 | 2 | A |
| C | 8 | 8 | B |
| D | 9 | 9 | B |

Query \(q=(2.1,2.1)\). Distances: \(d(q,A)\approx1.56\), \(d(q,B)\approx0.14\), \(d(q,C)\approx8.34\), and \(d(q,D)\approx9.76\). The three nearest are B, A, C: two A and one B. Predict A. If k=4, the vote is tied, so the chosen tie policy matters.

### Example 2: Scaling changes neighbors

Suppose height is in centimeters and weight in kilograms. Two records differ by 1 cm and 10 kg; a raw scale would treat the weight difference as more important if its numeric magnitude is larger. Standardizing each feature using its training mean and standard deviation makes the comparison based on relative variation rather than units.

### Example 3: Weighted vote

If the nearest neighbors have distances 1, 2, and 3 and classes A, A, B, equal voting predicts A. With inverse-distance weights, scores are

\[
A:1+0.5=1.5,\qquad B:1/3=0.333,
\]

still A, but the margin is much larger. If the only A neighbor is at distance 0.1 and both B neighbors are at 0.2, weighted voting can still favor A; this may be desirable or may amplify an outlier, so validate it.

### Example 4: Confusion matrix for a medical use

A screening k-NN model produces TP=18, FP=2, FN=2, TN=78. Recall is \(18/20=90\%\), specificity is \(78/80=97.5\%\), and precision is \(18/20=90\%\). Accuracy is 96% because the negative class is larger. These values show the local prediction and its operational trade-off.

## Key terms & formulas

- **k-NN:** classify using the \(k\) closest labeled objects.
- **Lazy learner:** postpones computation until prediction.
- **Euclidean distance:** square root of squared feature differences.
- **Manhattan distance:** sum of absolute differences.
- **Minkowski distance:** generalized \(L_p\) distance.
- **Distance-weighted vote:** weight neighbors by \(1/d\) or similar.
- **k selection:** choose neighborhood size by validation.
- **Curse of dimensionality:** distances become less discriminative in high dimensions.
- **Brute-force complexity:** approximately \(O(nd)\) distance work.
- **Local explanation:** the neighbor list supporting a prediction.

## Common mistakes

1. **Not scaling features:** one large unit dominates distance.
2. **Choosing \(k\) from training accuracy alone:** use validation or cross-validation.
3. **Ignoring ties:** state a deterministic policy.
4. **Using a distance on categorical or missing values without a definition:** choose an appropriate measure.
5. **Assuming k-NN learns during training:** it mostly stores data and searches at query time.
6. **Forgetting irrelevant features:** every feature affects Euclidean distance.
7. **Reporting only accuracy in imbalanced data:** inspect class-specific results.

## Exam prep

**Likely 2-mark questions**
1. Define a k-nearest neighbor classifier. *Hint: classify from the majority or weighted vote of \(k\) closest examples.*
2. State Euclidean and Manhattan distance. *Hint: square root of squared differences; sum of absolute differences.*
3. Why normalize attributes for k-NN? *Hint: otherwise units with larger numerical scale dominate distance.*

**Likely long-answer questions**
1. Work a k-NN classification from a supplied table. *Hint: compute every distance, sort neighbors, vote, and handle ties.*
2. Compare unweighted and distance-weighted k-NN. *Hint: equal votes versus inverse-distance contributions.*
3. Discuss advantages and limitations of k-NN, including the curse of dimensionality. *Hint: simple/nonlinear versus cost, scaling, outliers, and sparse neighborhoods.*
