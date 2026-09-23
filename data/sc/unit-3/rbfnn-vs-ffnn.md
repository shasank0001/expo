---
subject: sc
unit: 3
topic: rbfnn-vs-ffnn
syllabus_ref: CSM3202 Unit-III
status: draft
---
# RBFNN vs FFNN

## Overview

An RBF network and a multilayer feed-forward network are both supervised neural networks. RBF networks use distance-based local hidden activations; general FFNNs use learned weighted sums and activation functions. RBF networks often train their output layer quickly, while FFNNs use backpropagation throughout the network.

Neither is universally better. The choice depends on data size, dimensionality, locality, required accuracy, speed, and whether an approximate interpolation or a complex learned representation is desired.

## Explanation

### 1. Common structure

Both networks can have:

- an input layer;
- one or more hidden layers;
- an output layer;
- weights and biases;
- a training set of input-target pairs;
- a validation procedure.

Both can solve XOR with a hidden layer and can approximate nonlinear functions. Their hidden representations differ.

### 2. RBF hidden activation

For an RBF unit,

\[
h_i(\mathbf x)
=
\phi\left(\frac{\|\mathbf x-\mathbf c_i\|}{\sigma_i}\right).
\]

The center and width determine a local response. The output layer is commonly linear:

\[
\hat y=\mathbf w^{\mathsf T}\mathbf h.
\]

### 3. FFNN hidden activation

For a general FFNN unit,

\[
a_i=\phi(\mathbf w_i^{\mathsf T}\mathbf x+b_i).
\]

Each hidden unit learns a weighted combination of all input features and a bias. Sigmoid, tanh, and ReLU functions are common. The output may be sigmoid, softmax, or linear.

### 4. Training comparison

#### RBF network

A common two-stage method selects centers by k-means or samples, chooses widths, and solves output weights by least squares or ridge regression. Centers and widths may also be gradient-trained.

#### FFNN

Backpropagation calculates gradients through every layer. Weight and bias updates use gradient descent, minibatches, and an optimizer such as SGD or Adam.

The RBF output stage is linear once hidden parameters are fixed; FFNN training is nonlinear throughout the network.

### 5. Local versus distributed representations

RBF hidden units are local or locally concentrated. A center represents a prototype, and nearby inputs activate it strongly.

An FFNN hidden unit is distributed: its output depends on a learned weighted sum of all inputs. Several FFNN units can collectively represent features, but individual units need not correspond to input locations.

A ReLU FFNN may develop sparse local-like features, but it is not automatically an RBF network.

### 6. Interpretability

RBF centers can be visualized as prototypes and responses as local influence maps. Output weights show how prototypes contribute to a class or regression.

FFNN weights are distributed across features and layers. Tools such as feature attribution can provide explanations, but a single hidden unit often has no direct semantic meaning.

RBF interpretability is useful but not complete: a center is a location in input space, not automatically a causal concept.

### 7. Data requirements

RBF networks can perform well with moderate data and smooth targets, especially when center selection is meaningful. FFNNs can learn complex representations but often need more data and careful regularization.

Neither is immune to overfitting. An RBF network with every sample as a center can memorize data; a large FFNN can memorize labels.

### 8. High-dimensional data

RBF distance computation grows with input dimension. In high-dimensional spaces, distances concentrate, so Gaussian neighborhoods may not be selective unless the width and dimensionality are handled carefully.

An FFNN avoids explicitly storing all pairwise center distances during forward propagation, although it has many weights. CNNs and tree/kernel methods may be better than either for particular high-dimensional modalities.

### 9. Computational cost

RBF inference computes a distance to every center:

\[
O(NdH)
\]

for \(H\) centers, \(N\) input features, and one sample, plus output combination.

A dense FFNN forward pass costs roughly the sum of adjacent-layer products:

\[
O\left(\sum_l n_l n_{l+1}\right).
\]

Which is cheaper depends on the number and dimension of centers versus network width and depth. RBF training may be fast for small or medium data; many centers make it expensive.

### 10. Function approximation

RBF networks are natural for smooth interpolation and local approximation. They can represent a broad class of continuous functions when enough centers and suitable widths are used.

A deep FFNN can learn hierarchical nonlinear features and is more flexible for large-scale pattern recognition, but optimization and architecture design are more involved.

### 11. Noise and regularization

RBF ridge regression directly controls output-weight magnitude. Narrow widths and many centers can create high variance.

FFNN regularization includes L1/L2, dropout, early stopping, data augmentation, batch normalization, and architecture constraints. A small weight penalty may not fully address noisy labels; robust loss and data cleaning may be needed.

### 12. Adaptation and changing data

An RBF network can add new centers or refit output weights quickly when new data arrive. FFNNs can also continue training, but updating all weights can cause catastrophic forgetting in a deployed model.

Both methods need a strategy for detecting distribution shift.

### 13. Classification comparison

For \(K\) classes:

- RBF: class-specific linear outputs on local basis functions, often argmax or softmax.
- FFNN: hidden features followed by softmax, sigmoid, or another output layer.

A softmax FFNN may produce calibrated probabilities more naturally, but calibration still requires validation. RBF scores require a declared probability mapping.

### 14. Regression comparison

RBF regression is often smooth and data-efficient when centers represent the domain. FFNN regression can model complex relationships and high-dimensional interactions, but needs more careful training and scaling.

For a noisy physical process, RBF ridge may be a useful stable baseline. For a large image or text model, a deep FFNN or specialized architecture may be more appropriate.

### 15. Choosing between them

Choose RBF when:

- the input dimension is moderate;
- local similarity has meaning;
- smooth interpolation is desired;
- data are limited or medium-sized;
- fast refitting of a fixed basis is valuable.

Choose FFNN when:

- a complex nonlinear mapping is needed;
- distributed learned features are useful;
- the input is suitable for a deep model;
- flexible backpropagation and representation learning are required.

Use validation and a baseline rather than choosing by rule of thumb.

### 16. Hybrid models

A model can combine them:

- RBF features feed an FFNN output;
- FFNN embeddings define a metric for RBF centers;
- an RBF network supplies local features to a neural controller;
- a GA chooses RBF centers and FFNN hyperparameters.

A hybrid adds complexity and should be justified by a held-out comparison.

## Worked examples

### Example 1: Same function, different training

Suppose three centers are selected and their Gaussian responses are fixed. An RBF output fit is a linear least-squares problem:

\[
\hat{\mathbf y}=\Phi\mathbf w.
\]

An FFNN with the same number of hidden units would jointly optimize centers/weights and hidden activations through backpropagation. RBF can solve its output stage directly; FFNN requires iterative nonlinear optimization.

### Example 2: Locality test

For a one-dimensional input, an RBF center at \(c=0.5,\sigma=0.1\):

\[
h(0.5)=1,\quad h(0.55)=e^{-0.25}\approx0.7788,\quad h(1.5)\approx e^{-100}\approx0.
\]

The response is clearly local. A sigmoid unit with learned weight and bias can also become selective, but it is governed by a weighted threshold rather than an explicit distance prototype.

### Example 3: Data-size experiment

Train both models on 50, 500, and 5,000 examples. An RBF model may do well with the smaller sets if centers are well chosen, while a larger FFNN may improve with more data. Report validation curves; do not compare only one training size.

### Example 4: Cost comparison

A model with 100 centers and 20 input features evaluates 2,000 squared-distance terms per sample. A network with layer sizes \(20\to50→10\) performs roughly \(20(50)+50(10)=1,500\) multiply-accumulate terms, plus activations. The RBF may still be preferable if its centers are updated less frequently or the task has locality.

## Key terms & formulas

- **FFNN:** General feed-forward network using weighted activations.
- **RBFNN:** Network with distance-based radial hidden units.
- **Prototype:** RBF center.
- **Locality:** Response concentrated near a center.
- **Backpropagation:** Gradient training through FFNN layers.
- **Two-stage RBF learning:** Choose basis parameters, then fit outputs.
- **Inductive bias:** Assumption built into a model about the kind of function likely.
- **Conditioning:** Sensitivity/stability of the parameter-fitting system.

RBF:

\[
h_i(\mathbf x)=\exp\left[-\frac{\|\mathbf x-\mathbf c_i\|^2}{2\sigma_i^2}\right].
\]

FFNN:

\[
a_i=\phi(\mathbf w_i^{\mathsf T}\mathbf x+b_i).
\]

RBF output fit:

\[
\mathbf w=(\Phi^{\mathsf T}\Phi+\lambda I)^{-1}\Phi^{\mathsf T}\mathbf y.
\]

## Common mistakes

1. **Saying FFNN always uses sigmoid units.** ReLU, tanh, linear, and other activations are common.
2. **Saying RBF is always faster.** Cost depends on centers, dimension, and hardware.
3. **Treating RBF centers as class labels.** They are locations in input space.
4. **Claiming FFNN cannot represent locality.** Some FFNN units can be selective, but locality is not guaranteed.
5. **Ignoring overfitting in RBF networks.** One center per sample can memorize data.
6. **Comparing models with different data splits or preprocessing.** Use the same controlled experiment.
7. **Calling RBF scores probabilities.** Calibration is additional.
8. **Assuming a deep network is always more accurate.** Data and regularization determine performance.

## Exam prep

### Likely 2-mark questions

- **Give two differences between RBFNN and FFNN.**  
  **Hint:** Distance-based local hidden units versus weighted activation units; staged versus backpropagation training.

- **What is an RBF center?**  
  **Hint:** A prototype location in input space.

- **What is the main output-layer difference?**  
  **Hint:** RBF commonly uses a linear weighted sum after basis activations; FFNN may use sigmoid, softmax, or linear output.

- **Which model is naturally suited to local interpolation?**  
  **Hint:** RBFNN, subject to center and width choices.

- **Why can a ReLU FFNN be high-dimensional?**  
  **Hint:** It avoids explicit distance to every center and learns distributed features, but may need more data and regularization.

### Likely long-answer questions

- **Compare RBFNN and FFNN in terms of architecture, training, and representation.**  
  **Hint:** Equations, two-stage learning, backpropagation, local versus distributed features.

- **Discuss computational complexity and data requirements of RBF and FFNN models.**  
  **Hint:** Distance cost versus layer products, center count, scaling, and validation.

- **Explain when an RBF network is preferable to an FFNN.**  
  **Hint:** Moderate dimension, local similarity, smooth interpolation, limited data, and fast output fitting.

- **Explain when an FFNN is preferable to an RBF network.**  
  **Hint:** Complex learned representations, larger models, flexible nonlinear tasks, and available training infrastructure.

- **Compare classification and regression performance of RBF and FFNN models.**  
  **Hint:** Output scores, probability calibration, smoothness, generalization, and regularization.
