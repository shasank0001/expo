---
subject: dwdm
unit: 4
topic: model-evaluation-and-selection
syllabus_ref: CSM3101 Unit-IV
status: draft
---
# Classification Model Evaluation and Selection

## Overview

A classifier that performs well on its training data may still fail on new cases. Evaluation estimates how well a learned model generalizes, compares candidate models fairly, and selects an operating point for a real decision. This is one of the most important Unit-IV topics: accuracy alone can hide serious failures, especially with imbalanced classes or unequal error costs. The notes below cover data splitting, confusion matrices, classification measures, threshold and ranking measures, validation, uncertainty, and model selection.

## Explanation

### 1. Evaluation data and leakage

A model is fit on training data, tuned on validation data, and assessed on a final test set. The test set must not influence feature selection, hyperparameter tuning, class weighting, or threshold choice. If records from one customer, patient, or time period appear in both training and testing, the estimate may be optimistic. Split by the independent unit when appropriate.

**Cross-validation** partitions training data into \(k\) folds. Train on \(k-1\) and validate on the remaining fold, repeating \(k\) times:

\[
\text{CV error}=\frac1k\sum_{i=1}^{k}e_i.
\]

For stratified classification, preserve class proportions in each fold. Time-dependent data often needs forward-chaining validation rather than random folds.

### 2. Confusion matrix

For a binary problem, let positive mean the class of interest:

- **TP:** actual positive predicted positive;
- **TN:** actual negative predicted negative;
- **FP:** actual negative predicted positive;
- **FN:** actual positive predicted negative.

| Actual \ Predicted | Positive | Negative |
|---|---:|---:|
| Positive | TP | FN |
| Negative | FP | TN |

For \(K\) classes, a \(K\times K\) matrix records all class confusions. A macro-average gives each class equal weight; a micro-average weights by class support.

### 3. Accuracy and balanced accuracy

\[
\operatorname{Accuracy}=\frac{TP+TN}{TP+TN+FP+FN}.
\]

Accuracy is useful when classes and error costs are reasonably balanced. **Balanced accuracy** averages recall across classes:

\[
\operatorname{BalAcc}=\frac1K\sum_{c=1}^{K}\operatorname{Recall}_c.
\]

It gives a rare class equal weight with a majority class. Accuracy should be reported alongside class-wise measures and the number of examples.

### 4. Precision, recall, specificity, and F1

\[
\operatorname{Precision}=\frac{TP}{TP+FP},
\]
\[
\operatorname{Recall}=\frac{TP}{TP+FN},
\]
\[
\operatorname{Specificity}=\frac{TN}{TN+FP}.
\]

Precision answers “of predicted positives, how many are correct?” Recall answers “of actual positives, how many were found?” F1 is their harmonic mean:

\[
F_1=\frac{2PR}{P+R}=\frac{2TP}{2TP+FP+FN}.
\]

F1 is useful for an imbalanced positive class, but it still ignores true negatives and can be inappropriate when false positives have a very different cost.

### 5. Cost-sensitive measures

If false positives cost \(C_{FP}\) and false negatives cost \(C_{FN}\), expected misclassification cost is

\[
C=C_{FP}FP+C_{FN}FN.
\]

A model can reduce expected cost even with lower accuracy. Bayes decision theory chooses the class with minimum expected cost rather than maximum probability. Cost-sensitive learning can alter class weights, thresholds, or the loss function during training.

### 6. Ranking measures: ROC and PR

A probabilistic model can rank cases by score. Vary the threshold to obtain a trade-off between true-positive rate and false-positive rate:

\[
TPR=\operatorname{Recall},\qquad FPR=1-\operatorname{Specificity}.
\]

The **ROC curve** plots TPR against FPR; ROC-AUC summarizes ranking performance across thresholds. When positives are rare, false positives can remain low even while the positive precision is poor. A **precision-recall curve** plots precision against recall and is often more informative for rare-event detection. Select a threshold using validation data and the intended costs.

### 7. Calibration

A calibrated model has predicted probability 0.80 for a group that experiences the event about 80% of the time. Discrimination asks whether higher-risk cases receive higher scores; calibration asks whether the numeric probabilities are meaningful. A model can rank well but be badly calibrated, or vice versa. Use reliability plots or a calibration measure when probabilities drive decisions.

### 8. Overfitting, underfitting, and bias–variance

Underfitting means the model cannot represent the training pattern. Overfitting means it memorizes training noise. Across model complexity or training-set size, there is a trade-off between bias (systematic error from too-simple assumptions) and variance (sensitivity to the particular sample). Validation performance—not training performance—selects complexity.

### 9. Comparing models

Use the same splits, preprocessing, features, and evaluation metric for candidates. Prefer confidence intervals or paired tests over a single point estimate. For repeated cross-validation, compare fold results carefully because folds are not independent. A final test comparison should be pre-specified and include the selected model only.

### 10. Practical selection checklist

1. Define the error costs and target population.
2. Choose a split that respects time/group structure.
3. Fit a simple baseline.
4. Compare candidate models with the same validation protocol.
5. Inspect confusion matrices and calibration.
6. Select the operating threshold using validation, not test data.
7. Refit on training plus validation if appropriate, then evaluate once on test.
8. Record uncertainty, subgroup performance, and limitations.

## Worked examples

### Example 1: Complete binary metrics

From a test set:

- TP = 40
- FP = 5
- FN = 10
- TN = 945

Total = 1,000.

\[
\operatorname{Accuracy}=(40+945)/1000=0.985.
\]

\[
\operatorname{Precision}=40/(40+5)=0.8889,
\]
\[
\operatorname{Recall}=40/(40+10)=0.80,
\]
\[
\operatorname{Specificity}=945/(945+5)=0.9947,
\]
\[
F_1=2(40)/(2(40)+5+10)=80/95=0.8421.
\]

The classifier misses 20% of positives despite very high accuracy. If a missed positive costs \$100 and a false alarm costs \$1, the cost is \(10(100)+5(1)=\$1{,}005\); if false alarms cost \$500, it is \(10(100)+5(500)=\$3{,}500\).

### Example 2: Imbalanced accuracy

A dataset has 980 safe and 20 fraud cases. Predicting every case safe gives accuracy \(98\%\), but fraud recall is zero. Balanced accuracy is

\[
(0+\text{safe recall})/2 \approx (0+1)/2=0.50.
\]

This exposes the useless rare-class prediction.

### Example 3: Threshold trade-off

At threshold 0.50: TP=20, FP=100, FN=5, TN=875.
At threshold 0.80: TP=15, FP=20, FN=10, TN=955.

Lower threshold:

\[
P=20/120=16.7\%,\quad R=20/25=80\%.
\]

Higher threshold:

\[
P=15/35=42.9\%,\quad R=15/25=60\%.
\]

A fraud team may prefer the first for screening, while an expensive investigation workflow may prefer the second. There is no universally correct threshold.

### Example 4: Cross-validation

Model A has fold accuracies 0.82, 0.85, 0.80, 0.84, and 0.79, so its mean is \(0.82\). Model B has a slightly higher mean, 0.83, but fold values ranging from 0.60 to 0.96. If both models matter in the same deployment setting, Model A's more stable performance may be safer. Report the distribution and uncertainty, not only the best mean.

## Key terms & formulas

- **TP, TN, FP, FN:** confusion-matrix counts.
- **Accuracy:** \((TP+TN)/N\).
- **Precision:** \(TP/(TP+FP)\).
- **Recall/TPR/sensitivity:** \(TP/(TP+FN)\).
- **Specificity/TNR:** \(TN/(TN+FP)\).
- **F1:** harmonic mean of precision and recall.
- **Balanced accuracy:** mean recall across classes.
- **Expected cost:** \(C_{FP}FP+C_{FN}FN\).
- **ROC:** TPR versus FPR across thresholds.
- **PR curve:** precision versus recall across thresholds.
- **Cross-validation:** repeated train/validation partitions.
- **Calibration:** agreement of predicted probabilities with observed frequencies.
- **Generalization:** performance on unseen data.

## Common mistakes

1. **Using accuracy alone:** it hides minority-class errors and unequal costs.
2. **Swapping precision and recall:** their denominators differ.
3. **Choosing a threshold on the test set:** it contaminates final evaluation.
4. **Randomly splitting dependent records:** group or time leakage inflates scores.
5. **Comparing models on different splits:** differences may be caused by the evaluation design.
6. **Treating ROC-AUC as the only metric:** rare positive classes may need PR-AUC and threshold analysis.
7. **Ignoring uncertainty:** a one-point difference on a small test set may not be meaningful.
8. **Selecting on training error:** it rewards overfitting.

## Exam prep

**Likely 2-mark questions**
1. Define precision, recall, and F1. *Hint: conditional fractions using TP, FP, and FN.*
2. Why is accuracy misleading for imbalanced data? *Hint: majority class dominates the average.*
3. What is ROC-AUC? *Hint: ranking performance across decision thresholds.*

**Likely long-answer questions**
1. Derive all binary classification measures from a confusion matrix. *Hint: write counts, formulas, numerical substitution, and interpretation.*
2. Compare threshold selection using ROC and precision–recall curves. *Hint: rare positives, false alarms, costs, and operating point.*
3. Explain cross-validation and model selection without leakage. *Hint: folds, stratification, hyperparameters, untouched test set.*
4. Design an evaluation plan for a medical or fraud classifier. *Hint: class imbalance, costs, calibration, subgroup checks, temporal validation, monitoring.*
