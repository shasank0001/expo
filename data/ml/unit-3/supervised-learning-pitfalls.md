---
subject: ml
unit: 3
topic: supervised-learning-pitfalls
syllabus_ref: CSM3201 Unit-III
status: draft
---
# Supervised Learning Pitfalls

## Overview

Supervised learning is easy to start and easy to misuse. A model can produce a high score while learning the wrong target, leaking future information, ignoring a minority group, or failing to generalise beyond a convenient test set. Pitfalls arise from data, problem framing, model choice, evaluation, and deployment.

Recognising these failures is an examinable skill. A careful answer should identify the issue, explain why it invalidates the claim, propose a prevention, and describe how to verify the correction.

## Explanation

### Target and label pitfalls

- **Wrong target:** the label is a proxy, consequence, or consequence measured too late. “Clicked” is not automatically satisfaction.
- **Noisy labels:** annotators disagree, records are mis-keyed, or the class boundary is vague.
- **Inconsistent definitions:** different sources use the same label for different concepts.
- **Target leakage:** a feature reveals the answer or is recorded after prediction time.
- **Selective labels:** only cases that received an outcome are included, creating collider or selection bias.
- **Unstable target:** the policy or process changes, so the old labels no longer represent the current relationship.

Prevention starts with a written target definition, provenance, annotation guidelines, temporal availability checks, and label audits.

### Data leakage

Leakage can occur through:

- target or post-outcome fields;
- future timestamps in a random split;
- duplicate or near-duplicate records across partitions;
- global scaling, imputation, vocabulary, or feature selection;
- group information shared by rows in train and test;
- using the outcome to define a feature or select examples.

Leakage makes offline performance optimistic. Prevention uses chronological/group-aware splits, pipelines fitted inside training folds, feature-availability audits, and realistic deployment tests.

### Overfitting and model selection

Selecting the best of many models and hyper-parameters on the same test set creates selection bias. Small validation sets produce noisy choices. A complex model can memorise idiosyncrasies. Use nested cross-validation or a genuinely untouched test set, regularise, compare a baseline, report uncertainty, and avoid chasing tiny improvements.

### Class imbalance and threshold errors

Accuracy can be dominated by the majority class. A model may ignore rare positives. Resampling can distort priors; class weights can produce poorly calibrated probabilities. Choose metrics and thresholds from costs, check precision-recall behaviour, and inspect minority examples. A high score for the majority group is not an acceptable solution if the minority group is the purpose.

### Distribution shift and extrapolation

Training data may come from a different time, location, device, or population. A model can fail when the target relationship changes (concept drift) or when input prevalence changes. Random cross-validation can hide this problem. Use time-aware validation, external test sites, drift monitoring, and a fallback.

### Regression-specific pitfalls

- Extrapolating a linear or polynomial model outside the data range.
- Ignoring nonlinearities, interactions, or heteroscedasticity.
- Interpreting coefficients as causal effects.
- Reporting \(R^2\) without MAE/RMSE or residual analysis.
- Using squared error when extreme errors are not the main concern.
- Failing to provide prediction intervals.

### Classification-specific pitfalls

- Evaluating only accuracy on imbalanced data.
- Treating a probability as a class without a cost-sensitive threshold.
- Reporting ROC-AUC without checking rare-positive precision-recall behaviour.
- Forgetting calibration and subgroup performance.
- Multilabel data collapsed into one mutually exclusive label.

### Operational and ethical pitfalls

- The model is accurate offline but too slow, fragile, or costly online.
- Users do not know when the system is uncertain or how to appeal.
- Historical labels encode discrimination.
- The model changes a person's opportunity without a safe human process.
- The team cannot reproduce the result, explain the data, or roll back a bad release.
- Monitoring detects a problem but there is no owner or response.

### A checklist for reliable supervised learning

1. Can every feature be known at prediction time?
2. Is the target defined, reliable, and aligned with the action?
3. Are train/validation/test boundaries representative?
4. Are preprocessing steps fitted without leakage?
5. Is a simple baseline and a suitable metric reported?
6. Are uncertainty, subgroup errors, and calibration checked?
7. Are residuals or confusion matrices inspected?
8. Is the model monitored and can it be rolled back?

## Worked examples

### Example 1: temporal leakage

A model predicts loan default using “number of missed payments this year.” The prediction is made at the start of the year, but the feature is known only after several months. Training accuracy is inflated; live data cannot reproduce it. Use only variables available at origination and split by time.

### Example 2: class imbalance

A rare-fraud classifier predicts “not fraud” for every row and obtains 99.9% accuracy. The team uses PR-AUC, recall, cost-weighted loss, and a carefully validated threshold. It also checks whether resampling changes the real prevalence.

### Example 3: regression extrapolation

A linear price model performs well for houses up to 200 m² and predicts a negative price for an unusual input after a coding or unit error. Range checks, physical constraints, abstention, and domain review prevent a confident nonsense answer.

### Example 4: historical bias

A hiring model trained on past interview outcomes predicts decisions that reproduce the historical pattern. Overall accuracy is high, but qualified candidates from an underrepresented group have a larger false-negative rate. The team measures subgroup results, reviews the label process, and does not deploy the model as an autonomous decision-maker.

## Key terms & formulas

- **Target leakage:** target-revealing information in the inputs.
- **Temporal leakage:** future information used to train a past prediction.
- **Selection bias:** systematic difference caused by how examples enter the data.
- **Overfitting:** fitting training idiosyncrasies rather than stable structure.
- **Model selection bias:** choosing a model using noisy or repeatedly inspected test data.
- **Class imbalance:** unequal class frequencies.
- **Calibration:** predicted score–frequency agreement.
- **Concept drift:** change in \(P(y\mid x)\).
- **Covariate drift:** change in \(P(x)\).
- **Heteroscedasticity:** changing residual variance.
- **Extrapolation:** prediction outside observed support.
- **Abstention:** declining to predict when uncertain.
- **Fallback:** safe alternative when a model cannot serve.
- **Fairness:** subgroup performance and treatment assessed with explicit criteria.

## Common mistakes

1. **Treating every high score as evidence of a good model.** The evaluation protocol may be invalid.
2. **Using a post-outcome feature.** It is target leakage even if named innocently.
3. **Ignoring rare classes.** A trivial classifier can dominate the average.
4. **Interpreting associations as causal effects.** Predictive coefficients do not identify interventions.
5. **Extrapolating without checking support.** Predictions outside the training range are uncertain.
6. **Reporting only one metric and one split.** Robust evaluation needs several views.
7. **Not planning human oversight or rollback.** Production failures need a response.

## Exam prep

### Likely 2-mark questions

- **Define target leakage.** Use of information unavailable at prediction time that reveals or closely predicts the target.
- **Why can accuracy fail for imbalanced data?** A majority-class predictor can obtain high accuracy while missing all minority cases.
- **What is concept drift?** A change in the relationship between inputs and targets over time.
- **What is the remedy for overfitting?** More appropriate regularisation, simpler models, better data, and honest validation.

### Long-answer prompts

- **Explain the major pitfalls in supervised learning.** Cover leakage, labels, imbalance, overfitting, shift, extrapolation, and deployment.
- **How would you detect that a classifier is overfitting?** Compare training and validation curves, use repeated validation, inspect errors, and test on a fresh distribution.
- **Explain regression-specific diagnostic pitfalls.** Discuss residuals, heteroscedasticity, nonlinearities, multicollinearity, and prediction intervals.
- **A model has high accuracy but may be harmful. What would you investigate?** Target quality, leakage, subgroup metrics, calibration, costs, interpretability, and human impact.
