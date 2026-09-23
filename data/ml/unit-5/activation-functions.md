---
subject: ml
unit: 5
topic: activation-functions
syllabus_ref: CSM3201 Unit-V
status: draft
---
# Types of Activation Functions

## Overview

An activation function transforms a neuron's pre-activation \(z\) into its output \(a=\phi(z)\). It introduces nonlinearity, controls the range of outputs, and affects gradient flow during training. The choice is part of the model design: it changes optimisation, representation, sparsity, and numerical stability.

Common functions include the step/threshold, sigmoid, hyperbolic tangent, ReLU and its variants, and linear output functions. A network may use different functions in hidden and output layers.

## Explanation

### Step or threshold activation

\[
\phi(z)=\begin{cases}
0,&z<0,\\
1,&z\geq0.
\end{cases}
\]

It models an on/off decision and introduces nonlinearity. Its derivative is zero almost everywhere, so ordinary gradient descent cannot update it smoothly. It is useful for explaining biological firing and binary decisions but is difficult to optimise in a multilayer network.

### Sigmoid

\[
\sigma(z)=\frac{1}{1+e^{-z}}.
\]

It maps any real number to \((0,1)\), so it is convenient for binary probability output. Its derivative is

\[
\sigma'(z)=\sigma(z)(1-\sigma(z)).
\]

The derivative is small for large positive or negative \(z\), causing **vanishing gradients** in deep networks. Sigmoid outputs near zero or one at saturation, which can also slow learning. It is still common in binary output layers, but ReLU-family functions are often preferred in hidden layers.

### Hyperbolic tangent

\[
\tanh(z)=\frac{e^z-e^{-z}}{e^z+e^{-z}}.
\]

It maps to \((-1,1)\), is zero-centred, and is related to sigmoid by \(\tanh(z)=2\sigma(2z)-1\). Its derivative is

\[
\tanh'(z)=1-\tanh^2(z).
\]

It can be useful as a hidden activation for centred data, but it also saturates and can produce vanishing gradients.

### ReLU

\[
\operatorname{ReLU}(z)=\max(0,z),
\qquad
\operatorname{ReLU}'(z)=
\begin{cases}
1,&z>0,\\
0,&z<0.
\end{cases}
\]

ReLU is computationally simple, preserves positive values, and often trains faster than sigmoid in deep networks. Its positive derivative can reduce vanishing gradients. However, units with negative inputs for many examples may never activate and receive no gradient, known as the dying-ReLU problem. At exactly zero, implementations may choose a subgradient.

### Leaky and parametric ReLU

Leaky ReLU uses

\[
\phi(z)=z\quad(z\ge0),\qquad
\phi(z)=\alpha z\quad(z<0),
\]

with a small positive \(\alpha\). A negative input can therefore produce a small gradient. Parametric ReLU learns \(\alpha\) per unit. The leakage can improve optimisation, but the learned value and numerical implementation need monitoring.

### Other hidden activations

- **ELU:** \(x\) for \(x>0\), \(\alpha(e^x-1)\) for \(x\leq0\), allowing a small negative mean.
- **GELU:** a smooth, approximately Gaussian-weighted activation used in some transformers.
- **Swish/SiLU:** \(z\sigma(z)\), smooth and often effective in larger models.
- **Softmax:** normalises a vector of logits into probabilities:
  \[
  p_k=\frac{e^{z_k}}{\sum_j e^{z_j}}.
  \]
  It is normally an output function for multiclass classification, not a general hidden activation.

### Linear activation

\[
\phi(z)=z.
\]

It does not add nonlinearity but can be used for regression output. Stacking only linear layers is equivalent to a linear transformation, so hidden layers need nonlinear functions for added expressivity.

### Choosing an activation

- Use sigmoid for a binary probability output when appropriate.
- Use softmax for mutually exclusive multiclass classification.
- Use linear output for unrestricted regression.
- Use ReLU or a variant in many hidden layers, monitoring inactive units and gradient norms.
- Match the activation to the target range and loss; do not choose by popularity alone.

### Numerical stability

Computing \(\sigma(z)\) naively can overflow for large negative \(z\). Stable implementations use algebraically equivalent forms. Softmax subtracts the maximum logit before exponentiation:

\[
p_k=\frac{e^{z_k-\max z}}{\sum_j e^{z_j-\max z}}.
\]

Cross-entropy can be combined with logits for a stable loss. Initialisation and normalisation affect whether activations saturate.

### Practical selection and monitoring

A common hidden-layer choice is ReLU or a smooth variant, followed by a task-specific output. The choice is a starting point, not a rule. Compare at least one alternative and inspect training curves, activation distributions, and validation performance. If many ReLU units are inactive, investigate initialisation, bias, input scale, and learning rate; if sigmoid/tanh units saturate, consider initialisation, normalisation, or a different hidden activation.

For binary classification, a single logit plus binary cross-entropy is usually more numerically stable than explicitly computing a sigmoid and then taking logs. For multiclass classification, use logits with a combined softmax/cross-entropy implementation. For regression, use a linear output unless the target has a known bounded range and a corresponding transformation. Activation functions cannot repair a wrong target definition.

The output activation also affects interpretation. A softmax probability can be compared with observed frequencies, but a large maximum value is not automatically a calibrated confidence. Evaluate calibration and abstention, and provide a human review path for high-impact decisions.

## Worked examples

### Example 1: sigmoid

At \(z=0\), \(\sigma(0)=0.5\). At \(z=2\), \(\sigma(2)\approx0.881\); at \(z=-2\), it is approximately 0.119. The output is probability-like, but the network's calibration still needs validation.

### Example 2: ReLU gradient

For \(z=3\), ReLU output is 3 and derivative is 1. For \(z=-3\), output and derivative are 0. If every example gives a unit negative input, its weights receive no gradient through that unit.

### Example 3: softmax

For logits \([1,2,3]\), subtracting the maximum gives \([0,-1,-2]\); exponentiation and normalisation yield probabilities approximately \([0.09,0.245,0.665]\). The largest logit is selected for a hard prediction, while the full vector supports log loss.

### Example 4: choosing output

A house-price model should normally use a linear output; forcing a sigmoid would restrict the price to a narrow range. A binary spam model can use one sigmoid logit. A three-class model uses three logits and softmax/cross-entropy.

## Key terms & formulas

- **Activation function:** \(\phi(z)\) transforming a pre-activation.
- **Threshold/step:** binary output.
- **Sigmoid:** \(\sigma(z)=1/(1+e^{-z})\).
- **Sigmoid derivative:** \(\sigma'(z)=\sigma(z)(1-\sigma(z))\).
- **Tanh:** \(\tanh(z)\in(-1,1)\).
- **ReLU:** \(\max(0,z)\).
- **Leaky ReLU:** negative slope \(\alpha z\) for \(z<0\).
- **Softmax:** \(e^{z_k}/\sum_j e^{z_j}\).
- **Linear output:** \(a=z\).
- **Vanishing gradient:** derivative becomes too small to train earlier layers.
- **Dying ReLU:** inactive units receiving zero gradient.
- **Logit:** pre-softmax score.

## Common mistakes

1. **Using a step function as a hidden activation.** Gradients are mostly zero.
2. **Confusing sigmoid output with a calibrated probability.** Calibration must be evaluated.
3. **Using softmax for binary independent labels.** Use separate sigmoids for multilabel tasks.
4. **Using a linear activation throughout.** The network collapses to a linear map.
5. **Ignoring saturation or dead units.** Monitor gradients and activation distributions.
6. **Computing softmax without numerical stabilisation.** Subtract the maximum logit.
7. **Choosing an activation without considering the output loss.** The task determines the appropriate output behaviour.

## Exam prep

### Likely 2-mark questions

- **Write sigmoid and ReLU.** \(\sigma(z)=1/(1+e^{-z})\), \(\operatorname{ReLU}(z)=\max(0,z)\).
- **What is the main purpose of an activation function?** To add nonlinearity and shape outputs.
- **What is the dying-ReLU problem?** A unit remains inactive, giving zero gradient and preventing learning.
- **When is softmax used?** For mutually exclusive multiclass classification over a vector of logits.

### Long-answer prompts

- **Compare sigmoid, tanh, ReLU, and leaky ReLU.** Discuss ranges, derivatives, saturation, gradient flow, and use cases.
- **Explain why activation functions are needed in deep networks.** Show that linear layers collapse and nonlinear layers add expressivity.
- **Choose activations for binary classification, multiclass classification, and regression.** Justify output functions and losses.
- **Discuss vanishing and dying gradients.** Give causes, symptoms, and remedies.
