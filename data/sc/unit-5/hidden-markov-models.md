---
subject: sc
unit: 5
topic: hidden-markov-models
syllabus_ref: CSM3202 Unit-V
status: draft
---
# Hidden Markov Models

## Overview

A hidden Markov model (HMM) is a probabilistic finite-state model with a hidden state process and an observed emission process. We do not directly see the state that generated each observation; instead, we infer it from data. HMMs are used for sequence classification, speech recognition, activity monitoring, fault diagnosis, and time-series analysis.

The key algorithms are the forward algorithm for filtering, backward smoothing, and Viterbi for finding the most likely state sequence. Their results depend on correct state definitions, transition assumptions, emission models, and parameter estimation.

## Explanation

### 1. Components of an HMM

An HMM has:

1. a finite state set
   \[
   \mathcal S=\{s_1,\ldots,s_K\};
   \]
2. an initial distribution
   \[
   \pi_i=P(Z_1=s_i);
   \]
3. transition probabilities
   \[
   a_{ij}=P(Z_{t+1}=s_j\mid Z_t=s_i);
   \]
4. emission probabilities
   \[
   b_j(o_t)=P(O_t=o_t\mid Z_t=s_j).
   \]

Here \(Z_t\) is hidden state and \(O_t\) is observed symbol or continuous observation. A discrete HMM has finite emissions; a continuous-density HMM uses a Gaussian or other density.

### 2. Markov assumption

The hidden state follows a first-order Markov chain:

\[
P(Z_{t+1}\mid Z_{1:t})=P(Z_{t+1}\mid Z_t).
\]

The observation at time \(t\) depends on the current state:

\[
P(O_t\mid Z_{1:t},O_{1:t-1})
=
P(O_t\mid Z_t=s_i).
\]

Thus the model factorizes:

\[
P(Z_{1:T},O_{1:T})
=
\pi_{z_1}b_{z_1}(o_1)
\prod_{t=2}^{T}a_{z_{t-1}z_t}b_{z_t}(o_t).
\]

### 3. Why the states are hidden

In speech recognition, the hidden state may be a phoneme and the observation an acoustic frame. In monitoring, the state may be normal, warning, or failed while the observations are noisy sensor values. The hidden state is a model abstraction; it need not correspond to a directly measured physical condition.

### 4. Forward algorithm

Define the forward probability

\[
\alpha_t(i)=P(o_1,\ldots,o_t,z_t=s_i).
\]

Initialization:

\[
\alpha_1(i)=\pi_i b_i(o_1).
\]

Recursion:

\[
\alpha_{t+1}(j)
=
\left[\sum_{i=1}^{K}\alpha_t(i)a_{ij}\right]b_j(o_{t+1}).
\]

The likelihood of the complete observation sequence is

\[
P(O_{1:T})=\sum_i\alpha_T(i).
\]

In log space:

\[
\log\alpha_{t+1}(j)
=
\logsumexp_i
\left(\log\alpha_t(i)+\log a_{ij}\right)
+\log b_j(o_{t+1}).
\]

Scaling by a constant at each time prevents underflow in long sequences.

### 5. Backward algorithm

Define

\[
\beta_t(i)=P(o_{t+1},\ldots,o_T\mid z_t=s_i).
\]

Initialization:

\[
\beta_T(i)=1.
\]

Recursion:

\[
\beta_t(i)
=
\sum_{j=1}^{K}a_{ij}b_j(o_{t+1})\beta_{t+1}(j).
\]

Smoothing at time \(t\):

\[
\gamma_t(i)=P(z_t=s_i\mid o_{1:T})
=
\frac{\alpha_t(i)\beta_t(i)}
{\sum_j\alpha_t(j)\beta_t(j)}.
\]

Forward filtering uses only observations up to \(t\); smoothing uses the entire sequence and is an offline calculation.

### 6. Viterbi algorithm

Viterbi finds the most likely hidden path, not the most likely state at every individual time independently. Define

\[
\delta_t(i)
=
\max_{z_1,\ldots,z_t}
P(z_1,\ldots,z_t,o_1,\ldots,o_t,z_t=s_i).
\]

Initialization:

\[
\delta_1(i)=\pi_i b_i(o_1).
\]

Recursion:

\[
\delta_{t+1}(j)
=
b_j(o_{t+1})
\max_i\left[\delta_t(i)a_{ij}\right].
\]

The best final state is

\[
z_T^*=\arg\max_i\delta_T(i).
\]

Store backpointers

\[
\psi_{t+1}(j)=\arg\max_i[\delta_t(i)a_{ij}]
\]

and backtrack to obtain the path.

### 7. Difference between forward and Viterbi

Forward sums over all paths:

\[
\alpha_t(j)=\sum_{\text{paths ending at }j}\text{probability}.
\]

Viterbi keeps the maximum path ending at each state:

\[
\delta_t(j)=\max_{\text{paths ending at }j}\text{probability}.
\]

Forward is appropriate for filtering and likelihood; Viterbi is appropriate for a single most likely state sequence.

### 8. Discrete example

Let states be \(A=\) normal, \(B=\) degraded, \(C=\) failed, and observations be \(o_1=0,o_2=1,o_3=0\).

Initial distribution:

\[
\pi=(0.7,0.3,0).
\]

Transition matrix:

\[
A=
\begin{bmatrix}
0.8&0.2&0\\
0.1&0.7&0.2\\
0&0.3&0.7
\end{bmatrix}.
\]

Emission probabilities for observation 0 are

\[
b(0)=(0.9,0.6,0.2),
\]

and for observation 1 are

\[
b(1)=(0.1,0.4,0.8).
\]

At \(t=1\):

\[
\alpha_1
=(0.7(0.9),0.3(0.9),0(0.9))
=(0.63,0.27,0).
\]

At \(t=2\), before emission:

\[
\alpha_1A
=
(0.63(0.8)+0.27(0.1),
 0.63(0.2)+0.27(0.7)+0(0.3),
 0.63(0)+0.27(0.2)+0(0.7)).
\]

\[
=(0.504+0.027,\;0.126+0.189,\;0.054)
=(0.531,0.315,0.054).
\]

For \(o_2=1\),

\[
\alpha_2=(0.531(0.1),0.315(0.4),0.054(0.8))
=(0.0531,0.126,0.0432).
\]

At \(t=3\), before emission:

\[
\alpha_2A
=(0.0531(0.8)+0.126(0.1),
0.0531(0.2)+0.126(0.7)+0.0432(0.3),
0.126(0.2)+0.0432(0.7)).
\]

\[
=(0.04248+0.0126,
0.01062+0.0882+0.01296,
0.0252+0.03024)
\]

\[
=(0.05508,0.11178,0.05544).
\]

For \(o_3=0\):

\[
\alpha_3
=(0.05508(0.9),0.11178(0.6),0.05544(0.2))
=(0.049572,0.067068,0.011088).
\]

Observation likelihood:

\[
P(O_{1:3})=\sum_i\alpha_3(i)
=0.127728.
\]

The probability is small because three emissions must all be explained by some hidden path.

### 9. Viterbi on the same example

Initialize:

\[
\delta_1=(0.63,0.27,0).
\]

For \(o_2=1\):

\[
\delta_2(0)=0.1\max(0.63(0.8),0.27(0.1))=0.0504,
\]

\[
\delta_2(1)=0.4\max(0.63(0.2),0.27(0.7),0(0.3))
=0.4(0.189)=0.0756,
\]

\[
\delta_2(2)=0.8\max(0,0.27(0.2),0(0.7))
=0.8(0.054)=0.0432.
\]

The best final state at \(t=2\) is \(B\).

For \(o_3=0\):

\[
\delta_3(0)=0.9\max(0.0504(0.8),0.0756(0.1),0.0432(0))
=0.9(0.04032)=0.036288,
\]

\[
\delta_3(1)=0.6\max(0.0504(0.2),0.0756(0.7),0.0432(0.3))
=0.6(0.05292)=0.031752,
\]

\[
\delta_3(2)=0.2\max(0,0.0756(0.2),0.0432(0.7))
=0.2(0.03024)=0.006048.
\]

The best final state is \(A\), with score 0.036288. Backtracking depends on the stored \(\psi\) values. The Viterbi path score is not the total sequence likelihood; it is the probability of one most likely path.

### 10. Emission probabilities for continuous observations

For a continuous observation vector \(o_t\) under state \(j\),

\[
b_j(o_t)
=
\mathcal N(o_t;\mu_j,\Sigma_j).
\]

Use log densities in the recursions. Gaussian mixtures can represent multimodal emissions. Numerical scaling and covariance constraints are important.

### 11. Parameter estimation

For a fully observed HMM, count transitions and emissions. For hidden states, use the forward-backward algorithm and Baum–Welch/EM:

1. E-step: calculate \(\gamma_t(i)\) and \(\xi_t(i,j)\);
2. M-step: update
   \[
   a_{ij}=\frac{\sum_{t=1}^{T-1}\xi_t(i,j)}
   {\sum_{k}\sum_{t=1}^{T-1}\xi_t(i,k)};
   \]
3. update emissions and initial probabilities;
4. iterate until log-likelihood improvement is small.

EM converges to a local optimum and can get stuck in a poor state labeling. Initialization and model selection matter.

### 12. Forward-backward and Viterbi applications

- **Forward:** online state filtering, anomaly detection, and predictive probability.
- **Backward:** offline hidden-state smoothing and sequence annotation.
- **Viterbi:** most likely path, segmentation, decoding, and error correction.

### 13. State duration modeling

A standard HMM is a geometric-duration model. If self-loops are high, a state can persist for a long random duration. If explicit minimum or maximum durations matter, use a semi-Markov or HSMM model.

### 14. Initialization and numerical stability

Random initialization can produce different local optima. Try multiple initializations, use sensible emissions, and compare held-out likelihood. In log space, use `logsumexp`; in probability space, scale \(\alpha\) or \(\beta\) at every step.

### 15. Applications

- speech recognition;
- handwriting and gesture recognition;
- fault diagnosis;
- activity and posture monitoring;
- bioinformatics sequence analysis;
- market-state modeling;
- sensor anomaly detection;
- tracking and process monitoring.

### 16. Advantages

- Models temporal dependencies and hidden states.
- Efficient dynamic programming algorithms.
- Can combine many observations.
- Works with discrete or continuous emissions.
- Provides likelihoods for sequence comparison.

### 17. Limitations

- State identities are not always uniquely identifiable.
- First-order Markov assumptions may be too simple.
- Training can converge locally.
- Hidden-state labels may be arbitrary permutations.
- Complex continuous models require many parameters.
- Mis-specified emissions can produce confident but wrong states.

## Worked examples

### Example 1: One-step state probability

If the current hidden-state distribution is

\[
p_t=(0.6,0.3,0.1)
\]

and transition matrix is

\[
A=
\begin{bmatrix}
0.8&0.2&0\\
0.1&0.7&0.2\\
0&0.3&0.7
\end{bmatrix},
\]

then

\[
p_{t+1}=p_tA
=(0.51,0.36,0.13).
\]

Rain/failure probability increases from 0.1 to 0.13.

### Example 2: Normalize a filtered distribution

If the forward values at time \(t\) are

\[
\alpha_t=(0.06,0.03,0.01),
\]

the filtered state probabilities are

\[
\gamma_t^{\text{filtered}}
=
\frac{\alpha_t}{\sum_i\alpha_t}
=(0.6,0.3,0.1).
\]

Filtering normalizes the forward mass to a distribution over the current state.

### Example 3: Missing observation

If the next symbol is unknown, omit its emission factor when predicting the next state distribution. The forward likelihood is not updated as if the symbol were a particular value. Emission likelihoods and missing-data models must be defined.

### Example 4: Compare forward and Viterbi

Suppose at a time step the most likely current state has probability 0.5, but the globally most likely complete path assigns a different state at that time. The path is more informative for decoding, while marginal \(\gamma\) is more informative for filtering. They answer different questions.

## Key terms & formulas

- **HMM:** Hidden Markov model.
- **Hidden state:** Unobserved state \(Z_t\).
- **Emission:** \(b_j(o)=P(o|Z=j)\).
- **Forward algorithm:** Sum over paths to filter.
- **Backward algorithm:** Future likelihood and smoothing.
- **Viterbi:** Most likely complete path.
- **Baum–Welch:** EM parameter estimation.
- **Scaling:** Numerical stabilization of probabilities.

Forward:

\[
\alpha_{t+1}(j)=b_j(o_{t+1})\sum_i\alpha_t(i)a_{ij}.
\]

Backward:

\[
\beta_t(i)=\sum_j a_{ij}b_j(o_{t+1})\beta_{t+1}(j).
\]

Smoothing:

\[
\gamma_t(i)=\frac{\alpha_t(i)\beta_t(i)}
{\sum_j\alpha_t(j)\beta_t(j)}.
\]

Viterbi:

\[
\delta_{t+1}(j)=b_j(o_{t+1})\max_i[\delta_t(i)a_{ij}].
\]

## Common mistakes

1. **Using forward recursion with the Viterbi max and calling it likelihood.** Sum and max answer different questions.
2. **Forgetting the emission factor in the forward recursion.** Transition alone gives a hidden-state prediction, not observed-data likelihood.
3. **Omitting \(\pi\).** The first state is not obtained from a transition.
4. **Ignoring numerical underflow.** Scale probabilities or use log-space calculations.
5. **Calling the most likely marginal state the most likely path.** Viterbi can assign a different state at a time.
6. **Interpreting hidden states as directly observed physical labels.** They are latent model variables.
7. **Initializing Baum–Welch once.** Try multiple initializations because EM is local.
8. **Evaluating a time-dependent model with a random split.** Keep sequence order and avoid leakage.

## Exam prep

### Likely 2-mark questions

- **List the four components of an HMM.**  
  **Hint:** States, initial probabilities, transition probabilities, and emissions.

- **Write the forward recursion.**  
  **Hint:** Emission times the sum of previous states times transitions.

- **Write the Viterbi recursion.**  
  **Hint:** Emission times the maximum predecessor transition.

- **What does backward smoothing calculate?**  
  **Hint:** Posterior hidden-state probability given all observations.

- **State one use of Baum–Welch.**  
  **Hint:** Estimate HMM parameters from unlabeled sequences.

### Likely long-answer questions

- **Explain HMM structure and the Markov assumptions.**  
  **Hint:** Hidden state, observations, transition/emission probabilities, and factorization.

- **Perform a complete forward-algorithm calculation.**  
  **Hint:** Initialize alpha, recurse for each observation, and sum the final values.

- **Perform a complete Viterbi decoding calculation.**  
  **Hint:** Delta, backpointers, final state, and reconstructed path.

- **Compare forward, backward, and Viterbi algorithms.**  
  **Hint:** Filtering, smoothing, best path, time, and uses.

- **Discuss HMM parameter estimation, numerical stability, and limitations.**  
  **Hint:** Baum–Welch, log-space, multiple initializations, state identifiability, and Markov assumptions.
