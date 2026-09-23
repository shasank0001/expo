---
subject: ml
unit: 4
topic: density-based-clustering
syllabus_ref: CSM3201 Unit-IV
status: draft
---
# Density-Based Clustering

## Overview

Density-based clustering identifies regions where many observations are close together. It can discover clusters of arbitrary shape, separate points that do not belong to a dense region, and avoid forcing every observation into a cluster. DBSCAN is the standard example; HDBSCAN and OPTICS extend the idea for varying density, hierarchy, and noise.

These methods depend on a distance and density definition. Parameters such as neighbourhood radius and minimum points must be chosen or estimated carefully, especially when density varies across the data.

## Explanation

### Density concepts

A point \(p\) is a **core point** if at least `minPts` points, including itself, lie within radius `eps`:

\[
N_\epsilon(p)=\{q:d(p,q)\leq\epsilon\},
\qquad |N_\epsilon(p)|\geq \text{minPts}.
\]

A point is a **border point** if it lies within the neighbourhood of a core point but is not itself dense. A **noise/outlier point** is not within any core-point neighbourhood. These roles explain why DBSCAN can leave unassigned points instead of forcing them into a group.

### DBSCAN algorithm

1. Choose \(\epsilon\) and `minPts`.
2. For each unvisited point, find its \(\epsilon\)-neighbours.
3. If it is a core point, start a cluster and expand it by adding reachable neighbours, including their qualifying neighbours.
4. If it is not a core point, mark it as noise (it may later be attached as a border point).
5. Continue until all points are visited.

A density-reachable chain can connect points through core points, allowing non-convex shapes. The result is not controlled by a preselected \(K\).

### Parameter effects

- Small \(\epsilon\): many points become noise and clusters fragment.
- Large \(\epsilon\): dense regions merge and a single broad cluster may result.
- High `minPts`: fewer core points, more noise, more conservative clusters.
- Low `minPts`: more points join clusters and noise may be accepted.

A k-distance graph can help inspect a candidate \(\epsilon\), and a k-distance elbow is common. There is no universally correct value; validate with domain examples and stability.

### HDBSCAN

HDBSCAN estimates a hierarchy of density clusters rather than one fixed \(\epsilon\). It can find clusters of varying density and return cluster probabilities/stability. It is useful when density is not uniform, but parameter interpretation and computational cost require care. It still depends on a meaningful distance representation.

### OPTICS

OPTICS orders points by reachability density and produces a reachability plot. Valleys in the plot suggest clusters, and a threshold can extract a flat clustering. It is helpful for data with varying density and for exploring many scales, but users must read the plot and choose parameters.

### Advantages

- Finds arbitrary or crescent-shaped clusters.
- Does not require a fixed number of clusters.
- Identifies noise explicitly.
- Can handle clusters of different densities with HDBSCAN/OPTICS.
- Does not need a centroid, so it is not tied to spherical geometry.

### Limitations

- Sensitive to \(\epsilon\), `minPts`, scaling, and distance.
- High-dimensional data suffer from distance concentration; a poor metric can merge everything.
- Standard DBSCAN can have difficulty with strongly varying density.
- Distance-neighbour searches can be expensive in high dimensions or very large data.
- Noise is a modelling decision, not proof that a point is erroneous.
- Clusters still need interpretation and validation.

### Applications

DBSCAN is useful for spatial points, geospatial grouping, image segmentation, sensor networks, trajectory grouping, and anomaly screening. A group of GPS points following a road can form a connected density region even if it is not a simple circle. An isolated faulty sensor can be marked noise rather than averaged into a cluster.

### Choosing parameters and validating density structure

Density methods are especially sensitive to scale. A feature measured in thousands can dominate the \(\epsilon\)-neighbourhood, so standardise or use a domain metric. Inspect a k-distance graph or a reachability plot to understand the parameter range, then test a small set of plausible settings. A result that is stable over a broad parameter range is more convincing than a single carefully tuned result.

Core and border definitions are model decisions, not natural categories. A point just below the core threshold is labelled noise, while a point just above it is accepted. For decisions with meaningful cost, use a secondary model or a review queue rather than forcing a hard label. HDBSCAN can provide membership probabilities, but probability/stability still needs domain validation.

Noise should be analysed in context. It may be a data error, a rare valid event, a new population, or an attack signal. Keep the original record, route it for investigation, and monitor how the noise rate changes over time. A rising noise fraction can indicate drift, a changed data pipeline, or a new operating regime.

## Worked examples

### Example 1: core and noise

With \(\epsilon=1\) and minPts=4, a point with five neighbours is core. A point with two neighbours is not core, but if one of those neighbours is core, it may be a border point. A point isolated from every core point remains noise.

### Example 2: crescent shapes

Two interlocking crescents cannot be represented well by one centroid per group. Density connectivity can follow each crescent separately. K-means may instead split each crescent into pieces.

### Example 3: varying density

A sparse outer cluster and a dense inner cluster have different neighbourhood scales. A single DBSCAN \(\epsilon\) may label the sparse region as noise or merge the regions. HDBSCAN or OPTICS can expose multiple density levels.

### Example 4: anomaly screening

Most server records are dense around normal request volume. A rare record far from all dense regions is labelled noise. The operations team investigates it, but does not call it an attack automatically.

## Key terms & formulas

- **Density-based clustering:** groups data by connected dense regions.
- **DBSCAN:** density-based spatial clustering.
- **Core point:** point with at least `minPts` points within \(\epsilon\).
- **Border point:** non-core point near a core point.
- **Noise point:** point not assigned to a cluster.
- **\(\epsilon\)-neighbourhood:** \(N_\epsilon(p)=\{q:d(p,q)\le\epsilon\}\).
- **Eps parameter:** neighbourhood radius.
- **MinPts:** minimum neighbourhood count for a core point.
- **Density reachability:** chain of overlapping dense neighbourhoods.
- **HDBSCAN:** hierarchical density clustering with varying-density handling.
- **OPTICS:** ordering points by density and producing a reachability plot.
- **K-distance:** distance to the kth nearest neighbour, often used to choose \(\epsilon\).
- **Outlier/noise:** unusual point under the density model, not automatically an error.

## Common mistakes

1. **Choosing epsilon without inspecting the distance scale.** Results can be all noise or one cluster.
2. **Using DBSCAN directly on unscaled high-dimensional data.** Distance becomes uninformative.
3. **Assuming DBSCAN finds the right number of clusters.** Parameters and representation still matter.
4. **Treating noise as invalid data.** It may be a meaningful rare case.
5. **Ignoring density variation.** Standard DBSCAN may miss sparse clusters.
6. **Forgetting computational cost.** Neighbour searches and large data can be expensive.
7. **Interpreting a cluster boundary as a hard natural fact.** It reflects density and threshold choices.

## Exam prep

### Likely 2-mark questions

- **Define DBSCAN.** A density-based clustering algorithm that finds connected dense regions and labels sparse points as noise.
- **What is a core point?** A point with at least `minPts` points within radius \(\epsilon\).
- **What does eps control?** The neighbourhood radius used to assess density.
- **Give one advantage of density-based clustering.** It can find non-convex clusters and does not require \(K\).

### Long-answer prompts

- **Explain the DBSCAN algorithm step by step.** Define core, border, and noise points and discuss expansion.
- **Compare DBSCAN and k-means.** Discuss shape, \(K\), noise, scaling, parameters, and complexity.
- **How do \(\epsilon\) and minPts affect clustering?** Give examples of fragmentation, merging, and noise.
- **Describe HDBSCAN or OPTICS.** Explain why it helps with varying density and how its output is interpreted.
