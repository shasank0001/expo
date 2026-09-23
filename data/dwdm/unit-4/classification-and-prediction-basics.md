---
subject: dwdm
unit: 4
topic: classification-and-prediction-basics
syllabus_ref: CSM3101 Unit-IV
status: draft
---
# Classification and Prediction: Basic Concepts

## Overview

Classification and prediction are supervised learning tasks. **Classification** assigns an object to a discrete class, such as spam/not spam, approved/rejected, or disease/no disease. **Prediction** estimates a numeric value, such as house price, demand next month, or delivery time. The model is learned from examples with known outputs and is then used to estimate an output for a new object.

The syllabus covers many algorithms, but they share the same lifecycle: define the classes and target, split data without leakage, learn a model, evaluate it on unseen data, and monitor performance after deployment. A high training score alone does not demonstrate generalization.

## Explanation

### 1. Supervised learning

In supervised learning, every training example has one or more labels:

\[
D=\{(x^{(1)},y^{(1)}),\ldots,(x^{(n)},y^{(n)})\}.
\]

The input vector \(x\) contains attributes or features. The label \(y\) is known during training. The goal is to learn a function

\[
\hat y=f(x)
\]

that approximates the unknown target relationship and performs well on new data.

The training set should be representative of the population on which predictions will be used. Random splitting is common, but time, location, or customer grouping may require a different split to prevent leakage.

### 2. Classification

For a categorical target with classes \(C=\{c_1,\ldots,c_K\}\), a classifier returns a class or a score for each class. Common tasks include:

- binary classification: one positive and one negative class;
- multiclass classification: more than two mutually exclusive classes;
- multilabel classification: an object may have several labels.

A classifier may output hard labels or probabilities. A probability is useful for ranking and threshold selection, but must be calibrated if it is treated as a real likelihood.

### 3. Prediction or regression

If \(y\) is continuous, the model predicts a number. Common methods include linear regression, regression trees, neural networks, and support-vector regression. Mean squared error is common for numeric prediction; mean absolute error is more robust to outliers. Classification and regression share data preparation and validation, but their target types and evaluation measures differ.

### 4. Building a classifier

1. Understand the prediction target and its unit of analysis.
2. Collect, clean, and encode attributes.
3. Split or sample data into training, validation, and test sets.
4. Select candidate models and their hyperparameters.
5. Train using the training data only.
6. Tune using validation or cross-validation.
7. Evaluate once on the untouched test data.
8. Refit, deploy, and monitor for drift and changing behavior.

A **validation set** selects hyperparameters, while a **test set** estimates final performance. Repeatedly tuning on the test set turns it into a validation set and makes its score optimistic.

### 5. Model output and decision threshold

A probability threshold of 0.5 is a default, not a law. If false negatives are expensive, the classifier should predict the positive class at a lower threshold. The operating point should reflect costs and the business action. With multiple classes, predictions may be one-versus-one or one-versus-rest; confusion matrices must state the class orientation.

### 6. Generalization and overfitting

**Generalization** is performance on previously unseen data. A model overfits when it learns training details that do not transfer, such as noise or a coincidental customer ID. Underfitting occurs when the model is too simple to capture the structure. Validation, regularization, adequate model complexity, and representative data manage the trade-off.

### 7. Common data issues

- Missing values require an explicit strategy.
- Duplicate records can leak a case into training and testing.
- Rare classes can be hidden by overall accuracy.
- High-cardinality identifiers can cause memorization.
- Irrelevant attributes can distort distances and splits.
- Data leakage uses information that would not be available at prediction time.

## Worked examples

### Example 1: Classification versus regression

A bank wants to answer two questions:

- “Will this application default?” is classification; the answer is yes/no.
- “How much will this applicant pay next month?” is regression; the answer is a number.

A model that predicts probabilities and then chooses “yes” is still a classifier. A model that predicts \(\$4{,}200\) is a predictor/regressor.

### Example 2: Basic confusion matrix

Suppose 1,000 test loans are labeled risky or safe.

| | Predicted risky | Predicted safe |
|---|---:|---:|
| Actual risky | 80 | 20 |
| Actual safe | 100 | 800 |

There are 100 actual risky loans: recall is \(80/100=80\%\). There are 900 actual safe loans: specificity is \(800/900=88.9\%\). Overall accuracy is \(880/1000=88\%\). Accuracy is high because the safe class is large; the class-specific measures expose the risky miss rate.

### Example 3: Effect of a threshold

Suppose fraud scores are 0.30, 0.45, and 0.60 for three cases. At threshold 0.5, only the last is flagged. At 0.4, the first two are also flagged. The model's ranking has not changed, but the action has. Threshold selection is therefore part of deployment, not just an afterthought.

### Example 4: Leakage

A bank's “account closed” field is set when a loan defaults. Training on it to predict default lets the model read the answer. A closed-account flag available only after default is leakage. A balance recorded before the decision may be valid, but its timestamp must be checked.

## Key terms & formulas

- **Feature/input \(x\):** an attribute used for prediction.
- **Label/target \(y\):** known class or numeric value in training.
- **Classification:** assign a discrete class.
- **Regression/prediction:** estimate a continuous value.
- **Generalization:** performance on unseen data.
- **Training set:** data used to estimate model parameters.
- **Validation set:** data used for model and hyperparameter selection.
- **Test set:** untouched data for final estimation.
- **Decision threshold:** probability or score boundary for an action.
- **Hard prediction:** selected class; **probability prediction:** estimated class likelihood.

## Common mistakes

1. **Calling every numeric target “prediction” without naming regression:** state that the target is continuous.
2. **Reporting training accuracy as final performance:** it measures fit, not generalization.
3. **Reusing the test set for tuning:** the reported score becomes optimistic.
4. **Ignoring class imbalance:** a majority-class model can have high accuracy while failing the rare class.
5. **Using future information:** feature timestamps must precede the prediction time.
6. **Assuming output probabilities are perfectly calibrated:** ranking and probability reliability are related but different.

## Exam prep

**Likely 2-mark questions**
1. Differentiate classification and prediction. *Hint: discrete class versus continuous numeric estimate.*
2. Define supervised learning. *Hint: learn a mapping from labeled examples.*
3. What is data leakage? *Hint: training uses information unavailable at prediction time.*

**Likely long-answer questions**
1. Explain the supervised classification workflow. *Hint: target, split, train, validate, test, deploy, monitor.*
2. Compare hard and probability predictions and describe threshold selection. *Hint: class label versus score; costs and operating point.*
3. Explain overfitting and underfitting with a train/validation example. *Hint: training-test gap, model complexity, and generalization.*
