---
subject: dwdm
unit: 5
topic: cluster-analysis-basics
syllabus_ref: CSM3101 Unit-V
status: draft
---
# Cluster Analysis: Basic Concepts and Issues

## Overview

Cluster analysis groups similar objects so that objects in the same group are more alike than objects in different groups. It is an **unsupervised learning** task: the class labels are not supplied. The result depends on the features, similarity or distance measure, number of clusters, algorithm, and evaluation criterion. Clustering is useful for customer segmentation, document grouping, image organization, anomaly exploration, and simplifying data, but a cluster is not automatically a meaningful natural class.

## Explanation

### 1. Unsupervised learning

In supervised classification, a target label guides learning. In clustering, the algorithm receives objects \(x_1,\ldots,x_n\), often with attributes \(x_{ij}\), and returns a partition or hierarchy:

\[
C=\{C_1,\ldots,C_k\},\qquad \bigsqcup_{r=1}^{k}C_r=D.
\]

Each object is assigned to a cluster, with “noise” or unassigned membership allowed by some density methods. The algorithm optimizes a mathematical objective, not a universally correct interpretation.

### 2. Similarity and distance

A **similarity** is larger for more alike objects; a **dissimilarity or distance** is larger for more different objects. A clustering algorithm needs a measure appropriate to the data. Euclidean distance is common for numeric variables, Manhattan distance for robust linear differences, cosine similarity for direction, and Jaccard similarity for sets. Standardize variables before combining them.

### 3. Major clustering types

- **Partitioning:** choose \(k\), assign objects to \(k\) groups, and update representatives. K-means is the standard example.
- **Hierarchical:** create a dendrogram by merging or splitting groups. Agglomerative and divisive are the two directions.
- **Density-based:** expand connected dense regions, often identifying clusters of arbitrary shape and noise. DBSCAN is a standard example.
- **Grid-based:** divide the feature space into cells and cluster neighboring occupied cells. CLIQUE is a standard example.
- **Graph-based:** treat objects as vertices and relationships as edges, then find dense or highly connected communities.

Different families make different assumptions. A partition of \(k\) rounded groups can be appropriate for k-means, while a density method may be better for a curved cluster and an outlier label.

### 4. What makes a useful clustering

A useful solution should be:

- compact: members are close or connected;
- separated: different clusters are not trivially overlapping;
- stable: small sampling or parameter changes do not drastically alter it;
- interpretable: members share understandable characteristics;
- useful: the groups support an action or further task.

These goals can conflict. A dendrogram can make a pleasing picture while separating data too aggressively. High-dimensional clusters can have high internal cohesion but no useful business meaning. A method's objective is not a complete validation of the clusters.

### 5. Clustering workflow

1. Define the unit of analysis and the purpose.
2. Select relevant attributes and clean missing/invalid values.
3. Normalize or transform the attributes.
4. Choose a distance or similarity and a family of algorithm.
5. Select parameters such as \(k\), \(\epsilon\), or a grid resolution.
6. Run the algorithm, possibly with several initializations.
7. Evaluate internal quality, stability, external labels if available, and usefulness.
8. Describe clusters and monitor whether the solution is fit for deployment.

### 6. Important issues

- **Scale:** a large-range variable can dominate distance.
- **Noise and outliers:** they can distort centroids or create false groups.
- **High dimensionality:** distances become less discriminative and visualization is difficult.
- **Parameter choice:** \(k\) is not always obvious; density parameters are sensitive.
- **Initialization:** k-means can reach a poor local solution.
- **Shape and size:** k-means favors convex, similar-sized clouds.
- **Interpretability:** a statistical group may not correspond to a useful category.
- **Evaluation:** no single score settles validity.

### 7. Clustering versus classification

If labels already exist, classification usually predicts them. Clustering can discover groups and then be used as features or exploratory segmentation. A cluster ID is not a ground-truth class unless domain evidence and validation establish that meaning.

## Worked examples

### Example 1: A simple two-cluster solution

Points are `(1,1), (1.2,0.8), (8,8), (8.2,7.8)`. With k=2, the first two are near each other and the last two are near each other. The large gap between groups makes the partition stable. A one-cluster solution has less separation; the choice depends on the question, not just an algorithm.

### Example 2: Choosing attributes

Suppose customers have age in years and annual spend in dollars. A raw distance is dominated by spending. Standardizing age and spending permits both to contribute according to variation. If the application specifically cares about absolute spend, a weighted distance may be more appropriate; there is no universal normalization.

### Example 3: Clustering is not proof

A k-means grouping of students by marks into low, medium, and high bands is descriptive. It does not prove that a natural ability class exists or that an intervention based on the band will improve outcomes. External evidence and stability are needed.

## Key terms & formulas

- **Cluster:** a group of mutually similar objects.
- **Clustering:** unsupervised grouping of objects.
- **Similarity:** \(s(x,y)\), larger when more alike.
- **Dissimilarity/distance:** \(d(x,y)\), smaller when more alike.
- **Partition:** disjoint clusters covering the data, unless noise is allowed.
- **Flat clustering:** one-level groups.
- **Hierarchical clustering:** nested groups represented by a dendrogram.
- **Compactness:** members are close to one another or their center.
- **Separation:** clusters are distinct.
- **Stability:** solution persists under sampling or perturbations.
- **Noise/outlier:** object that does not fit a strong cluster.

## Common mistakes

1. **Calling clustering supervised:** it starts without class labels.
2. **Assuming a cluster is a true class:** it is a model-produced group.
3. **Ignoring feature scale:** distance-based results change with units.
4. **Using a single run of a random algorithm:** restarts and sensitivity analysis are important.
5. **Selecting \(k\) only because it is visually convenient:** use domain needs and validation.
6. **Ignoring outliers:** they can pull centers or create false density peaks.
7. **Reporting an internal score as proof of usefulness:** internal, external, stability, and interpretation checks differ.

## Exam prep

**Likely 2-mark questions**
1. Define cluster analysis. *Hint: unsupervised grouping by similarity.*
2. Differentiate partitioning, hierarchical, and density-based clustering. *Hint: fixed representatives, nested tree, connected dense regions.*
3. Why normalize attributes? *Hint: avoid large-range variables dominating similarity/distance.*

**Likely long-answer questions**
1. Explain the cluster-analysis workflow from data preparation to interpretation. *Hint: purpose, features, measure, algorithm, parameters, validation.*
2. Compare clustering and classification. *Hint: no labels versus known target and prediction.*
3. Discuss major challenges in high-dimensional noisy data. *Hint: scale, sparsity, outliers, initialization, shape, stability, interpretation.*
