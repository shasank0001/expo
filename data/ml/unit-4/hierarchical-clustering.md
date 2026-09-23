---
subject: ml
unit: 4
topic: hierarchical-clustering
syllabus_ref: CSM3201 Unit-IV
status: draft
---
# Hierarchical Clustering

## Overview

Hierarchical clustering builds a tree of groups rather than one flat partition. It can be agglomerative, merging clusters step by step, or divisive, splitting a group repeatedly. A dendrogram shows which observations or clusters merge at different distances or similarities. The method is useful when the analyst wants to explore several granularities, identify nested structure, or understand relationships.

Its result depends strongly on the distance and linkage choice. Hierarchical clustering does not require an initial \(K\) to produce a single final grouping, but a cut level still must be chosen, and a merge cannot be undone in the agglomerative process.

## Explanation

### Agglomerative algorithm

Start with each observation in its own cluster. At every step:

1. Compute the dissimilarity between every pair of clusters.
2. Merge the pair with the selected smallest dissimilarity.
3. Update pairwise cluster dissimilarities.
4. Repeat until one cluster remains or a stopping rule is reached.

A cut through the dendrogram at a chosen height yields a partition. The number of clusters is therefore a later interpretation of the merge tree, not necessarily specified at the start.

### Linkage methods

For clusters \(A\) and \(B\):

- **Single linkage:** \(d(A,B)=\min_{a\in A,b\in B}d(a,b)\). It can chain clusters.
- **Complete linkage:** \(d(A,B)=\max_{a\in A,b\in B}d(a,b)\). It favours compact, equal-sized groups.
- **Average linkage:** \(d(A,B)=\frac{1}{|A||B|}\sum_{a\in A,b\in B}d(a,b)\), a compromise.
- **Ward linkage:** merges clusters to minimise the increase in within-cluster sum of squares; it assumes Euclidean geometry and is biased toward spherical clusters.

Linkage is not a neutral detail. A domain expert should understand whether a method is sensitive to outliers and chaining.

### Distance and representation

Use Euclidean distance for scaled numerical data, correlation or cosine for features where magnitude is not meaningful, and a suitable dissimilarity for categorical or mixed data. A distance that treats two different categories as far apart may be appropriate; one based on arbitrary category codes is not. Missing values and rare groups require a policy.

### Divisive clustering

Divisive methods begin with all observations in one cluster and split it, often using clustering within each group. They can be computationally expensive and may use a global view, but the result also depends on the split criterion. Divisive methods are less common than agglomerative methods in basic implementations.

### Choosing a cut and validating

A dendrogram can suggest a large jump in merge distance. Choosing that cut is a heuristic. Compare the resulting clusters with internal metrics, bootstrap stability, and domain knowledge. Assess whether groups are compact, have distinct profiles, and remain meaningful at a nearby cut. Do not claim that the tree proves a unique natural hierarchy.

### Computational considerations

A naïve agglomerative implementation compares every pair at every merge and can require \(O(n^2)\) memory and \(O(n^3)\) time in simple cases. Memoisation, Lance–Williams formulas, or approximate nearest-neighbour methods reduce cost for larger data. Sampling or first reducing dimensions can help, but may discard structure.

### Interpretation and uses

Hierarchical clustering is used in gene expression, taxonomy, document organisation, customer analysis, and nested segmentation. The dendrogram can show relationships at several scales. It is useful when no single cluster count is known and domain experts want to inspect substructures.

### Limitations

The greedy agglomerative process makes an early merge irreversible, so a poor initial representation or linkage can affect the final tree. It can be sensitive to outliers, scaling, and missingness. A high-resolution tree can be difficult to read. It does not naturally provide a probability or uncertainty. Large data may be computationally expensive.

### Choosing linkage and interpreting the tree

Linkage determines the tree, so it should be treated as a modelling assumption. Single linkage is sensitive to chains and outliers; complete linkage can favour compact, similar-sized groups; average linkage is a middle ground; Ward's method is tied to squared Euclidean error and spherical clusters. Run more than one linkage where practical and compare the profiles. If the groups change substantially, the data do not support a strong unique hierarchy.

A cut level should be chosen using both the merge distances and the intended use. Look for a large increase in dissimilarity, stable membership under resampling, and a number of groups that can be described and supported. A dendrogram is not a statistical test, and a visually attractive branch does not prove a biological, social, or causal hierarchy. Distances should be reported so another analyst can reproduce the tree.

For a large data set, a full pairwise distance matrix is costly. A sample-based tree, an approximate neighbour method, or a two-stage approach can provide an overview, but it may miss rare branches. Preserve the scale and linkage used in any documented result.

## Worked examples

### Example 1: merge sequence

Three customers have distances 2, 3, and 6. The pair at distance 2 merges first. The distance from the merged cluster to the third customer is then recomputed. Depending on linkage, it may be 3, 4, 5, or 6. This illustrates why the pairwise distance must be updated after every merge.

### Example 2: single versus complete linkage

Suppose two points near a third bridge points. Single linkage can chain them into one long cluster. Complete linkage requires a larger separation before merging and may create compact clusters. Compare profiles and stability rather than choosing by habit.

### Example 3: selecting a cut

A dendrogram has small distances within broad groups, then one large jump from 0.3 to 0.9. Cutting after the jump gives two groups. The analyst also checks whether a three-group cut is stable and operationally useful; the large jump is evidence, not a guarantee.

### Example 4: gene expression

Genes with similar expression patterns merge. The tree suggests modules, but expression similarity is not necessarily biological function. Researchers validate modules with independent experiments and avoid treating the dendrogram as causal evidence.

## Key terms & formulas

- **Hierarchical clustering:** clustering that builds a hierarchy.
- **Agglomerative:** bottom-up merging.
- **Divisive:** top-down splitting.
- **Dendrogram:** tree representation of merges/splits.
- **Dissimilarity:** distance used between clusters.
- **Single linkage:** minimum pairwise distance.
- **Complete linkage:** maximum pairwise distance.
- **Average linkage:** mean pairwise distance.
- **Ward linkage:** merge minimising increase in WCSS.
- **Cut level:** horizontal cut yielding a flat clustering.
- **Chaining:** single-linkage merging of a sequence through close pairs.
- **Cophenetic correlation:** agreement between tree distances and original distances, when used.
- **Stability:** consistency of cluster membership under resampling.

## Common mistakes

1. **Choosing linkage without checking its assumptions.** Results can change substantially.
2. **Using unscaled features.** The tree then reflects units, not domain similarity.
3. **Treating a dendrogram as proof of hierarchy.** It reflects one algorithm and metric.
4. **Selecting a cut by aesthetics alone.** Use stability, profiles, and domain needs.
5. **Forgetting that agglomerative merges are irreversible.** Early errors propagate.
6. **Ignoring computational cost.** A full pairwise matrix can be large.
7. **Using a cluster as a fixed identity.** Behaviour and context change.

## Exam prep

### Likely 2-mark questions

- **Define hierarchical clustering.** Building a tree of nested groups by merging or splitting.
- **What is a dendrogram?** A diagram showing the order and level of cluster merges or splits.
- **Name two linkage methods.** Single, complete, average, or Ward.
- **What is single linkage?** The minimum distance between any pair of members in two clusters.

### Long-answer prompts

- **Explain the agglomerative hierarchical algorithm.** Include initialisation, pairwise distance, merge, update, stopping, and cut selection.
- **Compare single, complete, average, and Ward linkage.** Discuss chaining, compactness, geometry, and use cases.
- **How would you validate a hierarchical clustering?** Use cut sensitivity, bootstrap stability, cluster profiles, internal/external measures, and domain interpretation.
- **Describe advantages and limitations of hierarchical clustering.** Discuss interpretability, multiple scales, cost, irreversibility, scale, and outliers.
