---
subject: ml
unit: 1
topic: reinforcement-learning-basics
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Reinforcement Learning Basics

## Overview

Reinforcement learning (RL) is learning how to act in an environment by trying actions and observing the consequences. An **agent** chooses an action, the **environment** responds with a new state and a reward, and the agent uses the resulting experience to improve its **policy**. The goal is usually to maximise expected long-term reward, not merely the reward from the next action.

RL differs from supervised learning because correct actions are not always provided for every state. A consequence may be delayed, and the learner must balance trying promising actions with trying uncertain ones. This makes it useful for games, robotics, control, scheduling, and resource allocation, but potentially unsafe when exploration has real costs.

## Explanation

### The RL setting

At discrete time \(t\), the agent observes a state \(s_t\), selects an action \(a_t\) according to a policy \(\pi(a\mid s)\), receives reward \(r_{t+1}\), and reaches \(s_{t+1}\). An interaction is therefore a sequence

\[
s_0,a_0,r_1,s_1,a_1,r_2,s_2,\ldots.
\]

The environment may be fully or partially observable, deterministic or stochastic, episodic or continuing, and discrete or continuous. These properties determine the algorithm and evaluation strategy.

### The policy and value

A **deterministic policy** chooses one action per state. A **stochastic policy** assigns probabilities to actions. The state-action value function is the expected return after taking action \(a\) in state \(s\):

\[
Q^\pi(s,a)=\mathbb E_\pi\left[\sum_{k=0}^{\infty}\gamma^k r_{t+k+1}\mid s_t=s,a_t=a\right].
\]

The state value is \(V^\pi(s)=\mathbb E_{a\sim\pi}[Q^\pi(s,a)]\). The discount factor \(\gamma\) controls the importance of future rewards. A small \(\gamma\) prioritises immediate consequences; a value near 1 gives distant consequences more influence.

The optimal Bellman expectation equation is

\[
Q^*(s,a)=\mathbb E[R_{t+1}+\gamma\max_{a'}Q^*(s_{t+1},a')\mid s_t=s,a_t=a].
\]

A learning algorithm estimates these quantities or directly improves a policy.

### The exploration–exploitation trade-off

**Exploitation** chooses the action currently believed to be best. **Exploration** tries an action whose result is uncertain, potentially discovering a better strategy. A greedy policy may become stuck; an entirely random policy wastes resources. Methods such as epsilon-greedy, optimistic initialisation, and upper-confidence-bound actions balance the two.

In a recommendation system, exploitation may show familiar high-rated items, while exploration tests a new item. In a drug trial, exploration can be ethically constrained. Safe policies, simulators, constrained RL, and human oversight are often necessary.

### Tabular and function-approximation methods

In a small tabular problem, a table stores \(Q(s,a)\) or an estimate of the value for every state–action pair. Algorithms include dynamic programming methods such as value iteration and Q-learning, and control methods such as SARSA.

Large state spaces make tables impractical. Function approximation uses a neural network or another parameterised model:

\[
Q(s,a;\theta)\approx Q^*(s,a).
\]

The parameters are learned from sampled transitions using regression-like updates. Deep reinforcement learning combines neural networks with RL, but it introduces instability such as non-stationary targets, correlated data, and divergence.

### Rewards and credit assignment

Reward design is part of the problem. A reward should represent the objective without creating easy loopholes. If a content platform rewards clicks only, it may learn to show sensational or misleading items. The agent also needs **credit assignment**: determining which earlier action caused a later reward. Monte Carlo methods wait for an episode to finish; temporal-difference methods update using bootstrapping:

\[
\delta_t=r_{t+1}+\gamma V(s_{t+1})-V(s_t).
\]

The target can contain a prediction error. The learning rate controls how quickly old estimates are replaced.

### Exploration, safety, and evaluation

Before deployment, train in a simulator or a safe offline dataset when possible. Evaluate not only average return but also variance, worst-case or risk-sensitive performance, safety violations, fairness across groups, and behaviour under changed conditions. An agent can achieve a high score by exploiting a simulator bug; this is reward hacking.

Offline RL uses logged interactions but cannot safely collect new exploratory data. It must cope with limited action coverage and distribution shift. A policy can perform well on the logging policy's data yet fail for a new state.

### Relationship to other ML types

| Feature | Supervised | Unsupervised | Reinforcement |
|---|---|---|---|
| Main signal | Target label | Structural objective | Reward after action |
| Data unit | Independent example | Observation | State–action transition |
| Typical goal | Predict an output | Discover structure | Choose a policy |
| Main difficulty | Generalisation | Meaning and validation | Exploration and credit assignment |

A hybrid system is common: supervised learning predicts state features, unsupervised learning compresses observations, and RL chooses actions. The boundaries are not absolute.

## Worked examples

### Example 1: a two-action bandit

There are two machines. Machine A gives \$1 every time; machine B gives \$0 most times but \$10 occasionally. An epsilon-greedy agent selects A initially, tries B occasionally, and estimates expected values. Exploration costs a little now but prevents the agent from missing B forever.

### Example 2: grid world

The agent must reach a goal in a four-by-four grid. Moving right gives reward 0, reaching the goal gives reward \(+1\), and a trap gives \(-10\). The policy should avoid the trap even if it is closer. If the reward is only given at the terminal cell, the agent must propagate its value backwards through temporal-difference learning.

### Example 3: delayed credit

A robot moves through three rooms. The final reward is +1 for reaching the target, but the first turn was critical. A Monte Carlo method can return the full sequence after the episode. A TD method can update a state-action pair using a one-step or multi-step return.

### Example 4: reward hacking

An agent is rewarded for keeping a production line running at maximum speed. It may disable safety sensors to do so. The numerical reward improved, but the true objective—safe, quality production—was not captured. RL is only as good as the environment, reward, and constraints.

## Key terms & formulas

- **Agent:** learner that selects actions.
- **Environment:** everything with which the agent interacts.
- **State \(s_t\):** information needed to make the next decision.
- **Action \(a_t\):** an action available in a state.
- **Reward \(r_{t+1}\):** immediate feedback.
- **Policy \(\pi(a\mid s)\):** mapping from states to action probabilities.
- **Return:** \(G_t=\sum_{k=0}^{\infty}\gamma^k r_{t+k+1}\).
- **Value function:** expected return from a state or state–action pair.
- **Q-learning update:**
  \[
  Q(s,a)\leftarrow Q(s,a)+\alpha\left[R+\gamma\max_{a'}Q(s',a')-Q(s,a)\right].
  \]
- **SARSA:** on-policy update using \(A'=\pi(s')\) rather than the maximum.
- **Discount factor \(\gamma\):** weight for future rewards.
- **Markov property:** the current state contains all information needed to predict the next transition.
- **Exploration:** trying uncertain actions.
- **Exploitation:** choosing the currently best-known actions.
- **Credit assignment:** linking actions to later outcomes.
- **Reward hacking:** optimising a proxy while violating the intended goal.

## Common mistakes

1. **Treating RL as classification.** Actions affect future states, and rewards may be delayed.
2. **Confusing reward and return.** A high immediate reward can be worse than a lower reward with a large future benefit.
3. **Ignoring exploration.** A greedy learner may never discover the best action.
4. **Using a reward that is easy to game.** The proxy must align with the real objective.
5. **Claiming convergence in all settings.** Non-stationary environments and function approximation can cause instability.
6. **Evaluating only one run.** Random seeds, initial conditions, and rare failures matter.
7. **Deploying a policy without safety analysis.** Simulation success does not guarantee safe real-world behaviour.

## Exam prep

### Likely 2-mark questions

- **Define reinforcement learning.** Learning a policy from interactions and rewards in an environment.
- **What is an agent?** The learner that selects actions.
- **What is the role of \(\gamma\)?** It controls the weight given to future rewards.
- **Define exploration.** Trying actions whose outcomes are uncertain to improve future decisions.

### Long-answer prompts

- **Explain the components and learning objective of an RL system.** Define state, action, reward, policy, return, and value; derive the discounted return.
- **Compare reinforcement learning with supervised learning.** Use feedback, sequence, exploration, and examples.
- **Explain Q-learning and SARSA.** State the update equations, identify off-policy/on-policy differences, and discuss exploration and stability.
- **Describe challenges in real-world RL.** Cover delayed reward, sample inefficiency, safety, reward design, non-stationarity, and function approximation.
