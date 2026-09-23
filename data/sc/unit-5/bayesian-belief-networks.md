---
subject: sc
unit: 5
topic: bayesian-belief-networks
syllabus_ref: CSM3202 Unit-V
status: draft
---
# Bayesian Belief Network

## Overview

A Bayesian belief network, or Bayesian network (BBN), is a directed acyclic graph representing random variables and their conditional dependencies. Each node has a conditional probability table (CPT) given its parents. A full joint distribution is obtained by multiplying local probabilities.

A BBN supports probabilistic inference, reasoning under uncertainty, diagnosis, reliability analysis, and decision support. Its power comes from representing local dependencies compactly and updating beliefs when evidence is observed.

## Explanation

### 1. Graph structure

A BBN is a directed acyclic graph \(G=(V,E)\). Nodes represent random variables; an edge \(X\to Y\) represents that \(Y\)'s conditional distribution depends on \(X\).

For example:

\[
\text{Age}\to\text{Symptom},\qquad
\text{Smoking}\to\text{Disease},\qquad
\text{Disease}\to\text{Symptom}.
\]

The graph must be acyclic. A cycle would prevent a consistent factorization in the ordinary BBN definition.

### 2. Joint distribution factorization

If \(X_1,\ldots,X_n\) are the nodes and \(\operatorname{Pa}(X_i)\) is the parent set, the joint distribution is

\[
P(X_1,\ldots,X_n)
=
\prod_{i=1}^{n}P(X_i\mid\operatorname{Pa}(X_i)).
\]

A binary node with two parents has \(2^2=4\) rows in its CPT. A node with \(k\) binary parents has \(2^k\) rows.

The factorization reduces the number of parameters compared with an unrestricted joint table.

### 3. Conditional probability tables

For a binary node \(C\) with parent \(A\),

\[
\begin{array}{c|cc}
A & P(C=1\mid A) & P(C=0\mid A)\\\hline
0&0.2&0.8\\
1&0.8&0.2
\end{array}
\]

Each row should sum to 1. A CPT can be estimated from data using counts with smoothing:

\[
P(X_i=x\mid pa)
=
\frac{N(x,pa)+\alpha}
{\sum_{x'}N(x',pa)+\alpha|\mathcal X_i|}.
\]

Smoothing avoids zero probabilities for unseen combinations.

### 4. Prior and posterior beliefs

Before evidence, a marginal belief is obtained by summing over all other variables. For a simple chain

\[
A\to B,
\]

the probability of \(B=1\) is

\[
P(B=1)=P(B=1\mid A=0)P(A=0)+P(B=1\mid A=1)P(A=1).
\]

Evidence \(E\) updates beliefs:

\[
P(X\mid E)\propto P(X,E).
\]

The proportionality is normalized over all values of \(X\).

### 5. Exact inference

For small networks, exact inference uses:

- variable elimination;
- enumeration;
- junction-tree/message passing.

A query such as

\[
P(C\mid D=1,S=1)
\]

is obtained by multiplying the relevant joint terms and dividing by the evidence probability:

\[
P(C=c\mid D=d,S=s)
=
\frac{P(C=c,D=d,S=s)}
{\sum_{c'}P(C=c',D=d,S=s)}.
\]

Exact inference becomes expensive as treewidth and evidence size grow.

### 6. Approximate inference

Large networks may use:

- belief propagation;
- variational methods;
- importance sampling;
- particle filtering;
- MCMC.

Approximate methods trade exactness for speed. Report approximation error or enough samples to estimate variability when possible.

### 7. D-separation

D-separation is a graphical test for whether a set \(Z\) blocks every active path between two variables \(X\) and \(Y\).

A path is active when it contains no collider or when it contains a collider that is in the conditioning set or has a descendant in the conditioning set.

If \(X\perp Y\mid Z\), then

\[
P(X,Y\mid Z)=P(X\mid Z)P(Y\mid Z)
\]

under the BBN distribution.

Useful graph patterns:

- a non-collider in \(Z\) blocks a chain \(X\to Z\to Y\);
- a collider blocks a chain unless it or a descendant is observed;
- conditioning on a collider can create dependence between its parents.

### 8. Markov blanket

The Markov blanket of node \(X\) consists of its parents, children, and the other parents of its children. Once the blanket is known, the rest of the network is conditionally independent of \(X\):

\[
P(X\mid\text{all others})
=
P(X\mid\operatorname{MB}(X)).
\]

This is useful for explanation and local updates.

### 9. Bayesian diagnosis

A diagnostic network commonly uses:

- disease nodes;
- symptom or test nodes;
- risk factors;
- background conditions.

A positive test \(T=1\) is not simply converted to a disease probability. Use

\[
P(D\mid T=1,E)
\propto P(T=1\mid D,E)P(D\mid E).
\]

Base rates and dependencies matter. If a symptom has different likelihoods under different diseases, update all hypotheses together.

### 10. Learning structure and parameters

Parameter learning estimates CPTs from complete or incomplete data. Structure learning searches for a graph using score-based or constraint-based methods.

A score-based method may use

\[
\operatorname{BDeu}(G,D)
\]

or a decomposable likelihood score. A constraint-based method searches for conditional independences. Both can overfit or choose a different graph when data are limited; domain knowledge is valuable.

### 11. Missing data

If a node is unobserved, summing over its possible states gives its marginal contribution. If a parent is missing, marginalize its children and sum conditional probabilities weighted by the missing parent's marginal:

\[
P(X\mid Y=y)
=
\sum_{z}P(X\mid Y=y,Z=z)P(z).
\]

Missing values are not automatically evidence that a variable is absent.

### 12. Dynamic Bayesian networks

A dynamic Bayesian network extends BBNs over time with slices and transition structure. It can represent temporal dependencies more explicitly than a static network. A hidden Markov model is a special structured sequence model; BBN terminology and HMM terminology overlap in applications.

### 13. Advantages

- Represents uncertainty and dependencies explicitly.
- Supports forward and backward reasoning.
- Can combine heterogeneous evidence.
- Learns or updates probabilities from data.
- Provides a causal-like dependency structure, subject to assumptions.
- Compact compared with a full joint table.

### 14. Limitations

- Structure and CPT assumptions may be wrong.
- Exact inference can be expensive.
- Missing data complicates learning.
- A graph does not prove causation.
- Sparse evidence can give high posterior uncertainty.
- Parameter estimates can be unstable with small samples.

## Worked examples

### Example 1: Simple diagnostic network

Let

\[
P(D=1)=0.01,
\]

\[
P(T=1\mid D=1)=0.9,\quad
P(T=1\mid D=0)=0.05.
\]

The network is \(D\to T\). Given a positive test,

\[
P(D=1\mid T=1)
=
\frac{0.9(0.01)}
{0.9(0.01)+0.05(0.99)}
=0.153846.
\]

The BBN simply reproduces Bayes' theorem for this chain.

### Example 2: Two-parent BBN

Let binary variables \(A,B,C\) form a collider:

\[
A\to C\leftarrow B.
\]

Use

\[
P(A=1)=P(B=1)=0.5
\]

and

\[
P(C=1\mid A,B)=
\begin{cases}
0.1,&A=0,B=0,\\
0.2,&A=0,B=1,\\
0.7,&A=1,B=0,\\
0.9,&A=1,B=1.
\end{cases}
\]

Without evidence,

\[
P(C=1)
=
0.1(0.5)(0.5)+0.2(0.5)(0.5)
+0.7(0.5)(0.5)+0.9(0.5)(0.5)
=0.475.
\]

If \(C=1\) is observed, observing the collider can make \(A\) and \(B\) dependent even though they were independent marginally. This is explaining away, a classic BBN phenomenon.

### Example 3: Factorization and conditional independence

If \(A\to B\to C\), the joint is

\[
P(A,B,C)=P(A)P(B\mid A)P(C\mid B).
\]

Given \(B\), \(A\) and \(C\) are d-separated under the Markov property:

\[
P(A,C\mid B)=P(A\mid B)P(C\mid B).
\]

This conditional independence is why the network can be compact.

### Example 4: Two pieces of evidence

Suppose disease \(D\) has prior 0.1, and two conditionally independent symptoms have:

\[
P(S_1\mid D)=0.8,\quad
P(S_1\mid\neg D)=0.2,
\]

\[
P(S_2\mid D)=0.7,\quad
P(S_2\mid\neg D)=0.1.
\]

The unnormalized masses are

\[
0.1(0.8)(0.7)=0.056,
\]

\[
0.9(0.2)(0.1)=0.018.
\]

The posterior is

\[
P(D\mid S_1,S_2)=\frac{0.056}{0.056+0.018}=0.756757.
\]

This multiplication is valid only under the stated conditional independence model.

## Key terms & formulas

- **BBN:** Bayesian belief network.
- **Node:** Random variable.
- **Edge:** Conditional dependence.
- **CPT:** Conditional probability table.
- **Factorization:** Product of local conditionals.
- **Evidence:** Observed variable value.
- **Marginalization:** Sum over unobserved variables.
- **D-separation:** Graphical conditional independence test.
- **Markov blanket:** Parents, children, and children's other parents.

Joint:

\[
P(X_1,\ldots,X_n)=\prod_iP(X_i\mid\operatorname{Pa}(X_i)).
\]

Posterior:

\[
P(X\mid E)=\frac{P(X,E)}{P(E)}.
\]

D-separation consequence:

\[
X\perp Y\mid Z
\Rightarrow
P(X,Y\mid Z)=P(X\mid Z)P(Y\mid Z).
\]

## Common mistakes

1. **Using a directed cycle in a BBN.** A Bayesian network is a DAG.
2. **Omitting a parent in a CPT.** Every parent combination needs a conditional row.
3. **Treating a graph edge as proof of causation.** It encodes the chosen probabilistic dependency model.
4. **Conditioning on a collider incorrectly.** This can create dependence.
5. **Multiplying evidence without checking conditional independence.** Likelihoods may be dependent.
6. **Treating missing values as zero evidence.** Missingness needs explicit handling.
7. **Ignoring normalization in exact inference.** Query probabilities must sum to one.
8. **Using exact inference on a large network without considering cost.** Approximate methods may be necessary.

## Exam prep

### Likely 2-mark questions

- **Define a Bayesian belief network.**  
  **Hint:** DAG of random variables with local CPTs.

- **Write the factorization of a BBN joint distribution.**  
  **Hint:** Product of \(P(X_i\mid\operatorname{Pa}(X_i))\).

- **What is a CPT?**  
  **Hint:** Table of a node's conditional probabilities for each parent configuration.

- **Define d-separation.**  
  **Hint:** Conditioning set blocks all active paths between variables.

- **What is the Markov blanket?**  
  **Hint:** Parents, children, and other parents of children.

### Likely long-answer questions

- **Explain BBN structure, CPTs, and joint factorization with an example.**  
  **Hint:** DAG, conditional rows, factorization, and parameter count.

- **Perform exact Bayesian inference in a small network.**  
  **Hint:** Multiply relevant factors, sum hidden variables, normalize query.

- **Explain d-separation and collider effects.**  
  **Hint:** Active paths, conditioning, explaining away, and conditional independence.

- **Discuss applications, learning, and limitations of BBNs.**  
  **Hint:** Diagnosis, reliability, parameter/structure learning, missing data, and inference cost.
