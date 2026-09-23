---
subject: ml
unit: 1
topic: problems-not-suited-to-machine-learning
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Problems Not Suited to Machine Learning

## Overview

Machine learning is not the default answer to every problem. It is most useful when there is a meaningful task, representative data, a measurable objective, and enough feedback to learn. A problem may be better handled by exact rules, optimisation, simulation, human expertise, or a change to the process.

Recognising unsuitable cases is an important engineering skill. Building a model when the assumptions fail can waste time, create false confidence, and cause harm. The aim is not to reject ML everywhere; it is to match the method to the structure and consequences of the problem.

## Explanation

### 1. Problems with simple, exact rules

If the rules are known, stable, and auditable, a rule-based system is often better. Tax calculations, eligibility checks with explicit regulations, and a deterministic routing rule can be implemented directly. A model may match most cases but still be unacceptable if it misses an exception that must be handled exactly.

**Example:** a university rule says that students with a credit total of at least 120 are eligible. A direct predicate is clearer and easier to test than a classifier. A learned system would introduce unnecessary error and maintenance cost.

### 2. Tasks with insufficient or unrepresentative data

Learning cannot recover a reliable pattern from a handful of cases when the input space is complex. Lack of data is especially damaging for rare but important events: fraud, rare diseases, and equipment failure. A high score on common cases can hide failure on the cases that matter most.

Data can be plentiful but still inadequate if it is noisy, systematically biased, collected under a different environment, or labelled with a poor proxy. More data of the wrong kind does not guarantee learning.

### 3. Tasks where labels or feedback do not match the goal

A label is useful only if it represents the concept the system should learn. Predicting clicks does not guarantee satisfaction. A proxy can create **Goodhart's law**: once the proxy becomes the target, behaviour can optimise the measurement rather than the intended outcome. Credit ratings, employee productivity, and policing measures are examples where proxies require caution.

### 4. High-stakes decisions needing causal or normative reasoning

A predictive association such as “people with feature \(X\) have higher risk” does not establish that changing \(X\) will improve the outcome. Medical treatment, hiring, lending, and criminal justice may require causal evidence, rights, explanations, and human review. A high-performing predictor may still be the wrong tool for deciding what *should* be done.

### 5. Problems requiring guaranteed correctness

Some systems must never exceed a hard error bound, such as a safety interlock, a flight-control component, or a cryptographic protocol. Statistical models provide performance estimates, not absolute guarantees. For such cases use formal verification, safety cases, redundant sensors, rule-based safeguards, or a hybrid design.

### 6. Non-stationary or adversarial environments

If the environment changes faster than the model can be retrained, or an adversary can manipulate inputs, ordinary generalisation may fail. Spam filters face changing language; fraudsters adapt to detection systems; markets change because a model is deployed. Adaptive systems need monitoring, robust objectives, and a response plan.

### 7. Tasks with poor observability

If important state is hidden, the agent may learn the wrong decision from the available data. Partial observability is not automatically unsolvable, but it requires memory, recurrent models, belief states, or extra sensors. It becomes unsuitable when the required information is fundamentally unavailable or impossible to measure accurately.

### 8. Explanability, autonomy, and responsibility problems

A system may be unable to explain a decision to a patient, employee, judge, or regulator, even if its aggregate accuracy is high. If the system cannot be audited or challenged, it may not be acceptable. This is especially relevant when people have a right to know, contest, or appeal a decision.

### 9. Problems where a workflow change is better

Sometimes prediction is the wrong lever. If queues are long, adding staff or redesigning the process may help more than predicting demand. If a product is defective, improving materials or testing may be more reliable than predicting which defective units will be detected. ML should solve the right problem, not merely a measurable symptom.

### 10. ML is inappropriate as a substitute for ethics or policy

An algorithm can reproduce historical inequalities. A system that allocates fewer opportunities to a group is not made fair simply because it maximises overall accuracy. Decisions about acceptable error rates, privacy, consent, and recourse are human and institutional choices.

## Worked examples

### Example 1: tax rules

A tax formula is explicitly published and changes rarely. Software can calculate it with exact rules, test edge cases, and provide an audit trail. A regression model may predict close to the formula but offers no reason to prefer it.

### Example 2: rare disease

A hospital has 20 positive cases and thousands of negative cases. A model may achieve 99.9% accuracy by predicting negative every time while missing every positive case. Without representative labels, uncertainty bounds, or a human diagnostic process, deployment is not justified.

### Example 3: hiring

A historical hiring classifier may reproduce the pattern of past biased decisions. Its feature correlations do not show which candidate will perform well or whether the process is fair. A fair, legally reviewed process and representative evaluation are required.

### Example 4: safety interlock

A neural network may predict a dangerous temperature well on average, but a mechanical or rule-based interlock can provide a hard stop. The latter is a better component for a guarantee that a human-independent safety rule is never violated.

## Key terms & formulas

- **Rule-based system:** an implementation of explicit, auditable if/then logic.
- **Representative data:** data whose distribution reflects deployment.
- **Data scarcity:** insufficient examples for stable estimation, especially in rare regions.
- **Proxy target:** a measurable stand-in for the true objective.
- **Goodhart's law:** a measure stops being a good target when it is optimised directly.
- **Causal inference:** reasoning about interventions and outcomes, not only associations.
- **Domain shift:** the input or target distribution changes between training and use.
- **Adversarial adaptation:** an opponent deliberately changes behaviour to defeat a detector.
- **Partial observability:** the true state cannot be seen directly.
- **Safety case:** documented evidence that a system meets required risk limits.
- **Algorithmic recourse:** a meaningful way for a person to understand or change an outcome.
- **Human-in-the-loop:** a person reviews, approves, or overrides an automated decision.

## Common mistakes

1. **Assuming every pattern is learnable.** Some relationships are unstable, too small, or not statistically identifiable.
2. **Assuming more data always helps.** Data from the wrong population can make bias worse.
3. **Ignoring the right-to-explain and contest decisions.** A score is not the only requirement.
4. **Treating a correlation as an intervention policy.** It may harm people when used causally.
5. **Using ML for an exact rule.** The model is harder to test and less transparent.
6. **Calling every difficult problem impossible.** A hybrid system or better data collection may make it feasible.
7. **Ignoring maintenance and drift.** A model unsuitable at deployment time is not suitable for production.

## Exam prep

### Likely 2-mark questions

- **Give one problem not suited to ML.** An exact deterministic rule, a data-scarce high-stakes task, or a causal decision without adequate evidence.
- **Why can a high-accuracy model still be unsuitable?** It may use leaked features, exploit a proxy, or perform poorly on important subgroups.
- **What is domain shift?** A change between the training and deployment data distributions.
- **What is a human-in-the-loop system?** A system in which a person reviews or approves important outputs.

### Long-answer prompts

- **Explain why some problems are not appropriate for machine learning.** Discuss exact rules, insufficient data, causal reasoning, guarantees, drift, explainability, and ethics.
- **Compare rule-based and ML solutions for a problem.** Choose a suitable example, state assumptions, evaluate accuracy, auditability, and maintenance.
- **A model achieves 99% accuracy in medical screening. Would you deploy it?** Analyse class imbalance, false negatives, distribution shift, calibration, human review, and regulatory requirements.
- **When is a hybrid system preferable?** Give an example combining rules, optimisation, statistical models, and human judgement.
