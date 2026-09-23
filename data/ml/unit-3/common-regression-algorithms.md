---
subject: ml
unit: 3
topic: common-regression-algorithms
syllabus_ref: CSM3201 Unit-III
status: draft
---
# Common Regression Algorithms

## Overview

Regression algorithms estimate a continuous target from input features. Common choices range from linear and regularised models to k-nearest neighbours, decision trees, support-vector regression, random forests, gradient boosting, and neural networks. Each method encodes different assumptions about the relationship between features and target.

The right choice depends on data size and type, relationship shape, noise, need for extrapolation, interpretability, latency, and error cost. Start with a mean baseline and a simple linear model, then add complexity only when validation and error analysis justify it.

## Explanation

### Linear regression

Linear regression predicts

\[
\hat y=w_0+w^\top x.
\]

It is fast, interpretable, and works well when the relationship is approximately linear or when features already encode nonlinear structure. It can extrapolate mathematically but may extrapolate badly. Ordinary least squares is sensitive to outliers and multicollinearity; Ridge, LASSO, and Elastic Net add stability or sparsity.

### Polynomial regression

Polynomial features extend \(x\) with powers or interactions:

\[
\hat y=w_0+w_1x+w_2x^2+\cdots+w_px^p.
\]

They can model curvature but increase dimensionality and can oscillate badly outside the observed range. Use regularisation and validate the degree. Splines and basis expansions are often safer than unrestricted high-degree polynomials.

### k-nearest-neighbour regression

kNN predicts the mean or weighted mean target of nearby points:

\[
\hat y(x)=\frac{1}{k}\sum_{i\in N_k(x)}y_i.
\]

It makes few distribution assumptions and works well for smooth local relationships with enough data. It is expensive at prediction, sensitive to scaling and irrelevant dimensions, and weak with high-dimensional sparse features. Standardise before distance calculations.

### Decision-tree regression

A tree recursively splits features and stores a target statistic, often the mean, in leaves. It captures nonlinearity, thresholds, and interactions without scaling. It can overfit, be unstable, and cannot extrapolate beyond leaf values. Limit depth, set a minimum leaf size, or use an ensemble.

### Random forest regression

A random forest averages many trees trained on bootstrap samples and random feature subsets. Averaging reduces variance and handles nonlinear tabular data well. It may be less interpretable, can be slow for large data, and usually predicts within the range of observed targets. Out-of-bag scores and feature importance can help analysis.

### Gradient-boosted regression trees

Boosting adds shallow trees sequentially to reduce the current model's error:

\[
F_m(x)=F_{m-1}(x)+\eta h_m(x).
\]

It is often highly accurate for tabular data and can model interactions. It needs careful learning-rate, depth, and early-stopping choices; excessive boosting can overfit. SHAP values or permutation importance can support interpretation.

### Support-vector regression

SVR seeks a function within an \(\epsilon\)-tube of the target, penalising points outside it:

\[
\min_{f,w,b,\xi}\frac12\|w\|^2+C\sum_i(\xi_i+\xi_i^*),
\]

with a kernel for nonlinear functions. It can work well in moderate dimensions and is robust to some outliers, but kernel computation and parameter selection can be costly. Scale features and tune \(C,\epsilon,\) and kernel type.

### Regularised linear models

Ridge minimises squared error plus an \(L_2\) penalty; LASSO adds an \(L_1\) penalty; Elastic Net combines them. Regularisation reduces variance, handles correlated predictors, and can select features. It shrinks coefficients and may introduce bias, so evaluate prediction and interpretability on validation data.

### Neural regression

A neural network maps \(x\) through nonlinear layers to \(\hat y\). It can learn complex interactions in large data and can share representations across related targets. It requires careful normalisation, optimisation, regularisation, and uncertainty estimation. It can fit a nonlinear trend but still fail under extrapolation or distribution shift.

### Bayesian and probabilistic regression

Bayesian methods specify a prior and likelihood, then obtain a posterior over parameters or predictions. They can express uncertainty and incorporate prior knowledge, but computation and modelling assumptions may be demanding. Probabilistic outputs are useful when decisions depend on uncertainty, provided calibration is checked.

### Selecting and improving a regressor

A practical regressor selection starts with a target distribution and a baseline. Plot the target, inspect missingness and outliers, and decide whether the task is to predict a mean, median, quantile, or count. Then compare models with the same chronological or group-aware split. A more flexible model should be justified by a repeatable validation improvement, not by a more complicated name.

- If a straight line fits well and extrapolation is required, linear or regularised linear regression is transparent and stable.
- If a smooth curve is visible, a spline or low-degree polynomial may help, but predictions outside the observed range need caution.
- If local neighbourhoods are meaningful, kNN can work, although it is costly at prediction time and sensitive to scaling.
- If thresholds, missing paths, and interactions drive the outcome, a decision tree may be easier to inspect than a black-box model.
- If tabular prediction accuracy and nonlinear interactions are the priority, random forests or gradient boosting are strong candidates.
- If uncertainty or raw sequences are central, a probabilistic model, recurrent model, or carefully designed Bayesian/quantile approach may be preferable.

Regularisation is often the first improvement to try when coefficients are unstable. Select \(\lambda\) using validation folds and report both prediction error and how the model changes. For tree ensembles, early stopping is the usual capacity control. For neural regression, monitor both the loss and calibration/interval quality; a lower training loss is not enough.

Residual analysis should guide the next model choice. A curved residual plot may justify nonlinear features; a fan-shaped pattern may justify a variance model or weighted loss; group-specific residuals may justify a hierarchical or subgroup-aware approach. Do not add a complex model merely to conceal systematic errors in the target or data pipeline.

## Worked examples

### Example 1: linear versus polynomial

A plot of demand versus temperature curves upward. A linear model misses the middle or edges. A quadratic or spline may fit validation data better, but high-degree polynomials can oscillate. Compare with a tree and check the physical range before extrapolating.

### Example 2: kNN regression

For a house, the five nearest comparable properties have prices 80, 85, 90, 95, and 100 lakh. The mean prediction is 90 lakh. A weighted average can favour closer properties. Standardising area and distance features is essential.

### Example 3: ridge regression

Two features, height and weight, are strongly correlated in training data. OLS coefficients swing when a few points change. Ridge stabilises them and may improve test RMSE. The penalty strength is selected on validation folds, not by inspecting the final test score.

### Example 4: boosting early stopping

Validation RMSE decreases for 80 boosting rounds and rises afterwards. Save the checkpoint at the minimum rather than training until the default number of rounds. The stopping point is an important model parameter.

## Key terms & formulas

- **Linear regression:** \(\hat y=w_0+w^\top x\).
- **Polynomial regression:** polynomial basis expansion of features.
- **kNN regression:** average target of nearby observations.
- **Regression tree:** leaves store numeric target summaries.
- **Random forest:** averaged bootstrap tree ensemble.
- **Gradient boosting:** sequential ensemble correcting residuals.
- **SVR:** kernel support-vector regression with an \(\epsilon\)-tube.
- **Ridge:** squared loss plus \(L_2\) penalty.
- **LASSO:** squared/other loss plus \(L_1\) penalty.
- **Elastic Net:** combination of \(L_1\) and \(L_2\) penalties.
- **Bayesian regression:** posterior distribution over model parameters.
- **Inductive bias:** assumptions a method makes about the target function.
- **Hyper-parameter:** setting such as \(k\), depth, \(C\), or \(\lambda\).
- **Extrapolation:** prediction outside observed feature/target ranges.
- **Prediction interval:** range for a future target value.

## Common mistakes

1. **Using a complex method without a linear baseline.** Extra complexity may not improve validation.
2. **Using high-degree polynomial extrapolation.** Oscillations can make predictions nonsensical.
3. **Applying kNN to unscaled features.** Distance is dominated by large units.
4. **Confusing tree leaf averages with continuous extrapolation.** Trees are piecewise constant.
5. **Ignoring outliers in OLS.** A robust loss or transformation may be more appropriate.
6. **Tuning regularisation on test data.** The estimate becomes optimistic.
7. **Reporting a point prediction without uncertainty.** Users may overtrust it.
8. **Assuming feature importance is causal.** It describes model behaviour under the fitted data.

## Exam prep

### Likely 2-mark questions

- **Name four regression algorithms.** Linear, polynomial, kNN, tree, random forest, boosting, SVR, or neural regression.
- **What is the main advantage of linear regression?** Simple, fast, interpretable, and a strong baseline.
- **State the ridge penalty.** \(\lambda\|w\|_2^2\).
- **Why can trees fail at extrapolation?** Their leaves store observed target summaries and do not extend beyond them.

### Long-answer prompts

- **Compare linear, tree, ensemble, and neural regression methods.** Discuss assumptions, data needs, extrapolation, and interpretability.
- **Explain regularised regression.** Derive/describe ridge and LASSO objectives, shrinkage, sparsity, and validation of \(\lambda\).
- **How would you choose a regressor for a tabular data set?** Establish a baseline, consider data shape and requirements, tune candidates, inspect residuals, and validate.
- **Explain why uncertainty matters in regression.** Discuss conditional mean, noise, intervals, heteroscedasticity, calibration, and distribution shift.
