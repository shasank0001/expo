---
subject: dwdm
unit: 3
topic: association-rule-generation
syllabus_ref: CSM3101 Unit-III
status: draft
---
# Association Rule Generation

## Overview

Frequent-itemset mining finds sets that occur often. Association-rule generation turns those sets into implications such as “if a customer buys tea, they often buy biscuits.” Every nontrivial subset of a frequent itemset can be an antecedent or consequent, but the resulting rules differ greatly in confidence and usefulness. This topic explains generation, calculation, pruning, and interpretation.

## Explanation

### 1. Rules from one itemset

Let \(X\) be a frequent itemset of size \(k\). Choosing a nonempty subset \(A\subset X\) gives the rule

\[
A\rightarrow X-A.
\]

Subtract the itemset \(A\), not a set difference of occurrences. Rules in which \(A=X\), or \(A=\varnothing\), are excluded. Because both directions can be formed, an \(k\)-itemset yields

\[
2^k-2
\]

nontrivial, distinct rules. The set \(A\) is the **antecedent** or body; \(X-A\) is the **consequent** or head.

A frequent itemset guarantees a minimum joint support, but it does not guarantee the same confidence in every direction.

### 2. Confidence

For a rule \(A\rightarrow B\),

\[
\operatorname{conf}(A\rightarrow B)
=P(B\mid A)
=\frac{\operatorname{supp}(A\cup B)}{\operatorname{supp}(A)}.
\]

Confidence is the proportion of transactions containing \(A\) that also contain \(B\). A rule satisfies **minimum confidence** \(\operatorname{minconf}\) when this value reaches the threshold. A rule can never be generated from an infrequent itemset because every such rule has support below \(s_{\min}\). Some implementations also apply a user-specified **minimum support** to the rule; this is already guaranteed when it inherits the itemset's threshold.

### 3. Example-generation methods

1. For each frequent \(k\)-itemset \(X\), generate \(A\rightarrow X-A\) for every nonempty proper subset \(A\) of \(X\).
2. Compute support for \(A\), \(B\), and \(A\cup B\), then calculate confidence.
3. Retain rules reaching `minconf`.
4. Rank remaining rules using lift, leverage, conviction, or another objective-interest measure.

An equivalent method considers all one-item antecedents and then all two-item antecedents, and so on. The subset method is simpler when \(X\) is modest in size, but the number of rules can be enormous for large itemsets.

### 4. Rule quality is not just confidence

If milk is bought in 90% of all transactions, then milk has very high probability as a consequent. A rule such as `diapers -> milk` can have 95% confidence simply because almost everything co-occurs with milk. Lift checks whether the joint occurrence exceeds what independence would predict:

\[
\operatorname{lift}(A\rightarrow B)=
\frac{\operatorname{supp}(A\cup B)}
{\operatorname{supp}(A)\operatorname{supp}(B)}.
\]

The formal meaning and other measures are in the pattern-evaluation file. Use them to remove high-confidence but uninformative rules.

### 5. Redundancy and actionability

Many rules can express nearly the same behavior. For example, `A -> B`, `A -> B,C`, and `A -> C` may have identical lift. Redundancy analysis keeps a shorter rule when removing a consequent does not reduce lift. Actionability is a business judgment: shelf placement can directly use a pair rule, but a rule with hundreds of items may be impossible to deploy. Statistical significance and holdout validation are also needed for a stable claim.

### 6. Association by logical implication

The generated rule describes a co-occurrence implication in the observed database. It does not state a universal logical implication in the mathematical sense: the presence of \(A\) is not guaranteed to force \(B\), because only a fraction \(P(B\mid A)\) of the time does \(B\) appear. It can also be read as a probabilistic association.

## Worked examples

### Example 1: Generate all complement rules from \(\{A,B,C\}\)

For \(k=3\), generate \(2^3-2=6\) rules:

\[
A\rightarrow\{B,C\},\quad
B\rightarrow\{A,C\},\quad
C\rightarrow\{A,B\},
\]
\[
\{A,B\}\rightarrow C,\quad
\{A,C\}\rightarrow B,\quad
\{B,C\}\rightarrow A.
\]

A consequent may contain several items; `A -> B,C` means that **B and C occur jointly**. Rules with one item on each side, such as `A -> B`, can also be generated, but restricting the task to single-item consequents is a different rule family and does not use the standard \(2^k-2\) complement enumeration.

### Example 2: Calculate both directions

There are 1,000 transactions:

| Count | Meaning |
|---:|---|
| 400 | contain A |
| 500 | contain B |
| 300 | contain both A and B |

Using itemset \(\{A,B\}\):

\[
\operatorname{supp}(A)=0.40,\quad
\operatorname{supp}(B)=0.50,\quad
\operatorname{supp}(A\cup B)=0.30.
\]

For \(A\rightarrow B\):

\[
\operatorname{conf}=0.30/0.40=0.75.
\]

For \(B\rightarrow A\):

\[
\operatorname{conf}=0.30/0.50=0.60.
\]

At `minconf = 0.70`, keep only \(A\rightarrow B\). The same itemset and support threshold support both directions, but their confidence differs.

### Example 3: Explain misleading confidence

Bread appears in 80% of baskets. Butter appears in 75%. Both appear in 62%. Then

\[
\operatorname{conf}(\text{bread}\rightarrow\text{butter})=0.62/0.80=0.775,
\]

but

\[
\operatorname{lift}=\frac{0.62}{0.80(0.75)}
=\frac{0.62}{0.60}=1.033.
\]

The 77.5% conditional probability sounds high, yet purchasing bread changes butter probability from 75% to 77.5% only slightly. A 1.033 lift is weak.

### Example 4: Rule count

If mining returns 100 frequent 2-itemsets and 20 frequent 3-itemsets, and no larger itemsets exist, the number of generated nontrivial rules is

\[
100(2^2-2)+20(2^3-2)=100(2)+20(6)=320.
\]

This shows why frequent itemsets can exist even when rule presentation is unwieldy.

## Key terms & formulas

- **Antecedent/body \(A\):** the `if` side.
- **Consequent/head \(B\):** the `then` side.
- **Joint itemset \(A\cup B\):** all items required by both sides.
- **Rule support:** \(\operatorname{supp}(A\cup B)\).
- **Confidence:** \(P(B\mid A)\).
- **Minimum confidence:** lowest acceptable conditional probability.
- **Rule count from a \(k\)-itemset:** \(2^k-2\).
- **Lift:** \( \operatorname{conf}(A\rightarrow B)/[P(B)] \).
- **Redundant rule:** a longer or more specific rule with no added lift.
- **Vacuous rule:** a rule for which the consequents' frequencies already explain the association.

## Common mistakes

1. **Using only the antecedent count:** confidence uses the joint count, not the consequent's global frequency.
2. **Assuming all directions have equal confidence:** denominators differ.
3. **Forgetting two trivial rules:** empty antecedent and empty consequent are normally excluded.
4. **Reporting support as confidence:** support divides by all transactions; confidence divides by transactions containing \(A\).
5. **Treating a threshold as a discovery:** generated rules may be statistically unreliable and must be ranked and validated.
6. **Interpreting a rule as causal:** association alone does not establish causation.

## Exam prep

**Likely 2-mark questions**
1. Define antecedent, consequent, support, and confidence of a rule. *Hint: if-side, then-side, joint frequency, conditional frequency.*
2. How many nontrivial rules can be generated from a \(k\)-itemset? *Hint: \(2^k-2\).*
3. Why can association rules only be generated from frequent itemsets? *Hint: a rule's support is the joint itemset support.*

**Likely long-answer questions**
1. Generate and evaluate all rules from a supplied frequent itemset. *Hint: list subsets, count joint occurrences, divide by antecedent support, then compute lift.*
2. Explain why high confidence does not imply a strong association and demonstrate with a numeric example. *Hint: common frequent consequent.*
3. Describe a practical pipeline for turning many generated rules into a useful short list. *Hint: minimum confidence, significance/correlation, redundancy, external validation.*
