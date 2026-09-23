---
subject: ml
unit: 1
topic: machine-learning-basics
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Machine Learning Basics

## Overview

Machine learning (ML) is the study of algorithms that improve their performance at a task by using data or experience. Instead of writing every rule ourselves, we give an algorithm examples and let it find a useful pattern or function. The result may predict a house price, classify an e-mail as spam, group similar customers, or choose the next action for a robot.

ML matters because modern problems often involve too many inputs, uncertain relationships, changing patterns, or data that is easier to collect than rules. A model can be evaluated objectively on unseen data, but only when the task, data, and evaluation are specified carefully.

## Explanation

### Definition in terms of a task

Tom Mitchell's useful formulation is:

> A computer program learns from experience \(E\) with respect to a task \(T\) and performance measure \(P\), if its performance at \(T\), measured by \(P\), improves with experience \(E\).

The three parts are essential:

- **Task \(T\):** what must be done, for example classify an e-mail or predict a numeric price.
- **Experience \(E\):** observations or feedback, usually examples \((x,y)\), with input \(x\) and target \(y\).
- **Performance \(P\):** the score used to judge success, such as accuracy, squared error, or expected reward.

If an algorithm reduces training error but not \(P\) on unseen data, it has not learned a useful task performance.

### Data, features, and targets

A data set is often written

\[
D=\{(x_i,y_i)\}_{i=1}^{n},
\]

where each example contains a feature vector \(x_i\in\mathbb R^d\) and, in supervised learning, a target \(y_i\). Features may be age, pixel values, words, measurements, or one-hot encoded categories. The target is the quantity or class to predict.

The **feature space** is the set of possible inputs. The **hypothesis space** is the set of functions the algorithm can represent. Learning searches that hypothesis space for a function with good expected performance on unseen examples.

### The central generalisation idea

A model is judged on data not used to choose its parameters. The training set is for fitting; the validation set is for choosing hyper-parameters and models; the test set is used only for the final unbiased estimate. The training objective is a proxy for the real objective, so a model that memorises training examples can have low training loss and poor deployment performance.

Generalisation is not memorisation. A memoriser may produce the correct label for every training row but fail on a new row. A useful model captures stable structure while avoiding noise and accidental coincidences.

### Main ingredients of an ML workflow

1. Define the decision to be made and the cost of each error.
2. Collect or obtain relevant data, with consent and lawful provenance.
3. Split the data without leaking information from the future into training.
4. Explore distributions, missing values, outliers, and relationships.
5. Clean and transform data; fit preprocessing steps on training data only.
6. Choose a baseline and candidate algorithms.
7. Tune the model using a validation protocol.
8. Evaluate with task-appropriate metrics, uncertainty, error analysis, and subgroup checks.
9. Deploy, monitor, retrain, and document the model.

The order is not always strictly linear. New insights from evaluation can send us back to data collection or to redefining the objective.

### Main families of learning

- **Supervised learning:** learn \(y=f(x)\) from labelled examples. Classification predicts a class; regression predicts a number.
- **Unsupervised learning:** find structure in unlabelled data, commonly clusters, lower-dimensional representations, or association rules.
- **Reinforcement learning:** learn a policy from an agent's interaction with an environment using rewards. There is no complete label for every action.

Semi-supervised learning uses some labels with many unlabelled examples; self-supervised learning creates targets from the data itself; transfer learning reuses knowledge from a related task.

### Models are not magic

A model can only learn from the information exposed by its input representation and objective. If a medical model is not given symptoms, age, or test results, it cannot infer them reliably. If the loss rewards always predicting the majority class, the selected policy may be mathematically successful but socially and operationally useless. Model choice is therefore a decision about assumptions, data, and consequences.

### Learning, inference, and deployment

**Learning/fitting** estimates parameters from a training set. **Inference** applies the frozen model to a new example. **Deployment** exposes the model to changing users and environments. A good offline score is only the beginning; production monitoring must detect drift, latency changes, and subgroup failures.

### Learning objectives and task framing

A useful project begins with a decision statement and a performance measure, not with a dataset. For example, “flag likely late payments so that a support team can contact customers” is more actionable than “analyse customer data.” Define the prediction date, available features, target definition, class/cost trade-offs, and the action that follows. This prevents a technically accurate model from being deployed in the wrong place.

The same underlying prediction can support different decisions. A probability of disease may trigger screening, a diagnosis, or a research flag; those uses have different thresholds, explanations, and harms. Ask who is affected, what happens on a false positive and false negative, whether a person can contest the result, and whether the model is intended to replace or assist a professional. Framing is part of learning because it determines the data, target, loss, and evaluation.

## Worked examples

### Example 1: spam classification

Let \(T\) be “identify spam”, \(E\) be labelled e-mails, and \(P\) be accuracy, \(P(\hat y=y)\).

One training example is

\[
x=(\text{contains ``free''},\text{contains ``meeting''},\text{from known contact}),
\quad y=\text{spam}.
\]

After training on many labelled messages, the classifier scores an unseen message. If it labels 95 of 100 held-out messages correctly, its measured accuracy is 0.95. The test set must not be used while selecting the threshold or features.

### Example 2: house-price regression

For a house, use \(x=(\text{area},\text{rooms},\text{location})\). A linear model is

\[
\hat y=w_0+w_1\text{area}+w_2\text{rooms}+w_3\text{location}.
\]

Here \(T\) is price prediction, \(E\) is past house prices, and \(P\) may be root mean squared error. The model can learn useful approximate coefficients, but it does not know why a house is expensive unless causal evidence is supplied.

### Example 3: an objective mismatch

A rare-disease dataset has 1% positive cases. A model that always predicts “negative” obtains 99% accuracy. This is a reminder that the performance measure must include false negatives, class costs, calibration, or another relevant criterion.

### Example 4: generalisation

A student studies 100 labelled photos of cats and dogs and labels the next 100 examples. If the second set contains a different camera, lighting, and breed, the score may drop. The problem is not necessarily a bad algorithm; it is a change in the data distribution.

## Key terms & formulas

- **Instance/example:** one observation of features and, for supervised learning, a target.
- **Feature:** an input variable used by the model.
- **Label/target:** the class or numeric value being predicted.
- **Hypothesis:** a candidate function mapping inputs to predictions.
- **Parameter:** a value learned from data, such as \(w\) in a linear model.
- **Hyper-parameter:** a value chosen before training, such as a tree depth or regularisation strength.
- **Training error:** loss on examples used to fit parameters.
- **Generalisation error:** expected loss on unseen data from the target distribution.
- **Overfitting:** low training error with high unseen error.
- **Underfitting:** high error because the model is too simple or badly matched.
- **Cross-validation:** resampling training/validation folds to estimate performance.
- **Baseline:** a simple reference against which a model should be compared.
- **Data leakage:** information that should not be available while fitting reaches the training process.
- **Mitchell task tuple:** \((T,E,P)\).

## Common mistakes

1. **Saying ML replaces all rules.** It often encodes assumptions, constraints, and preprocessing; it complements rather than eliminates rules.
2. **Treating training accuracy as proof of success.** Always test on unseen, representative data.
3. **Confusing a feature with a label.** The label is the answer being learned, not an input available at prediction time.
4. **Ignoring class imbalance and unequal costs.** Accuracy may hide serious errors.
5. **Fitting preprocessing on the full data.** This leaks test information and makes validation optimistic.
6. **Assuming a model explains causality.** Predictive association is not a causal claim.
7. **Forgetting deployment drift.** The world can change after the training data were collected.

## Exam prep

### Likely 2-mark questions

- **Define ML using \(T,E,P\).** State that performance on a task improves with experience under a performance measure.
- **What is generalisation?** Good performance on unseen examples from the intended distribution.
- **Give one task and two possible performance measures.** Regression/prediction with RMSE or MAE; classification with accuracy or F1.
- **What is overfitting?** A model fits training noise and performs poorly on new data.

### Long-answer prompts

- **Explain the main components of a machine-learning system.** Cover data, features, target, hypothesis space, algorithm, loss, optimisation, and evaluation, with a worked example.
- **Describe a complete ML lifecycle.** Explain question formulation, data preparation, training, validation, testing, deployment, and monitoring, highlighting leakage and distribution shift.
- **Compare supervised, unsupervised, and reinforcement learning.** Use data, feedback, objective, and example tasks; explain why the same algorithm may be used in different settings.
