---
subject: ml
unit: 2
topic: machine-learning-activities
syllabus_ref: CSM3201 Unit-II
status: draft
---
# Machine Learning Activities

## Overview

The syllabus uses “machine-learning activities” to describe the practical work involved in turning a data problem into a working model. Activities include understanding the problem, collecting and preparing data, exploring patterns, selecting a model, training it, evaluating it, improving it, and deploying it. They are related but distinct: an activity is work to be done, while an algorithm is one method used inside an activity.

A strong ML project makes each activity explicit. It documents the assumptions, records versions, and checks that the result addresses the original decision. Otherwise a team may spend weeks tuning a model that solves the wrong question.

## Explanation

### 1. Identify the task

Describe the desired output and the available information. Decide whether the task is classification, regression, clustering, anomaly detection, recommendation, ranking, or sequential decision-making. State the unit of analysis: a customer, transaction, image, time window, or device. A target can be a label, a continuous value, a probability, a ranking, or a policy.

### 2. Collect and understand data

Data collection may use surveys, sensors, transactions, logs, experiments, public datasets, or expert annotation. Create a data dictionary and provenance record. Ask:

- What does one row represent?
- When was each field recorded?
- Which population is represented?
- How were labels produced?
- Is consent and lawful use documented?
- Are duplicates, missing values, and outliers expected?

### 3. Explore and understand

Exploratory data analysis (EDA) uses summary statistics, distributions, plots, and domain questions to form hypotheses. Look at class balance, ranges, skew, missingness, correlations, unusual categories, time effects, and group differences. EDA is not just a preliminary screenshot; it determines which cleaning and modelling decisions are reasonable.

### 4. Prepare data

Cleaning may correct impossible values, remove duplicates, handle missing data, and resolve schema errors. Transformation may scale numbers, encode categories, tokenise text, resize images, or create time features. Feature engineering creates useful signals, while feature selection removes noise or cost. All transformations used for training must be reproducible and must not see future test information.

### 5. Select a model

Start with a baseline and consider the task, data volume, feature type, latency, interpretability, and error cost. Compare a simple linear or rule-based model with a tree, nearest-neighbour, support-vector, ensemble, or neural model. Select hyper-parameters using validation data or cross-validation, not the final test set.

### 6. Train and tune

Training estimates parameters by minimising a loss. Optimisation may be gradient descent, coordinate descent, closed-form solution, tree construction, expectation–maximisation, or another procedure. Monitor training and validation curves, control overfitting with regularisation or early stopping, and preserve the best validated state.

### 7. Evaluate

Choose metrics linked to the decision. For classification, report confusion-matrix counts, precision, recall, F1, ROC/PR analysis, and calibration where relevant. For regression, use MAE, RMSE, \(R^2\), and residual plots. Include uncertainty, subgroup results, and error analysis. A score without a split and preprocessing record is not reproducible evidence.

### 8. Improve and iterate

Improvement can come from better data, corrected labels, better features, a different objective, more capacity, stronger regularisation, calibration, thresholding, or a new algorithm. Use an experiment log and keep the evaluation protocol fixed. Do not change many things and attribute the result to one unexplained change.

### 9. Deploy and learn from outcomes

Package the model with its preprocessing and schema, monitor input and output quality, latency, errors, drift, and delayed outcomes, and provide a fallback. A feedback loop can generate new labels, but the feedback must not create a self-reinforcing bias.

### Iterative nature

The activities are not a one-way waterfall. Error analysis can send the team back to data collection. A new population can require a new target. Monitoring can reveal that the business objective changed. The important discipline is to record why a decision was made and which evidence supported it.

## Worked examples

### Example 1: activity sequence for a loan model

The team defines default risk and approval policy, checks whether application features are available at decision time, examines missing income documents, creates a chronological split, compares a baseline rate with logistic regression and gradient-boosted trees, evaluates subgroup errors, and sets a review threshold. It does not use the “loan was repaid” field that is only known after months because that would leak the answer.

### Example 2: activity sequence for text clustering

The team defines a document-segmentation goal, removes boilerplate, tokenises and normalises text, explores vocabulary and document lengths, compares TF–IDF with a small neural representation, tests stability, and gives clusters to subject-matter experts. It does not claim that a high silhouette score proves the clusters are useful topics.

### Example 3: iteration after an error

A demand model's validation error is high for holiday weeks. Error analysis reveals a missing promotion and holiday flag. The team obtains those features, checks that they are known before the forecast, retrains, and reports improvement on a later time split. The lesson is not “add more features”; it is “link an observed failure to a justified data change.”

### Example 4: deployment feedback

A fraud model is retrained monthly from confirmed cases. It keeps a model version, detects a change in transaction volume, and compares precision and recall when labels arrive. A sudden rise in flagged transactions triggers review rather than automatic deployment.

## Key terms & formulas

- **Task framing:** specifying output, population, time, and cost.
- **EDA:** exploratory data analysis.
- **Data dictionary:** definitions, types, units, and allowed values for fields.
- **Provenance:** origin and history of data.
- **Baseline:** simple reference model.
- **Training:** estimating parameters from learning data.
- **Tuning:** choosing hyper-parameters using validation evidence.
- **Evaluation:** measuring performance on representative unseen data.
- **Iteration:** returning to a previous activity after new evidence.
- **Experiment log:** record of data, code, parameters, and results.
- **Model artefact:** serialised model and preprocessing state.
- **Monitoring:** ongoing measurement after deployment.

## Common mistakes

1. **Confusing activity and algorithm.** Algorithms are tools used inside activities.
2. **Skipping problem framing.** A technically strong model can be irrelevant or harmful.
3. **Doing EDA only to make a presentation.** It should guide decisions and reveal data risks.
4. **Tuning repeatedly on the test set.** The reported performance becomes optimistic.
5. **Treating deployment as the end of the project.** Outcomes and drift must be monitored.
6. **Changing data and model simultaneously.** It becomes difficult to know what caused an improvement.

## Exam prep

### Likely 2-mark questions

- **What are the main ML activities?** Data understanding, preparation, modelling, evaluation, improvement, and deployment.
- **What is EDA?** Exploratory analysis of data to understand distributions, relationships, and problems.
- **Why maintain an experiment log?** To reproduce results and attribute changes.
- **What is a baseline?** A simple reference used to judge whether a model adds value.

### Long-answer prompts

- **Describe the activities involved in developing an ML model.** Explain their order, outputs, and iteration.
- **How do data preparation and model selection interact?** Use examples of scaling, encoding, feature leakage, and inductive bias.
- **Explain why evaluation is an activity rather than a final step.** Discuss validation, uncertainty, subgroup checks, and deployment feedback.
- **Prepare a project plan for a supervised classification problem.** Include target, data, baseline, preprocessing, candidates, metrics, and monitoring.
