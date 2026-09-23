---
subject: ml
unit: 5
topic: gradient-descent
syllabus_ref: CSM3201 Unit-V
status: draft
---
# Gradient Descent

## Overview

Gradient descent is an optimisation method for reducing a function. At the current parameter value, it computes the gradient—the direction in which the function increases fastest—and moves in the opposite direction:

\[
\theta_{t+1}=\theta_t-\eta\nabla_\theta J(\theta_t).
\]

In neural-network training, \(J\) is the average loss over a batch and \(\theta\) includes all weights and biases. The learning rate \(\eta\) controls the step size. The method is simple, scalable, and central to training, but convergence depends on scaling, conditioning, noise, and the loss surface.

## Explanation

### The gradient

For a scalar function \(J(\theta_1,\ldots,\theta_p)\),

\[
\nabla J=\left(\frac{\partial J}{\partial\theta_1},\ldots,
\frac{\partial J}{\partial\theta_p}\right).
\]

A small positive displacement \(\delta\) changes the function approximately by \(\nabla J^\top\delta\). The negative gradient therefore gives a locally downhill direction. At a point with no gradient, plain gradient descent stops even if it is not a global minimum.

### Learning rate and convergence

If \(\eta\) is too large, updates can overshoot a narrow valley, oscillate, or diverge. If it is too small, learning is slow and may stop in a poor region. A learning-rate schedule can reduce the rate over time. Gradient normalisation methods such as Adam adapt the effective step per parameter, but they do not remove the need for a sensible learning-rate range.

### Batch, stochastic, and mini-batch descent

**Batch gradient descent** uses

\[
\theta\leftarrow\theta-\eta\frac1n\sum_{i=1}^{n}\nabla_\theta L_i.
\]

It is smooth but computes the whole data set for every step. **Stochastic descent** uses one example:

\[
\theta\leftarrow\theta-\eta\nabla_\theta L_i.
\]

The gradient is noisy but can escape small local minima and is cheap per update. **Mini-batch descent** averages \(B\) examples:

\[
\theta\leftarrow\theta-\eta\frac1B\sum_{i\in\mathcal B}\nabla_\theta L_i.
\]

It is the usual large-scale neural-network compromise. Shuffling examples and choosing a suitable batch size affect exploration, memory, and hardware utilisation.

### Momentum and adaptive methods

Momentum accumulates velocity:

\[
v_t=\mu v_{t-1}+g_t,\qquad
\theta_{t+1}=\theta_t-\eta v_t.
\]

It smooths oscillations and accelerates consistent directions. Nesterov momentum evaluates a lookahead gradient. Adam combines an exponentially smoothed first moment and second moment:

\[
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\quad
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,
\]

then uses approximately

\[
\theta_{t+1}=\theta_t-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.
\]

RMSProp, Adagrad, and other methods make different assumptions. Optimiser choice is part of tuning, not a replacement for learning-rate and batch-size management.

### Loss surfaces and local minima

Neural-network losses are often non-convex. They may contain saddles, flat regions, sharp valleys, and local minima. Stochastic noise from mini-batches can help escape some regions. Modern networks often have many usable stationary points, so a global mathematical minimum is not necessary for good generalisation. Initialisation, normalisation, architecture, and regularisation affect optimisation.

### Regularisation and weight decay

An explicit \(L_2\) penalty adds \(\frac{\lambda}{2}\|\theta\|^2\) to the loss. Many optimisers implement **weight decay** by multiplying weights by a factor near each update. For plain SGD, \(L_2\) regularisation and weight decay are closely related; for adaptive methods they are not always identical. Decoupled weight decay in AdamW is a common implementation. Do not confuse weight decay with a learning-rate schedule.

### A practical training procedure

1. Standardise or otherwise prepare inputs.
2. Initialise parameters with a suitable scheme.
3. Choose a loss matching the task.
4. Select a batch size and optimiser.
5. Tune the learning rate on validation data, using a small grid/range or schedule.
6. Run for many epochs, logging train/validation loss and gradient norms.
7. Use early stopping and save the best checkpoint.
8. Check calibration, subgroups, and test data only after selection.
9. Diagnose divergence, dead activations, and distribution shift.

### Convergence criteria

Stop when the objective or metric has improved by less than a tolerance for several evaluations, when a maximum time/iteration budget is reached, or when validation performance worsens. A small training loss does not guarantee a useful model. Use a test set once and report uncertainty.

### Choosing and scheduling the learning rate

A learning-rate range test can provide a useful starting point. Run short trials with exponentially increasing rates, record training loss and gradient norm, and select a rate that decreases loss rapidly without repeated divergence. This is a diagnostic, not a guarantee: batch size, architecture, optimiser, and data scaling change the safe range.

Schedules often combine a warm-up with a decay. Linear warm-up can protect large batches during the first steps; cosine or step decay can reduce the rate when progress plateaus. Reduce the rate only after observing validation behaviour, and retain the best checkpoint. A schedule that always lowers the rate can still fail if the initial rate is already too high.

For a non-convex neural loss, monitor more than the scalar loss. Plot gradient norms by layer, activation distributions, and the fraction of inactive ReLU units. An exploding layer may require a smaller rate, clipping, or better initialisation. A vanishing early layer may require a different activation, initialisation, normalisation, or residual path. Gradient descent does not repair an incorrect data split or label.

### Generalisation consequences of optimisation

An optimiser influences which solution is reached, but validation performance also depends on implicit regularisation such as early stopping and small-batch noise. A faster optimiser may reach a sharper solution that performs worse on shifted data; a slower run may generalise better. Compare final and best-validation checkpoints, run multiple seeds where feasible, and report the variation. Do not select a method solely by the fastest training time when reliability and fairness are more important.

## Worked examples

### Example 1: quadratic update

For \(J(w)=\frac12(w-3)^2\), \(\nabla J=w-3\). With \(w_0=0,\eta=0.1\),

\[
w_1=0-0.1(-3)=0.3,
\]

\[
w_2=0.3-0.1(-2.7)=0.57.
\]

The sequence approaches 3. This is convex, unlike many neural loss surfaces.

### Example 2: momentum

If gradients are consistently 5 and momentum \(\mu=0.9\), velocity approaches \(5/(1-0.9)=50\) under the recurrence \(v_t=0.9v_{t-1}+5\), so effective steps can become large. A learning rate that is safe for plain SGD may not be safe with momentum.

### Example 3: too-high learning rate

A one-dimensional loss has a narrow minimum. A step of size 10 repeatedly jumps across it, with loss oscillating or increasing. Reduce the learning rate, use a schedule, or apply normalisation and a suitable optimiser.

### Example 4: mini-batch estimate

For gradients 2, 4, and 6 in a batch of three, the average is 4. The update uses 4, not the sum, if the loss is averaged. This matters when changing batch size; otherwise effective learning rates change unintentionally.

## Key terms & formulas

- **Gradient:** \(\nabla J\), vector of partial derivatives.
- **Gradient descent:** \(\theta\leftarrow\theta-\eta\nabla J\).
- **Learning rate:** \(\eta\), step size.
- **Convex function:** loss surface with one global minimum basin.
- **Local minimum/stationary point:** point with small or zero gradient.
- **Saddle:** stationary point that is a minimum in some directions and maximum in others.
- **Batch gradient descent:** update from all examples.
- **SGD:** update from one example.
- **Mini-batch:** update from a subset.
- **Momentum:** velocity accumulation.
- **Adam:** adaptive first/second-moment optimiser.
- **Weight decay:** parameter shrinkage during optimisation.
- **Learning-rate schedule:** time-dependent learning-rate policy.
- **Convergence:** parameters reach a stable region under the optimiser.

## Common mistakes

1. **Using a learning rate without validation.** It can cause divergence or stagnation.
2. **Treating a zero gradient as a globally optimal solution.** It may be a saddle or poor plateau.
3. **Confusing batch average and sum.** Scaling changes the effective step.
4. **Using momentum with an unchanged learning rate without testing.** Effective steps increase.
5. **Assuming adaptive optimisation removes tuning.** Learning rate, schedule, and weight decay still matter.
6. **Stopping at the last epoch rather than the best validation checkpoint.** Overfitting may have begun.
7. **Failing to monitor gradient norms and activation distributions.** Vanishing/exploding signals can be hidden by a loss curve.

## Exam prep

### Likely 2-mark questions

- **State the gradient descent update.** \(\theta_{t+1}=\theta_t-\eta\nabla J(\theta_t)\).
- **What is the learning rate?** The factor controlling parameter-update magnitude.
- **Compare batch, stochastic, and mini-batch descent.** State the number of examples used per update and the main trade-off.
- **What is momentum?** Accumulation of past gradients to smooth and accelerate updates.

### Long-answer prompts

- **Explain gradient descent in neural-network training.** Derive the update, define learning rate, and discuss batch variants.
- **Compare SGD, momentum, and Adam.** Discuss velocity, adaptive estimates, convergence, and tuning.
- **Why are neural loss surfaces difficult?** Discuss non-convexity, saddles, flat regions, and local minima.
- **How would you troubleshoot an ANN that will not converge?** Inspect scaling, initialisation, learning rate, gradients, activations, loss, data, and implementation.
