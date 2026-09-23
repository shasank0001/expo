---
subject: ml
unit: 3
topic: classification-learning-steps
syllabus_ref: CSM3201 Unit-III
status: draft
---
# Classification Learning Steps

## Overview

Classification learning is a sequence of decisions for turning labelled data into a reliable class predictor. The steps are: define the classes, understand and prepare the data, split it without leakage, establish a baseline, choose and train a model, tune it, evaluate it, analyse errors, and deploy it responsibly.

The order matters. A sophisticated classifier cannot repair an undefined target, inconsistent labels, or a split that leaks future information. Good practice makes each step explicit and repeatable.

## Explanation

### Step 1: Define the classification problem

Write the class definitions precisely. Are the classes mutually exclusive? Is “unknown” a valid outcome? What is the prediction time? What action follows each prediction? For a multi-class problem, decide how to handle rare or ambiguous cases. A clear label guideline reduces annotator disagreement.

### Step 2: Collect and inspect labelled data

Check the number of examples per class, class proportions, source populations, time span, duplicates, missingness, and label quality. Examine whether some groups or situations are absent. A classifier cannot learn a class or subgroup that is not represented in the labels.

### Step 3: Choose features available at prediction time

For each feature, record its source, units, availability time, and reliability. Remove target leakage such as an outcome recorded after the decision. Engineer features only from information available before the target. For images, text, or audio, define the representation and any privacy constraints.

### Step 4: Clean and encode

Validate types and ranges, handle missing values, encode categories, scale numerical values where needed, and create a reproducible preprocessing pipeline. Fit transformations on training folds only. Preserve an indicator when missingness itself is informative.

### Step 5: Split the data

Use a training set for fitting, a validation set for selection, and a test set for final evaluation. Stratify for classification when appropriate. Use temporal splits for future prediction and group splits for repeated records. A repeated subject must not appear in both training and test.

### Step 6: Establish a baseline

A majority-class predictor, a simple rule, or a small decision tree gives a reference. If a complex model does not beat it meaningfully on the relevant metric, reconsider the data, objective, or added complexity.

### Step 7: Choose a classifier

Match the method to the data and requirements. Logistic regression is a strong interpretable baseline for linear boundaries. Trees capture nonlinear interactions. SVMs can be effective with suitable scaling and kernels. kNN is simple but may be slow. Neural networks learn rich representations but need data and compute. Consider class weights, calibration, and interpretability.

### Step 8: Train and tune

Define a loss such as cross-entropy. Optimise model parameters, then tune hyper-parameters on validation data. Use early stopping, regularisation, pruning, or class weighting to control overfitting. Keep preprocessing, feature choices, and threshold selection inside the validation protocol.

### Step 9: Evaluate

Choose metrics from the decision costs. Report a confusion matrix, precision, recall, F1, ROC/PR analysis, calibration, and uncertainty. For multiclass tasks, explain averaging. Check subgroup and error-slice performance. Compare with the baseline and a naive confidence interval or bootstrap where appropriate.

### Step 10: Error analysis and improvement

Inspect false positives, false negatives, mislabelled cases, rare classes, and high-confidence errors. Relate errors to data, features, model assumptions, and policy. Add data, fix labels, adjust features, change the objective, tune the threshold, or use a different model. Re-evaluate on fresh data.

### Step 11: Deployment and monitoring

Package the model, preprocessing, schema, and threshold as one versioned artefact. Define latency, abstention, and fallback behaviour. Monitor input quality, output distribution, delayed accuracy, subgroup outcomes, drift, and service errors. Establish who can approve updates and roll back a change.

## Worked examples

### Example 1: medical diagnosis

Classes are disease present, disease absent, and inconclusive. Labels are adjudicated by clinicians, and the prediction time is admission. Images are split by patient, preprocessing is fitted on training patients, and a baseline predicts the majority class. A model is evaluated with sensitivity, specificity, calibration, and subgroup results; positive predictions route to clinician review.

### Example 2: document classification

Documents are assigned topic labels. The pipeline removes accidental IDs, tokenises text, fits a TF–IDF vocabulary on training documents, and trains a linear classifier. A chronological split tests new topics. The team examines per-topic precision/recall and unknown-category behaviour.

### Example 3: threshold improvement

A model has high recall but too many false positives. On validation data, the team evaluates a cost-sensitive threshold and calibrates probabilities. The test set is touched only after the threshold is fixed. This can improve the business outcome even if the unthresholded ranking is unchanged.

## Key terms & formulas

- **Class label:** target category.
- **Baseline:** simple reference classifier.
- **Stratified split:** split preserving class proportions.
- **Group split:** keeps all records of an entity together.
- **Temporal split:** trains on the past and tests on the future.
- **Cross-entropy:** classification loss using predicted probabilities.
- **Class weight:** multiplier giving selected errors greater influence.
- **Threshold:** decision boundary on a score.
- **False positive:** predicted positive when truly negative.
- **False negative:** predicted negative when truly positive.
- **Calibration:** agreement between scores and observed frequencies.
- **Error slice:** a subgroup or region with distinctive errors.
- **Abstention:** allowing the model to decline when confidence is low.

## Common mistakes

1. **Starting with a model before defining classes.** Ambiguous labels create ambiguous learning.
2. **Randomly splitting repeated patients or documents.** Identical information can leak across partitions.
3. **Using post-decision features.** The model learns a task that cannot be performed live.
4. **Fitting encoders and scalers on all data.** This leaks test information.
5. **Selecting a threshold on test data.** The test score becomes biased.
6. **Reporting accuracy alone.** It can hide rare-class and subgroup failures.
7. **Deploying without an abstention or fallback path.** Confidence and service failures require a safe response.

## Exam prep

### Likely 2-mark questions

- **List four classification learning steps.** Define target, inspect data, preprocess/split, train, tune, evaluate, or deploy.
- **Why use a baseline?** To provide a reference and reveal whether complexity helps.
- **What is stratification?** Preserving class proportions across data partitions.
- **What is abstention?** Declining to make a prediction when confidence is insufficient.

### Long-answer prompts

- **Explain the complete classification-learning workflow.** Include target definition, labels, preprocessing, splitting, training, evaluation, error analysis, and deployment.
- **How do you prevent leakage in a classification project?** Give temporal, target, group, duplicate, and preprocessing examples.
- **Describe how you would choose an evaluation metric.** Connect false positives, false negatives, class imbalance, calibration, and business costs.
- **What would you do after seeing high false-negative rate?** Check labels and subgroup coverage, inspect errors, improve data/features/objective, tune threshold, and revalidate.
