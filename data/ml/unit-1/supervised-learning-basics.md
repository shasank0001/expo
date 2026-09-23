---
subject: ml
unit: 1
topic: supervised-learning-basics
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Supervised Learning Basics

## Overview

Supervised learning uses labelled examples to learn a mapping from inputs to known outputs. The input is usually called \(x\), and the correct answer is \(y\). After training, the model receives an input whose target is unknown and predicts \(\hat y\).

It is the usual choice when historical data already contains the answer we want to predict: a customer either churned or stayed, a machine part failed or survived, an image contains a car, or a house sold for a price. The “supervision” is the known target during training, not a human watching every production prediction.

## Explanation

### The supervised-learning setup

Given training data

\[
D=\{(x_i,y_i)\}_{i=1}^{n},
\]

a learning algorithm selects a hypothesis \(h\) from a hypothesis class. The quality of \(h\) is measured by a loss function that compares \(h(x_i)\) with \(y_i\). After parameter estimation, the learned function is

\[
\hat y=h_{\hat\theta}(x).
\]

The data should be independent and representative examples from the population to which the model will be applied. If the future distribution changes, the learned relationship may no longer hold.

### Classification and regression

**Classification** predicts a class label. The target may be binary, multiclass, multilabel, or hierarchical.

- Binary: fraud/not fraud.
- Multiclass: cat/dog/bird.
- Multilabel: an article can be about sport and politics.
- Ordinal: low/medium/high satisfaction, where order matters.

**Regression** predicts a continuous value, such as demand, temperature, or price. A classification model may output probabilities, but a high probability is not automatically a numeric prediction unless a decision rule is specified.

### Typical workflow

1. Define the prediction target and the time at which the prediction will be made.
2. Collect labels, checking how they were created and whether they are consistent.
3. Split data into training, validation, and test sets; group repeated records to prevent leakage.
4. Explore features and encode categorical, numerical, text, or image data.
5. Establish a simple baseline.
6. Train one or more candidate models using a suitable loss.
7. Select hyper-parameters on validation data or cross-validation.
8. Evaluate on untouched test data with metrics suitable for the task.
9. Analyse errors and subgroups, deploy carefully, and monitor drift.

### Important forms of supervision

- **Exact labels:** one known target per row.
- **Noisy labels:** targets contain mistakes or disagreements.
- **Partial labels:** the annotator knows only part of the answer.
- **Weak labels:** an indirect signal such as a click or purchase is used as a proxy.
- **Delayed labels:** the target arrives after a long time, so training is delayed.
- **Aggregate labels:** a label applies to a group but not to every individual member.

The label should match the decision. “Clicked” is not the same as “will be satisfied,” and “was treated” is not automatically evidence that treatment was necessary.

### Losses and model fitting

For squared-error linear regression, a common objective is

\[
J(\theta)=\frac{1}{2n}\sum_{i=1}^{n}(h_\theta(x_i)-y_i)^2.
\]

For binary classification, logistic regression often minimises binary cross-entropy:

\[
J(\theta)=-\frac1n\sum_{i=1}^{n}
\left[y_i\log p_i+(1-y_i)\log(1-p_i)\right],
\]

where \(p_i=P(Y=1\mid x_i)\). Optimisation changes parameters until the loss is low. Regularisation and validation are needed to control overfitting.

### Overfitting and underfitting

A high-capacity model can memorise idiosyncrasies of the training set. It then has low training error but poor test error—**overfitting**. A model that is too weak or poorly specified has high error on both sets—**underfitting**. Remedies include more representative data, simpler models, regularisation, feature selection, early stopping, and better validation.

### When supervised learning is suitable

It is suitable when:

- the target is available and meaningful;
- enough labelled examples cover important cases;
- prediction time is after the feature collection time;
- the cost of errors can be specified;
- the deployment population resembles the training population.

It is unsuitable or risky when labels are systematically biased, examples are too few, the target is not actionable, or a high-stakes decision needs causal or human explanation.

### Relationship to other learning types

A classification or regression problem can be handled with a linear model, decision tree, SVM, neural network, or ensemble. A semi-supervised method can use extra unlabelled data. A recommender can be trained with implicit feedback. Reinforcement learning is different because it learns a sequence of actions from delayed consequences rather than fitting a target for each input.

## Worked examples

### Example 1: a tiny classifier

Suppose a spam filter uses whether an e-mail contains the word “offer.”

Training data:

| Contains “offer” | Label |
|---|---|
| Yes | Spam |
| No | Normal |
| Yes | Spam |
| No | Normal |

The model learns a score such as

\[
\hat y=\mathbf{1}(x_{\text{offer}}=1).
\]

On a new message with no “offer,” it predicts normal. This model is a transparent baseline, although it ignores many real spam signals.

### Example 2: regression calculation

A simple model predicts price as \(\hat y=50,000+1,500\cdot\text{area}\), with area in square metres. For a 100 m² home,

\[
\hat y=50,000+1,500(100)=200,000.
\]

If the observed price is 220,000, the squared error is \(20,000^2\). One observation does not justify the coefficient; it merely illustrates prediction and loss.

### Example 3: threshold choice

A fraud classifier produces scores. Lowering the threshold catches more fraud but may reject more legitimate transactions. The correct threshold is a business decision informed by precision, recall, and expected cost, not a universal default.

### Example 4: label leakage

A hospital model predicts readmission using a field “discharge medication prescribed after readmission.” The field is recorded later than the prediction time. Including it makes test accuracy look excellent but makes the model unusable at admission time.

## Key terms & formulas

- **Feature vector:** \(x\in\mathbb R^d\).
- **Target:** \(y\), known during training and unknown at prediction time.
- **Prediction:** \(\hat y=h_{\hat\theta}(x)\).
- **Training loss:** empirical objective minimised while fitting.
- **Squared error:** \((y-\hat y)^2\).
- **Mean squared error:** \(\frac1n\sum_i(y_i-\hat y_i)^2\).
- **Mean absolute error:** \(\frac1n\sum_i|y_i-\hat y_i|\).
- **Binary cross-entropy:** \(-\left[y\log p+(1-y)\log(1-p)\right]\).
- **Classification:** target is a class.
- **Regression:** target is numeric.
- **Decision threshold:** probability or score at which a class is selected.
- **Overfitting:** fitting training noise.
- **Underfitting:** failing to capture relevant structure.
- **Data leakage:** future or protected information entering training.
- **Target leakage:** a feature directly reveals the target.

## Common mistakes

1. **Calling any labelled problem “supervised” without defining the label.** Say what \(y\) means and when it is known.
2. **Using accuracy for every classification task.** Imbalanced costs can make it misleading.
3. **Confusing a predicted probability with a hard class.** State the threshold and calibration if relevant.
4. **Training on test data.** This invalidates the final performance estimate.
5. **Using features unavailable at prediction time.** Avoid target and temporal leakage.
6. **Assuming a high-capacity model is always better.** Compare against a simple, well-validated baseline.
7. **Reporting only one number.** Include the split protocol, class balance, uncertainty, and error analysis.

## Exam prep

### Likely 2-mark questions

- **Define supervised learning.** Learning a mapping from input features to known targets using labelled examples.
- **Give one classification and one regression example.** Fraud detection; house-price prediction.
- **What is overfitting?** Low training error but poor performance on unseen data.
- **Name two common regression losses.** Mean squared error and mean absolute error.

### Long-answer prompts

- **Explain the supervised-learning workflow.** Include labels, splitting, preprocessing, training, model selection, testing, and deployment; explain leakage prevention.
- **Compare classification and regression.** Give target types, examples, suitable metrics, and two examples each.
- **How can overfitting be controlled?** Discuss simpler models, regularisation, more data, feature work, early stopping, and honest validation.
- **Explain why a label can be misleading.** Use weak labels, delayed labels, bias, and target leakage as examples.
