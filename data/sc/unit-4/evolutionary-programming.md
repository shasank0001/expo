---
subject: sc
unit: 4
topic: evolutionary-programming
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# Evolutionary Programming

## Overview

Evolutionary programming (EP) is a population-based optimization method that emphasizes mutation of strategy or behavior parameters. Individuals are usually real-valued vectors representing candidate strategies, control policies, or numerical solutions. There is often no chromosome crossover requirement.

EP differs from a classical genetic algorithm mainly in its emphasis: mutation is the dominant variation operator, selection is often tournament-based, and the individual may include adaptive mutation widths. It is useful for continuous parameter optimization and adaptive control.

## Explanation

### 1. Basic representation

An individual may be

\[
\mathbf x_i=(x_{i1},x_{i2},\ldots,x_{id})
\]

or include a strategy vector

\[
\boldsymbol{\sigma}_i=(\sigma_{i1},\ldots,\sigma_{id})
\]

and objective value \(J(\mathbf x_i)\). In some versions, the individual represents a behavior mapping rather than a single parameter vector.

### 2. Mutation-centered generation

A parent generates an offspring by changing its parameters:

\[
x'_{ij}=x_{ij}+\sigma_{ij}z_{ij},
\qquad z_{ij}\sim\mathcal N(0,1).
\]

The mutation is centered at the parent, so a zero-mean Gaussian has no systematic directional bias before selection. Multiple children provide a sample of possible moves.

If no crossover is used, the population must be large enough to cover useful directions. A small population may repeatedly explore one local region.

### 3. Adaptive mutation strategy

An EP strategy can store a mutation width and update it after a run:

\[
\sigma'_{ij}
=
\sigma_{ij}
\exp\left(\tau_{ij}N_{ij}+\tau_0N_0\right),
\]

where \(N_{ij}\sim\mathcal N(0,1)\). The coefficients \(\tau_{ij},\tau_0\) are commonly based on the number of parameters \(d\) and the square root of the parent population.

An alternative adaptive scheme is deterministic:

- widen mutations after unsuccessful generations;
- narrow them after successful generations.

The random rule supports self-adaptation; the deterministic rule is a simple feedback controller.

### 4. Tournament selection

EP often selects parents by randomly drawing \(q\) individuals and choosing the best. Repeating this tournament selects the next population.

The probability that a strong candidate wins a tournament is high, but weaker individuals can still survive. The tournament size controls selection pressure: larger \(q\) is greedier and usually reduces diversity.

### 5. Elitism and replacement

Some EP variants preserve the best individual explicitly. If the best is not preserved, the method may accept a temporarily worse strategy and explore more widely.

The population can be replaced after the offspring are generated, or parents and offspring can compete. This choice changes stability and convergence.

### 6. Fitness evaluation

For minimization, candidates are ordered by increasing objective value. For maximization, the order is reversed. Noisy evaluation should be repeated or smoothed; a one-time simulation error can incorrectly reward a bad strategy.

An EP objective can combine performance, cost, and stability:

\[
J(\mathbf x)=\alpha\text{tracking error}
+\beta\text{energy}
+\gamma\text{control effort}.
\]

The weights should reflect the application, not be chosen to make a preferred answer look best.

### 7. Continuous and discrete strategies

EP is most natural for real-valued parameters. It can handle discrete variables through rounding, repair, or specialized mutation, but a GA or local search may be more natural for permutations and bit strings.

The representation must ensure that a mutation changes the phenotype in a controlled and useful way.

### 8. Multiobjective EP

For multiple objectives, retain nondominated candidates or use an external archive. A single weighted score is simpler but hides the trade-off. A Pareto set is often more useful in design, where cost, robustness, and quality conflict.

### 9. EP compared with GA and ES

| Feature | EP | GA | ES |
|---|---|---|---|
| Main emphasis | mutation/behavior | encoded crossover and mutation | real mutation/self-adaptation |
| Crossover | usually absent or optional | common | often absent |
| Selection | tournament common | roulette/rank/tournament | comma or plus selection |
| Representation | strategy/behavior vector | chromosome | real vector plus parameters |
| Self-adaptation | common | optional | central |
| Typical use | control and numeric search | general optimization | continuous numeric search |

The boundaries are not rigid. An EP implementation may borrow GA selection, and an ES may use tournament selection.

### 10. Design parameters

- population size \(\mu\);
- offspring per parent or total offspring;
- tournament size \(q\);
- initial mutation width;
- self-adaptation coefficients;
- elitism;
- replacement rule;
- stopping criterion.

Use multiple runs and report mean, median, standard deviation, and best feasible result. A single unusually good run is not enough.

### 11. Advantages

- Simple mutation-based implementation.
- Natural fit for real-valued parameters.
- Can adapt search width automatically.
- Does not require a chromosome grammar.
- Useful for control and parameter tuning.
- Parent and offspring evaluations are easy to parallelize.

### 12. Limitations

- Slow or unreliable if mutation is poorly scaled.
- No crossover may reduce exploration of combinations.
- Can converge to a local solution.
- Objective evaluation may dominate runtime.
- High-dimensional covariance or mutation adaptation is difficult.
- Tournament pressure may eliminate diversity.
- No global guarantee.

## Worked examples

### Example 1: EP mutation

A parent is

\[
\mathbf x=(1.0,2.0),\qquad\boldsymbol\sigma=(0.1,0.2).
\]

Draw

\[
\mathbf z=(0.5,-1.0).
\]

The child is

\[
\mathbf x'=(1.0,2.0)+(0.1(0.5),0.2(-1.0))
=(1.05,1.80).
\]

If its objective is better, selection makes it more likely to survive or become a parent.

### Example 2: Tournament selection

Fitness values, larger is better, are

\[
(0.2,0.9,0.5,0.1,0.8).
\]

A tournament of size 2 samples candidates 2 and 5; candidate 5 with fitness 0.8 wins. A tournament of size 5 selects the best, 0.9. A larger tournament creates stronger selection pressure.

### Example 3: Width adaptation

After a successful generation, set

\[
\sigma\leftarrow0.8\sigma.
\]

After a failed generation,

\[
\sigma\leftarrow1.2\sigma.
\]

If the objective is noisy, this rule may respond to noise. A self-adaptation rule that learns from many offspring is usually more stable, but still requires validation.

### Example 4: EP control tuning

A controller has gains

\[
\mathbf x=(K_p,K_i,K_d).
\]

An EP population starts with a broad mutation width, explores unstable and stable gains, and then narrows around better strategies. A safety simulation should reject unstable controllers regardless of a high nominal score.

## Key terms & formulas

- **EP:** Evolutionary programming.
- **Behavior strategy:** Individual representing a parameterized behavior or solution.
- **Tournament selection:** Select the best of a random subset.
- **Self-adaptation:** Evolve search parameters such as mutation widths.
- **Offspring:** Candidate generated from a parent.
- **Elitism:** Preserve the best strategy.
- **Selection pressure:** Strength of preference for high-fitness individuals.

Mutation:

\[
x'_{ij}=x_{ij}+\sigma_{ij}z_{ij},\qquad z_{ij}\sim\mathcal N(0,1).
\]

Tournament selection:

\[
P_{t+1}=\operatorname{Best}_q(P_t).
\]

## Common mistakes

1. **Calling EP identical to a GA.** EP emphasizes mutation and may omit crossover.
2. **Forgetting to scale the initial mutation width.** It must match parameter scale.
3. **Using a tournament size of one and expecting strong selection.** It is almost random.
4. **Assuming self-adaptation always finds a good width.** It is stochastic and objective-dependent.
5. **Ignoring the global optimum guarantee.** None is provided.
6. **Using an objective that rewards unsafe behavior.** Add constraints and robust evaluation.
7. **Reporting only the best EP run.** Include repeated-run statistics.
8. **Treating a real-valued strategy as a permutation.** Use an appropriate representation.

## Exam prep

### Likely 2-mark questions

- **Define evolutionary programming.**  
  **Hint:** Population-based method emphasizing mutation of strategy or behavior parameters.

- **Write the EP mutation equation.**  
  **Hint:** \(x'=x+\sigma z\), with Gaussian \(z\).

- **What is tournament selection?**  
  **Hint:** Choose the best individual from a randomly sampled subset.

- **State two differences between EP and GA.**  
  **Hint:** Mutation emphasis, optional/absent crossover, real strategy vectors, and selection.

- **Name one use of EP.**  
  **Hint:** Control tuning, parameter optimization, or adaptive behavior.

### Likely long-answer questions

- **Explain the structure and operation of evolutionary programming.**  
  **Hint:** Individual, mutation, selection, replacement, stopping, and examples.

- **Compare evolutionary programming with evolutionary strategies and genetic algorithms.**  
  **Hint:** Representation, mutation/crossover, selection, self-adaptation, and applications.

- **Explain tournament selection and self-adaptation in EP.**  
  **Hint:** Tournament size, selection pressure, lognormal width rules, and stability.

- **Discuss advantages and limitations of EP for control-system tuning.**  
  **Hint:** Real parameters, parallel evaluation, safety constraints, noise, and local minima.
