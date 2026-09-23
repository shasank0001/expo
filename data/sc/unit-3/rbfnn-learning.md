---
subject: sc
unit: 3
topic: rbfnn-learning
syllabus_ref: CSM3202 Unit-III
status: draft
---
# Learning of an RBFNN

## Overview

RBFNN learning has two main choices: determine the centers and widths of hidden units, then fit the linear output weights. This staged approach is faster and more stable than jointly optimizing every parameter with ordinary gradient descent. Gradient methods can also learn centers, widths, and output weights, but they need careful initialization and regularization.

The quality of learning depends on center coverage, width selection, data scaling, and the number of hidden units. This note covers common algorithms and complete numerical fitting steps.

## Explanation

### 1. Learning stages

A typical RBF training procedure is:

1. preprocess and scale input features;
2. choose a basis function;
3. select \(H\) centers;
4. choose widths;
5. compute hidden responses for every training sample;
6. solve output weights by least squares or ridge regression;
7. validate and adjust \(H,\sigma,\lambda\).

This is often called **two-stage learning** or **hybrid learning**.

### 2. Center selection methods

#### Every training sample

Set \(\mathbf c_i=\mathbf x_i\). If there are \(N\) samples and one output, the network has \(N\) hidden units. It can interpolate training data exactly under suitable conditions, but it may overfit and use substantial memory.

#### Random subset

Choose a representative subset of samples. Repeat with different seeds or use validation to select the subset size. This is useful for large datasets.

#### K-means

Run k-means with \(H\) clusters and use cluster centroids as centers. This places centers in dense regions and reduces the number of hidden units.

#### Farthest-point selection

Start with one center, then repeatedly add the point farthest from the nearest existing center. This improves coverage but may select outliers, which can be undesirable.

#### Greedy/orthogonal-center selection

Add a candidate sample if its hidden activation reduces the current approximation error. This directly targets the target function but is more computationally demanding.

### 3. Width selection

A single global Gaussian width is often used:

\[
h_{ni}
=
\exp\left[
-\frac{\|\mathbf x_n-\mathbf c_i\|^2}{2\sigma^2}
\right].
\]

Possible rules include:

- set \(\sigma\) to the average distance between neighboring centers;
- set it to a fraction of the mean nearest-center distance;
- choose \(\sigma\) by cross-validation;
- optimize one width per center.

If centers are too close, activations are highly correlated and the design matrix is ill-conditioned. If widths are too large, centers become difficult to distinguish.

### 4. Design matrix

After centers and widths are fixed, create

\[
\Phi=
\begin{bmatrix}
h_1(\mathbf x_1)&\cdots&h_H(\mathbf x_1)\\
\vdots&&\vdots\\
h_1(\mathbf x_N)&\cdots&h_H(\mathbf x_N)
\end{bmatrix}.
\]

For one output, solve

\[
\min_{\mathbf w}\|\Phi\mathbf w-\mathbf y\|^2.
\]

For multiple outputs, the same \(\Phi\) is used with a target matrix \(\mathbf Y\).

### 5. Ordinary least squares

If \(\Phi\) has full column rank,

\[
\mathbf w=(\Phi^{\mathsf T}\Phi)^{-1}
\Phi^{\mathsf T}\mathbf y.
\]

If \(\Phi\) is rank deficient, use a pseudoinverse or ridge regression. A direct inverse of a nearly singular matrix can produce huge, unstable weights.

### 6. Ridge regularization

Ridge minimizes

\[
J(\mathbf w)
=
\|\Phi\mathbf w-\mathbf y\|^2
+\lambda\|\mathbf w\|^2.
\]

The solution is

\[
\mathbf w
=
(\Phi^{\mathsf T}\Phi+\lambda I)^{-1}
\Phi^{\mathsf T}\mathbf y.
\]

The parameter \(\lambda\) controls smoothness. Larger \(\lambda\) shrinks weights and may underfit; smaller \(\lambda\) follows training data more closely.

If a bias is used, append a column of ones to \(\Phi\) or treat it separately.

### 7. Exact interpolation

Given \(N\) centers at all training inputs, \(\Phi\) is an \(N\times N\) matrix. A small width can make it close to the identity, so

\[
\mathbf w=\Phi^{-1}\mathbf y
\]

interpolates the training targets.

This is useful for demonstration and interpolation, but it can produce a highly irregular function between points and poor extrapolation. Regularized approximation is usually preferable for prediction.

### 8. Gradient learning of all parameters

A full RBF network can be optimized with

\[
J(\theta)=\frac1N\sum_n(\hat y_n-y_n)^2
\]

using gradient descent. The parameters include centers, widths, and output weights. The output-weight derivative is

\[
\frac{\partial J}{\partial w_i}
=
\frac{2}{N}\sum_n
(\hat y_n-y_n)h_i(\mathbf x_n).
\]

For a Gaussian center coordinate \(c_{ij}\),

\[
\frac{\partial h_i}{\partial c_{ij}}
=
h_i(\mathbf x_n)\frac{x_{nj}-c_{ij}}{\sigma_i^2}.
\]

For a shared \(\sigma\),

\[
\frac{\partial h_i}{\partial \sigma}
=
h_i(\mathbf x_n)
\frac{\|\mathbf x_n-\mathbf c_i\|^2}{\sigma^3}.
\]

Use the chain rule to connect these derivatives to the loss. Optimize the log width if positivity is required:

\[
\sigma=\exp(\rho).
\]

### 9. Hybrid training

A useful hybrid procedure is:

1. initialize centers by k-means;
2. fix centers and widths;
3. solve output coefficients by least squares;
4. update membership centers or widths with gradient descent;
5. recompute the linear output weights;
6. repeat until validation improvement stops.

This often converges faster than starting all parameters randomly.

### 10. Classification learning

For \(K\) classes, form class-specific output weights:

\[
\mathbf W=(\Phi^{\mathsf T}\Phi+\lambda I)^{-1}
\Phi^{\mathsf T}\mathbf Y.
\]

Use the output scores with argmax, softmax, or a separate calibrated model. If class imbalance is present, class-weighted loss or a one-vs-rest strategy may be more appropriate than unweighted least squares.

### 11. Selecting the number of centers

Try a sequence such as \(H=5,10,20,50\), or a range related to \(N\). For each value:

1. run center selection;
2. fit output weights;
3. evaluate validation loss and classification metrics;
4. record training time and prediction cost;
5. choose the smallest adequate model or the best validated trade-off.

Too many centers can memorize noise; too few can miss narrow class regions.

### 12. Error and stopping criteria

Stop when:

- validation error has not improved for several trials;
- the change in centers is below a tolerance;
- the maximum epochs are reached;
- the numerical system becomes ill-conditioned;
- a target error is achieved.

Do not stop solely because the training error is zero if the goal is generalization.

### 13. Advantages of staged learning

- Output fitting is a convex linear problem when centers and widths are fixed.
- Training is often fast.
- Center-selection methods have practical interpretations.
- Ridge regularization is easy to apply.
- The design can be inspected and updated.

### 14. Limitations

- Center placement remains a difficult unsupervised choice.
- K-means assumes geometry and may not match target-relevant regions.
- Many centers increase distance computation.
- Gradient learning of centers can move units into unhelpful regions.
- Least squares assumes squared error; classification mismatch can hurt.
- Extrapolation is unreliable outside the center cloud.

## Worked examples

### Example 1: Build a design matrix

Use two Gaussian centers

\[
\mathbf c_1=(0,0),\quad \mathbf c_2=(2,0),
\]

with \(\sigma=1\). For inputs

\[
\mathbf x_1=(0,0),\quad
\mathbf x_2=(1,0),\quad
\mathbf x_3=(2,0),
\]

the hidden matrix is

\[
\Phi=
\begin{bmatrix}
1&e^{-2}\\
e^{-0.5}&e^{-0.5}\\
e^{-2}&1
\end{bmatrix}.
\]

Numerically,

\[
\Phi\approx
\begin{bmatrix}
1&0.1353\\
0.6065&0.6065\\
0.1353&1
\end{bmatrix}.
\]

The middle input is equally distant from both centers, which is reflected by equal activations.

### Example 2: Solve a one-hidden-unit output fit exactly

Suppose one hidden unit produces the responses

\[
\mathbf h=[1,2,3]^{\mathsf T}
\]

for three training inputs, and the desired scalar targets are

\[
\mathbf y=[1,2,3]^{\mathsf T}.
\]

The design matrix is the single column

\[
\Phi=\begin{bmatrix}1\\2\\3\end{bmatrix}.
\]

The least-squares output weight is

\[
w=(\Phi^{\mathsf T}\Phi)^{-1}\Phi^{\mathsf T}\mathbf y
=\frac{1}{1^2+2^2+3^2}
(1\cdot1+2\cdot2+3\cdot3)
=\frac{14}{14}=1.
\]

Thus

\[
\hat y=\Phi w=[1,2,3],
\]

which matches the target exactly. The calculation shows the important point: after centers and widths are fixed, output training is ordinary least squares. It does not mean that one arbitrary hidden feature can reproduce every target.

### Example 3: Ridge shrinkage

Suppose

\[
\Phi^{\mathsf T}\Phi=
\begin{bmatrix}
2&0.5\\
0.5&1
\end{bmatrix},
\qquad
\Phi^{\mathsf T}\mathbf y=
\begin{bmatrix}4\\1\end{bmatrix}.
\]

With \(\lambda=1\),

\[
\mathbf w=
\begin{bmatrix}
2.5&0.5\\
0.5&2
\end{bmatrix}^{-1}
\begin{bmatrix}4\\1\end{bmatrix}.
\]

The determinant is \(5-0.25=4.75\), and the inverse is

\[
\frac1{4.75}
\begin{bmatrix}
2&-0.5\\
-0.5&2.5
\end{bmatrix}.
\]

Thus

\[
\mathbf w
=
\frac1{4.75}
\begin{bmatrix}8-0.5\\-2+2.5\end{bmatrix}
=
\frac1{4.75}
\begin{bmatrix}7.5\\0.5\end{bmatrix}
\approx
\begin{bmatrix}1.5789\\0.1053\end{bmatrix}.
\]

A larger ridge parameter would generally reduce the magnitude of the weights.

### Example 4: Gaussian width and conditioning

If two centers are very close relative to \(\sigma\), their rows in \(\Phi\) are almost identical. The system can fit the targets only with large opposing weights, which is unstable. Increase separation, reduce width, or add ridge regularization.

### Example 5: Classification with class scores

For two classes, a network may produce scores

\[
(\hat y_0,\hat y_1)=(0.2,0.8).
\]

Argmax predicts class 1. If a probabilistic output is required, apply a calibrated sigmoid or softmax and train with the corresponding loss. Do not call the raw score a probability without that step.

## Key terms & formulas

- **Two-stage learning:** Select hidden parameters, then fit output weights.
- **Center selection:** Choose prototype locations.
- **Width selection:** Choose the radial scale.
- **Design matrix:** \(\Phi\) of hidden activations.
- **Ridge regression:** Least squares with an L2 penalty.
- **Interpolation:** Fit all training points exactly.
- **Approximation:** Fit a smooth function with fewer centers.
- **Conditioning:** Stability of the normal equations.

OLS:

\[
\mathbf w=(\Phi^{\mathsf T}\Phi)^{-1}\Phi^{\mathsf T}\mathbf y.
\]

Ridge:

\[
\mathbf w=(\Phi^{\mathsf T}\Phi+\lambda I)^{-1}\Phi^{\mathsf T}\mathbf y.
\]

Gaussian center derivative:

\[
\frac{\partial h_i}{\partial c_{ij}}
=h_i\frac{x_j-c_{ij}}{\sigma_i^2}.
\]

## Common mistakes

1. **Using k-means centers without scaling features.** Cluster geometry follows the chosen distance.
2. **Using every data point and calling it generalization.** It may interpolate noise.
3. **Inverting a singular design matrix.** Use a pseudoinverse, ridge, or better center coverage.
4. **Forgetting to append a bias column.** A constant output offset may be lost.
5. **Using one width for very uneven data without validation.** Local widths may be more appropriate.
6. **Stopping on zero training error.** Check validation performance.
7. **Applying a regression output directly as a probability.** Calibration is a separate model.
8. **Ignoring distance computation cost.** Many centers and high dimensions can make inference slow.

## Exam prep

### Likely 2-mark questions

- **List the two stages of RBF learning.**  
  **Hint:** Select centers/widths, then fit output weights.

- **Write the Gaussian RBF output design matrix entry.**  
  **Hint:** \(\Phi_{ni}=\exp[-\|x_n-c_i\|^2/(2\sigma_i^2)]\).

- **State the ridge-regression solution.**  
  **Hint:** \((\Phi^T\Phi+\lambda I)^{-1}\Phi^Ty\).

- **Name three center-selection methods.**  
  **Hint:** All samples, subset, k-means, SOM, farthest point, or greedy.

- **What is the benefit of fixing centers before fitting output weights?**  
  **Hint:** Output training becomes a linear least-squares problem.

### Likely long-answer questions

- **Explain the complete learning procedure for an RBFNN.**  
  **Hint:** Scaling, center selection, width, design matrix, least squares, regularization, validation.

- **Derive and compare ordinary least squares and ridge learning for RBF output weights.**  
  **Hint:** Objectives, solutions, condition number, overfitting, and bias–variance trade-off.

- **Explain how centers and widths are learned by gradient descent.**  
  **Hint:** Gaussian derivatives, chain rule, log-width parameterization, and optimization.

- **Work out an RBF classification example.**  
  **Hint:** Hidden responses, class output weights, argmax/softmax, and a training table.

- **Discuss methods for selecting the number of RBF centers.**  
  **Hint:** Validation, complexity, overfitting, distance cost, and interpretation.
