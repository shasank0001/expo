---
subject: ml
unit: 4
topic: unsupervised-learning-applications
syllabus_ref: CSM3201 Unit-IV
status: draft
---
# Applications of Unsupervised Learning

## Overview

Unsupervised learning helps people explore data when labels are unavailable, expensive, or not the first question. It can discover customer segments, organise documents and images, compress high-dimensional data, identify anomalies, reveal latent factors, and find co-occurring items or events. The output is a hypothesis about structure that must be tested and interpreted.

Applications are strongest when there is a clear action after discovery. A cluster that nobody can use is an analysis curiosity; a segment that changes a support policy, a low-dimensional representation that improves a model, or an anomaly queue that prioritises investigation can be valuable.

## Explanation

### Customer segmentation and marketing

Behavioural variables such as recency, frequency, monetary value, product preferences, and response rates can be clustered. Businesses may create segments for onboarding, retention, inventory, or campaigns. Cluster profiles are descriptive, not identities. They can change over time, and assigning a person based on past behaviour can exclude people with little history.

### Document and text organisation

TF–IDF vectors, embeddings, topic models, and hierarchical clustering can organise articles, support tickets, or emails. The result can improve search, routing, or human review. A cluster label such as “billing” is an interpretation. Evaluate on later documents and check whether the vocabulary distinguishes a useful topic rather than a formatting artefact.

### Image and video analysis

Unsupervised methods can group images by visual similarity, remove near-duplicates, discover object categories, and compress representations. Autoencoders and contrastive methods learn features from unlabelled images. They can still encode sensitive attributes and must be tested for bias, privacy, and failure under new cameras or environments.

### Anomaly detection

Density, distance, reconstruction, and one-class methods flag records unlike normal data. Applications include fraud screening, equipment monitoring, network intrusion, data-quality monitoring, and unusual customer behaviour. An anomaly is a triage signal, not a diagnosis. A rare event may be important, and a normal-looking record may be harmful.

### Dimensionality reduction and visualisation

PCA, t-SNE, UMAP, autoencoders, and factor analysis compress many features. They can make high-dimensional data visible and speed up a model. A 2-D plot is a projection: distances and clusters may be distorted. Use quantitative validation and domain inspection before interpreting axes as real factors.

### Latent-factor and recommender support

Factor models infer hidden preferences or traits from responses. Collaborative filtering and clustering can identify user/item groups, while matrix factorisation learns latent preferences. The learned factors may improve recommendations, but they can amplify popularity, exposure, or sensitive correlations.

### Association and event discovery

Market-basket analysis finds products bought together; event logs can reveal sequences or co-occurrences. Support and confidence quantify observed frequency, but association does not imply that one item causes another. Confounders such as a seasonal promotion can explain both purchases.

### Scientific and industrial use

Astronomy, genomics, chemistry, agriculture, and manufacturing contain high-dimensional observations with few labels. Unsupervised methods help identify candidate subtypes, quality regimes, or experimental conditions. Scientific validation and replication are essential; a computational cluster is a hypothesis about a system.

### Responsible deployment

Unsupervised outputs can be sensitive because they create groups or profiles without an individual label. Apply data minimisation, access control, purpose limitation, fairness analysis, and human review. A cluster may proxy for protected characteristics. An anomaly score may expose a person to investigation. Document the objective, intended use, uncertainty, and retention period.

## Worked examples

### Example 1: retail segmentation

A retailer clusters customers by recency, frequency, and average order value. One group has high frequency and low returns; another has high value but infrequent purchases. The marketing team tests different offers with a controlled experiment. It does not assume the groups are permanent or inherently valuable.

### Example 2: document routing

A help desk has 100,000 tickets. Unlabelled text is clustered into topics. Representatives label a sample, merge incorrect groups, and train a supervised classifier for routing. The clustering reduces annotation cost, while the classifier supplies task-level evaluation.

### Example 3: manufacturing anomalies

A machine's vibration representation is learned from normal operation. A high reconstruction error flags a tool change. The technician checks the machine; the model does not stop it automatically unless a safety rule requires it.

### Example 4: grocery association

Bread and butter co-occur in 30% of transactions, and 37.5% of bread purchases include butter. The rule may support a promotion, but a sale campaign could cause both items to appear together. Test the recommendation or intervention rather than claiming causality.

## Key terms & formulas

- **Segmentation:** division into meaningful behavioural groups.
- **Topic model:** probabilistic model of latent topics in documents.
- **Embedding:** dense vector representation of an object.
- **Anomaly detection:** identification of unusual observations.
- **One-class model:** model of normal data used to score novelty.
- **Dimensionality reduction:** representation with fewer variables.
- **PCA:** orthogonal linear projection using leading eigenvectors.
- **t-SNE/UMAP:** non-linear visualisation methods.
- **Latent preference:** unobserved user or item factor.
- **Support:** frequency of an item set or rule.
- **Confidence:** conditional frequency of a consequent.
- **Novelty score:** degree to which an observation differs from learned normal structure.
- **Data governance:** rules for access, use, retention, and accountability.

## Common mistakes

1. **Treating clusters as permanent customer identities.** Behaviour and data change.
2. **Using a 2-D visualisation as proof of separation.** Projection can distort distance.
3. **Calling an anomaly malicious or defective.** It needs investigation.
4. **Treating association as causation.** Promotions, season, and confounding are alternatives.
5. **Ignoring privacy when profiling groups.** Unlabelled data can still be identifiable.
6. **Evaluating clusters only by an internal score.** Domain usefulness and stability are essential.
7. **Assuming a self-supervised representation is unbiased.** It learns patterns from the data source.

## Exam prep

### Likely 2-mark questions

- **Give three applications of unsupervised learning.** Segmentation, document organisation, anomaly detection, dimensionality reduction, or recommendation.
- **What is an anomaly?** An observation unusual under a reference distribution or model.
- **Why are association rules not causal?** They describe frequency, not interventions or mechanisms.
- **What is a latent factor?** An unobserved construct inferred from observed variables.

### Long-answer prompts

- **Describe three unsupervised applications in detail.** Include data, method, output, validation, and risk.
- **Explain how clustering can support a supervised system.** Use segmentation, feature construction, or annotation triage.
- **How should an unsupervised anomaly-detection system be deployed?** Discuss normal-data modelling, thresholds, investigation, drift, and false alarms.
- **Evaluate the use of clustering for customer marketing.** Discuss representation, stability, privacy, fairness, experiments, and interpretation.
