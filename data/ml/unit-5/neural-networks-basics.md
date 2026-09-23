---
subject: ml
unit: 5
topic: neural-networks-basics
syllabus_ref: CSM3201 Unit-V
status: draft
---
# Neural Network Basics

## Overview

An artificial neural network (ANN) is a composition of connected processing units called neurons. Each unit computes a weighted sum of its inputs, adds a bias, and passes the result through an activation function. Organising units into input, hidden, and output layers allows a network to learn nonlinear relationships.

Neural networks are useful for classification, regression, ranking, representation learning, and prediction from images, text, audio, and time series. They can fit complex patterns, but they need appropriate data, an objective, careful optimisation, regularisation, and evaluation. A network is a mathematical model, not a literal copy of a brain.

## Explanation

### Why use a neural network?

A linear model combines inputs with fixed coefficients. A network composes simple functions:

\[
\hat y=f_L\bigl(f_{L-1}(\cdots f_1(x)\cdots)\bigr).
\]

This composition can approximate complex functions when enough hidden units and suitable activations are available. It also learns useful internal representations—for example, edges in an image or combinations of words—without requiring every feature to be designed by hand.

Neural networks are attractive when raw data are high-dimensional and patterns are difficult to specify, when labelled data are plentiful or can be generated through pretraining, and when prediction performance matters more than a short rule list. They are less attractive when data are tiny, explanations are legally required, latency is strict, or the data distribution is unstable.

### Network components

- **Input layer:** receives the feature vector or raw modality.
- **Hidden layer:** applies affine transformations and nonlinear activations to learn representations.
- **Output layer:** produces a class score/probability, numeric prediction, or other output.
- **Weights:** learned strengths of connections.
- **Biases:** learned offsets that shift activation thresholds.
- **Activation function:** introduces nonlinearity and controls the output range.
- **Loss function:** measures mismatch between output and target.
- **Learning algorithm:** updates weights, usually by gradient descent and backpropagation.

### Forward propagation

For one neuron with input \(x\), weight \(w\), and bias \(b\),

\[
z=wx+b,\qquad a=\phi(z).
\]

For a layer with matrix \(W\), bias \(b\), and previous activation \(A\),

\[
Z=WA+b,\qquad A'=\phi(Z).
\]

A network's forward pass starts with the input and applies these equations layer by layer. The output is a prediction or score. The computational graph records intermediate operations so derivatives can be calculated later.

### Losses and tasks

For binary classification with logits \(z\) and labels \(y\in\{0,1\}\),

\[
\mathcal L=-\frac1n\sum_i[y_i\log\sigma(z_i)+(1-y_i)\log(1-\sigma(z_i))].
\]

For \(K\)-class classification, a network outputs logits \(z_k\) and uses softmax with categorical cross-entropy. For regression, mean squared error,

\[
\mathcal L=\frac1n\sum_i(\hat y_i-y_i)^2,
\]

or mean absolute error may be used. The loss must match the task and cost; a high-quality representation is not enough if the output objective is wrong.

### Training loop

1. Obtain a mini-batch of input–target examples.
2. Perform a forward pass.
3. Compute the loss.
4. Backpropagate the gradient of loss with respect to every weight and bias.
5. Update parameters with gradient descent or another optimiser.
6. Repeat over the data for multiple epochs.
7. Monitor validation performance and stop at the best checkpoint.

An epoch is one complete pass through the training data. Mini-batches trade computation, noise, and memory. Learning rate, batch size, optimiser, initialisation, and regularisation affect convergence.

### Generalisation and overfitting

A high-capacity network can memorise training examples. Use a representative split, regularisation such as \(L_2\) penalty, dropout, data augmentation, early stopping, and appropriate model size. Neural-network training is non-convex, so different initialisations can lead to different solutions. Reproducibility requires recording seeds, versions, and data.

### Interpretability and deployment

A network's individual weights usually do not have a simple human meaning. Explanations may use gradients, saliency, integrated gradients, occlusion, concept tests, attention, or surrogate models. High-stakes applications need uncertainty, subgroup evaluation, human review, and a fallback. Monitor latency, input drift, output drift, calibration, and failures after deployment.

### Biological analogy

Biological neurons communicate through electrochemical signals, but an ANN is an abstract function approximator. It does not have consciousness, intention, or a human-like representation. The analogy explains names and inspiration, not an equality of mechanism.

### Capacity, generalisation, and responsible design

A network's capacity is not just its number of parameters. Effective capacity also depends on activation functions, initialisation, normalisation, regularisation, optimisation, and the amount and diversity of data. A small, well-regularised network can outperform a much larger one when the latter memorises noise. Conversely, a high-capacity model may be justified for images or text when the representation cannot be specified by hand.

Before training, check the data contract. Inputs should be scaled where appropriate, labels should match the output, and groups or time should be separated in evaluation. A network can learn a shortcut, so inspect feature sensitivity, errors, calibration, and subgroup results. For a high-stakes application, include an abstention threshold and a non-model fallback.

During deployment, monitor the input schema, missingness, activation or confidence distributions, latency, and delayed outcome metrics. A change in data can produce a high-confidence prediction even when the model is uncertain. Save the preprocessing state, architecture, weights, loss, and version together. A reproducible result records random seeds, library versions, batch order where relevant, and the exact evaluation protocol.

### Choosing a network for a task

A small MLP with a linear or tree-like data table is often enough for tabular data. A CNN is a strong default for local spatial patterns. An RNN/LSTM is useful for compact sequential models, while attention-based architectures are attractive when long-range context and parallel training matter. The choice should be justified by the data structure and deployment constraints, not by the number of layers. Always compare a simple baseline and monitor the model after release.

## Worked examples

### Example 1: one neuron

A neuron receives \(x_1=2,x_2=3\), weights \(w_1=0.5,w_2=-1\), and bias \(b=1\). Then

\[
z=0.5(2)-1(3)+1=-1,
\]

and with sigmoid activation \(a=\sigma(-1)\approx0.269\). A network of such units can compose more expressive functions.

### Example 2: two-layer prediction

A hidden layer produces \(A^{(1)}\) and an output layer produces \(\hat y\). If the output is 0.8 and the target is 1, binary cross-entropy is \(-\log 0.8\approx0.223\), not \(0.2\). A loss based on the model's probability behaves differently from squared error on the probability.

### Example 3: XOR

A single linear threshold cannot represent XOR. A hidden layer with nonlinear units can transform the four points so a linear output separates them. This illustrates why depth and nonlinearity matter, though modern networks are not limited to this small example.

## Key terms & formulas

- **ANN:** connected network of artificial neurons.
- **Neuron/unit:** affine transform plus activation.
- **Input/hidden/output layer:** roles in a network.
- **Weight \(w\):** learned connection strength.
- **Bias \(b\):** learned offset.
- **Pre-activation \(z\):** weighted sum before activation.
- **Activation \(a\):** nonlinear transformed value.
- **Forward propagation:** compute outputs from inputs.
- **Loss:** objective measuring prediction error.
- **Epoch:** one pass over training data.
- **Parameter:** learned weight or bias.
- **Overfitting:** fitting training-specific noise.
- **Gradient:** derivative of loss with respect to a parameter.
- **Epoch/mini-batch:** training iteration vocabulary.
- **Parameter sharing:** the same learned rule applied at multiple positions in an architecture.

## Common mistakes

1. **Calling an ANN a literal brain model.** It is an inspired mathematical construction.
2. **Forgetting the bias.** A neuron without it cannot shift its threshold freely.
3. **Using a linear activation throughout.** Without nonlinearities, stacked linear layers collapse to a linear map.
4. **Choosing a loss after training.** The objective should be defined from the task.
5. **Reporting training loss only.** Generalisation requires validation/test data.
6. **Ignoring scaling and optimisation.** Neural networks often need normalised inputs and careful learning rates.
7. **Assuming more layers always help.** Data, objective, and deployment constraints matter.

## Exam prep

### Likely 2-mark questions

- **What is an ANN?** A network of connected artificial neurons that learns a function from data.
- **Define weight, bias, and activation.** Explain their roles in a neuron.
- **What is an epoch?** One complete pass through the training data.
- **Why are nonlinear activations needed?** To allow layers to represent nonlinear relationships.

### Long-answer prompts

- **Explain the basic components and forward propagation of an ANN.** Include equations for a neuron and layer, losses, and output tasks.
- **Describe the training loop.** Discuss batching, loss, gradients, parameter updates, epochs, and validation.
- **Compare ANNs with linear models.** Discuss representation, data needs, interpretability, overfitting, and computation.
- **Why can a neural network overfit, and how can it be reduced?** Use regularisation, dropout, augmentation, early stopping, and data evidence.
