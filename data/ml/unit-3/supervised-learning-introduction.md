---
subject: ml
unit: 3
topic: supervised-learning-introduction
syllabus_ref: CSM3201 Unit-III
status: draft
---
# Supervised Learning: An Introduction

## Overview

Supervised learning is the branch of machine learning in which a learner receives examples consisting of inputs and their correct outputs. From these labelled examples it estimates a function that can predict the output for a new input. The core idea is simple, but the design decisions are important: the target must be meaningful, features must exist at prediction time, and evaluation must represent deployment.

In this unit, supervised learning is divided into **classification**, which predicts a category, and **regression**, which predicts a number. Both use the same general workflow, but their targets, losses, predictions, and metrics differ.

## Explanation

### Formal learning problem

Let the input space be \(\mathcal X\) and target space be \(\mathcal Y\). Given a training set

\[
D=\{(x_1,y_1),\ldots,(x_n,y_n)\},
\]

a learning algorithm selects a hypothesis \(h\in\mathcal H\) that approximates the unknown target function \(f:\mathcal X\to\mathcal Y\). The empirical error is

\[
\hat R(h)=\frac1n\sum_{i=1}^{n}L(h(x_i),y_i),
\]

and the algorithm searches for parameters or structure that reduce this error while controlling complexity. The population goal is to minimise expected error on unseen data from the deployment distribution.

### Classification and regression

**Classification** has discrete targets. A binary classifier estimates

\[
P(Y=y\mid x)
\]

for each class, or a decision function \(h(x)\in\{0,1\}\). Examples include fraud detection, disease screening, and image labels.

**Regression** has a continuous target, such as a price, demand, age, or error rate. It estimates \(Y\) or \(E[Y\mid x]\). Regression can support decisions, but a point prediction alone may hide uncertainty.

A task can move between the two. Predicting whether a machine will fail is classification; predicting the remaining life in hours is regression. Predicting a customer's spending category is classification; predicting spending in rupees is regression.

### Why labels enable learning

In the loss \(L(\hat y,y)\), the known \(y\) provides direct feedback. An optimiser can compare its prediction with the target and adjust parameters. For a linear model this may be a squared-error gradient; for a tree it may be a split that improves impurity reduction; for a neural network it is a backpropagated derivative.

The feedback is only as good as the label. A label can be noisy, subjective, biased, or defined after the prediction time. A strong model cannot learn a target that the data do not contain.

### Training and inference

Training uses labelled data to estimate parameters, select features, and choose settings. Inference applies the fixed model to an unlabelled instance. The deployment contract should state the input schema, allowable missing values, output type, threshold or interval, latency, and fallback behaviour.

### The supervised workflow

1. Define the decision and target.
2. Gather representative labelled data.
3. Split according to time, groups, and deployment.
4. Explore and preprocess without leakage.
5. Establish a simple baseline.
6. Train candidate models and tune on validation data.
7. Evaluate with suitable metrics, uncertainty, and error analysis.
8. Improve the data, features, objective, or model.
9. Deploy with monitoring, documentation, and human oversight where appropriate.

### Generalisation and inductive bias

A hypothesis class restricts possible solutions. Linear models favour linear boundaries, trees favour axis-aligned partitions, nearest neighbours favour local similarity, and neural networks favour flexible distributed representations. The right bias depends on the data-generating process. A model with enough capacity can fit training examples but still fail on unseen ones.

### Statistical and operational issues

Supervised models need enough examples of the target relationship. Rare classes, changed populations, label noise, and unequal costs complicate evaluation. A model should be assessed for calibration, robustness, fairness, latency, and stability, not just one aggregate score.

## Worked examples

### Example 1: predicting loan default

Inputs are income, debt ratio, and prior payment history; the target is default within 12 months. The label is known historically. A logistic regression estimates a probability. The bank chooses a threshold based on the cost of a missed default versus the cost of an unnecessary restriction. A future borrower has no known default label, so the model is performing inference.

### Example 2: predicting house price

Area, location, rooms, and age are inputs; sale price is a continuous target. A linear model estimates a conditional mean. Errors are measured with MAE/RMSE and residuals. The model can interpolate between observed houses but extrapolation beyond the training range can be unreliable.

### Example 3: a noisy target

Annotators label a sentiment as positive, negative, or uncertain. Training only on positive/negative rows discards useful ambiguity. A model trained on soft or three-class labels may be more honest than one forced to a binary answer.

### Example 4: leakage

A churn model uses “customer called cancellation support” even though the call occurs after the prediction date. The feature predicts the target in the training set but is unavailable when the decision is made. Proper time-based preprocessing and feature availability checks prevent this.

## Key terms & formulas

- **Supervised learning:** learning from input–target pairs.
- **Input/feature space:** \(\mathcal X\).
- **Target space:** \(\mathcal Y\).
- **Training set:** \(D=\{(x_i,y_i)\}\).
- **Hypothesis space:** \(\mathcal H\), the set of representable functions.
- **Classification:** prediction of a discrete class.
- **Regression:** prediction of a continuous target.
- **Loss:** \(L(y,\hat y)\), the cost of an error.
- **Empirical risk:** average loss on training examples.
- **Expected generalisation risk:** expected loss on unseen deployment examples.
- **Inductive bias:** assumptions that favour particular solutions.
- **Parameter:** value estimated from training data.
- **Hyper-parameter:** setting selected through validation.
- **Inference:** prediction on new data with a learned model.
- **Target leakage:** future or target-revealing information used as input.

## Common mistakes

1. **Confusing supervised learning with a particular algorithm.** Linear models, trees, SVMs, and networks can all be supervised.
2. **Defining a target after seeing the desired result.** The target must be available at training and relevant at prediction time.
3. **Assuming labels are objective.** They can be noisy, biased, or subjective.
4. **Using random splits for time or grouped records.** This produces leakage and optimistic results.
5. **Reporting training error.** Generalisation must be measured on unseen data.
6. **Ignoring the application cost.** A technically good score can be operationally or ethically poor.
7. **Forgetting inference requirements.** Missing values, schema changes, and latency matter after training.

## Exam prep

### Likely 2-mark questions

- **Define supervised learning.** Learning a mapping from inputs to known targets using labelled examples.
- **What is the difference between classification and regression?** Discrete class versus continuous target.
- **Define a loss function.** A function measuring the cost of a prediction error.
- **What is inference?** Applying a learned model to a new unlabelled example.

### Long-answer prompts

- **Explain the supervised-learning problem formally.** Define \(D,\mathcal X,\mathcal Y,\mathcal H\), loss, and generalisation.
- **Describe a supervised-learning workflow.** Include target definition, labels, splitting, preprocessing, model selection, evaluation, and deployment.
- **Compare classification and regression with examples.** Discuss targets, outputs, losses, metrics, and uncertainty.
- **Why is label quality important?** Use examples of noise, weak labels, bias, delay, and leakage.
