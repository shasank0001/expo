---
subject: ml
unit: 1
topic: machine-learning-applications
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Machine Learning Applications

## Overview

Machine learning is used when software can improve decisions by finding patterns in data, adapting to users, or processing information at a scale people cannot handle manually. Applications range from recommendations and fraud detection to medical diagnosis, computer vision, language translation, predictive maintenance, and scientific discovery.

The application is not just choosing an algorithm. A useful ML system starts with a decision, identifies available feedback, checks whether predictions can be acted upon, and accounts for errors and people. The same algorithm can work in very different domains, while two applications with similar data can require different objectives and safeguards.

## Explanation

### Application categories

1. **Prediction and classification:** estimate a numeric outcome or assign a class.
2. **Recommendation and ranking:** choose items, content, or actions for a particular user.
3. **Anomaly and risk detection:** identify records that differ from normal patterns.
4. **Forecasting and time-series prediction:** predict demand, prices, traffic, weather proxies, or resource use.
5. **Perception:** interpret images, video, speech, and sensor signals.
6. **Language understanding:** classify text, translate, summarise, answer questions, or detect sentiment.
7. **Control and optimisation:** choose actions for vehicles, robots, networks, or energy systems.
8. **Scientific and industrial analysis:** discover patterns in biology, chemistry, physics, agriculture, and manufacturing.

### Healthcare and medicine

ML can help with medical-image screening, risk prediction, drug discovery, patient monitoring, and clinical decision support. The target must be clinically meaningful and measured at the correct time. A model can support triage, but it should not conceal uncertainty or replace professional responsibility. Data privacy, demographic bias, distribution differences between hospitals, and false negatives are central concerns.

**Example:** a radiology model is trained on labelled scans to flag possible pneumonia. Its sensitivity, specificity, and calibration should be reported for relevant patient groups. A clinician reviews flagged and uncertain cases, and the system is monitored for changes in scanners and patient mix.

### Finance, banking, and fraud

Banks use ML for credit-risk estimation, fraud detection, customer segmentation, anti-money-laundering alerts, and algorithmic trading. Historical labels may reflect policy or inequality, and a model that maximises overall accuracy can impose heavy costs on rare fraud or minority applicants. Threshold selection, calibration, explainability, and regulatory review are important.

**Example:** a card-fraud model scores each transaction. A high score triggers a temporary review, not an automatic accusation. Investigators examine false positives and attack patterns; the score is one signal among transaction rules and customer history.

### Retail, marketing, and recommendation

Recommendation systems rank products using user history, item content, context, and sometimes sequential behaviour. They can be trained with explicit ratings or implicit feedback such as a click, purchase, or dwell time. Optimising clicks alone can promote clickbait. Systems use experimentation, counterfactual analysis, diversity, novelty, and business constraints.

**Example:** an online store suggests a product using collaborative filtering (customers with similar histories) and content features (brand, category, price). A ranking model then balances relevance, availability, margin, and fairness among sellers.

### Manufacturing and predictive maintenance

Sensors on machines produce time series. Models can detect abnormal vibration, estimate remaining useful life, and schedule maintenance before failure. A false alarm costs inspection; a missed failure can be expensive or dangerous. Models should be evaluated over time and integrated with work orders and human technicians.

**Example:** a motor's vibration spectrum changes as a bearing wears. A time-series anomaly model raises a maintenance ticket. The technician confirms the diagnosis; the model does not silently shut down the production line.

### Computer vision

Image classification, object detection, segmentation, face analysis, medical imaging, autonomous driving, and quality inspection use visual patterns. CNNs and vision transformers are common modern models. Data collection, lighting, camera angle, occlusion, label consistency, privacy, and adversarial examples are major issues.

### Natural-language processing

Text and speech systems classify documents, translate languages, extract entities, summarise content, answer questions, and recognise speech. Language contains ambiguity, slang, and context. A model trained on one domain may fail in another, and fluent output can still be factually wrong.

### Transportation and mobility

ML supports traffic forecasting, route optimisation, demand prediction, autonomous perception, driver assistance, and predictive fleet maintenance. Real-time data streams create latency and drift requirements. Safety-critical decisions need redundant sensors, deterministic safeguards, and human or system-level validation.

### Agriculture, environment, and education

Crop-yield models can combine weather, soil, and satellite data. Remote sensing can monitor forests, drought, and pollution. Education systems can recommend practice material or identify learners who need support, but high-stakes decisions require fairness, privacy, and teacher oversight.

## Worked examples

### Example 1: spam

A mail provider trains a classifier from messages users marked spam or not spam. Features include sender reputation, links, words, and attachment patterns. A message above a threshold is moved to a spam folder; a user can report a false positive. Feedback improves later models, subject to privacy controls.

### Example 2: demand forecasting

A retailer records date, weather, promotions, and units sold. A model forecasts demand for each store/product horizon. It must be evaluated with time-aware splits so that future information never enters training. Forecasts help stock and staffing decisions; they are not guarantees.

### Example 3: crop yield

A model uses rainfall, soil nutrients, temperature, and satellite features to predict yield. A high predicted yield is not an instruction to plant differently; agronomic experiments and local expertise are still needed to establish a causal recommendation.

### Example 4: quality inspection

A camera system learns defects from labelled images. It can inspect thousands of items quickly, but a rare defect may be absent from training. Confidence thresholds, human inspection of uncertain cases, and periodic re-sampling are safer than blind automation.

## Key terms & formulas

- **Application domain:** the real-world setting in which a model operates.
- **Task:** the prediction or decision the application needs.
- **Explicit feedback:** a direct signal such as a rating, label, or measurement.
- **Implicit feedback:** indirect behaviour such as a click, purchase, or watch time.
- **Decision threshold:** score boundary that triggers an action.
- **Calibration:** agreement between predicted probabilities and observed frequencies.
- **Predictive maintenance:** maintenance scheduled from predicted failure risk.
- **Anomaly:** an observation that differs from an expected pattern.
- **Recommendation:** a ranked item suggested to a user or context.
- **Business metric:** an outcome tied to value or harm, not only technical accuracy.
- **Deployment feedback:** new labels, outcomes, or user behaviour used to improve a system.
- **Human oversight:** review, escalation, or override by an authorised person.

## Common mistakes

1. **Starting with an algorithm instead of a decision.** Define who acts, on what, and how errors cost.
2. **Equating a technical metric with business value.** Accuracy must be connected to the application consequence.
3. **Ignoring time and context.** A model trained before a policy change may be invalid after it.
4. **Using implicit feedback without checking bias.** Clicks and purchases reflect availability and exposure as well as preference.
5. **Failing to include people in the workflow.** Clinicians, operators, teachers, and customers may need explanations and override.
6. **Assuming more data from the same biased system is neutral.** It can reproduce historical discrimination.

## Exam prep

### Likely 2-mark questions

- **Name three application domains of ML.** Any of healthcare, finance, retail, manufacturing, vision, NLP, transport, agriculture, or education.
- **What is predictive maintenance?** Using data to estimate equipment failure risk and schedule maintenance.
- **Why can a recommendation system optimise clicks incorrectly?** Clicks are a proxy and can be manipulated or reflect exposure.
- **Give one application-specific data concern.** Privacy in health data, drift in fraud, or class imbalance in medical screening.

### Long-answer prompts

- **Describe ML applications in one domain of your choice.** Explain the task, features and labels, model, metrics, workflow integration, risks, and monitoring.
- **Compare recommendation, forecasting, and classification applications.** Discuss feedback, data, decisions, and metrics.
- **How should ML be used in healthcare?** Describe possible benefits, validation requirements, privacy, bias, human oversight, and failure cases.
- **Explain why application design is more than model selection.** Use cost of errors, feedback loops, deployment, and governance.
