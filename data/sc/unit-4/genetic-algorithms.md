---
subject: sc
unit: 4
topic: genetic-algorithms
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# Genetic Algorithm

## Overview

A genetic algorithm (GA) solves optimization problems by evolving a population of encoded candidate solutions. It repeatedly selects parents, combines them through crossover, changes them through mutation, evaluates the offspring, and forms a new population.

The method is derivative-free and can handle complex representations, but its success depends on encoding, fitness, selection, operator rates, diversity, and stopping. A GA is a stochastic heuristic and does not guarantee the global optimum.

## Explanation

### 1. Formal cycle

For a problem

\[
\min_{\mathbf x\in\mathcal S}J(\mathbf x),
\]

a GA maintains a population

\[
P_t=\{\mathbf x_{t,1},\ldots,\mathbf x_{t,P}\}.
\]

The cycle is:

1. encode a population of candidate solutions;
2. evaluate each candidate's fitness;
3. select parents;
4. apply crossover;
5. apply mutation and repair;
6. evaluate offspring;
7. replace or merge with the parent population;
8. stop and return the best.

### 2. Representation and initialization

A chromosome may be:

- a binary string;
- a real-valued vector;
- a permutation;
- a tree or rule sequence;
- a graph or schedule.

The initial population is

\[
P_0=\{g_1,\ldots,g_P\},
\]

generated randomly or using domain knowledge. Initial diversity is valuable. Seeding some known good solutions can speed convergence but may make the population too similar and reduce exploration.

### 3. Fitness function

Selection usually maximizes a score. If minimizing cost \(J\), use

\[
f=\frac1{J+\epsilon}
\]

or rank candidates. A constrained objective may be

\[
f(\mathbf x)=f_0(\mathbf x)
-\lambda_1P_1(\mathbf x)-\lambda_2P_2(\mathbf x),
\]

where each \(P_i\ge0\) is a violation.

The fitness must measure the actual goal. A proxy that rewards a solution for a narrow benchmark can produce a poor real-world design.

### 4. Selection

Parent-selection methods include:

- roulette wheel;
- rank;
- tournament;
- truncation;
- stochastic universal sampling.

Selection increases the frequency of high-fitness material but can reduce diversity. A tournament of size \(q\) gives strong pressure; a small rank distribution gives lower pressure.

### 5. Crossover

Crossover combines parts of parents. For binary chromosomes, one-point crossover cuts each string and exchanges suffixes. For real vectors, arithmetic crossover interpolates between parents. For permutations, order crossover or PMX preserves validity.

Crossover probability \(p_c\) controls how often recombination is applied. It should be high enough to combine useful building blocks but not so high that it repeatedly destroys them.

### 6. Mutation

Mutation injects new information by changing a gene. Examples:

- bit-flip mutation for binary strings;
- Gaussian or uniform perturbation for real vectors;
- swap, insertion, or inversion for permutations.

Mutation probability \(p_m\) and mutation magnitude control the amount of random change. A common mistake is to use a per-gene probability that is too high for a long chromosome.

### 7. Replacement and elitism

Possible replacement rules include:

#### Generational replacement

\[
P_{t+1}=\{\text{offspring}\}.
\]

#### Steady-state replacement

A few offspring replace selected or worst parents in the current population.

#### Elitist replacement

Copy the best \(E\) individuals unchanged:

\[
P_{t+1}
=
\operatorname{Elite}_E(P_t)
\cup
\operatorname{Offspring}.
\]

Elitism prevents loss of the best fitness, but too many elites can make the population converge prematurely.

### 8. Constraints

A GA may generate invalid routes, schedules, or parameter assignments. Common methods are:

- penalty functions;
- repair after decoding;
- feasibility-preserving operators;
- constrained selection;
- reject-and-resample.

A penalty must be large enough to deter invalid solutions but not so large that all fitness calculations become numerically unstable. Repair can create bias; a pure penalty preserves genotype diversity but may waste evaluations.

### 9. Genetic algorithm for maximization

For a fitness-maximization problem, select high fitness and keep the best. The algorithm is the same as minimization after converting or reversing the objective.

For minimization, a common transformation is

\[
f_i=\frac1{J_i+\epsilon},
\]

where \(\epsilon>0\) avoids division by zero. If \(J_i\) can be negative, use a shift or rank selection.

### 10. Fitness scaling and niching

Roulette selection can be affected by score magnitude. Linear scaling, power scaling

\[
f_i' = f_i^\alpha,
\]

or rank selection changes selection pressure. A power \(\alpha>1\) for positive fitness makes the best candidates more likely.

Niching methods—fitness sharing, crowding, and clearing—reduce competition among similar solutions. They are useful in multimodal problems where several good optima should be maintained.

### 11. Parallel evaluation

If the population has \(P\) members, their fitness evaluations can often run in parallel. The generation barrier means the next selection waits for the whole batch unless a steady-state method is used.

Parallel speedup depends on overhead and the cost of an individual evaluation. A simulation-based objective may be more expensive than the genetic operators.

### 12. Control parameters

Important parameters are:

- population size;
- crossover probability;
- mutation probability;
- mutation magnitude;
- selection pressure;
- elite count;
- stopping generations and function evaluations.

No universally best setting exists. Use a budget, pilot runs, adaptive control, and validation. Record the seed and number of independent runs.

### 13. Premature convergence

Premature convergence occurs when the population loses diversity and focuses on a local or poor solution. Signs include:

- a small number of unique chromosomes;
- nearly identical fitness values;
- continued mutation that cannot improve the mean;
- a very fast best-score curve followed by a plateau.

Remedies include:

- lower selection pressure;
- avoid excessive elitism;
- increase mutation or use adaptive mutation;
- fitness sharing or niching;
- random immigrants or restarts;
- larger population;
- better representation.

### 14. Types of GA

A GA may be classified by:

- representation: binary, real, permutation, tree;
- selection: roulette, rank, tournament, truncation, SUS;
- crossover: one-point, two-point, uniform, arithmetic, order, PMX;
- mutation: bit-flip, Gaussian, swap, insertion, inversion;
- replacement: generational, steady-state, elitist;
- objective: single or multiobjective;
- adaptation: fixed or self-adaptive parameters.

Some classifications overlap because a GA is defined by its complete combination of choices rather than one operator.

### 15. Genetic algorithm workflow

A reproducible implementation should:

1. state the problem and representation;
2. define feasibility and fitness;
3. seed and initialize;
4. evaluate;
5. select;
6. vary and repair;
7. replace;
8. log best/mean/diversity;
9. stop;
10. validate the best feasible solution;
11. repeat with multiple seeds.

### 16. Applications

GAs are used in scheduling, routing, machine layout, feature selection, parameter tuning, network optimization, game strategies, VLSI placement, and design synthesis. They are especially useful when the objective can be evaluated but a good analytical search method is difficult.

## Worked examples

### Example 1: Maximize a binary function

Maximize the number of 1 bits in a 4-bit string. Fitness is

\[
f(g)=\text{number of ones in }g.
\]

Initial population:

\[
0000,\quad1010,\quad1110,\quad0111.
\]

Fitnesses are 0, 2, 3, 3. Selection favors the last two. A one-point crossover between 1010 and 1110 after position 2 can produce 1010 or 1110, while mutation of 0000 can produce new strings. Eventually a high-fitness string such as 1111 may appear, although the exact run depends on random choices.

### Example 2: Real-valued minimization

Minimize

\[
J(x,y)=x^2+y^2
\]

over \([-5,5]^2\). A real chromosome is \((x,y)\). Initial candidates \((4,3)\) and \((-2,1)\) have costs 25 and 5. Arithmetic crossover with \(\alpha=0.5\) gives

\[
(1,2)
\]

with cost 5. Gaussian mutation may then produce \((0.8,2.1)\), which has cost 5.05; selection retains the better parent. The run can improve toward \((0,0)\) but may settle at a nearby point.

### Example 3: Constraint penalty

Minimize travel time \(T\) subject to a vehicle capacity constraint. If a candidate violates capacity by \(v\), use

\[
f=\frac1{T+10v+\epsilon}.
\]

A slightly faster but infeasible route receives lower fitness than a feasible route. The coefficient 10 should be tuned; too small permits violations, too large can make the search avoid all candidates near the feasible boundary.

## Key terms & formulas

- **GA:** Genetic algorithm.
- **Chromosome:** Encoded candidate solution.
- **Population:** Set of chromosomes.
- **Fitness:** Selection score.
- **Crossover:** Recombination.
- **Mutation:** Random change.
- **Elitism:** Preserve best chromosomes.
- **Premature convergence:** Loss of useful diversity.

Maximization selection:

\[
p_i=\frac{f_i}{\sum_jf_j}.
\]

Minimization conversion:

\[
f_i=\frac1{J_i+\epsilon}.
\]

Elitist next population:

\[
P_{t+1}=\operatorname{Elite}_E(P_t)\cup O_t.
\]

## Common mistakes

1. **Forgetting that GA usually maximizes selection fitness.** Convert minimization objectives.
2. **Using a chromosome representation that cannot express the required solution.** Check all variables and constraints.
3. **Applying binary crossover to a permutation without repair.** Feasibility fails.
4. **Using one mutation probability blindly.** Scale by chromosome length and representation.
5. **Overusing elitism.** The best survives, but diversity may vanish.
6. **Claiming a GA is deterministic.** Initialization and operators are usually random.
7. **Ignoring the evaluation budget.** Large populations and many generations may be too expensive.
8. **Reporting only the best of one run.** Use repeated seeds and summary statistics.
9. **Using no stopping criterion.** An endless run never produces a final answer.

## Exam prep

### Likely 2-mark questions

- **Define a genetic algorithm.**  
  **Hint:** Population-based search using selection, crossover, mutation, and fitness.

- **List the main steps of a GA.**  
  **Hint:** Initialization, evaluation, selection, crossover, mutation, replacement, termination.

- **State the role of elitism.**  
  **Hint:** Preserve the best solutions unchanged.

- **What is premature convergence?**  
  **Hint:** Premature loss of diversity and convergence to a poor or local solution.

- **Give two GA representations.**  
  **Hint:** Binary, real, permutation, tree, or rule sequence.

### Likely long-answer questions

- **Explain the complete operation of a genetic algorithm.**  
  **Hint:** Representation, fitness, selection, variation, replacement, constraints, and stopping.

- **Compare different selection and variation methods in a GA.**  
  **Hint:** Roulette, rank, tournament, crossover, mutation, diversity, and probabilities.

- **Discuss applications, advantages, and limitations of GAs.**  
  **Hint:** Derivative-free search, representation dependence, cost, stochasticity, and no guarantee.

- **Explain how constraints and premature convergence are handled.**  
  **Hint:** Penalty, repair, strict operators, diversity, elitism, immigration, and restarts.
