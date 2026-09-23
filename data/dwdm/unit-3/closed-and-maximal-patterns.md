---
subject: dwdm
unit: 3
topic: closed-and-maximal-patterns
syllabus_ref: CSM3101 Unit-III
status: draft
---
# Closed and Maximal Frequent Patterns

## Overview

A database may contain many overlapping frequent itemsets. **Maximal frequent itemsets** are frequent sets that cannot be enlarged while staying frequent. **Closed frequent itemsets** are frequent sets for which no immediate superset has exactly the same support. These concepts reduce redundancy and change how a frequent-pattern family is represented. They are not synonyms, and neither concept means “the itemset with the most items.”

## Explanation

### 1. Maximal frequent itemset

An itemset \(I\) is **maximal frequent** if:

1. \(\operatorname{supp}(I)\ge s_{\min}\); and
2. no proper superset \(J\supset I\) is frequent.

A maximal set can be pruned during search once discovered because none of its descendants can be frequent. Every maximal itemset is closed, but a closed itemset need not be maximal.

### 2. Closed frequent itemset

An itemset \(I\) is **closed** if it is frequent and no immediate superset has the same support:

\[
I\neq\emptyset,\quad
\operatorname{supp}(I)\ge s_{\min},\quad
\forall x\notin I,\quad
\operatorname{supp}(I\cup\{x\})<\operatorname{supp}(I).
\]

Equivalently, no single item can be added without increasing support. Closure captures a property of exact support, not merely the threshold. A closed set can be frequent while some extension is infrequent, so the total-support constraint \(T(I)\ge s_{\min}\) is not enough to make it closed.

### 3. \(T\)-items and \(T\)-closures

The **\(T\)-itemset** (or tidset) of \(I\) is the set of all items that occur in every transaction containing \(I\):

\[
T(I)=\bigcap_{T_j\supseteq I} T_j.
\]

The **\(T\)-closure** is

\[
\operatorname{cl}(I)=I\cup T(I).
\]

Every item in \(T(I)\) can be added to \(I\) without reducing support. Thus \(I\) is closed exactly when \(\operatorname{cl}(I)=I\). This provides a practical way to recognize closure from a transaction subset.

### 4. Why these concepts matter

The set of closed frequent itemsets determines the entire frequent family. If \(X\) is frequent, repeatedly adding common items until no more can be added eventually reaches a closed frequent itemset containing \(X\). Closed itemsets therefore provide a compact representation, while maximal itemsets are useful when only the largest frequent combinations matter.

They can simplify mining and presentation, but neither is automatically an actionable association rule. A very large closed set may be difficult to deploy, and rules still need confidence and correlation analysis.

### 5. Important distinctions

- **Frequent:** passes minimum support.
- **Maximal frequent:** no frequent proper superset.
- **Closed frequent:** no immediate superset with equal support.
- **Maximum-size frequent itemset:** a frequent itemset with the greatest cardinality. It is necessarily maximal, but maximality itself imposes no size requirement.

A set can be maximal because every extension fails the threshold, but not because every extension increases support. Conversely, an itemset can be non-maximal but closed if extensions are frequent with equal support.

## Worked examples

### Example 1: Simple database

Transactions:

| ID | Items |
|---|---|
| 1 | A, B, C |
| 2 | A, B, C |
| 3 | A, B |
| 4 | A, D |

Use \(s_{\min}=2\).

Supports:

| Itemset | Support | Closed? | Maximal frequent? |
|---|---:|---|---|
| A | 4 | yes | no |
| B | 3 | no: \(AB\) has equal support | no |
| C | 2 | no: \(AC\) has equal support | no |
| D | 1 | not frequent | no |
| AB | 3 | yes | no: \(ABC\) is frequent |
| AC | 2 | no: \(ABC\) has equal support | no |
| BC | 2 | no: \(ABC\) has equal support | no |
| ABC | 2 | yes | yes |
| AD | 1 | not frequent | no |

For example, \(AB\) is closed because every immediate extension has lower support, but it is not maximal because \(ABC\) is frequent. \(ABC\) is both closed and maximal. Item \(A\) is also closed: its extensions \(AB, AC,\) and \(AD\) all reduce its support, even though a lower-support extension can still be frequent.

The closed frequent itemsets are \(A\), \(AB\), and \(ABC\); the only maximal frequent itemset is \(ABC\).

### Example 2: Closed but not maximal

In a database with four transactions `ABC`, `ABC`, `ABC`, `AC`, and threshold 3, \(AB\) has support 3 and \(ABC\) has support 3. Since adding C does not reduce support, AB is closed. Yet ABC is also frequent, so AB is not maximal. This is the canonical distinction.

### Example 3: Maximal but not closed

Let the transactions be `AB`, `AC`, and `BC`, with threshold 2. The pairs \(AB\), \(AC\), and \(BC\) each have support 2. They are maximal because the only immediate extensions are the full set \(ABC\), whose support is 1 and is therefore infrequent. They are not closed: for example, extending \(AB\) with C gives \(AC\), also support 2, so closure is violated. This pair of examples shows why maximality and closedness are genuinely different tests.

### Example 4: Compute a closure

Let the transactions containing \(\{A\}\) be `ABD`, `ACD`, and `ABD`. The intersection is \(\{A,B,D\}\), so

\[
T(\{A\})=\{A,B,D\},\qquad \operatorname{cl}(\{A\})=\{A,B,D\}.
\]

A alone is not closed; ABD is the closed representative. If the database also has `ABCD`, the intersection becomes ABCD and the closure extends again.

## Key terms & formulas

- **Frequent:** \(\operatorname{supp}(I)\ge s_{\min}\).
- **Maximal frequent:** no proper frequent superset.
- **Closed frequent:** \(\operatorname{supp}(I)>\operatorname{supp}(I\cup\{x\})\) for every \(x\notin I\).
- **\(T\)-itemset:** intersection of all transactions containing \(I\).
- **\(T\)-closure:** \(I\cup T(I)\).
- **Immediate superset:** \(I\cup\{x\}\) for one new item.
- **Proper superset:** any set containing \(I\) and at least one extra item.
- **Closed-pattern representation:** closed itemsets determine all frequent itemsets through repeated closure.

## Common mistakes

1. **Equating maximal and closed:** a closed itemset may have a frequent strict superset with lower support.
2. **Equating maximal and maximum cardinality:** maximal means no frequent extension, not “largest by size.”
3. **Checking only the final itemset size:** closure is about support equality of immediate extensions.
4. **Forgetting frequency:** a nonfrequent set is not called a closed *frequent* pattern.
5. **Dropping the intersection item itself:** \(T(I)\) includes items from the paths; the closure is \(I\cup T(I)\).

## Exam prep

**Likely 2-mark questions**
1. Define a closed frequent itemset. *Hint: frequent and no immediate superset has equal support.*
2. Define a maximal frequent itemset. *Hint: frequent and no proper superset is frequent.*
3. What is the \(T\)-closure of an itemset? *Hint: the itemset plus all items common to every transaction containing it.*

**Likely long-answer questions**
1. Compare closed and maximal frequent itemsets with a transaction example. *Hint: show one closed non-maximal set and explain support equality versus threshold.*
2. Prove that every maximal frequent itemset is closed. *Hint: a frequent proper superset would contradict maximality.*
3. Explain how \(T\)-items reduce the frequent family. *Hint: intersect containing transactions, take closures, and recover all frequent subsets.*
