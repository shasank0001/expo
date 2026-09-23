---
subject: sc
unit: 2
topic: multi-valued-logic
syllabus_ref: CSM3202 Unit-II
status: draft
---
# Multi-Valued Logic

## Overview

Classical logic uses only TRUE and FALSE. Multi-valued logic adds one or more truth grades between or beyond those two values. The extra values can describe uncertainty, indeterminacy, degree of truth, or a failure of reference.

A three-valued system may use FALSE, UNKNOWN, and TRUE. A fuzzy logic uses a continuum from 0 to 1. Multi-valued logic therefore provides the bridge from Boolean reasoning to fuzzy propositions and fuzzy inference.

## Explanation

### 1. Motivation

Sometimes a statement is neither clearly true nor clearly false. Examples include “the patient is anaemic” before a precise threshold is established, or “the person is a child” when the age is uncertain. A multi-valued system can assign an intermediate label.

This does not mean that the underlying proposition has several physical truth values. It means the decision procedure has a third classification, such as UNKNOWN.

### 2. Three-valued logic

A common value set is

\[
V_3=\{0,1,\tfrac12\},
\]

where 0 is false, \(1/2\) is unknown, and 1 is true. This is Kleene's strong three-valued logic.

#### Negation

A symmetric definition is

\[
\neg 0=1,\qquad
\neg 1=0,\qquad
\neg\tfrac12=\tfrac12.
\]

#### AND (min)

\[
a\land b=\min(a,b).
\]

| \(\land\) | 0 | 1/2 | 1 |
|---|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1/2 | 0 | 1/2 | 1/2 |
| 1 | 0 | 1/2 | 1 |

#### OR (max)

\[
a\lor b=\max(a,b).
\]

| \(\lor\) | 0 | 1/2 | 1 |
|---|---:|---:|---:|
| 0 | 0 | 1/2 | 1 |
| 1/2 | 1/2 | 1/2 | 1 |
| 1 | 1 | 1 | 1 |

With min, max, and this negation, AND and OR recover the classical truth table when only 0 and 1 are present.

#### Implication

Several implications are possible. A common choice is

\[
a\rightarrow b=\neg a\lor b.
\]

Using the tables:

| \(\rightarrow\) | 0 | 1/2 | 1 |
|---|---:|---:|---:|
| 0 | 1 | 1 | 1 |
| 1/2 | 1/2 | 1/2 | 1 |
| 1 | 0 | 1/2 | 1 |

Another Łukasiewicz-style implication is

\[
a\rightarrow b=\min(1,1-a+b).
\]

The exact table depends on the chosen definition. The implication must be named.

### 3. Łukasiewicz logic

Łukasiewicz logic is based on the unit interval

\[
V=[0,1].
\]

Its standard operations are

\[
\neg a=1-a,
\]

\[
a\land b=\max(0,a+b-1),
\]

\[
a\lor b=\min(1,a+b),
\]

\[
a\rightarrow b=\min(1,1-a+b).
\]

For \(a=0.4\), \(b=0.7\):

\[
a\land b=\max(0,0.1)=0.1,
\]

\[
a\lor b=\min(1,1.1)=1,
\]

\[
a\rightarrow b=\min(1,1.3)=1.
\]

The Łukasiewicz AND is often called the bounded product or Łukasiewicz t-norm. The Łukasiewicz OR is the bounded sum t-conorm.

### 4. Gödel logic

Gödel logic also uses the unit interval but defines a sharp order.

#### Gödel t-norm

\[
a\land_G b=\min(a,b).
\]

#### Gödel t-conorm

\[
a\lor_G b=
\begin{cases}
\max(a,b),&\max(a,b)<1,\\
1,&\text{otherwise}.
\end{cases}
\]

Thus \(0.2\lor_G0.7=0.7\), but \(0.7\lor_G1=1\).

#### Gödel implication

\[
a\to_G b=
\begin{cases}
1,&a\le b,\\
b,&a>b.
\end{cases}
\]

These operations form the standard Gödel many-valued logic.

### 5. Product logic

Product t-norm and t-conorm are

\[
a\land_P b=ab,
\]

\[
a\lor_P b=a+b-ab.
\]

For \(a=0.4\), \(b=0.7\):

\[
a\land_Pb=0.28,
\]

\[
a\lor_Pb=0.4+0.7-0.28=0.82.
\]

The product conorm is also called the probabilistic sum or bounded sum. Product logic is useful when conjunction should be more conservative than min.

### 6. Other finite-valued systems

#### Finite Łukasiewicz logic

For \(k+1\) values

\[
V_k=\{0,\tfrac1k,\ldots,1\},
\]

Łukasiewicz operations can be defined on the grid using the real formulas followed by appropriate boundary behavior. Fuzzifying a crisp system means every strict logical boundary may become a graded transition.

#### Belnap's logic

Belnap logic uses a set with two independent dimensions, for example

\[
\{0,1,B,N\},
\]

where B is “both true and false” and N is “neither true nor false.” It is useful in inconsistent information systems.

#### Bochvar and Priest logics

Bochvar logic introduces an unknown value that contaminates many operations, often making an expression unknown if any part is unknown. Priest's paraconsistent logic permits a statement to be both true and false without arbitrary explosion.

#### Modal multi-valued logics

Fuzzy modal logic adds truth degree to propositions involving necessity, possibility, belief, or knowledge. They are not required in the core CSM3202 syllabus, but show that graded truth can be combined with other logics.

### 7. Why operations must be chosen

Two t-norms both act like intersection, but they behave differently at intermediate values:

- min gives \(0.4\land0.7=0.4\);
- product gives \(0.4\land0.7=0.28\);
- Łukasiewicz gives \(0.4\land0.7=0.1\).

The choice expresses a modeling policy. In a rule, the weakest antecedent may be a reasonable basis, or the designer may want several moderate supports to accumulate less strongly. Numerical choice without a stated interpretation can make results difficult to reproduce.

### 8. Desirable algebraic properties

A fuzzy conjunction is a binary operation \(T:[0,1]^2\to[0,1]\) that is:

- **commutative:** \(aTb=bTa\);
- **associative:** \((aTb)Tc=aT(bTc)\);
- **monotone:** if \(a\le b\), then \(aTc\le bTc\);
- **boundary preserving:** \(aT1=a\) and \(aT0=0\) for a t-norm.

A fuzzy disjunction \(S\) is commutative, associative, monotone, and satisfies \(aS0=a\), \(aS1=1\) for a t-conorm. A negation \(N\) should satisfy

\[
N(0)=1,\qquad N(1)=0,
\]

and an involutive negation also satisfies \(N(N(a))=a\). Many alternative negations exist, so “the complement” is not always uniquely \(1-a\).

### 9. Truth, membership, and uncertainty

A multi-valued truth value describes the status of a proposition. A fuzzy membership value describes compatibility with a concept. They often play the same numerical role in an inference rule, but the interpretation must be kept consistent.

A probability \(P(A)=0.7\) means a probability model assigns 0.7 to event \(A\). It is not automatically a truth degree. A fuzzy proposition can use \(\mu_A(x)=0.7\) to say \(x\) is 0.7 compatible with class \(A\).

### 10. From multi-valued logic to fuzzy inference

A fuzzy rule such as

\[
\text{If temperature is HIGH then fan is FAST}
\]

uses HIGH and FAST as fuzzy sets. Their membership values act as truth-like grades. The rule can fire approximately rather than only when the input is fully HIGH.

A multi-valued system with a few named values can be easier to explain:

- HIGH = 0.9;
- MEDIUM-HIGH = 0.7;
- UNKNOWN = 0.5.

A continuous fuzzy system avoids forcing intermediate values into a few arbitrary categories.

## Worked examples

### Example 1: Three-valued rule evaluation

Let \(p=\text{input is hot}\) have value 1/2, and \(q=\text{output should be high}\) have value 1.

For AND:

\[
p\land q=\min(1/2,1)=1/2.
\]

For OR:

\[
p\lor q=\max(1/2,1)=1.
\]

For symmetric negation:

\[
\neg p=1/2.
\]

The UNKNOWN value remains unknown under negation; it is not silently converted to true or false.

### Example 2: Compare t-norms

For \(a=0.6,b=0.4\):

\[
\min(a,b)=0.4,
\]

\[
ab=0.24,
\]

\[
\max(0,a+b-1)=0.
\]

All satisfy the required boundary values at 0 and 1, but they imply different rule strengths.

### Example 3: Łukasiewicz implication

Let \(a=0.8\) and \(b=0.5\).

\[
a\to b=\min(1,1-0.8+0.5)=0.7.
\]

Using the other Łukasiewicz form,

\[
\neg a\lor b=(1-0.8)+0.5=0.7,
\]

because the sum is already below 1.

### Example 4: Three-valued sensor system

A sensor rule says a component is safe if temperature is LOW and vibration is LOW. Suppose temperature is definitely LOW (membership 1) and vibration is UNKNOWN (0.5).

With Kleene min:

\[
w=\min(1,0.5)=0.5.
\]

The system can report a partially supported safety conclusion. A strict classical system would either accept an uncertain input or reject the rule, which are both less informative.

### Example 5: Product aggregation

Suppose two independent-looking supports are 0.8 and 0.5. The product gives

\[
0.8\times0.5=0.4,
\]

while min gives

\[
\min(0.8,0.5)=0.5.
\]

The product treats two partial factors as multiplying, which is often useful in conjunctive rules. It should not be described as a probability unless the model explicitly supports that interpretation.

## Key terms & formulas

- **Multi-valued logic:** Logic with more than two truth values.
- **Kleene 3-valued logic:** Values \(0,1/2,1\).
- **Unknown:** Inability to classify as true or false.
- **t-norm:** Commutative, associative, monotone conjunction with identity 1.
- **t-conorm:** Corresponding disjunction with identity 0.

Kleene operations:

\[
\neg(1/2)=1/2,\quad
a\land b=\min(a,b),\quad
a\lor b=\max(a,b).
\]

Łukasiewicz:

\[
\neg a=1-a,\quad
a\land b=\max(0,a+b-1),
\]

\[
a\lor b=\min(1,a+b),\quad
a\to b=\min(1,1-a+b).
\]

Product:

\[
a\land b=ab,\quad a\lor b=a+b-ab.
\]

Gödel:

\[
a\land_Gb=\min(a,b),\quad
a\to_Gb=
\begin{cases}
1,&a\le b,\\
b,&a>b.
\end{cases}
\]

## Common mistakes

1. **Using max for conjunction or min for disjunction by accident.** Min is AND; max is OR in fuzzy notation.
2. **Assuming every multi-valued logic has the same implication.** Implication is system-dependent.
3. **Calling \(\neg(1/2)=1/2\) mandatory.** Other negations exist; symmetric negation is one choice.
4. **Treating UNKNOWN as a probability 0.5.** It may be an epistemic label, not a numeric probability.
5. **Claiming a t-norm equals classical AND at every intermediate value.** It agrees at 0 and 1, not generally elsewhere.
6. **Ignoring required t-norm properties.** Arbitrary arithmetic is not automatically a logical conjunction.
7. **Using probability symbols for membership without explanation.** A mapping between the two is an extra modeling step.
8. **Fuzzifying without specifying the operator family.** State the conjunction, disjunction, complement, and implication used.

## Exam prep

### Likely 2-mark questions

- **What is multi-valued logic?**  
  **Hint:** A logic with more than the two classical truth values.

- **Write Kleene's AND, OR, and NOT for \(0,1/2,1\).**  
  **Hint:** Min, max, and symmetric unknown.

- **List two Łukasiewicz operations.**  
  **Hint:** \(1-x\), \(\max(0,x+y-1)\), and bounded sum.

- **Define t-norm properties.**  
  **Hint:** Commutative, associative, monotone, identity 1.

- **Differentiate UNKNOWN from probability 0.5.**  
  **Hint:** Classification versus a numerical random-model probability.

### Likely long-answer questions

- **Explain three-valued logic with truth tables.**  
  **Hint:** Values, NOT/AND/OR, implication choice, and recovery of Boolean behavior at 0 and 1.

- **Compare Łukasiewicz, Gödel, and product fuzzy operations.**  
  **Hint:** Formula and numerical example for each, then discuss different behavior at intermediate values.

- **Explain how t-norms and t-conorms generalize Boolean AND/OR.**  
  **Hint:** Required algebraic properties, boundary values, and min/product/Łukasiewicz examples.

- **Differentiate multi-valued truth, fuzzy membership, and probability.**  
  **Hint:** Proposition status, concept compatibility, and random-event probability; include a conversion warning.

- **Describe the progression from Boolean to three-valued to continuous fuzzy logic.**  
  **Hint:** More values, finer distinctions, continuous membership, and increased modeling flexibility.
