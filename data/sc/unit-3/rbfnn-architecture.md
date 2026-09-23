---
subject: sc
unit: 3
topic: rbfnn-architecture
syllabus_ref: CSM3202 Unit-III
status: draft
---
# Architecture of an RBFNN

## Overview

The architecture of a radial basis function neural network is defined by input features, a set of hidden centers and widths, and output weights. Each hidden unit computes the similarity of an input to one center. The output layer combines these similarities into a prediction.

The key design decision is how many centers to use and where to place them. The rest of the network is often a linear output layer, which can be solved by least squares after the hidden responses are fixed.

## Explanation

### 1. Network layers

For an input vector

\[
\mathbf x\in\mathbb R^d,
\]

the architecture has three layers.

#### Input layer

It stores or receives the \(d\) input features. It usually has no learned activation.

#### Hidden layer

It contains \(H\) radial basis units:

\[
h_i(\mathbf x)=\phi_i(\|\mathbf x-\mathbf c_i\|),
\qquad i=1,\ldots,H.
\]

Each unit has a center \(\mathbf c_i\in\mathbb R^d\) and a width parameter, often \(\sigma_i\).

#### Output layer

For scalar output,

\[
\hat y=w_0+\sum_{i=1}^{H}w_ih_i.
\]

For \(K\) outputs,

\[
\hat{\mathbf y}=\mathbf W\mathbf h+\mathbf b.
\]

A direct input-output term may be included when the target has a strong linear trend.

### 2. Gaussian hidden unit

The common Gaussian unit is

\[
h_i(\mathbf x)
=
\exp\left[
-\frac{\|\mathbf x-\mathbf c_i\|^2}{2\sigma_i^2}
\right].
\]

Its maximum is 1 at \(\mathbf x=\mathbf c_i\), and it falls toward zero as distance increases. The denominator \(2\sigma^2\) controls smoothness and local versus broad response.

If the squared Euclidean distance is

\[
d_i^2=\sum_{j=1}^{d}(x_j-c_{ij})^2,
\]

then

\[
h_i=e^{-d_i^2/(2\sigma_i^2)}.
\]

### 3. Other radial basis functions

#### Multiquadric

\[
h_i(\mathbf x)=\sqrt{\|\mathbf x-\mathbf c_i\|^2+\sigma_i^2}.
\]

It has a nonzero value even at the center and grows with distance.

#### Inverse multiquadric

\[
h_i(\mathbf x)=\frac{1}{\sqrt{\|\mathbf x-\mathbf c_i\|^2+\sigma_i^2}}.
\]

It decreases with distance but is never zero.

#### Thin-plate spline

\[
h_i(\mathbf x)
=\|\mathbf x-\mathbf c_i\|^2
\log\|\mathbf x-\mathbf c_i\|.
\]

It is used for smooth interpolation and has a different shape near the center.

#### Compact-support basis

A spherical basis can be exactly zero beyond a chosen radius. This reduces computation and can improve locality.

### 4. Width parameter

For Gaussian units:

- small \(\sigma_i\): only inputs very near \(\mathbf c_i\) activate the unit;
- large \(\sigma_i\): many inputs activate the unit;
- a single global \(\sigma\): simpler but may not fit unevenly distributed data;
- a separate \(\sigma_i\): more flexible but has more parameters.

The width should be considered together with center density. Many widely spaced centers with broad widths may produce an ill-conditioned design matrix.

### 5. Normalized output

A single output can be written as

\[
\hat y=\mathbf w^{\mathsf T}\mathbf h.
\]

For multiple outputs,

\[
\hat{\mathbf Y}=\mathbf H\mathbf W^{\mathsf T},
\]

where \(\mathbf H\) has one hidden row per sample and \(\mathbf W\) has one column per output.

A bias can be represented either by an extra hidden unit with activation 1 or by a separate bias term.

### 6. Direct linear component

An expanded RBF architecture is

\[
\hat y
=w_0+\mathbf a^{\mathsf T}\mathbf x
+\mathbf w^{\mathsf T}\mathbf h(\mathbf x).
\]

The linear component captures a trend that the localized RBF units might otherwise approximate inefficiently. It is especially useful for interpolation and regression.

### 7. Number of hidden units

If there are \(H\) centers, the model has approximately

\[
dH+H+1
\]

parameters for one output: \(dH\) center coordinates, \(H\) widths, and \(H+1\) output parameters. If centers are fixed data samples, only the output layer is learned.

Too few centers produce an overly smooth or biased model. Too many can fit noise and create many nearly redundant units. Select \(H\) using validation or a regularization method.

### 8. Center placement

Centers should represent regions where the target changes. Good methods include:

- k-means clustering of training inputs;
- choosing representative samples by farthest-point selection;
- random subsampling for a large data set;
- self-organizing maps;
- fuzzy clustering;
- greedy selection based on approximation error.

A center need not correspond exactly to a labeled class; it is a location in input space.

### 9. Feature scaling

Euclidean distance is sensitive to units. If one feature ranges from 0 to 1 and another from 0 to 10,000, the second feature dominates unless the data are normalized. Standardize or otherwise scale features before center selection and training.

The same scaling must be used for new inputs at prediction time.

### 10. Classification architecture

For \(K\) classes, use \(K\) output units:

\[
\hat y_k=\mathbf w_k^{\mathsf T}\mathbf h.
\]

The class prediction may be

\[
k^*=\arg\max_k\hat y_k.
\]

If probabilities are needed, a softmax or a separate probabilistic calibration model can be applied. The raw RBF scores are not automatically calibrated probabilities.

### 11. Regression architecture

For continuous targets, a linear output is natural:

\[
\hat y=\mathbf w^{\mathsf T}\mathbf h.
\]

Training minimizes squared error. A second output can be a variance estimate, but a basic RBF regression network does not automatically provide reliable uncertainty.

### 12. Regularization and conditioning

The hidden design matrix

\[
\Phi_{ni}=h_i(\mathbf x_n)
\]

may be ill-conditioned when centers are very close or widths are poorly chosen. Ridge regularization:

\[
\min_{\mathbf w}\|\Phi\mathbf w-\mathbf y\|^2+\lambda\|\mathbf w\|^2
\]

improves stability and smooths the fitted function.

If the number of centers is large, use a subset, regularize, or solve iteratively instead of forming a huge inverse.

### 13. Local versus global basis functions

Gaussian RBF functions are global in the mathematical sense because they are nonzero everywhere, but they respond strongly only near their centers. A compact-support basis has true local support. This distinction matters for approximation cost and numerical behavior.

### 14. Architectural choices to record

An RBF implementation should document:

- input features and scaling;
- distance measure;
- basis-function type;
- center-selection method;
- number of centers;
- width rule;
- output bias and direct linear term;
- regularization;
- output transformation for classification.

Without these details, an “RBF network” result is not reproducible.

## Worked examples

### Example 1: Architecture count

Inputs have \(d=3\) features. There are \(H=8\) Gaussian hidden units and one scalar output. The learned parameters, including centers and one width per unit, are

\[
dH+H+H+1=3(8)+8+8+1=41.
\]

If centers are selected from data and fixed, only output weights and bias are learned, giving \(8+1=9\) trainable output parameters.

### Example 2: Compute a hidden response

Let

\[
\mathbf x=(0,2),\quad
\mathbf c=(1,0),\quad\sigma=2.
\]

Distance squared:

\[
d^2=(0-1)^2+(2-0)^2=5.
\]

Activation:

\[
h=\exp(-5/8)=0.5353.
\]

### Example 3: Compare a global and compact basis

For distance \(d=1\) and \(\sigma=1\):

\[
h_{\text{Gaussian}}=e^{-1/2}\approx0.6065.
\]

A spherical basis with support radius 1 is also active but goes to zero beyond the support. The output layer must be trained with the selected basis, not with an assumed Gaussian.

### Example 4: Classification output scores

Suppose three class output weights produce

\[
(\hat y_1,\hat y_2,\hat y_3)=(0.2,-0.4,0.6).
\]

An argmax classifier predicts class 3. These are scores, not probabilities. Applying softmax would produce normalized values, but it changes the loss and calibration and must be specified during training.

## Key terms & formulas

- **Center \(\mathbf c_i\):** Prototype location of hidden unit \(i\).
- **Width \(\sigma_i\):** Radial scale.
- **Hidden response:** \(h_i(\mathbf x)=\phi(d(\mathbf x,\mathbf c_i))\).
- **Design matrix:** \(\Phi_{ni}=h_i(\mathbf x_n)\).
- **Output weights:** Linear combination coefficients.
- **Direct term:** Optional linear input-to-output connection.
- **Conditioning:** Sensitivity of the design matrix to small changes.

Gaussian:

\[
h_i(\mathbf x)=\exp\left[-\frac{\|\mathbf x-\mathbf c_i\|^2}{2\sigma_i^2}\right].
\]

Output:

\[
\hat y=w_0+\sum_iw_ih_i.
\]

Ridge normal equations:

\[
(\Phi^{\mathsf T}\Phi+\lambda I)\mathbf w
=\Phi^{\mathsf T}\mathbf y.
\]

## Common mistakes

1. **Counting hidden units but forgetting their centers and widths.** They are learned or selected parameters.
2. **Using unscaled features.** Distances become meaningless across mixed units.
3. **Adding a bias but not documenting it.** It can be an extra unit or a separate parameter.
4. **Assuming all RBF networks use Gaussian functions.** Other bases exist and change training behavior.
5. **Interpreting class scores as probabilities.** Calibration is separate.
6. **Using a direct input term without saying so.** It changes the model capacity.
7. **Forming a large inverse without conditioning checks.** Use regularization or a stable solver.
8. **Forgetting feature scaling at prediction time.** Training and deployment preprocessing must match.

## Exam prep

### Likely 2-mark questions

- **Draw an RBFNN architecture.**  
  **Hint:** Input, radial hidden units with centers/widths, and weighted output layer.

- **Write the output equation of a scalar RBF network.**  
  **Hint:** \(w_0+\sum_iw_ih_i(\mathbf x)\).

- **What is the role of a center?**  
  **Hint:** It is the prototype location at which its radial unit responds maximally.

- **What is the effect of a small Gaussian width?**  
  **Hint:** A narrower, more local response.

- **Why is bias often included in the output layer?**  
  **Hint:** To represent a constant offset and complete a flexible linear model.

### Likely long-answer questions

- **Explain the architecture of an RBF neural network in detail.**  
  **Hint:** Layers, distance, basis functions, widths, output, classification/regression forms.

- **Compare Gaussian, multiquadric, inverse-multiquadric, and thin-plate functions.**  
  **Hint:** Formula, behavior at center, tail, smoothness, and use.

- **Explain how hidden-unit count and center placement affect an RBFNN.**  
  **Hint:** Capacity, local detail, overfitting, conditioning, and selection methods.

- **Discuss feature scaling and regularization in RBF networks.**  
  **Hint:** Distance units, validation scaling, ridge objective, and numerical stability.
