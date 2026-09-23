---
subject: ml
unit: 2
topic: model-representation-and-interpretability
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Model Representation and Interpretability

## Overview

A model representation is the form in which a learning method expresses its solution: a set of weights, a tree, a set of rules, a probability distribution, or a network of activations. A representation makes some patterns easy to learn and others difficult. Interpretability asks how well a person can understand why a model produced an output and how that understanding can be checked.

Accuracy and interpretability are related but not identical. A simple model may be understandable but inaccurate; a complex model may be accurate but opaque. The right representation depends on the audience, task, and consequences. Interpretability is useful for debugging, scientific insight, user trust, and contestability, but an explanation is not automatically a causal reason.

## Explanation

### Linear representations

In linear regression,

\[
\hat y=w_0+w_1x_1+\cdots+w_dx_d,
\]

each coefficient gives the change in prediction associated with a one-unit change in one feature while other features are held fixed. The interpretation is local to the model and depends on feature scaling, interactions, and omitted variables. In logistic regression,

\[
p(y=1\mid x)=\sigma(w_0+w^\top x),
\]

where the log-odds are \(w_0+w^\top x\). Coefficients are easier to inspect but may be unstable under correlated features. Regularisation can make a model sparse and easier to read.

### Tree representations

A decision tree partitions the feature space with questions such as “income > 50,000?” and leaves store a class or numeric prediction. A path such as `income > 50,000 → age < 30 → predict yes` explains one decision. Trees handle mixed feature types and nonlinear interactions, but can be unstable: a small data change can produce a different tree. Limiting depth, using many trees, and validating stability help.

### Rule-list and prototype representations

A rule list states conclusions of the form

\[
\text{IF condition}_1\text{ AND condition}_2\text{ THEN outcome},
\]

with ordered rules. Prototypes or nearest-neighbour examples show cases similar to a prediction. These can be easy to communicate, but rules may be too rigid and prototypes may expose sensitive training data.

### Ensemble representations

Random forests and gradient boosting aggregate many trees. An individual tree may be understandable, but the ensemble is a complex function of trees. Feature importance, permutation importance, SHAP values, or surrogate trees can summarise behaviour. None should be called “the reason” without understanding its assumptions.

### Neural representations

A neural network distributes a prediction across layers of weights and nonlinear activations. Individual weights usually do not have a simple semantic meaning. Explanation may use input gradients, saliency, integrated gradients, attention, concept-based tests, or local surrogate models. Explanation methods can be unstable and sensitive to baseline, normalisation, and perturbation.

### Global versus local explanation

**Global** explanation describes overall model behaviour, such as average feature importance or partial dependence. **Local** explanation describes one prediction, such as feature contributions for a particular loan decision. A user asking “why was this application rejected?” needs a local explanation; a regulator asking “what does the model generally do?” needs global evidence.

### Partial dependence and individual curves

Partial dependence approximates the average relationship between feature \(x_j\) and prediction:

\[
PD_j(x_j)=E_{X_{-j}}[\hat f(x_j,X_{-j})].
\]

It can reveal nonlinear trends but averages over other features and can be misleading with strong correlations. Individual conditional expectation (ICE) shows the relationship for each observation and often reveals heterogeneity hidden by the average.

### Feature importance

Permutation importance measures the increase in validation loss when a feature is shuffled. It is model- and protocol-dependent, especially with correlated features. Impurity-based tree importance may favour continuous or high-cardinality features. Use importance for diagnosis and comparison, not as proof of causation.

### Explanation and trust

An explanation can increase understanding but also create false confidence if it omits uncertainty, counterfactuals, data quality, or the model's limitations. For high-stakes decisions, combine an explanation with confidence, uncertainty, data provenance, recourse, and a human review route. Users should be told what the model can and cannot do.

### Choosing a representation

Choose based on the data and constraints:

- sparse, interpretable linear models for tabular data with explainability needs;
- shallow trees for transparent nonlinear decisions;
- ensembles for strong tabular prediction when interpretability can be supported;
- neural networks for high-dimensional raw modalities and sufficient data/compute;
- probabilistic models when uncertainty and dependencies matter.

Interpretability should be evaluated with real users or domain experts, not just assumed from a plot.

## Worked examples

### Example 1: linear coefficient

A model predicts risk as \(\hat y=-2+0.8\,\text{age}+0.5\,\text{score}\). Holding score fixed, a one-year increase in age raises predicted risk by 0.8 units. This is an association in the model, not proof that age causes risk; the coefficient may absorb confounding and depends on the data and scale.

### Example 2: tree path

A tree asks whether monthly payment is above ₹10,000, then whether the account is more than 12 months old, and predicts a class. The path is a faithful model explanation, but the tree can change when retrained. Stability and validation are still needed.

### Example 3: local image explanation

A classifier labels an image “cat.” A saliency map highlights pixels that most affect the score. It can help a developer find a background artefact, but the map is not a human explanation of the cat and may change with the method.

### Example 4: partial dependence

A tree model plots average predicted price across area values, holding other features at their observed combinations. The curve may be flat in unrealistic combinations if features are correlated. ICE plots or a carefully chosen subgroup analysis can reveal more detail.

## Key terms & formulas

- **Representation:** form of a model's learned function, such as coefficients, tree, rules, or network.
- **Interpretability:** extent to which behaviour can be understood and explained.
- **Global explanation:** explanation of overall model behaviour.
- **Local explanation:** explanation of a particular prediction.
- **Coefficient:** parameter describing change in a linear prediction.
- **Log-odds:** \(\log\frac{p}{1-p}\).
- **Tree path:** sequence of splits leading to a leaf.
- **Permutation importance:** validation degradation after shuffling a feature.
- **Partial dependence:**
  \[
  PD_j(x_j)=E_{X_{-j}}[\hat f(x_j,X_{-j})].
  \]
- **ICE:** prediction curve for an individual observation as one feature varies.
- **Surrogate model:** simpler model fitted to approximate another model's predictions.
- **SHAP value:** additive feature contribution under a chosen cooperative-game framework.
- **Saliency:** map of input sensitivity.
- **Counterfactual:** smallest meaningful change that would change a prediction.

## Common mistakes

1. **Calling a coefficient a causal effect.** It describes a fitted predictive relationship.
2. **Treating feature importance as proof of importance in the real world.** Correlation, preprocessing, and sampling affect it.
3. **Using a single local explanation for a global conclusion.** Many local behaviours can differ.
4. **Ignoring correlated features in importance or partial dependence.** Shared information can make the explanation misleading.
5. **Assuming attention is an explanation.** Attention weights may not represent causal importance.
6. **Promising explanations without exposing uncertainty.** A plausible reason is not a guarantee.
7. **Selecting a complex model when a transparent one is sufficient.** Simplicity improves auditability and maintenance.

## Exam prep

### Likely 2-mark questions

- **What is a model representation?** The structure used to express the learned function, such as coefficients, a tree, or neural network.
- **Distinguish global and local interpretability.** Global describes overall behaviour; local explains one prediction.
- **Define a decision-tree path.** The sequence of splits and leaf used for a case.
- **What is permutation importance?** The increase in validation error when a feature's values are shuffled.

### Long-answer prompts

- **Compare linear, tree, ensemble, and neural representations.** Discuss interpretability, flexibility, data needs, and stability.
- **Explain global and local methods for interpreting a classifier.** Use a concrete example and state limitations.
- **Why are feature-importance methods potentially misleading?** Discuss correlation, data distribution, model choice, and causal versus predictive meaning.
- **How would you make a high-stakes ML decision more interpretable?** Discuss representation, local/global explanations, uncertainty, recourse, and human review.
