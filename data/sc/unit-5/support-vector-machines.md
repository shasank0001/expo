---
subject: sc
unit: 5
topic: support-vector-machines
syllabus_ref: CSM3202 Unit-V
status: draft
---
# Support Vector Machines

## Overview

A support vector machine is a supervised learning method that seeks a separating hyperplane with the largest possible margin. The boundary is determined by the training samples closest to the opposite classes, called support vectors. A kernel allows the same idea to classify data that are not linearly separable in their original coordinates.

SVMs are effective for classification and regression, especially when data have many features and limited labeled examples. They require scaling, regularization, and careful choice of kernel and penalty.

## Explanation

### 1. Linear separation

For labeled data

\[
\{(\mathbf x_i,y_i)\}_{i=1}^{N},
\qquad y_i\in\{-1,+1\},
\]

a separating hyperplane is

\[
\mathbf w^{\mathsf T}\mathbf x+b=0.
\]

The signed score is

\[
f(\mathbf x)=\mathbf w^{\mathsf T}\mathbf x+b.
\]

The predicted label is

\[
\hat y=\operatorname{sign}(f(\mathbf x)).
\]

A point far from the boundary has a large score; a support vector lies on or near the margin.

### 2. Maximum margin

The two margin planes are

\[
\mathbf w^{\mathsf T}\mathbf x+b=+1
\]

and

\[
\mathbf w^{\mathsf T}\mathbf x+b=-1.
\]

The distance between them is

\[
\frac{2}{\|\mathbf w\|}.
\]

Maximizing the margin is equivalent to minimizing

\[
\frac12\|\mathbf w\|^2.
\]

The constraints for linearly separable data are

\[
y_i(\mathbf w^{\mathsf T}\mathbf x_i+b)\ge1.
\]

This formulation makes the SVM a convex optimization problem when the data are separable.

### 3. Support vectors

Support vectors are points for which

\[
y_i(\mathbf w^{\mathsf T}\mathbf x_i+b)\le1
\]

under the full-margin definition; in a soft-margin trained solution, many points lie on the margin and some violate it. Points with a strict margin do not determine the boundary, so removing them does not change the solution.

This gives a form of sparsity in the dual representation, although a high-dimensional problem can still have many support vectors.

### 4. Soft-margin SVM

Real data may overlap or contain noise. Introduce slack variables \(\xi_i\ge0\):

\[
y_i(\mathbf w^{\mathsf T}\mathbf x_i+b)\ge1-\xi_i.
\]

Minimize

\[
\frac12\|\mathbf w\|^2
+C\sum_i\xi_i
\]

or a squared hinge version

\[
\frac12\|\mathbf w\|^2
+C\sum_i\max(0,1-y_if(\mathbf x_i))^2.
\]

\(C>0\) balances margin size against violations:

- large \(C\): penalize errors strongly, possibly narrow margin;
- small \(C\): tolerate errors, possibly wider margin and more regularization.

The exact loss changes the trade-off and should be stated.

### 5. Lagrangian and dual problem

Using Lagrange multipliers \(\alpha_i\ge0\), the dual for a soft-margin classifier is

\[
\max_\alpha
\sum_i\alpha_i
-\frac12\sum_{i,j}\alpha_i\alpha_jy_iy_j
\mathbf x_i^{\mathsf T}\mathbf x_j
\]

subject to

\[
\sum_i\alpha_iy_i=0,
\]

and for the standard \(0/1\) slacks,

\[
0\le\alpha_i\le C.
\]

The primal weights are reconstructed as

\[
\mathbf w=\sum_i\alpha_iy_i\mathbf x_i,
\]

and

\[
b=\sum_{i:\alpha_i<C}y_i-\mathbf w^{\mathsf T}\mathbf x_i
\]

using suitable support vectors.

The decision function is

\[
f(\mathbf x)=\sum_i\alpha_iy_iK(\mathbf x_i,\mathbf x)+b.
\]

### 6. Kernel trick

A kernel is a similarity function

\[
K(\mathbf x,\mathbf z)
\]

that implicitly represents a dot product in a feature space:

\[
K(\mathbf x,\mathbf z)=\phi(\mathbf x)^{\mathsf T}\phi(\mathbf z).
\]

The algorithm uses \(K\) without explicitly computing \(\phi\). This is called the kernel trick.

#### Linear kernel

\[
K(\mathbf x,\mathbf z)=\mathbf x^{\mathsf T}\mathbf z.
\]

#### Polynomial kernel

\[
K(\mathbf x,\mathbf z)
=(\gamma\mathbf x^{\mathsf T}\mathbf z+r)^d.
\]

#### Radial basis function kernel

\[
K(\mathbf x,\mathbf z)
=\exp(-\gamma\|\mathbf x-\mathbf z\|^2).
\]

The RBF kernel is often written with \(0<\gamma\le1\) or with \(\gamma=1/(2\sigma^2)\). State the convention.

### 7. Feature scaling

Distance-based kernels are sensitive to feature scale. If one feature is in meters and another in thousands of meters, the larger-scale feature dominates the RBF distance. Standardize or min–max scale features using training statistics.

SVM performance should be checked after scaling and with a linear-kernel baseline.

### 8. Support vector regression (SVR)

SVR predicts a continuous function while allowing most points inside an \(\epsilon\)-tube. The objective uses \(\epsilon\)-insensitive loss:

\[
L_\epsilon(r)=
\begin{cases}
0,&|r|\le\epsilon,\\
|r|-\epsilon,&|r|>\epsilon,
\end{cases}
\]

where \(r=f(\mathbf x)-y\).

Parameters \(C\), \(\epsilon\), and the kernel control the fit. A small \(\epsilon\) demands accurate predictions; a large \(\epsilon\) tolerates a wider error band.

### 9. Multiclass SVM

A binary SVM handles two classes. For \(K>2\) classes, common strategies are:

#### One-versus-one

Train \(K(K-1)/2\) binary classifiers and choose the class with the greatest decision score, often with voting.

#### One-versus-rest

Train \(K\) classifiers, one for each class against all others, and choose the largest positive score.

#### Crammer–Singer

Train a single multiclass formulation with coupled constraints. It can be more efficient but computationally harder.

Class scores from an SVM are not automatically calibrated probabilities. Use Platt scaling or another calibration method on validation data.

### 10. Model parameters and validation

Important choices are:

- kernel;
- \(C\);
- \(\gamma\);
- class weights;
- scaling;
- loss;
- probability calibration;
- train/validation/test split.

Use stratified splits for imbalanced classes, cross-validation when data are small, and a nested procedure if tuning and calibration are both performed.

### 11. Advantages

- Strong generalization through maximum margin.
- Effective in high-dimensional spaces.
- Convex optimization for fixed hyperparameters.
- Flexible kernels for nonlinear boundaries.
- Sparse dual representation through support vectors.
- Works for classification and regression.

### 12. Limitations

- Training cost can be high for large samples.
- Kernel and \(C\) selection require validation.
- Feature scaling is important.
- Probability outputs require calibration.
- A multiclass implementation may be expensive.
- Less interpretable when many support vectors are used.
- Sensitive to noisy labels and class imbalance.
- RBF behavior in very high dimension requires care.

## Worked examples

### Example 1: Find a linear SVM boundary

Consider three points:

\[
(-1,-1,-1),\quad(1,1,+1),\quad(2,2,+1).
\]

A separating line can be

\[
x_1+x_2-1=0.
\]

For \((-1,-1)\), score is \(-3\); for \((1,1)\), score is \(1\); for \((2,2)\), score is \(3\). The first two are support vectors on the margins \(f(x)=0\), but the full margin constraints need a geometric scale. A fitted SVM would calculate \(w,b\) from the optimization, not choose them by intuition.

### Example 2: RBF kernel value

Let

\[
K(\mathbf x,\mathbf z)=\exp(-\gamma\|\mathbf x-\mathbf z\|^2),
\]

with \(\gamma=0.5\), \(\mathbf x=(1,0)\), and \(\mathbf z=(0,1)\). Then

\[
\|\mathbf x-\mathbf z\|^2=2,
\]

so

\[
K=e^{-0.5(2)}=e^{-1}\approx0.3679.
\]

The kernel gives a moderate similarity, not a Euclidean distance.

### Example 3: Soft-margin interpretation

If \(C=10\), a misclassified point is penalized more than it would be with \(C=0.1\). The SVM may bend or create a complex boundary to fit outliers, reducing robustness. A smaller \(C\) can accept some errors for a smoother boundary.

### Example 4: SVR error tube

Let target \(y=4\), prediction \(f=4.2\), and \(\epsilon=0.5\). The residual is 0.2, so the epsilon-insensitive loss is 0. The point is considered sufficiently accurate. If \(f=5\), the residual is 1 and the loss is 0.5.

### Example 5: Multiclass voting

For three classes, one-vs-one classifiers may output votes A:2, B:1, C:0. A is selected. This is a decision procedure, not a probability estimate.

## Key terms & formulas

- **Support vector:** Training point on or near the margin.
- **Margin:** Distance between separating boundary planes.
- **Hard margin:** No training violations.
- **Soft margin:** Allows violations with a penalty.
- **Kernel:** Similarity function in implicit feature space.
- **RBF kernel:** \(\exp(-\gamma\|\mathbf x-\mathbf z\|^2)\).
- **SVR:** SVM with epsilon-insensitive regression loss.
- **Calibration:** Convert scores to meaningful probabilities.

Margin distance:

\[
\frac{2}{\|\mathbf w\|}.
\]

Dual:

\[
\max_\alpha
\sum_i\alpha_i-\frac12\sum_{i,j}
\alpha_i\alpha_jy_iy_jK(\mathbf x_i,\mathbf x_j).
\]

Decision:

\[
f(\mathbf x)=\sum_i\alpha_iy_iK(\mathbf x_i,\mathbf x)+b.
\]

## Common mistakes

1. **Ignoring feature scaling.** RBF and other distance-based kernels require it.
2. **Thinking the support vectors are the farthest points.** They are the closest margin points.
3. **Claiming a soft-margin SVM always separates every point.** It permits violations.
4. **Treating an SVM score as a probability.** Calibrate separately.
5. **Using \(C\) without explaining the trade-off.** Large C favors fitting; small C favors regularization.
6. **Forgetting the RBF gamma parameter.** It controls locality.
7. **Using a linear kernel for nonlinear data without validation.** It may underfit.
8. **Selecting \(K\) and \(C\) on the test set.** Tune on training/validation data.

## Exam prep

### Likely 2-mark questions

- **Define an SVM and identify support vectors.**  
  **Hint:** Maximum-margin classifier; points closest to the boundary.

- **Write the margin distance.**  
  **Hint:** \(2/\|\mathbf w\|\).

- **State the RBF kernel.**  
  **Hint:** \(K(x,z)=\exp(-\gamma\|x-z\|^2)\).

- **What is a soft-margin SVM?**  
  **Hint:** Allows violations using slack variables and a penalty.

- **Why scale SVM features?**  
  **Hint:** Distances and kernel similarities depend on feature units.

### Likely long-answer questions

- **Explain the maximum-margin formulation of a linear SVM.**  
  **Hint:** Hyperplane, constraints, margin, objective, support vectors, and decision.

- **Derive the need for kernels and explain the kernel trick.**  
  **Hint:** Feature map, similarity, nonlinear boundary, and no explicit high-dimensional coordinates.

- **Compare hard-margin, soft-margin, classification, and regression SVMs.**  
  **Hint:** Slack variables, \(C\), loss, epsilon tube, and use cases.

- **Explain multiclass SVM and probability calibration.**  
  **Hint:** One-vs-one, one-vs-rest, decision scores, and validation-based calibration.
