---
subject: dwdm
unit: 1
topic: kinds-of-patterns
syllabus_ref: CSM3101 Unit-I
status: draft
---
# Kinds of Patterns

## Overview

A data-mining task becomes concrete when we ask what kind of pattern we want to find. Han, Kamber, and Pei distinguish **descriptive** and **predictive** tasks. Descriptive tasks characterize data, while predictive tasks classify records or estimate an outcome. They also discuss association, clustering, sequence, trend, and outlier analysis. Tan, Steinbach, and Kumar similarly emphasize that an intended task determines the data representation, model objective, and evaluation method.

A pattern is not just any repeatable observation. It should be valid on the data, sufficiently supported, meaningful to the user, and useful for a decision or scientific question. This note covers the major pattern types in a simple, exam-ready order and connects each type to a numerical example.

## Explanation

### 1. What makes a pattern useful?

A pattern may summarize an association, define a class, predict an outcome, or expose structure not visible from individual records. A discovered result is useful only when it meets several conditions:

- **Validity:** it is logically true and free of unsupported interpretation.
- **Interestingness:** it is unusual, actionable, or more informative than the user's prior knowledge.
- **Support:** enough records or transactions support the result.
- **Generality:** it applies beyond a tiny exception, if generalization is intended.
- **Simplicity or interpretability:** a user can understand or act on it.
- **Usefulness:** it helps a decision, prediction, explanation, or scientific discovery.
- **Stability:** it remains reasonably reliable on new data from the intended population.

A rare observation may still be a valid outlier and therefore interesting, even if it has low frequency. Therefore “interesting” is not identical to “frequent.”

### 2. Descriptive patterns

A **descriptive pattern** summarizes the current data. It describes properties of a collection without necessarily using a trained model for prediction.

Examples include:

- the mean and spread of customer spending;
- the distribution of examination marks;
- the most common product categories;
- which customers form a large segment;
- items frequently purchased together;
- monthly sales trends;
- unusual records that differ from the main population.

Descriptive patterns answer questions such as:

- What does the data look like?
- What is common?
- How is it distributed?
- What changed over time?
- Which groups or exceptions exist?

Han, Kamber, and Pei use **characterization** to find a general feature or typical characteristics of a target class. It may be a summarized profile, such as “passing students usually have attendance above 75% and an average of 65% or more.” Discrimination finds features that distinguish a target class from other classes.

### 3. Classification patterns

A **classification pattern** assigns a record to a known class using attributes and learned decision rules or models. The class is a label such as pass/fail, fraud/not fraud, spam/not spam, low/medium/high risk, or healthy/diseased.

A classifier may use:

- decision trees;
- rules;
- naive Bayes models;
- k-nearest neighbors;
- logistic regression;
- support vector machines;
- neural networks.

For a new object, the classifier estimates a class. Classification is supervised because labeled training examples normally guide learning.

A confusion matrix evaluates the result. For two classes:

```text
                 Predicted positive  Predicted negative
Actual positive         TP                    FN
Actual negative         FP                    TN
```

The meaning depends on which outcome is treated as “positive.” Fraud detection and disease screening commonly care strongly about false negatives, while spam filters may need to control false positives.

### 4. Prediction patterns

A **predictive pattern** estimates a future or unknown value. Prediction may be:

- **Classification prediction:** predicts a category, such as whether a customer will churn.
- **Numeric regression prediction:** predicts a quantity, such as next month's sales.

A prediction pattern normally includes an estimated value and a measure of uncertainty or error. Useful evidence includes training performance, validation or test performance, comparison with a simple baseline, and behavior under realistic conditions.

A predictive pattern should not be confused with a causal explanation. A model may predict an outcome accurately because of correlations, but it does not by itself prove that changing the input will cause the predicted result.

### 5. Association patterns

An **association pattern** describes items, events, or conditions that occur together more often than expected. An association rule is written

\[
A \rightarrow B
\]

It expresses that the presence of antecedent \(A\) is associated with consequent \(B\).

Common measures are:

\[
\text{support}(A \rightarrow B) = \frac{N_{AB}}{N}
\]

\[
\text{confidence}(A \rightarrow B) = \frac{N_{AB}}{N_A}
\]

where \(N\) is the number of transactions, \(N_A\) is the number containing \(A\), and \(N_{AB}\) is the number containing both.

Association patterns may be unary, binary, or multi-association patterns. Examples include “bread and milk are often purchased together” and “high rainfall is associated with the use of umbrellas.”

A rule can be statistically frequent but not actionable. A high support/confidence rule may be a logical consequence of another rule and add little new knowledge, so lift, leverage, and confidence, or domain reasoning, may also be needed.

### 6. Cluster patterns

A **cluster pattern** organizes objects into groups whose members are more similar to one another than to objects in other groups. The data may not initially contain class labels, so clustering is commonly unsupervised.

Possible cluster characteristics include:

- similar purchasing behavior;
- similar movement patterns;
- similar geographic and environmental conditions;
- similar symptoms;
- customers with comparable risk profiles.

A useful cluster should have enough within-cluster similarity and between-cluster separation to justify its existence. Stability and interpretability matter. A grouping that changes drastically under a small change in method or random seed may not be reliable.

### 7. Sequence and trend patterns

A **sequence pattern** describes important ordered events. Examples include:

- bread → milk → cereal in supermarket transactions;
- fever → cough → recovery in clinical records;
- website page A → search → purchase;
- product defect → complaint → repair.

Sequences are not ordinary associations because the order and often the time gaps matter. A sequence may include a minimum and maximum time span and directional transitions.

A **trend pattern** describes gradual change over time, such as increasing online sales. Cyclical behavior, seasonality, and sudden changes may occur together, so a simple line trend is not always enough.

### 8. Outlier or exception patterns

An **outlier** is an object that differs substantially from the expected distribution or group. It may indicate:

- a data-entry error;
- unusual behavior;
- a rare but valid case;
- fraud or system failure;
- a scientifically important phenomenon.

Outliers should not be deleted automatically. The correct response depends on whether the record is erroneous, irrelevant, or a valid rare observation. Some methods, including clustering and density-based analysis, are designed to find outliers.

### 9. Choosing a pattern type

A useful decision sequence is:

1. State the question in plain language.
2. Decide whether the goal is description or prediction.
3. Identify the target output: none, class, numeric value, itemset, sequence, group, or anomaly.
4. Select the data attributes and check their types.
5. Choose an evaluation measure.
6. Split or collect validation data before tuning.
7. Test usefulness and stability on new data.

The following distinctions should be memorized:

- description reports what exists; prediction estimates what may occur;
- classification predicts a known class; clustering discovers unknown groups;
- association emphasizes co-occurrence; sequence emphasizes order;
- a rule says “if these occur, those tend to occur”; it does not necessarily imply “if this is done, that must happen.”

## Worked examples

### Example 1: Characterization

A college has 1,000 students. Of these, 800 pass. Among passing students, 680 have attendance above 75%, 620 have an average mark above 65, and 520 have both.

A characterization pattern is:

> Passing students commonly have high attendance and average marks above 65.

The pattern describes a typical feature of the target group. It does not claim that every passing student has both features or that low attendance makes passing impossible.

### Example 2: Classification and a confusion matrix

A model predicts whether a transaction is fraudulent. On 200 test transactions:

```text
                     Predicted fraud  Predicted legitimate
Actual fraud                 18                 2
Actual legitimate             8                172
```

Therefore:

- \(TP = 18\)
- \(FN = 2\)
- \(FP = 8\)
- \(TN = 172\)

\[
\text{Precision} = \frac{18}{18+8} = 0.6923
\]

\[
\text{Recall} = \frac{18}{18+2} = 0.9000
\]

\[
\text{Accuracy} = \frac{18+172}{200} = 0.9500
\]

The model has high accuracy but misses 2 of 20 actual fraud cases. A bank concerned about missed fraud may accept a lower precision if investigation capacity is sufficient. Thus the target class and cost determine the preferred measure.

### Example 3: Numeric prediction

A retailer records advertising spend and sales. A regression model predicts next month's sales as ₹480,000 with an uncertainty interval of ₹450,000 to ₹510,000. This is a predictive pattern. The interval communicates uncertainty; a point value alone hides it.

A stronger answer would also report the model's validation RMSE, compare it with a baseline, and state that the prediction is not automatically causal.

### Example 4: Association rule

There are 1,000 shopping transactions:

- 300 contain bread;
- 260 contain milk;
- 180 contain both.

Then:

\[
\text{support}(\text{bread} \rightarrow \text{milk})
= 180/1000 = 0.18
\]

\[
\text{confidence}(\text{bread} \rightarrow \text{milk})
= 180/300 = 0.60
\]

\[
\text{support}(\text{milk}) = 260/1000 = 0.26
\]

\[
\text{lift} = 0.60/0.26 \approx 2.31
\]

Because lift is above 1, bread purchases are positively associated with milk purchases. The retailer may test a bundle, but a temporary increase caused by a general sales campaign is another possible explanation.

### Example 5: Cluster pattern

A telecom company groups customers using average monthly use, late-payment frequency, and support calls. It obtains three groups:

- Cluster A: low use, low late payment, few calls;
- Cluster B: high use, high late payment, many calls;
- Cluster C: moderate use, moderate late payment, few calls.

These are discovered groups, not labels supplied by the bank. The group descriptions are descriptive patterns. If Cluster B has a high observed churn rate, that association may motivate a retention study, but it does not automatically prove the cluster causes churn.

### Example 6: Sequence pattern

A logging system records events:

```text
Monday 10:00  login
Monday 10:03  search product
Monday 10:07  add to cart
Monday 10:12  purchase
```

The ordered sequence `login → search → add to cart → purchase` is a sequence pattern. A set containing the same events without order would only be an association.

### Example 7: Outlier

Customer monthly spending values are:

```text
800, 850, 820, 790, 840, 860, 900, 2,300
```

Most values lie near ₹800–₹900. The value ₹2,300 is an outlier. The analyst should investigate whether it came from a bulk purchase, a data-entry error, or fraud. It may be invalid for an ordinary-spending model but highly important for fraud analysis.

## Key terms & formulas

- **Pattern:** a useful and potentially repeatable structure in data.
- **Descriptive pattern:** a summary of existing data.
- **Characterization:** identification of the general features of a target class.
- **Discrimination:** identification of features that distinguish one class from another.
- **Classification pattern:** a rule or model that assigns a record to a known class.
- **Predictive pattern:** an estimate of a class or numeric outcome for an unseen case.
- **Regression:** prediction of a continuous numeric value.
- **Classification:** prediction of a categorical class.
- **Association pattern:** a rule describing items or events that occur together.
- **Cluster pattern:** a group of similar objects discovered without required class labels.
- **Sequence pattern:** an ordered series of important events.
- **Trend pattern:** a change in level or direction over time.
- **Outlier:** an object substantially unlike the expected data.
- **Confidence factor:** the fraction of a rule's predictions that are correct, under the dataset's evaluation method.
- **Support:** \(\operatorname{support}(X)=\frac{N_X}{N}\).
- **Confidence:** \(\operatorname{confidence}(X\rightarrow Y)=\frac{N_{X\cap Y}}{N_X}\).
- **Lift:** \(\operatorname{lift}(X\rightarrow Y)=\frac{\text{confidence}(X\rightarrow Y)}{\operatorname{support}(Y)}\).
- **Accuracy:** \(\frac{TP+TN}{TP+TN+FP+FN}\).
- **Precision:** \(\frac{TP}{TP+FP}\).
- **Recall or sensitivity:** \(\frac{TP}{TP+FN}\).
- **F1:** \(\frac{2PR}{P+R}\), the harmonic mean of precision and recall.
- **Mean absolute error:** \(\frac{1}{n}\sum_{i=1}^{n}|y_i-\hat y_i|\).
- **Root mean squared error:** \(\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat y_i)^2}\).

## Common mistakes

1. **Equating description and prediction.** A description says what is in the data; a prediction estimates an unknown or future result.
2. **Confusing classification and clustering.** Classification predicts a supplied class; clustering discovers unknown groups.
3. **Confusing association and sequence.** Association requires co-occurrence; sequence includes meaningful order and possibly time constraints.
4. **Interpreting an association as causation.** Bread and milk may be bought together without one item causing the purchase of the other.
5. **Ignoring the class baseline.** A 95% accuracy may be worse than always predicting the majority class when 95% of records are negative.
6. **Deleting every outlier automatically.** An unusual value may be an error, or it may be the most important observation.
7. **Treating low frequency as uninteresting.** A rare failure or disease pattern can be highly valuable.
8. **Evaluating on training data only.** Patterns should be tested on unseen data to estimate generalization.
9. **Confusing association confidence with conditional probability under uncertain causation.** An association is estimated from data and does not guarantee future behavior.
10. **Forgetting goodness of fit for numeric prediction.** RMSE, MAE, \(R^2\), and uncertainty are needed as appropriate.

## Exam prep

### Likely 2-mark questions

1. **Differentiate descriptive and predictive patterns.**  
   *Hint:* Description summarizes existing data; prediction estimates an unknown class or value.

2. **Define a classification pattern.**  
   *Hint:* A learned rule or model that assigns an object to one of the known classes.

3. **What is an association pattern?**  
   *Hint:* A description of items or events that occur together, often represented by a rule \(A \rightarrow B\).

4. **Differentiate classification and clustering.**  
   *Hint:* Known class versus discovered group; supervised versus usually unsupervised.

5. **What is a sequence pattern?**  
   *Hint:* A meaningful ordered series of events, possibly constrained by time.

6. **Define support for a rule.**  
   *Hint:* The fraction of all transactions containing the rule's itemset.

7. **What is an outlier?**  
   *Hint:* An object substantially unlike the expected data; it may be erroneous or valid.

8. **Why is high classification accuracy not always sufficient?**  
   *Hint:* Class imbalance and the costs of false positives and false negatives can make accuracy misleading.

### Likely long-answer questions

1. **Explain the major kinds of data-mining patterns with examples.**  
   *Answer hint:* Cover descriptive, characterization, classification, predictive/numeric, association, cluster, sequence/trend, and outlier patterns. For each, state its output and one use case.

2. **Explain classification and evaluate a result using a confusion matrix.**  
   *Answer hint:* Define TP, TN, FP, and FN, compute accuracy, precision, recall, and F1, and discuss which metric matters for the chosen application.

3. **Explain association-rule mining using support, confidence, and lift.**  
   *Answer hint:* Give the formulas, calculate them from a transaction count, interpret lift, and distinguish association from causality.

4. **Compare clustering and classification as pattern-discovery tasks.**  
   *Answer hint:* Compare labels, objectives, algorithms, evaluation, interpretability, and the fact that clustering can generate candidate groups for later supervised analysis.

5. **Describe sequence, trend, and outlier patterns.**  
   *Answer hint:* Use ordered event examples, time-series examples, and a distribution-outlier example. Explain why rare values should be investigated rather than automatically deleted.
