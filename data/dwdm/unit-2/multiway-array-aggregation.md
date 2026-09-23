---
subject: dwdm
unit: 2
topic: multiway-array-aggregation
syllabus_ref: CSM3101 Unit-II
status: draft
---
# Multiway Array Aggregation for a Full Cube

## Overview

Multiway array aggregation computes a full data cube by viewing facts as cells in a multidimensional array. It aggregates along one dimension at a time, then along additional dimensions, producing every cuboid. The method is systematic and exam-friendly: given a small array, show the base cuboid, the partial aggregates, and the final totals. Large cubes require chunking, sparse storage, and an order that controls intermediate work.

## Explanation

### 1. Array representation

Let dimensions have cardinalities \(d_1,d_2,\ldots,d_k\). A cell is indexed by one member from each dimension:

\[
A[i_1,i_2,\ldots,i_k].
\]

A base fact updates one cell. The full cube contains cells for every subset of dimensions: for a 3-D cube, the cuboids are the base (day, product, region), 2-D cuboids for pairs, 1-D marginals, and the grand total. A 4-D cube similarly has \(2^4\) conceptual combinations of included dimensions, subject to hierarchy validity.

### 2. Aggregation along one axis

To collapse the third axis, for example,

\[
A^{(2)}[i,j]=\sum_{r}A[i,j,r].
\]

The result is a 2-D array. Collapse another axis:

\[
A^{(1)}[i]=\sum_j A^{(2)}[i,j],
\]
\[
A^{(0)}=\sum_iA^{(1)}[i].
\]

In a 3-D cube, compute all pair marginals and all one-dimensional marginals, then the grand total. Each marginal must be formed from a cell or a compatible aggregate exactly once; adding overlapping aggregates can double count.

### 3. Full-cube procedure

1. Define dimensions, levels, and measure aggregation functions.
2. Allocate or represent the base array and initialize cells to zero or a count.
3. Scan each fact and add its measure to its base cell.
4. For each axis, sum or apply the required function to create a collapsed array.
5. Save the desired cuboids before further collapse.
6. Continue until the grand total.
7. Validate totals against source sums and test sparse/empty cells.

A general conceptual recurrence is

\[
A^{S\cup\{j\}}[i_1,\ldots,i_n]
=\operatorname{AGG}_{j}\left(A^S[i_1,\ldots,i_n,j]\right),
\]

where \(S\) is the set of retained dimensions and \(j\) is the dimension being removed. `AGG` may be sum, count, min, or max. For average, retain the count and sum.

### 4. 2-D and 3-D examples

For a 2-D array, first form row sums and column sums, then the grand total:

\[
R_i=\sum_jA[i,j],\qquad C_j=\sum_iA[i,j],\qquad T=\sum_iR_i.
\]

For a 3-D array, form the six 2-D marginals:

\[
M_{12}=\sum_rA[i,j,r],\quad
M_{13}=\sum_jA[i,k,r],\quad
M_{23}=\sum_iA[i,j,k],
\]

then derive the one-dimensional marginals and \(T\). A 4-D cube repeats this logic along each axis.

### 5. Chunking and memory

A dense array of size \(\prod d_i\) can be too large. **Chunking** divides a dimension into blocks, computes a partial cube for each chunk, and combines the partial results using an associative/commutative aggregate such as sum or min. Max is also combinable; average requires sum and count. Choose the chunk dimension and order to balance memory, I/O, and parallelism.

For a 4-D array with dimensions \((d_1,d_2,d_3,d_4)\), one can process a slice of the first dimension at a time. The total of each output cell is the sum of corresponding partial cells. Chunk boundaries must not split a fact or double count a partial contribution.

### 6. Sparse representation and optimization

If most cells are empty, store a list or hash of nonzero cells. Sparse representation reduces memory but can make repeated aggregation slower. Dimension ordering affects locality and intermediate work; precompute common cuboids, use columnar storage, partition by time, and process independent chunks in parallel. Choose which cuboids to retain based on query workload.

### 7. Correctness checks

For an additive measure, the sum of every cuboid along an axis must equal the corresponding lower-level marginal. The grand total must equal the sum of base facts and the sum of the selected marginal. If these checks fail, inspect double counting, missing facts, wrong dimension mappings, or invalid aggregation.

## Worked examples

### Example 1: Complete 3-D base array

Let dimensions be product \(P=\{p1,p2\}\), time \(T=\{t1,t2,t3\}\), and region \(R=\{r1,r2\}\). Base cells are:

| Product | Time | Region | Sales |
|---|---|---|---:|
| p1 | t1 | r1 | 10 |
| p1 | t1 | r2 | 20 |
| p1 | t2 | r1 | 30 |
| p1 | t2 | r2 | 40 |
| p1 | t3 | r1 | 50 |
| p1 | t3 | r2 | 60 |
| p2 | t1 | r1 | 5 |
| p2 | t1 | r2 | 6 |
| p2 | t2 | r1 | 7 |
| p2 | t2 | r2 | 8 |
| p2 | t3 | r1 | 9 |
| p2 | t3 | r2 | 10 |

Base total: p1 subtotal 210, p2 subtotal 45, grand total 255. Each marginal below is computed directly from these base cells.

#### Product by region

| Product | r1 | r2 | All regions |
|---|---:|---:|---:|
| p1 | 90 | 120 | 210 |
| p2 | 21 | 24 | 45 |
| All | 111 | 144 | 255 |

#### Product by time

| Product | t1 | t2 | t3 | All |
|---|---:|---:|---:|---:|
| p1 | 30 | 70 | 110 | 210 |
| p2 | 11 | 15 | 19 | 45 |
| All | 41 | 85 | 129 | 255 |

#### Time by region

| Time | r1 | r2 | All |
|---|---:|---:|---:|
| t1 | 15 | 26 | 41 |
| t2 | 37 | 48 | 85 |
| t3 | 59 | 70 | 129 |
| All | 111 | 144 | 255 |

One-dimensional marginals are:

- Product: p1=210, p2=45.
- Time: t1=41, t2=85, t3=129.
- Region: r1=111, r2=144.

The eight cuboids (base, three 2-D marginals, three 1-D marginals, and grand total) are consistent.

### Example 2: 2-D row and column sums

Base matrix:

```text
       Jan Feb
North  10  20
South  30  40
```

Row sums are 30 and 70; column sums are 40 and 60; grand total is 100. The row total, column total, and base-cell sum must all reconcile.

### Example 3: Chunked sum

Suppose a 4-D array is split into two chunks along the first dimension. The first chunk produces a partial total 70 from 7 facts and the second 30 from 6 facts. The combined total is 100. For an average, the chunks must return both total and count:

\[
\frac{70+30}{7+6}=\frac{100}{13}\approx7.69,
\]

not the simple average of the chunk averages, \((10+5)/2=7.5\).

### Example 4: Sparse cube

A 100×100×100 logical cube has 1,000,000 possible cells, but only 12 facts. A sparse representation stores the 12 occupied cells and their counts; dense allocation would waste memory. When queried for a missing combination, the engine returns a defined zero/empty result only if the business rule permits it.

## Key terms & formulas

- **Multidimensional array:** \(A[i_1,\ldots,i_k]\).
- **Base cuboid:** all dimensions at base levels.
- **Marginal:** aggregate after removing one or more dimensions.
- **Grand total:** aggregate over all dimensions.
- **Multiway aggregation:** collapse axes successively.
- **Chunk:** block of the array.
- **Partial cube:** aggregate for one chunk.
- **Associative aggregate:** can combine partial results, such as sum/min/count.
- **Reconciliation:** equality checks across cuboids.
- **Sparse cube:** stores occupied cells rather than every possible cell.

## Common mistakes

1. **Adding overlapping cuboids:** a fact can be counted more than once.
2. **Using the wrong p1 subtotal:** calculate every marginal directly from base facts.
3. **Averaging chunk averages:** combine sum and count first.
4. **Treating an empty cell as a real zero:** its meaning depends on the measure and grain.
5. **Chunking a fact across two chunks:** partition by a complete dimension or a safe rule.
6. **Assuming every full-cube cell is needed:** materialized cuboids should follow queries.

## Exam prep

**Likely 2-mark questions**
1. What is multiway array aggregation? *Hint: collapse dimensions successively to form cuboids.*
2. Define a marginal cuboid. *Hint: an aggregate after one or more dimensions are removed.*
3. What is the purpose of chunking? *Hint: bound memory while combining partial cubes.*

**Likely long-answer questions**
1. Compute a full 3-D cube from a supplied base array. *Hint: base total, pair marginals, one-dimensional marginals, consistency checks.*
2. Explain chunking and combination for a 4-D cube. *Hint: partial arrays, sum/min/count combination, memory and parallelism.*
3. Compare dense and sparse cube computation. *Hint: allocation, occupied cells, query performance, and validation.*
