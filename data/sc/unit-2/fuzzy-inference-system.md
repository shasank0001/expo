---
subject: sc
unit: 2
topic: fuzzy-inference-system
syllabus_ref: CSM3202 Unit-II
status: draft
---
# Fuzzy Inference System

## Overview

A fuzzy inference system (FIS) converts numerical inputs into a decision or output using fuzzy membership functions, linguistic rules, an inference engine, and a defuzzifier. Unlike a crisp controller, it can represent gradual concepts and respond smoothly when measurements change.

A complete FIS requires both a model and a design process. This note covers the architecture, a full numerical Mamdani example, a Takagi–Sugeno example, and practical validation.

## Explanation

### 1. Main components

A basic fuzzy inference system has four functional blocks.

#### Fuzzifier

The fuzzifier maps a crisp input \(x_0\) to membership degrees in input fuzzy sets:

\[
\mu_{A}(x_0).
\]

#### Knowledge base or rule base

The rule base contains IF–THEN rules:

\[
\text{If }x\text{ is }A\text{ then }y\text{ is }B.
\]

The knowledge base also stores the membership functions and domain definitions.

#### Fuzzy inference engine

The engine:

1. evaluates each rule's antecedent;
2. combines antecedent terms with a t-norm or t-conorm;
3. applies the implication;
4. combines outputs of all rules.

#### Defuzzifier

The defuzzifier converts the resulting fuzzy output set to one crisp value. Common methods are centroid, bisector, mean of maxima, smallest-of-maxima, and weighted average for singleton/Sugeno outputs.

### 2. Data flow

For crisp input vector

\[
\mathbf x=(x_1,\ldots,x_m),
\]

the FIS computes an output vector

\[
\mathbf y=F(\mathbf x).
\]

A Mamdani FIS follows:

\[
\mathbf x
\rightarrow
\text{membership grades}
\rightarrow
\text{rule weights}
\rightarrow
\text{clipped output sets}
\rightarrow
\text{aggregated fuzzy set}
\rightarrow
\text{crisp }\mathbf y.
\]

This is approximate reasoning: a rule with antecedent grades \((0.8,0.6)\) is not simply accepted or rejected.

### 3. Rule construction

For \(m\) antecedents and rule weight \(w_r\),

\[
\alpha_r=w_rT\left(\mu_{A_{r1}}(x_1),\ldots,\mu_{A_{rm}}(x_m)\right).
\]

For two-input min rules,

\[
\alpha_r=w_r\min(a_1,a_2).
\]

For two-input product rules,

\[
\alpha_r=w_ra_1a_2.
\]

The output depends on the actual truth table or formula selected for the system.

### 4. Mamdani system

In Mamdani inference, each consequence is a fuzzy set \(B_r\). With min implication,

\[
\mu_{B_r'}(z)=\min(\alpha_r,\mu_{B_r}(z)).
\]

The rule outputs are aggregated by max:

\[
\mu_{B'}(z)=\max_r\mu_{B_r'}(z).
\]

A centroid defuzzifier is

\[
z^*=
\frac{\int_a^b z\mu_{B'}(z)\,dz}
{\int_a^b\mu_{B'}(z)\,dz}.
\]

For a discrete output universe,

\[
z^*=
\frac{\sum_{j=1}^{m}z_j\mu_{B'}(z_j)}
{\sum_{j=1}^{m}\mu_{B'}(z_j)}.
\]

The denominator is the area under the output membership function. A zero denominator makes the centroid undefined; the implementation must use a declared fallback.

### 5. Alternative defuzzification methods

#### Mean of maxima

First find \(h=\max_z\mu_{B'}(z)\), then

\[
z_{\text{MOM}}=\frac{1}{|M|}\sum_{z\in M}z,
\]

where

\[
M=\{z:\mu_{B'}(z)=h\}.
\]

#### Bisector

Choose \(z_b\) such that

\[
\int_{a}^{z_b}\mu_{B'}(z)\,dz
=
\frac12\int_a^b\mu_{B'}(z)\,dz.
\]

#### Smallest and largest of maxima

These return the extreme \(z\) values that reach maximum membership. They are discontinuous when the peak changes location and are less smooth than centroid.

### 6. Takagi–Sugeno system

A first-order Sugeno rule is

\[
\text{If }x_1\text{ is }A_{r1}\text{ and }x_2\text{ is }A_{r2}
\text{ then }y=a_rx_1+b_rx_2+c_r.
\]

The crisp output is

\[
y^*=
\frac{\sum_{r=1}^{R}\alpha_rf_r(\mathbf x)}
{\sum_{r=1}^{R}\alpha_r}.
\]

Zero-order Sugeno has constant \(f_r=k_r\).

Sugeno is easier to integrate into numerical controllers and often trains smoothly, but its rules may be less directly interpretable than Mamdani rules.

### 7. Singleton output as a special case

Let a Mamdani rule output a singleton at \(y_r\) with height \(\alpha_r\). If the aggregate can be represented by point masses \(\alpha_r\), centroid becomes

\[
y^*=\frac{\sum_r\alpha_ry_r}{\sum_r\alpha_r}.
\]

This is a weighted average. Do not infer from the numerical similarity that the two architectures are identical; their rule consequences and training behavior differ.

### 8. Choosing the number and shape of membership functions

Fewer terms produce a coarse system. More terms increase resolution but also increase rule combinations. If each input has \(k\) terms, a complete rule base may contain \(k^m\) rules for \(m\) inputs, before exclusions.

A practical design uses:

- three to seven terms per input;
- normal membership functions;
- some overlap;
- universal covering;
- clear expert semantics;
- fewer terms in less important variables.

### 9. Rule-base design and completeness

For \(n\) inputs with terms arranged from low to high, rules can be generated combinatorially, but not all combinations are useful. The designer should:

1. identify dominant combinations;
2. include boundary and exception rules;
3. add conflict-resolution rules if needed;
4. check that important regions are covered;
5. remove redundant rules;
6. verify that no input unexpectedly fires every rule.

### 10. FIS design procedure

1. **Define the problem:** input variables, output variables, constraints, and safety limits.
2. **Choose term sets:** linguistic labels and physical ranges.
3. **Choose membership functions:** parameters and shape.
4. **Build the rule base:** encode expert knowledge.
5. **Select inference operators:** t-norm, implication, aggregation.
6. **Select defuzzification:** centroid, weighted average, or another method.
7. **Tune:** parameters or rule weights using validation data.
8. **Test:** normal, boundary, noisy, and failure cases.
9. **Deploy and monitor:** track output smoothness and rule activity.

### 11. Parameter tuning

Possible parameters include membership-function centers, widths, shoulders, rule weights, and output gains. Tuning minimizes a selected loss:

\[
J(\theta)=\frac1N\sum_{i=1}^{N}
\ell(y_i,F_{\theta}(\mathbf x_i),y_i^*).
\]

For a controller, the loss may combine tracking error, control effort, overshoot, and robustness. A small training error is not enough if the controller becomes sensitive to noise.

### 12. Advantages

- Natural representation of linguistic knowledge.
- Smooth outputs near fuzzy boundaries.
- Robustness to imprecise measurements.
- Rule base can be inspected and modified.
- Handles nonlinear relationships without a full physical model.
- Suitable for moderate data sets and control applications.

### 13. Limitations and common failure modes

- Rule explosion.
- Conflicting rules.
- Poorly placed membership functions.
- Undercoverage of input space.
- Defuzzification dependence on output discretization.
- Difficulty optimizing weights and membership functions together.
- Limited formal verification.
- No automatic statistical uncertainty interpretation.
- Expert rules can be inconsistent.

An FIS should be compared with simpler baselines such as linear control, lookup tables, or ordinary optimization.

## Worked examples

### Example 1: Full two-rule Mamdani calculation

Let the input be temperature \(T\in[0,40]\).

Define:

- LOW: triangle \((0,10,20)\);
- HIGH: triangle \((20,30,40)\).

Rules:

\[
R_1:\text{If }T\text{ is LOW then fan is LOW},
\]

\[
R_2:\text{If }T\text{ is HIGH then fan is HIGH}.
\]

Let the output domain be fan speed \(F\in[0,30]\):

- LOW output: triangle \((0,5,10)\);
- HIGH output: triangle \((20,25,30)\).

At \(T=25\),

\[
\mu_{\text{LOW}}(25)=0,
\]

because the descending LOW side would be below zero outside its support, and

\[
\mu_{\text{HIGH}}(25)=\frac{25-20}{30-20}=0.5.
\]

Thus rule 1 has weight 0 and rule 2 has weight 0.5.

Mamdani outputs:

\[
C_1'(F)=0,
\]

\[
C_2'(F)=\min(0.5,\mu_{\text{HIGH output}}(F)).
\]

For HIGH output,

\[
\mu_H(F)=
\begin{cases}
0,&F<20,\\
(F-20)/5,&20\le F<25,\\
1,&25\le F\le30,\\
0,&F>30.
\end{cases}
\]

The clipped set is

\[
C_2'=
\begin{cases}
0,&F<20,\\
(F-20)/10,&20\le F<25,\\
0.5,&25\le F\le30,\\
0,&F>30.
\end{cases}
\]

Discrete centroid on output points \(F=20,21,\ldots,30\):

Membership values are

\[
[0,0.1,0.2,0.3,0.4,0.5,0.5,0.5,0.5,0.5].
\]

Sum:

\[
0.1+0.2+0.3+0.4+5(0.5)=3.0.
\]

Weighted values:

\[
21(0.1)+22(0.2)+23(0.3)+24(0.4)
+25(0.5)+26(0.5)+27(0.5)+28(0.5)+29(0.5)
\]

\[
=2.1+4.4+6.9+9.6+(12.5+13+13.5+14+14.5)=90.5.
\]

Centroid:

\[
F^*=90.5/3=30.1667.
\]

This is just outside \([20,30]\), revealing an important defuzzification issue: the clipped rising edge is triangular and the output is constant on \([25,30]\), so the centroid shifts slightly beyond the final point. The calculation is correct for the sampled aggregate, but the rule design or output shape is poor. A better-shaped consequent or a singleton-consequent system should be considered.

For a practical one-point rule system, the simpler singleton rules would give 30 at 25°C. This example shows why a numerically valid centroid is not automatically a sensible controller.

### Example 2: First-order Sugeno system

Consider two rules:

\[
R_1:\text{If }x\text{ is LOW, then }y=10+2x,
\]

\[
R_2:\text{If }x\text{ is HIGH, then }y=20+2x.
\]

At \(x=25\), with overlapping triangle memberships

\[
\mu_L=0.5,\qquad \mu_H=0.5,
\]

rule outputs are

\[
f_1=10+2(25)=60,\qquad f_2=20+2(25)=70.
\]

Sugeno output:

\[
y^*=\frac{0.5(60)+0.5(70)}{0.5+0.5}=65.
\]

### Example 3: Tuning a membership function

Suppose a GA changes the center of the HIGH triangle from 30 to 32. It evaluates validation mean squared error over many temperatures. If error decreases and all safety cases remain valid, 32 may be retained. A parameter change should be accepted based on validated behavior, not only appearance.

### Example 4: Zero area handling

If all active rules have firing strength zero, the Mamdani aggregate is the zero fuzzy set and centroid is \(0/0\). A safe system can:

- include a default rule;
- output a safe fallback;
- hold the last valid command;
- enter a diagnostic state.

The chosen fallback should be explicit.

## Key terms & formulas

- **Fuzzifier:** Converts crisp input to membership values.
- **Rule base:** Stores linguistic rules and membership functions.
- **Inference engine:** Evaluates and combines rules.
- **Defuzzifier:** Produces a crisp output.
- **Mamdani:** Fuzzy antecedent and fuzzy consequent.
- **Takagi–Sugeno:** Fuzzy antecedent and crisp function.
- **Firing strength:** Weighted antecedent match.
- **Aggregation:** Combination of all rule outputs.

Firing strength:

\[
\alpha_r=w_rT(\mu_{A_{r1}},\ldots,\mu_{A_{rm}}).
\]

Mamdani:

\[
\mu'(z)=\max_r\min(\alpha_r,\mu_{B_r}(z)).
\]

Centroid:

\[
z^*=\frac{\int z\mu'(z)dz}{\int\mu'(z)dz}
\]

or its discrete sum.

Sugeno:

\[
y^*=\frac{\sum_r\alpha_rf_r(\mathbf x)}
{\sum_r\alpha_r}.
\]

## Common mistakes

1. **Calling fuzzification label assignment.** It produces all relevant membership grades, not necessarily one winner.
2. **Leaving the operator configuration unstated.** Record t-norm, implication, aggregation, and defuzzifier.
3. **Confusing rule firing strength with output value.** A rule can fire strongly and still request a small output.
4. **Assuming centroid always lies in the support.** As the full example shows, it may lie outside a poorly shaped aggregate.
5. **Dividing by zero when output area is zero.** Define a safe fallback.
6. **Using a Sugeno average when all weights are zero.** Again define fallback behavior.
7. **Generating every rule combination blindly.** Rule explosion and conflicts often follow.
8. **Treating membership partitions as probability distributions.** They need not sum to 1.
9. **Validating only in the normal region.** Boundary and fault cases are essential.

## Exam prep

### Likely 2-mark questions

- **List the main components of a fuzzy inference system.**  
  **Hint:** Fuzzifier, knowledge/rule base, inference engine, defuzzifier.

- **Write the centroid defuzzification formula.**  
  **Hint:** Ratio of the first moment to the area.

- **What is the output of a first-order Sugeno FIS?**  
  **Hint:** Normalized weighted sum of rule functions.

- **Why is a t-norm used for an AND antecedent?**  
  **Hint:** It represents conjunctive support with \(T(1,a)=a\).

- **What should be done when all rule firing strengths are zero?**  
  **Hint:** Use a declared default/safe output or diagnostic state.

### Likely long-answer questions

- **Explain the architecture and complete data flow of a fuzzy inference system.**  
  **Hint:** Fuzzification, rule evaluation, implication, aggregation, defuzzification.

- **Work out a complete Mamdani inference example.**  
  **Hint:** State membership functions, evaluate input, clip consequents, aggregate, calculate centroid.

- **Compare Mamdani and Takagi–Sugeno fuzzy inference systems.**  
  **Hint:** Consequents, calculations, defuzzification, interpretability, learning, and applications.

- **Describe a systematic procedure for designing an FIS.**  
  **Hint:** Variables, terms, shapes, rules, operators, tuning, validation, and monitoring.

- **Discuss limitations and applications of fuzzy inference systems.**  
  **Hint:** Rule explosion, tuning, verification, and useful control/decision applications.
