---
subject: ml
unit: 2
topic: evaluating-and-improving-models
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Evaluating and Improving Models

## Overview

A model is evaluated by comparing its predictions with known outcomes on data that were not used to fit or select it, using measures connected to the application. Evaluation is not one number: it includes a metric, protocol, uncertainty, subgroup analysis, error analysis, and operational considerations. A sound evaluation tells us not only how well a model performs, but also when and why it fails.

Improvement follows evaluation. Better data, corrected labels, features, objective, regularisation, or algorithm may help, but each change should be tested under the same honest conditions. Tuning repeatedly on the test set can make a weak model appear strong without improving real performance.

## Explanation

### Classification metrics

For binary labels, the confusion matrix counts:

- **TP:** true positives;
- **TN:** true negatives;
- **FP:** false positives;
- **FN:** false negatives.

Then

\[
\text{Accuracy}=\frac{TP+TN}{TP+TN+FP+FN},
\]

\[
\text{Precision}=\frac{TP}{TP+FP},\qquad
\text{Recall}=\frac{TP}{TP+FN},
\]

\[
F_1=\frac{2PR}{P+R}.
\]

**Specificity** is \(TN/(TN+FP)\), and **sensitivity** is recall. For multiclass tasks, use micro-, macro-, or weighted averaging, but state the choice because each treats classes differently.

ROC-AUC measures ranking across thresholds and can look optimistic for rare positives. Precision–recall AUC focuses on the positive class and is often more informative under severe imbalance. A probability score also needs calibration: among predictions near 0.8, about 80% should have the event in a well-calibrated system, within sampling uncertainty.

### Regression metrics

For continuous targets:

\[
MAE=\frac1n\sum_i|y_i-\hat y_i|,
\qquad
RMSE=\sqrt{\frac1n\sum_i(y_i-\hat y_i)^2},
\]

\[
R^2=1-\frac{\sum_i(y_i-\hat y_i)^2}{\sum_i(y_i-\bar y)^2}.
\]

MAE is interpretable in target units and less dominated by extreme errors. RMSE penalises large misses and is useful when they are especially costly. \(R^2\) is relative to a mean baseline and can be negative for poor models. Inspect residuals by time, subgroup, and prediction range.

### Thresholds and cost curves

A model may output scores rather than hard classes. A threshold converts scores into actions. Choose it on validation data by minimising expected cost or meeting a recall requirement. The threshold depends on prevalence and deployment conditions; it should be revisited after drift.

### Cross-validation and resampling

\(k\)-fold cross-validation partitions data into \(k\) folds, trains on \(k-1\), evaluates on one, and repeats. It uses data efficiently, but folds must respect time, groups, and dependencies. Stratified folds preserve class proportions for classification. Repeated or nested cross-validation estimates variability and selection bias. A single split is easy but unstable, especially for small data.

### Baselines and statistical caution

Compare with a majority-class rule, mean/median regression, a simple linear model, or a domain rule. Report the difference and its uncertainty. A 0.5 percentage-point improvement may not matter; a 10-point subgroup gap may matter even if the overall average is high. Do not claim that the best of many models is superior without accounting for selection variability.

### Error analysis

Create a table of false positives, false negatives, and high-error residuals. Look for patterns by feature, subgroup, time, source, and data quality. Examples include errors concentrated in rare categories, night-time images, a new device, or long documents. Inspect mislabelled examples and investigate whether the target is ambiguous. Qualitative review often reveals a new feature or a better decision rule.

### Improving performance

Common directions are:

- collect more representative data and balance important groups;
- correct labels, define the target more precisely, and reduce leakage;
- engineer or select features based on error patterns;
- tune regularisation, model capacity, learning rate, depth, or threshold;
- calibrate probabilities;
- use ensembles or a different model family;
- add domain constraints or a hybrid rule/model system;
- improve the data pipeline and collect delayed feedback.

Improvement should be evaluated on a fresh validation/test protocol. Watch for a trade-off: recall may improve while precision or calibration declines.

### Deployment evaluation

Offline metrics are not the only criterion. Measure latency, throughput, memory, failure rate, abstention rate, cost, user outcomes, fairness, and robustness to perturbation. Monitor drift and delayed labels after release. Establish alert thresholds and a rollback or fallback plan.

### Evaluation report

A useful report states:

1. task and deployment population;
2. data period and split strategy;
3. preprocessing and leakage controls;
4. baselines and candidate models;
5. metrics with uncertainty and subgroup results;
6. calibration, error examples, and limitations;
7. deployment constraints and monitoring plan.

### A practical evaluation loop

Evaluation is most useful when it is tied to a sequence of decisions rather than performed once. Start with a simple baseline and a defined split. Fit preprocessing and the model on training data, tune only on validation data, and record every meaningful change. If performance is weak, inspect the data and error slices before increasing model capacity. If the score is strong, look for leakage, subgroup failures, calibration problems, and operational costs.

A practical loop is:

1. **Establish the reference:** majority class, mean/median target, or a domain rule.
2. **Measure a core metric:** use task-specific loss and a threshold selected from validation data.
3. **Quantify uncertainty:** report folds, repeated splits, or a bootstrap interval where feasible.
4. **Slice the results:** time, source, class, and relevant subgroups.
5. **Read errors:** distinguish model misspecification from bad labels, missing features, and data drift.
6. **Change one hypothesis at a time:** data correction, feature, objective, regularisation, threshold, or model family.
7. **Re-evaluate on fresh data:** never let repeated test inspection become a substitute for validation.

For a classifier, report the confusion matrix and both class-specific rates. For a regressor, report residual and error distributions rather than only an average. Compare not only the central score but also the cost of false alarms, missed events, large residuals, abstentions, and latency. A model that improves the headline metric while making a critical subgroup unsafe is not an improvement.

### Improving the model without self-deception

A model-improvement experiment should have a written hypothesis and a fixed evaluation protocol. “Try a larger network” is not a hypothesis; “add calendar and promotion features that were missing at the forecast time, then test on a later month” is. If a change helps training loss but not validation, it probably increased overfitting. If it helps one subgroup but harms another, it may have traded rather than improved fairness. If it improves a test score after many attempts, the test set has become a tuning set and a new evaluation data source is needed.

## Worked examples

### Example 1: confusion matrix

A test set has TP=40, TN=50, FP=10, FN=20.

\[
\text{Accuracy}=\frac{90}{120}=0.75,
\quad \text{Precision}=\frac{40}{50}=0.80,
\quad \text{Recall}=\frac{40}{60}=0.667,
\]

\[
F_1=\frac{2(0.8)(0.667)}{0.8+0.667}\approx0.727.
\]

The model catches two-thirds of positives but produces false alarms. The appropriate threshold depends on the relative costs.

### Example 2: regression

If observed prices are 10, 12, 14 and predictions are 9, 13, 12:

\[
MAE=\frac{1+1+2}{3}=1.333,
\]

\[
RMSE=\sqrt{\frac{1+1+4}{3}}=\sqrt 2\approx1.414.
\]

The errors are small, but residual and subgroup analysis is still required.

### Example 3: improvement experiment

A baseline has PR-AUC 0.40; a tree model has 0.46; a text-aware model has 0.45. The team chooses the tree only after checking latency, calibration, subgroup recall, and reproducibility. A higher score alone does not decide the application.

### Example 4: cross-validation by user

For recommendations, rows from one user are kept together. Otherwise the model can memorise the user's preferences in training and appear to understand new items. Grouped folds give a more realistic estimate.

## Key terms & formulas

- **Confusion matrix:** table of TP, TN, FP, and FN.
- **Accuracy:** \((TP+TN)/(TP+TN+FP+FN)\).
- **Precision:** \(TP/(TP+FP)\).
- **Recall/sensitivity:** \(TP/(TP+FN)\).
- **Specificity:** \(TN/(TN+FP)\).
- **F1:** harmonic mean of precision and recall.
- **ROC-AUC:** ranking quality across classification thresholds.
- **PR-AUC:** precision–recall area, useful for rare positives.
- **Calibration:** correspondence between predicted and observed probabilities.
- **MAE:** mean absolute error.
- **RMSE:** root mean squared error.
- **\(R^2\):** proportion of target variance explained relative to a mean baseline.
- **Cross-validation:** repeated train/validation partitions.
- **Residual:** observed minus predicted value.
- **Baseline:** reference performance.
- **Error analysis:** investigation of patterns in incorrect predictions.

## Common mistakes

1. **Reporting only accuracy.** It can hide class imbalance and unequal costs.
2. **Choosing a threshold on test data.** The test score becomes optimistic.
3. **Using random cross-validation for dependent records.** Group or time leakage remains.
4. **Ignoring calibration when probabilities drive decisions.** A good ranking does not guarantee good probabilities.
5. **Treating a small score difference as meaningful.** Report uncertainty and practical effect.
6. **Improving features after repeatedly checking the test set.** This is test-set overfitting.
7. **Forgetting deployment metrics.** Offline accuracy does not guarantee reliable service.

## Exam prep

### Likely 2-mark questions

- **Define precision and recall.** Precision is \(TP/(TP+FP)\); recall is \(TP/(TP+FN)\).
- **When is F1 useful?** When precision and recall both matter and the class distribution makes accuracy insufficient.
- **State MAE and RMSE.** Give their formulas and one difference.
- **What is calibration?** Agreement between predicted probabilities and observed event frequencies.

### Long-answer prompts

- **Explain evaluation of a supervised model.** Cover split, metrics, cross-validation, uncertainty, subgroups, error analysis, and deployment.
- **Compare accuracy, precision, recall, F1, ROC-AUC, and PR-AUC.** Use a class-imbalance example.
- **How can a model's performance be improved after error analysis?** Connect errors to data, features, objective, model, and evaluation.
- **Design an evaluation plan for a medical classifier.** Include temporal validation, sensitivity, specificity, calibration, subgroup analysis, and human review.
