---
subject: sc
unit: 4
topic: biological-evolutionary-process
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# Biological Evolutionary Process

## Overview

Biological evolution is the change in inherited characteristics of populations over generations. Individuals are born with variation, compete for limited resources, and reproduce. Individuals whose traits give higher reproductive success tend to leave more descendants, so those traits become more common.

Evolutionary algorithms borrow this process at an abstract level. The analogy helps explain selection, crossover, mutation, fitness, and adaptation, but a computer algorithm is not a literal simulation of biology. The mathematical design chooses operators that suit the problem.

## Explanation

### 1. Biological foundations

#### Genes and alleles

A gene is a segment of DNA associated with a trait. Different versions of a gene are **alleles**. An individual carries a genotype, and its observable characteristics are its phenotype.

In an evolutionary algorithm, a chromosome is a simplified genotype. A decoded solution is analogous to a phenotype, and the objective value is a mathematical fitness.

#### Population and individual

A population is a group of individuals of the same species in the same environment. Individuals vary in their genes and traits. The population is the unit on which evolutionary forces act over generations.

#### Generation and reproduction

A generation is a group of individuals born and living at approximately the same time. Reproduction creates offspring. Sexual reproduction combines genetic material from two parents; asexual reproduction copies an individual with possible mutation.

#### Fitness and natural selection

Fitness in biology means reproductive success, not physical strength. An individual that survives and leaves more offspring contributes more copies of its genes. Natural selection favors heritable traits that improve reproductive success in the current environment.

An algorithm's fitness function is a designed numerical measure. It may represent cost, accuracy, profit, safety, or a combination.

### 2. Sources of variation

#### Mutation

Mutation changes a gene or chromosome. It creates new alleles and can introduce traits not present in the parents. Without mutation, a population can lose the ability to explore new regions and may become trapped.

#### Recombination and crossover

During sexual reproduction, genetic material is reshuffled. Different offspring receive different combinations of parental alleles. This preserves useful material and creates novel combinations.

Crossover is an algorithmic abstraction. It need not follow biological meiosis exactly; the crossover point and representation are chosen by the algorithm designer.

#### Genetic drift

In a finite population, random sampling can change allele frequencies even when fitness differences are small. Algorithms also experience randomness through initialization, selection, and mutation. To reduce harmful drift, maintain diversity and repeat runs.

#### Gene flow

Movement of genes between populations can introduce variation. In distributed algorithms, migration of individuals between subpopulations can serve a similar role.

### 3. Natural selection

Natural selection has several ingredients:

1. **Variation:** individuals differ.
2. **Inheritance:** offspring receive some traits from parents.
3. **Competition:** limited resources favor some individuals.
4. **Differential reproduction:** successful individuals leave more offspring.
5. **Population change:** common traits become more frequent over generations.

The algorithm's selection pressure corresponds to competition, while fitness determines the probability or expected number of offspring.

### 4. Adaptation

An adaptation is a trait that improves performance in a particular environment. It is not universally best. A solution optimized for one data distribution or constraint may be poor after the environment changes.

Algorithm design should therefore test multiple environments and avoid overfitting to one training instance. A high score on a benchmark is not a guarantee of general success.

### 5. Species and niching

A biological species is a group of populations that can interbreed. A niche describes a role or resource-use pattern. In optimization, niches help maintain different solutions instead of allowing one local optimum to dominate.

Niche preservation can be achieved by:

- fitness sharing;
- crowding or deterministic crowding;
- clearing;
- speciation;
- separate subpopulations with migration.

### 6. Mutation and crossover at biological and algorithmic levels

| Biological idea | Algorithmic representation |
|---|---|
| gene/allele | position or gene in a chromosome |
| individual | candidate solution |
| population | set of candidates |
| reproductive success | fitness/objective value |
| inheritance | copying chromosome material |
| recombination | crossover operator |
| mutation | random operator change |
| generation | iteration or epoch |
| environment | objective function and constraints |

This table is an analogy, not a claim that an objective function is a complete habitat.

### 7. Selection pressure

High selection pressure quickly favors the best current candidates but can remove diversity. Low selection pressure preserves more alternatives but may take longer to improve.

Roulette selection can give a candidate a large probability when it has a high normalized fitness. Tournament selection compares a small sample and is less sensitive to the numerical scale of fitness. Rank selection changes only the order, not the magnitude of differences.

### 8. Genetic diversity

Diversity can be measured by:

- number of unique chromosomes;
- average pairwise distance;
- entropy of alleles;
- variance of fitness or decision variables;
- number of occupied niches.

If diversity collapses, the search may be trapped. Mutation, crossover, random immigrants, niching, and adaptive operators can restore it.

### 9. Fitness function design

A biological fitness is contextual. In an algorithm, the objective may be multiobjective or constrained. Common forms are

\[
f(x)=f_0(x)-P(x)
\]

for penalty, or

\[
f(x)=w_1\text{accuracy}-w_2\text{time}-w_3\text{energy}
\]

for a weighted objective. Weight choices change the answer and should be justified with stakeholders or a decision model.

Do not optimize a proxy objective that fails to represent the actual goal. A solution with a good score may be unsafe, unfair, or infeasible.

### 10. Generational versus steady-state models

#### Generational model

A whole new population is generated each generation. Common and easy to parallelize.

#### Steady-state model

One or a few offspring replace individuals in the current population each iteration. It can preserve a good solution but may converge faster to a local region.

### 11. Parallel and distributed evolution

Population members can be evaluated in parallel. A model can also use geographic subpopulations. Migration exchanges migrants and can maintain diversity, but too much migration can destroy local adaptation.

### 12. Limits of the biological analogy

A computer chromosome may represent a schedule, route, or network. Fitness is calculated exactly, unlike the noisy biological environment. Mutation and crossover are not physically meaningful mutations. Thus the useful part is the abstract cycle, not a claim that evolution is simulated in full detail.

## Worked examples

### Example 1: Fitness and inheritance

Suppose two candidate designs have objective costs

\[
J_1=8,\quad J_2=3.
\]

Convert cost to fitness:

\[
f_1=\frac1{8+0.1}=0.123,\quad
f_2=\frac1{3+0.1}=0.323.
\]

Normalized selection probabilities are

\[
p_1=\frac{0.123}{0.446}=0.276,\quad
p_2=0.724.
\]

Design 2 is more likely to be selected because it is better. The probabilities are not the fraction of biological traits; they are a selection convention.

### Example 2: Crossover creates a novel combination

Parents are

\[
P_1=10110,\qquad P_2=01101.
\]

One-point crossover after position 3 gives

\[
101|10,\qquad011|01
\]

and offspring

\[
C_1=10101,\qquad C_2=01110.
\]

Both contain a combination not exactly equal to either parent. This is the algorithmic role of recombination.

### Example 3: Mutation restores diversity

If a population contains only

\[
0000,\quad0001,\quad0010,
\]

crossover can create only a limited set of nearby strings. A mutation from 0000 to 0100 introduces a new bit. Repeated mutation can explore unseen regions.

### Example 4: Constraint and environmental change

A route optimizer is trained with fuel cost as its objective. When a road closes, the old route may be invalid or expensive. Re-evaluate candidates under the new environment; evolutionary search can then adapt the population rather than assuming the old fitness is still meaningful.

## Key terms & formulas

- **Gene:** Heritable unit or position in a representation.
- **Allele:** Alternative value at a gene position.
- **Genotype:** Encoded genetic representation.
- **Phenotype:** Decoded expressed characteristic.
- **Fitness:** Reproductive success in biology; objective score in an algorithm.
- **Natural selection:** Differential reproduction caused by inherited variation.
- **Mutation:** Random change introducing variation.
- **Recombination:** Reshuffling parental material.
- **Genetic drift:** Random change in allele frequencies.

Algorithm fitness conversion:

\[
f(x)=\frac1{J(x)+\epsilon}
\]

for minimizing cost \(J\).

Selection probability:

\[
p_i=\frac{f_i}{\sum_jf_j}.
\]

Generation:

\[
P_{t+1}=\operatorname{replace}(P_t,\operatorname{vary}(\operatorname{select}(P_t))).
\]

## Common mistakes

1. **Equating fitness with physical strength.** Biological fitness means reproductive success.
2. **Treating crossover as guaranteed improvement.** It creates variation; fitness decides what survives.
3. **Ignoring mutation.** Without it, a population can lose diversity.
4. **Assuming evolution always finds the best solution.** Selection is conditional and finite.
5. **Confusing genetic drift with deliberate selection.** Drift is random sampling change.
6. **Treating a chromosome as automatically meaningful.** The representation must match the problem.
7. **Assuming a trait is always beneficial.** Adaptation depends on the environment.
8. **Using a proxy fitness without validating the real goal.** A high score may not mean a good solution.

## Exam prep

### Likely 2-mark questions

- **What is biological fitness?**  
  **Hint:** Contribution to the next generation through reproduction, not physical strength.

- **Name two sources of genetic variation.**  
  **Hint:** Mutation and recombination; gene flow and drift are also valid.

- **Map four biological terms to evolutionary-algorithm terms.**  
  **Hint:** Gene→position, individual→candidate, population→population, fitness→objective score.

- **State the four conditions needed for natural selection.**  
  **Hint:** Variation, inheritance, competition, and differential reproduction.

- **Why is mutation necessary in an evolutionary algorithm?**  
  **Hint:** It introduces new variation and helps prevent premature convergence.

### Likely long-answer questions

- **Explain the biological basis of evolutionary computing.**  
  **Hint:** Genes, alleles, variation, fitness, selection, reproduction, and generation, followed by algorithmic mapping.

- **Compare natural selection and algorithmic selection.**  
  **Hint:** Reproductive success versus objective scoring, stochastic choices, and environment.

- **Explain genetic drift, gene flow, and niching in biological and algorithmic terms.**  
  **Hint:** Random frequency changes, migration, and maintenance of distinct subpopulations.

- **Discuss how biological concepts are adapted in a GA and where the analogy is limited.**  
  **Hint:** Encoding, fitness, operators, and mathematical versus environmental context.
