---
subject: sc
unit: 5
topic: discrete-markov-models
syllabus_ref: CSM3202 Unit-V
status: draft
---
# Discrete Markov Models

## Overview

A discrete Markov model (DMM) represents a finite-state process in which the next state depends only on the current state. It is the simplest sequence model in the syllabus. The transition probabilities form a stochastic matrix, and the initial state or distribution describes where the process starts.

DMMs are useful for modeling transitions such as weather changes, quality grades, machine conditions, or discrete stages of a process. They assume the Markov property, so the entire past can be summarized by the current state.

## Explanation

### 1. State and process

Let

\[
\{X_t\}_{t\ge1}
\]

be a discrete random process with state space

\[
\mathcal S=\{s_1,\ldots,s_K\}.
\]

At time \(t\), \(X_t=s_i\). The transition probability is

\[
a_{ij}=P(X_{t+1}=s_j\mid X_t=s_i).
\]

A row-stochastic transition matrix \(A\) has

\[
a_{ij}\ge0,\qquad \sum_j a_{ij}=1
\]

for every row \(i\).

### 2. Markov property

The first-order Markov assumption is

\[
P(X_{t+1}\mid X_t,X_{t-1},\ldots,X_1)
=
P(X_{t+1}\mid X_t).
\]

It says that once the current state is known, older states add no additional information about the next state under the model. A higher-order Markov model would require more recent history.

This is a modeling assumption, not proof that a real sequence is Markov. Test it with statistical or domain checks.

### 3. Initial distribution

The process begins with

\[
\boldsymbol\pi=P(X_1=s_1,\ldots,X_1=s_K),
\]

where

\[
\pi_i\ge0,\qquad\sum_i\pi_i=1.
\]

A row vector evolves by

\[
\boldsymbol\pi_{t+1}=\boldsymbol\pi_tA.
\]

After \(m\) steps,

\[
\boldsymbol\pi_{1+m}=\boldsymbol\pi_1A^m.
\]

### 4. Transition prediction

Given the current state \(s_i\), the most likely next state is

\[
s_{j^*}=\arg\max_j a_{ij}.
\]

Given a distribution \(\boldsymbol p_t\), the distribution next is

\[
p_{t+1,j}=\sum_i p_{t,i}a_{ij}.
\]

This is matrix multiplication, not a choice of one state unless the current state is known with certainty.

### 5. Joint sequence probability

A path \(x_1,\ldots,x_T\) has probability

\[
P(x_1,\ldots,x_T)
=
\pi_{x_1}
\prod_{t=1}^{T-1}a_{x_tx_{t+1}}.
\]

This product follows directly from the Markov property.

### 6. Stationarity

A distribution \(\boldsymbol\pi\) is stationary if

\[
\boldsymbol\pi A=\boldsymbol\pi.
\]

It then remains unchanged in the model at every step. A periodic chain, such as a deterministic two-state toggle, may have a stationary distribution but individual states occur periodically. A periodic or non-ergodic chain may not converge to its stationary distribution from every initial condition.

### 7. Classification of states

For a finite chain, states can be:

- **transient:** eventually leave and may not return;
- **recurrent:** return with probability one;
- **null recurrent** or **positive recurrent:** return behavior and expected time differ;
- **absorbing:** once entered, never left;
- **ergodic:** irreducible and aperiodic in the usual positive-recurrent sense.

These properties affect long-term behavior and convergence to stationary probabilities.

### 8. Communicating classes and reachability

State \(s_j\) is reachable from \(s_i\) if some positive power \(A^n\) has

\[
(A^n)_{ij}>0.
\]

A closed class has no outgoing transition to another class. Long-run probabilities depend on which class the process can reach.

### 9. Hitting and return times

For an absorbing or recurrent state, expected times can be found from the fundamental matrix or first-step equations. The expected number of visits to state \(j\) before absorption is related to

\[
N=(I-Q)^{-1},
\]

where \(Q\) is the transient-to-transient submatrix. These formulas are useful in reliability and failure analysis.

### 10. Estimation from data

Estimate

\[
\hat a_{ij}
=
\frac{\#\{t:X_t=s_i,\ X_{t+1}=s_j\}}
{\#\{t:X_t=s_i\}}.
\]

A transition not observed from a state causes a zero estimate. Add smoothing:

\[
\hat a_{ij}
=
\frac{N_{ij}+\alpha}
{\sum_jN_{ij}+\alpha K}.
\]

Rows must sum to one. If data are not stationary, use time-varying transition matrices or evaluate a specific time window.

### 11. Hidden states and DMM versus HMM

A DMM assumes the state sequence itself is observed or known. In many applications the true state is hidden and only observations are available. An HMM adds an emission model and hidden states. A DMM is therefore a special simpler sequence model, not the same thing as a full HMM.

### 12. Applications

- weather-state transitions;
- quality grades;
- machine health states;
- disease progression states;
- customer behavior states;
- network congestion states;
- reliability and failure-state chains;
- discrete event and process simulation.

### 13. Advantages

- Simple and interpretable.
- Compact transition representation.
- Efficient state probability updates.
- Useful for planning and long-run analysis.
- Easy to estimate from transition counts.

### 14. Limitations

- The first-order Markov assumption may fail.
- States may not be directly observable.
- Stationarity may not hold.
- Rare transitions may be poorly estimated.
- State definition strongly affects the model.
- A sequence-level model may be needed for longer dependencies.

## Worked examples

### Example 1: One-step prediction

Let states be Dry, Cloudy, Rain, with transition matrix

\[
A=
\begin{bmatrix}
0.7&0.3&0\\
0.2&0.5&0.3\\
0&0.4&0.6
\end{bmatrix}.
\]

If the current state is Cloudy, the next distribution is row 2:

\[
(0.2,0.5,0.3).
\]

The most likely next state is Cloudy with probability 0.5.

### Example 2: Several steps

Start with

\[
\pi_1=(1,0,0)
\]

for Dry. Then

\[
\pi_2=(0.7,0.3,0).
\]

After three transitions,

\[
\pi_4=\pi_1A^3.
\]

The first two steps give

\[
\pi_3=(0.7,0.3,0)A
=(0.55,0.36,0.09).
\]

The fourth distribution is

\[
\pi_4=(0.55,0.36,0.09)A
=(0.457,0.399,0.144).
\]

The probability of rain increases over these steps.

### Example 3: Sequence probability

For path Dry \(\to\) Cloudy \(\to\) Rain,

\[
P(\text{Dry},\text{Cloudy},\text{Rain})
=
1(0.3)(0.3)=0.09.
\]

Only the transitions after the initial state are multiplied.

### Example 4: Estimate a transition

Suppose Cloudy occurs 100 times and is followed by Dry 20 times, Cloudy 50 times, and Rain 30 times. Then

\[
(\hat a_{21},\hat a_{22},\hat a_{23})=(0.2,0.5,0.3).
\]

If no Rain transition was observed, an unsmoothed estimate would be zero; smoothing keeps a small probability for a possible transition.

## Key terms & formulas

- **State:** Value of the process at a time.
- **DMM:** Finite-state Markov model.
- **Markov property:** Next state depends only on current state.
- **Transition matrix:** \(A=[a_{ij}]\), row-stochastic.
- **Initial distribution:** \(\pi\).
- **Stationary distribution:** \(\pi A=\pi\).
- **Absorbing state:** State with no outgoing transition.
- **Ergodic chain:** Irreducible and aperiodic positive-recurrent chain.

Transition:

\[
a_{ij}=P(X_{t+1}=s_j\mid X_t=s_i).
\]

Matrix update:

\[
\boldsymbol\pi_{t+1}=\boldsymbol\pi_tA.
\]

Path probability:

\[
\pi_{x_1}\prod_{t=1}^{T-1}a_{x_tx_{t+1}}.
\]

## Common mistakes

1. **Using columns instead of rows without transposing.** State the row-vector convention.
2. **Forgetting rows of a transition matrix sum to one.** Check normalization.
3. **Assuming a chain always reaches its stationary distribution.** Periodic or non-ergodic chains may not.
4. **Ignoring the Markov assumption.** Test long-range dependencies.
5. **Using an HMM algorithm for a directly observed DMM unnecessarily.** Simplicity is useful.
6. **Estimating a zero transition without smoothing.** Rare events can be unstable.
7. **Forgetting the initial-state probability.** A path probability includes it.
8. **Interpreting a state label as certain physical truth.** It is a model state.

## Exam prep

### Likely 2-mark questions

- **Define the Markov property.**  
  **Hint:** Next state depends only on the current state.

- **Write the transition-probability equation.**  
  **Hint:** \(a_{ij}=P(X_{t+1}=j|X_t=i)\).

- **State the matrix update for a distribution.**  
  **Hint:** \(\pi_{t+1}=\pi_tA\).

- **What is a stationary distribution?**  
  **Hint:** \(\pi A=\pi\).

- **Name two DMM applications.**  
  **Hint:** Weather, health, quality, reliability, congestion, or network states.

### Likely long-answer questions

- **Explain discrete Markov models with transition and initial distributions.**  
  **Hint:** State space, Markov assumption, matrix, path probability, and prediction.

- **Work out multi-step probabilities and stationary behavior.**  
  **Hint:** Matrix multiplication, powers, absorbing/ergodic cases, and interpretation.

- **Estimate transition probabilities from data with smoothing.**  
  **Hint:** Counts, normalization, missing transitions, and stationarity.

- **Compare a DMM with an HMM.**  
  **Hint:** Observed versus hidden states, emissions, and algorithms.
