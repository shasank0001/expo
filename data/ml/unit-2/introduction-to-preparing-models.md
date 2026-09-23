---
subject: ml
unit: 2
topic: introduction-to-preparing-models
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Introduction to Preparing to Model and Evaluating ML

## Overview

A machine-learning project is a chain of decisions: understand the problem, inspect the data, prepare it, choose a model, train it, evaluate it honestly, and improve it. Most beginner projects focus only on the algorithm. In practice, data quality, feature design, evaluation design, and deployment constraints often decide whether the system is useful.

Unit II is about preparing to model and modelling with evaluation. The phrase “preparing to model” means deciding what the model should predict, representing observations as useful inputs, and making the data safe to use. “Modelling and evaluation” means fitting a model, measuring it on data it did not see, and improving it without cheating.

## Explanation

### Start with the decision, not the dataset

Write the intended decision in plain language: who will make the decision, at what time, for which population, and what action follows a prediction. A useful problem statement names the target, the available features at prediction time, the cost of false positives and false negatives, and the time horizon. “Predict churn” is incomplete. “On 1 October, predict which active subscribers will cancel within 30 days so that the retention team can offer support” defines a usable task.

### The end-to-end activities

1. **Frame:** identify users, decision, objective, constraints, and success measures.
2. **Collect:** obtain data with consent, provenance, and coverage of relevant groups and time.
3. **Explore:** study types, distributions, missingness, relationships, outliers, and possible leakage.
4. **Prepare:** clean, transform, encode, scale, engineer features, and split appropriately.
5. **Model:** establish a baseline and fit candidate algorithms.
6. **Evaluate:** use an honest test or validation process, appropriate metrics, and error analysis.
7. **Improve:** change features, data, objective, or algorithm based on evidence.
8. **Deploy and monitor:** serve predictions, record outcomes, detect drift, and retrain safely.

These are iterative activities. For example, error analysis may reveal a missing feature; collecting it changes the data schema; the model and evaluation plan must then be revisited.

### A clean experimental boundary

A useful separation is:

- **Training data:** estimate model parameters.
- **Validation data:** select features, hyper-parameters, thresholds, and candidate models.
- **Test data:** estimate final performance once.
- **Production data:** the changing stream encountered after deployment.

The boundary must match the application. For time series, split chronologically. For records from the same person or device, keep groups together. Do not calculate imputation values, vocabulary, feature scaling, or target encoding using the test set. A pipeline fitted on training data and applied to later data helps enforce this boundary.

### Representation and objective

Most algorithms require numeric input. A row becomes a feature vector, and a column transformation can turn categories, text, images, or times into numbers. The representation should preserve relevant information and remove nuisance variation. The target and loss should match the actual loss of the decision. A probability score may be needed to choose a threshold; a class label alone may hide uncertainty.

### Generalisation and validation

The model should work on future examples, not just the rows used to fit it. A representative split or cross-validation provides evidence of generalisation. The score should be accompanied by an uncertainty estimate, subgroup analysis, and a description of failure conditions. A single lucky split can change a conclusion, especially with small data.

### Model improvement discipline

Improvement is an experiment, not a list of tricks:

1. State a hypothesis, such as “standardisation will reduce tree sensitivity to scale.”
2. Change one important factor where possible.
3. Keep the evaluation protocol fixed.
4. Record the result and uncertainty.
5. Keep the change only if it improves the target metric without unacceptable trade-offs.

This prevents the common error of repeatedly testing on the test set until a good number appears.

## Worked examples

### Example 1: a churn project

A telecom company wants to target customers who may cancel next month. The target is cancellation within 30 days. Features available on the prediction date include tenure, plan, usage, and support contacts. Data is split by time, not randomly across future months. A baseline predicts the historical cancellation rate; then a regularised logistic model, tree model, and calibrated model are compared. The final threshold reflects the value of a retention offer and the cost of contacting a customer who will stay.

### Example 2: a small classification data set

With 80 records, a single test set of 20 records is unstable. Repeated stratified cross-validation gives a more useful comparison, but the final estimate still has wide uncertainty. The team reports the mean and spread, keeps a small untouched test set if possible, and avoids claiming that a 2% difference is meaningful without evidence.

### Example 3: an image project

Images are split by customer or capture session, not by individual image, because near-duplicate frames would otherwise appear in both training and test sets. Augmentation is fitted within the training pipeline. The model is evaluated by precision and recall on the clinically relevant positive class, not by frame accuracy alone.

## Key terms & formulas

- **Problem framing:** defining the decision, target, population, time, and costs.
- **Lifecycle:** data to deployment and monitoring.
- **Baseline:** simple reference model.
- **Training/validation/test split:** three roles for data.
- **Pipeline:** preprocessing plus estimator fitted as one unit.
- **Target leakage:** information unavailable at prediction time entering the input.
- **Generalisation:** performance on unseen data.
- **Reproducibility:** ability to repeat an experiment with the same documented setup.
- **Model improvement:** evidence-based changes to data, representation, objective, or algorithm.
- **Uncertainty:** variation in estimates and predictions.
- **Deployment boundary:** the point at which a model is used on live data.

## Common mistakes

1. **Starting by importing a classifier.** Start with the decision and the available prediction-time information.
2. **Treating all data as one undifferentiated table.** Consider time, group, source, and target definitions.
3. **Using the test set to tune a threshold.** This turns the test estimate into another validation estimate.
4. **Reporting only the best run.** Show the baseline, uncertainty, and chosen protocol.
5. **Assuming more preparation always helps.** Transformations can discard signal or create leakage.
6. **Ignoring the cost of collecting later features.** A feature that is unavailable at decision time is not usable.

## Exam prep

### Likely 2-mark questions

- **List four ML project activities.** Framing, data collection, exploration, preparation, modelling, evaluation, or deployment.
- **What is the purpose of a test set?** A final unbiased estimate on data not used for fitting or selection.
- **Why is a baseline useful?** It provides a simple reference for deciding whether a model adds value.
- **Name one leakage example.** Using a value recorded after the prediction time.

### Long-answer prompts

- **Explain the machine-learning project lifecycle.** Connect each stage to decisions, artefacts, and possible failure modes.
- **Describe how to create an honest train/validation/test boundary.** Cover time, grouping, preprocessing, tuning, and repeated evaluation.
- **Why is problem framing part of data preparation?** Use a healthcare or customer-churn example to connect features, targets, costs, and metrics.
- **How would you improve a weak model scientifically?** State hypotheses, change one factor, evaluate honestly, and record trade-offs.
