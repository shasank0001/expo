---
subject: sc
unit: 4
topic: ga-example-implementation
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# GA Example Implementation

## Overview

A complete genetic-algorithm example is the best way to connect the syllabus operators: representation, initialization, fitness, selection, crossover, mutation, replacement, and termination. This note implements a small binary GA for a feature-selection or maximum-ones problem, then shows a more realistic constrained example.

The numerical run is intentionally small so every parent, probability, cut point, and offspring can be checked by hand. A real implementation should use the same sequence with configurable population size, probabilities, and stopping criteria.

## Explanation

## Worked examples

### 1. Problem statement

Maximize the number of selected features in a 6-bit vector, but require at least two selected features. The unconstrained objective is

\[
J(\mathbf g)=\sum_{i=1}^{6}g_i.
\]

The constraint can be handled by a penalty:

\[
f(\mathbf g)
=
J(\mathbf g)-10\max(0,2-J(\mathbf g)).
\]

Thus fewer than two selected features receive a penalized score, while feasible strings receive the ordinary count.

The maximum is 6 at \(111111\). This is a demonstration problem, not a meaningful real-world optimization; it makes the operators visible.

### 2. Encoding and population

Each chromosome has six bits. Use a population of four:

\[
P_0=\{100100,\;011010,\;110011,\;001101\}.
\]

Fitness counts ones:

| Chromosome | Ones | Feasible fitness |
|---|---:|---:|
| 100100 | 2 | 2 |
| 011010 | 3 | 3 |
| 110011 | 4 | 4 |
| 001101 | 3 | 3 |

Total fitness is 12. If using roulette selection, the probabilities are

\[
(2/12,3/12,4/12,3/12)
=(0.1667,0.25,0.3333,0.25).
\]

### 3. Parent selection

To make the hand calculation deterministic, use tournament selection of size 2 rather than random roulette spins.

Sample individuals 1 and 3: individual 3 wins because it has fitness 4.
Sample individuals 2 and 4: they tie at fitness 3; choose individual 2 under a stated tie rule.
Sample individuals 4 and 1: individual 1 wins with fitness 2.
Sample individuals 3 and 2: individual 3 wins with fitness 4.

The selected parents, in order, are

\[
(110011,\;011010,\;100100,\;110011).
\]

Individual 3 appears twice; selection with replacement permits this.

### 4. Crossover

Use one-point crossover with probability \(p_c=0.9\). Apply crossover to the first two parent pairs and leave the last pair unchanged as a demonstration. The cut is after position 3.

#### Pair 1

\[
110011=110|011,
\]

\[
011010=011|010.
\]

Children:

\[
C_1=110010,\qquad C_2=011011.
\]

#### Pair 2

\[
100100=100|100,
\]

\[
110011=110|011.
\]

Children:

\[
C_3=100011,\qquad C_4=110100.
\]

The un-crossed parent copy is

\[
C_5=110011.
\]

The raw offspring population is

\[
\{110010,\;011011,\;100011,\;110100,\;110011\}.
\]

### 5. Mutation

Use per-bit mutation probability \(p_m=0.1\). For a hand run, flip exactly the listed bits, making the random event explicit:

- \(C_1=110010\), flip bit 3: \(C_1'=111010\);
- \(C_2=011011\), no flip: \(C_2'=011011\);
- \(C_3=100011\), flip bit 5: \(C_3'=100111\);
- \(C_4=110100\), no flip: \(C_4'=110100\);
- \(C_5=110011\), no flip: \(C_5'=110011\).

The mutated population is

\[
P_1=\{111010,\;011011,\;100111,\;110100,\;110011\}.
\]

A real run would generate a random flip pattern for every bit, not choose flips manually.

### 6. Fitness evaluation

| Offspring | Ones | Feasible fitness |
|---|---:|---:|
| 111010 | 4 | 4 |
| 011011 | 4 | 4 |
| 100111 | 4 | 4 |
| 110100 | 3 | 3 |
| 110011 | 4 | 4 |

The best offspring is 111010 or any other four-one string under this tie rule. Select 111010 as the best.

### 7. Replacement and next generation

The population size is four, but five offspring were produced because the demonstration created an un-crossed copy. A real generational GA must either produce exactly \(P\) offspring or define the replacement rule. For this example, retain the best four offspring by fitness and diversity:

\[
P_1=\{111010,\;011011,\;100111,\;110011\}.
\]

The discarded 110100 has fitness 3, while the retained strings have fitness 4. No elite copy is needed because the old best 110011 is already included.

If a fixed population of five is desired, set the population size to five or produce one extra pair consistently. Do not silently change the population size between generations.

### 8. Second generation

Repeat selection, crossover, and mutation. A possible result is

\[
P_2=\{111110,\;111011,\;110111,\;101111\}.
\]

All four strings have five ones, and the best fitness is 5. The population is now concentrated near the optimum. Strong selection and a small mutation probability may still prevent the exact 111111 from appearing, although a flip can produce it.

If a flip changes one zero in 111110, the result is 111111. With per-bit \(p_m=0.1\), the chance of a particular zero bit being flipped is 0.1 per offspring, subject to the implementation's random draws. The actual probability of obtaining the optimum in one offspring depends on the number of zero bits.

### 9. Constraint implementation

For a chromosome with one or zero ones,

\[
f=0-10(2-J),
\]

so a zero-one string has fitness \(-20\), and a two-one string has fitness 2. An invalid string can never win against a feasible string under this scale.

A repair alternative adds random missing bits until the minimum constraint is met. Repair is simpler for this toy problem, but it changes the genotype distribution.

### 10. Implementation pseudocode

```python
import random

def ones(g):
    return sum(g)

def fitness(g):
    count = ones(g)
    return count - 10 * max(0, 2 - count)

def tournament(pop, q):
    return max(random.sample(pop, q), key=fitness)

def crossover(a, b, point):
    return a[:point] + b[point:], b[:point] + a[point:]

def mutate(g, pm, rng):
    return [bit ^ 1 if rng.random() < pm else bit for bit in g]

def run(population_size=4, bit_length=6, generations=10,
        pc=0.9, pm=0.1, seed=None):
    rng = random.Random(seed)
    population = [
        [rng.randint(0, 1) for _ in range(bit_length)]
        for _ in range(population_size)
    ]
    for generation in range(generations):
        scored = [(fitness(g), g) for g in population]
        elite = max(scored, key=lambda item: item[0])[1]
        offspring = []
        while len(offspring) < population_size:
            p1 = tournament(population, 2)
            p2 = tournament(population, 2)
            if rng.random() < pc:
                c1, c2 = crossover(p1, p2, rng.randint(1, bit_length - 1))
            else:
                c1, c2 = p1[:], p2[:]
            offspring.append(mutate(c1, pm, rng))
            if len(offspring) < population_size:
                offspring.append(mutate(c2, pm, rng))
        population = offspring
        if fitness(elite) < max(fitness(g) for g in population):
            population[-1] = elite
    return max(population, key=fitness), population
```

The exact random path depends on the seed and Python's random sequence. The hand run above demonstrates the same operators.

### 11. Diagnostics

Log per generation:

- best fitness;
- mean fitness;
- worst fitness;
- fraction of feasible candidates;
- number of unique chromosomes;
- average pairwise Hamming distance.

A rising best score with falling diversity signals premature convergence. Add random immigrants or increase mutation rather than merely extending the same run.

### 12. A constrained scheduling example

For a permutation GA, use order crossover. If one-point crossover produces duplicates, repair them by scanning the child and removing repeated values, then fill missing values in a chosen order. Compare:

- raw crossover plus penalty;
- order crossover;
- order crossover plus repair.

Record feasibility rate and schedule quality. A GA is not evaluated only by its best score; an operator that produces mostly invalid schedules is not effective.

## Key terms & formulas

- **GA implementation:** Complete cycle from encoding to stopping.
- **Selection with replacement:** Same parent may be selected repeatedly.
- **One-point crossover:** Exchange suffixes after one cut.
- **Per-bit mutation:** Each bit flips with probability \(p_m\).
- **Elitism:** Preserve the best candidate.
- **Diversity:** Number or spread of distinct chromosomes.
- **Feasibility rate:** Fraction of offspring satisfying constraints.
- **Seed:** Random-number initialization for reproducibility.

Expected bit flips in a 6-bit chromosome:

\[
E[\text{flips}]=6p_m.
\]

With \(p_m=0.1\), the expected number is 0.6 per offspring, not a guarantee of zero or one flip.

## Common mistakes

1. **Changing population size between generations.** Produce exactly the declared number or define replacement.
2. **Forgetting a bias or penalty for constraints.** Invalid candidates need a defined treatment.
3. **Using a crossover cut outside the chromosome.** Choose \(1,\ldots,L-1\).
4. **Assuming mutation always improves fitness.** It is random; selection decides.
5. **Using one run to claim a general result.** Fix seeds for reproducibility and repeat with multiple seeds.
6. **Mixing a hand-calculated parent list with a different random implementation.** State the random choices or use a fixed seed.
7. **Ignoring diversity logs.** Best fitness alone hides premature convergence.
8. **Using bit-flip probability as if it were a whole-chromosome probability.** Specify the unit.

## Exam prep

### Likely 2-mark questions

- **List the steps in a GA implementation.**  
  **Hint:** Encode, initialize, evaluate, select, cross, mutate, replace, stop.

- **State the role of a seed in a GA program.**  
  **Hint:** Makes random choices reproducible for a given implementation.

- **What is a feasibility rate?**  
  **Hint:** Fraction of generated candidates that satisfy all constraints.

- **How can premature convergence be detected?**  
  **Hint:** Falling diversity with a stalled best score.

- **Write the expected number of bit flips.**  
  **Hint:** \(Lp_m\).

### Likely long-answer questions

- **Implement a binary GA for a stated problem and show one generation.**  
  **Hint:** Population table, fitness, tournament/roulette, cut, offspring, mutations, replacement, and new best.

- **Explain how a constraint penalty works in a GA.**  
  **Hint:** Feasibility, violation, coefficient, ranking, and numerical stability.

- **Compare repair, penalty, and feasibility-preserving operators.**  
  **Hint:** Validity, diversity, bias, computation, and suitability.

- **Design a GA experiment and report its results properly.**  
  **Hint:** Seed, budget, repeated runs, best/mean/standard deviation, diversity, and validation.
