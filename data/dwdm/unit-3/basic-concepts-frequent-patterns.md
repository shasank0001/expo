---
subject: dwdm
unit: 3
topic: basic-concepts-frequent-patterns
syllabus_ref: CSM3101 Unit-III
status: draft
---
# Basic Concepts of Frequent Pattern and Association Mining

## Overview

Frequent-pattern mining searches large transaction databases for groups of items that occur together more often than expected. It matters because the result is not just “people buy bread”; the result can be a quantified rule such as “customers who buy bread and butter often also buy jam.” A supermarket, bank, website, or hospital can use such patterns for shelf placement, cross-selling, bundling, and targeted services.

The usual transaction-mining model has two parts: **frequent-itemset mining**, which finds sets whose support passes a threshold, and **association-rule mining**, which turns useful frequent sets into directional rules. Frequent sets are the costly part; a large database can produce far too many candidates, so the Apriori and FP-growth methods in later notes solve this search problem differently.

## Explanation

### 1. Transaction data

A transaction database \(D=\{T_1,T_2,\ldots,T_m\}\) contains transactions, each representing one event such as a shopping basket. An item is one detail, for example `bread`. An **itemset** is any set of items; it may contain one item, two items, or many. Transaction \(T_3=\{A,B,D\}\) contains the 1-itemsets \(\{A\},\{B\},\{D\}\), three 2-itemsets, and one 3-itemset.

The number of possible itemsets is exponential. With 20 distinct items there are \(2^{20}\) subsets, so even a modest catalog creates too many candidates to test naively. Frequent-pattern algorithms use support constraints and the structure of itemsets to reduce the search.

### 2. Support and minimum support

The **support** of an itemset \(X\) is the fraction of transactions containing every item in \(X\):

\[
\operatorname{supp}(X)=\frac{\text{number of transactions containing }X}{|D|}.
\]

A user supplies **minimum support**, \(\operatorname{minsup}\), often as a percentage. An itemset is **frequent** when

\[
\operatorname{supp}(X)\ge \operatorname{minsup}.
\]

If the database has 1,000 transactions and \(\operatorname{minsup}=5\%\), an itemset must appear in at least 50 transactions. A fixed transaction count is often called **absolute support**. The choice of minimum support is a business and modeling decision: a high value returns fewer, broader patterns; a low value returns many detailed patterns but increases computation and the risk of accidental, useless rules.

### 3. From frequent itemsets to association rules

An association rule \(A\rightarrow B\) says that transactions containing \(A\) tend to contain \(B\). It has:

\[
\operatorname{conf}(A\rightarrow B)=
\frac{\operatorname{supp}(A\cup B)}{\operatorname{supp}(A)},
\]

where \(A\) is the **antecedent** and \(B\) the **consequent**. Every frequent itemset can produce \(2^{|X|}-2\) nonempty, distinct rules. Pattern evaluation is still required because frequent does not automatically mean useful.

### 4. Correlations and unusual patterns

A rule can be frequent but not informative. If 80% of all transactions contain bread and 75% contain bread and butter, bread implies butter with 93.75% confidence, but only 2.5 percentage points above buying butter by itself. This motivates **correlation measures** such as lift:

\[
\operatorname{lift}(A\rightarrow B)=
\frac{\operatorname{supp}(A\cup B)}
{\operatorname{supp}(A)\operatorname{supp}(B)}.
\]

Lift near 1 suggests little association, above 1 a positive association, and below 1 a negative association. Negative association may also be useful, although ordinary minimum-support mining will not discover it. Pattern evaluation is covered fully in a later file.

### 5. Other frequent-pattern settings

The same idea changes form with the data. Horizontal itemsets contain items only. **Multilevel itemsets** allow an item at a detail level, such as `Dell laptop`, to be related to broader concepts such as `laptop` or `electronics`. **Multidimensional itemsets** are selected with conditions over other dimensions, such as time, location, or customer segment. Sequential patterns add order, while graph patterns represent connected objects and relationships. The core support definition remains the frequency of simultaneous occurrence unless the task explicitly adds order or connectivity.

### 6. General mining workflow

1. Choose transactions, item encoding, and a meaningful minimum support.
2. Count 1-itemsets and discard infrequent items.
3. Generate and test larger candidates efficiently.
4. Retain frequent itemsets.
5. Generate rules and rank them with confidence, lift, leverage, conviction, or another measure.
6. Validate patterns on separate or later-period data before deployment.

## Worked examples

### Example 1: Count support

| Transaction | Items |
|---|---|
| \(T_1\) | A, B, C |
| \(T_2\) | A, C |
| \(T_3\) | A, B, D |
| \(T_4\) | B, C, D |
| \(T_5\) | A, B, C, D |
| \(T_6\) | B, C |

For \(\operatorname{supp}(\{A,C\})\), scan the transactions:

- \(T_1\): yes
- \(T_2\): yes
- \(T_3\): no D? A exists but C does not, so no
- \(T_4\): A missing, no
- \(T_5\): yes
- \(T_6\): A missing, no

Thus the count is 3 and \(\operatorname{supp}(\{A,C\})=3/6=0.50\). If \(\operatorname{minsup}=0.40\), the set is frequent.

### Example 2: Interpret a rule

Suppose 200 transactions contain U, 160 contain both U and V, and 120 contain V. Then

\[
\operatorname{supp}(U)=200/1000=0.20,
\]
\[
\operatorname{supp}(U\cup V)=160/1000=0.16,
\]
\[
\operatorname{conf}(U\rightarrow V)=0.16/0.20=0.80,
\]
\[
\operatorname{lift}(U\rightarrow V)=\frac{0.16}{0.20(0.12)}=6.67.
\]

Customers who buy U are much more likely than average to buy V. The rule is quantitatively interesting, but an explanation and an out-of-sample test are still required before treating it as a business cause.

### Example 3: Choose minimum support

For 10,000 sessions, \(s_{\min}=1\%\) requires 100 containing transactions. Raising it to \(5\%\) requires 500. The higher threshold will discard niche combinations, reduce candidate generation, and make discovered rules more stable across samples. A useful workflow is to run several thresholds and record how many itemsets and nontrivial rules remain.

## Key terms & formulas

- **Transaction:** one basket, session, or event.
- **Item:** one detail in a transaction.
- **Itemset \(X\):** a set of items.
- **Absolute support:** number of transactions containing \(X\).
- **Relative support:** \(c(X)/|D|\).
- **Frequent itemset:** support at least \(\operatorname{minsup}\).
- **Association rule \(A\rightarrow B\):** an implication evaluated with confidence and correlation.
- **Search space:** all \(2^m\) itemsets for \(m\) distinct items, absent pruning.
- **Maximum possible itemsets:** \(2^m-1\) nonempty sets.
- **Problem settings:** k-itemsets, frequent closed itemsets, maximal itemsets, association, correlation, classification, clustering, and sequential patterns.

## Common mistakes

1. **Confusing occurrence count with support:** 60 occurrences out of 1,000 transactions is support \(0.06\), not 60.
2. **Treating frequent as useful:** a rare consequent can make confidence high even when lift is near 1.
3. **Ignoring sparse data:** many items and a low threshold can make candidate generation infeasible.
4. **Using one threshold blindly:** support is relative to database size; compare absolute counts when datasets differ.
5. **Reversing a rule casually:** \(A\rightarrow B\) and \(B\rightarrow A\) have the same joint support but different confidence.
6. **Claiming causation:** association describes co-occurrence; it does not prove that \(A\) causes customers to buy \(B\).

## Exam prep

**Likely 2-mark questions**
1. Define an itemset and support. *Hint: a set of items; fraction of transactions containing every item.*
2. Differentiate a frequent itemset from an interesting association rule. *Hint: threshold crossing versus usefulness/confidence/correlation.*
3. State the benefit of the minimum-support threshold. *Hint: it prunes the exponential search space.*

**Likely long-answer questions**
1. Explain frequent-itemset and association-rule mining, including support, confidence, lift, and a complete example. *Hint: transaction model → candidate generation → threshold → rules → correlation.*
2. Describe how data type changes frequent-pattern mining at multiple levels and dimensions. *Hint: detail hierarchies plus independent attributes and constraints.*
3. Compare the cost and output of a naive itemset search with a support-pruning method. *Hint: \(2^m\) subsets versus repeated frequent-pattern algorithms.*
