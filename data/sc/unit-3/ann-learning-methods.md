---
subject: sc
unit: 3
topic: ann-learning-methods
syllabus_ref: CSM3202 Unit-III
status: draft
---
# Learning Methods in Neural Networks

## Overview

Neural-network learning means adjusting weights, biases, and sometimes the network structure so that predictions improve on data. The learning paradigm depends on the feedback available: supervised learning uses target values, unsupervised learning discovers structure without targets, and reinforcement learning uses delayed reward.

A feed-forward network is most commonly trained by supervised learning. Its principal methods include perceptron learning, delta learning, gradient descent, least-squares training, and backpropagation.

## Explanation

### 1. Parameters and learning rule

Let

\[
\hat{\mathbf y}=f(\mathbf x,\mathbf w,\mathbf b)
\]

be the network output. A learning rule changes parameters in response to an error. The simplest form is

\[
\mathbf w\leftarrow\mathbf w+\eta e\,\mathbf x,
\]

where

\[
e=t-\hat y
\]

and \(\eta\) is the learning rate.

A larger learning rate moves quickly but may oscillate. A smaller rate gives stable updates but may take longer. The learning rule must be paired with a suitable architecture and data preprocessing.

### 2. Supervised learning

Supervised learning uses input-target pairs

\[
\mathcal D=\{(\mathbf x_n,t_n)\}_{n=1}^{N}.
\]

The model predicts \(\hat{\mathbf y}_n\), compares it with \(t_n\), and updates parameters. The objective is often

\[
\min_{\theta}J(\theta)
=\frac1N\sum_{n=1}^{N}
\ell(f(\mathbf x_n;\theta),t_n).
\]

Training uses labeled examples, while validation estimates generalization and early stopping; the test set is used only after model selection.

### 3. Unsupervised learning

Unsupervised learning receives no target labels. It discovers structure such as clusters, low-dimensional representations, density estimates, or association rules.

Examples include:

- self-organizing maps;
- k-means clustering;
- autoencoders;
- association-rule learning;
- competitive learning.

Unsupervised learning is useful when labels are expensive or unavailable, but discovered structure still requires evaluation and interpretation.

### 4. Reinforcement learning

In reinforcement learning, an agent interacts with an environment. It receives rewards and learns a policy that maximizes expected cumulative reward. The core components are state, action, reward, transition, and policy.

The agent may learn through value iteration, Q-learning, policy gradients, or actor–critic methods. Unlike supervised learning, it may not receive an immediate target for every action; it learns from delayed consequences.

### 5. Perceptron learning

A single-layer perceptron computes

\[
y=\phi\left(\sum_{i=1}^{n}w_ix_i+b\right).
\]

For a binary step threshold, an error-correcting update is

\[
w_i\leftarrow w_i+\eta(t-y)x_i,
\]

\[
b\leftarrow b+\eta(t-y).
\]

The rule moves the decision boundary in the direction needed to classify the current example.

The original perceptron convergence theorem applies to linearly separable binary data with a suitable step activation and a fixed learning rate. It does not guarantee learning for XOR, which is not linearly separable.

### 6. Delta learning and the Widrow–Hoff rule

A linear neuron may use

\[
w\leftarrow w+\eta e\mathbf x,
\qquad e=t-\phi(v).
\]

With linear activation and mean squared error, this is the LMS or Widrow–Hoff rule. For stochastic updates:

\[
e_n=t_n-\mathbf x_n^{\mathsf T}\mathbf w.
\]

The update is

\[
\mathbf w\leftarrow\mathbf w+\eta e_n\mathbf x_n.
\]

For a linear model, minimizing squared error has a normal-equation solution; LMS is useful when iterative online updates are desired.

### 7. Gradient descent learning

For a differentiable loss, update each parameter in the negative gradient direction:

\[
\theta\leftarrow\theta-\eta\frac{\partial J}{\partial\theta}.
\]

A batch gradient uses all \(N\) examples:

\[
\theta\leftarrow\theta-\eta\nabla_\theta J(\theta).
\]

Stochastic gradient descent (SGD) uses one example or a small mini-batch. Mini-batch gradient descent is a common compromise between computational efficiency and stable updates.

The learning rate may be fixed, reduced by a schedule, or adapted by an optimizer such as Adam. Momentum and adaptive methods can help but introduce new hyperparameters.

### 8. Backpropagation

Backpropagation is the process of applying the chain rule through a network to calculate the gradient of the loss with respect to every weight and bias. It does not itself specify the entire training algorithm; gradient descent or another optimizer uses the gradients to update parameters.

For

\[
\hat y=f(\mathbf x;\theta),
\]

backpropagation computes

\[
\frac{\partial L}{\partial\theta}
\]

efficiently by reusing intermediate derivatives. It is the standard learning method for multilayer FFNNs with differentiable activations.

### 9. Generalized learning rules

A delta rule for a differentiable activation can be written

\[
\Delta w=\eta e\,\phi'(v)x,
\]

where

\[
e=t-\hat y.
\]

The factor \(\phi'(v)\) scales the update by the local slope. If the activation is flat, learning is weak even when the prediction error is large. This is one reason sigmoid saturation can slow training.

### 10. Learning rate and stability

For a linear neuron, a large step may overshoot or oscillate. Practical safeguards include:

- scale input features;
- choose a small initial learning rate;
- monitor training and validation loss;
- use a learning-rate schedule;
- use adaptive optimizers cautiously;
- clip gradients for recurrent or very deep models.

There is no universally correct learning rate. The best value depends on initialization, batch size, architecture, and loss.

### 11. Training, validation, and test sets

The **training set** fits parameters. The **validation set** selects hyperparameters and provides early-stopting signals. The **test set** estimates final performance after all choices are fixed.

If test data influence model selection, the reported test error is optimistic. Cross-validation can be used when data are limited:

- split into \(K\) folds;
- train on \(K-1\), validate on one;
- repeat and average.

The folds should preserve time order for time-dependent problems rather than randomly mixing future information into the past.

### 12. Epoch, batch, and iteration

An **epoch** is one complete pass through the training data. A **batch** is a subset used for one update. An **iteration** is one batch update. If there are \(N\) examples and batch size \(B\), there are approximately \(N/B\) iterations per epoch.

### 13. Overfitting and generalization

Overfitting occurs when the network memorizes training examples but performs poorly on unseen data. Signs include:

- training loss keeps decreasing;
- validation loss begins to increase;
- a very large network performs worse than a smaller model;
- small changes in data cause unstable predictions.

Use regularization, dropout, weight decay, data augmentation, early stopping, and a simpler architecture as appropriate. Generalization is not guaranteed by low training error.

### 14. Transfer learning and adaptation

Pretraining can learn general features from a large dataset. A smaller target task then trains a new output layer and possibly some upper layers. Transfer learning is especially useful when target labels are limited.

Fine-tuning too many layers can overfit a small target set. Freeze and unfreeze layers deliberately, and use a lower learning rate for pretrained parameters when appropriate.

### 15. Learning under noise and missing data

Networks can be trained with noisy examples, but labels may be corrupted. Use robust losses such as MAE, label smoothing, or robust estimation when noise is expected. Missing values require a consistent strategy: imputation, masking, native missing-value handling, or a model that accepts missing inputs. The training and deployment pipeline must use the same policy.

### 16. Choosing a learning method

| Situation | Suitable method |
|---|---|
| Linear threshold classification | Perceptron or delta rule |
| Linear regression | Least squares, LMS, gradient descent |
| Nonlinear multilayer mapping | Backpropagation with gradient descent |
| No labels and cluster structure | K-means, SOM, autoencoder |
| Delayed reward decisions | Reinforcement learning |
| Limited labels with a related source | Transfer learning |

No method is always best. The target, data size, structure, and required explanation determine the choice.

## Worked examples

### Example 1: Perceptron training for OR

Train an OR function:

\[
(1,0)\to1,\quad(0,1)\to1.
\]

Use threshold

\[
y=1\text{ if }w_1x_1+w_2x_2+b\ge0.5,
\]

with initial weights and bias zero and learning rate \(\eta=0.5\).

**First example \((1,0,1)\):**

Initial prediction \(y=0\), error \(e=1\).

\[
w_1\leftarrow0+0.5(1)(1)=0.5,
\]

\[
w_2\leftarrow0+0.5(1)(0)=0,
\]

\[
b\leftarrow0+0.5(1)=0.5.
\]

**Second example \((0,1,1)\):**

Current score is \(w_2+b=0.5\), so threshold output is 1. No update is needed.

Final model:

\[
y=1\text{ if }0.5x_1+0.5\ge0.5,
\]

which classifies both training examples correctly. A later input \((1,1)\) also outputs 1.

### Example 2: Widrow–Hoff update

For a linear neuron with

\[
\mathbf w=[0.2,-0.1],\quad b=0.3,
\]

input \(\mathbf x=[2,1]\), and target \(t=1\):

\[
\hat y=0.2(2)-0.1(1)+0.3=0.6.
\]

Error:

\[
e=1-0.6=0.4.
\]

With \(\eta=0.1\),

\[
\mathbf w\leftarrow[0.2,-0.1]+0.1(0.4)[2,1]
=[0.28,-0.06],
\]

\[
b\leftarrow0.3+0.1(0.4)=0.34.
\]

The new prediction is \(0.28(2)-0.06+0.34=0.84\), closer to 1.

### Example 3: Choose a validation model

Suppose two FFNN architectures produce:

- model A: training MSE 0.01, validation MSE 0.08;
- model B: training MSE 0.03, validation MSE 0.04.

The validation error suggests model B generalizes better despite higher training error. Reporting model A because it has the lower training loss would be a mistake.

### Example 4: Unsupervised clustering

A customer dataset has no labels. K-means partitions customers into \(k\) groups by minimizing within-cluster squared distance. The output is a group assignment, not automatically a correct class label. Domain experts must determine what each cluster represents.

## Key terms & formulas

- **Supervised learning:** Learning from input-target pairs.
- **Unsupervised learning:** Discovering structure without target labels.
- **Reinforcement learning:** Learning from rewards through interaction.
- **Perceptron rule:** Error-correcting binary threshold update.
- **Delta rule:** Error-based update using an activation derivative.
- **Gradient descent:** Update in the negative loss-gradient direction.
- **Backpropagation:** Efficient chain-rule computation of gradients.
- **Epoch:** One complete training pass.

Perceptron:

\[
w_i\leftarrow w_i+\eta(t-y)x_i.
\]

Gradient descent:

\[
\theta\leftarrow\theta-\eta\nabla_\theta J.
\]

Mean squared error:

\[
J=\frac1N\sum_n(\hat y_n-t_n)^2.
\]

LMS:

\[
\mathbf w\leftarrow\mathbf w+\eta(t-\mathbf x^{\mathsf T}\mathbf w)\mathbf x.
\]

## Common mistakes

1. **Confusing backpropagation with gradient descent.** Backpropagation computes gradients; an optimizer updates weights.
2. **Claiming a perceptron solves XOR.** XOR is not linearly separable by one layer.
3. **Using a learning rate that is too large.** Updates may oscillate or diverge.
4. **Reporting training error as generalization.** Use held-out validation/test data.
5. **Selecting hyperparameters on the test set.** This leaks information.
6. **Ignoring feature scaling.** Numerical ranges affect optimization.
7. **Confusing unlabeled clustering with classification.** Clustering has no target labels.
8. **Treating reward as an immediate supervised target in reinforcement learning.** Rewards may be delayed and action selection is involved.
9. **Forgetting bias terms in a learning rule.** Their gradients must be included.

## Exam prep

### Likely 2-mark questions

- **Define supervised, unsupervised, and reinforcement learning.**  
  **Hint:** Labels, discovered structure, and reward-based interaction.

- **State the perceptron learning rule.**  
  **Hint:** \(w_i\leftarrow w_i+\eta(t-y)x_i\).

- **What is backpropagation?**  
  **Hint:** Chain-rule calculation of loss gradients throughout a network.

- **Name two overfitting-control methods.**  
  **Hint:** Regularization, early stopping, dropout, data augmentation, or simpler architecture.

- **What is an epoch?**  
  **Hint:** One complete pass through the training data.

### Likely long-answer questions

- **Explain the main learning paradigms in neural networks with examples.**  
  **Hint:** Supervised labels, unsupervised structure, reinforcement reward, and method selection.

- **Derive and apply the perceptron learning rule.**  
  **Hint:** Prediction, error, threshold, update, and a linearly separable example.

- **Compare batch, stochastic, and mini-batch gradient descent.**  
  **Hint:** Data per update, speed, noise, hardware, and convergence.

- **Explain how to prevent overfitting in an FFNN.**  
  **Hint:** Data split, regularization, early stopping, dropout, architecture, and validation.

- **Discuss learning rate and data preprocessing in neural-network training.**  
  **Hint:** Stability, scaling, schedule, monitor curves, and hyperparameter validation.
