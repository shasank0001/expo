---
subject: sc
unit: 3
topic: xor-with-rbfnn
syllabus_ref: CSM3202 Unit-III
status: draft
---
# XOR Problem in an RBFNN

## Overview

XOR is not linearly separable: no single straight line can assign the four points \((0,0),(0,1),(1,0),(1,1)\) to classes 0 and 1. An RBF network solves it by using nonlinear hidden responses. A linear combination of those hidden responses can create a decision function that is nonlinear in the original two inputs.

This example is useful for showing why hidden layers matter, how centers act as local prototypes, and how an RBF output layer is trained.

## Explanation

### 1. XOR data

The Boolean exclusive OR is 1 when exactly one input is 1:

| \(x_1\) | \(x_2\) | \(y\) |
|---:|---:|---:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

No line \(ax_1+bx_2+c=0\) separates the positive points \((0,1),(1,0)\) from the negative points \((0,0),(1,1)\). A single linear neuron or perceptron cannot solve this dataset.

### 2. Four hidden centers

Use four Gaussian hidden units, one at each data point:

\[
\mathbf c_{00}=(0,0),\quad
\mathbf c_{01}=(0,1),\quad
\mathbf c_{10}=(1,0),\quad
\mathbf c_{11}=(1,1).
\]

Use a common width \(\sigma=0.5\):

\[
h_i(\mathbf x)
=\exp\left[-\frac{\|\mathbf x-\mathbf c_i\|^2}{2\sigma^2}\right]
=\exp[-2\|\mathbf x-\mathbf c_i\|^2].
\]

The four responses form a nonlinear feature vector. An output neuron can assign a positive or negative weight to each local response.

### 3. Output weights

Let the output be

\[
z(\mathbf x)
=
h_{11}(\mathbf x)
-h_{00}(\mathbf x)
-h_{01}(\mathbf x)
-h_{10}(\mathbf x).
\]

Predict class 1 when \(z\ge0\), and class 0 when \(z<0\). Equivalently,

\[
\mathbf w=(-1,-1,-1,1),\qquad b=0
\]

in the order \(00,01,10,11\).

### 4. Evaluate at the four points

Define

\[
q=e^{-1/(2\sigma^2)}
=e^{-1/(2(0.5)^2)}
=e^{-2}\approx0.135335.
\]

This is the response at distance 1 from a center.

At \((0,0)\):

\[
(h_{00},h_{01},h_{10},h_{11})
=(1,q,q,q).
\]

Therefore,

\[
z=q-1-q-q=-1-q\approx-1.1353.
\]

Predict class 0.

At \((0,1)\):

\[
(h_{00},h_{01},h_{10},h_{11})
=(q,1,q,q).
\]

\[
z=q-q-1-q=-1-q\approx-1.1353.
\]

Predict class 0.

At \((1,0)\), the same distances and negative label apply:

\[
z=-1-q\approx-1.0183,
\]

so the prediction is class 0.

At \((1,1)\):

\[
(h_{00},h_{01},h_{10},h_{11})
=(q,q,q,1).
\]

\[
z=1-3q
=1-3(0.0183156)
=0.593995.
\]

Predict class 1.

The four results are correct.

### 5. Why the output is nonlinear in input space

The final class boundary is

\[
h_{11}(\mathbf x)
=
h_{00}(\mathbf x)+h_{01}(\mathbf x)+h_{10}(\mathbf x).
\]

The left and right sides are nonlinear Gaussian functions of \(x_1,x_2\). The boundary can therefore bend into separate regions around the two positive points.

The hidden layer creates the feature that a single sigmoid perceptron lacks.

### 6. Training from data

In a regression-style output, use targets \(+1\) for class 1 and \(-1\) for class 0. For the four exact centers and an idealized narrow-width response, the hidden matrix is approximately the identity, and the weights are the target labels.

For the finite width \(\sigma=0.5\), the matrix is

\[
\Phi=
\begin{bmatrix}
1&q&q&q\\
q&1&q&q\\
q&q&1&q\\
q&q&q&1
\end{bmatrix}.
\]

Solve

\[
\mathbf w=(\Phi^{\mathsf T}\Phi)^{-1}\Phi^{\mathsf T}\mathbf y
\]

with

\[
\mathbf y=(-1,-1,-1,1)^{\mathsf T}.
\]

Because every row has the same symmetric off-diagonal structure, the exact solution is

\[
\mathbf w=(-1,-1,-1,1)
\]

up to numerical rounding. Adding ridge regularization can produce a slightly different but still correct solution.

### 7. Boundary points and decision convention

A threshold such as \(z=0\) is conventional. If \(z=0\), the implementation must choose whether to use \(\ge\) or \(>\). The four training points do not land exactly at zero for the chosen width, so this convention does not affect their predictions.

For a noisy or larger data set, a margin or class-weighted loss may be better than sign of a raw score.

### 8. Why a single center can fail

A single Gaussian centered at the origin cannot distinguish \((0,1)\) and \((1,0)\) because they have the same distance from \((0,0)\). A single linear output therefore cannot assign both opposite labels. At least two independent hidden features or a more expressive center arrangement are needed.

A single center at \((1,1)\) has the same limitation in the other direction. More centers provide local information.

### 9. FFNN comparison

A sigmoid FFNN with one hidden layer can also solve XOR by learning hidden features that separate the positive points. The RBF version places prototypes at the data points and uses distance-based activations. FFNN hidden units are not inherently local prototypes; their weights are learned for the chosen activation.

The RBF network is not “better” simply because it uses a hidden layer. It is a particular inductive bias: nearby inputs receive similar hidden responses.

### 10. Practical XOR variants

Real XOR data may include noise:

\[
(0.05,0.0)\to0,\quad(0.95,1.0)\to1.
\]

Centers can be selected by k-means, and widths can be tuned. Too small a width may leave unseen points with weak responses; too large a width may blur class regions. Add regularization and validate on perturbed points.

## Worked examples

### Example 1: Verify the response at \((0,1)\)

The distance from \((0,1)\) to its center is zero, so

\[
h_{01}=1.
\]

The distance to \((0,0)\) and \((1,0)\) is one:

\[
h_{00}=h_{10}=e^{-1/(2(0.5)^2)}=e^{-2}\approx0.1353.
\]

The distance to \((1,1)\) is one as well:

\[
h_{11}=e^{-2}\approx0.1353.
\]

With weights \((-1,-1,-1,1)\),

\[
z=-0.1353-1-0.1353+0.1353=-1.1353.
\]

The exact value is \(-1-e^{-2}\), and the prediction is 0. The denominator \(2\sigma^2\) is important: with \(\sigma=0.5\), the response at distance 1 is \(e^{-2}\), not \(e^{-4}\).

### Example 2: Recompute with a conventional Gaussian

For \(\sigma=0.5\),

\[
h_i=e^{-\|x-c_i\|^2/(2\sigma^2)}
=e^{-2d^2}.
\]

At distance 1,

\[
q=e^{-2}\approx0.135335.
\]

Then at \((0,0)\),

\[
z=q-1-q-q=-1-q=-1.135335.
\]

At \((0,1)\),

\[
z=q-q-1-q=-1-q=-1.135335.
\]

At \((1,1)\),

\[
z=1-3q=1-0.406005=0.593995>0.
\]

All four classifications remain correct.

### Example 3: Add a perturbed point

At \((0.4,0.1)\), distances squared to centers are approximately:

- to \((0,0)\): \(0.17\);
- to \((0,1)\): \(0.97\);
- to \((1,0)\): \(0.37\);
- to \((1,1)\): \(1.37\).

With \(\sigma=0.5\), the largest response is the \((0,0)\) center, and the output is negative. A nearby point on the opposite XOR region may have a different response. This illustrates that finite widths create smooth boundaries.

### Example 4: Ridge fit

If a regularized fit is used,

\[
\mathbf w
=
(\Phi^{\mathsf T}\Phi+\lambda I)^{-1}
\Phi^{\mathsf T}\mathbf y.
\]

As \(\lambda\) increases, the output weights shrink toward zero and the decision margin may become smaller. Validation should choose \(\lambda\), not training accuracy alone.

## Key terms & formulas

- **XOR:** Output 1 when inputs differ.
- **Linear separability:** Existence of one linear boundary; XOR lacks one.
- **Prototype:** Center representing a local region.
- **Gaussian width:** Controls response locality.
- **Feature transformation:** Hidden units convert input into a linearly usable representation.
- **Decision boundary:** Set where output score is zero.
- **Finite-width effect:** Nearby points receive smooth, overlapping responses.

Gaussian:

\[
h_i(\mathbf x)
=\exp\left[-\frac{\|\mathbf x-\mathbf c_i\|^2}{2\sigma^2}\right].
\]

Output:

\[
z=h_{11}-h_{00}-h_{01}-h_{10}.
\]

For four centers and a narrow width, the hidden matrix is approximately

\[
\Phi\approx I_4.
\]

The zero boundary:

\[
h_{11}(\mathbf x)
=h_{00}(\mathbf x)+h_{01}(\mathbf x)+h_{10}(\mathbf x).
\]

## Common mistakes

1. **Claiming one linear neuron can solve XOR.** No single line separates the classes.
2. **Using a wrong Gaussian exponent.** Check \(2\sigma^2\) carefully.
3. **Using a single center for both positive points.** Equal distances make the labels indistinguishable.
4. **Treating an RBF output score as a probability.** Use a declared decision or calibration method.
5. **Ignoring the finite width at the training points.** The response matrix is not exactly the identity unless the width is idealized.
6. **Forgetting the bias or threshold convention.** A zero decision value needs a defined rule.
7. **Concluding RBF is always better than FFNN.** It is a different inductive bias and can overfit with many centers.
8. **Testing only the four clean points.** Perturbed and unseen points test robustness.

## Exam prep

### Likely 2-mark questions

- **Why can a perceptron not solve XOR?**  
  **Hint:** The positive and negative points are not linearly separable.

- **How does an RBFNN solve XOR?**  
  **Hint:** Nonlinear distance-based hidden features followed by a linear output layer.

- **State the four XOR points and labels.**  
  **Hint:** \(00,01,10\to1\); \(11\to0\), or the equivalent binary convention.

- **Write an RBF output function for four XOR centers.**  
  **Hint:** Weighted sum of four Gaussian responses with a sign decision.

- **What is the role of \(\sigma\) in the XOR RBF network?**  
  **Hint:** It controls how local or overlapping the hidden responses are.

### Likely long-answer questions

- **Solve the XOR problem using an RBF network, showing all four evaluations.**  
  **Hint:** Centers, width, hidden responses, output weights, and decision table.

- **Explain why a hidden layer makes XOR possible.**  
  **Hint:** Nonlinear feature transformation and a non-linear-in-input decision boundary.

- **Compare a single perceptron and an RBF network on XOR.**  
  **Hint:** Linear separability, hidden features, prototypes, training, and robustness.

- **Discuss width and center choices for an RBF XOR classifier.**  
  **Hint:** Locality, overlap, noisy data, regularization, and validation.
