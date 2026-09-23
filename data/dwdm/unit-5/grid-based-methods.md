---
subject: dwdm
unit: 5
topic: grid-based-methods
syllabus_ref: CSM3101 Unit-V
status: draft
---
# Grid-Based Clustering Methods

## Overview

Grid-based clustering divides the feature space into cells and treats each cell as a unit for density computation. Neighboring dense cells are connected into clusters. The idea is powerful in multidimensional spaces because many cells are empty, so occupied cells can be processed efficiently. **CLIQUE** is the standard textbook method: it projects high-dimensional data, finds dense regions in lower-dimensional projections, then intersects them to recover clusters.

## Explanation

### 1. Grid representation

Choose a number of intervals or levels for every numeric attribute. Each tuple falls into one cell. A cell may be empty, sparse, or dense. A **dense cell** contains at least a user-defined number of points. A **dense region** is a connected set of dense cells. Grid-based methods cluster cells and assign their points to the resulting groups.

The grid resolution is a parameter. Fine grids reduce the chance that unrelated points share a cell but increase the number of cells; coarse grids are faster but can merge different structures. Empty cells are often ignored because the occupied region may be sparse.

### 2. CLIQUE

CLIQUE stands for **Clustering In QUotient space, Ensemble** conceptually in its original description, but students should focus on its algorithm:

1. Choose \(\alpha\), the density threshold.
2. Partition each dimension into equal-width intervals.
3. Mark a cell occupied or dense.
4. Find connected dense regions in each one-dimensional projection.
5. Select the projection with the best candidate regions.
6. Use overlapping projections and intersections to identify dense high-dimensional regions.
7. Merge overlapping regions and assign tuples.

The key assumption is the **anti-monotonicity property**: if a region is not dense in a projection, it cannot be dense in the full space. Therefore low-density projections need not be searched further for a dense high-dimensional cluster. The method trades detailed shape information for projection efficiency.

### 3. Other grid ideas

STING stores summary statistics in a hierarchical grid and queries cells for high-density regions. Grid-based methods can be combined with density measures, distance functions, and subspace search. In sparse data, only occupied cells need processing, but the number of dimensions still affects memory and search.

### 4. Advantages and limitations

**Advantages:** efficient for high-dimensional sparse data; does not require all pairwise distances; can find clusters of arbitrary shape in the occupied grid; supports density thresholds and subspace discovery.

**Limitations:** grid size and interval boundaries affect results; it can miss diagonal or narrow structures; high-dimensional grid cells become sparse; boundaries can split a natural group; projection and merging rules are complex. A dense cell does not by itself prove a meaningful cluster.

## Worked examples

### Example 1: Two-dimensional grid

Use intervals [0,2), [2,4), [4,6), [6,8) on two attributes. Six points occupy cells:

| Cell | Points | Count |
|---|---|---:|
| (low, low) | 4 | dense |
| (low, next) | 1 | sparse |
| (high, high) | 3 | dense |

If density threshold \(\alpha=3\), the first and third cells are dense. If they are not edge-neighbors, they form two clusters; the sparse point is not in a dense region. A finer grid might separate the four points in the first cell if their internal structure matters.

### Example 2: CLIQUE projection

A 3-D cloud has only a few points in any one \(x_1\) value, but many points when \(x_2,x_3\) are considered. A projection onto \((x_2,x_3)\) has a dense region; intersecting candidate regions with all coordinates recovers a 3-D group. If every pair projection is sparse, anti-monotonicity says the full 3-D region is not dense.

### Example 3: Boundary sensitivity

Two points at 1.99 and 2.01 have distance 0.02, but with a boundary at 2 they enter different cells. A shifted grid can create a gap where none exists. Overlapping grids or a careful choice of interval width reduces this artifact.

### Example 4: Resolution tradeoff

If there are 100 levels per attribute and 5 attributes, a full grid has \(100^5=10^{10}\) possible cells. Only occupied cells may be stored, but projections and density summaries still require careful indexing. This is why sparse occupancy and projections are central to CLIQUE.

## Key terms & formulas

- **Grid cell:** interval-defined region in feature space.
- **Density threshold \(\alpha\):** minimum points for a dense cell/region.
- **Dense cell:** cell meeting the density threshold.
- **Dense region:** connected set of dense cells.
- **Projection:** lower-dimensional view used to find candidates.
- **CLIQUE:** grid, projection, anti-monotonicity, intersection, and merging algorithm.
- **STING:** hierarchical grid summary approach.
- **Empty cell:** interval with no data points; often skipped.
- **Grid resolution:** interval count/width tradeoff.
- **Anti-monotonicity:** a region sparse in a projection cannot be dense in the full space.

## Common mistakes

1. **Ignoring interval-boundary effects:** close points can be split by a cell boundary.
2. **Assuming a dense cell is always a whole cluster:** connected dense cells must be found.
3. **Forgetting the curse of many dimensions:** a full grid can be enormous.
4. **Misusing anti-monotonicity:** it rules out dense full regions from a sparse projection, not all useful projected patterns.
5. **Using only one coarse resolution:** resolution changes discovered density.
6. **Treating grid output as external ground truth:** validate interpretability and stability.

## Exam prep

**Likely 2-mark questions**
1. Define a grid-based clustering method. *Hint: partition feature space into cells and cluster dense cells.*
2. State CLIQUE's anti-monotonicity property. *Hint: sparse in a projection implies not dense in the full space.*
3. What is the role of alpha? *Hint: density threshold for a cell or region.*

**Likely long-answer questions**
1. Explain CLIQUE step by step. *Hint: grid, projections, dense regions, anti-monotonicity, intersections, merging.*
2. Compare grid-based and density-based clustering. *Hint: cells versus neighborhoods; resolution, shape, sparsity, parameters.*
3. Discuss grid resolution and boundary sensitivity with an example. *Hint: memory/computation tradeoff and shifted partitions.*
