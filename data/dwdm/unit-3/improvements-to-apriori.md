---
subject: dwdm
unit: 3
topic: improvements-to-apriori
syllabus_ref: CSM3101 Unit-III
status: draft
---
# Improvements to the Apriori Algorithm

## Overview

Basic Apriori is correct, but it may generate many candidate itemsets, test too many candidates during each support-counting pass, and rescan the full database. The standard improvements attack three costs: **candidate generation**, **support counting**, and the **amount of data processed**. They retain the Apriori property and level-wise search while reducing I/O, memory, and candidate work. A correct answer should connect each improvement to the bottleneck it removes rather than merely list names.

## Explanation

### 1. Reduce candidate generation

**Candidate pruning** is Apriori's main reduction. Before testing a \(k\)-itemset, remove it if any \((k-1)\)-subset is infrequent. Self-join and a set-membership structure can perform this check. If \(L_{k-1}\) is small, generate only the join of matching frequent itemsets. Additional techniques include:

- ordering items to make duplicate joins easier to detect;
- maintaining a hash set or tree of frequent previous-level itemsets;
- using different minimum-support thresholds to discover level-specific rare patterns;
- constraining item counts, maximum itemset size, or user-supplied item constraints when appropriate.

These techniques cannot delete a truly frequent pattern unless the constraint says that pattern is outside the task.

### 2. Hash-based support counting

A naive candidate \(C\) is compared with every transaction. A **hash tree** maps items to buckets. A transaction is first sorted and its items are mapped into hash-table addresses. A lookup key is formed from the appropriate \(k\)-items of the transaction, and a matching subtree can be searched. The transaction increments counters only for candidates found there.

For a 3-itemset, for example, the first two items can select a bucket and the third can be compared within it. The number of comparisons depends on hash occupancy and the fraction of candidates present, rather than always being \(|C||D|\).

A hash tree is especially useful when candidate count is large. Hash functions and item ordering must be consistent between tree construction and transaction probing.

### 3. Reduce the data before mining

**Transaction reduction:** if a transaction \(T\) is a subset of another transaction \(T'\), it can be removed. Any itemset that occurs in \(T\) also occurs in \(T'\), so \(T\)'s presence adds no distinct support evidence. This is different from deleting duplicate **items inside one transaction**; it removes an entire transaction that is contained in another.

**Item removal:** items below minimum support can be removed first, and transactions updated.

**Dataset reduction before decomposition:** for a distributable database with \(N\) transactions and \(P\) partitions, first find and remove globally infrequent items. For each partition, use transaction lengths and the global support threshold to bound how much support the remaining transactions could contribute. A transaction is removed only when even the optimistic contribution from all other partitions could not make any of its itemsets frequent. This reduces the data used by later Apriori passes without discarding evidence that is needed.

### 4. Sampling and multiple minimum support

A **sample** can provide a quick estimate of support and candidate structure. It is useful for exploration, but a pattern may be lost because it did not appear in the sample. A safe design is:

1. find candidates on a sample;
2. verify their support in the full database;
3. optionally run one more full pass to find additional patterns.

**Multiple minimum-support mining** permits rare items or rare patterns in selected regions while using stronger support elsewhere. It is useful for hierarchical or domain-specific patterns, but a global candidate family cannot be pruned solely by a high threshold. Algorithms organize thresholds and maintain different levels rather than applying one standard Apriori threshold blindly.

### 5. Partition the database

Partition \(D\) into \(P\) parts. A \(k\)-itemset is potentially frequent in \(D\) only if its summed support over all partitions can reach the global threshold. While discovering global infrequent items, local counts in each partition provide bounds. After the initial filtering, a transaction or partition with insufficient remaining-support capacity is excluded. This is a data-reduction optimization; partition-wise mining alone must not mistake local frequency for global frequency.

### 6. Avoid repeated scans

Apriori normally rescans the database once per level. Alternatives include loading transactions into main memory, or using compressed/encoded transactions. In distributed settings, local candidate generation followed by a global support merge reduces communication. Vertical mining uses bit vectors: each item has a transaction-position bit vector, and support is obtained by bitwise AND of its vectors. It can be efficient when the item count is modest and vectors fit memory, but the vectors themselves may be sparse and large.

### 7. What each improvement does not change

All methods still mine exact support under their assumptions. FP-growth is a different algorithm rather than a small Apriori optimization. Accuracy can also be traded for approximation by sampling or bounding, so an exam or report should state whether a result is exact or approximate.

## Worked examples

### Example 1: Transaction reduction

Transactions:

- \(T_1=\{A,B\}\)
- \(T_2=\{A,B,C\}\)
- \(T_3=\{B,C\}\)

\(T_1\subseteq T_2\), so \(T_1\) can be removed without changing support: every transaction containing \(A,B\) can be represented by \(T_2\). The reduced database is \(T_2,T_3\). However, \(T_3\) is not a subset of \(T_2\) because \(A\) is missing.

### Example 2: Partition support bound

Let \(N=1{,}000\), \(s_{\min}=0.05\), and \(P=4\) partitions. Then each partition has 250 transactions, and the global threshold is 50 occurrences. Suppose a 2-itemset has counts 2, 0, 0, and 10 across the partitions. Its exact count is 12, so it is infrequent. Even its optimistic remaining count after the first two partitions is 10, below 50; the search can discard it early.

### Example 3: Hash-tree comparison

Suppose there are 1,000 transactions and 100,000 3-itemset candidates.

- Naive worst case: up to \(100{,}000\times1{,}000=10^8\) full candidate comparisons.
- If each transaction probes only 30 candidate leaves, the work is about 30,000 probes plus comparisons within selected buckets.

The exact saving depends on hash design, but the point is that support counting need not compare every candidate with every transaction.

### Example 4: Sampling verification

A 10% sample contains 1,000 of 10,000 transactions. A candidate has sample support 3%. This estimates about 300 full-database occurrences. It does **not** prove full support. If \(s_{\min}=5\%\), the full data must still be scanned and the candidate retained only if it occurs in at least 500 transactions.

## Key terms & formulas

- **Candidate generation cost:** number of itemsets proposed before pruning.
- **Support-counting cost:** candidate–transaction comparisons or probe operations.
- **Hash tree:** hierarchy of buckets used to locate candidates.
- **Transaction reduction:** remove a transaction contained in another transaction.
- **Item removal:** delete globally infrequent items before further mining.
- **Partitioned scan:** first filter database to reduce later work.
- **Sample verification:** exact second pass over full data.
- **Multiple minimum support:** separate support requirements or supports for different pattern regions.
- **Vertical bit vector:** transaction membership bitset for one item.
- **Approximate versus exact:** approximate can miss support; exact counts it fully.

## Common mistakes

1. **Deleting a duplicate transaction blindly:** identical duplicates are removable if treated as repeated evidence, but a transaction merely contained in a different transaction is handled by the subset argument.
2. **Calling a local partition threshold global:** local support must be combined or bounded against the global target.
3. **Assuming sampling is exact:** it is a candidate-selection device unless a full verification pass occurs.
4. **Forgetting candidate set size in complexity:** scanning is not the only cost.
5. **Claiming a hash tree reduces the number of candidate sets:** it normally reduces comparisons during counting, not candidate generation itself.
6. **Ignoring memory limits:** bit vectors and hash trees can themselves be expensive.

## Exam prep

**Likely 2-mark questions**
1. What is a hash tree in Apriori? *Hint: a candidate index used during transaction probing.*
2. State the transaction-reduction rule. *Hint: remove a transaction contained in another without changing itemset support.*
3. Why verify sampled candidates on the full database? *Hint: the sample can miss frequent itemsets.*

**Likely long-answer questions**
1. Explain and compare candidate-generation, hash-counting, and data-reduction improvements. *Hint: classify each by the bottleneck it attacks.*
2. Describe partition-based reduction with support bounds. *Hint: partitions, local counts, remaining global capacity, discard rules.*
3. Propose a practical accelerated Apriori for a very large database and state its trade-offs. *Hint: hash tree, transaction/partition reduction, sample prefilter, exact verification.*
