---
subject: sc
unit: 4
topic: evolutionary-computing-paradigms
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# Paradigms of Evolutionary Computing

## Overview

Evolutionary computing is a broad family, not one algorithm. This syllabus emphasizes evolutionary algorithms, evolutionary strategies, evolutionary programming, genetic algorithms, and swarm intelligence. They share inspiration from natural populations, but differ in representation, parent selection, variation, and self-adaptation.

Understanding the paradigms helps choose an algorithm. A GA is natural for encoded schedules or rules; an evolutionary strategy is useful for real-valued parameter optimization; evolutionary programming emphasizes mutation and adaptive behavior; swarm intelligence uses cooperative agents rather than sexual reproduction.

## Explanation

### 1. Evolutionary algorithm (EA)

An EA is the umbrella term for population-based, evolution-inspired search. Its abstract cycle is

\[
\text{population}\rightarrow\text{fitness}\rightarrow
\text{selection}\rightarrow\text{variation}\rightarrow\text{replacement}.
\]

The main EA design choices are:

- individual representation;
- initial population;
- fitness and constraint handling;
- selection method;
- variation operators;
- replacement and elitism;
- termination and diversity.

A GA, ES, and EP are all evolutionary algorithm paradigms, but they emphasize different mechanisms.

### 2. Genetic algorithms (GA)

A GA usually represents an individual as a fixed-length chromosome over an alphabet such as \(\{0,1\}\), a vector of real values, or a permutation. It uses selection, crossover, and mutation. A common cycle is

\[
P_t\rightarrow \text{selection}\rightarrow\text{crossover}
\rightarrow\text{mutation}\rightarrow P_{t+1}.
\]

GAs often separate the genotype from a decoded phenotype. They are widely used for combinatorial and numeric optimization.

### 3. Evolutionary strategies (ES)

An ES typically uses a vector of real-valued strategy parameters:

\[
\mathbf x'=\mathbf x+\mathbf z,\qquad
\mathbf z\sim\mathcal N(\mathbf0,\sigma^2\mathbf I).
\]

The step size may itself evolve:

\[
\sigma'=\sigma\exp(\tau N_0+N),
\]

where \(N\sim\mathcal N(0,1)\). ES emphasizes mutation and adaptation of search distributions. It is a natural choice for continuous parameter optimization.

#### \((1,\lambda)\)-ES

One parent creates \(\lambda\) offspring. The best offspring replaces the parent, even if it is worse. This accepts valleys and can help escape local optima, but it is less stable.

#### \((\mu,\lambda)\)-ES

\(\mu\) parents produce \(\lambda\) offspring, and the best \(\lambda\) among offspring form the next generation. The parent is not automatically retained.

#### \((\mu+\lambda)\)-ES

The best \(\mu\) individuals are selected from the \(\mu\) parents and \(\lambda\) offspring together. Elitism is stronger, but the search can converge more quickly.

### 4. Evolutionary programming (EP)

Evolutionary programming emphasizes a population of behavior-generating strategies, mutation of strategy parameters, and often tournament selection. The individual is commonly a real-valued vector of coefficients, not an explicit chromosome requiring crossover.

A generic EP update is

\[
\mathbf x_{i,t+1}
=\mathbf x_{i,t}+\Delta_{i,t},
\]

where \(\Delta\) is a mutation distribution. Adaptive mutation widths can be stored in the individual and changed by the evolutionary process.

### 5. Genetic programming

Genetic programming is a related paradigm in which individuals are program trees or expression trees. Fitness measures how well a program solves a task. Mutation changes an operator or subtree; crossover exchanges subtrees.

GP is not explicitly listed in the short syllabus line, but it is a useful example of why representation matters. A tree must preserve syntactic validity, which affects operator design.

### 6. Differential evolution

Differential evolution belongs to the broader evolutionary-search family. It creates a donor vector from three or more population members:

\[
\mathbf v=\mathbf x_{r1}
+F(\mathbf x_{r2}-\mathbf x_{r3}).
\]

A crossover between the donor and target gives a trial individual. Selection keeps the trial if its fitness is better. It is a strong real-valued baseline but is usually distinguished from classical GA terminology.

### 7. Swarm intelligence

Swarm intelligence is inspired by collective behavior rather than sexual reproduction. Many simple agents interact locally and share information.

- **Particle swarm optimization (PSO):** particles move using personal and neighborhood/global best positions.
- **Ant colony optimization:** pheromone trails reinforce good paths and evaporate over time.
- **Artificial bee colony:** scout, employed, and onlooker bees search and share food information.
- **Firefly algorithm:** brighter fireflies attract others.
- **Fireworks algorithm:** diverse explosions search around good solutions.

Swarm methods usually maintain a distributed population and use local/global communication rather than parent-offspring inheritance.

### 8. Cultural algorithms

Cultural algorithms maintain a population and a knowledge component called culture. Individuals receive guidance from beliefs and update the culture after evaluation. This can help learn problem-specific rules, but it adds memory and representation complexity.

### 9. Memetic algorithms

A memetic algorithm combines evolutionary search with local improvement, often called hill climbing. After creating an offspring, a local optimizer improves it before the next selection. This works well for separable or smooth subproblems, but local search can reduce diversity.

### 10. Multi-objective evolutionary algorithms

Many engineering problems have several conflicting objectives, such as cost, quality, and energy. A multiobjective EA returns a set of nondominated solutions rather than one scalar optimum.

A solution dominates another if it is no worse in every objective and better in at least one. The nondominated set is a Pareto front. Common algorithms include NSGA-II, SPEA2, and MOEA/D.

Combining objectives into one weighted score is simpler, but weights change the preferred design and may hide the front.

### 11. Comparison table

| Paradigm | Individual | Main variation | Typical use |
|---|---|---|---|
| GA | encoded chromosome | crossover + mutation | discrete, real, or permutation optimization |
| ES | real strategy vector | mutation and self-adaptive step sizes | continuous numerical optimization |
| EP | behavior/strategy vector | mutation | adaptive numerical or control strategies |
| GP | program tree | subtree mutation/crossover | symbolic programs and rules |
| DE | real vector | differential mutation + crossover | robust continuous optimization |
| PSO | particle with velocity | social/personal best attraction | continuous multidim search |
| ACO | path construction/pheromone | pheromone update and stochastic choice | routing and scheduling |
| Memetic | solution vector | evolutionary + local search | hybrid fine-grained optimization |

The categories overlap; implementations often combine features.

### 12. Choosing a paradigm

1. Determine the solution representation.
2. Check whether local derivatives are available.
3. Estimate evaluation cost and parallel hardware.
4. Decide whether real-valued or discrete variation is natural.
5. Account for constraints, diversity, and multi-objective needs.
6. Compare simple baselines and measure repeated-run performance.

A GA is a reasonable first choice for a binary or permutation problem; ES or differential evolution is often a baseline for continuous parameters; PSO is a useful baseline for smooth continuous search. No choice guarantees success.

## Worked examples

### Example 1: Same candidate through different paradigms

A candidate is

\[
\mathbf x=(0.2,3.0,-1.0).
\]

- A GA chromosome might encode it as bits or integer symbols.
- An ES would apply Gaussian mutation to the real vector.
- An EP would mutate adaptive behavior parameters.
- A PSO particle would move its position and velocity.
- A GP individual would represent a program, not this vector directly.

The representation determines which operators are meaningful.

### Example 2: ES mutation

Let

\[
\mathbf x=(1,2),\quad \sigma=0.1,
\]

and draw

\[
\Delta=(0.05,-0.08).
\]

The offspring is

\[
\mathbf x'=(1.05,1.92).
\]

If the best of several offspring is worse than the parent, a \((1,\lambda)\)-ES may still accept it, whereas a \((\mu+\lambda)\)-ES would retain the parent. This choice controls greediness.

### Example 3: PSO position update

A particle at \(x=2\) has velocity \(v=1\), personal best \(p=3\), global best \(g=5\), and inertia \(w=0.7\). With \(c_1=c_2=1\) and random values \(r_1=r_2=0.5\),

\[
v_{\text{new}}=0.7(1)+1(0.5)(3-2)+1(0.5)(5-2)
=0.7+0.5+1.5=2.7.
\]

Then

\[
x_{\text{new}}=2+2.7=4.7.
\]

This is movement using personal and social information, not crossover.

### Example 4: Nondominated solutions

Solutions A and B are compared on cost and error:

- A: cost 10, error 8;
- B: cost 12, error 5.

A is cheaper, B has lower error. Neither dominates the other, so both may belong to the Pareto front. Returning only one weighted optimum hides this trade-off.

## Key terms & formulas

- **EA:** General evolutionary algorithm.
- **GA:** Encoded-population algorithm using selection, crossover, and mutation.
- **ES:** Real-valued evolutionary strategy with mutation and self-adaptation.
- **EP:** Evolutionary programming emphasizing mutation and behavior strategies.
- **GP:** Program-tree evolution.
- **DE:** Differential evolution.
- **Swarm intelligence:** Cooperative search by simple agents.
- **Pareto dominance:** No worse in all objectives and better in at least one.

ES mutation:

\[
\mathbf x'=\mathbf x+\mathcal N(\mathbf0,\sigma^2\mathbf I).
\]

PSO velocity:

\[
\mathbf v'=\mathbf w\mathbf v
+c_1\mathbf r_1\odot(\mathbf p-\mathbf x)
+c_2\mathbf r_2\odot(\mathbf g-\mathbf x).
\]

Pareto dominance:

\[
x\prec y\iff
J_i(x)\le J_i(y)\ \forall i
\quad\text{and}\quad
J_j(x)<J_j(y)\text{ for some }j.
\]

## Common mistakes

1. **Treating all evolutionary paradigms as the same algorithm.** GA, ES, EP, and PSO have different operators.
2. **Confusing evolutionary strategies with genetic algorithms.** ES emphasizes real-valued mutation and adaptive step sizes.
3. **Calling PSO a genetic algorithm.** It uses attraction and velocities, not crossover as its main operator.
4. **Ignoring representation.** The same optimization problem may need different encodings.
5. **Using a single scalar score for a multiobjective task without discussing weights.** It hides trade-offs.
6. **Claiming a paradigm guarantees the global optimum.** None generally does.
7. **Forgetting local minima and diversity in a memetic or elitist method.** Local improvement can narrow search.

## Exam prep

### Likely 2-mark questions

- **List the main evolutionary-computing paradigms.**  
  **Hint:** EA, GA, ES, EP, GP/DE, and swarm intelligence.

- **What is the main emphasis of an evolutionary strategy?**  
  **Hint:** Real-valued mutation and adaptive strategy parameters.

- **How does PSO differ from a GA?**  
  **Hint:** Particles use velocity and personal/global best attraction rather than parent crossover.

- **Define Pareto dominance.**  
  **Hint:** No worse in every objective and better in at least one.

- **What is a memetic algorithm?**  
  **Hint:** Evolutionary search combined with local improvement.

### Likely long-answer questions

- **Compare evolutionary strategies, evolutionary programming, and genetic algorithms.**  
  **Hint:** Representation, selection, mutation, crossover, self-adaptation, and applications.

- **Explain swarm intelligence as an evolutionary-computing paradigm.**  
  **Hint:** Collective agents, local communication, PSO/ACO, and comparison with sexual reproduction.

- **Describe evolutionary approaches to multiobjective optimization.**  
  **Hint:** Nondomination, Pareto fronts, NSGA-II or related methods, and trade-offs.

- **Select an evolutionary paradigm for three problem types and justify each choice.**  
  **Hint:** Discrete schedule, continuous parameters, and routing/swarms; include representation and operators.
