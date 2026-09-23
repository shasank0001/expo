---
subject: ml
unit: 3
topic: regression-model
syllabus_ref: CSM3201 Unit-III
status: draft
---
# Regression Model

## Overview

A regression model estimates a continuous target as a function of input features. It may predict a conditional mean, a conditional median, or another location of \(Y\) depending on the loss and distribution assumptions. The most familiar example is ordinary least-squares linear regression, but regression includes trees, support-vector regression, ensembles, and neural networks.

A regression model is useful only when its target, features, loss, and uncertainty match the decision. A very precise-looking prediction can still be wrong if it extrapolates, omits important structure, or uses information unavailable at prediction time.

## Explanation

### Linear regression

For \(d\) features,

\[
\hat y=w_0+\sum_{j=1}^{d}w_jx_j.
\]

The design matrix form is \(\hat y=Xw\). Ordinary least squares minimises squared residuals:

\[
\hat w=\arg\min_w\frac{1}{2n}\|Xw-y\|_2^2.
\]

With full rank, the normal equation gives

\[
\hat w=(X^\top X)^{-1}X^\top y.
\]

The fitted line is not guaranteed to represent causation. It is a weighted average of observed relationships under the data and specification.

### Loss functions and estimands

Squared error targets the conditional mean when errors are well modelled:

\[
E[Y\mid x]=x^\top w.
\]

Absolute error can target the conditional median and is robust to outliers:

\[
\min_w\sum_i|y_i-x_i^\top w|.
\]

Huber loss combines smooth quadratic behaviour near zero with a linear penalty for large errors. A weighted loss gives higher influence to important cases. A quantile regression estimates a conditional quantile, useful when uncertainty or risk matters.

### Assumptions and diagnostics

OLS assumptions include a correctly specified mean relationship, independent errors for standard inference, no perfect multicollinearity, and roughly constant error variance for ordinary confidence intervals. For prediction, normality is not always essential, but residual structure and influential points still matter.

- Plot residuals versus fitted values for curvature or changing variance.
- Use Cook's distance or leverage to identify influential observations.
- Check multicollinearity using correlations, condition numbers, or variance-inflation factors.
- Examine nonlinear relationships and consider transformations or flexible models.
- Check whether errors are correlated over time for time series.

### Regularised regression

Ridge regression minimises

\[
\frac{1}{n}\sum_i(y_i-\hat y_i)^2+\lambda\|w\|_2^2,
\]

shrinking coefficients and stabilising correlated predictors. LASSO adds \(\lambda\|w\|_1\), which can set some coefficients exactly to zero. Elastic net combines both penalties. The value of \(\lambda\) is selected using validation data. Regularisation reduces variance but introduces bias.

### Tree and ensemble regression

A regression tree partitions the input space and stores a numeric value, often the mean target, in each leaf. It captures interactions and needs little scaling, but can overfit and predict only values observed in leaves, which makes extrapolation difficult. Random forests average many trees to reduce variance. Gradient boosting sequentially fits trees to residual error and is often strong on tabular data.

### kNN and support-vector regression

kNN predicts the mean (or weighted mean) target of nearby training points. It is non-parametric but can be expensive and sensitive to scaling. SVR uses a margin loss and kernel functions, ignoring errors within a tube and penalising violations outside it. Parameters such as \(C\), \(\epsilon\), and the kernel control the trade-off.

### Neural regression

A neural network maps features through hidden layers to a scalar output. It can model complex nonlinear relationships, but requires data and compute, and can extrapolate unpredictably. Mean-squared or absolute-error objectives, regularisation, early stopping, and uncertainty estimates are important. A neural output is not automatically calibrated.

### Model evaluation

Use MAE for an average absolute interpretation, RMSE for large-error penalties, \(R^2\) relative to a mean baseline, and metrics in the target's units. Evaluate on a representative test set and report uncertainty. Residual plots and subgroup analysis reveal errors that a single average hides.

### Prediction intervals

A regression prediction has uncertainty from the fitted parameters and from new observation noise. Under suitable assumptions, a prediction interval is wider than a confidence interval for the mean because it includes future variation. Tree and neural models need conformal or bootstrap methods for useful intervals. Intervals can be poorly calibrated under distribution shift.

### Generalisation and model selection

A regression model should be judged on the distribution of future cases, not on the equation that fit the historical sample. Compare it with a mean/median baseline and a simple linear model. Use MAE when an average absolute miss is meaningful, RMSE when large misses are especially expensive, and \(R^2\) only with its baseline and limitations. Report the metric in the target's units when communicating to a domain expert.

Check whether the model is being asked to interpolate or extrapolate. A tree is naturally suited to interpolation inside its observed leaves but cannot extend beyond them. A polynomial can fit a curve yet oscillate outside the range. A linear model is easy to extrapolate but may impose a physically impossible trend. Range checks, domain constraints, abstention, and a review path are safer than a confident unsupported number.

A useful model report contains the training objective, the selected loss, the validation protocol, residual plots, subgroup and time checks, and prediction intervals. If the target is heteroscedastic, consider a transformed target, robust or weighted loss, or a model that explicitly represents variance. If errors are correlated over time, a random split and iid regression assumptions are not appropriate.

## Worked examples

### Example 1: intercept and slope

A model fits \( \hat y=10+4x\). At \(x=3\), \(\hat y=22\). If the true value is 25, the residual is 3. The coefficient 4 is an association per unit of \(x\), not a claim that changing \(x\) causes a change of 4.

### Example 2: MAE versus RMSE

Errors are \([-2,2,-2,2]\). MAE is 2 and RMSE is 2. If an error is 20, MAE becomes 5 while RMSE increases much more. The choice depends on whether large misses are especially costly.

### Example 3: tree prediction

A tree splits area at 100 m². Leaves have mean prices 80 and 140 lakh. A 120 m² house is predicted 140, even if its area is 400 in a future case. A tree cannot extrapolate; a linear model can, though its extrapolation may also be unreliable.

### Example 4: ridge shrinkage

Two highly correlated features each have a large positive/negative coefficient in ordinary least squares. Ridge distributes their effect more evenly and reduces sensitivity to small data changes. The prediction may change little even though individual coefficients become less extreme.

## Key terms & formulas

- **Regression model:** \(f(x)\) estimating a continuous target.
- **Ordinary least squares (OLS):** minimises squared residuals.
- **Residual:** \(e_i=y_i-\hat y_i\).
- **MAE:** \(\frac1n\sum_i|e_i|\).
- **RMSE:** \(\sqrt{\frac1n\sum_i e_i^2}\).
- **\(R^2\):** \(1-\sum e_i^2/\sum(y_i-\bar y)^2\).
- **Multicollinearity:** near-linear dependence among predictors.
- **Heteroscedasticity:** non-constant residual variance.
- **Ridge penalty:** \(\lambda\|w\|_2^2\).
- **LASSO penalty:** \(\lambda\|w\|_1\).
- **Quantile regression:** estimates a conditional quantile.
- **Extrapolation:** prediction outside observed input ranges.
- **Leverage/influence:** extent to which an observation affects fitted parameters.
- **Prediction interval:** range intended to cover a future observation.

## Common mistakes

1. **Treating R² as the only performance measure.** It can be high despite a poor or biased application.
2. **Ignoring residual assumptions.** Diagnostics can reveal a misspecified mean or changing variance.
3. **Using OLS when the target has extreme outliers.** Robust or transformed loss may be better.
4. **Selecting the regularisation parameter on test data.** Use validation.
5. **Assuming a tree can extrapolate.** Tree leaves do not extend beyond observed values.
6. **Interpreting a coefficient causally.** It depends on included variables and data generation.
7. **Omitting uncertainty.** A point estimate alone may be overconfident.

## Exam prep

### Likely 2-mark questions

- **Write the linear regression model.** \(\hat y=w_0+\sum_jw_jx_j\).
- **Define MAE and RMSE.** Give formulas and explain their difference.
- **What is multicollinearity?** Near-linear dependence among predictors that destabilises coefficients.
- **What is extrapolation?** Prediction for inputs outside the training range.

### Long-answer prompts

- **Explain ordinary least-squares regression.** Derive the objective, normal equation, assumptions, and diagnostics.
- **Compare MAE, RMSE, and \(R^2\).** Discuss outliers, target units, and interpretation.
- **Explain ridge and LASSO regression.** Compare penalties, shrinkage, sparsity, and validation of \(\lambda\).
- **How would you build a reliable regression model?** Cover target, features, preprocessing, leakage, baselines, validation, residuals, uncertainty, and monitoring.
