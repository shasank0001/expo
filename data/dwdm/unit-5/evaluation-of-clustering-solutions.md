---
subject: dwdm
unit: 5
topic: evaluation-of-clustering-solutions
syllabus_ref: CSM3101 Unit-V
status: draft
---
# Evaluation of Clustering Solutions

## Overview

There is no universal ground truth for an unsupervised clustering. Evaluation asks several different questions: Is the solution compact and separated, is it stable under resampling, does it agree with known labels, and is it useful to the application? A high score for one criterion can coexist with a poor answer for another. A good evaluation therefore uses multiple measures and states the purpose of the clusters.

## Explanation

### 1. Internal validation

Internal measures use only the data and the produced clusters.

For K-means, the within-cluster sum of squares

\[
\mathrm{SSE}(k)=\sum_{r=1}^{k}\sum_{x\in C_r}\|x-\mu_r\|^2
\]

usually decreases as \(k\) grows. It is useful for comparing runs with the same data and objective, not by itself for choosing the final \(k\).

The **Calinski–Harabasz index** is

\[
CH(k)=\frac{(n-k)\mathrm{SSE}(1)}{(k-1)\mathrm{SSE}(k)}.
\]

Larger values favor more separation relative to within-cluster error, with the usual assumptions about numeric data.

The **Davies–Bouldin index** uses each cluster's scatter and separation; smaller values are generally preferred:

\[
DB=\frac1k\sum_{r=1}^{k}\max_{s\ne r}
\frac{S(C_r)+S(C_s)}{d(\mu_r,\mu_s)}.
\]

### 2. Silhouette

For object \(i\), let

\[
a(i)=\text{mean distance to other objects in its cluster}
\]

and let

\[
b(i)=\min_{r\ne c(i)}\text{mean distance to cluster }r.
\]

The silhouette is

\[
s(i)=\frac{b(i)-a(i)}{\max(a(i),b(i))}.
\]

It ranges from -1 to 1: near +1 means well separated, near 0 means weak separation, and negative means the object may be closer to another cluster. The average silhouette can compare partitions, but it assumes that a suitable distance reflects the structure. It is not meaningful for every density or irregular-shape solution.

### 3. Cluster validity and external labels

If trusted labels are available, **external validation** compares discovered clusters with them. ARI, adjusted Rand index, NMI, purity, and Fowlkes–Mallows are common. Adjusted measures correct for agreement that could occur by chance, while purity can be inflated by a solution with too many clusters. External labels may represent one valid partition of the data, not the only useful one.

### 4. Stability

A stable solution changes little when the sample is resampled, features are perturbed, or the algorithm is rerun. Compare clusterings using ARI/NMI or a matching procedure, not just whether the number of clusters stays the same. Stability can reveal robust structure, but a stable but meaningless partition still exists.

### 5. Interpretability and usefulness

Inspect descriptive statistics and examples in each cluster. Can a person state what distinguishes the groups? Does the solution support a decision or prediction? Internal scores cannot decide whether a cluster is actionable. Domain experts can identify a data error that an objective score rewards.

### 6. Validity indices and assumptions

Many measures assume compact spherical clusters, Euclidean geometry, or independent dimensions. Silhouette and Davies–Bouldin can underrate curved groups; SSE is especially tied to K-means. A valid evaluation plan matches the method to the assumed cluster shape. Report the preprocessing, distance, parameters, random seeds, and uncertainty.

### 7. Comparing algorithms

Use the same data representation and meaningful metrics. Compare multiple initializations and parameters, not a single lucky run. For a target task, evaluate downstream performance such as prediction, compression, or intervention response. A higher SSE or silhouette is not a universal ranking.

## Worked examples

### Example 1: Silhouette calculation

For one object, \(a(i)=2\) and nearest-other-cluster distance \(b(i)=5\):

\[
s(i)=\frac{5-2}{\max(2,5)}=0.60.
\]

If \(a=6\) and \(b=3\),

\[
s(i)=\frac{3-6}{6}=-0.50,
\]

suggesting the object is closer to another cluster than to its own average.

### Example 2: SSE and \(k\)

For three one-dimensional points 1, 2, and 10:

- \(k=1\), mean \(13/3\), SSE \(= (−10/3)^2+(−7/3)^2+(17/3)^2=146/3\approx48.67\).
- \(k=2\), clusters \(\{1,2\}\) mean 1.5 and \(\{10\}\) mean 10, SSE \(=0.5\).
- \(k=3\), each point is a cluster, SSE \(=0\).

SSE always improves as \(k\) increases, so the zero-SSE \(k=3\) result is not automatically meaningful. Use domain constraints and external or stability evidence.

### Example 3: Purity with too many clusters

With true labels A and B, a clustering that puts every point in a separate cluster has purity 1.0 but no useful grouping. ARI and NMI penalize the excessive fragmentation relative to chance, while the application can reject the solution.

### Example 4: Stability

Run a clustering on 20 bootstrap samples and compare each result with a reference using ARI. ARI values 0.85–0.95 indicate stable recovery of the same partition. A mean ARI of 0.20 suggests the algorithm or parameter is unstable, even if one run has a high silhouette.

## Key terms & formulas

- **Internal validation:** uses only features and cluster assignments.
- **External validation:** compares with trusted labels.
- **SSE:** within-cluster sum of squares.
- **Calinski–Harabasz:** separation relative to within-cluster error; higher often preferred.
- **Davies–Bouldin:** scatter/separation ratio; lower often preferred.
- **Silhouette:** \((b-a)/\max(a,b)\), in \([-1,1]\).
- **ARI/NMI:** chance-adjusted external agreement.
- **Stability:** persistence under resampling or perturbation.
- **Purity:** fraction assigned to their majority true class; can favor many clusters.
- **Interpretability:** meaningful description of members.

## Common mistakes

1. **Choosing the largest \(k\) because SSE falls:** SSE always falls with more clusters.
2. **Using silhouette for a method whose geometry it assumes:** match the measure to the cluster shape.
3. **Treating purity as sufficient:** excessive clusters inflate purity.
4. **Reporting one run:** initialization and parameter sensitivity matter.
5. **Ignoring external labels when available:** they provide useful, though imperfect, evidence.
6. **Equating stability with validity:** a consistently meaningless partition can be stable.
7. **Skipping downstream utility:** a cluster can be statistically neat but useless.

## Exam prep

**Likely 2-mark questions**
1. State the silhouette coefficient. *Hint: compare within-cluster and nearest-cluster mean distances.*
2. Differentiate internal and external validation. *Hint: no labels versus known labels.*
3. Why does SSE not choose k by itself? *Hint: it decreases as k increases.*

**Likely long-answer questions**
1. Compare SSE, silhouette, Calinski–Harabasz, and Davies–Bouldin. *Hint: assumptions, formulas, direction, and geometry.*
2. Explain stability and external validation. *Hint: resampling/perturbation, ARI/NMI, and label limits.*
3. Propose a complete evaluation plan for a customer-segmentation project. *Hint: internal, external if available, stability, interpretability, utility, parameter sensitivity.*
