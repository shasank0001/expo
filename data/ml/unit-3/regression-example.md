---
subject: ml
unit: 3
topic: regression-example
syllabus_ref: CSM3201 Unit-III
status: draft
---
# Example of Regression

## Overview

Regression predicts a continuous target from input features. A complete example should show more than a formula: it should define the prediction time, prepare a representative data set, fit a model, evaluate unseen errors, diagnose residuals, and explain how a prediction can be used. House-price prediction is a useful classroom example because the target is numeric, the features are intuitive, and mistakes have visible consequences.

The numerical calculations below use a tiny data set so the algebra can be checked by hand. Real projects use many observations, validation folds, uncertainty estimates, and domain checks.

## Explanation

### Problem definition

Suppose a property dataset contains, for each sold house:

- \(x_1\): floor area in square metres;
- \(x_2\): age in years;
- \(y\): sale price in ₹ lakh.

The goal is to estimate price for a house that is on the market now. All features must be known at the valuation time. The target is the price paid, which may itself be noisy because sale price depends on negotiation, location, and market conditions.

### A simple linear model

Let

\[
\hat y=w_0+w_1x_1+w_2x_2.
\]

The model says that, holding age fixed, each additional square metre changes predicted price by \(w_1\); holding area fixed, each additional year changes it by \(w_2\). The intercept is the model's prediction at zero area and zero age, which may not have practical meaning.

### Fitting by least squares

For observations \((x_i,y_i)\), minimise

\[
J(w)=\frac{1}{2n}\sum_{i=1}^{n}(w_0+w^\top x_i-y_i)^2.
\]

The design matrix is \(X\) with a column of ones, so

\[
\hat w=(X^\top X)^{-1}X^\top y
\]

when the inverse is stable. In practice, use a numerically stable solver, regularisation, or gradient descent. Standardising predictors can help optimisation, especially when units differ greatly.

### A two-record calculation

For a simple one-feature model \(\hat y=w_0+w_1x\), suppose the training pairs are \((1,3)\) and \((3,7)\). The least-squares line has slope

\[
w_1=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}
{\sum_i(x_i-\bar x)^2}=2,
\]

and intercept

\[
w_0=\bar y-w_1\bar x=5-2(2)=1.
\]

Thus \(\hat y=1+2x\). At \(x=2\), the prediction is 5. This is a hand illustration, not evidence of generalisation.

### Multiple features and interpretation

Suppose fitted coefficients are \(w_0=20\), \(w_1=1.2\), and \(w_2=-0.8\), with area in m² and age in years. For a 100 m², 10-year-old house,

\[
\hat y=20+1.2(100)-0.8(10)=132
\]

lakh. This is a conditional prediction, not a guaranteed price. If area and location are correlated, coefficients can be unstable even if predictions are good.

### Training and evaluation

A realistic workflow:

1. Split by time or property group, keeping related transactions together.
2. Fit imputation, scaling, encoding, and model on training data only.
3. Compare a mean baseline and a linear model.
4. Tune regularisation and polynomial features on validation data.
5. Evaluate MAE, RMSE, \(R^2\), residuals, and subgroup errors on test data.
6. Check whether errors are larger for expensive houses, new listings, or particular locations.

A model with lower MAE may be preferable if every price error has similar business cost; a model with lower RMSE may be preferable if very expensive mistakes are especially harmful.

### Diagnosing residuals

A residual is

\[
e_i=y_i-\hat y_i.
\]

Plot residuals against fitted values and each feature. A U-shaped residual plot suggests nonlinearity. A fan shape suggests changing variance. Systematic residuals for a location or time period suggest missing structure. A few very large residuals may be unusual but valid properties, or may reveal data errors.

### Uncertainty and intervals

A point estimate \(\hat y(x_0)\) can be accompanied by a prediction interval. The interval should include uncertainty from estimated coefficients, residual noise, and the model's limitations. An algorithm's confidence score is not automatically a calibrated interval. In a real valuation, comparable sales and expert judgement remain important.

### Using the prediction

A price estimate can support ranking or an offer range. It should not automatically set a final price without checking comparable properties, local policy, and uncertainty. The model may be useful for a first-pass triage while a professional reviews edge cases.

### From an example to a reliable study

A classroom regression example can be expanded into a reproducible study by adding uncertainty and comparison. Fit a mean-only baseline, an ordinary least-squares model, a regularised model, and at least one nonlinear candidate. Use the same train/validation split and report MAE, RMSE, and \(R^2\) with uncertainty. Inspect residuals by area, age, location, and time. If the model is intended for individual valuation, evaluate the cost of large percentage errors as well as absolute errors.

For a small hand-calculated data set, the exact least-squares line is useful for learning but has no reliable estimate of generalisation. A real project should preserve the raw data, fit preprocessing within the training fold, log the model version, and test on a later or independent property market. The example should teach the full logic—data, fit, error analysis, uncertainty—not only the normal equation.

## Worked examples

### Example 1: error calculation

Actual price \(y=140\), prediction \(\hat y=132\). The error is \(e=8\) lakh. Squared error is 64; squared error alone is not an intuitive price report, so MAE/RMSE are often used.

### Example 2: weighted loss

If underestimating an expensive house by 20 lakh is twice as costly as overestimating by 10 lakh, use asymmetric or weighted loss and evaluate cost on validation data. The objective must reflect the decision, not only statistical convenience.

### Example 3: extrapolation

The model was trained on areas from 40 to 160 m². Predicting a 400 m² house is extrapolation. A linear equation may produce a precise-looking but unsupported number. The model should flag such cases or use additional data/domain rules.

### Example 4: leakage and time

A feature “final sale price after negotiation” is nearly the target and is unavailable before valuation. Removing it fixes target leakage. A feature “price per square metre in the same month” must be calculated only from transactions known before the prediction date.

## Key terms & formulas

- **Regression:** prediction of a continuous target.
- **Design matrix:** \(X\) containing feature columns and an intercept.
- **Prediction:** \(\hat y=X\hat w\).
- **Residual:** \(e=y-\hat y\).
- **Least-squares objective:**
  \[
  \frac{1}{2n}\|Xw-y\|_2^2.
  \]
- **Normal equation:** \(X^\top Xw=X^\top y\).
- **MAE:** mean absolute error.
- **RMSE:** root mean squared error.
- **\(R^2\):** fraction of variance explained relative to a mean model.
- **Multicollinearity:** strong linear dependence among predictors.
- **Extrapolation:** prediction outside the training feature range.
- **Prediction interval:** range intended to cover future outcomes.
- **Heteroscedasticity:** residual variance changing with the predictor.
- **Baseline:** mean/median or simple domain predictor.

## Common mistakes

1. **Using a random split when sale prices are temporal.** Future market information can leak.
2. **Reporting \(R^2\) without units or MAE.** A high \(R^2\) may hide large errors.
3. **Ignoring residuals.** A good average score can hide nonlinear or biased patterns.
4. **Extrapolating outside the training range.** The model has no evidence there.
5. **Interpreting coefficients causally.** They describe fitted associations.
6. **Using every feature available after the decision.** Target or temporal leakage invalidates the result.
7. **Fitting scaling before splitting.** The preprocessing parameters see future distribution.

## Exam prep

### Likely 2-mark questions

- **Define regression and give one example.** Predicting a continuous value such as house price.
- **What is a residual?** The difference \(y-\hat y\) between observed and predicted target.
- **State the least-squares objective.** \(J(w)=\frac1{2n}\sum_i(w^\top x_i-y_i)^2\).
- **Why examine residual plots?** To detect nonlinearity, changing variance, bias, and outliers.

### Long-answer prompts

- **Solve or explain a simple regression example.** Show model setup, least-squares fitting, prediction, and error calculation.
- **Describe the complete workflow for house-price regression.** Include data leakage, validation, metrics, residual analysis, and uncertainty.
- **Explain multicollinearity and heteroscedasticity.** Give effects on coefficients, predictions, and diagnostics.
- **Why is a regression model not automatically a decision model?** Discuss thresholds, uncertainty, domain constraints, and costs.
