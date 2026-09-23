---
subject: sc
unit: 1
topic: crisp-set-theory
syllabus_ref: CSM3202 Unit-I
status: draft
---
# Crisp Set Theory

## Overview

Crisp—or classical—set theory studies sets whose members either belong or do not belong. Membership is binary: \(1\) means “in the set,” and \(0\) means “out.” This is the mathematical foundation used by databases, Boolean logic, rule systems, and ordinary computer control.

The idea seems simple, but its boundaries matter. A crisp set is appropriate when membership is clear—for example, the set of even integers. It becomes debatable when a boundary is gradual, such as the set of “tall people.” Fuzzy sets later extend the same basic notation by allowing every membership value to lie between 0 and 1.

## Explanation

### 1. Universal set

Let \(X\) be the collection of all objects under discussion. It is called the **universal set** or **universe**, and it is written

\[
X=\{x_1,x_2,\ldots,x_n\}.
\]

Every set in the problem is described relative to this universe. If a problem concerns the days of a week,

\[
X=\{\text{Monday},\text{Tuesday},\ldots,\text{Sunday}\}.
\]

A smaller set \(A\subseteq X\) selects some of these objects. The choice of universe is important: a person may belong to the universe of “registered voters” but not to the universe of “current students.” Changing the universe changes the membership question.

For a finite universe,

\[
|X|=n
\]

is the number of elements in \(X\), also called its cardinality.

### 2. Definition of a crisp set

A set \(A\) is a collection \(A\subseteq X\) of distinct objects such that each \(x\in X\) satisfies exactly one of two conditions:

\[
x\in A \quad\text{or}\quad x\notin A.
\]

The characteristic (or membership) function of \(A\) is

\[
\mu_A(x)=
\begin{cases}
1,&x\in A,\\
0,&x\notin A.
\end{cases}
\]

Thus a crisp set may be represented as

\[
A=\{(x,\mu_A(x)):x\in X\}.
\]

For example, with

\[
X=\{1,2,3,4,5\}
\]

and \(A=\{2,4\}\),

\[
\mu_A(1)=0,\quad\mu_A(2)=1,\quad\mu_A(3)=0,\quad\mu_A(4)=1,\quad\mu_A(5)=0.
\]

### 3. Roster, set-builder, and membership-vector forms

The same crisp set can be written in several ways.

- **Roster form:** list every element: \(A=\{2,4\}\).
- **Set-builder form:** state a property: \(A=\{x\in X:x\text{ is even}\}\).
- **Membership vector:** for ordered \(X=\{1,2,3,4,5\}\), write \(A=[0,1,0,1,0]\).

A characteristic (binary) matrix uses the same idea for a crisp relation: rows describe elements of the first universe and columns describe elements of the second universe.

### 4. Equality, inclusion, and strict inclusion

Two sets are equal if they contain exactly the same elements:

\[
A=B \iff (x\in A\Leftrightarrow x\in B)
\]

for every \(x\in X\).

A set \(A\) is a subset of \(B\) if every member of \(A\) is also in \(B\):

\[
A\subseteq B \iff \forall x,\ x\in A\Rightarrow x\in B.
\]

It is a proper subset if \(A\subseteq B\) but \(A\ne B\):

\[
A\subsetneq B.
\]

A necessary but not sufficient condition for \(A\subseteq B\) is \(|A|\le|B|\). Equal cardinalities do not prove inclusion because elements may differ.

### 5. Empty set and universal set

The **empty set** contains no elements:

\[
\varnothing=\{\}.
\]

Its membership is zero for every element in the universe. The universal set contains every permitted object:

\[
\mu_X(x)=1 \quad \forall x\in X.
\]

For every \(A\subseteq X\),

\[
A\cup X=X,\qquad A\cap X=A,\qquad X^c=\varnothing,\qquad \varnothing^c=X.
\]

### 6. Power set

The family of all subsets of \(X\) is the **power set**, written

\[
\mathcal P(X).
\]

If \(|X|=n\), then

\[
|\mathcal P(X)|=2^n.
\]

For \(X=\{a,b\}\),

\[
\mathcal P(X)=\{\varnothing,\{a\},\{b\},\{a,b\}\}.
\]

The power set grows quickly. A universe of 20 elements has \(2^{20}=1{,}048{,}576\) subsets. This combinatorial explosion is one reason exhaustive search is not feasible in many problems.

### 7. Operations on crisp sets

The principal operations are described fully in the companion note on crisp-set operations:

\[
\begin{aligned}
A\cup B &= \text{at least one of }x\in A,\ x\in B,\\
A\cap B &= \text{both }x\in A\text{ and }x\in B,\\
A^c &= \text{all }x\in X\text{ not in }A.
\end{aligned}
\]

Equality can be tested by \(A=B\) or \(A=B^c\) depending on the question. The identity, domination, and distributive laws include

\[
A\cup\varnothing=A,\quad A\cap X=A,\quad
A\cup(A\cap B)=A,\quad A\cap(A\cup B)=A.
\]

Complement obeys involution and De Morgan's laws:

\[
(A^c)^c=A,
\qquad
(A\cup B)^c=A^c\cap B^c,
\qquad
(A\cap B)^c=A^c\cup B^c.
\]

### 8. Cartesian product

The Cartesian product of two universes is

\[
A\times B=\{(a,b):a\in A,\ b\in B\}.
\]

If \(|A|=m\) and \(|B|=n\), then

\[
|A\times B|=mn.
\]

This construction underlies crisp relations between different sets.

### 9. Why crisp membership matters

A crisp boundary gives an exact and easily verified answer. It is suitable when the distinction is natural, such as whether a transaction was accepted, whether a file exists, or whether an integer is divisible by 3.

The weakness is not the mathematics; it is the assumption that the chosen boundary is meaningful. If the task is genuinely gradual, forcing each observation into 0 or 1 discards useful information. Fuzzy-set theory retains the same universe and operations but permits partial membership.

## Worked examples

### Example 1: Membership values and set equality

Let

\[
X=\{a,b,c,d,e\}
\]

and

\[
A=\{a,c,e\},\qquad B=\{a,c,e,f\}.
\]

A membership vector is possible only when elements are listed against the same universe. Add \(f\) and use \(X'=\{a,b,c,d,e,f\}\):

\[
A=[1,0,1,0,1,0],\qquad B=[1,0,1,0,1,1].
\]

Therefore \(A\ne B\). Also \(A\subsetneq B\), and \(|A|=3\), \(|B|=4\).

### Example 2: Operations

For the same sets,

\[
A\cup B=\{a,c,e,f\},
\]

\[
A\cap B=\{a,c,e\},
\]

and relative to \(X'\),

\[
A^c=\{b,d,f\},\qquad
B^c=\{b,d\}.
\]

Check De Morgan's law:

\[
(A\cup B)^c=\{b,d\}.
\]

Also,

\[
A^c\cap B^c=\{b,d,f\}\cap\{b,d\}=\{b,d\},
\]

so \((A\cup B)^c=A^c\cap B^c\).

### Example 3: Power-set count

For \(X=\{1,2,3\}\), the subsets are

\[
\varnothing,\{1\},\{2\},\{3\},\{1,2\},\{1,3\},\{2,3\},\{1,2,3\}.
\]

There are \(2^3=8\) subsets. The complement pairs are

\[
(\varnothing,X),\quad
(\{1\},\{2,3\}),\quad
(\{2\},\{1,3\}),\quad
(\{3\},\{1,2\}).
\]

### Example 4: Cartesian product

For \(A=\{1,2\}\) and \(B=\{x,y\}\),

\[
A\times B=
\{(1,x),(1,y),(2,x),(2,y)\}.
\]

It has \(2\times2=4\) ordered pairs. Notice that \((x,1)\) is not in \(A\times B\); Cartesian products preserve order.

## Key terms & formulas

- **Universe \(X\):** The complete set of permitted objects.
- **Crisp set \(A\):** A subset of \(X\) with binary membership.
- **Characteristic function:** \(\mu_A(x)\in\{0,1\}\).
- **Cardinality:** \(|A|\), the number of elements in a finite set.
- **Subset:** \(A\subseteq B\).
- **Proper subset:** \(A\subsetneq B\).
- **Power set:** \(\mathcal P(X)=\{A:A\subseteq X\}\).
- **Cardinality of power set:** \(|\mathcal P(X)|=2^{|X|}\).
- **Cartesian product:** \(A\times B=\{(a,b):a\in A,b\in B\}\).

Key laws:

\[
|A\cup B|=|A|+|B|-|A\cap B|
\]

for finite sets, and

\[
A\cup(A\cap B)=A,\quad
A\cap(A\cup B)=A,\quad
(A\cup B)^c=A^c\cap B^c.
\]

## Common mistakes

1. **Using membership \(0.5\) in a crisp set.** Crisp membership is only 0 or 1; \(0.5\) belongs to fuzzy-set notation.
2. **Ignoring the universe.** “Everything else” in a complement means everything else in the stated \(X\).
3. **Confusing subset with proper subset.** \(A\subseteq A\), but \(A\subsetneq A\) is false.
4. **Assuming equal size proves inclusion.** Two sets can have three different elements.
5. **Using \(|A|>|B|\) to infer \(A\nsubseteq B\).** It correctly proves that \(B\subseteq A\) is impossible, not that \(A\subseteq B\) is impossible.
6. **Swapping Cartesian-product order.** \(A\times B\) is not generally the same set as \(B\times A\).
7. **Confusing complement relative to an object with complement relative to the universe.** Always use \(A^c\subseteq X\).

## Exam prep

### Likely 2-mark questions

- **Define a crisp set with its membership function.**  
  **Hint:** A subset \(A\subseteq X\) for which every element receives membership 0 or 1.

- **What is a universal set?**  
  **Hint:** The complete collection of all permitted elements under consideration.

- **State the cardinality of a power set.**  
  **Hint:** If \(|X|=n\), then \(|\mathcal P(X)|=2^n\).

- **Write De Morgan's laws.**  
  **Hint:** \((A\cup B)^c=A^c\cap B^c\) and \((A\cap B)^c=A^c\cup B^c\).

- **When is a crisp set preferable to a fuzzy set?**  
  **Hint:** When membership is naturally binary and exact.

### Likely long-answer questions

- **Explain crisp set theory with notation and different set representations.**  
  **Hint:** Universe, definition, characteristic function, roster/set-builder/vector forms, and cardinality.

- **Describe set equality, inclusion, complement, power set, and Cartesian product.**  
  **Hint:** Define each operation and include one simple calculation.

- **Compare crisp and fuzzy representation of membership.**  
  **Hint:** Use the same universe, show binary versus graded membership, and explain when the crisp assumption fails.

- **Prove the power-set formula for a finite set.**  
  **Hint:** Give each of \(n\) elements two choices—include or exclude—so there are \(2^n\) subsets.
