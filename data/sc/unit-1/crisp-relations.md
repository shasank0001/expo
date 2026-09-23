---
subject: sc
unit: 1
topic: crisp-relations
syllabus_ref: CSM3202 Unit-I
status: draft
---
# Crisp Relations

## Overview

A crisp relation describes which ordered pairs are allowed between two sets. A binary relation can be listed as pairs, written as a set-builder rule, or represented by a 0–1 matrix. Relation operations support reasoning about “less than,” “belongs to,” and compatibility.

Crisp relations are the discrete and exact basis of relational databases and Boolean relational algebra. Fuzzy relations later relax each matrix entry from 0 or 1 to any value in \([0,1]\).

## Explanation

### 1. Definition

Let \(A\) and \(B\) be sets. A relation \(R\) from \(A\) to \(B\) is a subset of the Cartesian product

\[
R\subseteq A\times B.
\]

A pair \((a,b)\in R\) means that \(a\) is related to \(b\). It does not normally imply that \(b\) is related to \(a\).

If \(|A|=m\) and \(|B|=n\), there are \(mn\) possible ordered pairs, so there are \(2^{mn}\) possible binary relations.

### 2. Representations

#### Ordered-pair form

Let

\[
A=\{a_1,a_2\},\quad B=\{b_1,b_2,b_3\}.
\]

A relation may be

\[
R=\{(a_1,b_1),(a_1,b_3),(a_2,b_2)\}.
\]

#### Set-builder form

The same relation is

\[
R=\{(x,y)\in A\times B:(x=a_1\land y\ne b_2)\lor(x=a_2\land y=b_2)\}.
\]

#### Relation matrix

With rows ordered as \(a_1,a_2\) and columns as \(b_1,b_2,b_3\),

\[
M_R=
\begin{bmatrix}
1&0&1\\
0&1&0
\end{bmatrix}.
\]

An entry is 1 if the pair belongs to \(R\), and 0 otherwise.

#### Characteristic function

\[
\mu_R(a,b)=
\begin{cases}
1,&(a,b)\in R,\\
0,&\text{otherwise}.
\end{cases}
\]

The row set of the first column is called the domain, and the union of rows containing a 1 is the range:

\[
\operatorname{dom}(R)=\{a:\exists b,(a,b)\in R\},
\]

\[
\operatorname{ran}(R)=\{b:\exists a,(a,b)\in R\}.
\]

In the example,

\[
\operatorname{dom}(R)=\{a_1,a_2\},\quad
\operatorname{ran}(R)=\{b_1,b_2,b_3\}.
\]

### 3. Types of relations

A relation \(R\subseteq A\times A\) may be:

- **Reflexive:** \((a,a)\in R\) for every \(a\in A\).
- **Irreflexive:** \((a,a)\notin R\) for every \(a\in A\).
- **Symmetric:** \((a,b)\in R\Rightarrow(b,a)\in R\).
- **Asymmetric:** \((a,b)\in R\Rightarrow(b,a)\notin R\), for \(a\ne b\).
- **Antisymmetric:** \((a,b)\in R\) and \((b,a)\in R\) imply \(a=b\).
- **Transitive:** \((a,b),(b,c)\in R\Rightarrow(a,c)\in R\).
- **Total or complete:** for every \(a,b\), at least one of \((a,b)\) or \((b,a)\) belongs to \(R\).
- **Partial order:** reflexive, antisymmetric, and transitive.

Examples:

- \(\le\) is reflexive, antisymmetric, and transitive.
- \(<\) is irreflexive and transitive.
- Equality \(=\) is reflexive, symmetric, antisymmetric, and transitive.
- The sibling relation is normally symmetric but not reflexive or transitive.

### 4. Inverse relation

The inverse of \(R\) is

\[
R^{-1}=\{(b,a):(a,b)\in R\}.
\]

For the example,

\[
R^{-1}=\{(b_1,a_1),(b_3,a_1),(b_2,a_2)\}.
\]

The inverse matrix is the transpose:

\[
M_{R^{-1}}=M_R^T.
\]

If \(R\) is reflexive, symmetric, or transitive, its inverse has the same property. A relation is an equivalence relation if it is reflexive, symmetric, and transitive.

### 5. Complement

The complement of \(R\) relative to \(A\times B\) is

\[
R^c=(A\times B)-R.
\]

It contains every allowed pair not in \(R\). The matrix complement is

\[
M_{R^c}=J-M_R,
\]

where \(J\) is the all-ones matrix.

### 6. Union and intersection

For \(R,S\subseteq A\times B\),

\[
R\cup S=\{(a,b):(a,b)\in R\text{ or }(a,b)\in S\},
\]

\[
R\cap S=\{(a,b):(a,b)\in R\text{ and }(a,b)\in S\}.
\]

In the Boolean relation matrix, union is OR and intersection is AND:

\[
M_{R\cup S}=M_R\lor M_S,
\]

\[
M_{R\cap S}=M_R\land M_S.
\]

### 7. Difference

\[
R-S=R\cap S^c.
\]

It contains pairs that belong to \(R\) but not to \(S\).

The symmetric difference is

\[
R\triangle S=(R-S)\cup(S-R).
\]

### 8. Cartesian product of relations

A relation from \(A\) to \(B\) can be combined with one from \(B\) to \(C\):

\[
R\circ S=\{(a,c):\exists b\in B,\ (a,b)\in R\text{ and }(b,c)\in S\}.
\]

This is relational composition. With Boolean matrices,

\[
M_{R\circ S}=M_R\odot M_S,
\]

where \(\odot\) is Boolean matrix multiplication:

\[
[M_R\odot M_S]_{ik}
=\bigvee_{j=1}^{n}([M_R]_{ij}\land[M_S]_{jk}).
\]

The result is 1 if there is a connecting \(b_j\).

### 9. Reflexive, symmetric, and transitive closures

The **reflexive closure** is

\[
R\cup I,
\]

where \(I\) is the identity relation \((a,a)\).

The **symmetric closure** is

\[
R\cup R^{-1}.
\]

The **transitive closure** \(R^+\) consists of all pairs connected by a path of one or more \(R\)-edges. The **reflexive-transitive closure** is

\[
R^*=I\cup R^+.
\]

For a directed graph, an all-ones reachability block may indicate a cycle, but simple path counting can be harder because cycles create infinitely many walks. Reachability closure is what is usually needed.

### 10. Functions and relations

A relation is a function if every element of \(A\) is related to exactly one element of \(B\). It is one-to-one if no two elements of \(A\) share the same image. Functions are therefore special relations, but relations can represent many-to-many behavior.

## Worked examples

### Example 1: Relation matrix and properties

Let \(X=\{1,2,3\}\) and

\[
R=\{(1,1),(1,2),(2,1),(2,3),(3,2)\}.
\]

In the order \(1,2,3\),

\[
M_R=
\begin{bmatrix}
1&1&0\\
1&0&1\\
0&1&0
\end{bmatrix}.
\]

- Reflexive? No, because \((3,3)\notin R\).
- Symmetric? Yes: \((1,2)\) and \((2,1)\), and \((2,3)\) and \((3,2)\) are both present.
- Transitive? No: \((1,2)\) and \((2,3)\) exist, but \((1,3)\) does not.

Thus it is symmetric but not an equivalence relation.

### Example 2: Compute a relation composition

Let

\[
R=\{(a,x),(a,y),(b,y)\},
\]

\[
S=\{(x,z),(y,z),(y,w)\}.
\]

A common middle element gives:

- through \(x\): \((a,z)\);
- through \(y\): \((a,z),(a,w),(b,z)\).

Therefore,

\[
R\circ S=\{(a,z),(a,w),(b,z)\}.
\]

Boolean matrix multiplication gives the same result.

### Example 3: Complement

For

\[
M_R=
\begin{bmatrix}
1&0&1\\
0&1&0
\end{bmatrix},
\]

the complement is

\[
M_{R^c}=
\begin{bmatrix}
0&1&0\\
1&0&1
\end{bmatrix}.
\]

Because there are six possible pairs, \(R\cup R^c=A\times B\) and \(R\cap R^c=\varnothing\).

## Key terms & formulas

- **Binary relation:** \(R\subseteq A\times B\)
- **Relation matrix:** \(M_R=[m_{ij}]\), \(m_{ij}=\mu_R(a_i,b_j)\in\{0,1\}\)
- **Inverse:** \(R^{-1}=\{(b,a):(a,b)\in R\}\)
- **Complement:** \(R^c=(A\times B)-R\)
- **Composition:** \(R\circ S=\{(a,c):\exists b,(a,b)\in R,(b,c)\in S\}\)
- **Identity:** \(I=\{(a,a):a\in A\}\)

Boolean matrix product:

\[
(M_R\odot M_S)_{ik}=\bigvee_j(M_R(i,j)\land M_S(j,k)).
\]

Properties:

\[
\text{equivalence}=\text{reflexive}+\text{symmetric}+\text{transitive}.
\]

## Common mistakes

1. **Confusing \(A\times B\) with a relation.** A relation is only a subset of the Cartesian product.
2. **Treating a relation as symmetric automatically.** A directed relation may include \((a,b)\) without \((b,a)\).
3. **Swapping rows and columns without transposing the row/column labels.** Inverse is a transpose only with the universes aligned correctly.
4. **Using arithmetic multiplication instead of Boolean multiplication in composition.** Boolean composition uses OR and AND.
5. **Assuming reflexivity follows from symmetry.** They are independent properties.
6. **Checking symmetry only in the upper triangle.** Check every directed pair.
7. **Calling a one-to-one mapping a set.** It is a special relation, or function when total.

## Exam prep

### Likely 2-mark questions

- **Define a binary relation.**  
  **Hint:** A subset \(R\subseteq A\times B\).

- **State four properties of a relation.**  
  **Hint:** Reflexive, symmetric, antisymmetric, transitive.

- **How is a relation represented as a matrix?**  
  **Hint:** Rows/columns index set elements and entries are 0 or 1.

- **Define the inverse of a relation.**  
  **Hint:** Reverse every ordered pair.

- **What is an equivalence relation?**  
  **Hint:** Reflexive, symmetric, and transitive.

### Likely long-answer questions

- **Explain binary relations, representations, domain/range, and types.**  
  **Hint:** Pair, matrix, and characteristic function; classify with examples.

- **Define relation complement, union, intersection, inverse, and composition.**  
  **Hint:** Use formulas and one shared example.

- **Explain Boolean matrix composition of relations.**  
  **Hint:** AND along a path, OR across middle elements, and a complete matrix example.

- **Show whether a given relation is reflexive, symmetric, and transitive.**  
  **Hint:** List relevant pairs, test closure, and conclude the relation class.
