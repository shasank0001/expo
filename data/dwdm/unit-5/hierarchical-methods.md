---
subject: dwdm
unit: 5
topic: hierarchical-methods
syllabus_ref: CSM3101 Unit-V
status: draft
---
# Hierarchical Clustering Methods

## Overview

Hierarchical clustering builds a tree of groups rather than returning only one flat partition. **Agglomerative** methods start with singleton clusters and merge the closest pair. **Divisive** methods start with all objects together and split. A dendrogram shows when groups join or separate and can reveal structure at several scales. The final flat clusters are obtained by cutting the tree at a chosen height, so linkage method, distance, and cut level are important decisions.

## Explanation

### 1. Agglomerative algorithm

1. Put each object in its own cluster.
2. Compute pairwise dissimilarities.
3. Merge the closest clusters.
4. Update the distance matrix using the chosen linkage rule.
5. Repeat until one cluster remains or \(k\) clusters are requested.
6. Cut the dendrogram at the desired level.

Naive implementations take \(O(n^2)\) memory for the distance matrix and roughly \(O(n^3)\) time to recompute all distances. Nearest-neighbor chains, priority queues, and reducible distances improve practical scalability.

### 2. Linkage methods

Let \(d(i,j)\) be the original object distance, and \(A,B\) be clusters.

- **Single linkage:** \(d(A,B)=\min_{i\in A,j\in B}d(i,j)\). It chains loosely connected objects and can produce long “snakes.”
- **Complete linkage:** \(d(A,B)=\max_{i\in A,j\in B}d(i,j)\). It keeps clusters compact and can merge more slowly.
- **Average linkage:** \(d(A,B)=\frac1{|A||B|}\sum d(i,j)\). It balances the two extremes.
- **Centroid linkage:** distance between cluster means. It is most natural for Euclidean data and cannot be updated for every arbitrary merge without care.
- **Ward linkage:** merges the pair that causes the smallest increase in within-cluster sum of squares:

\[
\Delta(A,B)=\frac{|A||B|}{|A|+|B|}\|\mu_A-\mu_B\|^2.
\]

Ward's criterion and a squared Euclidean distance are related; the exact convention must be stated.

### 3. Lance–Williams update

Many linkage rules can be expressed by a recurrence. If \(A\) and \(B\) merge into \(C=A\cup B\),

\[
d(C,K)=\alpha_A d(A,K)+\alpha_Bd(B,K)
+\gamma|A|d(A,B),
\]

with method-specific coefficients. A complete-linkage tree, for example, uses a maximum, while a centroid or Ward tree uses a particular weighted combination. If an exam gives a Lance–Williams formula, calculate the new distances rather than guessing a merge.

### 4. Reading a dendrogram

The vertical axis is merge dissimilarity, not a class probability. A low cut produces many small groups; a high cut produces few large groups. Objects joined at a lower dissimilarity are more similar under the selected linkage. A tight pair of groups that joins at a much larger height suggests two well-separated subclusters. Rotation and leaf ordering do not change the set of merges, but visual clarity can.

### 5. Divisive clustering

Start with all objects in one cluster and split it, often choosing the split with the greatest dissimilarity or reduction in error. Methods include:

- **Top-down splitting:** bisect a cluster along a principal direction, farthest pair, or a k-means-like split.
- **k-d tree bisecting:** choose a median or mean split along an attribute and recurse.
- **Bisecting k-means:** run 2-means and recurse.

A divisive result can depend on the order and method of splits. A good coarse split can make later clusters easy; a poor first split can be hard to repair.

### 6. Selecting the number of clusters

A dendrogram offers a natural cut, silhouette, gap statistic, cophenetic correlation, or domain requirements. A tall merge height may suggest two macro-clusters, but linkage can make a misleading tree. Compare the flat solution with a partitioning method and inspect cluster descriptions.

### 7. Strengths and limitations

**Strengths:** no need to specify \(k\) before building the tree; results at multiple scales; dendrogram is interpretable; works with a chosen distance, including non-Euclidean measures.

**Limitations:** local greedy merges cannot be globally optimized; one merge cannot be undone; distance updates depend on linkage; memory and computation can be high; chain effects and inversions can make the tree unintuitive. Hierarchical methods can be sensitive to outliers and scale.

## Worked examples

### Example 1: Single versus complete linkage

Points: A=(0,0), B=(1,0), C=(5,0), D=(6,0).

Nearest pair is A–B at 1 and C–D at 1. Tie-breaking merges A and B, then C and D. The cluster distance is:

- single linkage: 4, distance between B and C;
- complete linkage: 6, distance between A and D.

If the tie is broken by merging AB and CD next, the final merge is 4 or 6. A clustering with one cluster cut at height 5 therefore has one group under complete linkage but two groups under single linkage.

### Example 2: Average linkage calculation

After merging A and B, compare that cluster to C and D. Suppose

\[
d(A,C)=4,\quad d(B,C)=6,\quad d(C,D)=1,\quad d(A,D)=6,\quad d(B,D)=8.
\]

Average distances are

\[
d(AB,C)=\frac{4+6}{2}=5,\qquad
d(AB,D)=\frac{6+8}{2}=7.
\]

C–D remains closest at 1. The matrix update illustrates why average linkage is less sensitive to one extreme pair than single linkage.

### Example 3: Ward increment

Two clusters with means \(\mu_A=(0,0)\), \(\mu_B=(2,2)\), and sizes 2 and 3 have

\[
\Delta=\frac{2(3)}{5}[(0-2)^2+(0-2)^2]
=\frac65(8)=9.6.
\]

Ward's criterion is in squared-distance units. If the class of the object distance is ordinary Euclidean distance, use the corresponding squared convention consistently.

### Example 4: Cutting a tree

Suppose A and B merge at 1, C and D at 1.2, and the two groups merge at 8. A cut at 1.5 gives two clusters, while a cut at 9 gives one. A cut at 0.5 gives four singleton clusters. The chosen level is a modeling decision.

## Key terms & formulas

- **Agglomerative:** merge from singletons upward.
- **Divisive:** split from one cluster downward.
- **Dendrogram:** tree of merges or splits.
- **Single linkage:** minimum cross-cluster distance.
- **Complete linkage:** maximum cross-cluster distance.
- **Average linkage:** mean cross-cluster distance.
- **Centroid linkage:** distance between means.
- **Ward:** minimize increase in within-cluster SSE.
- **Lance–Williams:** recurrence for updating cluster distances.
- **Cut level:** height at which the tree is interpreted as flat clusters.
- **Cophenetic correlation:** agreement between tree heights and original distances.

## Common mistakes

1. **Confusing single and complete linkage:** minimum versus maximum cross-cluster distance.
2. **Treating dendrogram height as probability:** it is a dissimilarity level.
3. **Ignoring a tie between equally close merges:** tie-breaking can change the tree.
4. **Assuming the greedy tree is globally optimal:** later merges cannot undo earlier choices.
5. **Using Ward with an arbitrary distance without checking the criterion:** Ward assumes squared Euclidean/SSE logic.
6. **Choosing a cut solely because it gives a desired \(k\):** validate and interpret.

## Exam prep

**Likely 2-mark questions**
1. Differentiate agglomerative and divisive hierarchical clustering. *Hint: merge upward versus split downward.*
2. State single and complete linkage formulas. *Hint: minimum versus maximum cross-cluster distance.*
3. What does a dendrogram represent? *Hint: nested merges/splits and their dissimilarity levels.*

**Likely long-answer questions**
1. Perform agglomerative clustering with a supplied distance matrix. *Hint: find minimum, merge, update using linkage, continue, draw/cut the dendrogram.*
2. Compare the five major linkage methods. *Hint: formulas, shapes, chaining, compactness, and use cases.*
3. Discuss divisive clustering and ways to choose a split. *Hint: maximum separation, k-d tree, bisecting k-means, recursion.*
