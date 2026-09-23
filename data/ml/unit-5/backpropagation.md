---
subject: ml
unit: 5
topic: backpropagation
syllabus_ref: CSM3201 Unit-V
status: draft
---
# Backpropagation

## Overview

Backpropagation is an algorithm for computing the derivatives of a network's loss with respect to its weights and biases. It applies the chain rule from the output backwards through the computation graph. The resulting gradients are used by gradient descent or another optimiser to update the network.

Backpropagation is not a separate learning rule; it is the efficient credit-assignment step that makes neural-network training practical. Its correctness depends on a clear forward computation, a scalar loss, differentiable operations, and correct handling of shapes, batches, and regularisation.

## Explanation

### Forward computation graph

For a layer,

\[
Z^{(\ell)}=W^{(\ell)}A^{(\ell-1)}+b^{(\ell)},\qquad
A^{(\ell)}=\phi(Z^{(\ell)}).
\]

The output layer produces \(\hat y=A^{(L)}\), and the scalar loss is

\[
J=\frac1B\sum_{i=1}^{B}L(y_i,\hat y_i),
\]

where \(B\) is a mini-batch size. Every intermediate value and operation is recorded conceptually so the backward pass can reuse them.

### Chain rule

If \(u=\phi(z)\), then

\[
\frac{\partial u}{\partial z}=\phi'(z).
\]

For an affine layer,

\[
z^{(\ell)}=W^{(\ell)}a^{(\ell-1)}+b^{(\ell)},
\]

so, for a scalar loss and a compatible batched derivative,

\[
\frac{\partial J}{\partial W^{(\ell)}}=\delta^{(\ell)}
\bigl(a^{(\ell-1)}\bigr)^\top,
\qquad
\frac{\partial J}{\partial b^{(\ell)}}=\delta^{(\ell)},
\]

where \(\delta^{(\ell)}\) is the error signal for layer \(\ell\). The transpose and averaging over the batch must be implemented with the correct orientation and shape.

### Error signal recursion

Let \(\delta^{(\ell)}=\partial J/\partial z^{(\ell)}\). The output-layer signal is

\[
\delta^{(L)}=\nabla_{\hat y}\mathcal L
\odot \phi'(Z^{(L)}),
\]

where \(\odot\) is elementwise multiplication. For a fully connected hidden layer,

\[
\delta^{(\ell)}
=\left((W^{(\ell+1)})^\top\delta^{(\ell+1)}\right)
\odot\phi'(Z^{(\ell)}).
\]

This sends credit backwards: an earlier unit is updated according to both how its activation affects the loss and how sensitive the later computation is to that activation.

### A scalar derivation example

Let \(z=wx+b\), \(a=\phi(z)\), and \(L=\frac12(a-y)^2\). Then

\[
\frac{\partial L}{\partial a}=a-y,
\qquad
\frac{\partial a}{\partial z}=\phi'(z),
\]

\[
\frac{\partial L}{\partial z}=(a-y)\phi'(z),
\]

\[
\frac{\partial L}{\partial w}=(a-y)\phi'(z)x,
\qquad
\frac{\partial L}{\partial b}=(a-y)\phi'(z).
\]

For a squared error the derivative has a factor of 2; the \(1/2\) in the loss cancels it.

### Classification example

For a binary output logit \(z\), sigmoid \(p=\sigma(z)\), and binary cross-entropy, the combined derivative is

\[
\frac{\partial L}{\partial z}=p-y.
\]

If the preceding hidden activation is \(a\) and weights multiply \(z=wa+b\), then

\[
\frac{\partial L}{\partial w}=(p-y)a,\qquad
\frac{\partial L}{\partial b}=p-y.
\]

This simplification is why frameworks often combine a sigmoid/BCE or softmax/cross-entropy operation as a numerically stable unit.

### Update after backpropagation

Once gradients are known, an optimiser updates parameters, e.g.

\[
W\leftarrow W-\eta\frac{\partial J}{\partial W}.
\]

The backward pass is repeated for every mini-batch. Regularisation adds a gradient, for example \(\lambda W\) for an \(L_2\) penalty. The order is usually zero gradients, forward pass, loss, backward pass, update.

### Important implementation issues

- Maintain shapes: for \(W\in\mathbb R^{d_{\text{out}}\times d_{\text{in}}}\), its gradient has the same shape.
- Average or sum over the batch consistently with the loss and learning rate.
- Handle the final bias derivative separately when summing examples.
- Avoid division by zero in ReLU/derivatives; use a convention at zero.
- Use stable log-sum-exp for softmax and cross-entropy.
- Check gradients numerically for small random networks.
- Detach or otherwise prevent accidental gradient flow when doing inference or a frozen component.

### Vanishing and exploding gradients

Repeated multiplication by \(\phi'\) and weights can make gradients shrink toward zero or grow rapidly. Consequences are slow early-layer learning, unstable updates, and poor convergence. Remedies include suitable initialisation, residual connections, normalisation, ReLU-family activations, careful scaling, clipping, and architectural design. Backpropagation itself does not cause all such behaviour; the computation graph and parameters do.

### Backpropagation and interpretation

A gradient says how a local loss changes under a small parameter change, not why a human made a decision. It is useful for optimisation, debugging, saliency-based analysis, and constraint methods, but it is not automatically a causal explanation. Gradient-based explanations can be unstable and sensitive to baseline and perturbation.

### Efficient computation and debugging

Backpropagation reuses intermediate derivatives rather than recomputing every partial derivative independently. For a feed-forward network this is efficient because the computation graph is a directed acyclic graph. Recurrent networks unroll time, which increases graph size; activation checkpointing or recomputation trades memory for computation. Convolutional and attention layers use structured operations so that many weights can be processed efficiently, but the mathematical chain rule is unchanged.

When a gradient is wrong, isolate a tiny network and compare the analytical result with a central finite difference:

\[
\frac{\partial J}{\partial \theta_i}\approx
\frac{J(\theta+\epsilon e_i)-J(\theta-\epsilon e_i)}{2\epsilon}.
\]

Use a small \(\epsilon\), double precision if needed, and inspect each layer separately. Common failures are an incorrect derivative, a missing mean over the batch, wrong transpose, an activation evaluated at \(a\) instead of \(z\), a forgotten residual connection, or an in-place operation that alters a value needed by an earlier operation.

A safe training step is:

```text
zero gradients -> forward pass -> compute scalar loss
             -> backward pass -> inspect/clip gradients -> update
```

Do not detach a tensor that still needs a gradient, and do not retain an inference graph unnecessarily. Include regularisation in the graph so its parameter gradient is included. A finite-difference check on a small random network is one of the most effective ways to confirm an implementation.

## Worked examples

### Example 1: one-neuron update

Let \(w=0.5,x=2,b=0,y=1\), and use \(a=w x\), with \(L=\frac12(a-y)^2\). Then \(a=1\), error derivative \(a-y=0\), so the gradient is 0 and no update occurs. This illustrates a stationary point for this simple objective.

### Example 2: hidden-layer chain rule

Suppose the output derivative with respect to a hidden pre-activation is 0.2 and the hidden activation derivative is 0.5. The error signal at that hidden unit is \(0.2\times0.5=0.1\). If its input activation is 3, the weight gradient is 0.3. Multiplying local derivatives propagates the loss influence backward.

### Example 3: mini-batch gradient

If each of 32 examples gives a weight gradient of 0.5 and the loss is averaged, the batch gradient is 0.5. If the implementation sums instead, the update is 32 times larger unless the learning rate is adjusted.

### Example 4: gradient check

For a small scalar parameter \(w\), compare

\[
\frac{J(w+\epsilon)-J(w-\epsilon)}{2\epsilon}
\]

with the analytical derivative. Agreement within a small tolerance catches sign, transpose, and missing-term errors.

## Key terms & formulas

- **Backpropagation:** backward computation of loss derivatives.
- **Forward pass:** compute activations and prediction.
- **Computation graph:** operations and dependencies used for differentiation.
- **Chain rule:** derivative of a composition is the product of local derivatives.
- **Error signal:** \(\delta^{(\ell)}=\partial J/\partial z^{(\ell)}\).
- **Weight gradient:** \(\partial J/\partial W\).
- **Bias gradient:** \(\partial J/\partial b\).
- **Elementwise product:** \(\odot\).
- **Vanishing gradient:** gradient becomes too small at earlier layers.
- **Exploding gradient:** gradient becomes too large and destabilises updates.
- **Numerical gradient check:** finite-difference verification.
- **Stable softmax:** subtract the maximum logit before exponentiation.
- **Gradient clipping:** limiting large gradient norms.
- **L2 gradient contribution:** \(\lambda W\).

## Common mistakes

1. **Using the derivative of the activation at the wrong pre-activation.** Keep \(z\) and \(a\) distinct.
2. **Forgetting the chain rule.** A local derivative alone is not a loss gradient.
3. **Getting matrix orientations wrong.** The weight-gradient shape must match the weight.
4. **Summing instead of averaging batch gradients.** This changes the effective learning rate.
5. **Omitting the bias gradient.** The network loses an offset degree of freedom.
6. **Dividating by zero at ReLU's corner.** Use a safe convention.
7. **Treating backpropagation as an explanation.** It is primarily an optimisation algorithm.
8. **Checking no gradients in a debugging run.** A NaN/zero gradient can reveal implementation or data problems.

## Exam prep

### Likely 2-mark questions

- **What is backpropagation?** An efficient chain-rule computation of loss gradients from output to input.
- **State the error-signal recursion.** \(\delta^{(\ell)}=(W^{(\ell+1)})^\top\delta^{(\ell+1)}\odot\phi'(Z^{(\ell)})\).
- **What is a gradient check?** Comparing analytical gradients with finite differences.
- **Give two causes of vanishing gradients.** Sigmoid/tanh saturation, poor initialisation, or repeated multiplication through layers.

### Long-answer prompts

- **Derive the gradient of a simple neuron.** Show the chain rule for activation, weight, and bias.
- **Explain the backpropagation algorithm step by step.** Include forward pass, loss, recursion, parameter gradients, and update.
- **Compare sigmoid/BCE and softmax/cross-entropy gradients.** Explain the \(p-y\) simplification and numerical stability.
- **Discuss vanishing and exploding gradients.** Give mathematical intuition, symptoms, and remedies.
