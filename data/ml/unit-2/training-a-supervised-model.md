---
subject: ml
unit: 2
topic: training-a-supervised-model
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Training a Supervised Model

## Overview

Training a supervised model means using labelled examples to estimate the parameters of a hypothesis and select a state that performs well on unseen data. The algorithm is only one part: the data split, preprocessing, loss, optimiser, regularisation, validation, and stopping rule determine what is learned.

Training should answer three questions: what is being predicted, what counts as a good prediction, and how will we know that the fitted model generalises? The same framework works for linear regression, logistic regression, decision trees, support-vector machines, and neural networks.

## Explanation

### The supervised training loop

1. Choose a target and prediction-time input definition.
2. Split or resample data into training and validation roles without leakage.
3. Fit preprocessing on the training portion.
4. Initialise a model and its parameters.
5. Compute predictions on a batch or full training set.
6. Calculate the loss against known targets.
7. Update parameters using an optimiser such as gradient descent.
8. Evaluate validation performance and monitor overfitting.
9. Tune hyper-parameters, repeat, and select the best validated configuration.
10. Fit the final chosen configuration appropriately and evaluate once on test data.

For tree algorithms, “gradient descent” is not always the update mechanism. A tree is grown by splits or leaf-value optimisation, but the overall training logic—fit, validate, regularise, stop, test—still applies.

### Loss functions

A loss \(L(y,\hat y)\) expresses the cost of a prediction error. The empirical risk minimised during training is often

\[
\hat R(\theta)=\frac1n\sum_{i=1}^{n}L(y_i,h_\theta(x_i)).
\]

**Squared error:** \(L=(y-\hat y)^2\), used in ordinary linear regression. Large errors receive high penalty.

**Absolute error:** \(L=|y-\hat y|\), less sensitive to extreme residuals.

**Binary cross-entropy:** for probability \(p=h_\theta(x)\),

\[
L=-[y\log p+(1-y)\log(1-p)].
\]

**Multiclass cross-entropy** sums negative log probabilities over classes. A hinge or margin loss is common in some SVM and classification settings. The loss should reflect the real cost; a team may use class weights or sample weights.

### Gradient descent

For parameters \(\theta\), update

\[
\theta_{t+1}=\theta_t-\eta\nabla_\theta J(\theta),
\]

where \(\eta\) is the learning rate. The gradient points towards increasing loss, so the negative gradient descends. Batch gradient descent uses all training examples per update; stochastic gradient descent uses one or a small batch and is common for large data. Mini-batches balance noise and computational efficiency.

Learning rate, momentum, weight decay, normalisation, and optimiser choice affect convergence. A learning rate that is too large can diverge; one that is too small can be slow or settle in a poor region. Random shuffling, seeds, and batch composition can also affect results.

### Regression training example

For linear regression,

\[
h_\theta(x)=\theta^\top x,\qquad
J(\theta)=\frac{1}{2n}\|X\theta-y\|_2^2.
\]

The normal-equation solution \(\hat\theta=(X^\top X)^{-1}X^\top y\) is possible when \(X\) has full rank and the matrix is well-conditioned. In practice, gradient descent or regularised optimisation is used for large or ill-conditioned data. Standardisation can make optimisation easier, but it changes the coefficient scale interpretation.

### Classification training example

For two classes, logistic regression computes

\[
p=\sigma(\theta^\top x),\qquad
\sigma(z)=\frac{1}{1+e^{-z}}.
\]

It minimises binary cross-entropy using gradient descent or a solver such as Newton/L-BFGS. For more than two classes, use multinomial logistic regression, one-vs-rest, or a multiclass loss. A probability output is not the same as a hard prediction; a threshold is needed.

### Regularisation and generalisation

High-dimensional or flexible models can memorise training examples. Ridge regression adds \(\lambda\|w\|_2^2\), and LASSO adds \(\lambda\|w\|_1\) to the objective:

\[
J_{\text{reg}}=J_{\text{data}}+\lambda R(w).
\]

Regularisation controls capacity. Tree depth and minimum leaf size act as structural controls. Early stopping uses validation performance. Dropout, data augmentation, and noise injection are common in neural models. The strength of regularisation is selected using validation, not by looking at the test score.

### Training, validation, and test sets

The training set fits parameters. The validation set selects hyper-parameters, features, transformations, and thresholds. The test set estimates final performance. For small data, \(k\)-fold cross-validation reuses data efficiently, but nested validation may be needed when many models and hyper-parameters are compared. For temporal data, train on the past and validate on the future.

### Convergence and stopping

Track the training loss and validation metric. A model can have a low training loss while validation loss rises, indicating overfitting. Stop at the best validation checkpoint, use a patience-based early-stopping rule, or regularise. “Training completed” does not mean the optimum was found.

### Reproducibility and experiment records

Save the data snapshot, code version, preprocessing parameters, feature schema, random seed, optimiser settings, hyper-parameters, checkpoint, and evaluation protocol. A training run that cannot be reproduced is difficult to audit or roll back.

## Worked examples

### Example 1: one linear-regression update

Assume \(J(w)=\frac12(w-3)^2\), so \(\nabla J=w-3\). With \(w_0=0\) and \(\eta=0.1\),

\[
w_1=0-0.1(0-3)=0.3.
\]

Repeated updates move \(w\) toward 3. In a real model, the gradient is the sum or average of many feature contributions.

### Example 2: logistic probability

For \(z=0\), \(\sigma(0)=0.5\). The model gives equal probability to the two classes before seeing the training data. A threshold of 0.5 is a decision convention, not a guarantee of correct classification.

### Example 3: overfitting curve

Training error falls from 0.20 to 0.02 while validation error falls to 0.15 and then rises to 0.25. The best checkpoint is near the validation minimum. Continuing training may improve the training objective but hurt generalisation.

### Example 4: weighted classification

A fraud dataset has 100 positives and 10,000 negatives. Give positive errors a larger weight or use class-balanced sampling, then select the threshold with a cost-based validation rule. Measuring accuracy alone will reward the useless all-negative classifier.

## Key terms & formulas

- **Training set:** data used to estimate parameters.
- **Validation set:** data used to select settings.
- **Test set:** untouched data for final estimation.
- **Loss function:** \(L(y,\hat y)\) measuring prediction error.
- **Empirical risk:** \(\frac1n\sum_i L(y_i,h_\theta(x_i))\).
- **Gradient descent:** \(\theta\leftarrow\theta-\eta\nabla J\).
- **Learning rate:** step size \(\eta\).
- **Epoch:** one pass through the training data.
- **Batch:** subset used for one update.
- **Regularisation:** penalty or constraint on model complexity.
- **Ridge penalty:** \(\lambda\|w\|_2^2\).
- **LASSO penalty:** \(\lambda\|w\|_1\).
- **Early stopping:** halt when validation performance no longer improves.
- **Convergence:** parameters reach a stable region under the optimisation rule.
- **Hyper-parameter:** setting not directly estimated from ordinary target examples.

## Common mistakes

1. **Fitting and evaluating on the same rows.** The score is training error, not generalisation.
2. **Selecting the threshold after seeing the test set.** The final estimate is contaminated.
3. **Using one learning rate for every problem.** Scale and conditioning matter.
4. **Assuming low training loss means success.** Validate and inspect learning curves.
5. **Skipping preprocessing inside folds.** Leakage or inconsistent deployment can result.
6. **Using class weights without checking calibration and costs.** A weighted model may improve recall while producing poor probabilities.
7. **Recording only the final checkpoint.** Keep the best validated model and its configuration.

## Exam prep

### Likely 2-mark questions

- **What is training a supervised model?** Estimating parameters from labelled data using an objective and validation strategy.
- **State the gradient descent update.** \(\theta_{t+1}=\theta_t-\eta\nabla J(\theta)\).
- **What is an epoch?** One complete pass through the training data.
- **What does regularisation do?** Penalises or controls complexity to reduce overfitting.

### Long-answer prompts

- **Explain the supervised training workflow.** Cover splitting, preprocessing, loss, optimiser, validation, regularisation, and testing.
- **Derive the linear-regression objective and one gradient update.** Define \(X,y,\theta\), compute the loss, and interpret the update.
- **Compare batch, stochastic, and mini-batch gradient descent.** Discuss computation, noise, convergence, and large data.
- **How do you decide when to stop training?** Use training/validation curves, early stopping, regularisation, and a final test set.
