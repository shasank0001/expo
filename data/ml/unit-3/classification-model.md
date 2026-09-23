---
subject: ml
unit: 3
topic: classification-model
syllabus_ref: CSM3201 Unit-III
status: draft
---
# Classification Model

## Overview

A classification model learns a boundary or probability distribution that maps features to one of several classes. It can predict a hard class label or a score/probability for each class. Classification models are used whenever the output is a category: spam, disease status, object type, customer segment, or risk band.

A useful model does more than count correct labels. It should produce calibrated scores when probabilities matter, behave sensibly on new data, make its error costs clear, and provide enough explanation for the decision. The model includes the target definition, representation, decision rule, and evaluation—not just an algorithm.

## Explanation

### Model formulation

For class \(k\), a classifier estimates

\[
p_k(x)=P(Y=k\mid x).
\]

A generative model estimates class-conditional distributions \(p(x\mid Y=k)\) and prior probabilities \(P(Y=k)\), then applies Bayes' rule:

\[
P(Y=k\mid x)=\frac{p(x\mid Y=k)P(Y=k)}
{\sum_jp(x\mid Y=j)P(Y=j)}.
\]

A discriminative model directly estimates \(p_k(x)\), as in logistic regression, a decision tree, an SVM score, or a neural softmax output. Generative models can be useful with small data or when modelling \(p(x\mid y)\); discriminative models often optimise the decision objective directly.

### Binary decision models

A binary model can output a linear score

\[
z=w^\top x+b.
\]

Logistic regression maps it to a probability:

\[
p_1=\sigma(z)=\frac{1}{1+e^{-z}},\qquad
p_0=1-p_1.
\]

The decision boundary is \(z=0\), a linear boundary in feature space. The sign of \(z\) is not a probability, and the default threshold 0.5 may not be optimal.

A decision tree partitions the space with axis-aligned rules. An SVM constructs a margin-maximising separator, with kernels allowing nonlinear boundaries. A k-nearest-neighbour classifier predicts from nearby labelled examples. A neural network learns nonlinear features through hidden layers and produces logits that become probabilities.

### Multiclass classification

For mutually exclusive classes, multiclass logistic regression uses one set of scores per class and a softmax:

\[
p_k(x)=\frac{e^{z_k(x)}}{\sum_{j=1}^{K}e^{z_j(x)}}.
\]

One-vs-rest trains \(K\) binary problems; one-vs-one trains \(K(K-1)/2\) binary problems and combines votes. Trees, SVMs, kNN, and neural networks also have multiclass variants. For multilabel data, each class has an independent sigmoid, so several labels can be active.

### Decision rule and costs

Given probabilities and a cost matrix \(C_{kj}\), a cost-sensitive rule predicts

\[
\hat k=\arg\min_j\sum_k C_{kj}p_k(x).
\]

The Bayes-optimal rule maximises posterior probability only when all errors cost the same. Threshold selection should use validation data and the real consequences of false positives and false negatives.

### Performance measures

For a binary task, form the confusion matrix and compute

\[
\text{precision}=\frac{TP}{TP+FP},\quad
\text{recall}=\frac{TP}{TP+FN},\quad
F_1=\frac{2PR}{P+R}.
\]

For multiclass tasks, macro averaging weights each class equally, while micro averaging aggregates counts. ROC-AUC measures ranking across thresholds; PR-AUC focuses on positive precision-recall behaviour. Log loss evaluates probabilities, and calibration plots check whether a score of 0.8 occurs about 80% of the time.

### Generalisation and overfitting

A classifier can memorise training labels. Use representative splits, regularisation, pruning or depth limits, ensembles, early stopping, and data augmentation where appropriate. Class imbalance can make accuracy misleading and can make a model ignore a minority class. Resampling, class weights, thresholding, and suitable metrics address different parts of the problem.

### Interpretability and error analysis

A tree path, linear log-odds, feature contributions, confusion matrix, and examples of errors provide different levels of understanding. Examine false positives and false negatives separately. A model may be accurate overall but systematically fail for a subgroup, a rare class, or a new data source. Error analysis should feed the next modelling decision.

## Worked examples

### Example 1: logistic prediction

For a customer, \(z=1.2\). Then

\[
p_1=\frac{1}{1+e^{-1.2}}\approx0.769.
\]

If a fraud policy uses a 0.60 threshold, the customer is flagged. The threshold is chosen from cost and validation data; it is not automatically 0.5.

### Example 2: Bayes classification

Suppose classes A and B have equal priors. A new observation is more likely under \(A\) than under \(B\), by a likelihood ratio of 3. The posterior odds are also 3:1, so the model predicts A with posterior probability \(3/(3+1)=0.75\).

### Example 3: multiclass softmax

If logits are \([2,1,0]\),

\[
e^2=7.39,\quad e^1=2.72,\quad e^0=1,
\]

so the softmax is approximately \([0.665,0.245,0.090]\). The model predicts class 1, but the probabilities provide more information for a cost-sensitive rule.

### Example 4: error pattern

A plant classifier has 98% accuracy but almost no recall for a rare disease class. The confusion matrix and subgroup analysis reveal the problem. Resampling or class-weighted loss may improve recall, but the team also checks whether the rare cases are correctly labelled and whether the new threshold harms precision.

## Key terms & formulas

- **Classifier:** function \(h(x)\) returning a class.
- **Class posterior:** \(P(Y=k\mid x)\).
- **Generative model:** models \(p(x\mid k)\) and \(p(k)\).
- **Discriminative model:** directly models \(p(k\mid x)\).
- **Logit:** \(w^\top x+b\).
- **Sigmoid:** \(\sigma(z)=1/(1+e^{-z})\).
- **Softmax:** \(p_k=e^{z_k}/\sum_j e^{z_j}\).
- **Bayes decision rule:** choose the lowest expected-cost class.
- **Decision boundary:** region where the predicted class changes.
- **Precision:** proportion of positive predictions that are correct.
- **Recall:** proportion of actual positives detected.
- **F1:** harmonic mean of precision and recall.
- **Multiclass:** more than two mutually exclusive classes.
- **Multilabel:** multiple labels may coexist.
- **Calibration:** correspondence between predicted and observed probabilities.
- **Class imbalance:** unequal numbers of training or deployment examples.

## Common mistakes

1. **Reporting a hard label only when probabilities are needed.** Lose useful uncertainty.
2. **Using accuracy with severe class imbalance.** A trivial predictor may look excellent.
3. **Treating 0.5 as a universal threshold.** The error costs and prevalence matter.
4. **Confusing logits with probabilities.** A logit is an unbounded score.
5. **Ignoring class order in ordinal tasks.** Standard multiclass models may make incorrect assumptions.
6. **Evaluating only overall accuracy.** Inspect false positives, false negatives, calibration, and subgroups.
7. **Assuming a classifier predicts causes.** It predicts the target association represented by training data.

## Exam prep

### Likely 2-mark questions

- **Define a classification model.** A model that maps features to a class or class probabilities.
- **State the sigmoid function.** \(\sigma(z)=1/(1+e^{-z})\).
- **What is a decision boundary?** The region or surface where predictions change class.
- **Give two classification evaluation measures.** Precision, recall, F1, accuracy, ROC-AUC, or PR-AUC.

### Long-answer prompts

- **Explain the structure of a binary classification model.** Discuss scores, probabilities, thresholds, loss, and Bayes-optimal decisions.
- **Compare logistic regression, decision trees, SVMs, kNN, and neural classifiers.** Use data needs, boundaries, interpretability, and scaling.
- **Describe multiclass and multilabel classification.** Include softmax, one-vs-rest, one-vs-one, and metric averaging.
- **How would you analyse a classifier's errors?** Discuss the confusion matrix, subgroup patterns, calibration, and feedback to data/model design.
