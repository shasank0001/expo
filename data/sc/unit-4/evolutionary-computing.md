---
subject: sc
unit: 4
topic: evolutionary-computing
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# Introduction to Evolutionary Computing

## Overview

Evolutionary computing is a family of optimization methods inspired by biological evolution. They maintain candidate solutions, evaluate their quality with a fitness function, and repeatedly apply selection and variation. Better solutions tend to leave more offspring, so useful information accumulates over generations.

The main members of the syllabus are evolutionary algorithms, evolutionary strategies, evolutionary programming, genetic algorithms, and swarm intelligence. A genetic algorithm usually uses a population of encoded chromosomes, whereas an evolutionary strategy emphasizes mutation and self-adaptation of strategy parameters.

Evolutionary computing is useful for nonlinear, discontinuous, constrained search problems where exact derivatives are unavailable. It does not guarantee the global optimum and must be designed with a meaningful representation, objective, diversity mechanism, and stopping rule.

## Explanation

### 1. Definition and motivation

An evolutionary algorithm is a population-based metaheuristic that improves candidate solutions through repeated evaluation and variation. It is appropriate when:

- the search space is large or difficult to enumerate;
- the objective is non-differentiable, discontinuous, or noisy;
- a good solution is more important than a formal proof;
- many independent candidate evaluations can be performed;
- constraints can be represented by a score or repaired.

A simple evolutionary loop is

\[
P_0 \rightarrow \text{evaluate} \rightarrow \text{select}
\rightarrow \text{vary} \rightarrow P_1 \rightarrow\cdots.
\]

### 2. Core components

#### Representation

A solution is encoded as a chromosome, individual, or strategy vector. A genetic algorithm commonly uses a binary string, real-valued vector, permutation, tree, or rule set. The representation must permit meaningful variation and must not make every feasible solution inaccessible.

#### Initialization

An initial population \(P_0=\{x_1,\ldots,x_P\}\) is generated. Random initialization gives broad coverage; domain-specific initialization can include known good solutions. A diverse starting population is important because a poor or clustered population can lead to premature convergence.

#### Fitness function

The fitness function maps a candidate to a quality score:

\[
f(x_i)\in\mathbb R.
\]

Most selection methods are easiest to define when larger fitness is better. If the objective is a cost \(J(x)\) to minimize, convert it:

\[
f(x)=\frac{1}{J(x)+\epsilon}
\]

or use rank selection. The fitness should reflect the real goal, including relevant penalties.

#### Selection

Selection favors fitter individuals to become parents. Methods include roulette-wheel, rank, tournament, truncation, and SUS. Selection alone reduces diversity, so it must be balanced with variation.

#### Variation

Variation creates new candidates:

- **crossover/ recombination** combines parts of parents;
- **mutation** changes individual components;
- other operators use insertion, inversion, permutation, or path operators for specialized representations.

#### Replacement and elitism

After producing offspring, the next population may be formed by replacing the parents, replacing the worst, or keeping the best. Elitism copies one or more best solutions into the next generation and prevents valuable information from being lost.

#### Termination

Stop after a maximum number of generations/evaluations, after a target fitness is reached, or when the best result has not improved for a specified number of generations. An excessive stopping rule can waste time; too early a rule returns an unconverged result.

### 3. A generic pseudo-algorithm

```text
Generate initial population P
evaluate fitness of every individual
repeat:
    select parents using fitness
    apply crossover with probability pc
    apply mutation with probability pm
    repair/project candidates if needed
    evaluate offspring
    P = replacement(P, offspring) with elitism if used
until stopping condition
return best individual and its fitness
```

The implementation must log the best, mean, and diversity measures. A decreasing best score without falling diversity can signal premature convergence.

### 4. Determinism and stochasticity

Initialization, selection, crossover, and mutation usually contain random choices. Fixing a seed can make a run reproducible, but it does not make the method globally deterministic across implementations. Report the number of independent runs and the distribution of results.

### 5. Exploration versus exploitation

**Exploitation** intensifies search around good solutions. Selection and elitism do this.

**Exploration** samples less-known regions. Random initialization, mutation, diversity maintenance, tournament selection, and adaptive population sizes help.

Too much exploitation causes premature convergence. Too much exploration wastes evaluations on poor solutions. A successful method balances them through operator probabilities, population diversity, niching, or restart policies.

### 6. Constraint handling

A common penalty method defines

\[
f(x)=f_0(x)-\lambda P(x),
\]

where \(P(x)\ge0\) measures constraint violation. Penalizing too little permits invalid solutions; penalizing too much can make the search infeasible.

Other methods include:

- repair or projection;
- feasibility rules;
- specialized operators;
- constrained selection;
- multi-objective handling.

A chromosome that decodes to an invalid object must be rejected, repaired, or assigned a defined score. Never allow hidden invalid states to reach the objective.

### 7. Applications

Evolutionary methods are used for:

- function and combination optimization;
- scheduling and routing;
- vehicle routing and travelling-salesperson-like problems;
- network design;
- feature selection;
- parameter tuning of neural, fuzzy, and control models;
- shape and structural design;
- VLSI and circuit design;
- multi-objective engineering design;
- game playing and agent strategies.

The method is attractive when the objective is easy to evaluate but the space of valid solutions is difficult to search.

### 8. Advantages

- Works without derivatives.
- Can search large and nonlinear spaces.
- Uses multiple candidate solutions in parallel.
- Handles complex encodings and constraints.
- Can exploit both local and global information.
- Is relatively easy to parallelize independent evaluations.
- Can produce a useful solution when a global guarantee is unavailable.

### 9. Limitations

- Stochastic and may return different answers.
- No general guarantee of the global optimum.
- Expensive when each fitness evaluation is costly.
- Encoding, fitness, and operators strongly affect performance.
- Can converge prematurely to a local solution.
- Parameters such as population size and mutation rate are difficult to tune.
- Constraints and reproducibility require explicit care.

## Worked examples

### Example 1: Minimize a one-dimensional function

Minimize

\[
J(x)=(x-3)^2,\qquad x\in[0,8].
\]

Use a real-valued chromosome and fitness

\[
f(x)=\frac{1}{J(x)+0.1}.
\]

If candidates are \(x=2,3,4\), their costs are \(1,0,1\), and fitness values are

\[
0.9091,\quad 10,\quad 0.9091.
\]

A selection method is much more likely to choose \(x=3\). Mutation around good values can generate candidates such as 2.8 or 3.2, after which selection can improve them.

### Example 2: Constraint penalty

Maximize

\[
f_0(x)=x
\]

subject to \(x\le5\), with integer chromosome \(x\in[0,10]\). For violation \(P(x)=\max(0,x-5)\),

\[
f(x)=x-\lambda P(x).
\]

With \(\lambda=2\):

- \(x=5\): \(f=5\);
- \(x=7\): \(f=7-2(2)=3\);
- \(x=10\): \(f=10-2(5)=0\).

The penalty makes the boundary solution preferable to clearly invalid values. The penalty coefficient is a modeling choice and should be tested.

### Example 3: Exploration and exploitation

If a population of 20 contains 19 copies of the best solution and one different solution, selection and crossover will produce nearly identical children. A local optimum may be repeated forever. Increase mutation, use tournament selection with a diversity-aware replacement rule, or restart from a new region.

## Key terms & formulas

- **Evolutionary computing:** Nature-inspired population-based optimization.
- **Individual:** Candidate solution.
- **Population:** Set of candidates processed together.
- **Chromosome:** Encoded representation of an individual.
- **Fitness:** Quality score used by selection.
- **Selection:** Choosing parents for reproduction.
- **Crossover:** Recombining parents.
- **Mutation:** Random change to an individual.
- **Elitism:** Preserving the best individuals.

Generic update:

\[
P_{t+1}=\operatorname{replace}\left(S(P_t),V(P_t)\right).
\]

Penalized fitness:

\[
f(x)=f_0(x)-\lambda P(x).
\]

## Common mistakes

1. **Calling evolutionary algorithms random search.** Selection and inheritance create directed search.
2. **Using a minimization cost directly as larger-is-better fitness.** Convert or use rank selection.
3. **Ignoring representation.** A bad encoding makes valid neighborhoods impossible.
4. **Using too little diversity.** Premature convergence is common.
5. **Using no penalty or repair for constraints.** Invalid offspring need an explicit treatment.
6. **Claiming a global optimum is guaranteed.** It is generally a heuristic search.
7. **Tuning only the mutation rate.** Population size, selection, encoding, initialization, and stopping also matter.
8. **Reporting one run without a seed or variability.** Stochastic results need repeats or uncertainty summaries.

## Exam prep

### Likely 2-mark questions

- **Define evolutionary computing.**  
  **Hint:** Population-based optimization inspired by biological evolution.

- **List the main components of an evolutionary algorithm.**  
  **Hint:** Representation, initialization, fitness, selection, variation, replacement, and termination.

- **What is the role of a fitness function?**  
  **Hint:** It ranks candidates and directs selection.

- **Give two applications of evolutionary algorithms.**  
  **Hint:** Scheduling, routing, tuning, design, feature selection.

- **State one limitation of evolutionary search.**  
  **Hint:** No global guarantee, stochasticity, cost, or premature convergence.

### Likely long-answer questions

- **Explain the structure and operation of an evolutionary algorithm.**  
  **Hint:** Complete cycle, operators, constraints, termination, and exploration/exploitation.

- **Compare evolutionary computing with conventional gradient optimization.**  
  **Hint:** Derivatives, local versus population search, constraints, guarantees, and cost.

- **Discuss advantages and limitations of evolutionary computing with applications.**  
  **Hint:** Parallel search, derivative-free operation, encoding, cost, and stochasticity.

- **Explain constraint handling and premature convergence in an evolutionary algorithm.**  
  **Hint:** Penalties, repair, diversity, elitism, and parameter choices.
