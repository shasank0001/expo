---
subject: ml
unit: 4
topic: partition-based-clustering
syllabus_ref: CSM3201 Unit-IV
status: draft
---
# Partition-Based Clustering

## Overview

Partition-based clustering divides a data set into a specified number of non-overlapping groups. Each point belongs to one cluster, and a representative such as a centroid or medoid defines the cluster. K-means is the standard example; k-medoids and fuzzy c-means are related variants.

These methods scale reasonably well and are intuitive when clusters are compact and roughly spherical. They can struggle with irregular shapes, varying density, outliers, and a large difference between cluster sizes. The result depends on initialisation and the chosen distance.

## Explanation

### K-means

K-means chooses \(K\) centroids \(\mu_1,\ldots,\mu_K\), assigns each point to the closest centroid, and recomputes centroids as means:

\[
z_i=\arg\min_k\|x_i-\mu_k\|^2,
\qquad
\mu_k=\frac{1}{|C_k|}\sum_{x_i\in C_k}x_i.
\]

It repeats assignment and update until the objective stabilises or a maximum iteration count is reached. The objective is

\[
J=\sum_{k=1}^{K}\sum_{x_i\in C_k}\|x_i-\mu_k\|^2.
\]

Use k-means++ initialisation, which selects initial centres with some distance from one another, or run several initialisations and choose the lowest inertia. Record the seed and initialisation method.

### Algorithm example

Suppose two centroids are initially at \((0,0)\) and \((10,0)\). Points at \((1,1)\) and \((9,2)\) are assigned to the nearest centres. New means become approximately \((1,1)\) and \((9,2)\). Reassignment may move a borderline point, so the process repeats. The result is local, not guaranteed globally optimal.

### Advantages

- Simple and easy to explain.
- Computationally efficient, often \(O(nKd)\) per iteration.
- Scales to moderately large numerical data.
- Produces compact clusters and useful centroids.
- Can be combined with a pipeline and repeated efficiently.

### Limitations

K-means assumes roughly spherical, similarly sized clusters and is sensitive to outliers. It is sensitive to feature scale, initial centres, and \(K\). It can split one irregular group into two or merge two nearby groups. It does not naturally model uncertainty or non-convex shapes. The Euclidean mean may be meaningless for categorical variables.

### K-medoids

K-medoids chooses actual data points as cluster representatives. The objective commonly uses within-cluster dissimilarity rather than squared distance. It is more robust to outliers and can work with arbitrary dissimilarity, such as Gower distance for mixed data, but is usually more computationally expensive. PAM or similar algorithms improve representative search.

### Fuzzy c-means

Fuzzy c-means assigns a membership \(u_{ik}\) and updates memberships and centroids under a fuzziness parameter \(m\). With \(m=1\), membership is hard; larger \(m\) makes assignments softer. It is useful when points overlap, but results depend on \(m\), initialisation, and scaling.

### Choosing K and preprocessing

Use a domain requirement, elbow of inertia, silhouette, Davies–Bouldin, Calinski–Harabasz, gap statistic, or stability. Do not select solely by the lowest computational cost. Standardise continuous features, encode categories meaningfully, remove or handle identifiers, and consider robust scaling. Missing values need a policy.

### Interpretation and validation

Summarise each cluster by centroid/medoid, size, feature distributions, representative examples, and temporal stability. Compare with a hierarchical or density method when the data may be irregular. A lower inertia for a larger \(K\) is expected, so it is not evidence by itself that \(K\) is correct.

### Applications and cautions

Partition clustering is used for customer segmentation, image colour grouping, document grouping, compression, and exploratory analysis. It can make groups that look convenient but are unstable or sensitive to a few outliers. It may create sensitive profiles. Avoid using a cluster assignment as an irreversible label without human review and a way to reassign people when behaviour changes.

### Practical choices and validation

Partition algorithms optimise a global geometry. This makes them fast and predictable, but the prediction for a new point depends on the fitted centroids or medoids. Before accepting a solution, inspect the effect of scaling, random initialisation, outliers, and \(K\). Run several initialisations and retain the best objective only as a starting point for validation; the lowest inertia is not automatically the most useful partition.

For mixed data, do not encode a category as an arbitrary integer and then take its mean. Use k-medoids with a documented dissimilarity, a suitable mixed distance, or a separate representation with a model such as k-prototypes. For high-dimensional data, dimensionality reduction can improve visualisation but may impose its own geometry; compare clustering before and after the reduction.

A useful result report includes cluster size, centroid/medoid, feature distributions, representative members, sensitivity to the seed, and a comparison with hierarchical or density methods. If one cluster is dominated by an outlier or a rare category, investigate the data rather than deleting the outlier automatically. A partition is a proposal for interpretation, not a natural identity.

## Worked examples

### Example 1: k-means calculation

Two one-dimensional points are 1 and 3, and one centroid starts at 0. Both are closer to 0, so the mean moves to 2. Reassignment may remain the same. Inertia is then \((1-2)^2+(3-2)^2=2\). Running from many starts can find a lower-inertia partition.

### Example 2: k-medoids with categories

A mixed customer record has age, income, city, and returns. A k-medoids method with a mixed-type dissimilarity can use a real customer as a representative. The resulting groups can be easier to inspect than means of one-hot vectors.

### Example 3: irregular clusters

Two crescent-shaped groups cannot be separated well by centroids because each cluster surrounds the other. A density or spectral method may be more appropriate. K-means may split the crescents into pieces with low inertia relative to its assumption.

### Example 4: selecting K

The team compares \(K=2,3,4\) across bootstrap samples. The 3-cluster solution is stable and matches operational teams, while the 2-cluster solution has a slightly better silhouette. The final choice records the stability and business evidence, not just the metric.

## Key terms & formulas

- **Partition-based clustering:** divides points into groups.
- **K-means:** centroid-based partition method.
- **Centroid:** mean of a cluster.
- **Inertia/WCSS:**
  \[
  J=\sum_{k=1}^{K}\sum_{x_i\in C_k}\|x_i-\mu_k\|^2.
  \]
- **K-means++:** distance-aware initialisation.
- **K-medoids:** partition using a representative actual observation.
- **Fuzzy c-means:** soft membership partition.
- **Hard clustering:** one cluster per observation.
- **Fuzziness parameter:** controls softness in fuzzy c-means.
- **Local optimum:** best solution found from one initialisation, not necessarily globally optimal.
- **Cluster stability:** similarity of partitions across resamples.
- **Robust scaling:** scaling using resistant centre and spread.
- **Mixed-type distance:** dissimilarity combining numerical, categorical, and binary attributes.

## Common mistakes

1. **Running k-means on unstandardised features.** Units dominate the result.
2. **Treating inertia as a direct measure of business usefulness.** It measures only compactness.
3. **Assuming the algorithm finds the global optimum.** Initialisation and local minima matter.
4. **Ignoring outliers.** Means can be pulled toward a few extreme records.
5. **Using k-means for arbitrary shapes.** A non-convex cluster may be split.
6. **Treating categorical means as meaningful.** Use k-medoids or an appropriate encoding.
7. **Not checking cluster stability or fairness.** A partition can be statistically neat but harmful.

## Exam prep

### Likely 2-mark questions

- **Define partition-based clustering.** Dividing observations into a fixed number of groups using representatives.
- **State the k-means update steps.** Assign to nearest centroid, then recompute centroids as means.
- **What is inertia?** Within-cluster sum of squared distances.
- **Give one advantage and one limitation of k-means.** Advantage: fast/simple; limitation: assumes spherical clusters and is sensitive to scale/outliers.

### Long-answer prompts

- **Explain the k-means algorithm step by step.** Include initialisation, assignment, update, stopping, objective, and complexity.
- **Compare k-means and k-medoids.** Discuss representatives, outliers, distance, interpretability, and mixed data.
- **Why can k-means fail on real data?** Discuss scale, shape, density, outliers, \(K\), and initialisation.
- **How would you validate a partition-based clustering result?** Use baseline comparisons, internal metrics, stability, profiles, and domain tests.
