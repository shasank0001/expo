---
subject: sc
unit: 1
topic: fuzzy-set-operations
syllabus_ref: CSM3202 Unit-I
status: draft
---
# Fuzzy Set Operations

## Overview

Fuzzy set operations combine graded membership values in the same way that crisp operations combine membership 0 and 1. Union usually uses maximum, intersection usually uses minimum, and complement uses \(1-\mu\). Other t-norms and t-conorms, such as product and bounded sum, are also common.

The operation must be named. A fuzzy union is not uniquely defined unless the chosen operator is stated. Alpha-cuts provide a useful way to understand these operations geometrically.

## Explanation

### 1. Standard fuzzy complement

Let \(\tilde A\) and \(\tilde B\) be fuzzy subsets of \(X\). The usual complement is

\[
\mu_{\tilde A^c}(x)=1-\mu_{\tilde A}(x).
\]

This satisfies

\[
\mu_{\tilde A^c}(x)=1\iff\mu_{\tilde A}(x)=0,
\]

and

\[
\mu_{\tilde A^c}(x)=0\iff\mu_{\tilde A}(x)=1.
\]

If \(\mu_{\tilde A}(0.7)=0.7\), its complement grade is 0.3.

### 2. Fuzzy union

The most common union is the max t-conorm:

\[
\mu_{\tilde A\cup\tilde B}(x)
=\max(\mu_{\tilde A}(x),\mu_{\tilde B}(x)).
\]

An alternative is the **bounded sum**, also called the probabilistic sum:

\[
\mu_{\tilde A\cup\tilde B}(x)
=\mu_{\tilde A}(x)+\mu_{\tilde B}(x)
-\mu_{\tilde A}(x)\mu_{\tilde B}(x).
\]

The product is another conorm:

\[
\mu_{\tilde A\cup\tilde B}(x)
=\mu_{\tilde A}(x)\mu_{\tilde B}(x).
\]

A union should be commutative, associative, monotone, and have \(\mu_0(x)=0\) as a neutral element. Max, bounded sum, and product satisfy these requirements for fuzzy-set union.

### 3. Fuzzy intersection

The most common intersection is the min t-norm:

\[
\mu_{\tilde A\cap\tilde B}(x)
=\min(\mu_{\tilde A}(x),\mu_{\tilde B}(x)).
\]

Other widely used t-norms are:

#### Product t-norm

\[
\mu_{\tilde A\cap\tilde B}(x)
=\mu_{\tilde A}(x)\mu_{\tilde B}(x).
\]

#### Bounded difference (Łukasiewicz t-norm)

\[
\mu_{\tilde A\cap\tilde B}(x)
=\max\left(0,\mu_{\tilde A}(x)+\mu_{\tilde B}(x)-1\right).
\]

#### Hamacher product

\[
\frac{\mu_{\tilde A}(x)\mu_{\tilde B}(x)}
{\mu_{\tilde A}(x)+\mu_{\tilde B}(x)-\mu_{\tilde A}(x)\mu_{\tilde B}(x)}
\]

when the denominator is nonzero, with suitable definition at zero.

The **drastic-product t-norm** is

\[
\begin{cases}
\min(a,b),&\max(a,b)=1,\\
0,&\text{otherwise},
\end{cases}
\]

where \(a=\mu_{\tilde A}(x)\), \(b=\mu_{\tilde B}(x)\).

### 4. Why min/max are not the only choices

The min t-norm can be viewed as the largest value guaranteed not to exceed either input. The product t-norm is smaller for grades strictly between 0 and 1, so it makes the rule conclusion more conservative. The Łukasiewicz t-norm equals 0 unless the sum of the grades exceeds 1.

The choice affects rule firing and output values, so it must be recorded in an experiment or model.

### 5. Fuzzy difference

The standard relative difference is

\[
\mu_{\tilde A-\tilde B}(x)
=\mu_{\tilde A}(x)\wedge(1-\mu_{\tilde B}(x)),
\]

where \(\wedge\) is normally min. Another common definition is

\[
\mu_{\tilde A-\tilde B}(x)
=\max\left(0,\mu_{\tilde A}(x)-\mu_{\tilde B}(x)\right).
\]

The first is used when the difference should be bounded like a complement-based operation; the second never exceeds \(\mu_{\tilde A}\). Always state which definition is intended.

### 6. Symmetric difference

Using the crisp-style definition \(A\triangle B=(A-B)\cup(B-A)\), the result depends on the chosen difference, union, and intersection operators. If bounded difference and max union are used,

\[
\mu_{A\triangle B}(x)
=\max\left[
\max(0,a-b),\max(0,b-a)
\right]
=|a-b|,
\]

where \(a=\mu_A(x)\), \(b=\mu_B(x)\).

This is not the only fuzzy definition, which again shows why the operator must be named.

### 7. Cartesian product and fuzzy relations

For fuzzy sets \(\tilde A\subseteq X\) and \(\tilde B\subseteq Y\), the Cartesian fuzzy set is

\[
\mu_{\tilde A\times\tilde B}(x,y)
=\min(\mu_{\tilde A}(x),\mu_{\tilde B}(y))
\]

with max as an alternative.

A fuzzy relation \(R\subseteq X\times Y\) is represented by a membership function

\[
\mu_R(x,y):X\times Y\rightarrow[0,1].
\]

The zero relation has all memberships 0. If \(R\) is normal, at least one pair has membership 1. Max-min composition of two fuzzy relations is

\[
\mu_{R\circ S}(x,z)
=\max_{y\in Y}\min\bigl(\mu_R(x,y),\mu_S(y,z)\bigr).
\]

### 8. De Morgan's laws

For complement \(1-x\), min intersection, and max union,

\[
\mu_{(A\cup B)^c}(x)
=\min(1-a,1-b)
=1-\max(a,b)
=\mu_{A^c\cap B^c}(x).
\]

Thus,

\[
(A\cup B)^c=A^c\cap B^c,
\qquad
(A\cap B)^c=A^c\cup B^c.
\]

These identities do not automatically hold for every t-norm/t-conorm pair. The chosen operators must preserve the required dual relationship.

### 9. Operations through alpha-cuts

For min and max,

\[
(A\cap B)_\alpha=A_\alpha\cap B_\alpha
\]

and

\[
(A\cup B)_\alpha=A_\alpha\cup B_\alpha.
\]

For the product t-conorm (if it is selected for a fuzzy union),

\[
(A\cup B)_\alpha
=
\{x:a(x)b(x)\ge\alpha\}.
\]

For the bounded-sum t-conorm,

\[
(A\cup B)_\alpha
=
\{x:a(x)+b(x)-a(x)b(x)\ge\alpha\}.
\]

For the Łukasiewicz t-norm,

\[
(A\cap B)_\alpha
=
\{x:a(x)+b(x)\ge1+\alpha\}.
\]

These level sets are not generally equal to the simple union or intersection of the individual alpha-cuts. For the standard complement,

\[
(A^c)_\alpha
=
\{x:1-a(x)\ge\alpha\}
=
\{x:a(x)\le1-\alpha\}
=
X\setminus A_{1-\alpha}^{>},
\]

where \(A_\gamma^{>}=\{x:a(x)>\gamma\}\) is the strong alpha-cut. The strict/weak convention matters at the boundary.

### 10. Set properties in fuzzy form

With min, max, and standard complement:

- **Commutativity:** \(A\cup B=B\cup A\), \(A\cap B=B\cap A\).
- **Associativity:** parentheses may be moved.
- **Idempotence:** \(A\cup A=A\), \(A\cap A=A\).
- **Identity:** \(A\cup0=A\), \(A\cap1=A\).
- **Domination:** \(A\subseteq B\) implies \(A\cap B=A\), \(A\cup B=B\).
- **Involution:** \((A^c)^c=A\).

### 11. Algebraic product sum

One may also define

\[
\mu_{A\cdot B}(x)=ab,
\]

and the algebraic sum

\[
\mu_{A+B}(x)=
\begin{cases}
a+b,&a+b\le1,\\
1,&a+b>1.
\end{cases}
\]

These are not always true union/intersection operators, so their purpose must be stated. A common rule-consequence aggregation is the algebraic sum of clipped membership values.

## Worked examples

### Example 1: Union, intersection, and complement

Let \(X=\{1,2,3,4\}\) and

\[
\tilde A=[0,0.5,0.8,1],\qquad
\tilde B=[1,0.6,0.8,0.2].
\]

Using max for union and min for intersection:

\[
A\cup B=[1,0.6,0.8,1],
\]

\[
A\cap B=[0,0.5,0.8,0.2],
\]

\[
A^c=[1,0.5,0.2,0].
\]

For example, at element 2,

\[
\max(0.5,0.6)=0.6,\qquad
\min(0.5,0.6)=0.5.
\]

### Example 2: Compare t-norms and t-conorms

At one element, let \(a=0.6\) and \(b=0.4\).

- Min intersection: \(0.4\).
- Product intersection: \(0.24\).
- Łukasiewicz intersection: \(\max(0,0.6+0.4-1)=0\).
- Max union: \(0.6\).
- Bounded-sum union: \(0.6+0.4-0.24=0.76\).
- Product union: \(0.24\).

The same two input grades produce very different outputs under different operators.

### Example 3: Verify De Morgan's law

Let \(a=0.3\), \(b=0.8\).

Left side:

\[
(A\cup B)^c=1-\max(0.3,0.8)=0.2.
\]

Right side:

\[
A^c\cap B^c=\min(0.7,0.2)=0.2.
\]

Now:

\[
(A\cap B)^c=1-\min(0.3,0.8)=0.7,
\]

\[
A^c\cup B^c=\max(0.7,0.2)=0.7.
\]

Both laws hold.

### Example 4: Relative difference

For \(a=0.7\), \(b=0.4\):

- Complement-based min difference:
  \[
  \min(0.7,1-0.4)=\min(0.7,0.6)=0.6.
  \]
- Bounded difference:
  \[
  \max(0,0.7-0.4)=0.3.
  \]

The two values are both valid under different named definitions.

### Example 5: Alpha-cut of a discrete fuzzy set

For

\[
A=[0,0.2,0.7,0.9,0.4],
\]

the \(0.5\)-cut on the index set \(X=\{1,2,3,4,5\}\) is

\[
A_{0.5}=\{3,4\}.
\]

The strong \(0.7\)-cut is \(\{4\}\), because \(0.7>0.7\) is false for element 3.

## Key terms & formulas

Let \(a=\mu_A(x)\), \(b=\mu_B(x)\).

- **Complement:** \(A^c:1-a\)
- **Union (max):** \(a\vee b\)
- **Union (bounded sum):** \(a+b-ab\)
- **Intersection (min):** \(a\wedge b\)
- **Intersection (product):** \(ab\)
- **Intersection (Łukasiewicz):** \(\max(0,a+b-1)\)
- **Relative difference:** \(a\wedge(1-b)\)
- **Bounded difference:** \(\max(0,a-b)\)

A t-norm \(T\) is commutative, associative, monotone, and has \(T(a,1)=a\). A t-conorm \(S\) has the same properties with \(S(a,0)=a\).

For max-min composition:

\[
\mu_{R\circ S}(x,z)=\max_y\min(\mu_R(x,y),\mu_S(y,z)).
\]

## Common mistakes

1. **Writing only “union” for fuzzy sets.** State max, bounded sum, product, or another operator.
2. **Using union and intersection without considering order.** Union is commutative, but rule implication is not.
3. **Applying De Morgan blindly.** The usual form assumes compatible min/max and complement operators.
4. **Using product as max-min composition.** Product is not the same as the min t-norm.
5. **Confusing complement with difference.** Complement is relative to the whole universe.
6. **Using strict \(>\) in an ordinary alpha-cut.** Use \(\ge\).
7. **Forgetting that alpha-cuts are calculated for the same universe and order.**
8. **Claiming product is always the best t-norm.** It may be too conservative or poorly matched to the expert's intent.

## Exam prep

### Likely 2-mark questions

- **Write the standard fuzzy union and intersection.**  
  **Hint:** max and min pointwise.

- **Define the standard fuzzy complement.**  
  **Hint:** \(1-\mu_A(x)\).

- **State two alternative t-norms.**  
  **Hint:** Product and Łukasiewicz \(\max(0,a+b-1)\).

- **What is the t-conorm property \(S(a,0)=a\)?**  
  **Hint:** The universal crisp value 0 is the neutral element for a t-conorm.

- **Write max–min composition of fuzzy relations.**  
  **Hint:** \(\max_y\min(\mu_R,\mu_S)\).

### Likely long-answer questions

- **Explain fuzzy set operations and compare min/max with product and bounded-sum operators.**  
  **Hint:** Definitions, algebraic properties, and a numerical pointwise table.

- **Derive the alpha-cut properties of min intersection, max union, and complement.**  
  **Hint:** Start from the membership inequalities and show crisp set results.

- **Explain the difference between Boolean and fuzzy operations.**  
  **Hint:** Use graded values to show how min/max and OR/AND coincide only in the binary case.

- **Explain fuzzy relations and max–min composition with an example.**  
  **Hint:** Membership matrix, path interpretation, minimum edge strength, and maximum path choice.
