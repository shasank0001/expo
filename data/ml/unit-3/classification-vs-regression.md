---
subject: ml
unit: 3
topic: classification-vs-regression
syllabus_ref: CSM3201 Unit-III
status: draft
---
# Classification vs Regression

## Overview

Classification and regression are the two central forms of supervised learning. **Classification** predicts a discrete class or category, while **regression** predicts a continuous numeric value. Both learn from labelled examples, but the output space, loss, decision rule, evaluation metrics, and uncertainty are different.

Choosing the correct form is part of problem framing. “Will a customer churn?” is a classification question; “How many months until churn?” is a regression question. The answers may be related, but they require different modelling and evaluation.

## Explanation

### Target type and output

For classification, \(Y\in\{y_1,\ldots,y_K\}\) for \(K\) classes. A model may output a hard label or probabilities

\[
p_k(x)=P(Y=y_k\mid x),\qquad \sum_{k=1}^{K}p_k(x)=1.
\]

The decision rule selects a class, often

\[
\hat y=\arg\max_k p_k(x),
\]

or a class after a cost-sensitive threshold.

For regression, \(Y\in\mathbb R\), and a model estimates a real value \(\hat y(x)\), often the conditional mean \(E[Y\mid x]\). A prediction may include an interval or distribution when uncertainty matters.

### Problems solved by each

**Classification examples:** spam versus normal e-mail, loan default yes/no, disease diagnosis, image category, sentiment label, product defect.

**Regression examples:** house price, temperature, sales demand, exam score, loan amount, time to failure, probability expressed as a calibrated percentage (though a probability target may be treated with care).

Classification labels can be binary, multiclass, multilabel, or ordinal. Regression can be ordinary, count-based (Poisson/negative-binomial style), time-to-event, or bounded. These distinctions affect the loss and output interpretation.

### Losses

For regression, common losses are

\[
L_2=(y-\hat y)^2,\qquad L_1=|y-\hat y|.
\]

Squared error penalises large misses and supports smooth linear fitting. Absolute error is more robust and is often easier to interpret in target units.

For classification, cross-entropy measures the quality of probabilities:

\[
L_{\mathrm{CE}}=-\sum_k y_k\log p_k.
\]

For a binary target, this reduces to binary cross-entropy. Hinge loss is used in some margin-based models. A class-weighted loss can reflect unequal error costs.

### Metrics

Regression commonly uses MAE, RMSE, \(R^2\), and residual diagnostics. Classification uses accuracy, precision, recall, F1, specificity, ROC-AUC, PR-AUC, log loss, and calibration. The best metric depends on the action taken after prediction. A false negative in screening may matter more than a false positive, or vice versa.

### Decision thresholds and uncertainty

A regression estimate \(\hat y=12.3\) may be rounded to 12 or 13, but a classification probability \(p=0.52\) becomes a class only after a threshold. Neither output is self-interpreting. Uncertainty, prediction intervals, and calibration help users understand confidence.

A regression model can be used for a binary decision by thresholding \(\hat y\), but that is not identical to a probability classifier. Conversely, a classifier's probability can be used as a score in some decisions, but the probability and the numeric target have different semantics.

### Relationship between tasks

Classification and regression can be connected. Logistic regression models the probability of a class and is sometimes called a classification model; a regression model can predict a risk score. Ordinal regression handles ordered labels. A multiclass classifier can be implemented through regression models, but its interpretation and loss may be awkward. A model can be trained with one objective and evaluated as another task only when the conversion is explicit.

### Model behaviour and assumptions

Regression commonly predicts a smooth average and may extrapolate in a dangerous way beyond the observed feature range. Classification often focuses on boundaries and can be accurate while poorly calibrated. Trees can solve either. Neural networks can solve both, but the output layer, loss, and evaluation change.

### Choosing between them

Ask what the decision needs:

- a category or event: classification;
- a quantity with units: regression;
- an ordered level: ordinal classification/regression;
- a count: count regression;
- a survival time: time-to-event method;
- both a score and a label: a probability or interval model may be best.

## Worked examples

### Example 1: customer churn

Binary classification predicts whether a customer cancels this month. A model outputs 0.73. If the retention offer costs ₹200 and saves ₹1,000 on average, the team can compare expected value and choose a threshold such as 0.4. Reporting 0.73 alone does not tell the team what action to take.

### Example 2: house prices

Regression predicts

\[
\hat y=50{,}000+1{,}500x_{\text{area}}+30x_{\text{rooms}}.
\]

For area 120 and rooms 3,

\[
\hat y=50{,}000+180{,}000+90=230{,}100.
\]

The output is a price estimate, not a probability. A confidence interval can describe uncertainty, and residuals identify systematic errors.

### Example 3: converting a score to a label

A risk model predicts expected loss \(\hat y=0.18\). A policy might classify the customer as “high risk” when \(\hat y>0.15\). This threshold is a decision rule, not a learned class probability. Validate its consequences separately.

### Example 4: ordinal labels

A survey has poor, fair, good, excellent. An ordinary multiclass classifier treats the order as arbitrary, while ordinal regression or a model with monotonic constraints can use the information that excellent is higher than good. The evaluation should still consider pairwise or distance-sensitive errors.

## Key terms & formulas

- **Classification:** \(Y\) is discrete.
- **Regression:** \(Y\) is continuous.
- **Binary classification:** two classes.
- **Multiclass:** more than two mutually exclusive classes.
- **Multilabel:** several labels can be present together.
- **Ordinal classification:** classes have meaningful order.
- **Squared error:** \((y-\hat y)^2\).
- **Absolute error:** \(|y-\hat y|\).
- **Cross-entropy:** \(-\sum_k y_k\log p_k\).
- **MAE:** \(\frac1n\sum_i|y_i-\hat y_i|\).
- **RMSE:** \(\sqrt{\frac1n\sum_i(y_i-\hat y_i)^2}\).
- **Threshold:** score boundary for a hard decision.
- **Calibration:** agreement between predicted and observed event rates.
- **Prediction interval:** range intended to cover an outcome with a stated probability.

## Common mistakes

1. **Using regression loss for class labels.** Treating class 0, 1, 2 as continuous imposes an artificial order.
2. **Using classification accuracy for a continuous target.** It hides the size of numerical errors.
3. **Confusing a probability with a hard class.** A threshold and decision cost are required.
4. **Ignoring class order.** Treating poor/fair/good/excellent as unordered can lose information.
5. **Using a regression model outside its training range.** Extrapolation may be nonsensical.
6. **Assuming a lower RMSE is always preferable.** Large or small errors may have different business consequences.
7. **Evaluating the converted task incorrectly.** A thresholded regression score needs its own policy analysis.

## Exam prep

### Likely 2-mark questions

- **Differentiate classification and regression.** State target type, output, one loss, and two metrics.
- **What is regression?** Predicting a continuous numeric target from input features.
- **What is classification?** Predicting a discrete class or label.
- **Why use a threshold for a probability?** To convert a score into an action according to a decision rule.

### Long-answer prompts

- **Compare classification and regression in detail.** Cover target, hypothesis space, losses, metrics, thresholds, uncertainty, and examples.
- **Explain when a regression prediction may be converted into a classification decision.** Give a risk threshold example and discuss cost and calibration.
- **Discuss how model choice changes between tasks.** Compare linear/logistic models, trees, SVMs, and neural networks.
- **Explain the special issues of ordinal classification and count regression.** Give suitable losses and evaluation ideas.
