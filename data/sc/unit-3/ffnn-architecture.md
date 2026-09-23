---
subject: sc
unit: 3
topic: ffnn-architecture
syllabus_ref: CSM3202 Unit-III
status: draft
---
# Multilayer Feed-Forward Neural Network

## Overview

A feed-forward neural network passes data in one direction from input units to output units without feedback or cycles. A multilayer feed-forward network (MLFFN or FFNN) contains one or more hidden layers. Hidden units learn intermediate features that allow the network to approximate nonlinear relationships that one layer cannot learn.

The architecture includes the number of layers and units, connections, weights, biases, activation functions, objective function, and training algorithm. Architecture is not just a drawing: it determines the functions the network can represent and the way errors are calculated.

## Explanation

### 1. Artificial neuron

A neuron receives inputs \(x_1,\ldots,x_n\). It computes a weighted sum plus a bias:

\[
v=\sum_{i=1}^{n}w_ix_i+b.
\]

The bias acts like a weight attached to a constant input 1. It shifts the activation threshold and is important when the desired hyperplane does not pass through the origin.

An activation function produces the output:

\[
y=\phi(v).
\]

Common choices include:

- **Logistic sigmoid**
  \[
  \sigma(v)=\frac{1}{1+e^{-v}};
  \]
- **Hyperbolic tangent**
  \[
  \tanh(v)=\frac{e^v-e^{-v}}{e^v+e^{-v}};
  \]
- **ReLU**
  \[
  \operatorname{ReLU}(v)=\max(0,v);
  \]
- **Linear**
  \[
  y=v.
  \]

### 2. Why a hidden layer is needed

A single layer of linear neurons computes

\[
\mathbf y=W\mathbf x+\mathbf b.
\]

A composition of linear layers is still linear:

\[
W_2(W_1\mathbf x)=W_2W_1\mathbf x.
\]

Therefore adding linear layers does not increase representational power. Nonlinear activations between layers are essential. A multilayer FFNN can represent nonlinear boundaries and functions through compositions of simpler transformations.

### 3. Layer organization

A typical FFNN has:

- an **input layer** with one unit per feature;
- one or more **hidden layers**;
- an **output layer** with units for the target variables.

Every unit in layer \(l+1\) is normally connected to every unit in layer \(l\). This is a fully connected feed-forward architecture. A recurrent architecture, by contrast, feeds outputs back to later inputs; a self-organizing network may also use a topology unlike the standard FFNN.

### 4. Forward propagation

Let \(W^{(l)}\) be the weight matrix from layer \(l\) to \(l+1\), and \(b^{(l)}\) the bias vector. Matrix notation is

\[
\mathbf a^{(l+1)}
=\phi\left(W^{(l)}\mathbf a^{(l)}+\mathbf b^{(l)}\right).
\]

The input layer stores \(\mathbf a^{(0)}=\mathbf x\). The final output is

\[
\hat{\mathbf y}=\mathbf a^{(L)}.
\]

There is no backward connection during this forward pass. Backpropagation is used only during training to compute gradients.

### 5. Activation functions

#### Sigmoid

The logistic sigmoid maps any real value to \((0,1)\):

\[
\sigma'(v)=\sigma(v)(1-\sigma(v)).
\]

It is useful for binary probability outputs, but its derivative becomes small for large positive or negative \(v\), causing vanishing gradients.

#### Hyperbolic tangent

Tanh maps to \((-1,1)\), often centers data better than sigmoid, and can train more quickly. It also suffers from saturation for large magnitudes.

#### ReLU

ReLU is computationally simple and often used in deep networks. Its derivative is

\[
\operatorname{ReLU}'(v)=
\begin{cases}
1,&v>0,\\
0,&v<0.
\end{cases}
\]

At zero the derivative is conventionally chosen as 0 or another value. ReLU can produce dead units when their input remains negative.

#### Linear activation

A linear output unit allows negative and unrestricted outputs. It is standard for regression because nonlinear output activation may distort the target. The loss still needs to penalize error, so an unbounded linear output does not make the whole network incapable of learning.

### 6. Choosing the output layer

The output structure follows the target:

- **Binary classification:** one sigmoid unit; threshold at a chosen value such as 0.5.
- **Multiclass classification:** one softmax unit per class; select the highest probability.
- **Regression:** one linear unit for one continuous target.
- **Multiple regression:** one linear unit per target.
- **Multi-label classification:** several sigmoid units, each with its own binary decision.

The number of output units alone is not enough; the loss and output nonlinearity must match the target type.

### 7. Softmax and cross-entropy

For \(K\) classes, softmax produces

\[
p_k=\frac{e^{z_k}}{\sum_{j=1}^{K}e^{z_j}},
\qquad \sum_kp_k=1.
\]

Categorical cross-entropy is

\[
L=-\log p_y
\]

for the true class \(y\). The loss strongly penalizes assigning very low probability to the observed class.

### 8. Loss functions

#### Mean squared error

\[
L=\frac1N\sum_{n=1}^{N}(\hat y_n-y_n)^2.
\]

MSE is common for regression.

#### Mean absolute error

\[
L=\frac1N\sum_n|\hat y_n-y_n|.
\]

It is less sensitive to large residual outliers.

#### Binary cross-entropy

For \(y_n\in\{0,1\}\) and predicted probability \(p_n\),

\[
L=-\frac1N\sum_n
\left[y_n\log p_n+(1-y_n)\log(1-p_n)\right].
\]

#### Cross-entropy and softmax

\[
L=-\frac1N\sum_n\log p_{n,y_n}.
\]

#### Regularized objective

\[
J=L+\lambda R(\theta),
\]

where \(R\) can be the sum of squared weights (L2) or sum of absolute weights (L1).

### 9. Fully connected structure

If layer widths are

\[
(n_0,n_1,\ldots,n_L),
\]

a fully connected FFNN has

\[
\sum_{l=0}^{L-1}n_{l+1}(n_l+1)
\]

trainable weights and biases, assuming every adjacent pair is connected. Biases are included because there are \(n_{l+1}\) bias parameters per layer.

This count matters for data requirements, memory, and overfitting.

### 10. Activation and loss choice by task

| Task | Typical output activation | Typical loss |
|---|---|---|
| Binary classification | Sigmoid | Binary cross-entropy |
| Multiclass classification | Softmax | Categorical cross-entropy |
| Regression | Linear | MSE or MAE |
| Multilabel classification | Multiple sigmoids | Sum/average binary cross-entropy |

These are typical choices, not absolute laws. The data scaling, output meaning, and decision threshold still matter.

### 11. Data preprocessing

A network learns more reliably when:

- features are scaled to comparable ranges;
- missing values are handled explicitly;
- training and deployment preprocessing are identical;
- target values are transformed when the scale is extreme;
- labels are encoded consistently.

Min–max scaling is

\[
x'=\frac{x-x_{\min}}{x_{\max}-x_{\min}}.
\]

Standardization is

\[
x'=\frac{x-\mu}{\sigma}.
\]

The scaling parameters are learned from training data and then applied unchanged to validation and test data.

### 12. Architecture design choices

Important questions are:

1. How many input features are required?
2. Which target type and loss will be used?
3. How much nonlinear complexity is expected?
4. How much data is available?
5. Which layers are needed for a first baseline?
6. How will the network be regularized?
7. What latency and memory limits apply?
8. How will performance be validated?

A very large network is not automatically more accurate. Irrelevant units and parameters increase overfitting and cost.

### 13. Feed-forward network as a function approximator

A deep FFNN composes several functions:

\[
\hat{\mathbf y}
=\phi_L(W^{(L-1)}\cdots\phi_1(W^{(1)}\mathbf x+\mathbf b^{(1)})\cdots+\mathbf b^{(L-1)}).
\]

The hidden layers learn useful internal representations. The exact interpretation of a hidden unit is often not unique because many parameter settings can implement similar functions.

### 14. Initialization

Weights should not all be set to zero, because every hidden unit would compute the same signal and gradients could be symmetric. A common initialization is

\[
W\sim U\left(-\frac1{n_l},\frac1{n_l}\right)
\]

for tanh, or Xavier initialization

\[
W\sim U\left(-\sqrt{\frac6}{n_l+n_{l+1}}},
\sqrt{\frac6}{n_l+n_{l+1}}}\right)
\]

for tanh units. For ReLU, He initialization uses a scale related to

\[
\sqrt{\frac{2}{n_l}}.
\]

Initialization affects symmetry breaking and training behavior.

### 15. Forward pass versus training iteration

A trained network's inference is a single forward pass. Training repeats:

1. forward propagation;
2. loss calculation;
3. backpropagation;
4. gradient-based weight and bias update.

Inference does not update parameters. The weights are frozen unless online learning is explicitly enabled.

### 16. Advantages and limitations

**Advantages**

- Learns nonlinear relationships.
- Works with raw or transformed numerical features.
- Can adapt to patterns through training.
- Supports classification, regression, and feature transformation.

**Limitations**

- Data intensive.
- Can overfit.
- Training may reach local optima or suffer from unstable gradients.
- Predictions may be hard to explain.
- Scaling and architecture choices affect performance.
- A large network can be expensive and latency-heavy.

## Worked examples

### Example 1: One neuron

Let

\[
x_1=2,\quad x_2=-1,\quad
w_1=0.5,\quad w_2=-0.3,\quad b=0.1.
\]

Net input:

\[
v=0.5(2)-0.3(-1)+0.1=1.4.
\]

With sigmoid,

\[
y=\sigma(1.4)=\frac1{1+e^{-1.4}}\approx0.8022.
\]

### Example 2: Matrix forward pass

Suppose

\[
W^{(1)}=
\begin{bmatrix}
0.1&0.2\\
-0.3&0.4
\end{bmatrix},
\quad
b^{(1)}=
\begin{bmatrix}0\\0.1\end{bmatrix},
\]

\[
\mathbf x=\begin{bmatrix}1\\2\end{bmatrix},
\quad
\mathbf a^{(1)}=\begin{bmatrix}0.5\\1\end{bmatrix}.
\]

Then

\[
W^{(1)}\mathbf x=
\begin{bmatrix}0.5\\0.5\end{bmatrix},
\]

and after adding bias,

\[
\mathbf z^{(1)}=
\begin{bmatrix}0.5\\0.6\end{bmatrix}.
\]

With sigmoid activation,

\[
\mathbf a^{(1)}\approx
\begin{bmatrix}0.6225\\0.6457\end{bmatrix}.
\]

This is the hidden activation passed to the next layer.

### Example 3: Regression architecture

For predicting house price, use four input features, two hidden layers with 16 and 8 ReLU units, and one linear output. Squared error is a suitable base loss. A sigmoid output would be unsuitable unless prices were first normalized to \([0,1]\).

### Example 4: Multiclass architecture

For five classes, the output has five linear logits. Softmax converts them to class probabilities, and categorical cross-entropy compares them with the true class. Applying a separate sigmoid and then normalizing the five outputs is not equivalent to the standard softmax setup.

## Key terms & formulas

- **FFNN/MLFFN:** Feed-forward neural network with hidden layers
- **Neuron:** Weighted sum plus bias followed by activation
- **Hidden layer:** Layer between input and output
- **Forward propagation:** Input-to-output computation
- **Activation function:** Nonlinear transformation
- **Bias:** Offset in a weighted sum
- **Loss:** Objective measuring prediction error
- **Softmax:** Converts logits to class probabilities

Forward propagation:

\[
\mathbf a^{(l+1)}=\phi(W^{(l)}\mathbf a^{(l)}+\mathbf b^{(l)}).
\]

Sigmoid:

\[
\sigma(z)=\frac1{1+e^{-z}},\quad \sigma'(z)=\sigma(z)(1-\sigma(z)).
\]

Softmax:

\[
p_k=\frac{e^{z_k}}{\sum_je^{z_j}}.
\]

Parameter count for adjacent layers:

\[
n_{l+1}(n_l+1).
\]

## Common mistakes

1. **Building several linear layers and expecting nonlinear learning.** Insert nonlinear activations.
2. **Using a hidden layer with no units.** A layer that passes the input through is not a useful hidden representation.
3. **Choosing output activation and loss independently.** Match them to the target.
4. **Forgetting biases.** A network without them is tied to hyperplanes through the origin.
5. **Setting every weight to zero.** Hidden units are symmetric and learning is impaired.
6. **Scaling the test set with test statistics.** Learn preprocessing from training data.
7. **Confusing a feed-forward network with a recurrent one.** There are no feedback cycles in FFNN inference.
8. **Assuming a deeper network is always better.** Data, regularization, and optimization determine performance.

## Exam prep

### Likely 2-mark questions

- **Draw and explain the architecture of a multilayer FFNN.**  
  **Hint:** Input, hidden, output layers and fully connected weighted links.

- **Write the neuron equation.**  
  **Hint:** \(y=\phi(\sum w_ix_i+b)\).

- **State two common FFNN activation functions.**  
  **Hint:** Sigmoid, tanh, ReLU, or linear with uses.

- **Which output activation is appropriate for multiclass classification?**  
  **Hint:** Softmax, normally with categorical cross-entropy.

- **Why are hidden layers nonlinear?**  
  **Hint:** A composition of linear layers remains linear.

### Likely long-answer questions

- **Explain the architecture and forward propagation of an FFNN.**  
  **Hint:** Layers, weights, biases, activations, output structure, and matrix form.

- **Compare activation functions used in FFNNs.**  
  **Hint:** Range, gradient, saturation, dead units, task, and output choice.

- **Explain loss and output-layer selection for classification and regression.**  
  **Hint:** MSE/MAE for regression, sigmoid/softmax and cross-entropy for classification.

- **Describe the design of an FFNN for a specified application.**  
  **Hint:** Input/output units, hidden layers, preprocessing, loss, regularization, training, and validation.

- **Discuss advantages and limitations of FFNNs.**  
  **Hint:** Nonlinear approximation, learning, data dependence, overfitting, and interpretability.
