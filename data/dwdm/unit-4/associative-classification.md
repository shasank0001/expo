---
subject: dwdm
unit: 4
topic: associative-classification
syllabus_ref: CSM3101 Unit-IV
status: draft
---
# Associative Classification

## Overview

Associative classification uses association rules discovered from the training data to predict a class. Frequent patterns provide candidate conditions; the class label attached to each pattern tells how strongly the condition predicts a target category. It combines ideas from association-rule mining and classification. The method is interpretable when rules are short, but it can produce too many patterns and may need pruning to avoid overfitting.

## Explanation

### 1. Relationship with association mining

A classifier is trained on labeled transactions, so each transaction contains attributes and a class label. Treat the class as a special item and mine patterns such as

\[
\{\text{income}=\text{low},\text{debt}=\text{high}\}\rightarrow\text{class}=\text{reject}.
\]

An **associative classifier** uses these rules to assign a class to a new object. It is related to rule-based classification, but the rules are initially discovered using frequent-pattern machinery such as Apriori or FP-growth rather than hand-written expert rules.

### 2. Rule quality for classification

For a rule \(A\rightarrow C\), useful measures include:

- **coverage:** fraction of all training objects satisfying \(A\);
- **confidence or accuracy:** fraction of covered objects with class \(C\);
- **lift:** \(P(C\mid A)/P(C)\);
- **leverage:** observed minus expected probability of \(A\) and \(C\);
- **class distribution counts:** absolute numbers of correct and incorrect covered cases.

A rule with 100% confidence on two examples is not necessarily useful. Coverage, support, validation error, and rule complexity must be considered.

### 3. Finding candidate rules

1. Add the class label to each transaction.
2. Mine frequent itemsets with the class as a distinguished item, or mine attribute patterns and retain their class distributions.
3. Generate `attributes -> class` rules.
4. Remove redundant or low-coverage rules.
5. Sort or combine rules for prediction.

Mining a single global minimum support can discard useful class-specific rules. A class-based approach may use different thresholds or a refinement method to find enough rules for every class.

### 4. Prediction

If a new object matches one rule, return its consequent. If several rules match:

- use the highest-confidence rule;
- use a priority or decision-list order;
- sum confidence evidence or lift;
- vote among class consequents;
- use a default majority class.

A weighted score can be formed from rule confidence and coverage. The exact score is a modeling choice and must be evaluated rather than assumed optimal.

### 5. Pruning and overfitting

Many highly specific rules can memorize training objects. Prune rules with low coverage, low estimated accuracy, redundant consequents, or poor validation performance. Generalization can replace a specific condition with a broader one if it preserves class information. Associative classifiers can be sensitive to minimum support and the choice of ranking policy.

### 6. Advantages and limitations

**Advantages:** rules are readable, support and confidence expose evidence, frequent-pattern algorithms are mature, and class-specific patterns can be found.

**Limitations:** many rules, difficult conflict resolution, redundant patterns, sensitivity to support, and potential poor performance when class labels interact with many attributes. Like any rule method, it can be less accurate than a tuned ensemble and still be valuable when explanation is a requirement.

## Worked examples

### Example 1: Class-association rules

Training data has 100 objects:

| Pattern | Total covered | Class A | Class B |
|---|---:|---:|---:|
| P | 40 | 36 | 4 |
| Q | 20 | 10 | 10 |
| R | 8 | 8 | 0 |

For P:

\[
\operatorname{coverage}(P)=0.40,\quad
\operatorname{accuracy}(P\rightarrow A)=36/40=0.90.
\]

If \(P(A)=0.50\), lift is \(0.90/0.50=1.80\). For R:

\[
\operatorname{coverage}=0.08,\quad
\operatorname{accuracy}=1.00,\quad
\operatorname{lift}=2.00.
\]

R has better accuracy and lift but covers only 8% of cases. A default rule or fallback is needed.

### Example 2: New object matches two rules

Suppose a new object matches P and Q. Highest-accuracy policy predicts A because P has 90% accuracy. Majority voting counts one vote for A and one for B, then uses the default or a weighted score. These policies can disagree, so evaluation must include all matching rules and the chosen combination rule.

### Example 3: Support and rule generation

If the class A occurs in 30 of 100 objects and a pattern P occurs in 36 of them, P is frequent for A with support 0.36. A global pattern P occurring in 40 objects may also be frequent, but its class distribution could be 20 A and 20 B. Mining the class as a distinguished item lets the system avoid a rule whose class-specific evidence is weak.

## Key terms & formulas

- **Associative classifier:** classifier based on discovered attribute-to-class association rules.
- **Coverage:** fraction of all training objects satisfying an antecedent.
- **Rule accuracy:** correct class among covered objects.
- **Class-specific support:** support of an attribute pattern within a class.
- **Rule ranking:** order rules by confidence, lift, coverage, or another score.
- **Default rule:** fallback majority class.
- **Rule pruning:** remove redundant, low-coverage, or unreliable rules.
- **Conflict:** multiple matching rules imply different classes.

## Common mistakes

1. **Treating 100% accuracy on a tiny rule as proof:** report coverage.
2. **Using a global threshold without considering class frequencies:** rare classes may be missed.
3. **Ignoring overlapping matches:** define the first-match, vote, or score policy.
4. **Forgetting a fallback/default class:** some objects may match no rule.
5. **Confusing association-rule support with classification accuracy:** support is joint frequency; accuracy conditions on covered cases.
6. **Overfitting with very specific rules:** prune and validate.

## Exam prep

**Likely 2-mark questions**
1. What is associative classification? *Hint: use discovered association rules to assign a class.*
2. Define rule coverage. *Hint: matching training objects divided by all training objects.*
3. Why are small rules filtered? *Hint: perfect accuracy with negligible coverage can be unreliable.*

**Likely long-answer questions**
1. Explain the training and prediction phases of an associative classifier. *Hint: class-augmented mining, rule generation, ranking, matching, default.*
2. Compare associative classification with rule-based classification and decision trees. *Hint: mining versus expert/greedy rules; shared interpretability.*
3. Derive precision, recall, and coverage for an associative rule set on supplied data. *Hint: count matching class and nonclass cases.*
