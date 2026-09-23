---
subject: sc
unit: 2
topic: fuzzy-propositions
syllabus_ref: CSM3202 Unit-II
status: draft
---
# Fuzzy Propositions

## Overview

A classical proposition has one truth value: true or false. A fuzzy proposition can be true to a degree that depends on the situation being described. It is especially useful for linguistic statements involving vague concepts such as warm, young, safe, or nearly finished.

A fuzzy proposition is normally represented by a fuzzy set or a truth value generated from that set. A rule “If the room is warm” does not become globally true or false; its degree is obtained after a current input is fuzzified.

## Explanation

### 1. Classical and fuzzy propositions

A classical proposition \(p\) has truth function

\[
v(p)\in\{0,1\}.
\]

A fuzzy proposition \(p'\) receives a truth or support value from a continuously graded set, often

\[
v(p')\in[0,1].
\]

Example:

\[
p':\text{ “The temperature is high.”}
\]

If temperature is 30°C and HIGH is represented by a membership function, then

\[
v(p'@30)=\mu_{\text{HIGH}}(30).
\]

The observation is part of the meaning of the truth degree. A fuzzy proposition is not a permanent claim that “30 is 0.7 true.”

### 2. Representation by fuzzy sets

A unary fuzzy proposition about variable \(x\) can be written

\[
A(x)\text{ is }a,
\]

where \(A\) is a fuzzy set in \(X\) and \(a\in X\) is the observed value. Its truth is

\[
v(A(a))=\mu_A(a).
\]

Examples:

- \(v(\text{WARM}(25))=\mu_{\text{WARM}}(25)\);
- \(v(\text{FAST}(65))=\mu_{\text{FAST}}(65)\);
- \(v(\text{SAFE}(0.4))=\mu_{\text{SAFE}}(0.4)\).

A binary proposition “\(x\) is close to \(y\)” is represented by a fuzzy relation

\[
\mu_{\text{close}}(x,y).
\]

A proposition “vehicle \(x\) is older than vehicle \(y\)” is normally crisp or represented with a thresholded relation. Not every relation should be fuzzified.

### 3. Single and multiple propositions

A simple fuzzy proposition is

\[
p':x\text{ is }A.
\]

A compound proposition joins simple propositions:

\[
p'=A(x)\land B(y),
\]

\[
p'=A(x)\lor B(y),
\]

or

\[
p'=A(x)\rightarrow B(y).
\]

Using min and max,

\[
v(p'\land q')=\min(v(p'),v(q')),
\]

\[
v(p'\lor q')=\max(v(p'),v(q')).
\]

Thus a compound statement can be evaluated once all input-dependent terms are known.

### 4. Linguistic hedges and modifiers

Natural language contains qualifiers that modify a fuzzy term.

- **Very:** intensity or concentration.
- **More or less:** dilution.
- **Slightly:** often moves membership toward zero.
- **Extremely:** strengthens a high grade.
- **Approximately:** approximates a value or set.
- **Not:** complement.

A common concentration function is

\[
\mu_{\text{very }A}(x)=\mu_A(x)^2.
\]

A dilution function is

\[
\mu_{\text{more or less }A}(x)=2\sqrt{\mu_A(x)}-\mu_A(x)^2
\]

for values in \([0,1]\). An intensifier can be

\[
\mu_A^\gamma(x)=
\begin{cases}
2\mu_A(x)^2,&0\le\mu_A(x)\le0.5,\\
1-2(1-\mu_A(x))^2,&0.5<\mu_A(x)\le1.
\end{cases}
\]

These conventions vary. An application should define its modifiers rather than assume that “very” has a universal formula.

### 5. Truth value, membership value, and possibility

Three quantities are related but not identical:

1. **Membership:** \(\mu_A(x)\), compatibility of \(x\) with concept \(A\).
2. **Truth value:** how strongly a proposition is supported under an interpretation.
3. **Possibility:** how feasible an event or value is under a possibility model.

Zadeh's possibility theory uses

\[
\min(\mu_A,\mu_B)\le\min(\max(\mu_A,\mu_B),\mu_{A\cup B})
\le\max(\mu_A,\mu_B,\mu_{A\cup B}).
\]

Possibility is not probability. A possibility of 1 means something is fully possible under the model, not that it is certain or has probability 1.

### 6. Fuzzy negation

The standard negation is

\[
\neg A: \mu_{\neg A}(x)=1-\mu_A(x).
\]

If \(A(x)\) has truth 0.7, its negation has truth 0.3. This complement has involution:

\[
\neg\neg A=A.
\]

Other negations exist when a different interpretation is desired, so the model should identify the operator.

### 7. Fuzzy conjunction and disjunction

A proposition may use AND or OR.

#### Min (Kleene or Mamdani convention)

\[
\mu_{p'\land q'}=\min(\mu_{p'},\mu_{q'}),
\]

\[
\mu_{p'\lor q'}=\max(\mu_{p'},\mu_{q'}).
\]

#### Product

\[
\mu_{p'\land q'}=\mu_{p'}\mu_{q'},
\]

\[
\mu_{p'\lor q'}=\mu_{p'}+\mu_{q'}-\mu_{p'}\mu_{q'}.
\]

#### Łukasiewicz

\[
\mu_{p'\land q'}=\max(0,\mu_{p'}+\mu_{q'}-1),
\]

\[
\mu_{p'\lor q'}=\min(1,\mu_{p'}+\mu_{q'}).
\]

For \(a=0.6,b=0.4\), the three conjunctions are \(0.4,0.24,0\), respectively. No operator is “the truth”; each expresses a chosen logical policy.

### 8. Fuzzy implication

An implication from antecedent \(A\) to consequent \(B\) is represented by a relation

\[
R(a,b)
\]

where \(a,b\in[0,1]\). Common formulas are

\[
R_Z(a,b)=\max(1-a,b),
\]

\[
R_M(a,b)=\min(a,b),
\]

\[
R_L(a,b)=\min(1,1-a+b),
\]

\[
R_P(a,b)=ab.
\]

An implication function should satisfy desirable conditions such as \(R(1,1)=1\), \(R(0,1)=1\), and \(R(1,0)=0\), although stronger axiom systems may impose more conditions.

### 9. Generalized modus ponens

A crisp rule is

\[
A\rightarrow B.
\]

With actual input \(A'\), generalized modus ponens derives \(B'\) from \(A'\) and the implication relation:

\[
B'=\mu_{A'\circ R}.
\]

This is approximate rather than exact reasoning. If \(A'\) partially matches \(A\), \(B'\) partially expresses the expected consequent.

### 10. Rule weights and certainty

A fuzzy rule may have a weight

\[
w_r\in[0,1],
\]

representing confidence, importance, or frequency. One convention combines weight and antecedent strength as

\[
\alpha_r=w_r\min_j\mu_{A_{rj}}(x_j).
\]

Do not automatically call this value a probability. A rule weight is usually a designer or expert parameter.

### 11. Contradictory and uncertain propositions

Suppose two sources give

\[
\mu_A(x)=0.8,\qquad
\mu_{\neg A}(x)=0.4.
\]

With standard complement, a fuzzy description of not-\(A\) would be 0.2, so the evidence is inconsistent or the models came from different contexts. Fuzzy logic can represent and combine inconsistency, but it does not by itself resolve which source is correct. A conflict-management policy, data source, or additional evidence is needed.

### 12. Quantified fuzzy propositions

A universal fuzzy proposition might be

\[
\forall x\in X,\quad x\text{ is acceptable},
\]

with truth value based on the minimum:

\[
v(p)=\min_{x\in X}\mu_{\text{acceptable}}(x).
\]

An existential proposition might use maximum:

\[
v(q)=\max_{x\in X}\mu_{\text{acceptable}}(x).
\]

These are the extension-principle interpretations on a finite or well-ordered domain. For a continuous universe, supremum and infimum are generally written instead of max and min.

### 13. Defuzzifying a proposition

If an application needs a crisp statement from a fuzzy truth distribution, possible methods include:

- maximum membership: choose the highest compatible value;
- thresholding: retain values above \(\alpha\);
- centroid: weighted average of output universe;
- bisector: split the area in half;
- mean of maxima.

A thresholded proposition can be written

\[
p_\alpha(x)=1\quad\text{if }\mu_p(x)\ge\alpha,
\]

and 0 otherwise. Threshold selection is itself a design decision.

## Worked examples

### Example 1: Single proposition

Let “high speed” be represented by a Gaussian

\[
\mu_H(v)=\exp\left[-\frac{(v-70)^2}{2(10)^2}\right].
\]

At \(v=60\),

\[
\mu_H(60)=\exp(-100/200)=e^{-0.5}\approx0.6065.
\]

The proposition “speed is high” is strongly but not fully supported for this speed.

### Example 2: Compound proposition

Let “load is heavy” have value 0.8 and “temperature is high” have value 0.6.

With min AND:

\[
v(p\land q)=\min(0.8,0.6)=0.6.
\]

With product AND:

\[
v(p\land q)=0.8\times0.6=0.48.
\]

With Łukasiewicz AND:

\[
v(p\land q)=\max(0,0.8+0.6-1)=0.4.
\]

All are valid operator-dependent results.

### Example 3: Linguistic modifier

If \(\mu_A(x)=0.5\), then using \(\mu_{\text{very }A}=\mu_A^2\),

\[
\mu_{\text{very }A}(x)=0.25.
\]

Using a power hedge \(\mu_A^0.5\),

\[
\mu_{\text{more or less }A}(x)=\sqrt{0.5}\approx0.7071.
\]

The modifier changes the distribution; it does not merely rename the same number in a unique universal way.

### Example 4: Fuzzy implication

For antecedent strength \(a=0.7\) and consequent membership \(b=0.8\):

- Zadeh: \(\max(0.3,0.8)=0.8\);
- min: \(\min(0.7,0.8)=0.7\);
- Łukasiewicz: \(\min(1,0.3+0.8)=1\);
- product: \(0.7\times0.8=0.56\).

The rule-engine design must select one implication and apply it consistently.

### Example 5: Generalized reasoning

Rule: IF speed is HIGH THEN braking pressure is STRONG.

Let \(\mu_{\text{HIGH}}(65)=0.8\), and use min implication. The inferred fuzzy conclusion is

\[
\mu_{B'}(p)=\min(0.8,\mu_{\text{STRONG}}(p)).
\]

If strong pressure is 0.9 at one point, the inferred membership there is 0.8, not 0.9.

### Example 6: Universal and existential propositions

For

\[
\mu_{\text{acceptable}}=[0.4,0.7,0.6]
\]

on a finite domain:

\[
v(\forall x\,acceptable(x))=\min(0.4,0.7,0.6)=0.4,
\]

\[
v(\exists x\,acceptable(x))=\max(0.4,0.7,0.6)=0.7.
\]

The universal statement is as strong as the least acceptable item; the existential statement is as strong as the best item.

## Key terms & formulas

- **Fuzzy proposition:** A statement with input-dependent truth/support in \([0,1]\).
- **Unary proposition:** \(A(x)\).
- **Binary proposition:** represented by a fuzzy relation \(R(x,y)\).
- **Fuzzy truth value:** Degree of support of a proposition.
- **Linguistic modifier:** A word that changes a membership function.
- **Generalized modus ponens:** Derive \(B'\) from \(A'\) and \(A\rightarrow B\).

Standard operators:

\[
\neg\mu=1-\mu,\quad
\mu_{p\land q}=\min(\mu_p,\mu_q),\quad
\mu_{p\lor q}=\max(\mu_p,\mu_q).
\]

Implications:

\[
R_Z=\max(1-a,b),\quad R_M=\min(a,b),
\]

\[
R_L=\min(1,1-a+b),\quad R_P=ab.
\]

Weighted firing strength:

\[
\alpha_r=w_r\min_j\mu_{A_{rj}}(x_j).
\]

## Common mistakes

1. **Assigning a fuzzy proposition a single permanent truth value.** It normally depends on the input or interpretation.
2. **Confusing membership with truth without stating the link.** They are often numerically related in a rule, but their interpretations are distinct.
3. **Treating “very” as a fixed universal modifier.** Define its function in the model.
4. **Using the same connective for every part of a system.** State min, product, Łukasiewicz, or another operator.
5. **Calling a rule weight a probability.** It may be an expert confidence or importance score.
6. **Ignoring contradictions between sources.** Fuzzy representation does not automatically resolve them.
7. **Using max instead of min for a conjunction.** Max is normally disjunction.
8. **Confusing possibility with probability.** Possibility is not a random frequency.

## Exam prep

### Likely 2-mark questions

- **Define a fuzzy proposition.**  
  **Hint:** A statement whose truth/support is graded and depends on an interpretation or input.

- **Write standard fuzzy negation, conjunction, and disjunction.**  
  **Hint:** \(1-a\), min, and max.

- **Give two examples of linguistic modifiers.**  
  **Hint:** Very, more or less, slightly, approximately, extremely.

- **State generalized modus ponens.**  
  **Hint:** From a fuzzy input \(A'\) and implication \(A\to B\), infer \(B'\).

- **Write two fuzzy implication functions.**  
  **Hint:** Zadeh, min, Łukasiewicz, or product.

### Likely long-answer questions

- **Explain fuzzy propositions, their representation, and compound forms.**  
  **Hint:** Input-dependent truth, membership functions, relations, AND/OR, and an example.

- **Discuss linguistic variables and modifiers in fuzzy propositions.**  
  **Hint:** Domain, terms, fuzzification, and very/more-or-less functions.

- **Derive generalized modus ponens using an implication relation.**  
  **Hint:** Define relation matrix, composition, and calculate a numerical output.

- **Compare membership, fuzzy truth, possibility, and probability.**  
  **Hint:** Definitions, interpretation, aggregation behavior, and an example.

- **Explain how a fuzzy proposition can be converted to a crisp output.**  
  **Hint:** Threshold, maximum, centroid, bisector, and design consequences.
