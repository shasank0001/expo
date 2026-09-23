---
subject: sc
unit: 3
topic: backpropagation
syllabus_ref: CSM3202 Unit-III
status: draft
---
# Back-Propagation Method

## Overview

Backpropagation calculates how the prediction error changes every weight and bias in a neural network. It applies the chain rule from the output back toward the input. A gradient optimizer then uses those derivatives to update the parameters.

For a multilayer feed-forward network, backpropagation is the standard supervised training method. It can solve problems that are not linearly separable, such as XOR, provided the architecture, activations, data, and optimization settings are suitable.

## Explanation

### 1. Objective of training

For \(N\) training examples, minimize a loss such as mean squared error:

\[
J=\frac1{2N}\sum_{n=1}^{N}
(\hat y_n-y_n)^2.
\]

The factor \(1/2\) is included because it cancels the derivative factor 2. The exact normalization depends on the loss convention.

Backpropagation computes

\[
\frac{\partial J}{\partial w},\qquad
\frac{\partial J}{\partial b}.
\]

Afterward, gradient descent updates

\[
w\leftarrow w-\eta\frac{\partial J}{\partial w},
\qquad
b\leftarrow b-\eta\frac{\partial J}{\partial b}.
\]

### 2. Forward pass

For one example, layer \(l\) receives

\[
\mathbf a^{(l-1)}
\]

and computes

\[
\mathbf z^{(l)}
=W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)},
\]

\[
\mathbf a^{(l)}=\phi^{(l)}(\mathbf z^{(l)}).
\]

The input is

\[
\mathbf a^{(0)}=\mathbf x,
\]

and the final activation is the prediction

\[
\hat y=\mathbf a^{(L)}.
\]

The forward pass stores intermediate values because backpropagation reuses them.

### 3. Output-layer error

For a single output and squared loss,

\[
\frac{\partial J}{\partial \hat y}
=\hat y-y.
\]

Define the output delta

\[
\delta^{(L)}=\frac{\partial J}{\partial \mathbf z^{(L)}}
=\frac{\partial J}{\partial \mathbf a^{(L)}}
\odot \phi'(\mathbf z^{(L)}).
\]

For a sigmoid output and squared error,

\[
\delta^{(L)}=(\hat y-y)\hat y(1-\hat y).
\]

If sigmoid output is paired with binary cross-entropy, the output derivative simplifies to

\[
\delta^{(L)}=\hat y-y.
\]

This is why loss and output activation must be considered together.

### 4. Backward pass for a layer

For any layer \(l\),

\[
\delta^{(l-1)}
=
\left(W^{(l)\mathsf T}\delta^{(l)}\right)
\odot\phi'(\mathbf z^{(l-1)}).
\]

The first factor carries the error backward through incoming connections. The elementwise activation derivative applies the local slope.

### 5. Weight and bias gradients

For the connection from layer \(l-1\) to layer \(l\),

\[
\frac{\partial J}{\partial W^{(l)}}
=
\delta^{(l)}\left(\mathbf a^{(l-1)}\right)^{\mathsf T}.
\]

For biases,

\[
\frac{\partial J}{\partial \mathbf b^{(l)}}
=
\delta^{(l)}.
\]

Each unit's error is multiplied by the activation that caused that unit's input.

### 6. Why the name “back-propagation” is used

The output error is propagated backward through the hidden layers. Each layer's delta depends on the delta of the layer after it. The process is efficient because the chain rule reuses derivatives rather than recalculating the loss for every parameter separately.

Backpropagation does not mean that data are sent backward during ordinary inference. The backward computation is needed for training; inference normally uses one forward pass.

### 7. Complete two-layer network derivation

Consider two inputs, two hidden sigmoid neurons, one sigmoid output, and squared-error loss.

Forward pass:

\[
z_1^{(1)}=w_{11}^{(1)}x_1+w_{12}^{(1)}x_2+b_1^{(1)},
\]

\[
z_2^{(1)}=w_{21}^{(1)}x_1+w_{22}^{(1)}x_2+b_2^{(1)},
\]

\[
h_j=\sigma(z_j^{(1)}),
\]

\[
z^{(2)}=v_1h_1+v_2h_2+b^{(2)},
\]

\[
\hat y=\sigma(z^{(2)}).
\]

Output delta:

\[
\delta_o=(\hat y-t)\hat y(1-\hat y).
\]

Gradients:

\[
\frac{\partial J}{\partial v_j}=\delta_oh_j,
\qquad
\frac{\partial J}{\partial b^{(2)}}=\delta_o.
\]

Hidden deltas:

\[
\delta_1=h_1(1-h_1)(v_1\delta_o),
\]

\[
\delta_2=h_2(1-h_2)(v_2\delta_o).
\]

Then

\[
\frac{\partial J}{\partial w_{j1}^{(1)}}=\delta_jx_1,
\]

\[
\frac{\partial J}{\partial w_{j2}^{(1)}}=\delta_jx_2,
\]

\[
\frac{\partial J}{\partial b_j^{(1)}}=\delta_j.
\]

### 8. Multiclass output

For a softmax output with categorical cross-entropy, the output delta is

\[
\delta^{(L)}=\mathbf p-\mathbf y,
\]

where \(\mathbf y\) is the one-hot target. Hidden deltas still use

\[
\delta^{(l-1)}
=
\left(W^{(l)\mathsf T}\delta^{(l)}\right)
\odot\phi'(\mathbf z^{(l-1)}).
\]

A common regression output is linear, so \(\phi'(z)=1\). For MSE and one output,

\[
\delta^{(L)}=\hat y-y.
\]

### 9. Batch, mini-batch, and stochastic gradients

For one example, the gradient is used directly. For a batch \(B\),

\[
\nabla_{W^{(l)}}J
=
\frac1{|B|}
\sum_{n\in B}
\delta_n^{(l)}
\left(\mathbf a_n^{(l-1)}\right)^{\mathsf T}.
\]

- **SGD:** one example per update.
- **Mini-batch:** a small group per update.
- **Batch gradient:** all examples per update.

Mini-batches often provide a practical balance between noise, hardware use, and stable gradients.

### 10. Learning rate

Gradient descent is

\[
W^{(l)}\leftarrow W^{(l)}-\eta\nabla_{W^{(l)}}J.
\]

If \(\eta\) is too small, learning is slow. If it is too large, the error may oscillate or diverge. Adaptive optimizers such as Adam use per-parameter learning rates, but their settings still require validation.

A learning-rate schedule may reduce the step size after the validation loss stops improving.

### 11. Initialization and local minima

All-zero weights create identical hidden units and symmetric gradients, preventing different hidden units from learning different features. Random or Xavier/He initialization breaks symmetry.

A deep nonconvex network can have local minima. Practical training uses suitable initialization, normalization, regularization, and optimization, and may use multiple restarts when resources permit. Backpropagation itself does not guarantee the global minimum.

### 12. Vanishing and exploding gradients

Repeatedly multiplying derivatives \(\phi'(z)\) can make gradients very small or very large.

- **Vanishing:** early layers learn very slowly, common with deep sigmoid/tanh networks.
- **Exploding:** large derivatives cause unstable updates.

ReLU, careful initialization, normalization, gradient clipping, residual connections, and good architecture can help. A smaller learning rate alone may slow learning without fixing the underlying scale.

### 13. Bias gradients

Bias gradients are not multiplied by an input activation, so

\[
\frac{\partial J}{\partial b}=\delta.
\]

Forgetting bias updates is a common implementation error. Biases shift a unit's activation threshold and often improve fitting.

### 14. Overfitting control

Backpropagation minimizes the training objective, not automatically generalization. Use:

- weight decay or L1/L2 regularization;
- early stopping;
- dropout;
- data augmentation;
- minibatch training;
- a smaller network;
- cross-validation;
- proper train/validation/test separation.

The objective may be

\[
J_{\text{total}}=J_{\text{data}}+\lambda R(\theta).
\]

### 15. Convergence and stopping

Training may stop when:

- a maximum epoch count is reached;
- training loss changes very little;
- validation loss has not improved for several epochs;
- the gradient norm is small;
- a wall-clock or memory limit is reached.

Small gradient norms do not always mean the model predicts well. Report validation and test metrics, not only the loss value.

## Worked examples

### 16. Worked training example with explicit simultaneous updates

Use a network with

\[
\mathbf x=(1,0),
\]

target \(t=1\),

\[
W^{(1)}=
\begin{bmatrix}
1&-1\\
1&1
\end{bmatrix},
\quad
\mathbf b^{(1)}=
\begin{bmatrix}0.5\\-0.5\end{bmatrix},
\]

\[
\mathbf v=(1,1),
\quad b^{(2)}=-0.5.
\]

Use sigmoid activations and the single-example loss

\[
J=\frac12(\hat y-t)^2.
\]

#### Forward pass

\[
z_1=1(1)-1(0)+0.5=1.5,
\]

\[
h_1=\sigma(1.5)\approx0.817574.
\]

\[
z_2=1(1)+1(0)-0.5=0.5,
\]

\[
h_2=\sigma(0.5)\approx0.622459.
\]

\[
z_o=1(0.817574)+1(0.622459)-0.5=0.940034,
\]

\[
\hat y=\sigma(0.940034)\approx0.719106,
\]

\[
J=\frac12(0.719106-1)^2\approx0.039451.
\]

#### Output delta and gradients

With \(\delta_o=\partial J/\partial z_o\),

\[
\delta_o=(\hat y-t)\hat y(1-\hat y)
=(-0.280894)(0.719106)(0.280894)
\approx-0.056738.
\]

The output gradients are

\[
\frac{\partial J}{\partial v_1}=\delta_oh_1\approx-0.046388,
\]

\[
\frac{\partial J}{\partial v_2}=\delta_oh_2\approx-0.035317,
\]

\[
\frac{\partial J}{\partial b^{(2)}}=\delta_o\approx-0.056738.
\]

With learning rate \(\eta=0.5\), the updated output parameters are

\[
v_1'=1-0.5(-0.046388)=1.023194,
\]

\[
v_2'=1-0.5(-0.035317)=1.017659,
\]

\[
b^{(2)\prime}=-0.5-0.5(-0.056738)=-0.471631.
\]

#### Hidden deltas and gradients

Use the parameters from the original forward pass, because a standard simultaneous update computes all gradients first.

\[
\delta_1
=h_1(1-h_1)v_1\delta_o
\approx0.817574(0.182426)(1)(-0.056738)
\approx-0.008462,
\]

\[
\delta_2
=h_2(1-h_2)v_2\delta_o
\approx0.622459(0.377541)(1)(-0.056738)
\approx-0.013334.
\]

The hidden gradients are

\[
\frac{\partial J}{\partial w_{11}}=\delta_1x_1=-0.008462,\qquad
\frac{\partial J}{\partial w_{12}}=\delta_1x_2=0,
\]

\[
\frac{\partial J}{\partial b_1}=\delta_1=-0.008462,
\]

\[
\frac{\partial J}{\partial w_{21}}=\delta_2x_1=-0.013334,\qquad
\frac{\partial J}{\partial w_{22}}=\delta_2x_2=0,
\]

\[
\frac{\partial J}{\partial b_2}=\delta_2=-0.013334.
\]

The simultaneous updates are

\[
w_{11}'=1.004231,\qquad w_{12}'=-1,\qquad b_1'=0.504231,
\]

\[
w_{21}'=1.006667,\qquad w_{22}'=1,\qquad b_2'=-0.493333.
\]

Because \(x_2=0\), both weights receiving the gradient from \(x_2\) remain unchanged.

#### Verify the new prediction

Using every updated parameter together:

\[
h_1'=\sigma(1(1.004231)-1(0)+0.504231)
=\sigma(1.508462)\approx0.818833,
\]

\[
h_2'=\sigma(1(1.006667)+1(0)-0.493333)
=\sigma(0.513334)\approx0.625588.
\]

\[
z_o'=1.023194(0.818833)+1.017659(0.625588)-0.471631
\approx1.002829,
\]

\[
\hat y'=\sigma(1.002829)\approx0.731614.
\]

The loss becomes

\[
J'=\frac12(0.731614-1)^2\approx0.036015<0.039451.
\]

The one step moved the prediction toward the target, as expected.

### 17. Training on a complete dataset

A practical epoch uses minibatches:

1. shuffle or select a batch;
2. run forward propagation;
3. compute loss;
4. run backpropagation for the batch;
5. accumulate or apply gradients;
6. repeat over batches;
7. evaluate validation loss;
8. save the best checkpoint.

Shuffling helps generalization when batches are formed by consecutive ordered records.

### 18. Classification and regression examples

For binary classification, use a sigmoid output and binary cross-entropy, or a two-logit softmax when the two classes are presented symmetrically. Choose a decision threshold using validation data rather than assuming 0.5 is always best.

For regression, use a linear output and MSE/MAE. If the target has a bounded range, transform it or use a bounded activation deliberately, and evaluate in the original units.

## Key terms & formulas

- **Backpropagation:** Chain-rule gradient computation through a network.
- **Forward pass:** Compute activations from input to output.
- **Backward pass:** Compute deltas and parameter gradients from output to input.
- **Delta:** Sensitivity of the loss to a neuron's weighted input.
- **Gradient descent:** Update parameters using the negative gradient.
- **Chain rule:** Differentiate a composition of functions.
- **Epoch:** Complete pass over training data.
- **Learning rate:** Size of a gradient update.

Layer forward:

\[
\mathbf a^{(l)}=\phi(W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)}).
\]

Layer backward:

\[
\delta^{(l-1)}
=
\left(W^{(l)\mathsf T}\delta^{(l)}\right)
\odot\phi'(\mathbf z^{(l-1)}).
\]

Gradients:

\[
\frac{\partial J}{\partial W^{(l)}}=\delta^{(l)}(\mathbf a^{(l-1)})^{\mathsf T},
\qquad
\frac{\partial J}{\partial \mathbf b^{(l)}}=\delta^{(l)}.
\]

Update:

\[
\theta\leftarrow\theta-\eta\frac{\partial J}{\partial\theta}.
\]

## Common mistakes

1. **Calling the forward pass backpropagation.** Backpropagation is the gradient pass used for training.
2. **Forgetting biases.** Include both weight and bias updates.
3. **Using \(1-y\) instead of \(\sigma'(z)\).** The derivative depends on the activation and its preactivation.
4. **Reusing updated weights during the same backward pass.** Save the forward-pass values and compute all gradients before updating.
5. **Using \(\delta=\text{error}\) at every layer.** The hidden delta must pass through incoming weights and the hidden activation derivative.
6. **Using a learning rate that is too large.** The error can oscillate or diverge.
7. **Setting all weights to zero.** Symmetric hidden units learn the same pattern.
8. **Assuming backpropagation always finds the global minimum.** It is a local gradient method.
9. **Combining sigmoid output with cross-entropy but using the wrong output delta.** The derivative simplifies only with the matching loss.
10. **Judging convergence by training error only.** Use validation data.

## Exam prep

### Likely 2-mark questions

- **What is backpropagation?**  
  **Hint:** Efficient chain-rule computation of loss gradients from output toward input.

- **Write the backpropagation equation for a layer delta.**  
  **Hint:** \(\delta^{l-1}=(W^{lT}\delta^l)\odot\phi'(z^{l-1})\).

- **State the weight-gradient formula.**  
  **Hint:** \(\partial J/\partial W^l=\delta^l(a^{l-1})^T\).

- **Why are sigmoid activations differentiable?**  
  **Hint:** They have a smooth derivative \(\sigma(z)(1-\sigma(z))\).

- **What does the learning rate control?**  
  **Hint:** The size of each gradient update.

### Likely long-answer questions

- **Derive backpropagation for a two-layer feed-forward network.**  
  **Hint:** Forward equations, output delta, hidden deltas, weight/bias gradients, and updates.

- **Perform one complete backpropagation training step numerically.**  
  **Hint:** Show input, target, all activations, deltas, gradients, and updated parameters.

- **Explain why a multilayer network can learn XOR but a single perceptron cannot.**  
  **Hint:** Nonzero hidden representation, nonlinear composition, and linear separability.

- **Compare backpropagation with perceptron learning.**  
  **Hint:** Hidden layers, differentiable loss, chain rule, nonlinear targets, and convergence conditions.

- **Discuss practical issues in backpropagation training.**  
  **Hint:** Initialization, learning rate, vanishing/exploding gradients, local minima, overfitting, and stopping.
