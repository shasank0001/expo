---
subject: sc
unit: 3
topic: rbfnn-overview
syllabus_ref: CSM3202 Unit-III
status: draft
---
# Radial Basis Function Neural Network

## Overview

A radial basis function neural network (RBFNN) is a feed-forward network whose hidden units use a function of distance between an input and a center. A hidden unit responds strongly when the input is near its center and weakly when it is far away. The output layer combines those local responses.

RBF networks are often easier to train than sigmoid FFNNs because hidden-unit learning is usually separated from output-weight learning. They perform well with moderate data, smooth interpolation, function approximation, and classification. Their accuracy can decline when many centers are required or the input space is high-dimensional.

## Explanation

### 1. Basic idea

Suppose hidden unit \(i\) has center \(\mathbf c_i\) and width \(\sigma_i\). Its activation is

\[
h_i(\mathbf x)
=
\phi\left(\frac{\|\mathbf x-\mathbf c_i\|}{\sigma_i}\right).
\]

The response depends only on distance, not on a separate weight for every input dimension in the same way a sigmoid neuron does. This gives hidden units a local, prototype-like meaning.

The network output is

\[
\hat y(\mathbf x)
=
\sum_{i=1}^{H}w_i h_i(\mathbf x)+w_0
\]

for a single scalar output, or a matrix form for multiple outputs. A direct connection from input to output may be added:

\[
\hat y(\mathbf x)
=w_0+\mathbf a^{\mathsf T}\mathbf x
+\mathbf w^{\mathsf T}\mathbf h(\mathbf x).
\]

### 2. Distance measures

#### Euclidean distance

\[
d(\mathbf x,\mathbf c_i)
=
\sqrt{\sum_{j=1}^{d}(x_j-c_{ij})^2}.
\]

This is the most common RBF distance.

#### Squared Euclidean distance

\[
d^2(\mathbf x,\mathbf c_i)
=
\sum_{j=1}^{d}(x_j-c_{ij})^2.
\]

Squared distance avoids a square root and is often used inside Gaussian functions.

#### Manhattan distance

\[
d_1(\mathbf x,\mathbf c_i)=\sum_j|x_j-c_{ij}|.
\]

This can be useful for sparse or piecewise-linear features.

The choice of distance should match the geometry of the data. Standardizing features is especially important when their units differ.

### 3. Common radial basis functions

#### Gaussian

\[
\phi(r)=e^{-r^2}.
\]

With width,

\[
h_i(\mathbf x)
=
\exp\left[-\frac{\|\mathbf x-\mathbf c_i\|^2}{2\sigma_i^2}\right].
\]

Gaussian functions are smooth and are the most common choice.

#### Multiquadric

\[
\phi(r)=\sqrt{r^2+1}.
\]

#### Inverse multiquadric

\[
\phi(r)=\frac{1}{\sqrt{r^2+1}}.
\]

#### Thin-plate spline

\[
\phi(r)=r^2\log r,
\]

with the value at \(r=0\) defined as 0. It is useful for smooth interpolation in some settings.

#### Cubic or spherical

\[
\phi(r)=
\begin{cases}
1-\frac53r^2+\frac12r^3,&0\le r\le1,\\
0,&r>1.
\end{cases}
\]

A spherical basis gives exact compact support.

### 4. Architecture

An RBF network has three conceptual layers:

1. **Input layer:** receives \(\mathbf x\).
2. **Hidden layer:** contains \(H\) radial basis functions, each with a center and width.
3. **Output layer:** computes a weighted sum.

Typical parameters are:

- centers \(\{\mathbf c_i\}\);
- widths \(\{\sigma_i\}\);
- output weights \(\{w_i\}\);
- output bias \(w_0\).

The number of hidden units and centers is central to the network's capacity.

### 5. Local response and width

A Gaussian with a small \(\sigma_i\) responds only very near \(\mathbf c_i\); a large \(\sigma_i\) gives a broad response. A very small width can cause numerical problems if an input is far from every center. A very large width makes many units respond almost identically and increases smoothness.

In high dimensions, distances concentrate: points may all be far apart relative to the width. This makes one global Gaussian width less effective, and regularization or a local method may be needed.

### 6. Center selection

Centers may be selected by:

- choosing all or a subset of training samples;
- k-means clustering;
- random sampling;
- self-organizing maps;
- fuzzy c-means or another clustering method;
- greedy/orthogonal-center selection.

k-means is common because it places centers in dense regions. With \(N\) samples and \(H\) centers, \(H\) controls memory and training time.

### 7. Output-weight learning

Once centers and widths are fixed, the hidden design matrix is

\[
\Phi=
\begin{bmatrix}
\phi(\mathbf x_1)&\cdots&\phi(\mathbf x_N)\\
\vdots&&\vdots
\end{bmatrix},
\]

where each row contains the hidden activations for one sample. For targets \(\mathbf y\), the least-squares output weights satisfy

\[
\mathbf w=\Phi^+\mathbf y
\]

where \(\Phi^+\) is a pseudoinverse, or

\[
\mathbf w=(\Phi^{\mathsf T}\Phi+\lambda I)^{-1}
\Phi^{\mathsf T}\mathbf y
\]

with ridge regularization.

This linear output layer can be solved efficiently and does not require the same iterative nonlinear search as a sigmoid FFNN.

### 8. Training modes

#### Exact interpolation

Choose as many centers as training samples and widths so that the Gaussian matrix is nonsingular. The network can interpolate all training targets, though it may oscillate between them.

#### Approximation learning

Use fewer centers than samples and choose widths to obtain a smooth approximation. This is usually more useful for prediction.

#### Regularized learning

Add a penalty to reduce sensitivity and improve smoothness:

\[
\min_{\mathbf w}\|\Phi\mathbf w-\mathbf y\|^2
+\lambda\|\mathbf w\|^2.
\]

Regularization is especially useful with many centers or noisy data.

### 9. RBF network versus a prototype method

A hidden center acts like a representative prototype. A new input activates nearby prototypes, and the output layer combines their local evidence. This is similar to nearest-neighbor and kernel methods.

RBF networks are therefore related to kernel regression:

\[
\hat y(\mathbf x)=\sum_n\alpha_nK(\mathbf x,\mathbf x_n).
\]

The centers are a compact set of representative basis locations; a kernel method may use every training point.

### 10. Classification form

For \(K\) classes, use one output neuron per class:

\[
\hat{\mathbf y}_k=\mathbf w_k^{\mathsf T}\mathbf h.
\]

The predicted class is often

\[
k^*=\arg\max_k \hat y_k,
\]

or, for probabilistic outputs, use a normalized or logistic model. A radial-basis network is not automatically a probability model; normalization is a design choice.

### 11. Training advantages

- Fast output-layer solution.
- Centers and widths can be selected separately.
- Smooth response functions.
- Straightforward local prototypes.
- Often fewer training difficulties than deep sigmoid networks.

### 12. Limitations

- Number and placement of centers strongly affect performance.
- Training can become expensive with many centers.
- Gaussian distance computation is costly in high dimensions.
- Extrapolation outside the training range can be poor.
- Output weights can overfit noisy data.
- A fixed center-selection heuristic may miss important regions.
- Interpretability is local and depends on the chosen basis functions.

### 13. Applications

RBF networks are used for:

- interpolation and function approximation;
- pattern classification;
- time-series prediction;
- system identification;
- control;
- image and signal processing;
- surface fitting;
- sensor calibration.

For large datasets or high-dimensional raw data, a kernel SVM, neural network, or nearest-neighbor method may be more scalable.

## Worked examples

### Example 1: One hidden unit

Let

\[
\mathbf x=(1,2),\quad
\mathbf c=(1,0),\quad
\sigma=2.
\]

Squared distance is

\[
d^2=(1-1)^2+(2-0)^2=4.
\]

Gaussian activation:

\[
h=\exp\left(-\frac4{2(2)^2}\right)
=\exp(-0.5)\approx0.6065.
\]

The input is moderately close to the center, so the hidden unit responds at 0.6065.

### Example 2: Width comparison

For the same center and input,

\[
\sigma=1:
\quad h=e^{-4/2}=e^{-2}\approx0.1353.
\]

\[
\sigma=2:
\quad h=e^{-4/8}=e^{-0.5}\approx0.6065.
\]

\[
\sigma=4:
\quad h=e^{-4/32}=e^{-0.125}\approx0.8825.
\]

A larger width produces a smoother, broader response.

### Example 3: Two-unit output

Suppose two hidden units produce

\[
\mathbf h=(0.8,0.4)
\]

and output weights are

\[
\mathbf w=(2,-1),\qquad w_0=0.5.
\]

Then

\[
\hat y=0.5+2(0.8)-1(0.4)=1.7.
\]

If a direct input term is present, it must be added separately.

### Example 4: Center selection by k-means

For a dataset with 1,000 points and 20 k-means clusters, choose the 20 cluster centroids as RBF centers. The network then uses 20 hidden units rather than 1,000. Validate several values of \(H\); more centers can represent local detail but increase overfitting and computation.

## Key terms & formulas

- **RBFNN:** Neural network using distance-based hidden activations.
- **Center:** Prototype location \(\mathbf c_i\).
- **Width:** Scale of basis function \(\sigma_i\).
- **Design matrix:** \(\Phi\) of hidden activations.
- **Center selection:** Choosing representative prototype locations.
- **Regularized learning:** Ridge-like penalty on output weights.
- **Local response:** Strong activation near a center.
- **Kernel relation:** RBF functions resemble kernel methods.

Gaussian activation:

\[
h_i(\mathbf x)=
\exp\left[-\frac{\|\mathbf x-\mathbf c_i\|^2}{2\sigma_i^2}\right].
\]

Output:

\[
\hat y=w_0+\sum_iw_ih_i.
\]

Ridge solution:

\[
\mathbf w=(\Phi^{\mathsf T}\Phi+\lambda I)^{-1}
\Phi^{\mathsf T}\mathbf y.
\]

## Common mistakes

1. **Using unscaled features with Euclidean distance.** Large-scale features dominate distances.
2. **Choosing too many centers.** The network can overfit and become expensive.
3. **Using a width that is too small.** Inputs far from centers receive nearly zero response.
4. **Confusing a fuzzy membership value with an RBF activation.** Both are numbers in \([0,1]\) for Gaussian units, but their semantics differ.
5. **Assuming the output is a probability.** Apply a declared classification or probability model.
6. **Forgetting regularization in least-squares output fitting.** A singular or ill-conditioned matrix can result.
7. **Ignoring extrapolation.** A smooth interpolation fit may be unreliable far outside the data.
8. **Comparing different numbers of centers without validation complexity.** Report both accuracy and resource cost.

## Exam prep

### Likely 2-mark questions

- **Define a radial basis function.**  
  **Hint:** A function of distance from a center, commonly Gaussian.

- **Write a Gaussian RBF hidden activation.**  
  **Hint:** \(\exp[-\|x-c\|^2/(2\sigma^2)]\).

- **State two ways to select RBF centers.**  
  **Hint:** Training samples, k-means, random selection, SOM, or fuzzy clustering.

- **What is the RBF design matrix?**  
  **Hint:** Matrix whose rows contain hidden-unit activations for training samples.

- **Why standardize input features?**  
  **Hint:** Distance and width would otherwise be dominated by feature scale.

### Likely long-answer questions

- **Explain the architecture and working of an RBF network.**  
  **Hint:** Input, centers/widths, radial activations, output combination, and local response.

- **Compare Gaussian, multiquadric, and thin-plate-spline basis functions.**  
  **Hint:** Formula, support/shape, smoothness, and use cases.

- **Describe center selection and output-weight training in an RBFNN.**  
  **Hint:** k-means/subsampling, design matrix, least squares/ridge, and validation.

- **Discuss advantages and limitations of RBF networks.**  
  **Hint:** Fast output training and smooth local responses versus center cost, high dimensionality, and overfitting.

- **Explain how an RBF network performs classification.**  
  **Hint:** Class-specific output weights, activation, argmax or declared probability conversion, and an example.
