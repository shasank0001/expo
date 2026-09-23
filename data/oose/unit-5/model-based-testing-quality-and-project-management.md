---
subject: oose
unit: 5
topic: model-based-testing-quality-and-project-management
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Model-Based Testing, Software Quality, and Project Management
## Overview
Model-based testing (MBT) derives and selects tests from a model of requirements, states, workflows, or data. A model makes expected behavior explicit and can generate combinations and paths that are difficult to imagine manually. The model must be reviewed and maintained like production code; otherwise tests can confidently encode a wrong assumption.

The syllabus also places software quality, quality attributes and criteria, and an introduction to software project management in this unit. Quality is the degree to which a product satisfies stated needs and is fit for use. Project management coordinates scope, people, time, cost, quality, risk, and change so the product can be delivered and maintained. This note connects the three topics: a good project plans quality into the product, and MBT is one way to obtain objective evidence.

## Explanation
### 1. Model-based testing
#### Definition and purpose
MBT uses an executable or formal model of system behavior to derive test cases, test data, or expected results. Models may represent:
- state transitions and lifecycle rules;
- workflows and decision rules;
- use-case sequences and messages;
- data schemas and invariants;
- nondeterministic choices and timing;
- performance or resource models.

The goal is not to model every implementation detail. The model captures properties needed to generate meaningful tests and compare actual behavior with a specification or oracle.

#### Benefits
- makes hidden state, ordering, and exception behavior visible;
- generates systematic combinations and paths;
- supports requirements traceability and coverage measurement;
- can produce many tests quickly;
- separates behavior specification from test data;
- supports model checking, simulation, and mutation analysis;
- is useful for stateful, protocol, and safety-critical behavior.

#### Limitations and risks
- building the model costs time and requires domain knowledge;
- a model can be incomplete or wrong;
- generated tests may be infeasible or redundant;
- coverage of the model is not coverage of the real environment;
- nondeterminism, time, and external services complicate oracles;
- generated tests need review, prioritization, and maintenance;
- model/code drift can create false confidence.

#### MBT process
1. Define model scope, level of abstraction, and intended properties.
2. Build the model with stakeholders/domain experts.
3. Review model syntax, assumptions, guards, and transitions.
4. Derive test objectives and coverage criteria.
5. Generate test cases/data and feasibility-filter them.
6. Define an oracle: model expected result, invariant, or independent reference.
7. Execute against the real product and compare outcomes.
8. Minimize failing tests and diagnose model/product mismatch.
9. Measure model coverage, defects, and flaky behavior.
10. Version, change-control, and maintain the model with the product.

### 2. Types of models and test generation
#### State-machine model
A state model has states, events, guards, actions, and outputs. Generation targets include state, transition, path, and guard coverage. The model can reveal that a state is unreachable, a guard has no feasible test, or an event has inconsistent handling.

#### Workflow/use-case model
A workflow model represents steps, decisions, loops, optional paths, and exceptions. It generates end-to-end scenarios and helps test whether required preconditions and recovery paths are reachable.

#### Decision-table/model-based combinatorial model
Conditions and actions can be represented as rules. A model generator selects rule combinations, boundaries, and contradictory/missing conditions. This is related to equivalence partitioning and decision-table testing.

#### Data/property model
A property-based model describes relationships such as invariants, algebraic laws, or allowed values. Tests generate data and check the property with an independent oracle. Examples include `sum(x + y) = x + sum(y)` or a balance that cannot become negative without authorization.

#### Executable specifications and model checking
An executable model can be run like software; a model checker explores states for a property such as “the lock state is never entered after three failures.” Model checking is valuable for finite or bounded state systems but can face state explosion for large concurrent systems.

### 3. Model coverage and test adequacy
Model-based coverage may include:
- state coverage;
- transition and path coverage;
- branch/guard coverage;
- rule/condition coverage;
- model-state and data-constraint coverage;
- mutation score of the model or implementation;
- property/violation coverage.

**Model coverage** is the proportion of model elements exercised. It is not the same as implementation coverage or requirements coverage. A report should state model version, generator/seed, environment, selected properties, and whether generated cases were executed, minimized, skipped, or infeasible.

An **oracle** can be:
- the model's expected output;
- a mathematically independent calculation;
- an invariant/property;
- a reference implementation or trace;
- a human-approved outcome for acceptance.

Avoid using the same faulty algorithm for both model and product when the goal is independent verification. If no strong oracle exists, combine model checks with targeted black-box and exploratory tests.

### 4. MBT example: inspection workflow
Model states:
```text
Draft → Submitted → UnderReview → Approved
                 └→ Returned → Submitted
                 └→ Rejected (policy permits)
```
Guards require evidence for closure and an assigned supervisor. MBT generates:
- valid submit/approve path;
- submit without evidence;
- return with and without a reason;
- approve while unassigned;
- repeated submit/return;
- invalid event in Approved;
- cancellation and recovery paths.

The model is reviewed with inspectors and policy owners. A failure in a generated case is triaged: model defect, implementation defect, test-data defect, or environment failure. The fix and model change are recorded.

### 5. Software quality
Software quality is the degree to which a product conforms to requirements and is fit for its intended use. It is not a vague feeling of professionalism. It must be expressed as quality characteristics and measured against criteria for a defined user, task, environment, and workload.

#### Quality characteristics
- **Correctness:** required functions and results.
- **Reliability:** consistent operation and recovery under expected conditions.
- **Usability:** learnability, efficiency, accessibility, and error recovery.
- **Efficiency:** CPU, memory, I/O, network, energy, and storage use.
- **Maintainability:** effort/risk to change, diagnose, and extend.
- **Portability:** ability to run in different supported environments.
- **Reusability:** safe use in another product or context.
- **Interoperability:** meaningful exchange with other systems.
- **Security:** confidentiality, integrity, availability, authentication, authorization, and audit.
- **Scalability/availability:** behavior under growth, load, failure, and recovery.
- **Testability/observability:** ability to exercise behavior and diagnose it.

These characteristics can conflict. A cache improves performance but may reduce freshness; strict logging improves auditability but increases storage and privacy risk; more layers improve maintainability but add latency.

### 6. Quality attributes and criteria
A **quality attribute** is a broad property; a **criterion** is a measurable target; a **metric** is the observed value. Examples:

| Attribute | Criterion/metric example |
|---|---|
| Performance | 95% of valid route requests complete within 2 seconds at 500 concurrent users |
| Reliability | fewer than 0.1% of scheduled transactions require manual recovery |
| Usability | 90% of representative users submit an inspection without facilitator help in under 3 minutes |
| Security | no unauthorized mark update succeeds; all denied attempts are audited |
| Maintainability | a representative rule change touches no more than 3 components and is covered by regression tests |
| Availability | service is available at least 99.5% during the monthly window, excluding planned maintenance |

A criterion must include workload, environment, measurement method, and time period. “Fast,” “secure,” “easy,” and “robust” are not criteria until operationally defined.

### 7. Quality assurance and quality control
- **Quality assurance (QA):** planned process activities that prevent defects and improve capability—standards, training, process audits, reviews, root-cause analysis, and prevention.
- **Quality control (QC):** inspection and testing of products—reviews, tests, measurements, inspections, and defect detection.
Quality is built through requirements, design, implementation, testing, deployment, and maintenance. Final testing cannot compensate for a weak architecture or ambiguous requirements.

### 8. Software project management
Software project management plans, organizes, measures, and controls the people and work needed to deliver a product. It balances:
- **scope:** what is included;
- **schedule:** when work will occur;
- **cost:** resources and budget;
- **quality:** required characteristics and acceptance;
- **resources:** people, tools, equipment, and time;
- **risk:** uncertainty and response;
- **communication:** stakeholder alignment;
- **change:** controlled adaptation.

#### Project life-cycle activities
1. **Initiation/feasibility:** need, objectives, stakeholders, business case, constraints, and go/no-go.
2. **Planning:** WBS, estimates, schedule, resources, communication, risk, quality, configuration, and change plans.
3. **Requirements/analysis:** elicit, analyze, specify, validate, and baseline needs.
4. **Design/implementation:** architecture, detailed design, coding, integration, and build.
5. **Testing and release:** verification, validation, deployment, training, and acceptance.
6. **Maintenance/closure:** defects, improvements, monitoring, handover, and lessons learned.

#### Estimation
- **Effort:** person-hours/days/months of work.
- **Cost:** effort rate × effort plus tools, cloud, licenses, training, and contingency.
- **Schedule:** activities, dependencies, durations, milestones, and capacity.
- **Three-point estimate:** `E = (O + 4M + P) / 6`, where `O` is optimistic, `M` most likely, and `P` pessimistic. This is PERT's weighted mean; the spread still represents uncertainty.
- **Function points/analogies:** use size and past projects for rough estimates, then adjust for complexity, risk, and team skill.
Estimate review, testing, rework, migration, and maintenance—not only coding.

#### Risk management
Identify risks, assess probability/impact, assign owners, choose responses (avoid, reduce, transfer, accept), and monitor. Risks include unclear requirements, technology failure, security threats, staff turnover, schedule dependency, data quality, and external-service outage. A risk register is updated at milestones.

#### Stakeholders and communication
Identify users, sponsors, customers, domain experts, developers, operations, legal/security, and suppliers. Use a communication plan: what information, who needs it, how often, and in what format. Conflict is managed through explicit decisions, not informal pressure.

#### Change and configuration management
A baseline, change request, impact analysis, approval, implementation, verification, and communication protect the product. Configuration management identifies versions of requirements, code, models, tests, data, and documents. A project can be agile, sequential, or hybrid, but the control principles remain.

#### Metrics and reporting
Use balanced metrics:
- schedule variance: `earned/actual or planned − actual` (state the convention);
- effort variance: `actual effort − planned effort`;
- scope completion: completed accepted requirements ÷ planned requirements × 100%;
- defect escape rate;
- change failure rate;
- review effectiveness;
- test coverage and defect density;
- milestone and risk status.
Metrics support decisions; they must not encourage gaming, hidden defects, or excessive individual measurement.

#### Agile and traditional management
A plan-driven approach may emphasize detailed upfront sequence and approvals. An agile approach delivers increments with a prioritized backlog, short iterations, frequent review, and adaptation. Hybrid projects combine a stable architecture/compliance plan with iterative delivery. Choose based on uncertainty, risk, stakeholders, and contract—not fashion.

## Worked examples
### Example 1: MBT for chat delivery
A state model covers `Queued → Sending → Delivered`, `Sending → RetryPending → Delivered`, and `Failed`. MBT generates duplicate ACK, timeout, offline recipient, and maximum-retry cases. The oracle is a delivery ledger; the test checks exactly-once visible delivery or an explicitly stated at-least-once policy. A model mismatch is analyzed rather than ignored.

### Example 2: Quality criteria for WMITS
- Performance: 95% of submissions accepted within 2 seconds at 500 concurrent users.
- Security: only authorized roles can approve; denied attempts are audited.
- Usability: 90% of pilot inspectors complete a standard inspection in under 3 minutes.
- Recovery: a service restart loses no acknowledged inspection and sync resumes within 10 minutes.
These criteria are testable and linked to design decisions.

### Example 3: Estimate and schedule
A project estimates 40, 60, and 100 person-days optimistically, most likely, and pessimistically. `E = (40 + 4×60 + 100)/6 = 63.33` person-days. The project still adds review, integration, contingency, and external dependency time. A milestone plan reports scope and risk, not only hours.

### Example 4: Risk response
A map provider may be unavailable. The project assigns an owner, builds a file-based fallback, tests it, and defines a degraded-mode message. The risk score falls when the prototype and contingency are verified. If the provider is a hard requirement, the risk instead becomes a release blocker.

### Example 5: Change impact
A request adds live traffic. The manager assesses design, API, cost, security, test, training, and schedule impacts. The request is deferred in favor of an authorization defect, but remains in the backlog with the decision. The project baseline and communication plan are updated.

## Key terms & formulas
- **Model-based testing:** deriving tests/oracles from a validated system model.
- **Model:** simplified executable/formal description of behavior or properties.
- **Model oracle:** expected result derived from a model or independent property.
- **State/transition/rule coverage:** proportions of model elements exercised.
- **Property-based test:** generated data checked against a stated invariant/property.
- **Quality characteristic:** broad dimension such as reliability or maintainability.
- **Quality criterion:** measurable target for a characteristic.
- **Quality metric:** observed measurement.
- **QA:** planned prevention and process improvement.
- **QC:** product inspection/testing.
- **Project:** temporary effort with defined scope, deliverables, and end.
- **WBS:** work breakdown structure decomposing the project into manageable work packages.
- **PERT estimate:** `(O + 4M + P) / 6`.
- **Risk exposure:** qualitative or calculated `probability × impact`; define scale and units.
- **Schedule variance:** planned/earned value minus actual, depending on the chosen convention.
- **Scope completion:** accepted planned deliverables ÷ planned deliverables × 100%.
- **Change failure rate:** changes causing rework/rollback/incident ÷ total changes × 100%.
- **Residual risk:** risk remaining after controls and tests.

## Common mistakes
- Treating a model as executable truth without stakeholder review.
- Claiming model coverage proves implementation or requirements coverage.
- Generating every combination without feasibility, priority, or risk review.
- Writing “fast,” “secure,” or “user-friendly” without criteria.
- Confusing QA process work with QC product testing.
- Estimating only coding and omitting tests, review, migration, and maintenance.
- Using a single project metric to judge people or hide scope/quality trade-offs.
- Letting an informal change bypass impact analysis and configuration control.
- Assuming an agile project needs no documentation or a plan-driven project cannot adapt.

## Exam prep
### Likely 2-mark questions
1. **Define model-based testing.** Deriving test cases, data, or expected results from a validated model of requirements or behavior.
2. **Give two benefits and one risk of MBT.** Benefits: systematic combinations/path generation and state visibility; risk: model cost/error or combinatorial explosion.
3. **What is a quality criterion?** A measurable target for a quality attribute in a stated context.
4. **Differentiate QA and QC.** QA prevents/improves process; QC inspects/tests the product.
5. **What does a software project manager coordinate?** Scope, schedule, cost, quality, people, risk, communication, and change.
6. **State the PERT estimate formula.** `(O + 4M + P) / 6`.
7. **Name four project activities.** Initiation, planning, requirements, design/implementation, testing/release, maintenance/closure—any four.

### Long-answer answer hints
- “Explain MBT”: model types, process, oracle, coverage, benefits, limits, and an inspection/chat example.
- “Explain software quality and quality criteria”: characteristics, measurable criteria, QA/QC, trade-offs, and evidence.
- “Introduce software project management”: lifecycle, estimation, risk, stakeholders, change, metrics, traditional/agile/hybrid comparison.
- “How does quality drive project planning?” map quality attributes to design choices, tests, milestones, roles, and exit criteria.
- “Apply project management to WMITS”: scope, stakeholders, estimates, risks, change, quality metrics, release and maintenance.
- “Compare model coverage and requirements coverage”: model elements versus real stakeholder needs; both are needed.

### Quality and planning frame
```text
Need → requirement/criterion → design decision → test/evidence
     → defect/change → release metric → residual risk and improvement
```

### PERT example
For `O=30`, `M=50`, `P=90` days: `E=(30+200+90)/6=53.33` days. This is an expected estimate, not a guarantee; report the range and risk.
