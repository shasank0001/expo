---
subject: sc
unit: 4
topic: ga-parent-selection
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# Selection of Parents in a Genetic Algorithm

## Overview

Parent selection chooses which individuals are allowed to reproduce. It is the main bridge between the current population's fitness and the next generation's genetic material. Good selection increases the chance that useful traits are inherited, but too much selection can remove diversity and cause premature convergence.

The syllabus methods include roulette-wheel selection, rank selection, tournament selection, and truncation selection. A complete implementation also specifies whether selection is with replacement, whether elites survive, and how ties and negative fitness values are handled.

## Explanation

### 1. Selection objective

Let individual \(x_i\) have fitness \(f_i\). Selection should favor high fitness while preserving enough variety for crossover and mutation to discover new solutions.

Selection pressure is the degree to which the best candidates are preferred:

- **low pressure:** many candidates reproduce;
- **high pressure:** a few strong candidates dominate;
- **too low:** slow progress;
- **too high:** premature convergence.

No method has a universally correct pressure. It should be adjusted to the representation, objective, population, and variation operators.

### 2. Roulette-wheel selection

For nonnegative fitness, the probability of selecting \(x_i\) is

\[
p_i=\frac{f_i}{\sum_{j=1}^{P}f_j}.
\]

The name comes from a wheel divided into sectors proportional to fitness. A random number selects a sector. Fitness must be nonnegative and positive in total. If the task minimizes a cost \(J_i\), use

\[
f_i=\frac1{J_i+\epsilon}
\]

or

\[
f_i=C-J_i
\]

with a suitable offset.

Roulette selection is easy to understand but can be dominated by one outlier. A very small fitness denominator can cause floating-point trouble.

### 3. Linear scaling

If fitness values have a narrow range, selection differences may be too weak. If one value is huge, selection may become too greedy. Linear scaling is

\[
f_i'=\frac{(f_i-f_{\min})(f_{\max}-f_{\text{scale}})}
{f_{\max}-f_{\min}}+f_{\text{scale}}.
\]

Choose \(f_{\text{scale}}\) to maintain positive fitness and the desired selection pressure. A common convention is a small value such as 1, but it is not universal.

### 4. Rank selection

Rank candidates from best to worst and assign probabilities independent of raw fitness gaps:

\[
p_i=\frac{k-r_i+1}{\sum_{j=1}^{P}(k-r_j+1)}
\]

if larger rank number is better, or an equivalent descending formula if rank 1 is best.

A common distribution is

\[
p_r=\frac{2(P-r+1)}{P(P+1)},\qquad r=1,\ldots,P,
\]

where \(r=1\) is the best. Rank selection is scale-independent and less sensitive to outliers, but it discards information about how much better the best solution is.

### 5. Tournament selection

Draw \(q\) individuals uniformly and select the best among them. Repeat until the required number of parents is obtained.

For independent uniform sampling,

\[
P(x_i\text{ wins one tournament})
=
p_i^q.
\]

The probability of selecting \(i\) in repeated tournaments depends on the process, but \(q\) clearly controls pressure:

- \(q=1\): random selection;
- \(q=2\): moderate pressure;
- large \(q\): strong pressure and low diversity.

Tournament selection is invariant to monotonic transformations of fitness, easy to implement, and often effective. It can be inefficient if \(q\) is large because many candidates are sampled.

### 6. Truncation selection

Select only the best \(T\) individuals:

\[
T=\lceil \alpha P\rceil
\]

or select the top \(P-\alpha P\). Individuals are usually selected randomly within the selected group, which allows all retained individuals to reproduce.

Truncation has strong selection pressure and can discard useful diversity. It is simple and can work well with a large offspring population.

### 7. Stochastic universal sampling (SUS)

SUS lays out selection probabilities around a wheel in one pass. Instead of independent random spins, it uses equally spaced pointers. It reduces the variance of selection counts: a candidate is not repeatedly overrepresented because of unlucky random boundaries.

SUS is useful when each parent should be selected approximately according to its probability.

### 8. Selection with and without replacement

With replacement, the same individual may be selected several times. Without replacement, each selected copy is removed from the selection pool for that generation.

With replacement is simple but can create many copies of a good individual. Without replacement controls counts but requires careful handling when the required offspring count exceeds the population.

### 9. Rank and fitness alternatives

If fitness is negative or zero, use:

- rank selection;
- roulette after shifting;
- tournament selection;
- a fitness transformation.

Never use a formula with a zero or negative denominator without an explicit transformation.

### 10. Elitism and parent survival

Elitism is not a selection method, but it interacts strongly with it. If the best \(E\) individuals are copied unchanged into the next population, their good traits cannot disappear. The next generation is often

\[
P_{t+1}=\operatorname{Elite}_E(P_t)
\cup\operatorname{Vary}(\operatorname{Select}(P_t)).
\]

Too many elites can reduce diversity. Keep enough non-elite parents for search.

### 11. Constraint handling during selection

A constrained candidate can be ranked after feasibility:

1. feasible candidates before infeasible candidates;
2. among feasible candidates, better objective value wins;
3. among infeasible candidates, lower violation wins.

This feasibility-dominance rule avoids assigning arbitrary huge penalties that may overflow.

### 12. Selecting for multiobjective problems

There is no single fitness for multiple objectives. Common approaches are:

- weighted scalarization;
- Pareto rank;
- crowding distance;
- nondominated sorting;
- niching.

NSGA-II uses nondominated rank and crowding distance to maintain both convergence and diversity. It is not ordinary roulette-wheel selection.

### 13. Adaptive selection

Selection pressure can vary over time. A high-pressure phase can exploit promising regions, followed by a low-pressure or restart phase to regain diversity. Adaptive selection should be based on measured diversity, not only generation number.

## Worked examples

### Example 1: Roulette-wheel probabilities

Let fitness values be

\[
(10,20,30,40).
\]

Total fitness is 100, so

\[
p=(0.1,0.2,0.3,0.4).
\]

One random draw \(r\in[0,1)\) selects:

- \(0\le r<0.1\): individual 1;
- \(0.1\le r<0.3\): individual 2;
- \(0.3\le r<0.6\): individual 3;
- \(0.6\le r<1\): individual 4.

A random draw of 0.45 selects individual 3.

### Example 2: Tournament selection

Fitness values are

\[
(0.1,0.8,0.4,0.7,0.2).
\]

A tournament of size 3 samples individuals 2, 4, and 5. Individual 2 with fitness 0.8 wins. A tournament of size 1 selecting individual 4 wins regardless of the other candidates, so it would provide no selection pressure.

### Example 3: Rank probabilities

For four candidates ordered best to worst, assign

\[
p=(0.4,0.3,0.2,0.1).
\]

The best candidate has probability 0.4 even if its raw fitness is only slightly larger than the second. Rank selection is robust to scale but loses magnitude information.

### Example 4: Elitism interaction

Population:

\[
x_1^\star,x_2,x_3,x_4.
\]

With one elite and three parent slots, copy \(x_1^\star\) unchanged and create three offspring from selected parents. The best solution cannot disappear, but if the three selected parents are identical, the offspring may be nearly identical. Elitism protects quality, not diversity.

### Example 5: Feasibility rule

Candidates:

| Candidate | Objective | Violation |
|---|---:|---:|
| A | 10 | 0 |
| B | 8 | 0.2 |
| C | 5 | 0 |

A feasible candidate should outrank C even if C has a lower objective. A common ordering is A, C, B. This avoids an arbitrary penalty scale.

## Key terms & formulas

- **Roulette-wheel selection:** Probability proportional to nonnegative fitness.
- **Rank selection:** Probability based on order rather than magnitude.
- **Tournament selection:** Select best among a random subset.
- **Truncation selection:** Select only a top fraction.
- **SUS:** Low-variance proportional selection using equally spaced pointers.
- **Selection pressure:** Strength of preference for high fitness.
- **Elitism:** Preserve best individuals unchanged.
- **Feasibility dominance:** Prefer feasible candidates, then lower violation.

Roulette:

\[
p_i=\frac{f_i}{\sum_jf_j}.
\]

Tournament size \(q\):

\[
P(x_i\text{ wins one tournament})=p_i^q.
\]

Rank:

\[
p_r=\frac{2(P-r+1)}{P(P+1)}.
\]

## Common mistakes

1. **Applying roulette to negative fitness.** Transform, rank, or use tournament selection.
2. **Forgetting to handle a zero total fitness.** Define a fallback or a different selection method.
3. **Confusing selection with crossover.** Selection chooses parents; crossover combines them.
4. **Using a tournament of size one.** It is random selection.
5. **Selecting the same parent repeatedly and losing diversity.** Add rank/tournament diversity, elites, or restarts.
6. **Using too many elites.** The best solution survives but population diversity may collapse.
7. **Ranking infeasible candidates only by objective.** Apply feasibility first.
8. **Choosing selection pressure without monitoring diversity.** Record unique genotypes and population spread.

## Exam prep

### Likely 2-mark questions

- **Define roulette-wheel selection and write its probability formula.**  
  **Hint:** \(p_i=f_i/\sum f_j\), for nonnegative fitness.

- **What is tournament selection?**  
  **Hint:** Select the fittest from a random subset of size \(q\).

- **State the advantage of rank selection.**  
  **Hint:** Scale-independent and less sensitive to outliers.

- **What is SUS?**  
  **Hint:** Stochastic universal sampling with equally spaced selection pointers.

- **Why is diversity monitored after selection?**  
  **Hint:** High pressure can cause premature convergence.

### Likely long-answer questions

- **Explain parent-selection methods in a genetic algorithm.**  
  **Hint:** Roulette, rank, tournament, truncation, SUS, formulas, and selection pressure.

- **Work out roulette and tournament selection for a population.**  
  **Hint:** Fitness normalization, random intervals or tournament samples, and parent counts.

- **Compare fitness-proportional and rank selection.**  
  **Hint:** Outliers, scale sensitivity, information loss, diversity, and implementation.

- **Explain elitism and its interaction with parent selection.**  
  **Hint:** Best-copy preservation, diversity trade-off, and next-generation construction.
