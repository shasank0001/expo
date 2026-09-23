---
subject: ml
unit: 2
topic: selecting-a-model
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Selecting a Model

## Overview

Model selection chooses a learning method, representation, and set of hyper-parameters that are appropriate for the data, objective, and deployment constraints. There is no universally best algorithm. A simple model may be more accurate, safer, faster, or more explainable than a sophisticated one on a particular problem.

Selection should be evidence-based. Begin with the task and a baseline, state what “good” means, evaluate candidates under the same honest protocol, and consider the consequences of errors. The final choice is often a trade-off rather than the single highest score.

## Explanation

### Start from requirements

List requirements before comparing algorithms:

- task type and target type;
- sample size, feature types, and expected missingness;
- accuracy requirement and relative costs of errors;
- latency, memory, energy, and hardware limits;
- interpretability and explanation obligations;
- privacy, fairness, and regulatory constraints;
- ability to update and monitor after deployment.

A model that is slightly better offline but too slow, opaque, or unfair may be rejected.

### Use a baseline

A baseline gives a meaningful reference. For classification it may predict the majority class or a simple rule. For regression it may use the training mean or median. A simple linear model, small tree, or nearest-centroid method can reveal whether complex features add value. A large improvement over a baseline is more persuasive than a small difference between two expensive models.

### Match inductive bias to the data

- **Linear models** assume a linear relationship in the chosen features; they are strong baselines and interpretable.
- **Decision trees** make few assumptions about scale and can capture interactions and thresholds, but may overfit.
- **Ensembles** such as random forests or gradient boosting combine many trees; they are often strong on tabular data but less interpretable.
- **Support-vector machines** work well in moderate-dimensional settings with effective kernels and scaling.
- **Nearest neighbours** are simple and non-parametric but can be expensive at prediction time and sensitive to distance.
- **Probabilistic models** represent uncertainty and dependencies but may require assumptions or computation.
- **Neural networks and deep learning** learn rich representations from raw or large data but need more data, compute, tuning, and monitoring.
- **Gaussian processes** are useful for small data and calibrated uncertainty but scale poorly with many inputs.

The data, not the popularity of a method, should guide the initial candidates.

### Hyper-parameters and tuning

Hyper-parameters control a learning process rather than being directly estimated from ordinary training examples. Examples include tree depth, learning rate, number of neighbours, regularisation strength, kernel, and batch size. Use a validation set or cross-validation, define the search space, and record the budget. Grid search is easy to explain; random search explores high-dimensional spaces efficiently; Bayesian optimisation can be useful when evaluations are expensive.

Tuning must not use the final test set. If the same validation set is used for hundreds of choices, its score becomes optimistically selected. A nested or held-out design may be appropriate for a small data set.

### Metrics and decision curves

For classification, accuracy may be enough when classes and costs are balanced. Otherwise consider precision, recall, F1, PR-AUC, ROC-AUC, calibration, and cost-weighted metrics. For regression, MAE is robust to outliers, RMSE penalises large errors, and \(R^2\) describes variance explained relative to a baseline. A threshold can be selected on validation data using a business cost curve.

Compare not only the point estimate but uncertainty and stability across folds, seeds, and time periods. A model with a lower mean score but high variance may be unsuitable for a regulated workflow.

### Complexity and deployment

More parameters and flexible representations can fit complex patterns but increase overfitting, memory, latency, energy use, and maintenance. A linear model can be served easily; a large neural network may require accelerators and a fallback. A tree ensemble may need periodic retraining when features change. Include monitoring and rollback in the selection decision.

### Interpretability and fairness constraints

If a regulator or user needs reasons, a sparse linear model, small tree, rule list, or carefully designed surrogate may be preferable. Interpretability does not guarantee fairness; a simple model can encode a discriminatory proxy. Evaluate subgroup performance and calibration regardless of model family.

### Model selection is iterative

The best model may become obsolete after error analysis, new data, or a changed objective. Keep a model registry and a challenger model. A champion model should not be replaced only because a challenger has a marginally higher average score.

## Worked examples

### Example 1: tabular classification

For 50,000 rows and 20 mixed features, compare a majority baseline, logistic regression with one-hot encoding, a random forest, and gradient-boosted trees. Use stratified cross-validation, tune regularisation/depth, and evaluate minority recall and calibration. The boosted model may win on AUC, but a simpler model wins if it meets the latency and explanation requirements.

### Example 2: small data and text

With 300 labelled documents, a pretrained representation plus a regularised linear classifier may outperform a neural network trained from scratch. Compare calibration and external validation. More layers are not automatically justified by the amount of labelled data.

### Example 3: regression trade-off

Two models predict delivery time. Model A has MAE 4 minutes and RMSE 9; Model B has MAE 5 and RMSE 6. A service that values every average minute may prefer B, while a risk-sensitive operation concerned with catastrophic delays may prefer A. The choice follows the loss and decision.

### Example 4: threshold selection

A classifier's validation probabilities range from 0.05 to 0.95. The team plots expected cost for a threshold, chooses one using validation data, and reports the corresponding precision/recall. It does not tune the threshold on the test set or assume 0.5 is universally correct.

## Key terms & formulas

- **Model selection:** choosing an algorithm, representation, and hyper-parameters.
- **Inductive bias:** assumptions or preferences favouring certain solutions.
- **Baseline:** simple reference method.
- **Hyper-parameter:** setting controlling a learning process.
- **Hyper-parameter tuning:** choosing these settings by validation evidence.
- **Cross-validation:** repeated train/validation partitions.
- **Grid search:** testing combinations from a predefined grid.
- **Random search:** sampling hyper-parameter combinations.
- **Bayesian optimisation:** using a surrogate model to choose promising trials.
- **Model complexity:** capacity and resource demands of a method.
- **Calibration:** agreement between predicted probabilities and outcomes.
- **Champion–challenger:** deployed model compared with a candidate.
- **Selection bias:** choosing a model because of a noisy or reused evaluation.
- **Cost-sensitive learning:** assigning different costs to different errors.

## Common mistakes

1. **Choosing the most complex method first.** A baseline reveals whether complexity is needed.
2. **Using the test set for tuning.** The final estimate is contaminated.
3. **Comparing models with different preprocessing or splits.** The comparison is invalid.
4. **Choosing solely by accuracy.** Consider cost, calibration, fairness, latency, and explainability.
5. **Ignoring uncertainty.** A small score difference may be noise.
6. **Selecting for the leaderboard rather than the deployment population.** External validity matters.
7. **Forgetting maintainability.** A model that cannot be updated or explained may be unusable.

## Exam prep

### Likely 2-mark questions

- **What is model selection?** Choosing an algorithm and its settings using data and requirements.
- **Why establish a baseline?** To measure the value added by a more complex model.
- **Give one hyper-parameter of a decision tree.** Maximum depth, minimum samples per leaf, or number of trees.
- **What is inductive bias?** Assumptions that make an algorithm favour certain solutions.

### Long-answer prompts

- **Explain a principled model-selection process.** Include requirements, baseline, candidates, preprocessing, tuning, metrics, uncertainty, and deployment.
- **Compare a linear model, tree, and neural network.** Discuss data needs, interpretability, capacity, and use cases.
- **How would you select a model under unequal error costs?** Define costs, choose a cost-sensitive metric or threshold, and validate the business outcome.
- **Why is the test set not used for model selection?** Explain selection bias and the need for an untouched final estimate.
