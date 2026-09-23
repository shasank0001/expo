---
subject: dwdm
unit: 4
topic: bayes-classification
syllabus_ref: CSM3101 Unit-IV
status: draft
---
# Bayes Classification

## Overview

Bayes classification uses probability and Bayes' theorem to choose the most likely class. It asks: given the observed attributes, which class has the highest posterior probability? **Naive Bayes** makes a strong simplifying assumption that attributes are conditionally independent once the class is known. Despite that assumption, it is fast, effective for many text and categorical tasks, and a core classification method in the syllabus.

## Explanation

### 1. Bayes' theorem

For classes \(C_1,\ldots,C_K\), attributes \(X=(x_1,\ldots,x_n)\), and prior class probabilities \(P(C_i)\),

\[
P(C_i\mid X)=\frac{P(X\mid C_i)P(C_i)}{P(X)}.
\]

The denominator \(P(X)\) is the same for every class, so it can be omitted when comparing classes:

\[
C^*=\arg\max_i P(C_i)P(X\mid C_i).
\]

The model learns class priors and attribute likelihoods from labeled data. At prediction time it multiplies them and chooses the largest unnormalized posterior.

### 2. Conditional independence

Naive Bayes assumes

\[
P(X\mid C_i)=\prod_{j=1}^{n}P(x_j\mid C_i).
\]

The features are therefore independent **given the class**, not generally independent in the raw data. For example, height and weight are strongly related overall but can be treated as independent within a particular class in a simplified model. The assumption usually makes estimation feasible; it can produce overconfident probabilities when the features are strongly dependent.

### 3. Categorical naive Bayes

For categorical features, count each feature-value/class combination. With Laplace smoothing, add 1 to each count:

\[
P(x_j\mid C_i)=\frac{n_{ij}+\alpha}{n_i+\alpha V_j},
\]

where \(n_{ij}\) is the count of value \(x_j\) in class \(i\), \(n_i\) is the class total, \(V_j\) is the number of possible values, and \(\alpha=1\) is standard.

### 4. Gaussian naive Bayes

Continuous features are often modeled by a normal distribution within each class:

\[
P(x_j\mid C_i)=\frac{1}{\sqrt{2\pi\sigma_{ij}^2}}
\exp\left[-\frac{(x_j-\mu_{ij})^2}{2\sigma_{ij}^2}\right].
\]

Estimate a separate mean and variance for each feature and class. The class with the largest joint score is selected. This is not the same as assuming the whole feature is one Gaussian mixture with a shared variance.

### 5. Bernoulli and other variants

**Bernoulli naive Bayes** is common for binary features: each feature records presence or absence. Multinomial naive Bayes counts repeated word occurrences in text; binarized Bernoulli variants count presence. The count definition and feature encoding must be consistent with the algorithm.

### 6. Zero-frequency and probability underflow

A value never observed in a class can make a categorical likelihood zero, eliminating that class. Laplace smoothing avoids exact zeros. Numerically, multiplying many tiny values can underflow, so implementations calculate log scores:

\[
\log S_i=\log P(C_i)+\sum_j\log P(x_j\mid C_i).
\]

Choosing the largest log score is equivalent to choosing the largest probability, because logarithm is monotonic.

### 7. Priors, calibration, and evaluation

A prior can be estimated from the training distribution or set from domain knowledge. Because the naive model can overstate certainty, probability calibration may be useful when decisions depend on exact probabilities. Classification accuracy depends on the chosen decision rule; always evaluate with appropriate class-wise and threshold metrics.

### 8. Strengths and limitations

**Strengths:** small prediction cost, simple training, works with many features, robust baseline for text/categorical data, supports incremental updates.

**Limitations:** conditional independence can be unrealistic; correlated features are counted twice; a zero-likelihood feature can erase a class without smoothing; poor probability calibration; missing-value and nonstationarity handling still require design.

## Worked examples

### Example 1: Categorical naive Bayes by counts

Training data:

| Class | Color | Shape |
|---|---|---|
| A | red | round |
| A | red | square |
| A | blue | round |
| B | green | round |
| B | yellow | square |

Suppose a new object is `red, round`. Estimate priors \(P(A)=3/5\), \(P(B)=2/5\). With Laplace smoothing and two possible colors and two shapes:

For A:

\[
P(\text{red}|A)=\frac{2+1}{3+2}=\frac12,\quad
P(\text{round}|A)=\frac{2+1}{3+2}=\frac12.
\]

For B:

\[
P(\text{red}|B)=\frac{0+1}{2+2}=\frac14,\quad
P(\text{round}|B)=\frac{1+1}{2+2}=\frac12.
\]

Scores:

\[
S(A)=\frac35\cdot\frac12\cdot\frac12=0.15,
\]
\[
S(B)=\frac25\cdot\frac14\cdot\frac12=0.05.
\]

Normalize: \(P(A\mid X)=0.15/(0.15+0.05)=0.75\), \(P(B\mid X)=0.25\). Predict A.

Without smoothing, \(P(\text{red}|B)=0\), so B would have zero posterior. The smoothed estimate is a modeling assumption, not proof that red is common in B.

### Example 2: Gaussian calculation

Training class C has feature X values 2, 4, 4, 6. Using population variance for the fitted Gaussian, estimate

\[
\mu=4,\qquad \sigma^2=\frac{(2-4)^2+(4-4)^2+(4-4)^2+(6-4)^2}{4}=2.
\]

For a new value \(x=3\),

\[
P(x|C)=\frac{1}{\sqrt{2\pi(2)}}
e^{-(3-4)^2/(2\cdot2)}
\approx0.220.
\]

If another class C2 has \(\mu_2=10,\sigma_2^2=4\) and the same prior, its likelihood is much smaller, so C wins. The full classifier must multiply all feature likelihoods and the prior.

### Example 3: Gaussian with multiple features

Let a class have \(\mu_A=(3,5)\), \(\sigma_A^2=(1,4)\). A new point is \(x=(3,7)\). Its likelihood score (ignoring the common normal constants for comparison) is

\[
\exp[-((3-3)^2/2+(7-5)^2/8)]
=\exp[-0.5]\approx0.607.
\]

If another class has means (3,9) and variances (1,4), its score is

\[
\exp[-((3-3)^2/2+(7-9)^2/8)]
=\exp[-0.5],
\]

a tie. The priors and exact normalization then determine the class. This illustrates why numerical precision and all features matter.

### Example 4: Log scores

Suppose class A has prior 0.3 and feature likelihoods 0.4, 0.5, 0.2. The product is 0.012. Class B has prior 0.7 and likelihoods 0.3, 0.6, 0.9, product 0.1134. B wins. Log scores are approximately `ln(0.012)=-4.42` and `ln(0.1134)=-2.18`. Comparing logs avoids underflow without changing the ranking.

## Key terms & formulas

- **Prior:** \(P(C)\).
- **Likelihood:** \(P(X\mid C)\).
- **Posterior:** \(P(C\mid X)\).
- **Bayes theorem:** \(P(C\mid X)=P(X\mid C)P(C)/P(X)\).
- **Naive assumption:** \(P(X\mid C)=\prod_jP(x_j\mid C)\).
- **Laplace smoothing:** add \(\alpha\) to category counts.
- **Gaussian likelihood:** mean/variance per feature and class.
- **Log score:** \(\log P(C)+\sum_j\log P(x_j\mid C)\).
- **Calibration:** agreement between predicted and observed frequencies.

## Common mistakes

1. **Using likelihood instead of posterior:** multiply by the prior or compare the full score.
2. **Reversing \(P(C\mid X)\) and \(P(X\mid C)\):** they answer different questions.
3. **Assuming features are unconditionally independent:** independence is conditional on class.
4. **Leaving unseen categories at zero probability:** use smoothing or another justified method.
5. **Using a shared Gaussian variance when class-specific variance is intended:** check the chosen variant.
6. **Treating naive Bayes probability as perfectly calibrated:** evaluate or calibrate when probabilities matter.

## Exam prep

**Likely 2-mark questions**
1. State Bayes' theorem. *Hint: posterior equals prior times likelihood divided by evidence.*
2. State the naive Bayes independence assumption. *Hint: feature likelihoods multiply conditional on the class.*
3. Why is Laplace smoothing used? *Hint: prevent zero probabilities for unseen category-class pairs.*

**Likely long-answer questions**
1. Derive the naive Bayes classifier from Bayes' theorem. *Hint: cancel common evidence and apply conditional independence.*
2. Perform a complete categorical naive Bayes classification with smoothing. *Hint: priors, likelihoods, products, normalization, and decision.*
3. Explain Gaussian naive Bayes for a continuous attribute. *Hint: class means/variances, density, multiplication, log arithmetic.*
4. Compare strengths and limitations of naive Bayes. *Hint: speed and baseline versus independence and calibration problems.*
