---
subject: sc
unit: 2
topic: fuzzy-inference-rules
syllabus_ref: CSM3202 Unit-II
status: draft
---
# Inference Rules for Fuzzy Propositions

## Overview

A fuzzy inference rule connects linguistic conditions to an action, conclusion, or output. Unlike a Boolean rule, it can fire partially when the input only approximately matches its antecedent. The engine then modifies or scales the consequent and combines outputs from all active rules.

A good rule-based system specifies its antecedents, consequent type, t-norm, implication, rule weight, aggregation, and defuzzification. Omitting one of these choices can make the calculation irreproducible.

## Explanation

### 1. Anatomy of a fuzzy rule

A rule has the form

\[
\text{IF }x_1\text{ is }A_1\text{ AND }x_2\text{ is }A_2
\text{ THEN }y\text{ is }B.
\]

The variables \(x_1,x_2\) are inputs and \(y\) is the output. \(A_1,A_2\) are antecedent fuzzy sets and \(B\) is a fuzzy or crisp consequent.

A rule may have an importance weight:

\[
w\in[0,1].
\]

The base rule is often stored as

\[
R_r=(A_1,A_2,B,w_r).
\]

### 2. Fuzzification

For crisp measurements \(x_1^0,x_2^0\), evaluate

\[
a_{rj}=\mu_{A_{rj}}(x_j^0).
\]

For example, if LOW has membership 0.8 at a load of 3 kg and HIGH has membership 0.4, the two grades are stored separately. Fuzzification does not force a single label.

### 3. Antecedent combination

A rule containing AND usually uses a t-norm. For \(m\) antecedent terms,

\[
\alpha_{\text{fire}}=\min(a_1,\ldots,a_m)
\]

for min, or

\[
\alpha_{\text{fire}}=\prod_{j=1}^{m}a_j
\]

for product.

The rule weight is included as

\[
\alpha_r=w_r\alpha_{\text{fire}}.
\]

For OR, a t-conorm is used:

\[
\alpha_{\text{fire}}=\max(a_1,\ldots,a_m)
\]

or bounded sum.

### 4. Rule implication

After computing \(\alpha_r\), the consequent is combined with the rule strength.

#### Mamdani min implication

\[
\mu_{B_r'}(z)=\min(\alpha_r,\mu_{B_r}(z)).
\]

The output is clipped above by \(\alpha_r\).

#### Product implication

\[
\mu_{B_r'}(z)=\alpha_r\mu_{B_r}(z).
\]

The whole consequent is scaled by \(\alpha_r\).

#### Łukasiewicz implication

\[
\mu_{B_r'}(z)=\min(1,1-\alpha_r+\mu_{B_r}(z)).
\]

#### Reichenbach implication

A common t-norm-based form is

\[
\mu_{B_r'}(z)=\max(\alpha_r,\mu_{B_r}(z))
\]

when \(\alpha_r\) and \(\mu_B\) denote the relevant rule/consequent compatibility under the selected convention. The exact formula must be stated because implication naming varies.

### 5. Aggregation of rule outputs

Each fired rule gives a fuzzy set \(B_r'\). The engine combines them.

#### Max aggregation

\[
\mu_{B'}(z)=\max_r\mu_{B_r'}(z).
\]

Max is standard in Mamdani systems. It preserves the highest support from any rule and does not accidentally accumulate repeated evidence too strongly.

#### Bounded-sum aggregation

\[
\mu_{B'}(z)=\min\left(1,\sum_r\mu_{B_r'}(z)\right).
\]

This is useful when the combined evidence of several rules should increase support. A large number of rules can then saturate at 1.

#### Bounded difference or other operators

\[
\mu_{B'}(z)=\max_r\left[\alpha_r-\mu_{B_r}(z)\right]
\]

is one alternative, but the choice should match the intended evidence model.

### 6. Mamdani rule inference

A complete Mamdani sequence is:

1. compute antecedent memberships;
2. combine them with a t-norm;
3. multiply by rule weight;
4. clip or scale the consequent fuzzy set;
5. aggregate all rule consequents;
6. defuzzify the aggregate.

This produces a transparent fuzzy output before the final crisp action.

### 7. Takagi–Sugeno rules

A zero-order Sugeno rule has constant consequent:

\[
\text{If }x\text{ is }A\text{ then }z=k_r.
\]

A first-order rule has a linear consequent:

\[
\text{If }x\text{ is }A\text{ then }z=a_rx+b_r.
\]

For firing strengths \(\alpha_r\) and rule functions \(f_r(x)\),

\[
z_{\text{out}}=
\frac{\sum_r\alpha_rf_r(x)}
{\sum_r\alpha_r}.
\]

If all \(\alpha_r=0\), the implementation must use a declared fallback output rather than divide by zero.

### 8. Singleton consequents

A singleton consequent is

\[
B_r=\{z_r,1\}.
\]

With min implication,

\[
B_r'=\{z_r,\alpha_r\}.
\]

The aggregate can be represented as a weighted discrete distribution. Exact centroid defuzzification becomes

\[
z_{\text{out}}=\frac{\sum_r\alpha_rz_r}{\sum_r\alpha_r}.
\]

This resembles the zero-order Sugeno output, but the interpretation of the intermediate values is different.

### 9. Weighted output and certainty

Rule weights can represent confidence, frequency, importance, or cost. They should not automatically be interpreted as probabilities. If weights are learned from data, the training objective must define what they mean.

An unweighted rule has \(w_r=1\). A disabled rule can be represented by \(w_r=0\) or removed. A duplicated rule with a high weight may dominate aggregation.

### 10. Rule types

1. **Mamdani rules:** fuzzy antecedent and fuzzy consequent.
2. **Takagi–Sugeno rules:** fuzzy antecedent and crisp function consequent.
3. **Singleton rules:** fuzzy antecedent and one crisp output.
4. **Fuzzy–neuro hybrid rules:** a neural network predicts or adapts membership functions, rule weights, or rule parameters.
5. **Rule ensembles:** several submodels vote or average; correlation and double counting must be managed.

### 11. Rule representation as a relation

A single-input, single-output implication can be stored as a two-dimensional matrix

\[
R(a,b),
\]

where rows are antecedent truth grades and columns are consequent truth grades. For a Mamdani relation,

\[
R(a,b)=\min(a,b).
\]

For a 0.1-spaced set of grades, this produces a matrix with \(\min(a,b)\) entries. A fuzzy input vector \(A'\) can be composed with \(R\) using max–min composition to obtain a consequence vector.

This relational view generalizes to a finite rule base, but direct rule evaluation is usually faster and clearer in a controller.

### 12. Rule-base organization

Rules may be grouped by:

- output variable;
- operating region;
- control mode;
- decision outcome;
- priority or exception.

A conflict occurs when two rules recommend incompatible actions at the same state. Design options include different rule weights, priorities, a decision layer, a more specific rule, or separate sub-systems.

### 13. Rule generation

Rules may come from:

1. expert elicitation;
2. observation of operator decisions;
3. decision-tree or data-mining induction;
4. clustering of input-output data;
5. optimization of membership functions and weights.

Induced rules must be checked for coverage, redundancy, and plausibility. A statistically frequent rule may contradict expert safety knowledge and therefore should not be adopted automatically.

### 14. Rule validation

Test rules under:

- normal conditions;
- each fuzzy term at 0, 0.5, and 1;
- overlapping terms;
- extreme and boundary inputs;
- missing or noisy inputs;
- combinations that may produce conflict.

Useful diagnostics are firing-strength maps, output surfaces, rule coverage, and sensitivity of the final output to each rule weight.

## Worked examples

### Example 1: Two-rule Mamdani inference

Let “LOW” be triangular \((0,10,20)\) and “HIGH” be triangular \((20,30,40)\). “LOW” consequent is singleton 10 and “HIGH” consequent is singleton 30. At 25:

\[
\mu_{\text{LOW}}(25)=\frac{20-25}{10}=0,
\]

\[
\mu_{\text{HIGH}}(25)=\frac{25-20}{10}=0.5.
\]

Rules:

- If temperature is LOW then output = 10;
- If temperature is HIGH then output = 30.

Weights are 1. The firing strengths are \((0,0.5)\), and weighted-average defuzzification gives

\[
z_{\text{out}}=\frac{0(10)+0.5(30)}{0+0.5}=30.
\]

Mamdani aggregation with max also gives highest support at 30. A centroid on the continuous triangular consequents could differ.

### Example 2: Multiple antecedent product t-norm

For rule “If load is HIGH and vibration is MEDIUM then speed is LOW,” suppose

\[
\mu_{\text{HIGH}}(\text{load})=0.8,
\]

\[
\mu_{\text{MEDIUM}}(\text{vibration})=0.6,
\]

and \(w=0.9\). With product AND,

\[
\alpha=0.9(0.8\times0.6)=0.432.
\]

With min AND,

\[
\alpha=0.9\min(0.8,0.6)=0.54.
\]

The selected t-norm changes the rule's effect.

### Example 3: Max versus bounded-sum aggregation

Let two rules produce clipped output memberships

\[
C_1'=[0.4,0.6,0.2],\qquad
C_2'=[0.5,0.2,0.3].
\]

Max aggregation:

\[
C'=\max(C_1',C_2')=[0.5,0.6,0.3].
\]

Bounded sum:

\[
C'=\min(1,C_1'+C_2')=[0.9,0.8,0.5].
\]

Bounded sum allows combined rule evidence to raise the peak.

### Example 4: Takagi–Sugeno weighted average

Three rules fire with strengths \((0.2,0.5,0.1)\) and constant consequents \((10,20,40)\). Then

\[
z_{\text{out}}=
\frac{0.2(10)+0.5(20)+0.1(40)}
{0.2+0.5+0.1}
=\frac{2+10+4}{0.8}=20.
\]

If the sum of strengths is zero, a default action must be specified.

### Example 5: Product scaling versus clipping

With firing strength 0.4 and consequent memberships \((0.8,0.5,0.2)\):

- min implication gives \((0.4,0.4,0.2)\);
- product gives \((0.32,0.20,0.08)\).

Both preserve the consequent shape differently; product scales the whole set.

### Example 6: Relational rule

For antecedent grade \(a=0.6\) and min relation, the row is

\[
R(0.6,b)=\min(0.6,b).
\]

At \(b=0.3\), the relation value is 0.3; at \(b=0.8\), it is 0.6. This is exactly the clipping behavior of Mamdani min implication.

## Key terms & formulas

- **Antecedent:** IF part
- **Consequent:** THEN part
- **Firing strength:** Degree to which a rule matches current input
- **Implication:** Combines firing strength with the consequent
- **Aggregation:** Combines outputs from all rules
- **Mamdani:** Fuzzy-to-fuzzy inference
- **Takagi–Sugeno:** Fuzzy-to-crisp-function inference
- **Singleton:** A consequent with membership 1 at one value

Firing strength:

\[
\alpha_r=w_rT(a_{r1},\ldots,a_{rm}).
\]

Mamdani min:

\[
\mu_{B_r'}(z)=\min(\alpha_r,\mu_{B_r}(z)).
\]

Product:

\[
\mu_{B_r'}(z)=\alpha_r\mu_{B_r}(z).
\]

Aggregation:

\[
\mu_{B'}(z)=\max_r\mu_{B_r'}(z).
\]

Sugeno average:

\[
z=\frac{\sum_r\alpha_rf_r(x)}{\sum_r\alpha_r}.
\]

## Common mistakes

1. **Omitting the rule weight from firing strength.** If weights are used, include them consistently.
2. **Using max for AND.** A conjunction needs a t-norm such as min or product.
3. **Applying implication but forgetting aggregation.** Every active rule must reach one final output.
4. **Conflating weighted average with a probability estimate.** Sugeno weights normalize rule activity, not necessarily chance.
5. **Dividing by zero when all rules have zero strength.** A fallback rule or default output is required.
6. **Using max aggregation and then calling the result an accumulated probability.** Max is a fuzzy aggregator, not probability addition.
7. **Assuming rule weight is the same as antecedent membership.** They represent different sources of support.
8. **Ignoring conflicts between strongly fired rules.** Test and resolve incompatible recommendations.
9. **Dropping a rule base into software without recording operators.** The exact configuration must be documented.

## Exam prep

### Likely 2-mark questions

- **What is a fuzzy inference rule?**  
  **Hint:** An IF–THEN relation whose antecedent and/or consequent are fuzzy and that can fire partially.

- **Write the standard firing-strength formula.**  
  **Hint:** \(w_r\) times a t-norm of antecedent memberships.

- **State Mamdani min implication.**  
  **Hint:** \(\min(\alpha_r,\mu_{B_r}(z))\).

- **Write the standard max aggregation.**  
  **Hint:** Maximum of all rule outputs at each \(z\).

- **What is the output of a zero-order Sugeno system?**  
  **Hint:** Weighted average of constant rule consequents.

### Likely long-answer questions

- **Explain the complete evaluation of a Mamdani fuzzy rule.**  
  **Hint:** Fuzzification, t-norm, weight, clipping, aggregation, and defuzzification.

- **Compare Mamdani and Takagi–Sugeno inference rules.**  
  **Hint:** Consequent type, shape, output formula, interpretability, and training.

- **Explain t-norm, implication, and aggregation choices in a fuzzy rule base.**  
  **Hint:** min/product/Łukasiewicz, min/product implication, max/bounded sum; include a numerical comparison.

- **Design a rule base for one engineering application.**  
  **Hint:** Inputs, terms, rules, weights, possible conflicts, output, and validation cases.

- **Explain rule weights, rule generation, and conflict handling.**  
  **Hint:** Expert/inductive sources, interpretation of weights, specificity, priorities, and safety review.
