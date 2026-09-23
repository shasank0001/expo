---
subject: dwdm
unit: 3
topic: apriori-algorithm
syllabus_ref: CSM3101 Unit-III
status: draft
---
# Apriori Algorithm

## Overview

Apriori is the classic level-wise algorithm for mining frequent itemsets. Its central observation is simple: if an itemset is infrequent, none of its supersets can be frequent. That observation, called the **Apriori property**, allows the algorithm to avoid testing many candidates. Apriori is easy to explain and implement, but candidate generation and repeated database scans can become expensive. It remains essential for exams because it explains the logic used by later methods and many optimizations.

## Explanation

### 1. Input and output

The input is a transaction database \(D\), its itemset \(I\), and minimum support \(s_{\min}\). The output is the set \(L\) of all frequent itemsets, grouped by size:

\[
L=L_1\cup L_2\cup\cdots\cup L_k.
\]

Here \(L_\ell\) contains all frequent \(\ell\)-itemsets. Candidate itemsets not known to be frequent are written \(C_\ell\).

### 2. The Apriori property

If \(X\not\subseteq Y\), then

\[
\operatorname{supp}(Y)\le \operatorname{supp}(X).
\]

Because transactions containing \(Y\) must also contain \(X\). Therefore:

> If an itemset is infrequent, every immediate or distant superset is infrequent.

Example: if \(\{A,D\}\) occurs in only 2 of 10 transactions, a candidate such as \(\{A,B,D\}\) cannot occur more than twice and need not be tested. This is **downward closure** of the frequent-itemset family.

The converse is false. A frequent set can have infrequent subsets. If \(\{A,B,C\}\) occurs in six transactions, each pair within it occurs in at least those six transactions.

### 3. Algorithm structure

At level \(k\), Apriori performs:

1. **Join:** combine frequent \((k-1)\)-itemsets to create \(k\)-itemset candidates.
2. **Prune:** remove candidates containing an infrequent \((k-1)\)-subset.
3. **Support count:** scan transactions and retain candidates reaching \(s_{\min}\).
4. Repeat while \(L_k\neq\varnothing\).

The highest useful size is the largest \(k\) for which \(L_k\) is nonempty. A database cannot support more items than its longest transaction.

### 4. Candidate generation by self-join

For ordered \(k\)-itemsets \(X=\{x_1,\ldots,x_k\}\) and \(Y=\{y_1,\ldots,y_k\}\), their join contains \(X\cup Y\) when the first \(k-1\) elements agree:

\[
x_1=y_1,\ldots,x_{k-1}=y_{k-1},
\]

and \(x_k\neq y_k\). Sorting items makes duplicate generation manageable. A generated set is the union of two distinct \((k-1)\)-itemsets whose first \(k-1\) items are equal.

After joining, each candidate's subsets of size \(k-1\) are formed. The candidate is pruned if any such subset is not in \(L_{k-1}\).

### 5. First iteration

Apriori begins with a full scan to count each individual item. The candidates are all 1-itemsets \(C_1=I\). Items below threshold are discarded to form \(L_1\). An infrequent item can be removed permanently because every larger set containing it is infrequent.

### 6. Support counting

For each transaction \(T_j\), only candidate itemsets that are subsets of \(T_j\) can receive a count. Naive Apriori may test every candidate against every transaction. Hash-based variants index candidates in buckets so that a transaction probes only a small number of candidates. Counts, not another database pass per item, determine frequent sets at a level.

### 7. Termination and correctness

If \(C_{k+1}\) is empty, the algorithm stops. If every candidate at a level is pruned, later levels cannot contain a frequent itemset, so it also stops. Completeness follows because every frequent \(k\)-itemset is made of frequent \((k-1)\)-itemsets; the join exposes it and pruning never removes it.

### 8. Cost and limitations

- Candidate growth is combinatorial. Even after pruning, dense data can produce many itemsets.
- Each level normally requires a database scan.
- Traditional support counting has memory cost for candidate hashes.
- A single minimum support can make long, infrequent patterns impossible to find.
- Apriori is a good baseline, but FP-growth avoids repeated full scans for typical transaction data.

The common optimizations are developed in the file on improvements to Apriori.

## Worked examples

### Example 1: Complete Apriori run

Database:

| Transaction | Items |
|---|---|
| \(T_1\) | A, B, C |
| \(T_2\) | A, C |
| \(T_3\) | A, B, D |
| \(T_4\) | B, C, D |
| \(T_5\) | A, B, C, D |
| \(T_6\) | B, C |

Use \(\operatorname{minsup}=3\) transactions.

#### Pass \(L_1\)

| Item | Count | Frequent? |
|---|---:|---|
| A | 4 | yes |
| B | 5 | yes |
| C | 5 | yes |
| D | 3 | yes |

Thus \(L_1=\{A,B,C,D\}\).

#### Generate \(C_2\) and prune

Self-join produces all six pairs:

\[
C_2=\{AB,AC,AD,BC,BD,CD\}.
\]

There is no 1-item subset to prune at this level. Count the pairs:

| Candidate | Transactions | Count | Result |
|---|---|---:|---|
| AB | 1, 3, 5 | 3 | frequent |
| AC | 1, 2, 5 | 3 | frequent |
| AD | 3, 5 | 2 | infrequent |
| BC | 1, 4, 5, 6 | 4 | frequent |
| BD | 3, 4, 5 | 3 | frequent |
| CD | 4, 5 | 2 | infrequent |

Therefore,

\[
L_2=\{AB,AC,BC,BD\}.
\]

#### Generate \(C_3\)

Join the frequent pairs that share their first item:

\[
C_3=\{ABC,ABD,BCD\}.
\]

Now prune:

- \(ABC\) has frequent subsets \(AB\) and \(BC\): retain.
- \(ABD\) contains infrequent \(AD\): prune.
- \(BCD\) contains infrequent \(CD\): prune.

Only \(ABC\) remains. Its count is 2 (\(T_1,T_5\)), so it is below minimum support. Thus \(L_3=\varnothing\), and the final result is

\[
L_1\cup L_2.
\]

Notice that \(AD\) and \(CD\) were removed after support counting at level 2, preventing four larger candidates from being tested.

### Example 2: Candidate generation and pruning by hand

Suppose \(L_2=\{AB,AC,BC,BD\}\).

Self-join gives:

- \(AB\cup AC=ABC\)
- \(AB\cup BC=ABC\) again
- \(AB\cup BD=ABD\)
- \(AC\cup BC=ABC\) again
- \(BC\cup BD=BCD\)

After duplicate removal,

\[
C_3=\{ABC,ABD,BCD\}.
\]

If \(AD\notin L_2\), then \(ABD\) is pruned. If \(CD\notin L_2\), then \(BCD\) is pruned. This is why a direct enumeration of all triples is unnecessary.

### Example 3: Pseudocode trace

```text
L1 = frequent_1_itemsets(D, smin)
for k = 2 while L(k-1) is not empty:
    Ck = join(L(k-1), L(k-1))
    Ck = prune(Ck, L(k-1))
    for transaction t in D:
        for c in Ck such that c is a subset of t:
            count[c] += 1
    Lk = {c in Ck : count[c] >= smin}
return union of all Lk
```

For the example above, the loops produce `L1={A,B,C,D}`, `C2={AB,AC,AD,BC,BD,CD}`, `L2={AB,AC,BC,BD}`, `C3={ABC}`, and then stop because `L3` is empty.

## Key terms & formulas

- **Candidate set \(C_k\):** tested \(k\)-itemsets at level \(k\).
- **Frequent set \(L_k\):** candidates meeting minimum support.
- **Apriori property:** \(X\subseteq Y\Rightarrow\operatorname{supp}(X)\ge\operatorname{supp}(Y)\).
- **Downward closure:** all subsets of a frequent itemset are frequent.
- **Pruning:** removing a candidate known to be infrequent.
- **Self-join:** generate the next itemset level from the current frequent level.
- **Join condition:** equal first \(k-1\) items, different final items.
- **Support threshold:** \(\operatorname{count}(X)\ge s_{\min}\).
- **Pass:** one candidate-generation and support-counting cycle at a fixed size.
- **Naive candidate bound:** \(\sum_{i=1}^{m}\binom{m}{i}=2^m-1\) nonempty itemsets.

## Common mistakes

1. **Calling infrequent items “dead” in only one level:** they are dead for all supersets, not just the next size.
2. **Confusing join and prune:** joining proposes candidates; pruning only removes candidates with known infrequent subsets.
3. **Pruning before support count using a candidate set:** the check is against frequent previous-level sets \(L_{k-1}\), not against current candidates \(C_k\).
4. **Counting item occurrences rather than containing transactions:** one transaction contributes at most one to a given itemset.
5. **Continuing after \(L_k=\varnothing\):** no larger frequent itemset can exist.
6. **Assuming Apriori generates rules:** its output is frequent itemsets; rules are a separate step.

## Exam prep

**Likely 2-mark questions**
1. State and explain the Apriori property. *Hint: every subset of a frequent itemset is frequent.*
2. Name the two main steps at each level. *Hint: candidate generation by join and pruning; support counting.*
3. Why can Apriori stop when \(L_k\) is empty? *Hint: no larger set can then be frequent.*

**Likely long-answer questions**
1. Explain Apriori with candidate generation, pruning, support counting, termination, and complexity. *Hint: write the \(C_k/L_k\) loop and explain downward closure.*
2. Run Apriori level by level on a supplied transaction table. *Hint: list every \(C_k\), show counts, then show exactly which candidates are pruned.*
3. Compare Apriori with FP-growth in candidate generation and database access. *Hint: repeated levels and scans versus constructing and mining an FP-tree.*
4. Prove that pruning cannot remove a frequent itemset. *Hint: an infrequent subset has support below the threshold, so no superset can be frequent.*
