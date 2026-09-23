---
subject: ml
unit: 1
topic: unsupervised-learning-basics
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Unsupervised Learning Basics

## Overview

Unsupervised learning works with observations that do not come with a target answer. The goal is to discover useful structure such as groups, low-dimensional patterns, relationships among attributes, or unusual records. It is useful when labels are expensive, unavailable, or not the main question at the beginning of an analysis.

Unlike supervised learning, an unsupervised method does not receive the sentence “this customer is in group A.” It receives records and an objective, such as making nearby records similar, separating groups, reconstructing observations, or finding rules that occur often. The resulting structure still needs interpretation and validation.

## Explanation

### Definition and setting

For unlabelled data

\[
D=\{x_1,x_2,\ldots,x_n\},
\]

an unsupervised algorithm seeks a representation, partition, density estimate, or rule set that captures a chosen notion of structure. There is no universally correct structure: the result depends on features, preprocessing, distance or similarity, algorithm assumptions, and the objective.

The word **unlabelled** does not mean that the data has no useful information. It means no target values were supplied for the learning objective. Later an expert may label a sample, discover a business meaning, or use the result as features in a supervised model.

### Main tasks

1. **Clustering:** partition observations into groups of similar points. Examples include customer segments, document groups, image grouping, and anomaly detection.
2. **Dimensionality reduction:** compress many variables into fewer informative components while preserving structure. PCA is a linear example; autoencoders are neural examples.
3. **Density estimation:** estimate a probability distribution \(p(x)\), useful for anomaly detection and generation.
4. **Association-rule mining:** find items or events that occur together, measured by support and confidence.
5. **Latent-factor analysis:** identify hidden factors that explain observed variables, such as customer preferences.
6. **Graph or community discovery:** infer connected groups in relationships.

### How clustering works at a high level

A clustering algorithm optimises a criterion such as within-cluster distance, separation, density, or graph connectivity. A common intuition for k-means is:

1. Choose \(k\) initial centroids.
2. Assign each point to its nearest centroid.
3. Recompute each centroid as the mean of assigned points.
4. Repeat until assignments stabilise or the objective changes little.

The result is a partition, not a universal truth. Scale dominates Euclidean distance, outliers can create tiny clusters, and a spherical-cluster assumption may fail for elongated or nested groups.

### Choosing a representation

Unsupervised learning is highly sensitive to representation. A monetary value of 1,000 and an age of 1,000 have radically different meanings, yet unscaled Euclidean distance treats their numerical differences alike. Standardisation or robust scaling may be needed. One-hot encoding can make categories distant; dimensionality reduction can remove noise but also discard useful rare information.

Feature selection should be guided by the question. For customer segmentation, spending frequency and average basket size may be useful; an arbitrary customer ID is not. For text clustering, raw counts can be dominated by common words, so normalisation or TF–IDF is often useful.

### Evaluating unsupervised results

There are three broad forms of evaluation:

- **Internal metrics:** measure compactness or separation, such as inertia, silhouette score, Davies–Bouldin index, or Calinski–Harabasz score. They are useful for comparison but not proof of usefulness.
- **External metrics:** compare assignments with labels held out or discovered later, using adjusted Rand index, normalised mutual information, or purity.
- **Stability and domain validation:** rerun with resampling or changed initialisation, and ask whether the groups are actionable, distinct, and stable over time.

A good cluster is not necessarily the one with the highest silhouette. It must make sense at the time of prediction and support the intended decision.

### Applications and limitations

Applications include market segmentation, document organisation, image compression, anomaly detection, network analysis, exploratory data analysis, and feature generation. Limitations include subjective meaning, sensitivity to scaling and initialisation, difficulty choosing the number of clusters, high computational cost, and accidental discovery of sensitive groupings. Privacy and fairness are important: clustering can expose or reinforce social patterns even without labels.

Unsupervised learning is often a first step. A business may use it to form segments and later train a supervised churn model for each segment. A semi-supervised method can use a few labels to make the clusters more useful.

## Worked examples

### Example 1: customer grouping

Suppose each customer has average monthly spend and number of orders. A manager wants to see whether customers form distinct groups. Plotting or clustering the two standardised variables may reveal “low frequency/low spend,” “high frequency/high spend,” and “high spend/low frequency.” The names are interpretations, not facts supplied by the algorithm.

### Example 2: anomaly detection

A server normally records about 100 requests per minute. A record with 20,000 requests is unusual. A density or distance-based method can flag it for investigation. It is not automatically an attack: a marketing event or a batch job could explain the spike.

### Example 3: association rules

In a shop, 1,000 transactions contain bread and butter together in 300. If 600 transactions contain bread, support is 0.3; if 800 contain butter, confidence \(P(\text{butter}\mid\text{bread})\) is \(300/800=0.375\). A rule may be useful for promotion but does not prove that bread causes buying butter.

### Example 4: projection

A researcher has 100 temperature, humidity, pressure, and noise measurements. PCA can transform them into two components retaining most of the variation. A plot may show a seasonal cycle. The components are linear combinations, so explaining them requires care.

## Key terms & formulas

- **Unlabelled data:** observations without a target for the chosen task.
- **Cluster:** a set of observations considered similar.
- **Centroid:** a representative point, often a cluster mean.
- **Distance:** a measure used to decide similarity; Euclidean distance is
  \[
  d(x,z)=\sqrt{\sum_{j=1}^{d}(x_j-z_j)^2}.
  \]
- **Inertia (within-cluster sum of squares):**
  \[
  \sum_{k=1}^{K}\sum_{x\in C_k}\|x-\mu_k\|^2.
  \]
- **Silhouette score:** combines within-cluster cohesion and separation; values are generally between \(-1\) and \(1\), with higher values preferred.
- **PCA:** an orthogonal linear projection using leading eigenvectors of the covariance matrix.
- **Support:** frequency of an item or rule's antecedent and consequent together.
- **Confidence:** conditional frequency of the consequent given the antecedent.
- **Density:** how concentrated observations are in a region.
- **Stability:** consistency of structure under resampling or perturbation.
- **Latent factor:** an unobserved construct inferred from observed variables.

## Common mistakes

1. **Saying unsupervised learning has no objective.** It optimises a structural or probabilistic objective.
2. **Trusting a plot before preprocessing.** Scaling, missing values, and outliers can change the structure.
3. **Choosing \(k\) only because it is easy to plot.** Use domain needs, stability, and internal/external evidence.
4. **Calling clusters classes.** A cluster is not automatically a meaningful label.
5. **Using a high silhouette score as the only proof.** The metric can favour the geometry assumed by the algorithm.
6. **Interpreting association as causation.** Both association rules and cluster patterns are observational unless an experiment supports causality.
7. **Ignoring privacy and fairness.** Hidden groups can still affect people and decisions.

## Exam prep

### Likely 2-mark questions

- **Define unsupervised learning.** Learning useful structure from unlabelled data.
- **Name two unsupervised tasks.** Clustering and dimensionality reduction.
- **What does a cluster represent?** A group similar under a chosen feature representation and distance/similarity measure.
- **Why is scaling important?** To prevent large-magnitude features dominating the similarity calculation.

### Long-answer prompts

- **Explain unsupervised learning and its main tasks.** Compare clustering, dimensionality reduction, density estimation, and association rules with examples.
- **Describe the k-means algorithm.** Include initialisation, assignment, update, stopping, and limitations; include the objective and one worked step.
- **How can clustering results be evaluated?** Discuss internal, external, stability, and domain validation; explain why no single metric is sufficient.
- **Compare supervised and unsupervised learning.** Cover labels, objectives, evaluation, interpretability, and failure modes.
