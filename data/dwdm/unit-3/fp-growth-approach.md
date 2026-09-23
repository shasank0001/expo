---
subject: dwdm
unit: 3
topic: fp-growth-approach
syllabus_ref: CSM3101 Unit-III
status: draft
---
# FP-Growth Approach

## Overview

FP-growth, or **frequent-pattern growth**, mines frequent itemsets by first finding frequent items and then compressing the transaction database into an **FP-tree (frequent-pattern tree)**. It does not need the large level-wise candidate sets of Apriori and normally does not rescan the original database for every level. Instead, it recursively mines smaller projected or conditional pattern bases. For transaction data, it is one of the most important algorithms in the syllabus.

## Explanation

### 1. FP-tree structure

An FP-tree has:

- a **root node** labelled null;
- child pointers and next pointers;
- each item node storing an item name and a support count;
- a **header table** listing frequent items and linking their node occurrences.

The support count on a node is the number of transactions whose projected paths pass through that node; it is not merely a per-database item count. The tree preserves the order in which transactions are inserted, so shared prefixes are compressed.

### 2. Steps of FP-growth

Given transaction database \(D\) and minimum support \(s_{\min}\):

1. Scan \(D\) once and count 1-item supports.
2. Retain frequent items in \(L_1\) and choose an order, commonly decreasing support, with deterministic tie-breaking.
3. Scan \(D\) a second time. Remove infrequent items from each transaction, sort the remaining items in the chosen order, and insert the resulting list into the FP-tree.
4. Select the least frequent item in the header table, follow its node links to form its **pattern base** (projected database), then construct a conditional FP-tree.
5. Recursively mine that conditional tree. Merge the patterns produced at different depths.
6. Return the frequent itemsets.

Two initial scans establish the item order and build the tree. Further mining uses projected bases and conditional trees rather than scanning all original transactions at every itemset size.

### 3. Pattern base and conditional pattern base

For an item \(x\), the **pattern base** \(P_b(x)\) is the set of paths from the root to nodes labelled \(x\). Each path is truncated at \(x\). It is not a second independent database; it represents transactions relevant to mining itemsets that include \(x\).

The **conditional pattern base** \(P_b(x\mid I)\) depends on already selected items \(I\). It contains the prefixes before the conditional items in the pattern base. Conditional mining enumerates combinations of \(I\) with extensions found in that smaller base.

### 4. Why support is inherited

An \(x\)-prefix-tree contains the path information needed to find extensions of \(x\), but an empty-root tree alone is not listed. If the sum of the node counts in a constructed conditional tree is less than the required projected support, the corresponding extension is discarded. This check prevents treating duplicated paths or different projections as separate original transactions.

### 5. Recursive mining and merge

For the chosen item \(x\), recursively mine its conditional tree. A frequent itemset found in that tree must be combined with \(x\) and the selected prefix \(I\). Results from distinct depths and conditional bases must be merged, not treated as the same itemset. Node-link traversal prevents repeatedly walking the entire header list.

### 6. Correctness intuition

Every transaction that can contribute to an itemset containing \(x\) appears on some root-to-\(x\) path. The pattern base therefore contains the required prefix information. Recursive conditional mining explores all combinations of extensions, and the minimum-support test removes only impossible branches. Thus FP-growth finds exactly the same frequent itemsets as Apriori, although its storage and search organization differ.

### 7. Complexity and limitations

FP-growth is typically much faster than repeated Apriori scans, especially when the number of frequent itemsets is large. Its tree can nevertheless be huge for dense data. Header-table, node, and projected-database memory are important. FP-growth is naturally designed for sparse horizontal transaction data; dense data and many singleton items can still cause a large tree. Single-path trees can be optimized, but the basic method should still be understood.

## Worked examples

### Example 1: First pass and item order

Database:

| Transaction | Items |
|---|---|
| \(T_1\) | A, B, C |
| \(T_2\) | A, C |
| \(T_3\) | A, B |
| \(T_4\) | B, C |
| \(T_5\) | A, B, C |
| \(T_6\) | B, C |

Use absolute minimum support 3. Item counts are A=4, B=5, C=5, and D=0. D is removed. Choose order \(C>A>B\) (decreasing support, with A before B by a fixed tie rule).

### Example 2: Build the FP-tree

Reorder and insert each transaction:

| Original | Filtered and ordered path |
|---|---|
| T1 | C, A, B |
| T2 | C, A |
| T3 | A, B |
| T4 | C, B |
| T5 | C, A, B |
| T6 | C, B |

Tree description:

```text
root
└─ C:5
   ├─ A:2
   │  ├─ B:1       (T1)
   │  └─ B:1       (T5)
   └─ B:2          (T4,T6)

root
└─ A:1             (T3)
   └─ B:1
```

Equivalent links: root-C is also the left child concept of root and C's second child B. The important facts are the item node names, counts, and header links. The header table has C:5, A:4, B:5.

### Example 3: Pattern base for the least-frequent item

A has count 4, so follow A's header links: root-C-A:2 and root-A:1.

Its pattern base is:

```text
C,A : 2
A : 1
```

These represent three transactions containing A: two with prefix C and one with only A. Mining this base finds the extension \(CA\), with count 2. Since projected minimum support is 3, \(CA\) is not frequent. No other extension is frequent.

### Example 4: Pattern base for C

C appears in five transactions. Its path links are:

- C:2
- C-A:2
- C-B:2

The truncated pattern base is:

```text
A,B : 2
A : 2
B : 2
```

The root node is not copied as a separate transaction. Build a conditional C-tree:

```text
C-root
├─ A:4
│  └─ B:2
└─ B:2
```

Conditional patterns for A include A alone with count 4 and AB with count 2. A alone is already a frequent singleton; AB is below minimum support. For B, B alone has count 2 in this projected context and is below the conditional threshold. Combining valid results with the root condition gives only \(C\) at this branch; no 2-itemset containing C reaches 3.

### Example 5: Check against Apriori

The result is

\[
L_1=\{A,B,C\},\qquad L_2=\varnothing.
\]

Apriori agrees: AB occurs 3, AC occurs 3, BC occurs 4, but every triple occurs at most 2. The FP-tree reached the same exact result without separately proposing six pairs and two triples.

### Example 6: Minimal second dataset

Suppose transactions are `AB`, `AB`, `AC`, and `B`, with \(s_{\min}=2\). Frequent items are A=3 and B=3. Order B before A. The tree is `root-B:3 -> A:2` plus `root-A:1`. The root-to-B paths are truncated after B: the first two paths contain prefix A and the third has an empty prefix. Empty prefixes are not counted as separate transactions, so the conditional B-tree has one node `A:2`. The extension BA therefore has support 2 and is frequent. The root-A node is not on a path to B and is not part of B's pattern base.

## Key terms & formulas

- **FP-tree:** compressed tree of frequent items and transaction paths.
- **Header table:** frequent items, counts, and links to all their nodes.
- **Item node count:** transactions represented through that node.
- **Pattern base \(P_b(x)\):** root-to-\(x\) paths truncated after \(x\).
- **Conditional pattern base \(P_b(x\mid I)\):** projected prefixes conditional on \(I\).
- **Conditional FP-tree:** tree built from a projected base.
- **Support inheritance:** recursive projected counts preserve evidence for \(I\cup x\).
- **Prefix sharing:** common transaction prefixes are stored once.
- **Node-link traversal:** follow header links rather than scan all nodes.
- **Projection:** restrict transactions to the items relevant to a recursive branch.

## Common mistakes

1. **Copying the root as a transaction:** it is a structural node, not an empty-basket record.
2. **Using the old header count as every extension's support:** conditional counts must be recomputed.
3. **Forgetting to sort after removing infrequent items:** the tree depends on one consistent order.
4. **Mining each header item as if its tree were the full database:** extensions are conditional on a prefix.
5. **Assuming no second scan:** two initial scans are standard for item order and insertion.
6. **Ignoring memory cost:** a huge tree is possible even when the algorithm is fast.

## Exam prep

**Likely 2-mark questions**
1. What is an FP-tree? *Hint: a compressed tree of frequent-item transaction paths with a header table.*
2. Define a pattern base. *Hint: truncated root-to-item paths used for conditional mining.*
3. Name the two initial FP-growth scans. *Hint: count frequent items; filter/sort/rebuild the tree.*

**Likely long-answer questions**
1. Explain every step of FP-growth and compare it with Apriori. *Hint: item count, ordering, tree build, header links, pattern bases, recursive mining, complexity.*
2. Build an FP-tree from a supplied database and mine at least one conditional branch. *Hint: show reordered transactions, node counts, header links, and projected support checks.*
3. Explain how FP-growth can avoid repeated database scans while remaining exact. *Hint: projection retains only paths relevant to an item and inherited prefix.*
4. Discuss when FP-growth may still be expensive. *Hint: dense data, many items, very large tree, projected bases.*
