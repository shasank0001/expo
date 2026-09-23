---
subject: dwdm
unit: 3
topic: pattern-evaluation-methods
syllabus_ref: CSM3101 Unit-III
status: draft
---
# Pattern Evaluation and Interestingness Measures

## Overview

Frequent-pattern mining can return millions of itemsets and rules. Passing support and confidence only says that a pattern is common; it does not say that the pattern is informative or reliable. Pattern evaluation ranks patterns using statistical, business, and sometimes coverage measures. The central question is whether the observed co-occurrence is stronger than expected by chance and whether the pattern is useful for a decision.

## Explanation

### 1. Support and confidence

Support is the joint frequency \(\operatorname{supp}(A\cup B)\). Confidence is

\[
\operatorname{conf}(A\rightarrow B)
=\frac{\operatorname{supp}(A\cup B)}{\operatorname{supp}(A)}.
\]

These are easy to calculate but can mislead. A consequent that is common in the whole database can produce high confidence even when the antecedent adds almost no information. They are also descriptive, not significance tests.

### 2. Lift

Lift compares the observed joint probability with the product of the marginal probabilities:

\[
\operatorname{lift}(A\rightarrow B)
=\frac{\operatorname{supp}(A\cup B)}
{\operatorname{supp}(A)\operatorname{supp}(B)}
=\frac{\operatorname{conf}(A\rightarrow B)}{\operatorname{supp}(B)}.
\]

- Lift \(=1\): the rule is consistent with independence.
- Lift \(>1\): positive association.
- Lift \(<1\): negative association.

Lift is symmetric in the sense that its value is the same for \(A\rightarrow B\) and \(B\rightarrow A\), although their confidences differ. A large lift can be unstable when support is small, so it must be read with support and sample size.

### 3. Leverage

Leverage is the absolute difference between observed joint probability and expected probability under independence:

\[
\operatorname{lev}(A\rightarrow B)
=\operatorname{supp}(A\cup B)
-\operatorname{supp}(A)\operatorname{supp}(B).
\]

Positive leverage means the items occur together more often than expected. Larger magnitude means a larger absolute departure. Like lift, leverage is symmetric and requires support to judge reliability.

### 4. Conviction

Conviction measures how strongly the rule contradicts the rule “if \(A\), then not \(B\).” A common definition is

\[
\operatorname{conv}(A\rightarrow B)
=\frac{1-\operatorname{supp}(B)}
{1-\operatorname{conf}(A\rightarrow B)}.
\]

Values below 1 indicate negative association; values above 1 quantify departure from independence. If confidence is 1 while \(B\) is not universally present, the denominator is zero and conviction is conventionally \(+\infty\): every transaction with \(A\) also has \(B\). Confidence 1 and \(B\) universal make the expression \(0/0\), so it should not be assigned a useful finite value.

### 5. Statistical significance

For a 2-by-2 contingency table of A and B, the **chi-square statistic** compares observed and expected counts. The expected count under independence is

\[
E_{ij}=\frac{\text{row total}_i\text{column total}_j}{N}.
\]

The statistic is

\[
\chi^2=\sum_{i,j}\frac{(O_{ij}-E_{ij})^2}{E_{ij}},
\]

usually compared with a chi-square distribution (for large samples, with an appropriate continuity correction). The G-test uses \(2\sum O\ln(O/E)\) and is asymptotically related. A low p-value provides evidence against independence under the model assumptions, but does not measure business value or prove causation. Very large samples can make trivial effects statistically significant, so effect size should be reported too.

### 6. Objective versus subjective interestingness

An **objective measure** depends only on database counts, such as support, confidence, lift, or leverage. A **subjective measure** also uses user expectations, costs, or domain knowledge. A retailer may value a rule with lower confidence if it applies to a high-value customer segment. A medical rule may be judged unacceptable because its false-negative cost is high even if its statistics are strong.

### 7. Evaluation workflow

1. Filter by minimum support and confidence.
2. Remove vacuous rules whose consequents explain them.
3. Compute lift, leverage, conviction, and significance.
4. Check coverage and redundancy; retain shorter rules when specificity adds no information.
5. Inspect unusual or negative rules, if the task permits them.
6. Validate on held-out data, time-separated data, or a domain experiment.
7. Apply cost and fairness constraints before deployment.

## Worked examples

### Example 1: A high-confidence weak rule

There are 10,000 transactions:

- A: 2,000
- B: 6,000
- A and B: 1,600

Then

\[
\operatorname{conf}(A\rightarrow B)=1600/2000=0.80,
\]
\[
\operatorname{lift}=0.16/(0.20\cdot0.60)=1.333,
\]
\[
\operatorname{lev}=0.16-0.12=0.04.
\]

Confidence is 80%, but B already occurs in 60% of all transactions. A raises the probability to 80%, a 20-point increase; the absolute effect is visible in leverage. Significance may be strong because the sample is large, but the action should depend on the value of the 20-point change.

### Example 2: Negative association and conviction

A occurs in 300 transactions, B in 600, and A with B in 120, out of 1,000.

\[
\operatorname{conf}(A\rightarrow B)=0.40,
\quad \operatorname{lift}=0.12/(0.30\cdot0.60)=0.667,
\]
\[
\operatorname{lev}=0.12-0.18=-0.06,
\]
\[
\operatorname{conv}=\frac{0.40}{0.60}=0.667.
\]

Lift, leverage, and conviction all indicate negative association. The direction is not causal and may reflect confounding, eligibility rules, or a deliberate substitution between products.

### Example 3: Chi-square calculation

Suppose 100 transactions give the following 2-by-2 table:

| | B | not B | total |
|---|---:|---:|---:|
| A | 40 | 20 | 60 |
| not A | 20 | 20 | 40 |
| total | 60 | 40 | 100 |

Under independence, the expected counts are

\[
E_{AB}=60(60)/100=36,\quad E_{A\bar B}=60(40)/100=24,
\]
\[
E_{\bar A B}=40(60)/100=24,\quad E_{\bar A\bar B}=40(40)/100=16.
\]

Thus

\[
\chi^2=\frac{(40-36)^2}{36}+\frac{(20-24)^2}{24}
+\frac{(20-24)^2}{24}+\frac{(20-16)^2}{16}
\approx2.78.
\]

With one degree of freedom, this is not conventionally significant at the 0.05 level. The observed lift is \(0.40/(0.60\cdot0.60)=1.11\), a weak positive association. Always check that all cells and margins are valid before computing significance.

### Example 4: Symmetric measures

For the first example, lift and leverage are the same in both directions:

\[
\operatorname{lift}(B\rightarrow A)=1.333,
\quad \operatorname{lev}(B\rightarrow A)=0.04.
\]

Confidence is 80% for \(A\rightarrow B\) but only \(1600/6000=26.67\%\) for \(B\rightarrow A\). This is why lift/leverage are called correlation measures, not directional prediction measures.

## Key terms & formulas

- **Support:** \(\operatorname{supp}(A\cup B)\).
- **Confidence:** \(\operatorname{conf}(A\rightarrow B)=\operatorname{supp}(A\cup B)/\operatorname{supp}(A)\).
- **Lift:** \( \operatorname{supp}(A\cup B)/[\operatorname{supp}(A)\operatorname{supp}(B)]\).
- **Leverage:** \( \operatorname{supp}(A\cup B)-\operatorname{supp}(A)\operatorname{supp}(B)\).
- **Conviction:** \((1-\operatorname{supp}(B))/(1-\operatorname{conf})\).
- **Expected count:** \(E_{ij}=\text{row total}_i\text{column total}_j/N\).
- **Chi-square:** \(\sum (O-E)^2/E\).
- **Vacuous rule:** high confidence explained by a globally frequent consequent.
- **Objective interestingness:** count-based measure.
- **Subjective interestingness:** user/domain-dependent measure.
- **Statistical significance:** evidence against a null model, not effect importance or causation.

## Common mistakes

1. **Using lift as confidence:** lift compares with independence; confidence conditions on the antecedent.
2. **Ignoring support with a large lift:** a tiny co-occurrence count can produce unstable ratios.
3. **Interpreting lift below 1 as no association:** it indicates negative association under the model.
4. **Treating a small p-value as proof or practical importance:** statistical and practical significance differ.
5. **Confusing symmetric and directional measures:** lift and leverage are symmetric; confidence is not.
6. **Using conviction when the denominator is zero:** handle the perfect-rule case explicitly.
7. **Applying formulas to invalid contingency tables:** counts must be consistent and nonnegative.

## Exam prep

**Likely 2-mark questions**
1. Define lift and state its interpretation. *Hint: observed joint probability divided by the independent expectation.*
2. Define leverage. *Hint: observed minus expected joint probability.*
3. Why can a high-confidence rule be uninteresting? *Hint: the consequent is globally common.*

**Likely long-answer questions**
1. Compare support, confidence, lift, leverage, and conviction with a numeric table. *Hint: show formulas, direction, symmetry, and zero cases.*
2. Explain the difference between statistical significance and subjective interestingness. *Hint: p-values versus effect size, cost, coverage, and domain use.*
3. Design an evaluation pipeline for a large set of association rules. *Hint: threshold, correlation, significance, redundancy, stability, deployment validation.*
