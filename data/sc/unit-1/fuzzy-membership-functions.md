---
subject: sc
unit: 1
topic: fuzzy-membership-functions
syllabus_ref: CSM3202 Unit-I
status: draft
---
# Fuzzy Membership Functions

## Overview

A fuzzy membership function assigns each input a degree of belonging between 0 and 1. It turns a raw number into the linguistic degree used by a fuzzy rule—for example, how strongly a temperature is “high.”

The shape of the membership function is a modeling decision. It should fit the domain, reflect expert meaning, and avoid unnecessary parameters. Triangular, trapezoidal, S-shaped, and Gaussian functions are common.

## Explanation

### 1. Definition and parts

A membership function for fuzzy set \(A\) is

\[
\mu_A:X\rightarrow[0,1].
\]

Its **domain** is the universe \(X\), its **range** is \([0,1]\), and its graph shows how membership changes. The core is where \(\mu_A(x)=1\), the support is where \(\mu_A(x)>0\), and the crossover is where \(\mu_A(x)=0.5\).

The function must obey

\[
0\le\mu_A(x)\le1
\]

for every \(x\in X\).

### 2. Singleton membership function

A singleton fuzzy set at \(c\) is

\[
\mu(x)=
\begin{cases}
1,&x=c,\\
0,&x\ne c.
\end{cases}
\]

In symbolic fuzzy notation,

\[
\tilde c=\frac1c.
\]

It is the crispest type-1 fuzzy set: only one exact value has full membership.

### 3. Triangular membership function

A triangular fuzzy set with support \([a,c]\) and core at \(b\), where \(a<b<c\), is

\[
\mu_A(x)=
\begin{cases}
0,&x\le a,\\
\dfrac{x-a}{b-a},&a<x<b,\\
1,&b\le x\le c,\\
\dfrac{c-x}{c-b},&c<x,\\
0,&x\ge c.
\end{cases}
\]

It has three parameters: lower support boundary, core location, and upper support boundary. A triangle is normal because it reaches 1.

### 4. Trapezoidal membership function

A trapezoidal fuzzy set has a plateau rather than a single core point. With \(a<b<c<d\),

\[
\mu_A(x)=
\begin{cases}
0,&x\le a,\\
(x-a)/(b-a),&a<x<b,\\
1,&b\le x\le c,\\
(d-x)/(d-c),&c<x<d,\\
0,&x\ge d.
\end{cases}
\]

The core is the interval \([b,c]\). Trapezoids are useful when a range of values is considered fully high or low.

### 5. S-shaped membership function

An S-shaped function gives a smooth, sigmoid-like transition. A common logistic form is

\[
\mu_A(x)=\frac{1}{1+\exp[-k(x-c)]},
\]

where \(c\) is the midpoint and \(k>0\) controls steepness.

The function is 0.5 at \(x=c\). Larger \(k\) makes the transition sharper; smaller \(k\) makes it gradual. It never reaches exactly 0 or 1 for finite \(x\), so on an unbounded domain it approaches them asymptotically.

A piecewise S-curve is also common. Let \(a<a'<b'<b\), where \(a\) and \(b\) are the outer feet and \(a'\), \(b'\) are the shoulders. A standard form is

\[
\mu_A(x)=
\begin{cases}
0,&x\le a,\\
2\left(\dfrac{x-a}{a'-a}\right)^2,&a<x<a',\\
1,&a'\le x\le b',\\
1-2\left(\dfrac{b-x}{b-b'}\right)^2,&b'<x<b,\\
1,&x\ge b.
\end{cases}
\]

The value is 0 at the outer left foot, 1 at the lower shoulder \(a'\), remains 1 through the upper shoulder \(b'\), and is 1 at the outer right foot. The 0.5 levels occur inside the two quadratic transition segments. Some textbooks call the points at membership 0.5 the crossovers, so the parameter terminology must be documented.

### 6. Z-shaped membership function

A Z-shaped function is intended to represent “not high” or decreasing membership. A common logistic form is

\[
\mu_A(x)=\frac{1}{1+\exp[k(x-c)]}.
\]

It equals 0.5 at \(c\), approaches 1 on the left, and approaches 0 on the right. The piecewise Z-curve is often used when exact shoulder and crossover values are required.

### 7. Gaussian membership function

A Gaussian fuzzy set is

\[
\mu_A(x)=\exp\left[-\frac{(x-c)^2}{2\sigma^2}\right],
\]

where \(c\) is the center and \(\sigma>0\) is the spread.

Properties:

- \(\mu_A(c)=1\), so a single Gaussian is normal;
- it is symmetric about \(c\);
- membership is close to 0 far from \(c\);
- larger \(\sigma\) gives a wider, softer set;
- it is never exactly 0 for finite \(x\).

A Gaussian with nonzero baseline has the form

\[
\mu(x)=\exp\left[-\frac{(x-c)^2}{2\sigma^2}\right],
\]

and often a product or minimum with the universe boundary is used if exact zero outside a range is required.

### 8. Generalized bell membership function

A generalized bell function is

\[
\mu_A(x)=\frac{1}{1+\left|\frac{x-c}{a}\right|^{2b}},
\]

where \(a>0\) controls width, \(b>0\) controls shape, and \(c\) is the center. It reaches 1 at \(c\) and approaches 0 as \(|x-c|\) becomes large.

### 9. Other functions

- **Ramp:** a linear increasing or decreasing membership segment.
- **Piecewise linear:** arbitrary control points joined with straight lines.
- **Intuitionistic fuzzy set:** includes both a membership function and a non-membership function subject to their constraints.
- **Type-2 function:** assigns a fuzzy set of secondary grades instead of one grade.

These alternatives are selected according to the meaning of the term, the available expertise, and computational cost.

### 10. Designing membership functions

A practical design procedure is:

1. Identify the linguistic term, such as LOW, MEDIUM, or HIGH.
2. Establish the physical domain and units.
3. Ask which values are completely outside, completely inside, and transitional.
4. Choose shoulder, core, and crossover points.
5. Choose a shape: piecewise linear is transparent; Gaussian is smooth.
6. Check overlap and coverage of neighbouring terms.
7. Validate the function against examples and expert judgment.
8. Adjust it if possible with data or optimization.

Good fuzzy partitions usually have overlap, because one input can be both somewhat medium and somewhat high. Poorly placed functions leave gaps, forcing an input to have no linguistic description, or make terms almost identical, making the rule base redundant.

### 11. Symmetrical and asymmetrical fuzzy sets

A symmetric set has the same shape and spread on both sides of its core. Real variables are often asymmetric. For example, an acceptable temperature range may extend much farther below the comfort point than above it. Separate breakpoints or Gaussian spread parameters are then required.

### 12. Universal covering and linguistic completeness

A good partition should cover the domain. If a value belongs to none of LOW, MEDIUM, or HIGH, a rule may not fire. Ensuring at least one term has positive membership is called **universal covering**. It is not necessary that one term always equal 1 for every input, although doing so makes the system normal.

## Worked examples

### Example 1: Triangular set

Let “warm” have \(a=15\), \(b=25\), and \(c=35\):

\[
\mu_W(x)=
\begin{cases}
0,&x\le15,\\
(x-15)/10,&15<x<25,\\
1,&25\le x\le35,\\
(35-x)/10,&35<x,\\
0,&x\ge35.
\end{cases}
\]

For \(x=20\),

\[
\mu_W(20)=\frac{20-15}{25-15}=0.5.
\]

For \(x=32\),

\[
\mu_W(32)=\frac{35-32}{35-25}=0.3.
\]

For \(x=28\),

\[
\mu_W(28)=1.
\]

### Example 2: Trapezoidal set

Let “low” be \((a,b,c,d)=(0,5,10,20)\). Then

\[
\mu_L(x)=
\begin{cases}
0,&x<0,\\
x/5,&0\le x<5,\\
1,&5\le x\le10,\\
(20-x)/10,&10<x\le20,\\
0,&x>20.
\end{cases}
\]

At \(x=3\),

\[
\mu_L(3)=3/5=0.6.
\]

At \(x=15\),

\[
\mu_L(15)=(20-15)/10=0.5.
\]

The entire interval \([5,10]\) belongs fully to LOW.

### Example 3: Gaussian calculation

Let

\[
\mu_A(x)=\exp\left[-\frac{(x-25)^2}{2(4)^2}\right].
\]

At \(x=21\),

\[
\mu_A(21)=\exp(-16/32)=e^{-0.5}\approx0.6065.
\]

At \(x=25\),

\[
\mu_A(25)=1.
\]

With \(\sigma=4\), the function is still \(e^{-0.5}\approx0.6065\) at 29 by symmetry.

### Example 4: Overlap in a two-term partition

Let LOW be \((0,5,15)\) and HIGH be \((10,20,30)\). For \(x=12\),

\[
\mu_{\text{LOW}}(12)=\frac{15-12}{15-5}=0.3,
\]

\[
\mu_{\text{HIGH}}(12)=\frac{12-10}{20-10}=0.2.
\]

The total is 0.5, which is allowed; fuzzy partitions need not sum to 1. This overlap expresses that 12 is between low and high.

### Example 5: Selecting a membership function

If operators need a transparent rule “below 20 is fully safe, 20–30 declines linearly, above 30 is not safe,” a trapezoidal or piecewise-linear function is ideal. If a temperature sensor exhibits smooth physical variation and the application can use more parameters, a Gaussian or S-shaped function may fit better. The choice should follow data or expert semantics, not fashion.

## Key terms & formulas

- **Domain:** \(X\)
- **Range:** \([0,1]\)
- **Core:** \(\{x:\mu(x)=1\}\)
- **Support:** \(\{x:\mu(x)>0\}\)
- **Crossover:** usually \(\{x:\mu(x)=0.5\}\)
- **Singleton:** \(\mu(x)=1\) at one point and 0 elsewhere
- **Symmetry:** \(\mu(c-d)=\mu(c+d)\)

Triangle:

\[
\mu(x)=
\begin{cases}
0,&x\le a\\
\frac{x-a}{b-a},&a<x<b\\
1,&b\le x\le c\\
\frac{c-x}{c-b},&c<x\\
0,&x\ge c
\end{cases}
\]

Trapezoid:

\[
\mu(x)=
\begin{cases}
0,&x<a\\
\frac{x-a}{b-a},&a\le x<b\\
1,&b\le x\le c\\
\frac{d-x}{d-c},&c<x\le d\\
0,&x>d
\end{cases}
\]

Logistic S:

\[
\mu(x)=\frac{1}{1+\exp[-k(x-c)]}.
\]

Gaussian:

\[
\mu(x)=\exp\left[-\frac{(x-c)^2}{2\sigma^2}\right].
\]

## Common mistakes

1. **Confusing a membership function with a probability density.** A membership function maps the input to a degree in \([0,1]\).
2. **Forgetting the core in a triangle or trapezoid.** The function must stay within 0 and 1.
3. **Using an invalid parameter order.** A triangle requires \(a<b<c\); a trapezoid requires \(a<b<c<d\).
4. **Assuming neighboring memberships sum to 1.** Fuzzy partitions usually overlap and need not be normalized by sum.
5. **Using a Gaussian on an unbounded domain and calling it exactly zero everywhere outside support.** It only approaches zero.
6. **Choosing a steep sigmoid without considering noisy data.** A sharp membership boundary can behave like a crisp threshold.
7. **Tuning membership functions without checking expert interpretation.** Lower accuracy is acceptable if the rule remains meaningful and safe.
8. **Writing a Z-shaped function as increasing.** The standard Z shape decreases.

## Exam prep

### Likely 2-mark questions

- **Define a fuzzy membership function and identify its domain and range.**  
  **Hint:** \(\mu_A:X\to[0,1]\).

- **Write a triangular membership function.**  
  **Hint:** Use \(a<b<c\), linear rise, core 1, linear fall, and zero outside.

- **Give the Gaussian membership function and define its parameters.**  
  **Hint:** Center \(c\), spread \(\sigma>0\).

- **What are support, core, and crossover?**  
  **Hint:** Positive membership, full membership, and usually 0.5 membership.

### Likely long-answer questions

- **Explain triangular, trapezoidal, S-shaped, Z-shaped, and Gaussian membership functions.**  
  **Hint:** Draw or describe each graph, list parameters, and compare smoothness and interpretability.

- **Describe the procedure for designing membership functions.**  
  **Hint:** Domain, semantics, full/partial/nonmember regions, shape, overlap, coverage, and validation.

- **Calculate memberships for a specified triangle or Gaussian and explain the result.**  
  **Hint:** Show piecewise evaluation and identify full, partial, and nonmembership.

- **Compare symmetric and asymmetric membership partitions.**  
  **Hint:** Equal spread versus separate breakpoints, and use a practical application.

- **Explain universal covering and overlap in a fuzzy partition.**  
  **Hint:** At least one term should be positive; neighboring terms can overlap without summing to one.
