---
subject: sc
unit: 5
topic: advanced-machine-learning
syllabus_ref: CSM3202 Unit-V
status: draft
---
# Introduction to Advanced Machine Learning Techniques

## Overview

Advanced machine-learning techniques use statistical learning, optimization, graph structure, or hidden state to solve tasks that ordinary rule-based methods handle poorly. The CSM3202 syllabus groups support vector machines, Bayesian reasoning, Dempster–Shafer theory, certainty factors, and Markov models under this unit.

These methods differ in what they model. SVMs seek a maximum-margin decision boundary. Bayesian methods update belief with evidence. Dempster–Shafer theory represents support for sets of hypotheses. Certainty factors combine rule-like confidence. Markov models represent dependence through states and transitions.

The common workflow is to define the data, choose an appropriate representation, estimate parameters, evaluate uncertainty or generalization, and validate on unseen data.

## Explanation

### 1. Why advanced methods?

Simple linear or rule-based models assume a particular structure. Advanced methods can handle:

- nonlinear boundaries;
- limited labeled data;
- uncertain or missing evidence;
- dependencies among variables;
- sequences and hidden states;
- multiple hypotheses and belief.

They are not automatically superior. A simpler model may be more interpretable and robust when its assumptions hold.

### 2. Support vector machines

A binary SVM finds a hyperplane

\[
\mathbf w^{\mathsf T}\mathbf x+b=0
\]

that separates classes with a large margin. Support vectors are the samples closest to the boundary. For linearly separable data,

\[
y_i(\mathbf w^{\mathsf T}\mathbf x_i+b)\ge1.
\]

The objective is often

\[
\min_{\mathbf w,b}\frac12\|\mathbf w\|^2
\]

subject to those constraints. For nonseparable data, slack variables and a penalty allow violations. A kernel maps inputs to a feature space.

SVMs are strong for small-to-medium, high-dimensional classification and regression. They need scaling, kernel selection, and regularization.

### 3. Bayesian reasoning

Bayes' theorem revises a prior:

\[
P(H\mid E)=\frac{P(E\mid H)P(H)}{P(E)}.
\]

A Bayesian belief network is a directed acyclic graph whose nodes are random variables and edges represent conditional dependencies. It supports exact inference in small networks and approximate inference in large ones.

Probability is especially useful when evidence is observed repeatedly and likelihoods can be estimated from data.

### 4. Dempster–Shafer theory

Dempster–Shafer evidence theory represents belief using a frame of discernment

\[
\Theta=\{H_1,\ldots,H_K\}.
\]

A mass function \(m\) assigns mass to focal sets:

\[
m(\varnothing)=0,\qquad \sum_{A\subseteq\Theta}m(A)=1.
\]

Evidence from independent sources is combined using Dempster's rule. Unlike probability, it can assign mass to a set of alternatives rather than committing to one. It is useful when hypotheses are ambiguous and probability estimates are unavailable, though conflict normalization and independence assumptions require care.

### 5. Certainty-factor model

A certainty factor represents a fact's confidence:

\[
CF(h,e)\in[-1,1].
\]

Positive CF supports a hypothesis, negative CF opposes it, and zero means no evidence. A simple combination rule is

\[
CF(h,e_1,e_2)
=
CF(h,e_1)+CF(e_2(1-CF(h,e_1))).
\]

Certainty factors are rule-based and easy to explain, but they are heuristic, not automatically calibrated probabilities. Combining independent-looking factors can overstate confidence.

### 6. Markov models

A discrete Markov model assumes the next state depends only on the current state:

\[
P(X_{t+1}\mid X_0,\ldots,X_t)
=
P(X_{t+1}\mid X_t).
\]

A **Discrete Markov Model (DMM)** directly represents states, often with transition and emission probabilities. A **Hidden Markov Model (HMM)** has a hidden state process and an observed emission process. It is useful for sequences where the true state is not directly visible.

### 7. Choosing a method

| Need | Starting method |
|---|---|
| Maximum-margin classification/regression | SVM |
| Prior/posterior with evidence | Bayes' theorem |
| Conditional dependencies | Bayesian network |
| Conflicting, set-valued evidence | Dempster–Shafer |
| Explainable rule confidence | Certainty factors |
| Observable state sequence | DMM |
| Hidden states generating observations | HMM |

The choice should reflect the data-generating process and operational requirements.

### 8. Parameter estimation and validation

Maximum likelihood estimates parameters from observed data. Bayesian methods may include priors and posterior inference. Cross-validation estimates generalization. For sequential models, evaluate likelihood or prediction metrics on held-out sequences, respecting time order.

Probability models require checking calibration, missing-data assumptions, and independence. An SVM requires checking scaling, \(C\), kernel, and class imbalance. A D-S or certainty model requires checking evidence independence and conflict.

### 9. Interpretability and uncertainty

SVM decisions can be explained by support vectors and kernel terms, but many support vectors may make the explanation complex. Bayesian networks expose conditional structure but may be large. D-S theory gives belief masses over sets. Certainty factors are readable rules. HMM state probabilities are latent interpretations rather than direct observed truths.

No method's internal score is automatically a calibrated real-world probability.

### 10. Applications

- SVM: text, image, intrusion, and bioinformatics classification.
- Bayesian networks: diagnosis, reliability, risk, and Bayesian decision support.
- D-S: sensor fusion, fault diagnosis, and ambiguous evidence.
- Certainty factors: expert systems and rule-based diagnosis.
- DMM/HMM: speech, time-series state tracking, and activity monitoring.

### 11. Advantages of advanced methods

- Can represent nonlinear or uncertain relationships.
- Can combine evidence from multiple sources.
- Provide principled inference when assumptions are valid.
- Can model temporal dependencies.
- May work well with limited or structured data.

### 12. Limitations

- Strong modeling assumptions.
- Probability calibration may be difficult.
- Inference can be computationally expensive.
- SVMs can be slow with very large datasets.
- D-S conflict can be severe.
- Certainty factors are heuristic.
- Hidden-state interpretations can be non-unique.
- Complex models can be harder to validate and explain.

## Worked examples

### Example 1: Choose a method for a problem

A system has noisy temperature, vibration, and acoustic sensors and must combine their conflicting reports about a motor fault. D-S theory can assign belief to “bearing fault” or “bearing or sensor fault.” A simple certainty-factor expert system may be enough if a small rule base exists, while an HMM is more appropriate when fault states evolve over time.

### Example 2: SVM versus HMM

For classifying a static image, an SVM or CNN is appropriate. For recognizing a sequence of speech observations, an HMM models the hidden phoneme/state sequence. The method follows the structure of the data.

### Example 3: Probability and evidence

If 1% of machines fail, a failure prior is \(P(F)=0.01\). A test has sensitivity 0.9 and false-positive rate 0.05. Bayes' theorem can compute the posterior. The test score is not a fuzzy membership; it is a probability under the model.

## Key terms & formulas

- **SVM:** Maximum-margin support vector machine.
- **Bayes' theorem:** Posterior from prior and likelihood.
- **D-S theory:** Dempster–Shafer belief theory.
- **Certainty factor:** \(CF\in[-1,1]\) confidence measure.
- **DMM:** Discrete Markov model.
- **HMM:** Hidden Markov model.
- **Calibration:** Agreement between predicted probabilities and observed frequencies.
- **Maximum likelihood:** Parameter values maximizing observed-data likelihood.

Bayes:

\[
P(H\mid E)=\frac{P(E\mid H)P(H)}{P(E)}.
\]

Markov property:

\[
P(X_{t+1}\mid X_{0:t})=P(X_{t+1}\mid X_t).
\]

SVM margin objective:

\[
\min_{\mathbf w,b}\frac12\|\mathbf w\|^2.
\]

## Common mistakes

1. **Calling every uncertainty method probability.** Membership, certainty factors, belief masses, and probabilities have different meanings.
2. **Ignoring model assumptions.** Independence, stationarity, and hidden-state assumptions may be false.
3. **Using a complex model without a baseline.** Validate against simpler alternatives.
4. **Interpreting an uncalibrated score as a real probability.** Calibrate on held-out data.
5. **Ignoring temporal order in sequence validation.** Random splits can leak future information.
6. **Combining D-S evidence from highly dependent sources without checking conflict.** The combination rule assumes a particular independence interpretation.
7. **Using an HMM state label as a guaranteed physical truth.** States are latent and may have multiple interpretations.

## Exam prep

### Likely 2-mark questions

- **List the advanced machine-learning techniques in Unit V.**  
  **Hint:** SVM, Bayes/Bayesian networks, D-S, certainty factors, DMM, and HMM.

- **Define a support vector machine.**  
  **Hint:** Maximum-margin classifier/regressor with a kernel for nonlinear data.

- **State Bayes' theorem.**  
  **Hint:** Posterior proportional to likelihood times prior.

- **What is the Markov property?**  
  **Hint:** Next state depends only on the current state.

- **Name one limitation of an HMM.**  
  **Hint:** Hidden states, assumptions, computational cost, or identifiability.

### Likely long-answer questions

- **Compare SVM, Bayesian methods, and Markov models.**  
  **Hint:** Representation, objective, assumptions, inference, and applications.

- **Explain the role of uncertainty in advanced machine learning.**  
  **Hint:** Probability, evidence, certainty, hidden states, calibration, and decision-making.

- **Select an appropriate method for three classification or sequence problems.**  
  **Hint:** Match data structure, uncertainty, and explainability to the method.

- **Discuss advantages and limitations of advanced machine-learning techniques.**  
  **Hint:** Power, assumptions, cost, calibration, interpretability, and validation.
