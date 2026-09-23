---
subject: sc
unit: 4
topic: evolutionary-strategies
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# Evolutionary Strategies

## Overview

An evolutionary strategy (ES) is an evolutionary method designed mainly for continuous numerical optimization. It represents each candidate as a real-valued strategy vector and generates offspring by Gaussian mutation. The mutation width can also adapt during the run, allowing the search to change from broad exploration to fine local search.

The main ES variants are \((\mu,\lambda)\), \((\mu+\lambda)\), and \((\mu+\lambda,\mu)\). Their selection rules determine whether parents compete only with offspring or survive alongside offspring.

## Explanation

### 1. Basic representation

An individual has a solution vector

\[
\mathbf x=(x_1,\ldots,x_d)
\]

and strategy parameters such as a global step size

\[
\sigma>0.
\]

For a diagonal strategy, each coordinate has its own \(\sigma_i\). A covariance matrix can describe correlated mutation directions:

\[
\mathbf x'=\mathbf x+\mathbf z,\qquad
\mathbf z\sim\mathcal N(\mathbf0,\mathbf\Sigma).
\]

The mutation distribution is a key part of the strategy.

### 2. Gaussian mutation

The simplest mutation is

\[
x_j'=x_j+\sigma z_j,\qquad z_j\sim\mathcal N(0,1).
\]

If mutation is isotropic, all coordinates use the same standard deviation. If anisotropic,

\[
x_j'=x_j+\sigma_jz_j.
\]

Mutation with zero mean is unbiased: averaged over many draws, the parent remains the expected position. The distribution's width controls exploration.

### 3. Self-adaptation of step size

A classic self-adaptation rule is

\[
\sigma'=\sigma\exp(\tau N_0+N),
\qquad N\sim\mathcal N(0,1),
\]

where

\[
\tau=\frac1{\sqrt{2d}},
\qquad
N_0=\frac1{\sqrt{2\sqrt d}}.
\]

The random lognormal multiplier changes the width gradually. Good solutions can be associated with useful widths, and those widths become more common through selection. The constants \(N_0\) and \(\tau\) are conventional choices, not universal requirements.

A simpler deterministic adaptation can use success/failure:

- increase \(\sigma\) after a failed generation;
- decrease \(\sigma\) after a successful generation.

### 4. \((\mu,\lambda)\)-ES

One parent produces \(\lambda\) offspring:

\[
\mathbf x_{i,t+1}
=\mathbf x_{t}+\mathbf z_i,\qquad i=1,\ldots,\lambda.
\]

The best of the offspring becomes the next parent, even if all are worse than the old parent.

**Effect:** the parent can move downhill, which may help cross a valley or escape a local optimum. It can also lose the best current solution and converge erratically.

### 5. \((\mu+\lambda)\)-ES

There are \(\mu\) parents and \(\lambda\) offspring. The best \(\mu\) individuals among all \(\mu+\lambda\) candidates form the next generation.

**Effect:** parents and offspring compete together, so the best solution is never lost through parent replacement alone. The population is more conservative and can converge faster to a local optimum.

### 6. \((\mu+\lambda,\mu)\)-ES

Parents produce \(\lambda\) offspring, but the next parent population is selected only from the \(\lambda\) offspring. The best offspring are chosen among offspring, not mixed with parents. This is often called comma selection.

### 7. Selection, elitism, and diversity

A \((\mu+\lambda)\) scheme is elitist because parents compete with offspring. A \((\mu,\lambda)\) scheme is non-elitist. Elitism protects quality but can reduce exploration.

Use random reinitialization, population diversity, covariance adaptation, or multiple restarts when a non-elitist or elitist method becomes trapped. A single very good individual does not guarantee a good population.

### 8. Covariance matrix adaptation

A covariance-matrix adaptation evolution strategy (CMA-ES) learns a full covariance matrix:

\[
\mathbf z\sim\mathcal N(\mathbf0,\mathbf C),
\]

\[
\mathbf x'=\mathbf x+\mathbf z.
\]

The covariance matrix is updated from successful steps so that useful correlated directions become more likely. CMA-ES is effective for continuous optimization with many variables, but its covariance update and parameter dimension require care.

### 9. Constraint handling

A real-valued chromosome can violate bounds or engineering constraints. Methods include:

- repair by clipping or projection;
- penalty fitness;
- feasibility-preserving mutation;
- repair-and-reoptimize;
- special operators.

Simple clipping can create many candidates at a boundary. A penalty or feasibility rule may be more informative.

### 10. Fitness and minimization

ES often minimizes a scalar objective \(J(\mathbf x)\). Sort lower \(J\) as better. If a maximization formulation is used, reverse the ordering or transform the score; do not mix conventions.

For noisy objectives, repeat evaluations, use a robust statistic, or reduce mutation variance. Evolution is misled by a measurement error treated as a real fitness difference.

### 11. Choosing \(\mu,\lambda,\sigma\)

- \(\mu=1,\lambda\) small: simple \((1+\lambda)\)-ES, sequential and local.
- Larger \(\lambda\): more mutation samples and better selection information, at higher cost.
- Large \(\sigma\): broad exploration but coarse local search.
- Small \(\sigma\): fine search but risk of stagnation.
- Self-adaptation: reduces manual schedule dependence but adds randomness.

Choose values using budget and validation, not one universal formula.

### 12. Applications

ES and CMA-ES are used for:

- continuous function optimization;
- robot and vehicle parameter tuning;
- control-system design;
- antenna and structural design;
- hyperparameter optimization;
- trajectory and motion planning;
- calibration of simulation models.

They are less natural for a simple permutation representation than a GA or specialized permutation operator, although hybrid encodings are possible.

### 13. Advantages

- Natural for real-valued continuous spaces.
- Gradient-free.
- Mutation distribution can adapt.
- CMA-ES can learn correlated search directions.
- Non-elitist variants can escape local optima.
- Simple \((1+\lambda)\)-ES has few parameters.

### 14. Limitations

- No global guarantee.
- Expensive if each evaluation requires simulation.
- Covariance matrices become costly in high dimension.
- Step-size adaptation can fail on a misleading noisy objective.
- Small populations may give poor diversity.
- Boundary and constraint handling must be designed.

## Worked examples

### Example 1: One mutation

Parent:

\[
\mathbf x=(2,4),\qquad \sigma=0.5.
\]

Draw

\[
\mathbf z=(-0.4,1.2).
\]

The offspring is

\[
\mathbf x'=(2,4)+0.5(-0.4,1.2)
=(1.8,4.6).
\]

If \(J(1.8,4.6)<J(2,4)\), the offspring is better and becomes the parent in a \((1,1)\)-ES.

### Example 2: Self-adaptive width

Let

\[
\sigma=0.2,\quad N=0.5.
\]

Ignoring the convention-dependent \(N_0\) term for this illustration,

\[
\sigma'=0.2e^{0.5}\approx0.3297.
\]

The next mutations are wider. If the wider step repeatedly finds better points, selection favors the new strategy. If it causes poor points, smaller widths can become more common.

### Example 3: Comma versus plus selection

Suppose the best parent has cost 1, and the best of five offspring has cost 1.5.

- \((\mu,\lambda)\) with \(\mu=1\): the offspring replaces the parent because it is the only candidate from offspring.
- \((\mu+\lambda)\): the parent cost 1 remains in the population and is selected.

The plus scheme preserves quality; the comma scheme may accept a downhill move.

### Example 4: Covariance intuition

Suppose the objective has a narrow valley along direction \(\mathbf d=(1,1)\). Isotropic mutation with equal variance in both coordinates wastes samples across the valley walls. A covariance matrix can make steps along \(\mathbf d\) more likely and perpendicular steps smaller, improving search efficiency.

## Key terms & formulas

- **ES:** Evolutionary strategy for continuous optimization.
- **Mutation width:** Standard deviation \(\sigma\).
- **Self-adaptation:** Evolution of strategy parameters.
- **Elitism:** Parent survival through selection over parents and offspring.
- **Comma selection:** \((\mu,\lambda)\), offspring compete only with offspring.
- **Plus selection:** \((\mu+\lambda)\), parents and offspring compete together.
- **CMA-ES:** Covariance-matrix adaptation ES.

Mutation:

\[
\mathbf x'=\mathbf x+\mathbf z,\qquad
\mathbf z\sim\mathcal N(\mathbf0,\mathbf\Sigma).
\]

Self-adaptation:

\[
\sigma'=\sigma\exp(\tau N_0+N).
\]

Selection:

\[
P_{t+1}=\operatorname{best}\left(P_t\cup \operatorname{mutate}(P_t)\right)
\]

for plus selection, or use only offspring for comma selection.

## Common mistakes

1. **Confusing ES and GA.** ES emphasizes real mutation and self-adaptation; GA often uses crossover and chromosomes.
2. **Using a negative or zero step size.** Standard deviation must be positive.
3. **Forgetting the variance normalization in self-adaptation.** Conventions vary; state the rule.
4. **Claiming \((\mu,\lambda)\) preserves the best parent.** It does not necessarily do so.
5. **Using an ES without scaling variables.** Step sizes are meaningful only relative to feature scale.
6. **Ignoring correlated directions.** Isotropic mutation may waste samples in narrow valleys.
7. **Treating a small \(\sigma\) as universally better.** It improves local precision but can stagnate.
8. **Reporting one run.** ES is stochastic; repeat runs and report variability.

## Exam prep

### Likely 2-mark questions

- **Define an evolutionary strategy.**  
  **Hint:** Population-based continuous optimization using mutation and often adaptive strategy parameters.

- **Write the basic ES mutation equation.**  
  **Hint:** \(\mathbf x'=\mathbf x+\mathbf z\), with Gaussian mutation.

- **State the difference between \((\mu,\lambda)\) and \((\mu+\lambda)\).**  
  **Hint:** Offspring-only versus parents-plus-offspring selection.

- **What is self-adaptation in an ES?**  
  **Hint:** Mutation width or covariance is itself evolved.

- **Give one application of CMA-ES.**  
  **Hint:** Continuous parameter optimization, control, trajectory, or structural design.

### Likely long-answer questions

- **Explain ES structure, mutation, and self-adaptation with an example.**  
  **Hint:** Real chromosome, Gaussian step, lognormal width update, selection, and validation.

- **Compare \((\mu,\lambda)\), \((\mu+\lambda)\), and comma selection.**  
  **Hint:** Parent retention, exploration, elitism, and convergence.

- **Explain CMA-ES and its advantage over isotropic mutation.**  
  **Hint:** Learned covariance, correlated directions, valley example, and limitations.

- **Discuss advantages and limitations of evolutionary strategies.**  
  **Hint:** Continuous search, derivative-free operation, step sizes, cost, dimension, and no global guarantee.
