---
subject: sc
unit: 3
topic: ann-design-issues
syllabus_ref: CSM3202 Unit-III
status: draft
---
# Design Issues of Artificial Neural Networks

## Overview

Designing an ANN means choosing its data representation, architecture, activation functions, loss, training procedure, regularization, and evaluation strategy. The task is not complete when training loss becomes small. A useful network must generalize, operate reliably within its input range, and meet practical constraints.

The central difficulty is that many network configurations can fit the training data. Design therefore requires data understanding, controlled experiments, and validation rather than a single universal rule.

## Explanation

### 1. Define the problem and output

Begin with a precise task:

- classification, regression, ranking, clustering, or control;
- target variables and their physical meaning;
- required prediction horizon;
- latency, memory, and hardware limits;
- safety and explanation requirements.

The output type determines the final activation and loss. A regression target may need a linear output and squared error. A probability output may use sigmoid plus binary cross-entropy. A decision may need a threshold chosen on validation data.

### 2. Data collection

The data should represent the intended operating conditions. Collect:

- normal cases;
- boundary and rare cases;
- noisy and missing inputs;
- changes in season, device, location, or population;
- labels or targets measured with reasonable reliability.

Too few examples can cause overfitting. A biased data set can make a high test score misleading. Data collection may cost more than network training, so it should not be skipped in favor of a complicated architecture.

### 3. Data preprocessing

Neural networks are sensitive to feature scale. Use standardization, min–max scaling, or domain-specific transforms. Fit the transformation on training data and apply it to validation and test data.

Handle categorical variables with an appropriate encoding, not arbitrary integer order unless that order has meaning. Missing values require a declared strategy. The preprocessing pipeline must be saved with the model.

### 4. Data splitting

Use separate training, validation, and test sets. For small data, use k-fold cross-validation. If observations are time ordered, use chronological splits and do not train on future observations to predict the past.

Stratification can preserve class balance. Grouped data—for example, several records from the same patient—must be split by group to avoid leakage.

### 5. Number of layers and units

More layers and units increase capacity but also increase:

- number of parameters;
- data requirements;
- memory and computation;
- optimization difficulty;
- overfitting risk.

A useful baseline is a small model:

- logistic regression or linear regression;
- a shallow tree or kernel method;
- a small FFNN.

Increase complexity only when validation evidence supports it. A network with one hidden layer is often a strong baseline for many tabular problems.

### 6. Activation functions

Use a differentiable activation inside hidden layers:

- sigmoid for smooth bounded outputs;
- tanh for centered bounded outputs;
- ReLU or variants for many deep architectures.

Choose the output activation from the target type. A linear hidden layer adds no representational power, so hidden nonlinearities must be present.

ReLU can create dead units. Leaky ReLU, a carefully chosen initialization, and monitoring of activation statistics can help.

### 7. Initialization

The initial weights should break symmetry and match the activation scale. Common choices include Xavier/Glorot and He/Kaiming initialization. All-zero weights are not suitable for a multilayer network because hidden units receive identical signals.

A different random seed can produce a different local solution. Compare seeds when results are unstable, especially with small data.

### 8. Optimization algorithm

Gradient descent may use:

- vanilla batch gradient descent;
- stochastic gradient descent;
- mini-batch SGD with momentum;
- adaptive methods such as Adam or RMSProp.

Each optimizer has hyperparameters and may behave differently. A learning-rate search and a short comparison are more reliable than assuming one optimizer is always best.

### 9. Learning rate and schedule

The learning rate controls the size of parameter changes. A value that is too high can cause divergence; a value that is too low can make training unnecessarily slow. Use:

- validation-based reduction;
- warm-up for some deep networks;
- a learning-rate range test;
- separate rates for pretrained and new layers.

Record the actual schedule; a nominal rate without the schedule can be misleading.

### 10. Loss function and class imbalance

A rare class may be ignored if the loss is dominated by common examples. Remedies include:

- class-weighted loss;
- resampling;
- balanced batches;
- precision-recall and recall-oriented metrics;
- threshold selection.

Accuracy can be misleading when one class is much more common. Report confusion matrices and per-class metrics.

### 11. Regularization

A regularized objective is

\[
J=J_{\text{loss}}+\lambda R(\theta).
\]

L2 penalty:

\[
R_2(\theta)=\frac12\sum_l\|W^{(l)}\|_F^2.
\]

L1 penalty:

\[
R_1(\theta)=\sum_l|W^{(l)}_1.
\]

L2 encourages smaller weights smoothly; L1 can produce sparse weights. Other methods include dropout, data augmentation, early stopping, noise injection, and restricting architecture.

The regularization strength must be validated. Too much can underfit.

### 12. Early stopping

Use a validation loss to monitor progress:

```text
for epoch in range(max_epochs):
    train one epoch
    if validation_loss improves:
        save checkpoint
    else:
        patience_counter += 1
        if patience_counter >= patience:
            stop
```

Restore the best checkpoint, not necessarily the last epoch. A validation set is needed for this decision.

### 13. Overfitting and underfitting

**Overfitting:** low training loss, higher validation loss, poor test behavior. Remedies include more data, augmentation, regularization, smaller capacity, and early stopping.

**Underfitting:** high training and validation loss. Remedies include more capacity, better features, a suitable activation, longer training, and a less restrictive objective.

A low training loss is not a sufficient condition for a good model.

### 14. Vanishing and exploding gradients

Deep networks may have very small or large gradients. Monitor gradient norms and activation distributions. Use suitable initialization, ReLU-family activations, normalization, residual connections, gradient clipping, and learning-rate control.

If a network cannot be trained, inspect preprocessing and data labels before adding more layers.

### 15. Initialization and local minima

A nonconvex objective can have many stationary points. Backpropagation does not guarantee a global optimum. Good initialization, multiple restarts, regularization, and a validation comparison are practical strategies.

A very small network may have a stronger convex or simpler objective in its restricted parameter class, sometimes making optimization easier.

### 16. Explainability and interpretability

If a model affects safety, credit, health, or hiring, consider whether a black-box prediction is acceptable. Possible techniques include:

- feature importance;
- perturbation tests;
- saliency maps;
- partial-dependence or accumulated-local-effect analysis;
- distillation into an interpretable model;
- case-based explanations.

An explanation should be tested for stability and correctness. A visually attractive heat map is not automatically a causal explanation.

### 17. Robustness

A deployed model may encounter inputs outside the training range. Test:

- small measurement noise;
- missing values;
- extreme values;
- adversarial or out-of-distribution inputs;
- changes in the environment.

Robustness can be improved with augmentation, noise injection, regularization, input constraints, and monitoring. Robustness to one perturbation does not guarantee safety in all circumstances.

### 18. Computational efficiency

Estimate:

- parameter count;
- memory for activations and gradients;
- training time;
- inference latency;
- batch size and hardware;
- energy and deployment cost.

A smaller model may be preferable if its accuracy is close and it runs on available hardware. Quantization or pruning can reduce deployment cost, but must be validated after compression.

### 19. Reproducibility

Record:

- random seeds;
- data version and split;
- preprocessing parameters;
- code and library versions;
- architecture and hyperparameters;
- optimizer state and stopping epoch;
- test predictions and uncertainty.

A model that cannot be reproduced is difficult to audit or improve.

### 20. Design workflow

1. Define the task and success metric.
2. Inspect and clean the data.
3. Create leakage-safe splits.
4. Establish simple baselines.
5. Build a small FFNN baseline.
6. Diagnose errors by subgroup and data region.
7. Tune one factor at a time where practical.
8. Add capacity or regularization based on evidence.
9. Test the final model once on untouched test data.
10. Deploy with monitoring and a rollback plan.

## Worked examples

### Example 1: Diagnose overfitting

A network has training MSE 0.002 and validation MSE 0.18. The gap is large. Adding more hidden units is unlikely to help. Try stronger regularization, early stopping, augmentation, more data, or a smaller network. If training and validation MSE are both 0.40, the problem may instead be underfitting or inadequate features.

### Example 2: Scaling prevents numerical imbalance

Suppose age ranges from 18 to 80 while income is measured in hundreds of thousands. Standardize both using training statistics. A large income number can dominate a gradient even if the age information is important.

### Example 3: Group leakage

If a dataset has multiple rows for each patient, a random row split can put the same patient in both training and test data. The resulting score may be artificially high. Split by patient group.

### Example 4: Accuracy is misleading

In a disease test, 1% of cases are positive. A model that always predicts negative has 99% accuracy but detects no disease. Report sensitivity, specificity, precision-recall, and confusion matrix.

### Example 5: Capacity comparison

Model A has 0.8 million parameters and validation accuracy 89%. Model B has 0.08 million parameters and validation accuracy 90%. Model B may be preferable because it is smaller, faster, and at least as accurate.

## Key terms & formulas

- **Generalization:** Performance on unseen data.
- **Overfitting:** Training performance much better than validation/test performance.
- **Underfitting:** Poor performance on both training and validation data.
- **Regularization:** Penalty or technique that limits effective complexity.
- **Early stopping:** Stop training when validation performance no longer improves.
- **Initialization:** Starting values of parameters.
- **Learning-rate schedule:** Planned change of learning rate over time.
- **Hyperparameter:** Setting chosen before training, such as depth or regularization strength.

L2 objective:

\[
J=L+\frac{\lambda}{2}\sum_l\|W^{(l)}\|_F^2.
\]

L1 penalty:

\[
R_1(\theta)=\sum_l\|W^{(l)}\|_1.
\]

Confusion-matrix metrics:

\[
\text{Precision}=\frac{TP}{TP+FP},
\qquad
\text{Recall}=\frac{TP}{TP+FN}.
\]

## Common mistakes

1. **Building a large network before establishing a baseline.** Accuracy alone does not show whether the network is needed.
2. **Scaling validation and test data with their own statistics.** Leakage and inconsistent preprocessing result.
3. **Selecting a model by training accuracy.** Use held-out validation/test results.
4. **Adding layers to solve bad labels or poor features.** Diagnose the data first.
5. **Ignoring subgroup performance.** Overall accuracy can hide poor behavior for rare groups.
6. **Using the test set during every tuning decision.** The final estimate becomes optimistic.
7. **Ignoring latency and memory.** A high-accuracy model may be unusable on target hardware.
8. **Assuming a saliency map explains causality.** It shows model sensitivity, not necessarily real-world cause.
9. **Leaving preprocessing and seeds unrecorded.** Reproduction becomes difficult.
10. **Ignoring distribution shift after deployment.** Monitor real inputs and performance.

## Exam prep

### Likely 2-mark questions

- **Define overfitting and underfitting.**  
  **Hint:** Training-validation gap versus poor performance on both.

- **Name two regularization methods for ANNs.**  
  **Hint:** L1/L2, dropout, early stopping, augmentation, or smaller architecture.

- **Why is feature scaling important?**  
  **Hint:** It improves numerical behavior and prevents large-scale features dominating gradients.

- **What is a leakage-free data split?**  
  **Hint:** Training, validation, and test separation respecting time/groups and preprocessing order.

- **Write the L2 regularization objective.**  
  **Hint:** \(J=L+\lambda\|W\|_F^2/2\).

### Likely long-answer questions

- **Explain the major design issues in an ANN.**  
  **Hint:** Data, preprocessing, architecture, activations, optimization, regularization, evaluation, robustness, and deployment.

- **Design an ANN for a given classification/regression problem.**  
  **Hint:** Task, input/output, architecture, loss, optimization, validation, metrics, and limitations.

- **Compare overfitting and underfitting with remedies.**  
  **Hint:** Learning curves, capacity, data, regularization, and feature quality.

- **Discuss the problems of vanishing/exploding gradients and local minima.**  
  **Hint:** Causes, initialization, activations, normalization, clipping, restarts, and validation.

- **Explain how to make an ANN system production-ready.**  
  **Hint:** Reproducibility, leakage control, monitoring, latency, security, rollback, and robustness.
