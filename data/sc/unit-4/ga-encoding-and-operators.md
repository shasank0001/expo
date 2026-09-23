---
subject: sc
unit: 4
topic: ga-encoding-and-operators
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# Encoding and Genetic Operators in GAs

## Overview

A genetic algorithm cannot evolve a solution until the solution is represented as a chromosome. Encoding converts a problem solution into symbols or numbers that operators can manipulate. Genetic operators then create new chromosomes: crossover exchanges material between parents, mutation makes small random changes, and other operators support a particular representation.

Operator design is as important as selection. A one-point binary crossover is not valid for a circular route without a suitable repair rule, and swapping bits may not preserve a valid schedule. The encoding and operators must be chosen together.

## Explanation

### 1. Encoding requirements

A useful representation should:

- represent every required feasible solution;
- make important solutions close in genotype space;
- allow simple variation;
- preserve feasibility or provide repair;
- avoid huge redundant search spaces;
- be interpretable enough to debug.

There is no encoding that is ideal for every problem. The representation determines which genetic neighborhoods are easy to reach.

### 2. Binary encoding

A real value in \([L,U]\) can be represented with \(k\) bits:

\[
x=L+\frac{v}{2^k-1}(U-L),
\]

where \(v\) is the unsigned decimal value of the bit string.

For \([0,31]\) and 5 bits, the mapping includes 32 levels. The resolution is

\[
\Delta=\frac{U-L}{2^k-1}.
\]

More bits improve resolution but enlarge the search space and may cause Hamming cliffs: 01111 and 10000 represent adjacent values but are far apart in bit space.

### 3. Real-valued encoding

For continuous parameters, use a vector

\[
\mathbf x=(x_1,\ldots,x_d)
\]

directly. Mutation is usually arithmetic or Gaussian:

\[
x_j'=x_j+\sigma z_j
\]

or

\[
x_j'=x_j+\Delta_j,\qquad \Delta_j\sim U(-r,r).
\]

Crossover may use arithmetic, blend, or simulated-binary crossover. Real encoding avoids bit-resolution problems and is often natural for engineering optimization.

### 4. Permutation encoding

A permutation chromosome represents an order:

\[
P=(p_1,p_2,\ldots,p_n).
\]

It is useful for travelling-salesperson, scheduling, and assignment problems. Ordinary one-point crossover can create duplicated or missing elements, so use:

- order crossover (OX);
- cycle crossover (CX);
- partially mapped crossover (PMX);
- swap or inversion mutation.

#### Order crossover

Choose a segment from one parent, copy it, remove those values from the other parent, and fill remaining positions in order. The result preserves a valid permutation.

#### Inversion mutation

Choose two positions \(i<j\) and reverse the segment:

\[
[p_i,\ldots,p_j]\longrightarrow[p_j,\ldots,p_i].
\]

A bounded inversion distance can control how much the schedule changes.

### 5. Character encoding

Each gene can be a symbol such as A, B, C, or a rule token. Crossover is simple, but the meaning of adjacent tokens depends on the problem. A rule-based chromosome may need a grammar to remain executable.

### 6. Crossover

Crossover creates one or more offspring from two parents.

#### One-point binary crossover

For parents

\[
P_1=A|B,\qquad P_2=C|D,
\]

choose a point and form

\[
C_1=A|D,\qquad C_2=C|B.
\]

The cut point must be chosen inside the chromosome. A chromosome of length 1 has no nontrivial internal cut point.

#### Two-point crossover

Choose two positions \(i<j\) and exchange the segment between them while retaining the outside portions.

#### Uniform crossover

Each gene position independently chooses a parent with probability 0.5. This can distribute genes broadly but may break a tightly linked block.

#### Arithmetic crossover

For real vectors,

\[
C_1=\alpha P_1+(1-\alpha)P_2,
\]

\[
C_2=(1-\alpha)P_1+\alpha P_2,
\]

with \(\alpha\in[0,1]\). Children remain inside the convex hull of the parents, which can limit exploration if the population is clustered.

#### Simulated binary crossover (SBX)

For real variables, SBX produces offspring around two parents with a distribution parameter. It is commonly used in continuous multiobjective GAs. The exact distribution is more involved than uniform interpolation, so the implementation should state its formula and parameter.

### 7. Mutation

#### Bit-flip mutation

For each bit, flip with probability \(p_m\):

\[
b_i\leftarrow1-b_i.
\]

For long chromosomes, a small probability can cause many changes. Expected flips are \(kp_m\).

#### Real-valued mutation

Add a random perturbation or draw a Gaussian step. A mutation rate and step scale are separate controls. Using a fixed absolute step when variables have different units can bias the search; scale the step or normalize variables.

#### Swap mutation

For a permutation, swap two positions. It can make a small local change but may be less expressive than inversion for a route.

#### Insertion mutation

Move one element from one position to another. It preserves all permutation elements and can change ordering locally.

#### Creative mutation

A small probability assigns a new arbitrary gene value. It can introduce new alleles but can also destroy useful structure.

### 8. Crossover and mutation probabilities

Crossover is often applied with probability \(p_c\), mutation to each gene with probability \(p_m\). A common start is

\[
p_c\approx0.8\text{--}0.9,\qquad
p_m\approx0.01\text{--}0.1
\]

for binary GAs, but these are not universal. A long chromosome usually needs a much smaller per-bit mutation probability than a short one.

If \(p_m=0\), diversity may collapse. If \(p_m\) is too high, offspring are random and parent information is lost. If \(p_c\) is too high with destructive operators, good blocks are broken.

### 9. Inversion and operator constraints

An operator should respect the intended neighborhood. For a graph, swapping two route positions can create an infeasible edge or enormous cost. Use adjacency-aware crossover, local repair, or a penalty. Feasibility can be enforced in three ways:

1. **Repair:** transform an invalid child into a valid one;
2. **Penalty:** assign a lower fitness while retaining the genotype;
3. **Strict operators:** generate only valid offspring.

A penalty preserves search diversity but may be numerically difficult. Repair can bias the distribution toward repaired solutions.

### 10. Adaptive operators

Operator probabilities can change with generation or measured diversity. When diversity is low, increase mutation or use a restart. When convergence is rapid, reduce destructive crossover. A self-adaptive GA can store operator probabilities in the chromosome and let selection evolve them.

Adaptation must be checked for oscillation and premature exploitation.

### 11. Worked design example

For a 24-bit binary chromosome representing a value in \([0,100]\),

\[
x=\frac{v}{2^{24}-1}100.
\]

If the chromosome is 100000000000000000000000, then

\[
v=2^{23},
\]

so

\[
x=\frac{2^{23}}{2^{24}-1}100\approx50.
\]

This is approximate because the exact encoded resolution is just below 50. A floating-point or Gray-code representation may be preferable when high numerical precision is required.

## Worked examples

### Example 1: One-point crossover

Parents:

\[
P_1=101011,\qquad P_2=011100.
\]

Cut after the third bit:

\[
P_1=101|011,\qquad P_2=011|100.
\]

Children:

\[
C_1=101100,\qquad C_2=011011.
\]

Every child contains one prefix and one suffix from the parents.

### Example 2: Bit-flip mutation

Let

\[
C=101011
\]

and flip positions 2 and 5:

\[
C'=111001.
\]

The expected number of flips is not the mutation rate; it is

\[
Lp_m
\]

for chromosome length \(L\).

### Example 3: Arithmetic crossover

For real parents

\[
P_1=(1,4),\qquad P_2=(3,8)
\]

and \(\alpha=0.25\),

\[
C_1=0.25P_1+0.75P_2=(2.5,7),
\]

\[
C_2=0.75P_1+0.25P_2=(1.5,5).
\]

The children lie between the parents' coordinates.

### Example 4: Permutation repair

Parents:

\[
P_1=(1,2,3,4,5),\qquad
P_2=(4,1,5,2,3).
\]

A naïve one-point cut after position 2 gives

\[
(1,2,5,2,3),
\]

which repeats 2 and omits 4. An order-crossover or repair operator is needed to restore a permutation.

### Example 5: Mutation scale

If parameter \(x_1\) ranges over \([0,1]\) and \(x_2\) over \([0,1000]\), a mutation of \(\pm0.1\) is small for \(x_1\) and negligible for \(x_2\). Use a relative scale or normalize both variables before evolution.

## Key terms & formulas

- **Encoding:** Mapping a solution to a chromosome.
- **Crossover:** Recombination of parent chromosomes.
- **Mutation:** Random change to a gene.
- **One-point crossover:** Exchange suffixes after one cut.
- **Uniform crossover:** Choose each gene from a parent independently.
- **SBX:** Distribution-based real-valued crossover.
- **Permutation repair:** Restore uniqueness and completeness after crossover.
- **Hamming cliff:** Adjacent values separated by many bit changes.

Binary decoding:

\[
x=L+\frac{v}{2^k-1}(U-L).
\]

Expected bit flips:

\[
E[\text{flips}]=kp_m.
\]

Arithmetic crossover:

\[
C_1=\alpha P_1+(1-\alpha)P_2.
\]

## Common mistakes

1. **Using binary crossover for a permutation without repair.** Duplicates and omissions make the chromosome invalid.
2. **Choosing a bit count without checking resolution.** The chromosome may not represent required values accurately.
3. **Using the same mutation probability for every chromosome length.** Long strings may be destroyed.
4. **Applying a fixed mutation size to variables with different scales.** Normalize or scale the perturbation.
5. **Assuming crossover always improves fitness.** It only creates candidates; selection decides.
6. **Using arithmetic crossover when extremes are needed.** It stays between parents and may limit exploration.
7. **Forgetting feasibility handling.** A decoded schedule or route may be invalid.
8. **Using a repair rule that changes the intended distribution.** Compare repaired and penalized approaches.

## Exam prep

### Likely 2-mark questions

- **What is encoding in a GA?**  
  **Hint:** Mapping a solution into a chromosome representation.

- **State the one-point crossover operation.**  
  **Hint:** Cut two chromosomes and exchange their suffixes.

- **Give two mutation operators.**  
  **Hint:** Bit flip, real Gaussian, swap, insertion, or inversion.

- **Why are permutation operators different from binary crossover?**  
  **Hint:** They must preserve all elements exactly once.

- **Write the binary decoding formula.**  
  **Hint:** \(x=L+v(U-L)/(2^k-1)\).

### Likely long-answer questions

- **Explain binary, real, and permutation encodings with examples.**  
  **Hint:** Resolution, direct vectors, validity, operators, and use cases.

- **Describe crossover and mutation operators and their probabilities.**  
  **Hint:** One/two-point, uniform/arithmetic, bit-flip/Gaussian, permutation operators, and \(p_c,p_m\).

- **Work out a complete crossover and mutation run.**  
  **Hint:** Parent strings, cut point, children, flipped positions, and resulting fitness.

- **Explain constraint handling for permutation and schedule GAs.**  
  **Hint:** Repair, penalty, strict operators, and trade-offs.

- **Compare mutation and crossover in terms of exploration and exploitation.**  
  **Hint:** New alleles, recombination, probabilities, and diversity effects.
