---
subject: ml
unit: 4
topic: evaluating-clustering-results
syllabus_ref: CSM3201 Unit-IV
status: draft
---
# Evaluating Clustering Results

## Overview

Clustering has no universally correct answer, so evaluation must combine mathematical criteria, stability, external evidence, and domain usefulness. A result can have a good internal score and still be unstable, unfair, or impossible to use. Conversely, a mathematically modest grouping may be valuable if it corresponds to a repeatable operational distinction.

Evaluation asks several separate questions: Are points compact or separated under the chosen metric? Does the structure persist under resampling? Does it agree with trusted labels or known patterns? Can people describe and act on the groups? Is the analysis safe and privacy-preserving?

## Explanation

### Internal measures

Internal metrics use the data and the cluster assignments without external labels.

**Inertia/WCSS** for k-means:

\[
J=\sum_{k=1}^{K}\sum_{x_i\in C_k}\|x_i-\mu_k\|^2.
\]

Lower inertia is better for a fixed \(K\), but it generally decreases as \(K\) grows, so it cannot choose \(K\) alone.

**Silhouette score** for point \(i\):

\[
s(i)=\frac{b(i)-a(i)}{\max(a(i),b(i))},
\]

where \(a(i)\) is mean distance to its own cluster and \(b(i)\) is the smallest mean distance to another cluster. It ranges from \(-1\) to \(1\) under common conventions; higher is better. It can fail for non-convex clusters or unusual densities.

**Davies–Bouldin index** is the average ratio of within-cluster scatter to between-centroid separation; lower is better. **Calinski–Harabasz** compares between-cluster to within-cluster variation; higher is often preferred. **Gap statistic** compares observed within-cluster variation with a reference distribution.

No metric is universally correct because each encodes geometric assumptions. A metric should be reported with the distance, preprocessing, \(K\), and algorithm.

### External measures

If trusted labels or a reference partition \(C^*\) exists, compare assignments with it:

- **Adjusted Rand index (ARI):** corrects for chance agreement; 1 is perfect and 0 is chance-level.
- **Normalised mutual information (NMI):** measures shared information between partitions, scaled to [0,1] in common variants.
- **Purity:** each predicted cluster is assigned its majority true class, then the weighted purity is calculated; it can be misleading with many clusters.
- **Homogeneity, completeness, and V-measure:** compare whether clusters contain one class and whether one cluster contains one class.

External labels may themselves be imperfect or describe a different task, so agreement is evidence, not truth.

### Stability and reproducibility

Rerun the algorithm on bootstrap or subsampled data, with perturbed features, or with different random seeds. Measure how often pairs of observations remain together, or compare adjusted Rand/ normalised mutual information between runs. Stable groups are more likely to reflect persistent structure. Stability can fail because the algorithm is unstable even when the data contain a clear pattern, so combine it with other evidence.

### Interpretability and usefulness

For each cluster, report:

- number of observations and feature distributions;
- centroid/medoid or representative examples;
- missingness and data-quality differences;
- temporal and subgroup composition;
- a plain-language description;
- intended action and expected benefit.

A cluster that contains many different profiles or cannot be described without vague labels may not be actionable. A useful business cluster should persist long enough to support a decision and have a process for reassignment.

### Clustering validity and uncertainty

Cluster membership can change with a new record, a new feature, or a new model version. For probabilistic models, report membership or posterior uncertainty. For hard methods, use sensitivity analysis and abstention for borderline points. A point close to a boundary should not trigger a high-impact action without review.

### Bias, privacy, and fairness

Even without labels, clusters may correlate with protected characteristics or proxies. Compare group representation, feature distributions, and the consequences of assigning people to segments. Do not use a cluster as a proxy for a sensitive attribute without a lawful and ethical basis. Limit access to profiles, document purposes, and allow correction or deletion.

### A validation report

A complete report includes:

1. data source, sample, representation, and distance;
2. algorithms and parameters, including initialisation;
3. \(K\) or cut/density rules;
4. internal and external metrics;
5. stability under resampling and time;
6. cluster profiles and representative examples;
7. sensitivity to preprocessing and feature changes;
8. intended use, privacy/fairness review, and monitoring plan.

### Validation in a changing environment

A clustering result should be tested on a later time period or an independent sample whenever possible. Compare the distribution of cluster sizes, feature profiles, and assignment stability. A solution that works only on the data used to discover it may be an artefact of sampling or preprocessing. If the application must assign new customers or devices, define how drift is detected and when a cluster is frozen, recalibrated, or retired.

Quantitative metrics should be accompanied by a decision test. For customer segmentation, conduct a controlled campaign or measure whether a cluster-specific policy improves an outcome without unacceptable harm. For anomaly detection, measure the proportion of true incidents reviewed and the false-alarm burden. For scientific grouping, seek independent replication. No internal score can replace this consequence or evidence check.

The report should also disclose failed or sensitive analyses. A group that is highly predictive of a protected attribute may need to be removed, even if it improves an internal metric. Transparent documentation allows a reviewer to challenge the representation, threshold, algorithm, and intended use.

## Worked examples

### Example 1: silhouette versus domain usefulness

Two clusters have a silhouette of 0.55, while three clusters have 0.48. The two-cluster solution produces a broad “customers” group that cannot support different service policies. The three-cluster profiles match operational teams. The report presents both scores and the business evidence; it does not declare the higher silhouette automatically best.

### Example 2: ARI with known labels

Researchers have held-out topic labels. A clustering solution has ARI 0.62, showing substantial but imperfect agreement. They inspect clusters that mix two topics and improve the text representation or use supervised refinement. They report that the external labels are not perfect.

### Example 3: stability

Bootstrap resampling produces pairwise assignments with ARI 0.80 for one grouping and 0.30 for another. The first is more stable, but if the algorithm is known to be sensitive to outliers, the team also tests a density method and profiles the groups. Stability is evidence, not proof.

### Example 4: privacy

Customer clusters include a group that almost perfectly identifies a small neighbourhood or protected group. The business purpose does not require that inference. The team removes the sensitive proxy, restricts access, and documents that clusters are not identities.

## Key terms & formulas

- **Internal validation:** metric from the clustering data and assignments.
- **External validation:** comparison with trusted labels or reference structure.
- **Silhouette:** \(s(i)=(b(i)-a(i))/\max(a(i),b(i))\).
- **Inertia/WCSS:** within-cluster squared error.
- **Adjusted Rand index:** chance-corrected agreement between partitions.
- **Purity:** majority-class proportion of each predicted cluster.
- **Stability:** consistency under resampling, perturbation, or new data.
- **Cluster profile:** feature summary of a group.
- **Membership uncertainty:** probability or degree that a point belongs to a group.
- **Sensitivity analysis:** change in results under plausible preprocessing/parameter choices.
- **Fairness:** equitable treatment and outcome across groups.
- **Domain validity:** usefulness in the real decision context.

## Common mistakes

1. **Choosing the method with the best silhouette only.** Metrics encode assumptions and can be gamed.
2. **Using external labels without questioning their quality.** Labels may be noisy or irrelevant.
3. **Ignoring stability.** A result that changes with every sample is weak evidence.
4. **Interpreting a cluster name as a fact.** It is an interpretation of a representation.
5. **Failing to inspect profiles.** A high score can hide a meaningless or harmful group.
6. **Ignoring privacy and sensitive proxies.** Unlabelled does not mean anonymous.
7. **Not comparing with a baseline.** Always compare simple methods and alternative representations.

## Exam prep

### Likely 2-mark questions

- **Name two internal clustering metrics.** Silhouette, Davies–Bouldin, Calinski–Harabasz, inertia, or gap statistic.
- **What is the silhouette score?** A cohesion/separation measure for each point and its cluster.
- **What is ARI?** A chance-corrected measure of agreement between two partitions.
- **Why test cluster stability?** To see whether structure persists under resampling or perturbation.

### Long-answer prompts

- **Explain how clustering results can be evaluated.** Cover internal, external, stability, interpretability, and domain evidence.
- **Compare silhouette, ARI, and NMI.** State what each measures, its assumptions, and when external labels are available.
- **Design an evaluation plan for customer clustering.** Include data, scaling, algorithm comparison, profiles, stability, fairness, privacy, and monitoring.
- **Why is no clustering metric universally correct?** Discuss geometry, density, representation, \(K\), and purpose.
