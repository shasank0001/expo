---
subject: ml
unit: 4
topic: unsupervised-learning-introduction
syllabus_ref: CSM3201 Unit-IV
status: draft
---
# Unsupervised Learning: An Introduction

## Overview

Unsupervised learning finds structure in data that does not include target labels. It can group similar observations, reduce many variables to a smaller representation, estimate a probability density, detect unusual records, or discover items/events that occur together. The structure is not automatically “true”; it depends on the representation, similarity, objective, and domain interpretation.

Unsupervised learning is useful at the beginning of exploration, when labels are scarce, or when the analyst wants to ask what distinctions exist in the data. It is also useful as preparation for a supervised model. Its central challenge is deciding whether a discovered pattern is stable, meaningful, and safe to use.

## Explanation

### Learning setting

Given unlabelled observations

\[
D=\{x_1,x_2,\ldots,x_n\},
\]

an algorithm seeks a structure \(S\) that optimises an objective. Possible structures include a partition into clusters, a low-dimensional embedding, a density \(p(x)\), or a set of rules. There is no target \(y\) against which to directly compare the result.

The word unlabelled does not mean that the data are meaningless. It means the learning task has no supplied answers. A human may later label a representative sample, or domain experts may interpret the output.

### Major forms

1. **Clustering:** partition observations into groups of similar points.
2. **Dimensionality reduction:** represent high-dimensional data with fewer variables while retaining useful variation.
3. **Density estimation:** model the distribution \(p(x)\) to support likelihood, generation, or anomaly detection.
4. **Association-rule mining:** find sets of items or events that frequently co-occur.
5. **Latent-factor analysis:** infer hidden factors such as customer preferences or economic conditions.
6. **Graph/community analysis:** find connected groups in relational data.

### Why structure is useful

Clusters can support customer segmentation, document organisation, image grouping, experiment design, and anomaly triage. Reduced dimensions can support visualisation and efficient prediction. Association rules can inform shelf placement or event analysis. Latent factors can make noisy questionnaires more interpretable. The value comes from a subsequent decision, not from the algorithm's name.

### Representation and similarity

Most methods need a distance or similarity. For numerical vectors, Euclidean distance is

\[
d(x,z)=\sqrt{\sum_{j=1}^{p}(x_j-z_j)^2}.
\]

Manhattan distance sums absolute differences, and cosine similarity measures directional alignment, often used for text. Scaling matters: a feature with a large range can dominate Euclidean distance. Categorical variables need a meaningful dissimilarity, such as mismatch or a learned metric. Missingness can itself be represented.

### Objectives and assumptions

A clustering objective might minimise within-cluster distance, maximise separation, model density, or optimise a graph cut. Different objectives can produce different answers on the same data. K-means assumes roughly spherical clusters and is sensitive to outliers; hierarchical clustering depends strongly on linkage; DBSCAN assumes density-connected regions; Gaussian mixtures assume a probabilistic mixture. State the assumptions before interpreting the output.

### Unsupervised versus self-supervised learning

Unsupervised learning has no task target. Self-supervised learning creates a target from the data—for example, predicting a masked token or reconstructing an image. The latter has a prediction loss like supervised learning, but the labels are generated automatically. Both are distinct from ordinary clustering.

### Evaluation and interpretation

Because there is no true answer, evaluation uses internal measures, external labels when available, stability, and domain validation. A high silhouette score means points are relatively well separated under the chosen distance, not that a cluster corresponds to a real customer need. Inspect cluster centres, representative examples, sizes, feature distributions, and changes over time.

### Applications and risks

Unsupervised methods can expose hidden segments and anomalies, but they can also create sensitive profiles or reinforce historical inequity. Clusters may correspond to protected characteristics or proxy variables. An anomaly may be a data error rather than a rare meaningful event. Results need governance, privacy controls, and a human interpretation step.

## Worked examples

### Example 1: customer structure

A retailer has purchase frequency, average basket value, and returns rate but no customer type. Clustering standardised features may reveal groups such as frequent low-return customers and occasional high-return customers. The names and actions are business interpretations, not labels supplied by the algorithm.

### Example 2: document exploration

A library has 10,000 abstracts. TF–IDF vectors and cosine similarity can group articles by vocabulary. A topic model may estimate hidden topics. Researchers inspect representative documents and check whether the groups remain stable on a later sample.

### Example 3: anomaly triage

Network records normally have 50–100 requests per minute. A 20,000-request record is an anomaly. It may be an attack, a scheduled job, or a broken sensor. The algorithm prioritises review; it does not determine guilt.

### Example 4: hidden factor

Questionnaire items about commuting, office size, and work location may be explained by one latent factor “traditional office dependence.” Factor analysis can suggest a compact representation, but its interpretation and rotation require domain judgement.

## Key terms & formulas

- **Unsupervised learning:** learning structure without target labels.
- **Unlabelled data:** observations without a task target.
- **Clustering:** grouping similar observations.
- **Dimensionality reduction:** representing data in fewer dimensions.
- **Density estimation:** learning a probability distribution \(p(x)\).
- **Distance:** \(d(x,z)\), used to define similarity.
- **Cosine similarity:**
  \[
  \operatorname{sim}(x,z)=\frac{x^\top z}{\|x\|_2\|z\|_2}.
  \]
- **Latent factor:** unobserved construct inferred from observed variables.
- **Inductive bias:** assumptions about the preferred structure.
- **Internal validation:** metric computed without external labels.
- **Stability:** persistence of structure under perturbation or resampling.
- **Anomaly:** observation unusual under a model or reference distribution.
- **Self-supervision:** targets generated from the input itself.

## Common mistakes

1. **Saying unsupervised learning has no objective.** It optimises structure, likelihood, or reconstruction.
2. **Assuming clusters are natural facts.** They depend on features and distance.
3. **Using unscaled numeric features without thought.** Large units can dominate similarity.
4. **Confusing a cluster with a class.** A cluster has no supplied label.
5. **Judging results by one internal metric.** Domain meaning and stability matter.
6. **Ignoring privacy and fairness.** Hidden groups can still affect people.
7. **Using future information to define a grouping.** This can leak outcomes and make the analysis optimistic.

## Exam prep

### Likely 2-mark questions

- **Define unsupervised learning.** Learning useful structure from data without target labels.
- **Name three unsupervised tasks.** Clustering, dimensionality reduction, density estimation, anomaly detection, or association mining.
- **Why is scaling important?** Feature magnitude can dominate distance and similarity.
- **What is a latent factor?** An unobserved construct inferred from observed variables.

### Long-answer prompts

- **Explain the main types of unsupervised learning.** Give data, objective, example, and limitation for clustering, reduction, density, and association rules.
- **Compare supervised and unsupervised learning.** Discuss labels, feedback, objectives, metrics, and interpretation.
- **Why can a discovered cluster be invalid?** Explain representation, distance, objective, sampling, stability, and domain meaning.
- **Describe a complete unsupervised analysis.** Cover preprocessing, algorithm comparison, validation, interpretation, and governance.
