---
subject: ml
unit: 5
topic: early-ann-implementation
syllabus_ref: CSM3201 Unit-V
status: draft
---
# Early Implementation of an ANN

## Overview

Early artificial neural networks were mathematical models and small algorithms before today's deep-learning frameworks. They showed that networks of simple units could learn nonlinear functions from examples. Important early ideas include the perceptron, the ADALINE model, associative memory, self-organising maps, and early backpropagation-based multilayer networks.

The historical lesson is practical: representation, training signal, and optimisation are as important as the neuron equation. A simple early implementation can be written from scratch to understand forward propagation, error correction, and learning.

## Explanation

### The perceptron

The perceptron, introduced by Rosenblatt, computes

\[
y=\mathbf1\left(\sum_jw_jx_j+b\geq0\right).
\]

It is a linear threshold classifier. For a misclassified example, a simple update is

\[
w\leftarrow w+\eta(y-\hat y)x,\qquad
b\leftarrow b+\eta(y-\hat y).
\]

The perceptron convergence result applies to data linearly separable by the chosen hypothesis class. It fails for XOR, which is not linearly separable. Its limitation motivated multilayer networks and more expressive hidden representations.

### ADALINE and least mean squares

Adaptive linear neuron (ADALINE) uses a continuous output

\[
y=w^\top x+b
\]

and a mean-squared error. It can be trained by the Widrow–Hoff learning rule,

\[
w\leftarrow w+\eta(y^{(d)}-y)x,
\]

where \(y^{(d)}\) is the desired target. Unlike a hard perceptron, the update uses the continuous error and can lead toward a least-squares solution for a linear model. It is a useful bridge from perceptrons to supervised learning.

### Associative memory

A linear associative memory stores associations between input and output patterns by forming a weight matrix from examples, for example

\[
W=\sum_k y_kx_k^\top.
\]

Given a noisy or partial input \(x'\), the output \(Wx'\) may retrieve a related stored pattern. Hopfield networks use a symmetric recurrent weight matrix and an energy function to store attractor states. They differ from feed-forward regression and can suffer from capacity limits and spurious states.

### Self-organising maps

Kohonen's self-organising map is an unsupervised or competitive network. Neurons in a lattice receive input, the closest/best-matching unit becomes active, and nearby units update toward the input:

\[
w_j(t+1)=w_j(t)+\alpha(t)[x-w_j(t)]h_{cj}.
\]

The neighbourhood function makes nearby map units similar. SOMs produce a low-dimensional, topology-preserving representation, but map orientation and scale require interpretation.

### Early multilayer learning

Early multilayer networks used hidden units, differentiable activations, and supervised error signals. With paired input/target data, one can minimise

\[
E=\frac12\sum_i\|y_i-\hat y_i\|^2
\]

by computing derivatives of the error with respect to hidden and output weights. The chain rule provides the mathematical basis of backpropagation. Early implementations were numerically difficult, computationally limited, and often used small data sets, but the core ideas remain.

### A small implementation plan

A from-scratch feed-forward example can use:

1. two input features and three hidden units;
2. sigmoid hidden activation and a linear output;
3. mean-squared-error loss;
4. forward pass \(a^{(1)}=\sigma(W^{(1)}x+b^{(1)})\), \(\hat y=W^{(2)}a^{(1)}+b^{(2)}\);
5. manual gradient computation or a small automatic-differentiation engine;
6. gradient-descent updates;
7. comparison with a numerical gradient check;
8. loss curves and a held-out test set.

The implementation should use a seed, fixed learning rate, and simple data so every calculation can be checked.

### Historical limitations

Early models could not scale to modern data or tasks, and training was sensitive to initialisation, learning rate, and data representation. They also often used small synthetic examples, so generalisation and deployment were less studied. Modern ANNs add GPUs, large datasets, optimisation algorithms, normalisation, residual connections, attention, and better architectures, but the fundamental unit and gradient ideas remain.

## Worked examples

### Example 1: perceptron update

For \(x=(1,2)\), \(w=(0.1,0.2)\), \(b=0\), the score is 0.5 and the prediction is 1. If the true label is 0 and \(\eta=0.1\),

\[
w_{\text{new}}=(0.1,0.2)+0.1(0-1)(1,2)
=(0.1,0.2)-(0.1,0.2)=(0,0),
\]

and \(b_{\text{new}}=0+0.1(0-1)=-0.1\). Repeating updates can separate linearly separable data; it cannot solve XOR.

### Example 2: ADALINE

For a one-dimensional example \(x=2\), desired \(y=5\), current output \(\hat y=2\), and \(\eta=0.01\),

\[
w_{\text{new}}=w+0.01(5-2)2=w+0.06.
\]

The update increases the slope in the direction of the positive error.

### Example 3: SOM

A 1-D map has units at positions 1, 2, and 3. If input \(x=2.1\) is closest to unit 2, a neighbourhood update moves units 1–3 toward 2.1, with unit 2 moving most. Nearby map units therefore learn similar input patterns.

### Example 4: numerical gradient check

For \(J(w)=(w-3)^2\), the analytical derivative at \(w=1\) is \(2(w-3)=-4\). A finite difference \((J(1+\epsilon)-J(1-\epsilon))/(2\epsilon)\) is close to \(-4\) for a small \(\epsilon\). This check catches errors in a hand-written backpropagation implementation.

## Key terms & formulas

- **Perceptron:** linear threshold classifier.
- **Perceptron learning rule:** \(w\leftarrow w+\eta(y-\hat y)x\).
- **Linear separability:** ability of one hyperplane to separate classes.
- **ADALINE:** adaptive linear neuron with continuous output.
- **Widrow–Hoff rule:** LMS linear error update.
- **Associative memory:** network retrieving a stored pattern from a related input.
- **Hopfield network:** recurrent attractor network with an energy function.
- **SOM:** self-organising competitive map.
- **Neighbourhood function:** controls which map units update and by how much.
- **Multilayer network:** stacked layers with hidden units.
- **Numerical gradient check:** finite-difference test of a derivative.
- **Convergence theorem:** perceptron convergence under linear separability conditions.

## Common mistakes

1. **Applying perceptron convergence to XOR.** XOR is not linearly separable.
2. **Confusing a hard perceptron with ADALINE.** One uses threshold output, the other continuous error.
3. **Ignoring the learning rate.** Updates can overshoot or be too slow.
4. **Using a hand-coded gradient without checking it.** Numerical gradient checks catch errors.
5. **Comparing training loss only.** Early models still need held-out evaluation.
6. **Treating historical significance as proof of current superiority.** Compare assumptions and requirements.
7. **Ignoring modern practical issues.** Scale, optimisation, memory, and deployment still matter.

## Exam prep

### Likely 2-mark questions

- **What is a perceptron?** A single neuron producing a thresholded linear classification.
- **State the perceptron learning rule.** \(w\leftarrow w+\eta(y-\hat y)x\).
- **Why did the perceptron fail on XOR?** XOR is not linearly separable by one hyperplane.
- **What is ADALINE?** An adaptive linear neuron trained with a continuous error and LMS rule.

### Long-answer prompts

- **Explain the perceptron and its convergence limitation.** Include equations, updates, separability, and XOR.
- **Compare ADALINE and the perceptron.** Discuss output, error, learning rule, and applications.
- **Describe an early ANN implementation.** Cover neuron, forward pass, loss, gradient update, seed, and validation.
- **What is the historical significance of early ANNs?** Discuss the perceptron, associative memory, SOM, and modern foundation.
