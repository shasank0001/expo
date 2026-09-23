---
subject: ml
unit: 5
topic: learning-in-ann
syllabus_ref: CSM3201 Unit-V
status: draft
---
# Learning Process in an ANN

## Overview

Learning in an artificial neural network is the process of adjusting weights and biases so that its predictions minimise a chosen loss on training data and generalise to new data. The process involves a forward pass, an error calculation, a backward pass using derivatives, and an update. Repetition over many examples and epochs gradually changes the network's function.

Learning is not simply memorising data. It uses feedback, but the representation, loss, optimiser, and validation protocol determine what is learned. A network can overfit, underfit, get stuck in a poor minimum, or fail to generalise.

## Explanation

### The supervised learning process

For a training example \((x_i,y_i)\):

1. **Forward propagation:** compute \(A^{(0)}=x_i\), then
   \[
   Z^{(\ell)}=W^{(\ell)}A^{(\ell-1)}+b^{(\ell)},\quad
   A^{(\ell)}=\phi(Z^{(\ell)})
   \]
   through all layers, producing \(\hat y_i\).
2. **Loss:** compute \(L_i=L(y_i,\hat y_i)\), often averaged over a mini-batch.
3. **Backward propagation:** apply the chain rule to obtain \(\partial L_i/\partial W^{(\ell)}\) and \(\partial L_i/\partial b^{(\ell)}\).
4. **Update:** use an optimiser such as
   \[
   W^{(\ell)}\leftarrow W^{(\ell)}-\eta\frac{\partial J}{\partial W^{(\ell)}}.
   \]
5. **Repeat:** shuffle or sample batches, use multiple epochs, and monitor validation.

The loss may be squared error for regression, binary cross-entropy with one sigmoid logit for binary classification, categorical cross-entropy with softmax for multiclass, or another task-specific objective.

### Batch, stochastic, and mini-batch learning

- **Batch:** all training examples contribute to one update. Stable but expensive per update.
- **Stochastic:** one example per update. Noisy and often slow to converge computationally.
- **Mini-batch:** a small group, common in deep learning. It balances gradient noise, memory, and hardware utilisation.

The learning rate \(\eta\) and batch size interact. Large batches may need a larger learning rate or different scaling. Gradient accumulation can simulate a large batch but changes optimisation dynamics and memory use.

### Optimisers

Plain SGD uses the mini-batch gradient. **Momentum** accumulates velocity:

\[
v_t=\mu v_{t-1}+(1-\mu)g_t,\qquad
\theta_{t+1}=\theta_t-\eta v_t.
\]

**Adaptive methods** such as Adam maintain running first- and second-moment estimates:

\[
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,
\]

\[
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,
\]

\[
\theta_{t+1}=\theta_t-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.
\]

These methods often converge quickly, but weight decay, learning-rate schedules, and calibration still require care.

### Initialisation

Parameters should not all start at the same value. Initialisation affects symmetry, signal scale, and gradient scale. Common schemes include Xavier/Glorot and He/Kaiming, with the latter suited to ReLU networks. Poor initialisation can cause vanishing/exploding signals or dead units.

### Normalisation and conditioning

Inputs are often standardised using training-set statistics. Batch normalisation normalises intermediate activations using mini-batch statistics; layer normalisation normalises across features for each example. Both can stabilise optimisation, but they introduce dependencies and deployment behaviour that must be implemented correctly. A train/evaluation discrepancy can produce bad predictions.

### Learning curves and stopping

Plot training and validation loss across epochs. If both remain high, the model may be underfitting, features may be poor, or optimisation may be stuck. If training falls while validation rises, the model is overfitting. Use regularisation, more data, augmentation, and early stopping. The best validation checkpoint, not necessarily the last epoch, is selected.

### Generalisation and regularisation

Regularisation can include \(L_2\) penalty,

\[
J_{\text{total}}=J_{\text{data}}+\frac{\lambda}{2}\|W\|_2^2,
\]

\(L_1\) penalty, dropout, data augmentation, and early stopping. These methods constrain effective capacity or reduce reliance on brittle features. The regularisation strength is a hyper-parameter selected without using the test set.

### Unsupervised and self-supervised learning in ANNs

An ANN can learn without class labels by reconstructing inputs (autoencoder), predicting masked inputs (self-supervision), or learning a policy from reward. The learning loop still uses a loss or objective, but the target is generated from the data or environment. A representation learned this way may be useful for downstream supervised tasks.

### Diagnosing the learning process

A training run should be inspected at several levels:

- **Data level:** are inputs scaled, labels correct, and batches shuffled without leakage?
- **Forward level:** do activations have a reasonable scale, and is the output compatible with the loss?
- **Backward level:** are gradients finite, non-zero where expected, and of a sensible norm?
- **Update level:** does the learning rate produce progress without oscillation?
- **Generalisation level:** do validation curves and subgroup slices reveal overfitting or bias?

If gradients are zero everywhere, check the loss–activation pair, detached tensors, an overly small learning rate, or saturated/units that are inactive. If gradients explode, inspect input scaling, initialisation, learning rate, normalisation, and numerical stability. If training loss is NaN, inspect invalid values, division by zero, extreme logits, and mixed precision ranges. If validation is poor while training is excellent, inspect data splits, augmentation, model capacity, and label quality before simply adding layers.

Learning rate range tests and short pilot runs are useful: sweep several orders of magnitude for a few hundred steps, record loss and gradient norms, and then tune more carefully. A schedule such as reducing the rate after a plateau can improve convergence, but the validation checkpoint remains the model-selection decision.

## Worked examples

### Example 1: one update

Suppose a parameter is \(w=2\), learning rate \(\eta=0.1\), and the batch gradient is 8. Then

\[
w_{\text{new}}=2-0.1(8)=1.2.
\]

The network moves in the direction that reduces the loss, assuming the local gradient is correct.

### Example 2: mini-batch

A batch contains 32 examples. The loss is averaged over the batch, so each example contributes \(1/32\) to the gradient. Changing batch composition changes gradient noise and can affect generalisation.

### Example 3: learning curves

Training loss falls from 1.0 to 0.2, validation loss falls to 0.4 and then rises to 0.6. The best checkpoint is near epoch 25. Continuing to epoch 100 would improve training fit but likely hurt deployment performance.

### Example 4: ReLU initialisation

For a layer with large fan-in, He initialisation uses a variance scaled differently from Xavier because ReLU halves positive activations. This helps preserve signal and gradient scale. It is not a guarantee of good learning.

## Key terms & formulas

- **Learning:** adjusting parameters to reduce an objective and generalise.
- **Forward pass:** compute the prediction.
- **Backward pass:** compute gradients using the chain rule.
- **Batch:** examples used together for one update.
- **Epoch:** one pass over the training data.
- **Gradient descent:** \(\theta\leftarrow\theta-\eta\nabla J\).
- **SGD:** stochastic gradient descent.
- **Momentum:** velocity based on past gradients.
- **Adam:** adaptive optimiser with first/second moments.
- **Initialisation:** starting values for parameters.
- **Xavier/He initialisation:** variance schemes for stable signals.
- **Batch/layer normalisation:** normalisation of intermediate features.
- **Learning curve:** loss or metric over training steps/epochs.
- **Early stopping:** stop when validation performance no longer improves.
- **L2 regularisation:** \(\lambda\|W\|_2^2/2\) added to loss.

## Common mistakes

1. **Updating parameters without a loss or gradient.** The learning objective is missing.
2. **Using the same parameter value for every unit.** Symmetry prevents differentiated learning.
3. **Choosing an inappropriate learning rate.** Too high diverges; too low is slow.
4. **Ignoring validation curves.** Low training loss can mean overfitting.
5. **Using test loss to tune optimisation.** The test set becomes contaminated.
6. **Failing to save the best checkpoint.** The last epoch may be worse.
7. **Confusing an epoch with a step.** An epoch contains many mini-batch updates.

## Exam prep

### Likely 2-mark questions

- **List four steps in ANN learning.** Forward pass, loss, backpropagation, parameter update, and repeat.
- **State the gradient descent update.** \(\theta_{t+1}=\theta_t-\eta\nabla J\).
- **What is an epoch?** One full pass through the training examples.
- **What is early stopping?** Saving the best validation state and stopping when improvement ends.

### Long-answer prompts

- **Explain the learning process of a supervised ANN.** Cover forward propagation, loss, gradients, optimiser, epochs, and validation.
- **Compare batch, stochastic, and mini-batch gradient descent.** Discuss cost, noise, convergence, and hardware.
- **Explain overfitting and underfitting in neural networks.** Use learning curves and remedies.
- **What is the role of initialisation and normalisation?** Discuss signal scale, vanishing/exploding gradients, and implementation.
