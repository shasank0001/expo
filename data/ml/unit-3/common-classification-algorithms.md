---
subject: ml
unit: 3
topic: common-classification-algorithms
syllabus_ref: CSM3201 Unit-III
status: draft
---
# Common Classification Algorithms

## Overview

Classification algorithms learn a relationship from labelled inputs to discrete classes. The main families include nearest-neighbour methods, probabilistic classifiers, linear models, decision trees, support-vector machines, ensembles, and neural networks. No family is universally best: performance depends on the data geometry, sample size, noise, class balance, and deployment requirements.

This note compares the common methods, their central idea, strengths, limitations, and useful hyper-parameters. The aim is to choose and explain methods, not to memorise only algorithm names.

## Explanation

### 1. Nearest-neighbour classification

k-nearest neighbours (kNN) stores labelled examples and assigns a new point using the classes of its \(k\) closest neighbours. For a continuous point,

\[
d(x,z)=\sqrt{\sum_{j=1}^{p}(x_j-z_j)^2}.
\]

A simple rule is majority vote; weighted kNN can use \(1/d\) weights. **Advantages:** simple, non-parametric, naturally multi-class, and useful for small data. **Limitations:** expensive prediction, sensitive to scaling and irrelevant features, and affected by class imbalance and high dimensionality. Standardise features, choose \(k\) and distance metric, and consider dimensionality reduction.

### 2. Naive Bayes

Naive Bayes models class-conditional features as conditionally independent given the class:

\[
P(Y=k\mid x_1,\ldots,x_p)\propto P(Y=k)\prod_{j=1}^{p}P(x_j\mid Y=k).
\]

Variants use Gaussian, Bernoulli, or multinomial likelihoods. It is fast, works well with high-dimensional text, and gives probabilities through the priors and likelihoods. The independence assumption is usually unrealistic, so probabilities can be poorly calibrated even when ranking is useful. Zero counts require smoothing.

### 3. Logistic regression

Binary logistic regression models

\[
\log\frac{p_k}{1-p_k}=w_0+w^\top x.
\]

It is a linear classifier in log-odds, interpretable, probabilistic, and a strong baseline. It handles mixed data after suitable encoding, but its decision boundary is linear unless polynomial or interaction features are added. Regularisation controls correlated or high-dimensional inputs.

For \(K\) classes, multinomial logistic regression uses one score per class and softmax. The loss is multiclass cross-entropy.

### 4. Decision trees

A tree recursively chooses a feature and threshold that improve a criterion such as Gini impurity,

\[
G=1-\sum_{k=1}^{K}p_k^2,
\]

or entropy,

\[
H=-\sum_{k=1}^{K}p_k\log p_k.
\]

Leaves store a class distribution. Trees need little scaling, capture interactions, and provide paths, but can overfit and are unstable. Control depth, minimum leaf size, number of leaves, and stopping criteria; prune or use an ensemble.

### 5. Support-vector machines

An SVM finds a separator with a large margin. For a linear binary problem it solves, informally,

\[
\min_{w,b,\xi}\frac12\|w\|^2+C\sum_i\xi_i
\]

subject to \(y_i(w^\top x_i+b)\ge1-\xi_i\). The \(C\) parameter trades margin size against training error. Kernels such as \(K(x,z)=x^\top z\), polynomial, radial basis, and sigmoid permit nonlinear boundaries. SVMs can be effective in moderate dimensions and are sensitive to scaling and \(C\); kernel methods may be costly for very large data.

### Decision trees in more detail

At each node, a tree searches candidate features and thresholds and chooses the split that reduces impurity the most. For a candidate split \(S\) of a node,

\[
\text{gain}(S)=I(\text{parent})-\sum_{c\in\{\text{left},\text{right}\}}\frac{n_c}{n}I(c).
\]

A greedy tree makes the best local split; it cannot revisit an earlier choice. Stopping rules such as maximum depth, minimum samples per leaf, or minimum impurity decrease limit overfitting. Cost-complexity pruning can remove branches that do not justify their complexity. A leaf's class probability is the proportion of its training labels, so a leaf with few examples is often uncertain.

Trees are attractive for mixed tabular data because thresholds and categorical splits can be handled directly. They are not invariant to every transformation: a monotonic transformation of a feature can change candidate thresholds, and a high-cardinality feature can receive many split opportunities. A tree's path is a useful local explanation, but a path is not a causal account. A single tree should be validated for stability, especially before a high-stakes decision.

### Support-vector machines in more detail

For a linearly separable binary problem, support vectors lie on or near the margin. The SVM optimisation above balances \(\|w\|^2\), which encourages a wide margin, against \(C\sum_i\xi_i\), which penalises margin violations. A large \(C\) produces fewer training violations and can fit a more complex boundary; a smaller \(C\) tolerates more violations for a wider, smoother margin. The solution is not obtained by ordinary least squares and is affected by the chosen class costs.

A kernel defines similarity without explicitly mapping to a high-dimensional space:

\[
K(x,z)=
\begin{cases}
x^\top z,&\text{linear},\\
(x^\top z)^d,&\text{polynomial},\\
\exp(-\gamma\|x-z\|^2),&\text{radial basis}.
\end{cases}
\]

The RBF kernel creates smooth nonlinear boundaries, but \(\gamma\) controls the influence of a nearby point. A polynomial kernel has a degree parameter. All kernel inputs should be scaled; otherwise a feature with a large numerical range dominates. A hard-margin SVM assumes perfect separability, while a soft-margin SVM uses slack variables for overlap or noise.

SVMs are often strong with moderate sample sizes and many features, including some text and biological settings. They can be costly for large \(n^2\) or \(n^3\) training, may return hard scores rather than calibrated probabilities, and are sensitive to \(C,\gamma,\) and kernel choice. Probability estimates can be obtained through a separate calibration procedure or a sigmoid/Platt-style method, but they must be evaluated. Always compare an SVM with a logistic/tree baseline and inspect the error cost rather than assuming a larger margin is always better.

### 6. Random forests

A random forest trains many decorrelated trees, usually on bootstrap samples with a random subset of features at each split. Classification uses majority vote or averaged probabilities. Bagging reduces variance, and out-of-bag samples can provide an internal estimate. Forests handle mixed features, nonlinearities, and interactions with relatively little tuning, but can be less interpretable and may not extrapolate smoothly.

### 7. Gradient-boosted trees

Boosting adds trees sequentially so each new tree corrects errors of the current ensemble:

\[
F_m(x)=F_{m-1}(x)+\eta h_m(x).
\]

Shallow trees and a learning rate control the trade-off between speed and approximation. Gradient boosting is often excellent on tabular data, but tuning, early stopping, class weights, and overfitting require care. Explainability can be provided through feature importance, SHAP, or surrogate models, with limitations.

### 8. Neural-network classifiers

A multilayer perceptron composes affine transformations and nonlinear activations and ends in a sigmoid or softmax. Neural networks learn representations, handle images/text/audio, and scale with large data, but require careful initialisation, optimisation, regularisation, and monitoring. They can be overconfident and need calibration.

### 9. Prototype and rule-based classifiers

Nearest-centroid, rule lists, and case-based methods can be transparent and data-efficient. Their quality depends on a meaningful distance, reliable rules, or representative prototypes. They are useful baselines when a complex model is not justified.

### Choosing and comparing classifiers

No classifier is best merely because it is more sophisticated. Compare candidates under the same preprocessing, split, and evaluation protocol. A useful comparison table records the inductive bias, training cost, inference cost, probability behaviour, interpretability, and treatment of missing/unscaled features.

- **Logistic regression** is a strong first model for tabular data because it is fast, regularisable, and interpretable. Its limitation is a linear log-odds boundary unless interaction or basis features are added.
- **Trees** are naturally robust to feature scale and can express interactions. A single tree is unstable and interpretable; an ensemble is often more accurate but less transparent.
- **SVMs** are attractive when the number of features is moderate and the margin matters. They need scaling and can be expensive with large data or unsuitable kernels.
- **kNN** is a useful non-parametric baseline, but its prediction cost and curse of dimensionality make it less suitable for large or sparse production systems.
- **Neural networks** can learn representations from raw modalities, but they need more data, tuning, and monitoring. Their probability outputs may require calibration.

Class imbalance changes the practical choice. A class-weighted logistic loss, balanced tree sampling, threshold selection, or a cost-sensitive SVM may improve minority recall, but the team must inspect precision, calibration, and subgroup effects. It is not enough to compare default accuracy.

A useful model-selection process is:

1. build a majority-class or simple rule baseline;
2. fit a linear/logistic or shallow-tree candidate;
3. add a more flexible candidate only if the problem warrants it;
4. tune each candidate on validation data;
5. compare metrics, uncertainty, calibration, latency, and failure slices;
6. select the simplest model that meets the application requirements.

For an exam or report, justify a method by stating the assumption it makes. For example, choose a tree when thresholds and interactions are plausible, a linear model when a smooth additive relationship is plausible, and a neural network when the raw input is high-dimensional and the data set is large enough to learn its representation.

## Worked examples

### Example 1: kNN

A new customer's standardised spending and frequency are closest to six high-value customers and four low-value customers. k=10 majority vote predicts high value. A value of k=1 may be noisy; a very large k may underfit. The team tunes k using validation folds and checks class balance.

### Example 2: decision tree

A tree first asks whether income is above ₹50,000, then whether an account is overdue. A leaf predicts default probability 0.75. The path is explainable, but a different sample can change the first split; an ensemble reduces variance.

### Example 3: SVM margin

A linear SVM tries to place the boundary midway between the nearest points of two classes. A large \(C\) penalises training mistakes more strongly and can create a narrower, more irregular boundary; a smaller \(C\) tolerates more error for a smoother margin.

### Example 4: boosting

A first shallow tree misses several difficult positive cases. The next tree is fitted to the current model's errors, increasing their score. A low learning rate with many trees can improve generalisation, but without early stopping it can eventually overfit.

## Key terms & formulas

- **kNN:** \(k\)-nearest-neighbour classifier.
- **Naive Bayes:** conditional-independence probabilistic classifier.
- **Logistic regression:** linear log-odds model.
- **Gini impurity:** \(G=1-\sum_k p_k^2\).
- **Entropy:** \(H=-\sum_kp_k\log p_k\).
- **SVM:** maximum-margin classifier.
- **Margin:** distance between a separator and nearest support vectors.
- **Kernel:** similarity function used by an SVM or other method.
- **Random forest:** bagged ensemble of randomized trees.
- **Boosting:** sequential ensemble correcting prior errors.
- **Out-of-bag estimate:** validation using samples not in a tree's bootstrap sample.
- **Softmax:** normalised multiclass scores.
- **Hyper-parameter:** setting such as \(k,C\), depth, or learning rate.
- **Calibration:** quality of predicted probabilities.

## Common mistakes

1. **Using kNN on unscaled features.** Large units dominate distance.
2. **Treating Naive Bayes independence as true.** It is an approximation.
3. **Saying logistic regression predicts a hard label only.** It can produce probabilities.
4. **Using unlimited tree depth.** A fully grown tree may memorise noise.
5. **Ignoring SVM scaling and \(C\).** The result can be highly sensitive.
6. **Calling random-forest probabilities perfectly calibrated.** Evaluate and calibrate when needed.
7. **Using a neural network without enough data or tuning.** Simpler models may generalise better.
8. **Evaluating many algorithms on the test set.** Keep a final honest estimate.

## Exam prep

### Likely 2-mark questions

- **Name four common classification algorithms.** kNN, Naive Bayes, logistic regression, decision tree, SVM, random forest, boosting, or neural network.
- **State the kNN prediction rule.** Use the majority/weighted vote of the \(k\) nearest labelled examples.
- **What is the main idea of an SVM?** Find a separator with a large margin, using a kernel for nonlinear cases.
- **What does boosting do?** Add learners sequentially to correct previous errors.

### Long-answer prompts

- **Compare kNN, Naive Bayes, logistic regression, and SVM.** Discuss decision geometry, assumptions, scaling, interpretability, and data size.
- **Explain decision trees and random forests.** Cover splitting criteria, overfitting, pruning, bagging, and stability.
- **Compare random forests with gradient boosting.** Discuss construction, bias/variance, tuning, interpretability, and use cases.
- **How would you select a classifier for an imbalanced data set?** Use a baseline, class weights/resampling, suitable metrics, calibration, error analysis, and validation.
