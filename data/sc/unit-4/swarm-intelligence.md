---
subject: sc
unit: 4
topic: swarm-intelligence
syllabus_ref: CSM3202 Unit-IV
status: draft
---
# Swarm Intelligence

## Overview

Swarm intelligence is a family of optimization methods inspired by the collective behavior of simple agents. A group of ants, bees, birds, or fish solves a problem through local rules, communication, and feedback. No single agent needs complete global knowledge.

The syllabus includes swarm intelligence as a distinct soft-computing paradigm. Particle swarm optimization, ant colony optimization, artificial bee colonies, and firefly algorithms are common examples. These methods are often grouped with evolutionary computation, but they are not ordinary genetic algorithms: they emphasize cooperation, attraction, pheromone, or neighborhood information rather than parent crossover.

## Explanation

### 1. Main idea

A swarm has many simple agents with limited individual capability. The group produces intelligent behavior because agents:

- sense local surroundings;
- exchange information through shared memory or communication;
- follow simple movement or choice rules;
- adapt based on quality;
- balance exploration and exploitation.

This combination can work in high-dimensional or nonlinear spaces where an exact gradient is unavailable.

### 2. Particle swarm optimization (PSO)

A particle \(i\) has position

\[
\mathbf x_i
\]

and velocity

\[
\mathbf v_i.
\]

It remembers a personal best position

\[
\mathbf p_i
\]

and the swarm or neighborhood best position

\[
\mathbf g.
\]

The velocity update is

\[
\mathbf v_i^{t+1}
=
w\mathbf v_i^t
+c_1r_1\odot(\mathbf p_i^t-\mathbf x_i^t)
+c_2r_2\odot(\mathbf g^t-\mathbf x_i^t),
\]

where:

- \(w\) is inertia;
- \(c_1,c_2\) are cognitive and social coefficients;
- \(r_1,r_2\) are independent random vectors;
- \(\odot\) is elementwise multiplication.

The position update is

\[
\mathbf x_i^{t+1}=\mathbf x_i^t+\mathbf v_i^t.
\]

#### Inertia

Large \(w\) encourages continuing in the current direction and broad exploration. Small \(w\) makes movement more responsive to personal and global best positions. An adaptive linearly decreasing inertia is common:

\[
w_t=w_{\max}
-\frac{w_{\max}-w_{\min}}{T}t.
\]

#### Local versus global best

A local-best PSO uses neighborhoods, which helps diversity and parallel search. A global-best PSO uses the best particle in the whole swarm, which can converge faster but risk premature convergence.

### 3. Ant colony optimization (ACO)

ACO models pheromone trails. More pheromone increases the probability of choosing a route, while pheromone evaporates over time.

A common transition probability is

\[
P_{ij}^{k}
=
\frac{[\tau_{ij}]^\alpha[\eta_{ij}]^\beta}
{\sum_{j\in N_i^k}[\tau_{ij}]^\alpha[\eta_{ij}]^\beta},
\]

where:

- \(\tau_{ij}\) is pheromone on edge \(i\to j\);
- \(\eta_{ij}\) is a heuristic, such as inverse distance;
- \(\alpha\) weights pheromone;
- \(\beta\) weights the heuristic.

After evaluating solutions, update pheromone:

\[
\tau_{ij}\leftarrow(1-\rho)\tau_{ij}
+\sum_k\Delta\tau_{ij}^{k},
\]

with evaporation \(0<\rho<1\). A candidate-list restriction can reduce computation on large graphs.

### 4. Artificial bee colony

An artificial bee colony has:

- employed bees exploring food sources;
- onlooker bees selecting sources according to quality;
- scout bees abandoning exhausted sources and searching globally.

A common source-selection probability is proportional to fitness:

\[
p_i=\frac{f_i}{\sum_jf_j}.
\]

The model balances local exploitation around promising sources with global exploration by scouts.

### 5. Firefly algorithm

Each firefly has brightness proportional to its solution quality. A brighter firefly \(j\) attracts firefly \(i\):

\[
\mathbf x_i^{t+1}
=
\mathbf x_i^t
+\beta e^{-\gamma d_{ij}^2}
(\mathbf x_j^t-\mathbf x_i^t)
+\alpha\epsilon_i.
\]

Here \(d_{ij}\) is distance, \(\beta\) controls attraction, and the random term supports exploration. Distance and brightness definitions vary by implementation.

### 6. Artificial immune systems and other swarm ideas

Artificial immune systems use populations of candidate solutions and concepts such as cloning, mutation, and selection based on similarity to antigens. They are related to evolutionary and swarm methods. Other variants include bacterial foraging, gravitational search, and firework algorithms.

The common thread is decentralized, adaptive search with feedback.

### 7. Comparison with evolutionary algorithms

| Feature | Swarm intelligence | Evolutionary computation/GA |
|---|---|---|
| Main memory | personal/global best, pheromone, population | population fitness and selected parents |
| Main movement | velocity, attraction, pheromone, local search | selection, crossover, mutation |
| Communication | direct neighbor or shared field | parent-offspring inheritance and fitness ranking |
| Exploitation | follow good solutions/regions | reproduce good chromosomes |
| Exploration | random components, scouts, velocity, diverse swarm | mutation, random initialization, diversity operators |
| Guarantee | usually heuristic | usually heuristic |

A swarm can be called an evolutionary algorithm in a broad sense, but PSO does not normally use crossover. Exam answers should distinguish the operators rather than label every swarm method a GA.

### 8. Design parameters

For PSO, important parameters are:

- swarm size;
- inertia \(w\);
- cognitive coefficient \(c_1\);
- social coefficient \(c_2\);
- local versus global topology;
- initial positions and velocities;
- stopping rule.

For ACO:

- pheromone factor \(\alpha\);
- heuristic factor \(\beta\);
- evaporation \(\rho\);
- number of ants;
- construction and update rules.

Parameters interact. A social coefficient that is too large can pull all particles to one poor point; a cognitive coefficient that is too large can make particles ignore useful global information.

### 9. Exploration and convergence

A swarm needs both:

- exploration: visit new regions;
- exploitation: refine promising regions.

In PSO, inertia and random terms support exploration; social attraction supports exploitation. In ACO, high pheromone reinforces good routes, while evaporation prevents old trails from dominating forever.

A good stopping rule balances quality and time. Convergence to a stable swarm does not prove global optimality.

### 10. Constraints

Handle constraints using:

- penalty functions;
- repair or projection;
- feasibility-preserving movement;
- specialized routing rules;
- constrained local search.

A particle or ant should not be evaluated on an invalid route without a defined score. A safe algorithm may project a candidate into the feasible region or reject it.

### 11. Applications

Swarm methods are used for:

- continuous function optimization;
- routing and travelling-salesperson variants;
- network routing and antenna placement;
- scheduling;
- feature selection;
- power-system tuning;
- robot navigation;
- molecular and structural design;
- multi-objective optimization.

They are useful when a problem is nonlinear and many agents can be evaluated in parallel.

### 12. Advantages

- Simple, derivative-free search.
- Good exploration from many local agents.
- Flexible for continuous and graph problems.
- Parallel evaluation.
- Memory of good regions through particles, pheromones, or archives.
- Often few problem-specific formulas beyond a heuristic.

### 13. Limitations

- No general global-optimality guarantee.
- Highly sensitive to topology, parameters, and initialization.
- PSO can stagnate when particles lose diversity.
- ACO's pheromone table may be costly for large graphs.
- Stochastic results vary by seed.
- Constraint handling and discrete transitions need care.

## Worked examples

### Example 1: PSO velocity update

Let a one-dimensional particle have

\[
x=2,\quad v=1,\quad p=3,\quad g=5,
\]

with \(w=0.7\), \(c_1=c_2=1\), and \(r_1=r_2=0.5\). Then

\[
v_{\text{new}}
=0.7(1)+1(0.5)(3-2)+1(0.5)(5-2)
=0.7+0.5+1.5=2.7.
\]

The new position is

\[
x_{\text{new}}=2+2.7=4.7.
\]

The particle is attracted to both its own best and the swarm best.

### Example 2: ACO probability

Suppose two edges from city \(i\) have pheromone \((2,1)\) and heuristic values \((1,1/2)\). With \(\alpha=1,\beta=2\),

\[
w_1=2(1)^2=2,
\]

\[
w_2=1(1/2)^2=0.25.
\]

Thus

\[
P_{i1}=\frac{2}{2.25}=0.8889,\qquad
P_{i2}=\frac{0.25}{2.25}=0.1111.
\]

A good edge is selected more often. After many ants use it, its pheromone grows further unless evaporation balances the reinforcement.

### Example 3: Pheromone evaporation

Let a trail have \(\tau=4\), evaporation \(\rho=0.2\), and 20 ants add \(\Delta\tau=0.05\) each. Then

\[
\tau'=0.8(4)+20(0.05)=3.2+1=4.2.
\]

If no ants use the trail, it falls to \(0.8(4)=3.2\). Evaporation prevents a stale trail from permanently locking the colony into an old route.

### Example 4: PSO stagnation

If all particles have nearly the same position and velocity, social and cognitive terms are small. Without mutation, random restarts, or a diversity mechanism, the swarm may stop improving. Increase random velocity, use local neighborhoods, or inject new particles.

## Key terms & formulas

- **Swarm intelligence:** Collective optimization by simple interacting agents.
- **Particle:** Agent with position and velocity in PSO.
- **Personal best:** Best position known to a particle.
- **Global best:** Best position known to the swarm.
- **Pheromone:** Storable trail intensity in ACO.
- **Scout:** Agent that explores a new region.
- **Inertia:** PSO momentum coefficient.
- **Evaporation:** Pheromone decay factor.

PSO:

\[
v_i^{t+1}=wv_i^t+c_1r_1(p_i-x_i^t)+c_2r_2(g-x_i^t),
\qquad
x_i^{t+1}=x_i^t+v_i^{t+1}.
\]

ACO probability:

\[
P_{ij}\propto[\tau_{ij}]^\alpha[\eta_{ij}]^\beta.
\]

Pheromone update:

\[
\tau_{ij}\leftarrow(1-\rho)\tau_{ij}+\Delta\tau_{ij}.
\]

## Common mistakes

1. **Calling PSO a genetic algorithm.** PSO uses velocity and attraction, not parent crossover.
2. **Forgetting random terms in PSO.** Without them, particles may move deterministically and stagnate.
3. **Using global best only and losing diversity.** Compare local and global topologies.
4. **Ignoring pheromone evaporation.** Old trails can dominate incorrectly.
5. **Assuming a swarm converges globally.** It is a heuristic.
6. **Using infeasible routes without penalties or repair.** Define feasibility.
7. **Tuning one parameter in isolation.** Coefficients, population size, and topology interact.
8. **Comparing a stochastic method from one seed.** Repeat runs.

## Exam prep

### Likely 2-mark questions

- **Define swarm intelligence.**  
  **Hint:** Collective intelligence from simple interacting agents with local rules and communication.

- **Write the PSO velocity update.**  
  **Hint:** Inertia plus cognitive and social attraction terms.

- **What is a pheromone in ACO?**  
  **Hint:** A memory trail whose intensity influences route choice and evaporates.

- **Give two swarm-intelligence algorithms.**  
  **Hint:** PSO, ACO, artificial bee colony, firefly, or firework.

- **State one advantage of swarm methods.**  
  **Hint:** Derivative-free, parallel, flexible exploration.

### Likely long-answer questions

- **Explain PSO with its parameters and update equations.**  
  **Hint:** Position, velocity, personal/global best, inertia, and convergence.

- **Explain ant colony optimization for routing.**  
  **Hint:** Construction probability, pheromone, heuristic, evaporation, update, and constraints.

- **Compare swarm intelligence with genetic algorithms.**  
  **Hint:** Agents and memory, operators, exploration, convergence, and applications.

- **Discuss advantages and limitations of swarm intelligence.**  
  **Hint:** Parallelism, local rules, parameter sensitivity, stagnation, and no guarantee.
