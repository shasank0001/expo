---
subject: sc
unit: 5
topic: dempster-shafer-theory
syllabus_ref: CSM3202 Unit-V
status: draft
---
# Dempster–Shafer Theory

## Overview

Dempster–Shafer (D-S) theory is a framework for representing and combining uncertain evidence. Instead of assigning all probability to one hypothesis, a source can assign belief to a set of possible hypotheses. It is useful when information is incomplete, ambiguous, or conflicting.

A mass function distributes belief among subsets of a frame of discernment. Dempster's rule combines independent evidence, but the normalization step can amplify sensitivity when conflict is high. Therefore, the combination rule, conflict handling, and source-independence assumption must be stated.

## Explanation

### 1. Frame of discernment

The frame of discernment is

\[
\Theta=\{\theta_1,\theta_2,\ldots,\theta_K\}.
\]

It contains all hypotheses under consideration. A focal element is any subset \(A\subseteq\Theta\) receiving positive mass, such as

\[
\{\theta_1\},\quad
\{\theta_1,\theta_2\},\quad
\Theta.
\]

Assigning mass to a set means the source cannot distinguish its elements, not that each element necessarily has equal probability.

### 2. Mass function

A basic belief assignment or mass function \(m\) satisfies

\[
m(\varnothing)=0,
\]

\[
m(A)\ge0\quad\text{for all }A\subseteq\Theta,
\]

\[
\sum_{A\subseteq\Theta}m(A)=1.
\]

For a frame with two hypotheses, possible focal elements are

\[
\varnothing,\{\theta_1\},\{\theta_2\},\{\theta_1,\theta_2\}.
\]

A mass function might be

\[
m(\{\theta_1\})=0.6,\quad
m(\{\theta_1,\theta_2\})=0.4.
\]

No mass is assigned directly to \(\theta_2\), but it remains possible because it is included in the set mass.

### 3. Belief and plausibility

The **belief** of a set \(A\) is the total mass of focal sets contained in \(A\):

\[
Bel(A)=\sum_{B\subseteq A}m(B).
\]

The **plausibility** is the total mass of focal sets that intersect \(A\):

\[
Pl(A)=1-\sum_{B\cap A=\varnothing}m(B)
=\sum_{B:B\cap A\ne\varnothing}m(B).
\]

Every belief is a lower support and every plausibility is an upper support:

\[
Bel(A)\le Pl(A).
\]

If \(m\) assigns no mass to ambiguous sets, belief and plausibility coincide.

### 4. Dempster's combination rule

Let \(m_1\) and \(m_2\) be mass functions from two sources. Their unnormalized conjunctive evidence is

\[
(m_1\oplus m_2)(C)
=
\sum_{A\cap B=C}m_1(A)m_2(B).
\]

The conflict is

\[
K=\sum_{A\cap B=\varnothing}m_1(A)m_2(B).
\]

Dempster's normalized rule is

\[
(m_1\oplus_2m_2)(C)
=
\frac{(m_1\oplus m_2)(C)}
{1-K},\qquad C\ne\varnothing,
\]

and

\[
m(\varnothing)=0.
\]

The normalization makes the total mass one again.

### 5. Three-source combination

Combine sources in sequence:

\[
m_{123}=((m_1\oplus_2m_2)\oplus_2m_3).
\]

Dempster's rule is associative for nonconflicting evidence, so the grouping should not change the result in theory. Numerical calculations can still accumulate error. If the first two sources have high conflict, their normalized output may strongly favor one interpretation before the third is added.

### 6. Conflict and its consequences

If \(K\to1\), the normalization denominator \(1-K\) becomes very small and small unnormalized masses are amplified. This is called the **conflict problem**. A high conflict may indicate:

- contradictory evidence;
- poorly chosen hypotheses;
- dependent sources;
- miscalibrated reliability;
- a need to model an “unknown” hypothesis explicitly.

Dempster's rule is not appropriate without modification for every high-conflict situation. Alternatives include:

- Yager's rule;
- Smets' rule;
- Dubois–Prade;
- averaging or discounting sources;
- explicit unknown frame element.

### 7. Reliability discounting

If a source has reliability \(r\in[0,1]\), one common discount model is

\[
m_r(A)=r\,m(A),\qquad A\ne\Theta,
\]

\[
m_r(\Theta)=r\,m(\Theta)+(1-r).
\]

The missing reliability is assigned to ignorance, \(\Theta\). This prevents an unreliable source from receiving full influence. The discount value is a modeling assumption.

### 8. Example: two hypotheses

Let

\[
\Theta=\{\theta_1,\theta_2\}.
\]

Source \(m_1\):

\[
m_1(\{\theta_1\})=0.6,\quad
m_1(\{\theta_1,\theta_2\})=0.4.
\]

Source \(m_2\):

\[
m_2(\{\theta_2\})=0.7,\quad
m_2(\{\theta_1,\theta_2\})=0.3.
\]

Intersections:

- \(\{\theta_1\}\cap\{\theta_2\}=\varnothing\): conflict
  \[
  0.6(0.7)=0.42;
  \]
- \(\{\theta_1\}\cap\Theta=\{\theta_1\}\):
  \[
  0.6(0.3)=0.18;
  \]
- \(\Theta\cap\{\theta_2\}=\{\theta_2\}\):
  \[
  0.4(0.7)=0.28;
  \]
- \(\Theta\cap\Theta=\Theta\):
  \[
  0.4(0.3)=0.12.
  \]

Thus

\[
K=0.42,
\]

and normalized masses are

\[
m(\{\theta_1\})=\frac{0.18}{0.58}=0.310345,
\]

\[
m(\{\theta_2\})=\frac{0.28}{0.58}=0.482759,
\]

\[
m(\Theta)=\frac{0.12}{0.58}=0.206897.
\]

The conflict is high but normalization is still possible. The combined belief in \(\theta_1\) is 0.3103, and belief in \(\theta_2\) is 0.4828; the remaining 0.2069 is unresolved.

### 9. Decision making

Several decision rules are possible:

- **Maximum belief:** choose the singleton with largest belief.
- **Maximum plausibility:** choose the hypothesis with largest plausibility.
- **Pignistic probability:**
  \[
  BetP(\theta)=
  \sum_{A\ni\theta}\frac{m(A)}{|A|};
  \]
- **Maximum expected utility:** use a utility for each hypothesis.

A decision rule should be selected for the application; D-S theory does not produce one mandatory decision.

### 10. Dempster–Shafer versus probability

Probability assigns mass to individual events and satisfies additivity for mutually exclusive events. D-S belief can assign mass to overlapping sets, representing lack of resolution.

If a mass function is singleton and normalized, it can resemble a probability distribution. In general, converting D-S mass to probability requires a decision rule and loses some set-valued ambiguity.

### 11. Applications

- sensor fusion;
- fault diagnosis;
- target identification;
- medical evidence combination;
- environmental monitoring;
- threat assessment;
- reliability and risk analysis.

D-S is useful when sources have different uncertainty types or cannot provide reliable probabilities. It is less convenient when a complete probabilistic generative model is available.

### 12. Common combination rules and variants

- **Dempster:** normalize by \(1-K\).
- **Yager:** move conflict to ignorance instead of normalizing.
- **Smets:** permit nonzero conflict mass as a model of total conflict.
- **Dubois–Prade:** uses a conflict-resolution choice based on a reference focal element.

The rule changes the result, especially at high conflict. Name the rule in every calculation.

## Worked examples

### Example 1: Combine two simple sources

Use the two-hypothesis sources above. The unnormalized masses are

\[
u(\{\theta_1\})=0.18,\quad
u(\{\theta_2\})=0.28,\quad
u(\Theta)=0.12.
\]

Conflict is 0.42, so the normalizing factor is 0.58. The normalized result is

\[
m(\{\theta_1\})=0.3103,
\quad
m(\{\theta_2\})=0.4828,
\quad
m(\Theta)=0.2069.
\]

The masses sum to

\[
0.3103+0.4828+0.2069=1.0000
\]

after rounding.

### Example 2: Belief and plausibility

For the combined result,

\[
Bel(\{\theta_1\})=0.3103,
\]

\[
Pl(\{\theta_1\})=m(\{\theta_1\})+m(\Theta)
=0.5172.
\]

Thus the evidence gives \(\theta_1\) belief support between about 0.31 and plausibility 0.52. It is not a single probability without a decision convention.

### Example 3: High conflict

If

\[
K=0.99,
\]

the denominator is 0.01. A raw mass of 0.005 becomes 0.5 after normalization. Tiny changes in the source can cause large output changes. Discount the sources, add an unknown hypothesis, or use Yager/Smets rather than blindly using Dempster's rule.

### Example 4: Discount an unreliable source

A source with \(m(\theta_1)=0.8,m(\Theta)=0.2\) and reliability 0.7 becomes

\[
m_r(\theta_1)=0.7(0.8)=0.56,
\]

\[
m_r(\Theta)=0.7(0.2)+0.3=0.44.
\]

Its ability to directly support \(\theta_1\) is reduced, and the missing confidence is treated as ignorance.

## Key terms & formulas

- **Frame of discernment:** \(\Theta\).
- **Focal element:** Set with nonzero mass.
- **Mass function:** \(m(A)\ge0,\sum m(A)=1\).
- **Belief:** \(\operatorname{Bel}(A)=\sum_{B\subseteq A}m(B)\).
- **Plausibility:** \(\operatorname{Pl}(A)=\sum_{B\cap A\ne\varnothing}m(B)\).
- **Conflict:** \(K\) from empty intersections.
- **Dempster rule:** Normalize nonempty conjunctive masses.
- **Ignorance:** Mass assigned to \(\Theta\).

Dempster:

\[
m_{12}(C)=\frac{\sum_{A\cap B=C}m_1(A)m_2(B)}
{1-K},\quad C\ne\varnothing.
\]

Conflict:

\[
K=\sum_{A\cap B=\varnothing}m_1(A)m_2(B).
\]

Pignistic probability:

\[
BetP(\theta)=\sum_{A\ni\theta}\frac{m(A)}{|A|}.
\]

## Common mistakes

1. **Treating mass on a set as equal probability on each element.** A set mass represents unresolved support.
2. **Forgetting to calculate conflict.** Empty intersections must be separated before normalization.
3. **Dividing by \(1-K=0\).** The evidence is completely conflicting; the rule is undefined.
4. **Applying Dempster's rule to dependent sources as if independent.** Double counting can occur.
5. **Ignoring the conflict problem near \(K=1\).** Use discounting or another rule.
6. **Confusing belief and plausibility.** They are lower and upper support.
7. **Using a decision rule without stating it.** Different rules can select different hypotheses.
8. **Claiming D-S mass is always a probability.** Only singleton normalized mass has a direct probability-like interpretation.

## Exam prep

### Likely 2-mark questions

- **Define a mass function in D-S theory.**  
  **Hint:** Nonnegative mass over subsets summing to one, with zero mass on empty set.

- **Define belief and plausibility.**  
  **Hint:** Sum of masses of focal sets contained in A and intersecting A.

- **Write Dempster's combination rule.**  
  **Hint:** Conjoin mass functions, compute conflict \(K\), normalize nonempty masses.

- **What is the conflict problem?**  
  **Hint:** \(K\) near 1 makes normalization highly sensitive.

- **Name two applications of D-S theory.**  
  **Hint:** Sensor fusion, diagnosis, target identification, or risk analysis.

### Likely long-answer questions

- **Explain D-S theory, mass functions, belief, and plausibility.**  
  **Hint:** Frame, focal sets, definitions, and an example.

- **Perform a complete two-source D-S combination numerically.**  
  **Hint:** Intersections, conflict, normalization, and resulting masses.

- **Compare D-S theory with probability.**  
  **Hint:** Set-valued mass, belief/plausibility, decision rules, and interpretation.

- **Explain the conflict problem and alternative combination rules.**  
  **Hint:** High \(K\), normalization sensitivity, Yager/Smets, discounting, and source dependence.
