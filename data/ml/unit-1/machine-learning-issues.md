---
subject: ml
unit: 1
topic: machine-learning-issues
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Issues in Machine Learning

## Overview

An ML model can score well in an experiment and still create serious problems for people or organisations. Issues arise from poor data, biased objectives, privacy and security risks, unexplainable decisions, changing environments, computational limits, and weak reproducibility. These are not optional “extra” concerns: they are part of the model’s quality.

Responsible practice means identifying risks early, measuring them, documenting decisions, limiting harm, and keeping human accountability. The goal is not to eliminate uncertainty; it is to make uncertainty and trade-offs visible so that a system is fit for its intended use.

## Explanation

### Data quality and quantity

Real data may contain missing values, duplicates, inconsistent units, typographical errors, outliers, inconsistent labels, and sampling bias. A model can learn annotation shortcuts rather than the intended concept. The data-generating process matters more than a spreadsheet of “clean” rows. Collect enough examples, preserve provenance, inspect missingness, and test performance on relevant subgroups.

### Bias and fairness

A model can reproduce historical discrimination through data or through the choice of target and features. **Representational bias** occurs when a group is underrepresented. **Measurement bias** occurs when a proxy behaves differently across groups. **Aggregation bias** hides meaningful differences when categories are combined. **Label bias** reflects unequal judgments or access.

A high overall score does not establish fairness. Compare false-positive rates, false-negative rates, calibration, opportunity, and error costs by group. There is no single universal fairness definition; the choice must be discussed with affected people and domain experts.

### Privacy and governance

Training data may contain names, addresses, health information, financial records, images, or private messages. Data minimisation, purpose limitation, informed consent, access control, encryption, anonymisation, retention limits, and secure deletion are basic controls. De-identification is not automatically perfect: quasi-identifiers can re-identify people. Synthetic data also requires checking privacy leakage and representativeness.

### Security

Models face data poisoning, adversarial examples, prompt injection in language systems, model theft, membership inference, extraction of sensitive training information, and unsafe tool use. Security must cover the data pipeline, model artefact, serving endpoint, dependencies, and user permissions. A high test score is not a security assessment.

### Interpretability and explainability

A complex model may be accurate but difficult to justify. Interpretability methods such as coefficients, tree diagrams, partial-dependence plots, permutation importance, local surrogates, and attention visualisations each provide a different partial view. An explanation should match the question: global understanding, a single decision, or a debugging signal. Explanation does not prove correctness or causality.

### Generalisation and distribution shift

Training data may represent a particular time, location, device, or population. The model can fail when the distribution changes:

- **Concept drift:** \(P(y\mid x)\) changes, such as customer behaviour after a policy change.
- **Covariate/data drift:** \(P(x)\) changes, such as a new camera or season.
- **Prior/label shift:** class proportions change.

Monitoring can compare feature ranges, missingness, confidence, outputs, and delayed outcome metrics. Drift alerts require investigation; they are not proof of failure.

### Overfitting, robustness, and uncertainty

A model can overfit training noise or be brittle to small changes. Regularisation, data augmentation, robust optimisation, ensembles, and careful validation help. Predictive uncertainty has two parts: **aleatoric** uncertainty from inherent noise and **epistemic** uncertainty from limited knowledge. Confidence scores need calibration; an uncalibrated 0.9 does not mean 90% chance of correctness.

### Compute and practical constraints

Large data and models require memory, energy, latency, and maintenance. A highly accurate model may be too slow for an emergency or too expensive to train frequently. Use model compression, caching, batching, feature selection, and an appropriate model size only after establishing that the constraints are real.

### Reproducibility and documentation

Random seeds, library versions, data snapshots, preprocessing, stopping criteria, and evaluation splits should be recorded. A result without uncertainty or provenance cannot be audited. Data and model licences also matter.

### Accountability and human factors

The organisation deploying a system remains responsible for its consequences. Define who can override, appeal, or disable predictions. Explain uncertainty in language users can understand, avoid manipulative interfaces, and obtain feedback from affected groups. A technically accurate recommendation can still be unacceptable if it causes fatigue, unsafe behaviour, or exclusion.

## Worked examples

### Example 1: biased medical data

A hospital system serves a population with limited representation of one ethnic group. A model trained on historical diagnoses may have different sensitivity for that group. A global accuracy report hides the issue. Before deployment, the team checks subgroup sensitivity and calibration, investigates data collection, and provides clinician review.

### Example 2: adversarial spam

A spam classifier learns that a particular token predicts spam. An attacker inserts the token into ordinary messages, causing false positives. Retraining on the attacked data may reduce security further. Robustness testing, rate limits, multiple signals, and human review are needed.

### Example 3: model drift

A news recommender trained before an election has historical click patterns. After the election, user interests and content supply change. A sudden change in feature and category distributions prompts investigation. The team compares click quality, not merely click-through rate, and retrains only after validating the new data.

### Example 4: unreproducible result

A researcher reports 94% accuracy but does not state the split, preprocessing, random seed, or class balance. Re-running the code may produce a different result. A versioned dataset, environment file, fixed evaluation protocol, and confidence interval make the claim reviewable.

## Key terms & formulas

- **Data quality:** fitness of data for the intended use.
- **Bias:** systematic error or unfairness relative to a stated objective and group.
- **Fairness:** property assessed using explicit criteria, not a single universal score.
- **Privacy:** protection against unwanted identification or disclosure.
- **Data minimisation:** collecting only data needed for a defined purpose.
- **Adversarial example:** an input designed to cause an unexpected model behaviour.
- **Interpretability:** degree to which a model or decision can be understood.
- **Distribution shift:** change in the data-generating distribution.
- **Concept drift:** change in \(P(y\mid x)\).
- **Data drift:** change in \(P(x)\).
- **Calibration:** agreement between predicted probability and observed frequency.
- **Robustness:** resistance to relevant perturbations.
- **Model card:** a document describing intended use, data, performance, limitations, and ethics.
- **Human override:** an authorised person changing or rejecting a model output.
- **Confidence interval:** a range expressing sampling uncertainty around an estimate.

## Common mistakes

1. **Treating accuracy as evidence of fairness, safety, or calibration.** It is only one metric.
2. **Ignoring subgroups because the overall test is large.** Rare groups can carry the greatest harm.
3. **Assuming anonymisation guarantees privacy.** Re-identification and leakage remain possible.
4. **Treating feature importance as causal proof.** Importance describes a model's behaviour under a chosen method.
5. **Failing to monitor drift.** Deployment data rarely remain exactly like training data.
6. **Recording results without a protocol.** An unrepeatable score is weak evidence.
7. **Making accountability diffuse.** Someone must own the system, review failures, and stop it when necessary.

## Exam prep

### Likely 2-mark questions

- **Name two issues in machine learning.** Bias, privacy, security, drift, interpretability, reproducibility, or compute.
- **What is concept drift?** A change in the relationship between inputs and targets over time.
- **Why is overall accuracy insufficient?** It can hide subgroup errors, class imbalance, calibration failures, and unequal costs.
- **What is a model card?** A document describing intended use, data, metrics, limitations, and safeguards.

### Long-answer prompts

- **Discuss ethical and technical issues in machine learning.** Cover data bias, privacy, fairness, security, interpretability, drift, and accountability with examples.
- **How would you evaluate whether an ML system is fair?** Describe subgroup definitions, error metrics, calibration, stakeholder input, and trade-offs.
- **Explain the security risks of an ML application.** Cover poisoning, adversarial inputs, privacy leakage, model extraction, and mitigations.
- **Describe a monitoring plan after deployment.** Include data quality, drift, performance with delayed labels, latency, cost, subgroup checks, alerts, and rollback.
