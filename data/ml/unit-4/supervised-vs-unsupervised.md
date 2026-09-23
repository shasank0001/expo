---
subject: ml
unit: 4
topic: supervised-vs-unsupervised
syllabus_ref: CSM3201 Unit-IV
status: draft
---
# Supervised vs Unsupervised Learning

## Overview

Supervised and unsupervised learning differ in whether the learner receives a target answer for each training example. Supervised learning fits a mapping from features to known labels or values. Unsupervised learning discovers structure in unlabelled data, such as clusters or low-dimensional patterns. Both can use the same algorithms and both can be useful, but their data requirements and validation are different.

The distinction is about feedback, not complexity. A simple nearest-neighbour method can be supervised or unsupervised depending on whether labels are used. A complex neural network can be trained in either paradigm.

## Explanation

### Supervised learning

For

\[
D_s=\{(x_i,y_i)\}_{i=1}^{n},
\]

the algorithm compares predictions with \(y_i\) through a loss. The target may be a class (classification) or a number (regression). A clear error measure such as accuracy, F1, MAE, or RMSE is available when the target is known. This makes model comparison and supervised tasks relatively direct.

The target must be available and meaningful. A weak label can be noisy, and a label recorded after the decision can create leakage. Historical labels can encode bias. A supervised model learns the relationship represented by those labels, not automatically the truth or a causal effect.

### Unsupervised learning

For

\[
D_u=\{x_1,\ldots,x_n\},
\]

there is no target. The algorithm optimises a structural criterion, for example

\[
\min_C\sum_{k=1}^{K}\sum_{x_i\in C_k}\|x_i-\mu_k\|^2
\]

for k-means, or a density, reconstruction, or rule objective. It can identify compact groups, high-dimensional structure, rare records, and co-occurrence. There is no unique answer without labels or a domain criterion.

### Data and feedback

| Aspect | Supervised | Unsupervised |
|---|---|---|
| Training target | Known \(y\) | None |
| Feedback | Compare with target | Objective on structure |
| Typical tasks | Classification, regression | Clustering, reduction, density, rules |
| Correctness | Metrics against target | Internal, stability, domain evidence |
| Main risk | Leakage/overfitting to labels | Meaningless or unstable structure |
| Human role | Define labels and costs | Interpret and validate structure |

### Strengths

Supervised learning directly addresses a defined prediction task and often offers clearer performance feedback. It is appropriate when labelled data and target decisions exist. Unsupervised learning can work with large unlabelled data, reveal unknown patterns, and support exploration or feature construction.

### Limitations

Supervised learning needs labels, which may be expensive, delayed, subjective, or biased. It can optimise a proxy and produce high average accuracy while failing on a minority group. Unsupervised learning is sensitive to preprocessing and assumptions, has subjective validity, and can produce clusters that are unstable or sensitive. Neither paradigm automatically handles concept drift or deployment risk.

### Hybrid use

The paradigms often work together. A bank can cluster customers before training separate churn models. Images can be grouped to create candidate labels for manual annotation, then used in supervised learning. A representation learned from unlabelled data can improve a classifier. Semi-supervised learning uses both labelled and unlabelled examples.

### Choosing between them

Choose supervised learning when the target is available, the decision is clear, and the deployment population is represented. Choose unsupervised learning when the goal is discovery and labels are unavailable. Choose hybrid methods when a small labelled set can anchor a large unlabelled set or when structure should be tailored to a downstream task. Ask what evidence would count as success.

## Worked examples

### Example 1: spam

Labelled spam and normal messages support supervised classification. A threshold, precision, recall, and false-positive cost can be measured. An unlabelled mail archive could be clustered to discover message types, but cluster names would not establish which type is spam without labels or domain review.

### Example 2: customer segmentation

Unsupervised clustering groups customers based on behaviour. If the business then predicts churn for each group using labels, the workflow becomes hybrid. The clusters may be useful features, but they can also reinforce unequal treatment and should not be treated as inherent customer types.

### Example 3: image data

A large unlabelled image collection can be clustered or used for self-supervised representation learning. A smaller labelled subset trains a classifier. The representation is not a class label; the labelled phase supplies the task meaning.

### Example 4: anomaly detection

A one-class or density model uses normal-looking unlabelled records to identify unusual ones. Investigators provide labels after reviewing alerts. The model is unsupervised at inference, while a supervised evaluator can later measure its usefulness.

## Key terms & formulas

- **Supervised learning:** learning from \((x,y)\) pairs.
- **Unsupervised learning:** learning structure from \(x\)'s without \(y\).
- **Label:** known target used as feedback.
- **Unlabelled observation:** an input without a task target.
- **Classification:** supervised prediction of a class.
- **Regression:** supervised prediction of a numeric target.
- **Clustering:** unsupervised grouping by similarity.
- **Dimensionality reduction:** unsupervised or self-supervised representation with fewer dimensions.
- **Within-cluster objective:** dispersion used by k-means and similar methods.
- **Inductive bias:** assumptions of the chosen algorithm.
- **Label quality:** correctness and meaningfulness of targets.
- **Weak label:** indirect or noisy proxy target.
- **Hybrid learning:** combining labelled and unlabelled information.
- **Domain validation:** checking that structure is useful to stakeholders.

## Common mistakes

1. **Saying supervised learning always has clean labels.** Labels can be noisy, biased, or weak.
2. **Saying unsupervised learning has no correctness.** There is no direct target, but there are internal, stability, and domain criteria.
3. **Assuming algorithm complexity determines the type.** kNN and neural networks can be used in both settings.
4. **Using cluster IDs as causal classes.** They are algorithmic summaries.
5. **Ignoring the cost of obtaining labels.** Semi-supervised or unsupervised approaches may be preferable when labels are scarce.
6. **Evaluating unsupervised results only by a silhouette score.** Meaning and stability also matter.
7. **Forgetting deployment drift and governance.** Both paradigms need monitoring and human accountability.

## Exam prep

### Likely 2-mark questions

- **Differentiate supervised and unsupervised learning.** State whether target labels and direct error feedback are available.
- **Give one supervised and one unsupervised task.** Fraud detection; customer clustering.
- **What is a weak label?** An indirect or noisy target used as a proxy for the true outcome.
- **Give one hybrid-learning example.** Cluster unlabelled customers, then train a supervised churn model.

### Long-answer prompts

- **Compare supervised and unsupervised learning in a table or discussion.** Cover data, objectives, metrics, strengths, limitations, and examples.
- **Explain why unsupervised results require interpretation.** Use distance, scaling, objective, stability, and domain meaning.
- **Describe a hybrid supervised/unsupervised workflow.** Use semi-supervision, clustering, representation learning, or human labelling.
- **How would you decide which paradigm fits a problem?** Discuss target availability, decision, costs, data, and evaluation.
