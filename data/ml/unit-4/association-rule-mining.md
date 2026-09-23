---
subject: ml
unit: 4
topic: association-rule-mining
syllabus_ref: CSM3201 Unit-IV
status: draft
---
# Association Rule Mining

## Overview

Association-rule mining finds sets of items or events that occur together frequently in a transaction or event database. A rule has an antecedent (if-part) and a consequent (then-part), for example bread \(\rightarrow\) butter. Rules are used in market-basket analysis, recommendation, inventory, web navigation, clinical event studies, and process mining.

The method is unsupervised in the sense that it does not require a target label. However, a frequent pattern is not automatically useful or causal. Support, confidence, and lift quantify observed co-occurrence, while minimum thresholds determine which rules are reported.

## Explanation

### Transactions and items

Let \(I=\{i_1,\ldots,i_m\}\) be the item universe and \(D=\{T_1,\ldots,T_n\}\) a database of transactions. A transaction \(T_j\subseteq I\) contains the items bought or events occurring together. Items can be products, pages, symptoms, drugs, or sequence positions. The transaction boundary and time window must be defined because they change the rules.

For an item set \(A\subseteq I\):

\[
\operatorname{support}(A)=\frac{\#\{T_j:A\subseteq T_j\}}{n}.
\]

A rule \(A\rightarrow B\) has:

\[
\operatorname{confidence}(A\rightarrow B)
=\frac{\operatorname{support}(A\cup B)}
{\operatorname{support}(A)},
\]

the proportion of transactions containing \(A\) that also contain \(B\).

**Lift** compares observed joint frequency with independence:

\[
\operatorname{lift}(A\rightarrow B)
=\frac{\operatorname{support}(A\cup B)}
{\operatorname{support}(A)\operatorname{support}(B)}.
\]

Lift greater than 1 indicates positive association; 1 suggests independence in the sample; less than 1 suggests negative association. Lift can be inflated by rare items, so support, confidence, lift, and a significance/robustness check should be reported together.

### Association versus sequence

An association says items co-occur. A sequential rule adds order, such as \(A\rightarrow B\rightarrow C\). Sequence analysis uses time/order constraints and is useful for process and web analysis. It is not the same as an unordered market-basket rule.

### Apriori algorithm

Apriori exploits the fact that if an item set is infrequent, all of its supersets are also infrequent. It proceeds in levels:

1. Find all frequent one-item sets at support \(\geq s_{\min}\).
2. Generate candidate \(k\)-item sets by joining frequent \((k-1)\)-sets.
3. Count candidate support in the transaction database.
4. Keep frequent \(k\)-sets and repeat.

The apriori property prunes candidates. The number of frequent sets can still be large, so minimum support, maximum itemset length, and transaction representation matter.

### FP-growth

FP-growth encodes transactions into a frequent-pattern tree. It finds frequent patterns without repeatedly scanning the full database, often faster and memory-efficient for dense data. Conditional-tree branches and support counting are more involved than a basic examination answer but can be described as an efficient alternative to apriori.

### Eclat

Eclat uses vertical data representation: for each item, record the transaction IDs containing it. Frequent sets are found by intersecting transaction-ID sets:

\[
T(A\cup B)=T(A)\cap T(B).
\]

Its efficiency depends on the size of these sets and the number of frequent patterns.

### Rule generation and interestingness

From every frequent set \(L=A\cup B\), consider \(A\rightarrow B\) where \(A,B\neq\emptyset\). Confidence and lift filter rules. Other measures include conviction, leverage, and statistical significance. High-confidence rules can be obvious or commercially useless; a common item may have high confidence simply because it is popular.

### Example: market baskets

Let there be 1,000 transactions. Bread appears in 600, butter in 400, and both in 300. Then

\[
\operatorname{support}(\text{bread})=0.6,\quad
\operatorname{support}(\text{butter})=0.4,
\]

\[
\operatorname{support}(\{\text{bread,butter}\})=0.3,
\]

\[
\operatorname{confidence}(\text{bread}\rightarrow\text{butter})=300/600=0.5,
\]

\[
\operatorname{lift}=\frac{0.3}{0.6\cdot0.4}=1.25.
\]

Bread and butter occur together more often than independence would predict, but this does not prove that buying bread causes buying butter.

### Evaluation and interpretation

Association rules have no single accuracy metric. Evaluate through:

- support and rule coverage;
- confidence, lift, leverage, or significance;
- stability across time periods, stores, and samples;
- novelty and redundancy of rules;
- business or domain plausibility;
- controlled experiments when a causal/action claim is intended.

A rule can be frequent because of a seasonal campaign. Splitting by time and examining conditional support helps identify such context. A recommendation should be tested rather than assumed to cause sales.

### Privacy and misuse

Basket data can reveal sensitive health, religion, or lifestyle information. Association with rare items may identify individuals. Apply access controls, minimum support thresholds, privacy review, purpose limitation, and aggregation. Do not use a rule to infer a protected characteristic without a lawful basis and ethical justification.

### Rule quality and actionable interpretation

A rule set can be large even when only a few rules are useful. Rank and filter by support, confidence, lift, leverage, novelty, and expected volume. Remove redundant rules that state nearly the same relation at different thresholds. Check each high-value rule across time periods, stores, customer segments, and alternative item groupings. A rule that appears only during one festival may be seasonal rather than stable.

The transaction database should be documented: what counts as a basket, whether returns and cancelled orders are removed, how missing items are treated, and whether a person or household is the customer. A small change in these definitions can change both support and confidence. For recommendations, test the rule in a controlled experiment or an online A/B test. A high-confidence association can still be caused by a common factor, such as a promotion or a demographic context.

Privacy is part of rule quality. Rare combinations can identify a customer, and a basket of health or religious items can reveal sensitive information. Apply minimum-support and access controls, aggregate reports, suppress unnecessarily specific rules, and obtain a lawful purpose before using them.

## Worked examples

### Example 1: confidence and lift

Suppose printers appear in 500 of 1,000 baskets and ink cartridges in 400. Both appear in 300. Confidence of printer \(\rightarrow\) ink is \(300/500=0.60\). Lift is \(0.30/(0.50\cdot0.40)=1.5\). The pair is positively associated, but the rule may be driven by office type; stratifying by office category can change the result.

### Example 2: rare item

A rare imported tea appears in 10 baskets, and a gift set appears in 5. Confidence is 0.5, but support is only 0.005. Lift may be large, yet the expected business impact and privacy risk are different from a high-volume rule.

### Example 3: sequence

Users often view a product, then a review, then checkout. A sequential pattern can suggest an interface flow. An unordered rule saying product and review co-occur does not establish that the review page caused checkout.

### Example 4: intervention

A supermarket tests placing bread near butter in selected stores while comparing sales with control stores. Randomisation and time controls provide stronger evidence about an action than association alone. Other changes must be kept stable.

## Key terms & formulas

- **Association rule:** \(A\rightarrow B\), an item/event-set relationship.
- **Antecedent:** \(A\), the if-part.
- **Consequent:** \(B\), the then-part.
- **Support:** frequency of an item set in transactions.
- **Confidence:** \(P(B\mid A)\).
- **Lift:** \(\operatorname{support}(A\cup B)/(\operatorname{support}(A)\operatorname{support}(B))\).
- **Frequent itemset:** item set meeting minimum support.
- **Apriori:** level-wise frequent-pattern algorithm using anti-monotonic pruning.
- **FP-growth:** frequent-pattern tree method.
- **Eclat:** vertical-ID intersection method.
- **Association:** observed co-occurrence, not necessarily causation.
- **Sequential rule:** association that includes order/time.
- **Minimum support:** user-set threshold for retaining an item set.
- **Leverage:** difference between observed and expected joint support.

## Common mistakes

1. **Calling high confidence proof of causation.** Popular items can have high confidence by default.
2. **Ignoring support.** A rule based on five transactions may be unstable or sensitive.
3. **Using lift without considering rare items.** Lift can exaggerate a small count.
4. **Forgetting the transaction boundary.** Rules change with time windows and grouping.
5. **Confusing association and sequence.** Co-occurrence does not preserve order.
6. **Evaluating only one time period.** Seasonal and promotional context can create rules.
7. **Ignoring privacy.** Basket combinations may reveal sensitive information.

## Exam prep

### Likely 2-mark questions

- **Define support, confidence, and lift.** Give formulas and interpret each.
- **What is an association rule?** A rule stating that an item/event set tends to be followed or co-occur with another.
- **State the anti-monotonic property used by apriori.** Every superset of an infrequent itemset is infrequent.
- **Why is association not causation?** Co-occurrence does not establish an intervention or mechanism.

### Long-answer prompts

- **Explain association-rule mining.** Define transactions, support, confidence, lift, thresholds, and rule generation.
- **Describe the apriori algorithm.** Explain candidate generation, support counting, pruning, and complexity.
- **Compare apriori, FP-growth, and Eclat.** Discuss data representation, efficiency, and limitations.
- **How would you evaluate and use association rules?** Discuss stability, business value, experiments, seasonality, privacy, and misuse.
