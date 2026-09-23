---
subject: ml
unit: 5
topic: artificial-neuron
syllabus_ref: CSM3201 Unit-V
status: draft
---
# Exploring the Artificial Neuron

## Overview

An artificial neuron is a mathematical unit that computes a weighted combination of its inputs, adds a bias, and applies an activation function. Many neurons arranged in layers form an artificial neural network. The artificial neuron is not intended to reproduce a biological cell; it is a convenient building block for representing nonlinear functions.

The unit is the connection between biological intuition and the equations used in training. Its parameters are adjusted to reduce a loss, usually through gradient descent and backpropagation.

## Explanation

### The artificial-neuron equation

For a neuron with inputs \(x_1,\ldots,x_d\),

\[
z=\sum_{j=1}^{d}w_jx_j+b,
\qquad
a=\phi(z).
\]

- \(x_j\): input from a previous neuron or a feature.
- \(w_j\): weight or strength of the connection.
- \(b\): bias, an adjustable threshold/offset.
- \(z\): pre-activation or net input.
- \(\phi\): activation function.
- \(a\): output passed to the next neuron.

A common convention writes the bias as a weight attached to a constant input \(x_0=1\). The neuron is therefore an affine transformation followed by a nonlinearity.

### Layer notation

If \(A^{(\ell-1)}\) is the activation vector entering layer \(\ell\), its pre-activation and output are

\[
Z^{(\ell)}=W^{(\ell)}A^{(\ell-1)}+b^{(\ell)},
\qquad
A^{(\ell)}=\phi(Z^{(\ell)}).
\]

For a batch, matrices allow all examples to be processed in parallel. The weight matrix shape reflects the number of inputs and outputs.

### Why a bias is needed

Without a bias, \(a=\phi(w^\top x)\) always passes through the origin before the activation. A bias shifts the decision boundary and lets a unit respond at non-zero input combinations. For example, a linear classifier \(w^\top x>0\) becomes \((w^\top x+b)>0\), which need not pass through the origin.

### Activation choice

A step function

\[
\phi(z)=
\begin{cases}
1,&z\geq0,\\
0,&z<0
\end{cases}
\]

models a threshold but has zero derivative almost everywhere, making gradient-based learning difficult. Sigmoid, tanh, ReLU, and related functions provide usable derivatives and different output ranges. The activation is where nonlinearity enters. If every layer is linear,

\[
W_2(W_1x+b_1)+b_2
\]

is still a linear function of \(x\), no matter how deep the network is.

### Example tasks

A single neuron can implement a linear classifier when it outputs a sigmoid probability. Several neurons with nonlinear activations can approximate nonlinear decision boundaries. A linear output neuron can perform regression. Multiple output units with softmax can perform multiclass classification. A recurrent neuron can model sequential dependencies when hidden state is carried through time.

### Parameters and learning

The weights and biases are parameters. For a loss \(J\), the gradient of \(J\) with respect to pre-activation \(z\) is used by the optimiser. In a network, backpropagation applies the chain rule from the loss back through layers. The update is typically

\[
\theta\leftarrow\theta-\eta\frac{\partial J}{\partial\theta}.
\]

The learning rate \(\eta\) controls how far a parameter moves. Too large a step can oscillate or diverge; too small a step can be slow.

### Interpretability and limitations

A single neuron's weight may be interpretable when features and the activation are simple. In a deep network, many interacting units produce a collective result, so individual weights are not usually meaningful explanations. A network can be overparameterised, sensitive to scaling, and dependent on optimisation and regularisation.

## Worked examples

### Example 1: sigmoid neuron

For \(x_1=1,x_2=0\), \(w_1=2,w_2=-0.5,b=0.2\),

\[
z=2(1)-0.5(0)+0.2=2.2,
\qquad
a=\sigma(2.2)\approx0.900.
\]

The neuron outputs a probability only in a classification setup where its score is interpreted as one.

### Example 2: ReLU neuron

For \(z=-3\), \(\operatorname{ReLU}(z)=0\); for \(z=4\), it returns 4. A ReLU network is piecewise linear and can represent many functions, but many units may be inactive for a given input, a phenomenon called dying ReLU.

### Example 3: layer composition

If \(W_1\) and \(W_2\) are matrices and both layers are linear, the composition has the form \(W_2W_1x+\text{constant}\). It is equivalent to one linear layer. Nonlinear activations are necessary for added expressivity.

### Example 4: bias boundary

A linear boundary \(2x_1-x_2+0.5=0\) is \(x_2=2x_1+0.5\), which does not pass through the origin. The intercept \(0.5\) comes from the bias. Removing it changes the geometry of the decision boundary.

## Key terms & formulas

- **Artificial neuron:** weighted-sum unit with bias and activation.
- **Net input/pre-activation:** \(z=w^\top x+b\).
- **Activation:** \(\phi(z)\).
- **Weight:** learned connection coefficient.
- **Bias:** learned additive offset.
- **Layer:** collection of units with shared input/output structure.
- **Matrix form:** \(Z=WA+b\).
- **Sigmoid:** \(1/(1+e^{-z})\).
- **ReLU:** \(\max(0,z)\).
- **Parameter update:** \(\theta\leftarrow\theta-\eta\nabla_\theta J\).
- **Threshold/step function:** binary activation.
- **Dying ReLU:** units with zero gradient and inactive inputs.
- **Affine transformation:** weighted sum plus bias.

## Common mistakes

1. **Forgetting the bias.** A neuron cannot freely shift its boundary.
2. **Confusing the pre-activation with the output.** The activation is applied after the sum.
3. **Using a step activation with ordinary gradient descent.** Its derivative is mostly zero.
4. **Thinking depth adds expressivity with only linear layers.** Linear compositions collapse.
5. **Interpreting a weight as a feature importance without context.** Weights interact through nonlinearities.
6. **Using a learning rate blindly.** Convergence depends on scale and optimiser.
7. **Forgetting the loss.** A neuron alone does not define learning or a valid task.

## Exam prep

### Likely 2-mark questions

- **Write the artificial-neuron equation.** \(z=\sum_jw_jx_j+b,\ a=\phi(z)\).
- **Define bias.** An adjustable offset added to the weighted input.
- **Why use a nonlinear activation?** To allow the network to represent nonlinear functions.
- **What is a dying ReLU?** A unit whose input remains negative, producing zero output and gradient.

### Long-answer prompts

- **Explain the working of an artificial neuron.** Describe inputs, weights, bias, activation, output, and learning.
- **Compare a step, sigmoid, tanh, and ReLU activation.** Discuss range, derivative, gradient learning, and use.
- **Why are bias terms necessary?** Use a non-origin linear boundary example.
- **Show that a stack of linear neurons is still linear.** Compare it with a network containing nonlinear activations.
