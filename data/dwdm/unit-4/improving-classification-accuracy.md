---
subject: dwdm
unit: 4
topic: improving-classification-accuracy
syllabus_ref: CSM3101 Unit-IV
status: draft
---
# Techniques to Improve Classification Accuracy

## Overview

Classification accuracy can be improved by changing the data, the learning algorithm, the decision threshold, or the model structure. The correct method depends on the source of error: noisy features, overfitting, class imbalance, bias, or high variance. This topic covers practical techniques from data preprocessing and resampling through ensembles, cost-sensitive learning, and validation. The aim is not to maximize one number blindly but to improve reliable performance on the target population.

## Explanation

### 1. Establish a baseline

Before a complex method, fit a simple baseline such as majority class, a small decision tree, logistic regression, or naive Bayes. Record accuracy, class-wise recall, cost, calibration, and training time. If a sophisticated method only improves training accuracy or changes a threshold, the source of the claimed improvement is unclear.

### 2. Feature engineering and selection

Feature engineering creates informative variables from domain knowledge: ratios, interactions, time windows, recency, and text features. Feature selection removes irrelevant or redundant variables. For \(K\) features, exhaustive search costs roughly \(2^K\) subsets; greedy forward selection adds one feature at a time, while backward selection removes one. Regularized logistic regression or tree importance can screen features, but importance is not always causal or stable.

Use feature selection only inside the training fold. Selecting variables using the full dataset leaks information. High-cardinality identifiers can be especially dangerous because a model memorizes their values.

### 3. Data cleaning and missing values

Correct impossible values, standardize units, remove duplicates, and investigate missingness. A missing value may be random, related to the target, or indicate a process failure. Imputation can use training-fold medians, model-based imputation, or a missingness indicator. For categorical data, an explicit “missing” category may be appropriate.

### 4. Class imbalance

If the rare class is important, several approaches help:

- **Random oversampling:** duplicate rare-class examples.
- **Random undersampling:** remove majority-class examples.
- **SMOTE:** synthesize rare-class points between close neighbors; do not use blindly on time or categorical data.
- **Class weighting:** give the rare class greater loss weight.
- **Threshold adjustment:** trade false positives for false negatives.
- **Balanced batch sampling:** sample rare cases more often during training.

Oversampling does not create genuinely new information and can overfit. Undersampling can discard useful information. Evaluate on the original, untouched class distribution, not on an artificially balanced test set.

### 5. Cost-sensitive learning

Define the cost of each error. Reweight the loss, use cost-sensitive decision thresholds, or train on examples with different weights. If a false negative is 20 times more costly, a positive class with moderate precision may be preferable. The chosen threshold should be validated, not guessed from training data.

### 6. Ensembles: bagging and random forests

**Bagging** trains many models on bootstrap samples and averages/majority-votes their predictions. It reduces variance and usually makes models more stable.

**Random forests** add a second randomization: at each node, only a random subset of features is considered. The forest averages many deep trees. Out-of-bag (OOB) samples provide an internal validation estimate when the training protocol is respected. OOB is not a substitute for an external test set.

Ensembles can lose interpretability, and majority voting can be poor for severe class imbalance. Measure class-specific performance and memory/runtime cost.

### 7. Boosting

**Boosting** adds models sequentially so later models focus on errors of earlier ones. A weighted combination is updated after each weak learner. It can reduce bias and achieve strong predictive performance, but it is sensitive to noisy labels and can overfit. Learning-rate control, shallow trees, early stopping, and validation are important.

### 8. Stacking and model combination

Stacking trains a meta-model on out-of-fold predictions from several base learners. It can combine different strengths, but its meta-features must not be generated from the same data used to train the base learner in a way that leaks labels. Simple voting or weighted averaging may be enough and easier to explain.

### 9. Regularization and model capacity

For linear and neural models, L1 can produce sparse coefficients; L2 shrinks coefficients smoothly. Decision-tree depth, minimum leaf size, neural hidden width, dropout, early stopping, and weight decay limit capacity. Hyperparameters should be selected through cross-validation or a validation set. More parameters are not automatically more accurate.

### 10. Calibration and thresholding

If the model ranks cases well but probabilities are not reliable, apply Platt scaling, isotonic regression, or another calibration method on validation data. Choose the operating threshold using the cost matrix or F-beta score. A threshold that improves recall may reduce precision, so report both.

### 11. Monitoring after deployment

Model accuracy can change because behavior, population, sensors, or policy changes. Track input distributions, missingness, score distributions, delayed labels, class metrics, subgroup performance, and drift. Retraining requires the same validation and governance process as initial development.

## Worked examples

### Example 1: Majority baseline and balanced accuracy

A test set has 950 negative and 50 positive examples. Always-negative accuracy is \(950/1000=95\%\), but positive recall is 0. A classifier has \(P=0.80,R=0.80\), so its accuracy might be lower than 95% while catching many more positives. The choice depends on whether missed positives are harmful and what false-positive investigations cost.

### Example 2: Class weighting

Let false-negative cost be \$100 and false-positive cost be \$1. A model has FP=5 and FN=10, giving cost \(5+1000=\$1{,}005\). Raising the positive threshold could reduce FN but increase FP. If a new threshold gives FP=15 and FN=4, cost is \(15+400=\$415\), so it is preferable even if accuracy falls. The threshold is selected on validation cost.

### Example 3: Bagging intuition

Five voters predict a class: four say `yes`, one says `no`; majority voting returns `yes`. If the same model is trained on different bootstrap samples, errors may be less correlated than the individual models, so the ensemble is often steadier. If all models make the same systematic error, voting cannot remove it.

### Example 4: Leakage during feature selection

Suppose 100 predictors are screened using the full dataset and only the best one is passed to five-fold cross-validation. The folds are no longer independent of feature selection. Feature screening must occur inside each training fold. This can make cross-validation accuracy optimistic.

## Key terms & formulas

- **Baseline:** simple reference model.
- **Feature selection:** choose a subset of predictors.
- **Over/undersampling:** change training class frequencies.
- **SMOTE:** interpolate synthetic minority examples.
- **Class weighting:** assign different loss weights to classes.
- **Bagging:** bootstrap ensemble for variance reduction.
- **Random forest:** bagged trees with feature randomization.
- **Boosting:** sequential learners emphasizing prior errors.
- **Out-of-bag estimate:** prediction error on examples omitted from a bootstrap training sample.
- **Stacking:** meta-model over out-of-fold base predictions.
- **L1/L2 regularization:** sparsity/shrinkage constraints.
- **Calibration:** agreement between scores and observed probabilities.
- **F-beta:** weighted precision–recall harmonic mean.

## Common mistakes

1. **Changing the test distribution for resampling:** evaluate on real deployment prevalence.
2. **Selecting features on all data before cross-validation:** leakage.
3. **Using SMOTE on categorical or ordered time data blindly:** interpolation may be meaningless.
4. **Assuming bagging fixes bias:** it mainly reduces variance.
5. **Ignoring early stopping in boosting:** noisy data can cause overfit.
6. **Calling OOB performance an external validation:** it is still based on the same training sample.
7. **Improving accuracy while destroying the rare-class recall:** inspect the full metric set.

## Exam prep

**Likely 2-mark questions**
1. Differentiate bagging and boosting. *Hint: parallel bootstrap averaging versus sequential error-focused learners.*
2. What is SMOTE? *Hint: synthetic interpolation between neighboring minority examples.*
3. Why perform feature selection inside each training fold? *Hint: prevent information leakage.*

**Likely long-answer questions**
1. Describe methods for handling imbalanced classification and their limitations. *Hint: sampling, weights, thresholds, costs, original test distribution.*
2. Explain random forest and boosting as accuracy-improvement techniques. *Hint: randomization, OOB, sequential weighting, noise, and validation.*
3. Design an improvement plan after diagnosing a classifier's errors. *Hint: baseline, data audit, class analysis, features, model, threshold, validation.*
