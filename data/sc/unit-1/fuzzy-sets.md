---
subject: sc
unit: 1
topic: fuzzy-sets
syllabus_ref: CSM3202 Unit-I
status: draft
---
# Fuzzy Sets

## Overview

A fuzzy set allows an element to belong partly rather than only yes or no. Instead of membership value 0 or 1, every element can receive any grade from 0 to 1. The grade is called the degree of membership and is represented by a membership function.

Fuzzy sets do not say that a statement is “0.8 of a fact.” They say that a value is 0.8 compatible with a concept such as warm, fast, or low. The same element can belong strongly to one fuzzy set and weakly to another.

## Explanation

### 1. Why fuzzy sets are needed

Crisp classification is effective only when the boundary is meaningful. A daylight-saving rule, an integer parity test, and a file-existence check have crisp boundaries. “Tall,” “young,” “cheap,” and “safe” do not.

Suppose speed is represented on

\[
X=\{0,10,20,30,40,50,60,70,80\}.
\]

A crisp set for “fast” might contain only 50 and above. But if 40 is fairly fast and 45 is fast, a hard boundary throws away that gradual behavior.

### 2. Zadeh's definition

Let \(X\) be a universe and \(x\in X\) one of its elements. A fuzzy subset \(A\) of \(X\) is characterized by a membership function

\[
\mu_{\tilde A}:X\rightarrow[0,1].
\]

The fuzzy set is written

\[
\tilde A=\{(x,\mu_{\tilde A}(x))\mid x\in X\}.
\]

At every \(x\):

- \(\mu_{\tilde A}(x)=1\): \(x\) fully belongs to \(\tilde A\);
- \(\mu_{\tilde A}(x)=0\): \(x\) has no membership in \(\tilde A\);
- \(0<\mu_{\tilde A}(x)<1\): \(x\) belongs partially.

Membership is always relative to a particular fuzzy set. A value can be 0.8 in “fast” and 0.2 in “slow” without contradiction.

### 3. Discrete representation

For a finite universe,

\[
X=\{0,10,20,30,40,50,60,70,80\},
\]

a discrete fuzzy set can be displayed as

\[
\tilde A=
\frac{0}{0}+\frac{0.2}{10}+\frac{0.5}{20}
+\frac{0.8}{30}+\frac{1}{40}+\frac{1}{50}
+\frac{0.7}{60}+\frac{0.3}{70}+\frac{0}{80}.
\]

The number above each element is its membership. The shorthand can also be written as the ordered vector

\[
[0,0.2,0.5,0.8,1,1,0.7,0.3,0].
\]

This representation is useful in calculations, although it is not tied to a physical shape.

### 4. Membership versus a probability

A membership value answers a compatibility question:

> How strongly does this value match the concept represented by the fuzzy set?

A probability answers a question in a random model:

> What is the probability of an event or hypothesis?

If a person is 0.8 compatible with “tall,” this does not mean there is an 80% physical chance that the person is tall. Membership and probability may be mapped to one another in a separate model, but they are not automatically identical.

### 5. Support, core, height, and width

For a fuzzy set \(\tilde A\):

- **Support**
  \[
  \operatorname{supp}(\tilde A)=\{x\in X:\mu_{\tilde A}(x)>0\}.
  \]

- **Core**
  \[
  \operatorname{core}(\tilde A)=\{x\in X:\mu_{\tilde A}(x)=1\}.
  \]

- **Height**
  \[
  h(\tilde A)=\max_{x\in X}\mu_{\tilde A}(x).
  \]

- **Width**
  \[
  w(\tilde A)=\sup(\operatorname{supp}(\tilde A))-\inf(\operatorname{supp}(\tilde A))
  \]
  for a continuous universe.

A **normal** fuzzy set has height 1. A non-normal set reaches a maximum below 1. A **subnormal** fuzzy set has height less than 1.

### 6. Normality and convexity

A fuzzy set is normal if

\[
\exists x\in X:\mu_{\tilde A}(x)=1.
\]

For a continuous universe, it is convex if its membership function is convex, meaning its graph lies below the straight line joining any two points of the graph. An \(\alpha\)-convex set is a generalized form that remains convex after every \(\alpha\)-cut.

Normality matters in fuzzy pattern matching because a template is often normalized so that at least one point has membership 1.

### 7. Alpha-cuts

An **\(\alpha\)-cut** of \(\tilde A\) is the crisp set of all elements whose membership is at least \(\alpha\):

\[
\tilde A_\alpha=\{x\in X:\mu_{\tilde A}(x)\ge\alpha\},\qquad 0<\alpha\le1.
\]

The **strong \(\alpha\)-cut** uses strict inequality:

\[
\tilde A_{\bar\alpha}=\{x:\mu_{\tilde A}(x)>\alpha\}.
\]

The family of alpha-cuts reconstructs a normal fuzzy set:

\[
\tilde A=\bigcup_{\alpha\in(0,1]}\frac{\alpha}{\tilde A_\alpha}.
\]

This expression says that fuzzy membership is described by nested crisp levels.

### 8. Singleton and null fuzzy sets

A **singleton fuzzy set** has exactly one element with nonzero membership:

\[
\tilde a=\{a,1\}.
\]

A fuzzy set whose membership is zero for every element is the **null fuzzy set**:

\[
\tilde\varnothing=\{(x,0):x\in X\}.
\]

The universe is the **universal fuzzy set**:

\[
\tilde X=\{(x,1):x\in X\}.
\]

### 9. Cardinality and representation

A finite fuzzy set can be listed as ordered pairs or as a membership vector. Its support size is

\[
|\operatorname{supp}(\tilde A)|.
\]

The set itself is not assigned a simple real-valued magnitude such as an ordinary sum of all memberships; any such number is a chosen property, not a universal definition.

### 10. Type-2 fuzzy sets

An ordinary fuzzy set is also called a **type-1 fuzzy set**. Its membership grade is a number. In a **type-2 fuzzy set**, each \(x\) is associated not with one membership value but with a fuzzy set of possible membership grades. This can represent uncertainty about the membership grade itself.

Type-2 fuzzy logic is useful when no single membership function reliably captures expert uncertainty, but it is more computationally complex. The core CSM3202 treatment normally concerns type-1 fuzzy sets.

### 11. Types of fuzzy sets

A few special classes are common:

- **Normal fuzzy set:** contains at least one point with membership 1.
- **Convex fuzzy set:** its graph is convex.
- **Ultrametric fuzzy set:** triangular inequality holds for the induced distance.
- **Subnormal fuzzy set:** maximum membership is less than 1.

For calculations in this course, the most important properties are membership values, support/core/height, alpha-cuts, and the set operations in the next note.

## Worked examples

### Example 1: Build a discrete fuzzy set

Let

\[
X=\{10,20,30,40,50\}
\]

and define “medium temperature” by

\[
\tilde M=[0,0.5,1,0.5,0].
\]

Written in long form,

\[
\tilde M=
\frac{0}{10}+\frac{0.5}{20}+\frac{1}{30}
+\frac{0.5}{40}+\frac{0}{50}.
\]

Its support is \(\{20,30,40\}\), its core is \(\{30\}\), and its height is 1. It is therefore normal.

Its alpha-cuts are:

\[
\tilde M_{0.5}=\{20,30,40\},
\]

\[
\tilde M_{0.75}=\{30\},
\]

and for \(0<\alpha<0.5\),

\[
\tilde M_\alpha=\{20,30,40\}.
\]

For \(\alpha=1\), the cut is the core \(\{30\}\).

### Example 2: Continuous triangular membership function

For “medium” on \([0,40]\), let the core be 20 and the support end at 0 and 40:

\[
\mu_M(x)=
\begin{cases}
x/20,&0\le x<20,\\
(40-x)/20,&20\le x\le40,\\
0,&\text{otherwise}.
\end{cases}
\]

At \(x=12\),

\[
\mu_M(12)=12/20=0.6.
\]

At \(x=32\),

\[
\mu_M(32)=(40-32)/20=0.4.
\]

Both are full positive members, but 12 is more strongly medium than 32.

### Example 3: Find alpha-cuts graphically

Suppose a fuzzy set has support \([10,50]\) and core \([20,30]\). If the 0.6 cut is \([15,35]\), an input \(x=17\) has membership at least 0.6. An input \(x=14\) does not belong to that cut. The boundary may lie exactly at 0.6 depending on the membership function.

### Example 4: Compare crisp and fuzzy versions

For \(X=\{1,2,3,4,5\}\), the crisp set \(A=\{4,5\}\) has vector

\[
[0,0,0,1,1].
\]

A fuzzy set may be

\[
\tilde A=[0,0,0.2,0.7,1].
\]

The fuzzy version preserves the observation that 2 is somewhat close to the concept represented by \(A\), while still showing that 5 is the strongest member.

## Key terms & formulas

- **Universe:** \(X\)
- **Fuzzy set:** \(\tilde A=\{(x,\mu_{\tilde A}(x)):x\in X\}\)
- **Membership function:** \(\mu_{\tilde A}:X\to[0,1]\)
- **Support:** \(\{x:\mu_{\tilde A}(x)>0\}\)
- **Core:** \(\{x:\mu_{\tilde A}(x)=1\}\)
- **Height:** \(h(\tilde A)=\max_x\mu_{\tilde A}(x)\)
- **Normal set:** \(h(\tilde A)=1\)
- **Alpha-cut:** \(\tilde A_\alpha=\{x:\mu_{\tilde A}(x)\ge\alpha\}\)
- **Strong alpha-cut:** \(\tilde A_{\bar\alpha}=\{x:\mu_{\tilde A}(x)>\alpha\}\)

Reconstruction of a normal fuzzy set:

\[
\tilde A=\bigcup_{\alpha\in(0,1]}\frac{\alpha}{\tilde A_\alpha}.
\]

## Common mistakes

1. **Writing \(\mu_A(x)\) without naming its universe.** The same membership value is meaningful only relative to \(X\) and a concept \(A\).
2. **Allowing membership below 0 or above 1.** Fuzzy membership lies in \([0,1]\).
3. **Calling a non-normal set invalid.** A fuzzy set may be subnormal; normality is only a special property.
4. **Using strict inequality for a normal alpha-cut.** The ordinary \(\alpha\)-cut uses \(\ge\).
5. **Treating 0.8 membership as 80% probability.** They are different interpretations.
6. **Confusing support and core.** Support begins at positive membership; core consists of full members.
7. **Dropping zero-membership elements without noting the universe.** A finite vector needs a stated element order.
8. **Claiming every type-1 fuzzy set has membership 1 somewhere.** Only a normal fuzzy set does.

## Exam prep

### Likely 2-mark questions

- **Define a fuzzy set.**  
  **Hint:** Use a universe and membership function mapping into \([0,1]\).

- **Define support and core of a fuzzy set.**  
  **Hint:** Positive membership versus membership equal to 1.

- **What is a normal fuzzy set?**  
  **Hint:** A set whose maximum membership is 1.

- **Define an \(\alpha\)-cut.**  
  **Hint:** \(\{x:\mu_{\tilde A}(x)\ge\alpha\}\).

- **Differentiate fuzzy membership from probability in one sentence.**  
  **Hint:** Compatibility/degree of belonging versus probability in a random model.

### Likely long-answer questions

- **Explain fuzzy-set theory with notation, discrete representation, and basic properties.**  
  **Hint:** Universe, membership, vector form, support, core, height, normality, and singleton.

- **Define alpha-cuts and explain how they represent a fuzzy set.**  
  **Hint:** Weak/strong cuts, nested levels, reconstruction, and a numerical example.

- **Compare crisp and fuzzy sets.**  
  **Hint:** Same universe, binary versus continuous membership, hard versus graded boundary, and an example.

- **Explain the meaning of membership grade 0.7 with an example.**  
  **Hint:** Strong compatibility, not probability; show another fuzzy set in which the same value has a different meaning.

- **Discuss type-1 and type-2 fuzzy sets.**  
  **Hint:** Numerical primary grade versus fuzzy secondary membership, benefits, and complexity.
