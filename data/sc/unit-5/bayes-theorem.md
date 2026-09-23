---
subject: sc
unit: 5
topic: bayes-theorem
syllabus_ref: CSM3202 Unit-V
status: draft
---
# Bayes' Theorem

## Overview

Bayes' theorem updates a prior belief about a hypothesis after observing evidence. It is the foundation of Bayesian reasoning: the posterior combines what was believed before with how likely the evidence is under each hypothesis.

The theorem is especially useful when the probability of a cause given a symptom is needed, because diagnosis questions often provide \(P(\text{symptom}\mid\text{disease})\) rather than \(P(\text{disease}\mid\text{symptom})\).

## Explanation

### 1. Conditional probability

For events \(A\) and \(B\) with \(P(B)>0\),

\[
P(A\mid B)=\frac{P(A\cap B)}{P(B)}.
\]

\(P(A\mid B)\) is the probability of \(A\) when \(B\) is known. The order matters: generally

\[
P(A\mid B)\ne P(B\mid A).
\]

The denominator is a normalization constant that makes the probabilities over hypotheses sum to 1.

### 2. Bayes' theorem

For a hypothesis \(H_j\) and evidence \(E\),

\[
P(H_j\mid E)
=
\frac{P(E\mid H_j)P(H_j)}
{\sum_kP(E\mid H_k)P(H_k)}.
\]

- \(P(H_j)\): prior probability;
- \(P(E\mid H_j)\): likelihood of evidence under \(H_j\);
- \(P(E\mid H_j)P(H_j)\): unnormalized posterior;
- \(P(H_j\mid E)\): posterior probability;
- \(P(E)\): total probability.

For two hypotheses,

\[
P(H_1\mid E)
=
\frac{P(E\mid H_1)P(H_1)}
{P(E\mid H_1)P(H_1)+P(E\mid H_2)P(H_2)}.
\]

### 3. Natural-frequency representation

Posterior probabilities can be easier to understand as frequencies. Suppose 1,000 people are in a population:

- 100 have disease \(D\), and 900 do not;
- the test detects the disease in 90 of the 100 diseased people;
- it gives a false positive in 45 of the 900 healthy people.

The test produces 90 true positives and 45 false positives. Among the 135 positive tests,

\[
P(D\mid +)=\frac{90}{90+45}=\frac23.
\]

The rare prior limits the posterior even though the test is fairly sensitive. This is a useful way to explain the base-rate effect.

### 4. Prior, likelihood, and posterior

A prior should represent knowledge before the current evidence. A likelihood is a conditional model, not a probability of the hypothesis:

\[
P(E\mid H)\ne P(H\mid E).
\]

Posterior probabilities must sum to 1:

\[
\sum_jP(H_j\mid E)=1.
\]

If likelihoods or priors are changed, the posterior changes. A weak or biased prior can dominate a large likelihood when the evidence is rare.

### 5. Odds form

Bayes' theorem can be written as posterior odds:

\[
\frac{P(H\mid E)}{P(\neg H\mid E)}
=
\frac{P(H)}{P(\neg H)}
\frac{P(E\mid H)}{P(E\mid\neg H)}.
\]

Thus

\[
\text{posterior odds}
=
\text{prior odds}\times\text{likelihood ratio}.
\]

A likelihood ratio of 1 leaves the odds unchanged. A ratio greater than 1 supports \(H\); below 1 supports \(\neg H\).

### 6. Multiple pieces of evidence

For conditionally independent evidence \(E_1,\ldots,E_n\),

\[
P(H\mid E_1,\ldots,E_n)
=
\frac{P(H)\prod_iP(E_i\mid H)}
{\sum_kP(H_k)\prod_iP(E_i\mid H_k)}.
\]

In odds form,

\[
\text{posterior odds}
=
\text{prior odds}
\prod_i\text{likelihood ratio}_i.
\]

If evidence is dependent, multiplying individual likelihoods can double-count evidence. A Bayesian network or a joint likelihood must model the dependency.

### 7. Sequential updating

Bayes' theorem can be applied one observation at a time:

\[
P(H\mid E_{1:t})
=
\frac{P(E_t\mid H)P(H\mid E_{1:t-1})}
{P(E_t\mid E_{1:t-1})}.
\]

The posterior after the previous observations becomes the new prior. This is valid because the posterior is a coherent probability distribution, not necessarily because the data were independent.

### 8. Bayesian decision making

Choose the action with the largest expected utility, not necessarily the largest posterior:

\[
a^*=\arg\max_a\sum_jP(H_j\mid E)U(a,H_j).
\]

A rare high-probability outcome with a catastrophic cost can outweigh a more likely outcome with a small cost.

### 9. Calibration

A probability is calibrated if events assigned probability \(p\) occur approximately \(p\) of the time in the long run. A model can rank cases well but still produce poorly calibrated probabilities. Evaluate with a reliability diagram, Brier score, or log loss on held-out data.

### 10. Common applications

- medical diagnosis;
- spam filtering;
- risk assessment;
- sensor diagnosis;
- reliability and fault analysis;
- adaptive systems;
- parameter learning in probabilistic models.

### 11. Assumptions and limitations

- Conditional probabilities and event definitions must be meaningful.
- Evidence models can be difficult to estimate.
- Priors can be subjective and sensitive.
- Independence assumptions are often wrong.
- Rare events and selection bias can distort priors.
- Posterior probability is not a guarantee about an individual outcome.

## Worked examples

### Example 1: Medical test

Let

\[
P(D)=0.01,\quad P(+|D)=0.9,\quad P(+|\neg D)=0.05.
\]

The total positive probability is

\[
P(+)=0.9(0.01)+0.05(0.99)=0.009+0.0495=0.0585.
\]

Then

\[
P(D|+)=\frac{0.009}{0.0585}=0.153846.
\]

A positive test raises the probability from 1% to about 15.4%, but most positive tests are still false positives because the disease is rare.

### Example 2: Two hypotheses

Suppose a fault is either A or B:

\[
P(A)=0.7,\quad P(B)=0.3,
\]

\[
P(E|A)=0.8,\quad P(E|B)=0.2.
\]

The evidence probability is

\[
P(E)=0.8(0.7)+0.2(0.3)=0.56+0.06=0.62.
\]

Then

\[
P(A|E)=\frac{0.56}{0.62}=0.903226,
\]

\[
P(B|E)=\frac{0.06}{0.62}=0.096774.
\]

The posterior probabilities sum to 1.

### Example 3: Odds form

Prior odds are

\[
\frac{0.01}{0.99}=0.010101.
\]

Likelihood ratio:

\[
\frac{0.9}{0.05}=18.
\]

Posterior odds:

\[
0.010101(18)=0.181818.
\]

Convert to probability:

\[
\frac{0.181818}{1+0.181818}=0.153846,
\]

matching the first example.

### Example 4: Two independent pieces of evidence

Let a hypothesis have prior 0.5, and two observations have likelihoods 0.8 and 0.6 under the hypothesis. Under the alternative, their likelihoods are 0.4 and 0.2.

Hypothesis mass:

\[
0.5(0.8)(0.6)=0.24.
\]

Alternative mass:

\[
0.5(0.4)(0.2)=0.04.
\]

Posterior:

\[
P(H\mid E_1,E_2)=\frac{0.24}{0.28}=0.857143.
\]

This multiplication assumes the conditional independence required by the model.

## Key terms & formulas

- **Prior:** \(P(H)\)
- **Evidence:** Observed event or data
- **Likelihood:** \(P(E\mid H)\)
- **Posterior:** \(P(H\mid E)\)
- **Marginal probability:** \(P(E)\)
- **Likelihood ratio:** \(P(E\mid H)/P(E\mid\neg H)\)
- **Calibration:** Agreement of predicted probabilities with observed frequencies.

Bayes:

\[
P(H_j\mid E)=\frac{P(E\mid H_j)P(H_j)}
{\sum_kP(E\mid H_k)P(H_k)}.
\]

Odds:

\[
\frac{P(H\mid E)}{P(\neg H\mid E)}
=
\frac{P(H)}{P(\neg H)}
\frac{P(E\mid H)}{P(E\mid\neg H)}.
\]

## Common mistakes

1. **Reversing conditional probability.** \(P(D|+)\) is not \(P(+|D)\).
2. **Forgetting the prior.** A likelihood alone is not a posterior.
3. **Ignoring the total-probability denominator.** Posterior values will not sum to 1.
4. **Multiplying dependent evidence without a dependency model.** Double counting occurs.
5. **Using a posterior as a guarantee for one case.** It is a probability under the model.
6. **Ignoring base rates.** A sensitive test can still have a low posterior in a rare condition.
7. **Treating a prior as unquestionable.** Priors should be stated and sensitivity-tested.

## Exam prep

### Likely 2-mark questions

- **State Bayes' theorem.**  
  **Hint:** Posterior equals likelihood times prior divided by evidence probability.

- **Define prior, likelihood, and posterior.**  
  **Hint:** Knowledge before evidence, \(P(E|H)\), and updated belief \(P(H|E)\).

- **Write the two-hypothesis form of Bayes' theorem.**  
  **Hint:** Normalize the two weighted likelihoods.

- **State the odds form of Bayes' theorem.**  
  **Hint:** Posterior odds = prior odds times likelihood ratio.

- **What is calibration?**  
  **Hint:** Agreement between predicted probabilities and observed frequencies.

### Likely long-answer questions

- **Explain Bayes' theorem with prior, likelihood, evidence, and posterior.**  
  **Hint:** Definitions, two-hypothesis formula, and interpretation.

- **Work out a diagnostic test problem using natural frequencies.**  
  **Hint:** Population counts, true/false positives, posterior ratio, and base rate.

- **Explain sequential and multiple-evidence Bayesian updating.**  
  **Hint:** Posterior becomes prior, likelihood multiplication, independence caveat.

- **Discuss applications, assumptions, and limitations of Bayes' theorem.**  
  **Hint:** Diagnosis, risk, prior sensitivity, data quality, and decision utility.
