---
subject: dwdm
unit: 4
topic: decision-tree-induction
syllabus_ref: CSM3101 Unit-IV
status: draft
---
# Decision Tree Induction

## Overview

A decision tree classifies data by repeatedly asking test questions. Internal nodes contain attribute tests, branches represent outcomes, and leaves contain class predictions. Trees are attractive because a prediction can be followed and explained as rules such as “if income is low and age is below 30, then approve.” Their flexibility also makes them prone to overfitting, so growth, stopping, and pruning must be chosen carefully.

## Explanation

### 1. Tree structure

For classification:

- a **root node** begins the test sequence;
- an **internal node** tests an attribute;
- an edge or branch is one possible test result;
- a **leaf node** stores a predicted class;
- each training tuple has a known class.

A path from root to leaf is a conjunction of conditions. A pure node contains examples of one class and can become a leaf immediately.

### 2. Entropy

For a node \(S\) with class counts \(n_1,\ldots,n_K\) and total \(n\), the class probabilities are \(p_i=n_i/n\). Entropy is

\[
H(S)=-\sum_{i=1}^{K}p_i\log_2p_i.
\]

Entropy is 0 bits when all labels are identical and maximum \(\log_2K\) when labels are evenly distributed. It measures label impurity.

### 3. Information gain

For candidate attribute \(A\), split \(S\) into subsets \(S_v\) with proportion \(p_v=|S_v|/|S|\). Conditional entropy is

\[
H(S|A)=\sum_v\frac{|S_v|}{|S|}H(S_v).
\]

Information gain is

\[
\operatorname{Gain}(S,A)=H(S)-H(S|A).
\]

Choose the test with the largest gain. The idea is to remove the greatest uncertainty in class labels. Greedy tree induction chooses each node independently; it does not search every possible tree.

### 4. Gain ratio

ID3 uses gain and is biased toward attributes with many possible values because such attributes can create many small pure subsets. C4.5 uses **gain ratio**:

\[
\operatorname{GainRatio}(S,A)
=\frac{\operatorname{Gain}(S,A)}
{-\sum_v p_v\log_2p_v}.
\]

The denominator is the split information, or entropy of the partition. If it is zero, the ratio is not defined. Gain ratio favors balanced splits, though it can prefer a low-gain attribute with many branches; practical implementations impose limits.

### 5. Gini index

CART commonly uses the Gini impurity:

\[
\operatorname{Gini}(S)=1-\sum_i p_i^2.
\]

For split \(A\),

\[
\operatorname{GiniSplit}(S,A)
=\sum_v\frac{|S_v|}{|S|}\operatorname{Gini}(S_v).
\]

Choose the smallest weighted Gini. Binary and multiclass splits are both possible; the set of possible subsets is exponential for a multiclass nominal attribute, so implementations restrict or optimize candidate partitions.

### 6. Categorical and continuous attributes

A categorical attribute can produce one branch per value, or, in binary classification, subsets of values. For a continuous numeric attribute, sort the values and test thresholds between adjacent values. Many thresholds are possible, so binning, candidate selection, or an efficient scan is used. The split does not require equality to a particular value.

### 7. Missing values and incomplete data

A strategy must say whether a missing value follows a branch, is handled using other attributes, or causes the example to be excluded. Test choice can use only known values or use distributions estimated from known values. Treating missing as zero or “no” without justification is dangerous.

### 8. Stopping and pruning

A node becomes a leaf if it is pure, has too few examples, has no useful remaining attribute, or another stopping rule fires. Stopping early can underfit.

**Pre-pruning** stops growth early. **Post-pruning** grows a large tree and then removes subtrees. A subtree is considered for replacement by a leaf; if its estimated validation error does not increase, the simpler structure is retained. Cost-complexity pruning balances error and the number of leaves:

\[
R_\alpha(T)=R(T)+\alpha|\text{leaves}(T)|.
\]

Different tree algorithms use different validation and pruning details, but all control complexity.

### 9. Overfitting and underfitting

An overly large tree can create leaves that contain one training example, memorize noise, and fail on new cases. A tiny tree may miss real structure. Evaluate validation error over tree size and choose a complexity that generalizes. The final test set must not be used for every pruning decision.

### 10. Decision trees for regression

For a numeric target, leaves store mean or median target values. Squared error or variance reduction can select splits. A tree is still interpretable, but stepwise constant predictions may be too rough for smoothly varying targets.

## Worked examples

### Example 1: Entropy and a split

Node \(S\) contains 10 examples: 6 yes and 4 no.

\[
p_Y=0.6,\quad p_N=0.4,
\]
\[
H(S)=-[0.6\log_2 0.6+0.4\log_2 0.4]
=0.971\text{ bits}.
\]

Suppose feature A creates `A=yes` with 3 yes, 1 no and `A=no` with 3 yes, 3 no.

\[
H(\text{yes branch})=-[0.75\log_2 0.75+0.25\log_2 0.25]=0.811,
\]
\[
H(\text{no branch})=-[0.5\log_2 0.5+0.5\log_2 0.5]=1.
\]

Then

\[
H(S|A)=\frac48(0.811)+\frac48(1)=0.906,
\]
\[
\operatorname{Gain}=0.971-0.906=0.065\text{ bits}.
\]

The gain is small because the class ratio remains similar in both branches.

### Example 2: Complete tree induction

Training data:

| Person | Age | Income | Class |
|---|---:|---:|---|
| 1 | 22 | 20 | Y |
| 2 | 35 | 45 | N |
| 3 | 28 | 25 | Y |
| 4 | 45 | 50 | N |
| 5 | 31 | 20 | Y |
| 6 | 52 | 60 | N |
| 7 | 25 | 35 | Y |
| 8 | 40 | 45 | N |

At the root, \(H=1\) bit because there are four of each class. Testing `income <= 35` gives:

- low: four Y, zero N; entropy 0;
- high: zero Y, four N; entropy 0.

Weighted conditional entropy is 0, so information gain is 1 bit. The root leaf splits perfectly, and both children are pure. The tree predicts Y for income at most 35 and N otherwise. This tiny tree may not generalize: a new person with income 36 could belong to either class. Validation or domain knowledge is required.

### Example 3: Continuous threshold

A sorted age list is 22, 28, 31, 35, 40, 45, 52. With binary class Y/N, only thresholds that change the class composition need close examination in an efficient implementation. A valid threshold is 35, producing `age <= 35` and `age > 35`. Age 35 is included on the lower side by the stated inequality; the boundary convention must be consistent.

### Example 4: Gain ratio warning

If A has thousands of nearly unique values, it can isolate examples and have high information gain but low gain ratio. A balanced binary split of a small domain may have lower gain but a more stable ratio. The algorithm's tie rule and validation still determine the final choice.

## Key terms & formulas

- **Entropy:** \(H(S)=-\sum p_i\log_2p_i\).
- **Conditional entropy:** \(H(S|A)=\sum_v p_vH(S_v)\).
- **Information gain:** \(H(S)-H(S|A)\).
- **Split information:** \(-\sum_v p_v\log_2p_v\).
- **Gain ratio:** gain divided by split information.
- **Gini impurity:** \(1-\sum p_i^2\).
- **Weighted Gini split:** \(\sum_v p_vG(S_v)\).
- **Pre-pruning:** stop during growth.
- **Post-pruning:** remove subtrees after growth.
- **Leaf prediction:** majority class or class distribution.

## Common mistakes

1. **Using information gain without weighting branches:** every branch must be weighted by its size.
2. **Forgetting a factor's size in conditional entropy:** small pure branches are not automatically a strong split.
3. **Confusing gain ratio denominator with class entropy:** it is entropy of the split, not necessarily \(H(S)\).
4. **Testing numeric equality instead of thresholds:** tree splits normally use \(x\le t\) and \(x>t\).
5. **Growing until every leaf is pure:** this often overfits and is not required.
6. **Using the test set for pruning:** keep it untouched.
7. **Ignoring missing-value rules:** every split needs a valid path for incomplete data.

## Exam prep

**Likely 2-mark questions**
1. Define information gain. *Hint: reduction in entropy after an attribute split.*
2. Why does C4.5 use gain ratio? *Hint: to counter the bias of gain toward many-valued attributes.*
3. State two ways a decision tree can overfit. *Hint: excessive growth, tiny leaves, weak stopping/pruning, noisy attributes.*

**Likely long-answer questions**
1. Derive entropy, conditional entropy, and information gain for a supplied node. *Hint: class proportions, branch entropies, weighted average, difference.*
2. Build a classification tree step by step and read it as rules. *Hint: calculate candidate gains, choose the best, repeat, and stop.*
3. Compare ID3, C4.5, and CART. *Hint: gain versus gain ratio, missing/continuous/pruning features, and classification trees.*
4. Explain pre-pruning and post-pruning with a validation example. *Hint: early stopping versus subtree replacement and complexity penalty.*
