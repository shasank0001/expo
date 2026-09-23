---
subject: ml
unit: 4
topic: clustering-basics
syllabus_ref: CSM3201 Unit-IV
status: draft
---
# Clustering Basics

## Overview

Clustering is an unsupervised grouping of observations so that points within a group are more similar than points in different groups. It is one of the main applications of unsupervised learning. Clustering can reveal segments, simplify analysis, support visualisation, detect anomalies, or provide features for a later model.

There is no universal definition of a natural cluster. The result depends on the feature representation, distance, number of groups, algorithm, and scale. A good clustering analysis therefore combines an objective, a stability check, and domain interpretation.

## Explanation

### Representation and distance

For numerical vectors \(x,z\in\mathbb R^p\), common distances are

\[
d_2(x,z)=\sqrt{\sum_{j=1}^{p}(x_j-z_j)^2},
\qquad
d_1(x,z)=\sum_{j=1}^{p}|x_j-z_j|.
\]

Cosine similarity,

\[
\operatorname{cos}(x,z)=\frac{x^\top z}{\|x\|_2\|z\|_2},
\]

ignores magnitude and measures direction. A distance must reflect what “similar” means in the domain. Standardise variables with different units, or use a domain-specific metric. Text, images, graphs, and mixed data need representations that preserve relevant relationships.

### What makes a cluster useful

A useful cluster may be:

- **compact:** points are close within it;
- **well separated:** groups are far apart;
- **dense:** a region has consistent local density;
- **stable:** similar data produce similar assignments;
- **interpretable:** a domain expert can describe its members;
- **actionable:** a decision or intervention can differ by group.

Compactness alone can favour tiny clusters; separation alone can miss overlapping groups. The objective is a tool for thinking, not a proof of reality.

### Hard versus soft clustering

**Hard/partitioned clustering** assigns each point to one cluster, represented by a binary assignment matrix. **Fuzzy or soft clustering** assigns a membership degree \(u_{ik}\in[0,1]\), with \(\sum_k u_{ik}=1\). Soft assignments express uncertainty but can be harder to interpret. Gaussian mixture models are a common probabilistic soft-clustering approach.

### Number of clusters

The number \(K\) may be specified by a business need, chosen by an elbow in an internal objective, or supported by a validation criterion. Methods such as silhouette, Davies–Bouldin, Calinski–Harabasz, gap statistic, and stability comparisons provide evidence, not a guarantee. Too many clusters may fragment a population; too few may hide important structure.

### Main algorithm families

- **Partition-based:** k-means, k-medoids, fuzzy c-means; assign points and update representatives.
- **Hierarchical:** agglomerative or divisive; produce a tree or dendrogram.
- **Density-based:** DBSCAN, HDBSCAN, OPTICS; find regions connected by density.
- **Model-based:** Gaussian mixtures, latent-class models; assume a probabilistic distribution.
- **Spectral/graph:** use graph Laplacian or eigenvectors to find structure.
- **Subspace:** identify clusters that may appear only in a subset of features.

Each family has different assumptions about shape, density, noise, and scalability.

### Feature engineering and preprocessing

A cluster can be an artefact of scaling, missing-value indicators, or an ID. Remove identifiers, examine skew, decide how to encode categories, and avoid using features known to encode a sensitive group unless justified and governed. A rare but meaningful segment may be lost by aggressive outlier removal.

### Interpreting clusters

For each cluster, report size, centroid or medoid, feature distributions, representative examples, and uncertainty. A cluster named “high-value” is a human label. Compare profiles and check whether groups overlap. Visualise with PCA/t-SNE/UMAP while remembering that a projection can distort geometry.

### Applications and risks

Clustering supports customer segmentation, image grouping, document organisation, anomaly detection, data compression, and exploratory analysis. It can also expose sensitive groups, reinforce historical inequity, or create decisions based on unstable behaviour. Require a purpose, access controls, fairness analysis, human review, and a way to challenge an assignment.

### Choosing the number and type of clusters

There is no universal rule for \(K\). A business constraint may require exactly two operational groups, while an exploratory analysis may benefit from a range of resolutions. Use several forms of evidence:

- an elbow or gap statistic for the trade-off between fit and complexity;
- silhouette, Davies–Bouldin, or related internal measures;
- a hierarchical tree or density plot that shows natural transitions;
- stability under resampling, perturbation, and new observations;
- cluster profiles that are interpretable and useful for a decision.

A model that creates 50 tiny groups can always obtain a good fit, and a model that creates one group can always have low within-group error. Neither fact establishes useful segmentation. Report sensitivity to \(K\) and to preprocessing. A cluster that changes dramatically after removing a small number of records or after adding one feature is a fragile result.

### From exploratory clusters to a production system

A production cluster model needs more than a one-time fit. Save the scaler, distance definition, cluster representatives, and version. For a new observation, compute the same assignment rule; do not refit silently on each request. Define how a borderline point is assigned, when a cluster is retrained, and how drift is detected. If a cluster is used for an action, provide a reason and an appeal or correction path.

## Worked examples

### Example 1: k-means objective

For two centroids \(\mu_1,\mu_2\), k-means minimises

\[
J=\sum_{i=1}^{n}\sum_{k=1}^{K}
\mathbf1(z_i=k)\|x_i-\mu_k\|^2.
\]

The assignment and update steps alternate. The final \(J\) tells how compact the groups are under squared Euclidean distance, not whether the groups are useful.

### Example 2: choosing \(K\)

An analyst computes silhouette for \(K=2,\ldots,10\) and finds a high value at 4, but a domain team needs two operational segments. The final choice records both evidence and business constraints. It is not chosen only because a metric favours 4.

### Example 3: mixed data

A customer has age, income, and city. Scaling numeric values prevents age or income from dominating; city uses one-hot or a suitable dissimilarity. A Gower distance can combine numeric, categorical, and binary attributes. The chosen metric should be validated.

### Example 4: soft assignment

A point near the boundary between two Gaussian clusters receives membership 0.55 and 0.45. A hard algorithm forces one label; soft clustering communicates uncertainty. The downstream action may still need a threshold and a human review rule.

## Key terms & formulas

- **Cluster:** a group of similar observations.
- **Clustering:** partitioning or representing data by similarity.
- **Centroid:** arithmetic mean representing a cluster.
- **Medoid:** most representative or central actual observation.
- **Euclidean distance:** \(d_2(x,z)=\sqrt{\sum_j(x_j-z_j)^2}\).
- **Manhattan distance:** \(d_1(x,z)=\sum_j|x_j-z_j|\).
- **Cosine similarity:** \(x^\top z/(\|x\|\|z\|)\).
- **Within-cluster sum of squares:** compactness objective.
- **Hard assignment:** one cluster per point.
- **Soft/fuzzy membership:** probability-like degree for several clusters.
- **Elbow method:** looking for a bend in an objective-versus-\(K\) plot.
- **Silhouette score:** cohesion/separation score, generally \([-1,1]\).
- **Stability:** consistency under resampling or perturbation.
- **Cluster profile:** summary of feature distributions for a group.

## Common mistakes

1. **Using raw unstandardised features.** Scale can determine the clusters.
2. **Choosing \(K\) only by a plot.** Validate stability and domain needs.
3. **Interpreting a cluster as a natural class.** It is an algorithmic partition.
4. **Forgetting outliers and noise.** They can distort centroids or disappear as their own group.
5. **Using t-SNE as proof of cluster count.** A 2-D plot is one projection.
6. **Ignoring missing values and mixed data.** Similarity must be defined carefully.
7. **Overlooking sensitive segmentation and consent.** A statistical group can have real consequences.

## Exam prep

### Likely 2-mark questions

- **Define clustering.** Grouping observations so that within-group similarity is greater than between-group similarity under a chosen representation.
- **What is a centroid?** The mean of points assigned to a cluster.
- **Why scale features?** To prevent large-magnitude features dominating distance.
- **Name two ways to validate clusters.** Stability, internal metrics, external labels, or domain validation.

### Long-answer prompts

- **Explain the main choices in a clustering problem.** Cover representation, distance, \(K\), algorithm, objective, and interpretation.
- **Compare hard and soft clustering.** Define assignments, give an example, and discuss uncertainty and decision use.
- **Describe how you would evaluate a clustering result.** Use internal, external, stability, and domain criteria.
- **Explain the risks of unsupervised segmentation.** Discuss privacy, fairness, instability, sensitive attributes, and accountability.
