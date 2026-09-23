---
subject: ml
unit: 1
topic: types-of-machine-learning
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Types of Machine Learning

## Overview

Machine-learning tasks are commonly classified by the kind of information and feedback available while the system learns. The three central types are **supervised learning**, **unsupervised learning**, and **reinforcement learning**. They differ mainly in the data, the feedback signal, and the question being answered—not necessarily in the mathematical algorithms that can be used.

These categories are useful for choosing a learning design. If a business has target outcomes, supervised learning is usually natural. If it has only customer records and wants to find groups, an unsupervised method is appropriate. If a robot must choose actions whose effects are learned through repeated interaction, reinforcement learning is a natural fit.

## Explanation

### 1. Supervised learning

In supervised learning, every training example has an input and a known target:

\[
D=\{(x_i,y_i)\}_{i=1}^{n}.
\]

The learner approximates a function \(h:X\to Y\). The target supplies direct feedback: the prediction can be compared with the correct answer after each example or after a batch.

**Main tasks:**

- **Classification:** \(Y\) is a category. Examples: spam/not spam, disease/no disease, image class.
- **Regression:** \(Y\) is a real number. Examples: price, temperature, demand, time to failure.
- **Ranking, tagging, and structured prediction** are related supervised settings.

A supervised workflow defines a target, creates a representative labelled data set, trains a model, and evaluates it on held-out data. The label must be correct and available at training time. A customer identifier or a quantity measured after the prediction may not be a valid label for every use case.

**Strengths:** direct feedback, objective metrics, and a clear deployment output.
**Weaknesses:** labels can be expensive, incomplete, biased, or unavailable; correlation can be mistaken for causation.

### 2. Unsupervised learning

In unsupervised learning, the training data usually has features but no target:

\[
D=\{x_1,x_2,\ldots,x_n\}.
\]

The algorithm optimises a structural objective, such as compactness, separation, density, reconstruction error, or rule interestingness. Clustering is the most common example, but dimensionality reduction, density estimation, anomaly detection, and association-rule mining are also unsupervised.

There is no automatically correct cluster label. A domain expert must decide whether the discovered structure is useful. Evaluation can use internal measures such as silhouette score and external labels when available, plus business validation.

**Strengths:** works when labels are scarce and can reveal unexpected structure.
**Weaknesses:** “meaning” is subjective; preprocessing and distance choices strongly affect results; the objective may not match the business goal.

### 3. Reinforcement learning

In reinforcement learning, an **agent** interacts with an **environment**. At time \(t\), it observes state \(s_t\), takes action \(a_t\), receives reward \(r_{t+1}\), and moves to \(s_{t+1}\). It learns a policy \(\pi(a\mid s)\) that maximises expected cumulative reward:

\[
J(\pi)=\mathbb E_\pi\left[\sum_{t=0}^{\infty}\gamma^t r_{t+1}\right],
\]

where \(0\le\gamma<1\) discounts future rewards.

Unlike supervised learning, there is usually no clean target for every decision. The consequence of an action may arrive later, and exploration is needed to discover useful behaviour. Examples include game playing, robot control, resource allocation, and some recommendation systems.

**Strengths:** learns sequential decisions from consequences.
**Weaknesses:** expensive or unsafe exploration, reward design, delayed credit assignment, and instability.

### Other important types

- **Semi-supervised learning:** combines a small labelled set with many unlabelled examples. It can help when labels are expensive but unlabelled data is plentiful.
- **Self-supervised learning:** creates a target from part of an unlabelled example, for example predicting a masked word or a removed image region.
- **Transfer learning:** reuses a representation or parameters learned on a source task for a related target task.
- **Online/streaming learning:** updates as new observations arrive. It must handle concept drift and cannot simply revisit old examples.
- **Multi-task and multi-agent learning:** learns related tasks or several interacting agents.
- **Federated learning:** trains across devices or organisations while keeping raw data more local; it is a distributed learning design, not automatically a private one.

### How to choose a type

Ask these questions:

1. Is a target outcome available for each example? If yes, consider supervised learning.
2. Is the goal to discover structure without labels? Consider unsupervised learning.
3. Are actions followed by consequences and does the learner need a policy? Consider reinforcement learning.
4. Are labels partially available? Consider semi-supervised or self-supervision.
5. Is the data arriving continuously? Include an update and drift strategy.

The categories overlap. A recommender may use supervised learning to predict ratings, unsupervised clustering to group users, and reinforcement learning to optimise long-term engagement. A neural network can be trained in several ways; “deep learning” is an architecture family, not a separate learning paradigm.

## Worked examples

### Example 1: choosing a type

A bank has historical records with a column saying whether a loan default occurred. Predicting default is supervised classification. The bank has customer spending records but no labels and wants to find spending segments: unsupervised clustering. A mobile game wants to learn which button presses maximise long-term reward: reinforcement learning.

### Example 2: delayed reward

A delivery agent takes a short route but arrives late and loses a customer; a longer route is safer and earns a larger long-term reward. A supervised dataset may not label every route as good or bad. An RL agent can learn from the cumulative outcome, provided the reward correctly represents the business objective.

### Example 3: semi-supervision

A medical imaging archive contains 500 scans labelled “malignant” or “benign” and 50,000 unlabelled scans. A semi-supervised classifier can use the labels plus the unlabelled distribution, but it must be tested on a truly independent labelled test set.

### Example 4: self-supervision

Mask 15% of the words in a sentence and train a model to predict the missing words. The target is generated from the input, so the data can be unlabelled by a human while still providing a learning signal.

## Key terms & formulas

- **Supervised learning:** learning from \((x,y)\) pairs.
- **Unsupervised learning:** learning structure from \(x\)'s without target labels.
- **Reinforcement learning:** learning a policy from state–action–reward interaction.
- **Classification:** predicting a discrete class.
- **Regression:** predicting a continuous target.
- **Clustering:** grouping similar observations.
- **Policy:** \(\pi(a\mid s)\), the agent's action distribution for a state.
- **Reward:** immediate numerical feedback from the environment.
- **Return:** discounted sum of future rewards.
- **Exploration:** trying actions whose value is uncertain.
- **Exploitation:** choosing the currently believed best action.
- **Semi-supervision:** learning with both labelled and unlabelled data.
- **Self-supervision:** targets derived automatically from the data.
- **Transfer learning:** reusing knowledge from one task for another.
- **Concept drift:** the relationship \(P(x,y)\) changes over time.

## Common mistakes

1. **Saying unsupervised learning has no feedback.** It has an objective or similarity feedback, just no target labels.
2. **Treating reinforcement learning as ordinary trial-and-error without a state or policy.** The environment, return, and decision sequence are essential.
3. **Confusing classification and regression because both are supervised.** The target type and loss usually differ.
4. **Claiming the three types cannot be combined.** Real systems routinely combine them.
5. **Calling a deep network a learning type.** Deep learning describes architectures and often the training method, not the label availability.
6. **Choosing a type from the algorithm name.** The available data and objective come first.

## Exam prep

### Likely 2-mark questions

- **List the three main types of ML.** Supervised, unsupervised, and reinforcement learning.
- **How does supervised learning receive feedback?** Through a known target label for each training example.
- **What is a cluster?** A group of observations judged similar under a chosen representation and similarity measure.
- **Define exploration in RL.** Trying actions whose outcomes are uncertain in order to learn.

### Long-answer prompts

- **Explain the three types of machine learning.** Include data, feedback, objective, examples, strengths, and limitations for each; end with a selection decision tree.
- **Compare supervised and unsupervised learning.** Discuss labels, tasks, metrics, interpretability, and examples.
- **Explain reinforcement learning and its main components.** Define agent, environment, state, action, reward, policy, return, and the role of exploration.
- **Describe semi-supervised, self-supervised, and transfer learning.** Give one use case and explain how each obtains a training signal.
