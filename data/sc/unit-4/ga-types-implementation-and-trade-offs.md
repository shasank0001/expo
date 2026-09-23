---
subject: sc
unit: 4
topic: ga-types-implementation-and-trade-offs
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# GA Types, Implementation, and Trade-Offs

## Overview

Genetic algorithms are not one fixed configuration. They can be classified by representation, selection, variation, replacement, adaptation, and objective. The same problem may work well with a binary GA, a real-valued GA, or a permutation GA; choosing the wrong type can make valid search neighborhoods difficult to reach.

Implementation adds practical issues: feasibility, stochastic reproducibility, population diversity, evaluation cost, stopping, and safe handling of invalid candidates. This note summarizes the main GA types and trade-offs.

## Explanation

### 1. Classification by representation

#### Binary GA

Chromosome:

\[
g\in\{0,1\}^k.
\]

Use bit-flip mutation and one/two-point/uniform crossover. Suitable for feature subsets, bit decisions, and small discretized problems. Resolution depends on bit length.

#### Real-valued GA

Chromosome:

\[
\mathbf x\in\mathbb R^d.
\]

Use arithmetic or blend crossover and Gaussian/uniform mutation. Suitable for continuous engineering parameters. It avoids binary rounding but needs bounds and scale-aware mutation.

#### Permutation GA

Chromosome is an ordering of \(n\) items. Use OX, CX, PMX, swap, insertion, or inversion. Suitable for routes, schedules, and assignment. Ordinary bit crossover is invalid.

#### Tree/program GA

Chromosome is a syntax tree. Use subtree crossover and mutation. Suitable for symbolic regression and program discovery, but syntax and evaluation can be expensive.

### 2. Classification by selection

- **Fitness proportional:** roulette-wheel or SUS.
- **Ordinal:** rank selection.
- **Sample based:** tournament selection.
- **Threshold:** truncation selection.
- **Multi-objective:** nondominated sorting, crowding, or niching.

Selection pressure should be compatible with diversity requirements. A tournament of size 2 is usually moderate; a large tournament or truncation is strong.

### 3. Classification by variation

- One-point, two-point, uniform, order, arithmetic, and SBX crossover.
- Bit-flip, Gaussian, uniform, swap, insertion, inversion, and subtree mutation.
- Rejection, repair, and projection operators for feasibility.

The operator is not independent of representation. A good operator creates meaningful nearby solutions and preserves important blocks.

### 4. Classification by replacement

#### Generational

All parents are replaced by offspring. Easy to understand and parallelize, but the best parent may disappear unless elites are copied.

#### Steady-state

One or a few offspring enter the current population and replace a selected or worst individual. Uses evaluations efficiently, but selection and diversity are more sensitive.

#### Elitist

Best individuals are copied unchanged. Prevents regression in the best score but can cause premature convergence.

### 5. Classification by adaptation

#### Fixed-parameter GA

Population size, \(p_c\), \(p_m\), and selection pressure remain constant. Simple and reproducible, but not adaptive to the search stage.

#### Adaptive GA

Parameters change according to generation, fitness improvement, or diversity. For example, increase mutation when diversity is low.

#### Self-adaptive GA

Operator probabilities and mutation ranges are encoded in each chromosome and evolve through selection. The search can discover useful operator settings, but the extra genes add complexity.

### 6. Single- and multiobjective GA

A single-objective GA ranks candidates by one score. A multiobjective GA handles conflicting objectives using:

- weighted scalarization;
- Pareto dominance and nondominated sorting;
- crowding distance;
- niching and archives.

NSGA-II is a common example. It maintains a spread of nondominated solutions rather than one arbitrary weighted answer.

### 7. Implementation workflow

1. State the optimization objective and constraints.
2. Choose a chromosome and decoder.
3. Decide whether a valid chromosome is guaranteed.
4. Choose fitness and scale it safely.
5. Initialize a diverse population.
6. Select parents.
7. Apply representation-aware crossover and mutation.
8. Repair or penalize invalid offspring.
9. Evaluate and replace, possibly with elitism.
10. Monitor best, mean, and diversity.
11. Stop using a budget and repeat with multiple seeds.

### 8. Feasibility implementation

A decoder can produce an invalid object from a binary string if weights or timing constraints are violated. Options:

- penalty;
- repair;
- rejection;
- specialized feasible operators.

For a penalty, use feasibility-dominance rules before objective comparison. This prevents a high objective score from hiding a hard violation.

### 9. Pseudocode

```text
P = initialize(population_size)
evaluate(P)
best_global = best(P)
for generation = 1 to max_generations:
    parents = select(P)
    offspring = crossover(parents, pc)
    offspring = mutate(offspring, pm)
    offspring = repair_or_penalize(offspring)
    evaluate(offspring)
    P = replacement(P, offspring, elites)
    if mean_diversity(P) < threshold and no_improvement:
        inject_random_individuals_or_restart()
    best_global = best(best_global, best(P))
    if best_global >= target or budget_exhausted:
        break
return best_global
```

### 10. Choosing population size

A small population is cheap per generation but may lose diversity. A large population provides more selection information and parallelism but costs more memory and fitness evaluations. If each evaluation is a simulation, a moderate population with good parallelization may be preferable.

A common starting range is 20–200, but it is not a rule. Use the number of variables, encoding, and budget to guide experiments.

### 11. Choosing mutation and crossover

For binary GAs, per-bit mutation should be much smaller for long chromosomes. For real vectors, mutation magnitude should reflect the variable range. For permutations, crossover should preserve validity and mutation should make a small order change.

Measure the fraction of feasible offspring, diversity, and improvement per evaluation. A high crossover rate is not automatically good.

### 12. Stopping criteria

Use more than one criterion:

- maximum generations;
- maximum objective evaluations;
- target fitness;
- no improvement for a number of generations;
- time or memory limit;
- convergence of population diversity.

A target fitness must be meaningful. A synthetic benchmark score can encourage overfitting.

### 13. Reproducibility

Record the random seed, software/library version, chromosome decoder, objective implementation, parameters, and number of runs. A GA result should be reported as a distribution, for example best/mean/median over 20–30 runs if the budget allows.

### 14. Trade-offs

| Choice | Benefit | Cost/risk |
|---|---|---|
| Large population | more diversity and parallel samples | more memory/evaluations |
| High crossover | recombines building blocks | can destroy good blocks |
| High mutation | explores new regions | destroys inherited structure |
| Strong selection | rapid exploitation | premature convergence |
| Elitism | preserves best | reduces diversity |
| Repair | maintains feasibility | may bias search |
| Penalty | preserves genotype variety | needs well-chosen penalty |
| Real encoding | precise continuous values | needs bounds/scaling |
| Binary encoding | simple operators | resolution and Hamming cliffs |
| Multiobjective selection | exposes trade-offs | larger, more complex fronts |

### 15. Failure diagnosis

#### No improvement

Check whether the population is collapsed, the fitness is wrong, mutation is ineffective, or the representation cannot reach the target. Test the decoder and inspect a few chromosomes.

#### Invalid offspring

Use a strict operator or repair. Do not silently let the optimizer compare invalid objects with valid ones.

#### Excellent training fitness, poor test score

The problem is overfitting, a distribution shift, or a proxy objective. Hold out independent data and test on new environments.

#### Very slow runs

Profile the objective and operators. Reduce population or output resolution only after checking whether a smaller budget sacrifices the needed accuracy.

## Worked examples

### Example 1: Choosing a GA type

For a vehicle route with 30 cities, a permutation GA with OX and inversion mutation is natural. A binary GA would require an awkward subset representation. For a five-variable motor-controller gain, a real GA with Gaussian mutation is simpler and more precise.

### Example 2: Repair a binary capacity chromosome

A chromosome encodes three item weights:

\[
(1,0,1)
\]

with total weight exceeding capacity. A repair operator flips selected bits until the capacity constraint holds. If the repair always removes the first feasible bit, the search may favor later items. A random repair or a penalty preserves more variation.

### Example 3: Diagnose premature convergence

Population diversity drops from 80% unique chromosomes to 2%, while the best score stalls. Use lower tournament size, inject random immigrants, or increase mutation temporarily. Do not immediately add more generations; they will only repeat the same population.

### Example 4: Multiobjective output

A design has cost 100 and error 5; another has cost 130 and error 2. Neither dominates. A multiobjective GA should retain both in the nondominated set. A weighted score could choose one, but stakeholders should see the trade-off.

## Key terms & formulas

- **Binary GA:** Bit-string representation.
- **Real GA:** Continuous-vector representation.
- **Permutation GA:** Order-preserving representation.
- **Adaptive GA:** Parameters change during search.
- **Self-adaptive GA:** Operator parameters are encoded and evolved.
- **Generational replacement:** Replace the whole population.
- **Steady-state replacement:** Replace a few individuals.
- **NSGA-II:** Multiobjective GA using nondominated rank and crowding.

Nondomination:

\[
x\prec y \iff
J_i(x)\le J_i(y)\ \forall i,\quad
J_j(x)<J_j(y)\text{ for some }j.
\]

Selection diversity measure:

\[
D=\frac{\#\text{unique chromosomes}}{\#\text{chromosomes}}.
\]

## Common mistakes

1. **Choosing binary encoding for a continuous problem without checking resolution.** Precision may be poor.
2. **Using crossover that creates invalid permutations.** Use valid operators.
3. **Using a mutation probability copied from another chromosome length.** Scale it.
4. **Adding elites without monitoring diversity.** Premature convergence may follow.
5. **Using a penalty so large that all values overflow.** Use feasibility-dominance or stable scaling.
6. **Reporting a single best run.** Use repeated runs and a seed.
7. **Confusing an adaptive parameter with a problem parameter.** Record all settings.
8. **Stopping only at a fixed generation count.** Include evaluation budget and no-improvement criteria.

## Exam prep

### Likely 2-mark questions

- **Classify GAs by representation.**  
  **Hint:** Binary, real, permutation, tree/program, and rule-based.

- **What is a self-adaptive GA?**  
  **Hint:** Operator parameters are encoded in the chromosome and evolved.

- **State one trade-off of elitism.**  
  **Hint:** Preserves the best but may reduce diversity.

- **Name two replacement strategies.**  
  **Hint:** Generational, steady-state, or elitist replacement.

- **What does a multiobjective GA return?**  
  **Hint:** A set of nondominated/Pareto solutions.

### Likely long-answer questions

- **Classify genetic algorithms and compare their operators.**  
  **Hint:** Representation, selection, crossover, mutation, replacement, and multiobjective classes.

- **Explain a practical GA implementation workflow.**  
  **Hint:** Encoding, fitness, feasibility, initialization, operators, monitoring, stopping, and repeatability.

- **Discuss the trade-offs between population size, selection pressure, crossover, mutation, and elitism.**  
  **Hint:** Exploration/exploitation, diversity, cost, and premature convergence.

- **Explain how to diagnose a GA that fails to improve.**  
  **Hint:** Check decoder, fitness, constraints, diversity, representation, rates, and budget.
