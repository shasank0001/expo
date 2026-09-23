---
subject: sc
unit: 1
topic: crisp-set-operations
syllabus_ref: CSM3202 Unit-I
status: draft
---
# Crisp Set Operations

## Overview

Crisp set operations build larger or smaller sets from existing crisp sets. They are used to combine alternatives, find common members, remove alternatives, and describe the complement. The operations are exact: every element is either present or absent.

The most important operations are union, intersection, complement, and difference. They obey algebraic laws and can be represented with membership vectors or Venn diagrams. These operations also provide a baseline for the fuzzy-set operations covered later in Unit I.

## Explanation

### 1. Setup

Let the universe be

\[
X=\{1,2,3,4,5,6\}
\]

and let

\[
A=\{1,2,4\},\qquad B=\{3,4,5,6\}.
\]

Every operation is interpreted relative to \(X\).

### 2. Union

The union contains every element that belongs to at least one set:

\[
A\cup B=\{x:x\in A\text{ or }x\in B\}.
\]

Thus

\[
A\cup B=\{1,2,3,4,5,6\}=X.
\]

In membership notation, Boolean OR is used:

\[
\mu_{A\cup B}(x)=
\begin{cases}
1,&\mu_A(x)=1\text{ or }\mu_B(x)=1,\\
0,&\text{otherwise}.
\end{cases}
\]

Equivalently,

\[
\mu_{A\cup B}(x)=\max(\mu_A(x),\mu_B(x))
\]

for binary crisp memberships.

### 3. Intersection

The intersection contains only elements common to both sets:

\[
A\cap B=\{x:x\in A\text{ and }x\in B\}.
\]

Therefore,

\[
A\cap B=\{4\}.
\]

Membership notation uses Boolean AND:

\[
\mu_{A\cap B}(x)=
\begin{cases}
1,&\mu_A(x)=1\text{ and }\mu_B(x)=1,\\
0,&\text{otherwise}.
\end{cases}
\]

For binary memberships,

\[
\mu_{A\cap B}(x)=\min(\mu_A(x),\mu_B(x)).
\]

### 4. Complement

The complement of \(A\) contains the elements of \(X\) that do not belong to \(A\):

\[
A^c=X\setminus A.
\]

Hence,

\[
A^c=\{3,5,6\}.
\]

Complement toggles membership:

\[
\mu_{A^c}(x)=1-\mu_A(x).
\]

Because the universe matters, \(A^c\) is always interpreted relative to \(X\).

### 5. Difference

The difference \(A-B\) contains elements in \(A\) but not in \(B\):

\[
A-B=A\cap B^c.
\]

For the example,

\[
A-B=\{1,2\}.
\]

The reverse difference is

\[
B-A=B\cap A^c=\{3,5,6\}.
\]

Unlike complement, \(A-B\) is not relative to the whole universe; it only removes the members of \(B\) from \(A\).

### 6. Symmetric difference

The symmetric difference contains elements in exactly one of \(A\) or \(B\), not both:

\[
A\triangle B=(A-B)\cup(B-A)
=(A\cup B)-(A\cap B).
\]

Thus,

\[
A\triangle B=\{1,2,3,5,6\}.
\]

### 7. Cartesian product

For two sets, possibly from different universes,

\[
A\times B=\{(a,b):a\in A,\ b\in B\}.
\]

Here,

\[
A\times B=
\{(1,3),(1,4),(1,5),(1,6),(2,3),(2,4),(2,5),(2,6),(4,3),(4,4),(4,5),(4,6)\}.
\]

There are \(3\times4=12\) ordered pairs.

### 8. Identities, domination, and hierarchy

The universal and empty sets obey:

\[
A\cup\varnothing=A,\qquad A\cap\varnothing=\varnothing,
\]

\[
A\cup X=X,\qquad A\cap X=A.
\]

If \(A\subseteq B\), then \(B\) dominates \(A\), and

\[
A\cap B=A,\qquad A\cup B=B.
\]

The disjointness condition is

\[
A\cap B=\varnothing.
\]

### 9. Algebraic laws

**Commutative laws**

\[
A\cup B=B\cup A,\qquad A\cap B=B\cap A.
\]

**Associative laws**

\[
(A\cup B)\cup C=A\cup(B\cup C),
\]

\[
(A\cap B)\cap C=A\cap(B\cap C).
\]

**Distributive laws**

\[
A\cap(B\cup C)=(A\cap B)\cup(A\cap C),
\]

\[
A\cup(B\cap C)=(A\cup B)\cap(A\cup C).
\]

**Idempotent laws**

\[
A\cup A=A,\qquad A\cap A=A.
\]

**Complement laws**

\[
A\cup A^c=X,\qquad A\cap A^c=\varnothing,
\]

\[
(A^c)^c=A.
\]

**De Morgan's laws**

\[
(A\cup B)^c=A^c\cap B^c,
\]

\[
(A\cap B)^c=A^c\cup B^c.
\]

### 10. Operations using membership vectors

For the fixed order \(X=(1,2,3,4,5,6)\),

\[
\chi_A=[1,1,0,1,0,0],
\]

\[
\chi_B=[0,0,1,1,1,1].
\]

Boolean OR, AND, and NOT yield

\[
\chi_{A\cup B}=[1,1,1,1,1,1],
\]

\[
\chi_{A\cap B}=[0,0,0,1,0,0],
\]

\[
\chi_{A^c}=[0,0,1,0,1,1].
\]

Using max and min is valid here only because all values are binary.

## Worked examples

### Example 1: Calculate all basic operations

Using

\[
A=\{1,2,4\},\quad B=\{3,4,5,6\},\quad X=\{1,\ldots,6\},
\]

we obtain:

\[
A\cup B=\{1,2,3,4,5,6\},
\]

\[
A\cap B=\{4\},
\]

\[
A^c=\{3,5,6\},
\]

\[
A-B=\{1,2\},
\]

\[
B-A=\{3,5,6\},
\]

\[
A\triangle B=\{1,2,3,5,6\}.
\]

Notice that \(A\cup A^c=X\) and \(A\cap A^c=\varnothing\).

### Example 2: Verify distributivity

\[
A\cap(B\cup A)=\{1,2,4\}\cap X=A.
\]

On the other side,

\[
(A\cap B)\cup(A\cap A)=\{4\}\cup A=A.
\]

Therefore,

\[
A\cap(B\cup A)=(A\cap B)\cup(A\cap A).
\]

### Example 3: Cartesian product and projection

Let

\[
A=\{a,b\},\quad B=\{1,2,3\}.
\]

Then

\[
A\times B=\{(a,1),(a,2),(a,3),(b,1),(b,2),(b,3)\}.
\]

Projecting onto the first coordinate gives \(A\); projecting onto the second gives \(B\).

### Example 4: Selection with union and intersection

A system accepts a request if it is either from an approved customer set \(A\) or is marked urgent \(B\), but only for active requests \(C\):

\[
S=(A\cup B)\cap C.
\]

This compact expression combines alternatives with a necessary restriction. In Boolean code, the corresponding logic is `(A OR B) AND C`.

## Key terms & formulas

- **Union:** \(A\cup B\)
- **Intersection:** \(A\cap B\)
- **Complement:** \(A^c=X-A\)
- **Difference:** \(A-B=A\cap B^c\)
- **Symmetric difference:** \(A\triangle B=(A-B)\cup(B-A)\)
- **Disjoint sets:** \(A\cap B=\varnothing\)

For finite sets:

\[
|A\cup B|=|A|+|B|-|A\cap B|,
\]

\[
|A-B|=|A|-|A\cap B|,
\]

\[
|A\triangle B|=|A|+|B|-2|A\cap B|.
\]

For finite crisp sets represented on the same ordered universe:

\[
\chi_{A\cup B}=\chi_A\lor\chi_B,\quad
\chi_{A\cap B}=\chi_A\land\chi_B,\quad
\chi_{A^c}=\neg\chi_A.
\]

## Common mistakes

1. **Using complement without a fixed universe.** \(A^c\) contains all elements of \(X\setminus A\).
2. **Swapping difference and intersection.** \(A-B=A\cap B^c\), not \(A\cap B\).
3. **Confusing symmetric difference with union.** Common elements are excluded from \(A\triangle B\).
4. **Using \(\max\) and \(\min\) as if they were only fuzzy operators.** For crisp 0/1 vectors they are equivalent to Boolean OR/AND.
5. **Ignoring the order of Cartesian pairs.** \((a,b)\) and \((b,a)\) are different when the elements come from different universes.
6. **Applying finite cardinality formulas to infinite sets.** Those formulas assume finite sets.
7. **Forgetting double counting in the union formula.** Subtracting the intersection removes repeated elements.

## Exam prep

### Likely 2-mark questions

- **Define union and intersection of two crisp sets.**  
  **Hint:** Use “at least one of” and “both,” respectively.

- **State De Morgan's laws.**  
  **Hint:** Complement of union equals intersection of complements, and vice versa.

- **Write the relation between difference and complement.**  
  **Hint:** \(A-B=A\cap B^c\) and \(B-A=B\cap A^c\).

- **What is the symmetric difference of two sets?**  
  **Hint:** Elements belonging to exactly one of them.

### Likely long-answer questions

- **Explain the principal operations on crisp sets with formulas and an example.**  
  **Hint:** Union, intersection, complement, difference, symmetric difference, and Cartesian product.

- **Prove the union cardinality formula for finite sets.**  
  **Hint:** Add both sizes, then subtract intersection elements counted twice.

- **Explain how set operations are represented by binary vectors and Boolean logic.**  
  **Hint:** Use OR, AND, NOT and show a numerical vector.

- **Compare crisp set operations with fuzzy set operations.**  
  **Hint:** Binary Boolean rules versus graded max/min or other operators; use the same example to show the difference.
