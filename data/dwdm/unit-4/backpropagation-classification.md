---
subject: dwdm
unit: 4
topic: backpropagation-classification
syllabus_ref: CSM3101 Unit-IV
status: draft
---
# Classification by Backpropagation

## Overview

Backpropagation trains a multilayer neural network by sending errors backward through its connections. For classification, input attributes pass forward through hidden layers and produce class scores or probabilities. A loss function compares predictions with known labels, and gradient descent updates weights to reduce the error. Backpropagation is efficient for learning complex nonlinear boundaries, but it needs enough representative data, appropriate scaling, regularization, and validation.

## Explanation

### 1. Network structure

A feedforward network has an input layer, one or more hidden layers, and an output layer. Each neuron computes a weighted sum and applies an activation:

\[
z_j=\sum_i w_{ji}x_i+b_j,\qquad h_j=f(z_j).
\]

For binary classification, one sigmoid output can represent \(P(y=1)\):

\[
\sigma(z)=\frac{1}{1+e^{-z}}.
\]

For \(K\) classes, a softmax output gives a probability vector:

\[
P(y=k\mid x)=\frac{e^{z_k}}{\sum_j e^{z_j}}.
\]

The output and loss must match the task; a softmax should normally be paired with multiclass cross-entropy.

### 2. Forward propagation

Given weights and an input vector, the forward pass computes the hidden activations and output. The prediction is the class with the largest output for multiclass classification, or a thresholded probability for binary classification. During training, all intermediate activations are saved because the backward pass needs them.

### 3. Loss functions

Binary cross-entropy is

\[
L=-\left[y\log p+(1-y)\log(1-p)\right].
\]

For \(K\)-class softmax labels, multiclass cross-entropy is

\[
L=-\sum_{k=1}^{K}y_k\log p_k,
\]

where exactly one \(y_k\) is 1 for a single-label example. Mean loss over the batch is used for gradient estimates. Cross-entropy penalizes confident wrong predictions strongly.

### 4. Backpropagation

The backward pass applies the chain rule from the output toward the input. For a simple linear unit \(z=wx+b\), the derivative is

\[
\frac{\partial z}{\partial w}=x,\qquad
\frac{\partial z}{\partial b}=1.
\]

At each neuron, the incoming error gradient is multiplied by the derivative of its activation. Weight gradients are the incoming gradient times the previous activation. For logistic sigmoid,

\[
\sigma'(z)=\sigma(z)(1-\sigma(z)).
\]

The gradients tell the direction in which a small weight change increases or decreases the loss. The optimizer moves in the negative-gradient direction:

\[
w_{ji}\leftarrow w_{ji}-\eta\frac{\partial L}{\partial w_{ji}},
\]

where \(\eta\) is the learning rate.

### 5. Optimization and training loop

A common loop is:

1. shuffle or sample a minibatch;
2. forward pass;
3. calculate mean loss;
4. backward pass;
5. gradient-descent update;
6. repeat for epochs.

Full-batch gradient descent uses all examples per update; stochastic gradient descent uses one; minibatch gradient descent is a practical compromise. Learning rate, momentum, weight decay, and initialization affect convergence. A loss that oscillates may indicate a rate that is too high; a loss that barely moves may indicate a rate, scaling, or architecture problem.

### 6. Scaling, initialization, and activation functions

Inputs with very different scales can make optimization slow or unstable. Standardize numeric features using training statistics. ReLU is common in hidden layers because it avoids saturation compared with sigmoid; tanh and sigmoid can still be useful. Initialize weights so activations have reasonable variance. Biases often start near zero. Neural networks do not need all inputs to be Gaussian, but preprocessing remains important.

### 7. Overfitting and validation

A network can memorize training examples, especially with many parameters. Use a validation set, regularization such as L2 or dropout, early stopping, data augmentation where valid, and an appropriately sized network. A validation curve can choose the epoch and regularization strength. The test set remains untouched.

### 8. Interpretability and limitations

A network can model interactions and nonlinear boundaries well, but its many weights are difficult to explain. Local explanations, feature perturbation, or attention-like diagnostics are not proof of causality. Neural training can be sensitive to initialization and preprocessing. It usually needs more data and computation than a simple tree or Bayes model, although performance depends on the problem.

## Worked examples

### Example 1: One sigmoid output

Suppose \(x_1=0.8,x_2=0.2\), \(w_1=1,w_2=-0.5,b=0.1\). Then

\[
z=0.8-0.1+0.1=0.8,\quad p=\sigma(0.8)\approx0.690.
\]

If the label is \(y=1\),

\[
L=-[\log(0.690)]\approx0.371.
\]

The prediction is positive at a 0.50 threshold. The error tells the optimizer how output probability should change; the backward pass propagates that error through every weight.

### Example 2: XOR with a hidden layer

XOR is not linearly separable, but a network with one or more hidden nonlinear units can represent it. Let hidden unit \(h=\sigma(2x_1+2x_2-3)\), approximately 0 for (0,0), 1 for (0,1) and (1,0), and approximately 1 for (1,1). A second hidden unit can respond to the (1,1) region. The output combines them to produce high values only for opposite bits. Repeated gradient updates find weights and biases; the exact values depend on initialization and stopping.

### Example 3: Softmax classification

For three class scores \(z=(2,1,0)\),

\[
e^z=(7.389,2.718,1),\quad
p=(0.665,0.245,0.090).
\]

The class is 1. If the true class is 3, cross-entropy is

\[
-\log(0.090)\approx2.408.
\]

A large loss appropriately reflects a confidently incorrect prediction.

### Example 4: Weight-gradient intuition

If a neuron has input activation 0.8 and incoming gradient 0.5, the weight gradient magnitude is \(0.8(0.5)=0.4\), before summing over examples or using a batch factor. With learning rate 0.01, one update reduces that weight by 0.004. This is why large input scales can produce large updates.

## Key terms & formulas

- **Neuron/unit:** weighted sum plus activation.
- **Forward propagation:** input to output computation.
- **Backpropagation:** chain-rule gradient computation from output to inputs.
- **Gradient descent:** update opposite the loss gradient.
- **Learning rate \(\eta\):** update size.
- **Epoch:** one pass over training data.
- **Sigmoid:** \(1/(1+e^{-z})\), binary output.
- **Softmax:** normalized class scores.
- **Cross-entropy:** loss for probabilistic classification.
- **L2 regularization/dropout/early stopping:** overfitting controls.
- **Minibatch:** small group used for one update.

## Common mistakes

1. **Using softmax with a binary target unnecessarily:** use a scalar sigmoid or two-class setup consistently.
2. **Forgetting the sigmoid derivative:** the chain rule requires the activation derivative.
3. **Updating weights in the positive-gradient direction:** descent uses a negative update.
4. **Using test data to choose the learning rate or epoch:** tune on validation.
5. **Leaving numeric features on incompatible scales:** optimize slowly or unstably.
6. **Reporting training loss as classification quality:** evaluate held-out accuracy, calibration, and cost.
7. **Assuming a complex network is always better:** compare with simple baselines.

## Exam prep

**Likely 2-mark questions**
1. What is backpropagation? *Hint: chain-rule computation of error gradients through a network.*
2. State the sigmoid formula. *Hint: \(1/(1+e^{-z})\).*
3. Why use early stopping? *Hint: limit overfitting by selecting a validation epoch.*

**Likely long-answer questions**
1. Explain forward and backward passes for a neural classifier. *Hint: activations, loss, derivatives, gradient accumulation, update.*
2. Compare sigmoid and softmax outputs and their losses. *Hint: binary versus multiclass probability normalization.*
3. Derive the update for a simple neuron. *Hint: chain rule, input activation, learning rate, negative gradient.*
4. Discuss practical training choices and failure modes. *Hint: scaling, initialization, minibatches, overfitting, validation.*
