---
subject: dwdm
unit: 4
topic: rule-based-classification
syllabus_ref: CSM3101 Unit-IV
status: draft
---
# Rule-Based Classification

## Overview

Rule-based classification represents knowledge as IF–THEN rules. The IF part, or antecedent, tests attributes; the THEN part assigns a class or a probability. Rules are readable, can encode domain expertise, and can be learned from labeled examples. A good rule set must cover many cases without making too many errors, and it must be tested on unseen data.

## Explanation

### 1. Rule form

A classification rule has the form

\[
\text{IF }A\text{ THEN class }C,
\]

where \(A\) is a conjunction of tests, for example:

```text
IF age >= 18 AND income < 30000 AND debt_ratio < 0.4
THEN approve.
```

A rule's **coverage** is the fraction of all training examples satisfying its antecedent. Its **accuracy** or **confidence** is the fraction of covered examples with the stated class:

\[
\operatorname{accuracy}(R)=\frac{\text{covered examples of class }C}
{\text{all covered examples}}.
\]

A rule that covers 40 examples and predicts the correct class for 36 has 90% rule accuracy. Low coverage can make an apparently perfect rule useless; low accuracy damages trust.

### 2. Covering algorithms

A greedy covering method starts with no rules and repeatedly selects a rule that covers many currently uncovered examples. **AQ** uses refinement searches and dominance pruning. **FOIL** grows rules by repeatedly adding literals that improve information gain in the class distribution. **RIPPER** uses ordered rule covering, post-pruning, and rule optimization. **CN2** adapts a separate-and-conquer method inspired by AQ.

A separate-and-conquer method learns one rule, removes the examples it covers, and repeats. It is efficient for disjoint rules but may miss cases that are easy only when combined with a broader rule. Some systems use a decision-list order, so an earlier rule can take precedence.

### 3. Literal and rule quality

A literal is one test, such as `income < 50000`. A longer rule can have high accuracy but low coverage. Candidate quality balances positive coverage, negative coverage, and simplicity. In FOIL, a useful information-gain-style gain compares the rule's class entropy before and after adding a literal. Redundant or contradictory rules should be removed.

A **default rule** assigns a class when no specific rule applies. If the majority class is \(C\), the default is `IF true THEN C`. It is necessary for complete coverage, but its use can be reported separately because a high overall accuracy may be mostly the default rule.

### 4. Rule refinement and pruning

Rules can be too general and classify many examples incorrectly, or too specific and cover only a few cases. **Generalization** broadens a rule when that improves its use; **specialization** adds a condition. Pruning deletes a rule or part of a rule when estimated error on validation data does not improve by keeping it. A post-pruning pass can use optimistic estimates followed by validation estimates.

Redundancy analysis removes a rule if another rule covers the same examples with equal or better accuracy. Duplicate rules must be identified before evaluating rule count.

### 5. Classification with a rule set

Given a new object, evaluate rules. If several match, the system can use the first match in a decision list, highest rule accuracy, highest estimated class probability, or a voting scheme. These policies can produce different predictions, so the evaluation must state the policy.

A rule set can also be expressed as a disjunctive normal form:

\[
(A_1\land A_2)\lor(B_1\land B_2\land B_3)\lor\cdots.
\]

### 6. Advantages and limitations

Rules are interpretable, can use domain constraints, and can be updated by experts. They may be brittle to missing values, can be long, and can become contradictory. Greedy covering does not guarantee the globally best rule set. Accuracy on training data can be high even when validation coverage is poor. Rule learning is related to decision trees, but a tree is a compact structured partition; a rule set need not be a tree.

## Worked examples

### Example 1: Coverage and rule accuracy

There are 200 training cases. A rule covers 50, of which 45 have class `yes`.

\[
\operatorname{coverage}=50/200=25\%,
\quad \operatorname{rule\ accuracy}=45/50=90\%.
\]

A second rule covers only 2 cases and is 100% accurate. It has lower coverage and should not automatically be preferred. A third rule covers 60 cases but is 70% accurate may be useful for a different class only if errors are tolerable.

### Example 2: Two rules and a default

```text
R1: IF age >= 18 THEN yes, coverage 70%, accuracy 80%.
R2: IF income > 50000 THEN yes, coverage 25%, accuracy 95%.
Default: yes.
```

Suppose a new object satisfies both R1 and R2. A first-match policy returns R1; a highest-accuracy policy returns R2. A voting policy could count both and return yes. The rules are not contradictory, but the combination policy is still a required design choice.

### Example 3: FOIL-style literal addition

A broad rule covers 100 cases: 50 yes and 50 no, entropy 1 bit. Add `income < 30000`; its covered subset has 45 yes and 5 no, entropy

\[
H=-[0.9\log_2 0.9+0.1\log_2 0.1]=0.469.
\]

The added literal improves purity. A different literal that covers 60 cases with 30 yes and 30 no does not improve it. A greedy learner may prefer the first literal even if a different combination has a better eventual rule.

### Example 4: Pruning

A rule covers 20 cases with 19 correct on training data but only 12 correct on validation data. Keeping it increases validation errors and provides little unique coverage, so post-pruning may delete it. A high training accuracy alone is not evidence that the rule should remain.

## Key terms & formulas

- **Antecedent/IF part:** conjunction of attribute tests.
- **Consequent/THEN part:** predicted class.
- **Literal:** one attribute-value test.
- **Coverage:** \(\#\text{matching examples}/|D|\).
- **Rule accuracy:** correct covered examples / all covered examples.
- **Generalization:** remove or broaden tests.
- **Specialization:** add tests.
- **Decision list:** ordered rules where an earlier match can win.
- **Default rule:** fallback class when no specific rule matches.
- **Redundancy:** a rule adds no unique or better-covered behavior.

## Common mistakes

1. **Confusing rule coverage with rule accuracy:** they have different denominators.
2. **Ignoring uncovered cases:** a rule set without a default is incomplete.
3. **Counting a matching rule twice without stating the policy:** specify first-match, priority, or voting.
4. **Keeping every high-accuracy tiny rule:** coverage and validation matter.
5. **Assuming greedy covering is globally optimal:** it is a heuristic search.
6. **Treating rule accuracy as model accuracy:** evaluate the complete classifier on held-out cases.

## Exam prep

**Likely 2-mark questions**
1. Define a classification rule and its coverage. *Hint: IF–THEN and fraction of all cases matching.*
2. What is rule accuracy? *Hint: correct covered cases divided by all covered cases.*
3. What does post-pruning do? *Hint: removes unnecessary rules or tests using estimated error.*

**Likely long-answer questions**
1. Explain sequential covering algorithms such as AQ, FOIL, and RIPPER. *Hint: select a rule, cover/remove cases, repeat, then prune.*
2. Construct and evaluate a rule set on supplied data. *Hint: count coverage and accuracy, resolve overlaps, and state the default.*
3. Compare rule-based classification and decision trees. *Hint: readable rules versus structured partition; both can overfit and need validation.*
