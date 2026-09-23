---
subject: sc
unit: 2
topic: fuzzy-logic
syllabus_ref: CSM3202 Unit-II
status: draft
---
# Fuzzy Logic

## Overview

Fuzzy logic extends logic from TRUE/FALSE to truth values in the continuous interval \([0,1]\). It supports statements such as “the room is somewhat warm” and rules that can fire to different degrees. Its central operation is approximate reasoning: conclusions are drawn from partially true premises.

Fuzzy logic is not merely probability with decimals. Probability represents a random event under a model, while fuzzy truth usually represents compatibility, certainty, preference, or similarity. A fuzzy system interprets a crisp input through membership functions, applies linguistic rules, and may return a crisp value through defuzzification.

## Explanation

### 1. Fuzzification and linguistic variables

A **linguistic variable** has a name, a physical domain, linguistic terms, and membership functions. For example:

- variable: TEMPERATURE;
- domain: \(X=[0,50]^\circ C\);
- terms: COLD, COOL, WARM, HOT.

Each term is a fuzzy set:

\[
\mu_{\text{COLD}}(T),\quad
\mu_{\text{COOL}}(T),\quad
\mu_{\text{WARM}}(T),\quad
\mu_{\text{HOT}}(T).
\]

**Fuzzification** maps a crisp input \(x_0\) to the membership grades of relevant linguistic terms. For a triangular COOL set with support \([10,30]\) and core 20,

\[
\mu_{\text{COOL}}(x_0)=\frac{x_0-10}{10},\quad10\le x_0\le20.
\]

If \(x_0=15\), then \(\mu_{\text{COOL}}(15)=0.5\).

### 2. A fuzzy proposition

A crisp proposition \(p\) is true or false. A fuzzy proposition has a variable value,

\[
p'=\text{temperature is WARM},
\]

and its truth or support at input \(T\) is represented by

\[
\mu_{p'}(T)=\mu_{\text{WARM}}(T).
\]

A statement may receive a truth degree for a particular interpretation. It is not valid to remove the input and say the statement is globally 0.7 true; the degree depends on the evidence or variable being evaluated.

### 3. Negation, conjunction, and disjunction

Using the standard operators:

\[
\mu_{\neg p'}(x)=1-\mu_{p'}(x),
\]

\[
\mu_{p'\land q'}(x)=\min(\mu_{p'}(x),\mu_{q'}(x)),
\]

\[
\mu_{p'\lor q'}(x)=\max(\mu_{p'}(x),\mu_{q'}(x)).
\]

Product t-norm/t-conorm and Łukasiewicz t-norm/t-conorm are also common. A complete fuzzy-logic system must specify the selected family.

### 4. Implication and inference

A classical implication \(p\rightarrow q\) is false only for true \(p\) and false \(q\). A fuzzy implication is a function

\[
I:[0,1]^2\rightarrow[0,1].
\]

Common choices include:

- **Zadeh implication:**
  \[
  I_Z(a,b)=\max(1-a,b);
  \]

- **Mamdani min implication:**
  \[
  I_M(a,b)=\min(a,b);
  \]

- **Łukasiewicz implication:**
  \[
  I_L(a,b)=\min(1,1-a+b);
  \]

- **Product implication:**
  \[
  I_P(a,b)=ab.
  \]

In fuzzy inference, min is often used both to obtain the rule's firing strength and as the consequence, producing a clipped output membership. Product gives a smoothly scaled consequence.

### 5. Approximate reasoning

Approximate reasoning means that a conclusion is accepted in proportion to how well its premises are satisfied. For the rule

\[
\text{If }A\text{ then }B,
\]

let

\[
A'=\mu_A(x_0),
\]

the degree to which current evidence matches \(A\). A common rule relation is

\[
B'=\min(A',B)
\]

for min implication, or

\[
B'=A'B
\]

for product implication. The output may be an aggregated fuzzy set, not yet a single number.

A complete chain is:

1. fuzzify crisp inputs;
2. evaluate antecedent matching;
3. apply implication;
4. aggregate rule outputs;
5. defuzzify if a crisp output is needed.

### 6. Compositional rule of inference

A compact general form is

\[
B^*=A^*\circ R,
\]

where:

- \(A^*\) is the current fuzzy input set;
- \(R(A,B)\) is a fuzzy relation representing “\(A\) implies \(B\)”;
- \(\circ\) is a relation-composition operator;
- \(B^*\) is the inferred output set.

With max–min composition,

\[
\mu_{B^*}(y)=\max_x\min\left(\mu_{A^*}(x),\mu_R(x,y)\right).
\]

This is useful for approximate pattern matching, but practical fuzzy controllers usually implement Mamdani or Takagi–Sugeno inference directly.

### 7. Approximate equality and matching

A template fuzzy set \(A\) can be compared with an observed set \(B\) using a sup-min distance:

\[
d_s(A,B)=\sup_x\min(\mu_A(x),\mu_B(x)).
\]

A value near 1 means strong matching; a low value means poor matching. Pattern recognition uses this idea to match an imperfect pattern to a template.

### 8. Fuzzy implication methods in inference

#### Mamdani inference

- Rule firing:
  \[
  \alpha_r=\min(\mu_{A}(x_0),\mu_B(y_0));
  \]
- Consequence:
  \[
  \mu_{C_r'}(z)=\min(\alpha_r,\mu_C(z));
  \]
- Aggregation over rules:
  \[
  \mu_{\text{out}}(z)=\max_r\mu_{C_r'}(z).
  \]

The final output is usually a fuzzy set defuzzified by centroid, bisector, mean of maxima, or smallest/largest-of-maxima.

#### Takagi–Sugeno inference

Each rule has a crisp function:

\[
\text{If }x\text{ is }A\text{ then }z=f_r(x).
\]

The output is a weighted average:

\[
z_{\text{out}}=
\frac{\sum_r\alpha_r f_r(x)}
{\sum_r\alpha_r}.
\]

No separate defuzzification stage is required.

### 9. Fuzzy rule representation

A linguistic fuzzy IF–THEN rule is

\[
(x\text{ is }A)\rightarrow(y\text{ is }B).
\]

A rule is a relation, not the same thing as its firing at one input. Multiple antecedent terms are usually combined with a t-norm:

\[
\alpha=\min(\mu_{A_1},\ldots,\mu_{A_m})
\]

or

\[
\alpha=\prod_{i=1}^{m}\mu_{A_i}.
\]

A consequent fuzzy set is clipped or scaled by the rule weight and antecedent strength.

### 10. Truth versus membership

Suppose “temperature is hot” has membership 0.8 at 40°C. This says 40 is strongly compatible with HOT. It does not say that 80% of the time it is hot or that the event has probability 0.8.

A fuzzy truth value can still have a practical interpretation: the rule is 0.8 supported, the input is 0.8 consistent with the antecedent, or the output is 0.8 close to a target. The interpretation should be stated.

### 11. Advantages and limitations

**Advantages**

- Represents vague linguistic information naturally.
- Uses expert knowledge in readable rules.
- Handles missing, noisy, or imprecise inputs well.
- Produces smooth control rather than abrupt switching.
- Is easier to explain than many black-box models.

**Limitations**

- Rule bases can become large and conflict.
- Membership functions and operators require design choices.
- There is no universal rule guaranteeing the best shape or scale.
- Defuzzification can hide a fuzzy output.
- Calibration may need data and domain experts.
- Fuzzy systems do not automatically give statistical confidence intervals.

### 12. Rule base design

A useful process is:

1. identify inputs and outputs;
2. choose linguistic terms and membership functions;
3. write rules from expert knowledge or data;
4. ensure rule coverage and remove contradictions;
5. set initial rule weights;
6. infer and test representative cases;
7. tune membership functions and weights;
8. validate on cases not used for tuning.

Too many terms create overlap and rules; too few make the system crude. Rules should be readable and testable.

## Worked examples

### Example 1: Evaluate a fuzzy proposition

Define

\[
\mu_{\text{WARM}}(T)=
\begin{cases}
0,&T<20,\\
(T-20)/10,&20\le T<30,\\
1,&30\le T\le35,\\
(40-T)/5,&35<T\le40,\\
0,&T>40.
\end{cases}
\]

At \(T=24\),

\[
\mu_{\text{WARM}}(24)=\frac{24-20}{10}=0.4.
\]

The proposition “temperature is warm” has strength 0.4 for this observation.

### Example 2: Fuzzy rule with min implication

Rule:

> If temperature is WARM, then fan speed is HIGH.

Let

\[
\mu_{\text{WARM}}(T_0)=0.7
\]

and HIGH have membership 1 at the relevant speed. The rule fires to

\[
\alpha=0.7.
\]

The clipped output is

\[
\mu'_{C}(z)=\min(0.7,\mu_{\text{HIGH}}(z)).
\]

Thus the output is at most 0.7 everywhere, but the shape of HIGH is retained.

### Example 3: Product implication

With the same firing strength,

\[
B'(z)=0.7\,\mu_{\text{HIGH}}(z).
\]

This is a scaled output rather than a clipped one. If HIGH membership is 0.6 at one speed, the product result is 0.42; min would give 0.6.

### Example 4: Compositional inference

Let a two-element input fuzzy set be

\[
A^*=[0.8,0.5]
\]

and an implication relation be

\[
R=
\begin{bmatrix}
0.8&0.6\\
0.5&0.4
\end{bmatrix}.
\]

Max–min composition gives

\[
\mu_{B^*}(y_1)=\max(\min(0.8,0.8),\min(0.5,0.5))=0.8,
\]

\[
\mu_{B^*}(y_2)=\max(\min(0.8,0.6),\min(0.5,0.4))=0.6.
\]

Hence

\[
B^*=[0.8,0.6].
\]

### Example 5: Explain an intermediate truth grade

For a rule “If road is wet, increase braking,” suppose wetness membership is 0.4. Using min implication, the increased-braking conclusion is supported to 0.4, not 1. It communicates partial evidence and supports smooth adjustment after defuzzification.

## Key terms & formulas

- **Fuzzification:** Mapping crisp input to membership grades.
- **Linguistic variable:** A variable described by linguistic terms and membership functions.
- **Fuzzy proposition:** A proposition with a variable truth/support degree.
- **Approximate reasoning:** Inferring a graded conclusion from partial premises.
- **Compositional rule:** \(B^*=A^*\circ R\)
- **Mamdani inference:** Clip each consequent by firing strength, aggregate, defuzzify.
- **Takagi–Sugeno inference:** Weight crisp rule outputs.

Core operations:

\[
\neg a=1-a,\quad a\land b=\min(a,b),\quad a\lor b=\max(a,b).
\]

Max–min composition:

\[
\mu_{B^*}(y)=\max_x\min(\mu_{A^*}(x),\mu_R(x,y)).
\]

Rule weight and strength:

\[
\alpha_r=w_r\min_j\mu_{A_{rj}}(x_j).
\]

Mamdani output:

\[
\mu'(z)=\max_r\min(\alpha_r,\mu_{C_r}(z)).
\]

## Common mistakes

1. **Calling fuzzy logic simply a many-valued Boolean logic.** Fuzzy logic includes membership interpretation and approximate reasoning.
2. **Conflating fuzzy truth and probability.** Use the correct interpretation in every result.
3. **Using min implication without stating that the rule weight is applied.** A complete implementation has \(w_r\) and antecedent strength.
4. **Aggregating rules with min only.** Max is the standard Mamdani aggregation; other aggregators are possible.
5. **Applying max–min composition to probability data as if it were a fuzzy relation.** The relation must have fuzzy semantics.
6. **Forgetting the input when quoting a fuzzy proposition's degree.** The degree changes with the observation.
7. **Assuming one membership function is always best.** Shape is chosen from semantics and validation.
8. **Leaving a Mamdani output fuzzy when the application requires a crisp action.** Defuzzify explicitly and state the method.

## Exam prep

### Likely 2-mark questions

- **Define fuzzification with an example.**  
  **Hint:** Convert a crisp measurement into one or more linguistic membership grades.

- **State three standard fuzzy-logic operations.**  
  **Hint:** NOT, AND, OR with \(1-a\), min, and max.

- **What is approximate reasoning?**  
  **Hint:** Derive a graded conclusion when premises are only partly satisfied.

- **Define a fuzzy proposition and give one example.**  
  **Hint:** A linguistic statement with variable truth/support over inputs.

- **Write the compositional rule of inference.**  
  **Hint:** \(B^*=A^*\circ R\).

### Likely long-answer questions

- **Explain fuzzy logic, fuzzification, fuzzy propositions, and fuzzy rules.**  
  **Hint:** Linguistic variables, membership, truth degrees, antecedents and consequents.

- **Describe approximate reasoning using a complete IF–THEN calculation.**  
  **Hint:** Match input, fire rule, apply implication, and explain output.

- **Explain Mamdani and Takagi–Sugeno inference and compare them.**  
  **Hint:** Consequent type, clipping versus function, aggregation, and defuzzification.

- **Differentiate fuzzy logic from classical logic and probability.**  
  **Hint:** Binary versus graded truth, knowledge representation, semantics, and applications.

- **Discuss the design of membership functions and a fuzzy rule base.**  
  **Hint:** Terms, shapes, coverage, conflicts, tuning, and validation.
