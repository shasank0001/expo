---
subject: oose
unit: 3
topic: object-oriented-modeling-falsification-and-prototyping
syllabus_ref: CSM3102 Unit-III
status: draft
---
# Object-Oriented Modeling, Falsification, and Prototyping
## Overview
Object-oriented modeling represents a problem or solution through objects, classes, responsibilities, collaborations, and use cases. **Falsification** deliberately tests whether a model is wrong by trying to break it with counterexamples, edge cases, and alternative explanations. **Prototyping** creates a limited model or working example to explore uncertain behavior and obtain feedback. Together they turn a paper model into an assumption-testing activity.

A model is useful only if it helps someone make a better decision. The team therefore checks that the model matches real needs, remains consistent, and can lead to implementation and tests. A prototype can validate a workflow, but it must not be mistaken for a production product.

## Explanation
### 1. Object-oriented modeling
An object-oriented model identifies:
- domain objects and actors;
- responsibilities and services;
- attributes/state and allowable values;
- relationships and multiplicity;
- lifecycles, events, and messages;
- use cases and scenarios;
- constraints and design decisions.

The model should use the domain's language and keep the boundary between problem and solution clear. A `RoutePlanner` may be a domain service in analysis; a database table and REST controller are design choices. A useful model evolves from a sketch to a validated specification, not from code copied into a diagram.

### 2. Analysis and design models
The **analysis model** focuses on what the system must do for whom and on essential domain responsibilities. It avoids choosing a database, framework, or detailed algorithm. The **design model** refines the analysis model with architectural structures, interfaces, data management, error handling, user interaction, technology, and testability. The same object can have an analysis counterpart and a design implementation, but traceability prevents accidental loss.

### 3. Falsification
Falsification is a disciplined attempt to disprove a claim or model assumption. Instead of asking only “Does the normal case work?” ask:
- What evidence would show this model is wrong?
- Can a valid user goal be expressed with the current concepts?
- What happens at boundaries, failures, concurrency, and recovery?
- Can two stakeholders interpret a relationship differently?
- Is a promised invariant actually preserved?
- Does the model scale to realistic volume, security, and change?
- Can the proposed service operate when an external system is unavailable?

The result may be a corrected requirement, a missing class, a changed multiplicity, a new state, a rejected design assumption, or a decision to gather more evidence.

### 4. Falsification techniques
- **Scenario walkthrough:** use real and adversarial stories.
- **Boundary and negative testing:** zero, maximum, missing, duplicate, expired, and malicious values.
- **Model consistency checks:** compare class diagrams, states, use cases, and sequences.
- **Prototype experiments:** test the uncertain behavior, not just the appearance.
- **Domain-expert review:** ask experts to explain exceptions and counterexamples.
- **Paper simulation:** walk a process with fake actors and data to expose missing steps.
- **Data profiling:** inspect real volume, distributions, and quality assumptions.
- **Architecture stress test:** test failure, load, security, and deployment assumptions.

### 5. Prototyping
A **prototype** is a simplified or experimental representation used to answer a question. It can be a paper sketch, storyboard, screen mock-up, data model, executable slice, or hardware demonstration. Good prototyping begins with a purpose:
- explore user workflow and usability;
- validate a technical approach or performance assumption;
- test an interface or data representation;
- obtain stakeholder feedback;
- measure feasibility before a full investment.

The prototype's fidelity should match the question. A low-fidelity sketch is enough to discuss navigation; a performance prototype is needed to measure routing under real data volume.

### 6. Throwaway versus evolutionary prototypes
A **throwaway prototype** is discarded after learning. It is appropriate for comparing user flows or tool choices. An **evolutionary prototype** is refined into a production implementation; it needs a quality baseline, security, testing, maintainability, and configuration control. Do not let a quick prototype become production merely because users like it.

### 7. Prototype validity and limitations
A prototype demonstrates only what it includes. A successful screen does not prove a secure backend; a fast data demo does not prove scale; a paper process does not prove concurrency or recovery. State the assumptions, data, environment, and validity limits. A feedback session should collect evidence tied to a question, not just “looks good.”

### 8. From model to validated requirement
For each important model element, record:
- the source need and scenario;
- the behavior/constraint represented;
- a prototype or falsification experiment;
- the result and evidence;
- the change made or remaining risk.

This record creates traceability from a stakeholder conversation to a class, state, test, and release decision.

## Worked examples
### Example 1: Falsifying a chat model
The model says a `Conversation` has exactly one owner. A stakeholder says a group can have two supervisors. Falsifying the multiplicity with that scenario changes the association to zero-or-many managers and adds a role model. The prototype then tests assigning and removing a manager. The model is improved because a counterexample was found.

### Example 2: GPS performance prototype
The model assumes a route can be calculated from two coordinates. A field trip reveals that route calculation needs a downloaded map, GPS updates, and traffic data. A small performance prototype measures a large region on the target device. The team adds offline/route-state requirements and changes the architecture; the original assumption was falsified.

### Example 3: WMITS paper simulation
Give paper forms to the analyst and role-play an inspector submitting a violation while a supervisor is absent. The simulation reveals that the form has no way to record a returned reason. The domain model adds `ReturnReason` and a `Returned` state. This is cheaper than building the screen and discovering the problem after deployment.

### Example 4: Throwaway prototype
A team tries two map libraries in a small program. It measures startup time, memory, and route quality, records the results, and removes the test program. The chosen library is then integrated through a normal interface. The prototype was an experiment, not a hidden production dependency.

## Key terms & formulas
- **Object-oriented model:** a representation using objects/classes, responsibilities, relationships, and interactions.
- **Analysis model:** problem- and user-focused model.
- **Design model:** solution-focused refinement with technical structures and interfaces.
- **Falsification:** an attempt to disprove an assumption or model using counterexamples.
- **Counterexample:** a valid scenario that violates a claimed rule or exposes a model gap.
- **Prototype:** limited representation used to learn or validate an assumption.
- **Fidelity:** how closely a prototype resembles the real product in relevant dimensions.
- **Throwaway prototype:** prototype discarded after learning.
- **Evolutionary prototype:** prototype developed into the real system.
- **Model validity:** the extent to which a model accurately serves its intended purpose for its users and decisions.
- **Prototype goal (test statement):** question + environment + data + success criterion; use this before building.

## Common mistakes
- Treating modeling as drawing attractive class diagrams without source evidence.
- Calling a prototype a model of every nonfunctional property.
- Using only happy-path scenarios as “validation.”
- Failing to distinguish throwaway and evolutionary prototypes.
- Letting feedback become personal preference rather than evidence tied to a question.
- Removing a valid counterexample because it does not fit the current design.
- Building a production system from a prototype without security, test, and maintenance work.

## Exam prep
### Likely 2-mark questions
1. **Define falsification in modeling.** A deliberate attempt to find evidence that a model or assumption is wrong using counterexamples and edge scenarios.
2. **Differentiate analysis and design models.** Analysis describes the problem and essential behavior; design specifies the technical solution.
3. **What is prototyping?** Building a limited model or implementation to explore, demonstrate, or validate a requirement or assumption.
4. **Differentiate throwaway and evolutionary prototypes.** Throwaway is discarded; evolutionary becomes or informs the product.
5. **Give one falsification technique.** Boundary/negative test, scenario walkthrough, prototype experiment, expert review, consistency check, or data profiling.
6. **What is a counterexample?** A legitimate scenario that contradicts a claimed rule, invariant, or model assumption.

### Long-answer answer hints
- “Explain object-oriented modeling, falsification, and prototyping”: define each, show the cycle, explain analysis/design separation, and give a case study.
- “How can a model be falsified?” list counterexamples, expert review, boundary tests, consistency checks, prototypes, and the resulting changes.
- “When is a prototype useful?” state the uncertainty, choose fidelity, define success evidence, pilot with users, and document limits.
- “Compare throwaway and evolutionary prototypes”: purpose, code reuse, quality effort, risk, and maintenance.
- “Why is prototyping not testing?” prototypes can answer selected questions, but they do not replace requirements validation or systematic testing.

### Cycle sketch
```text
Model → ask what could disprove it → counterexample/prototype → evidence
     → revise requirement/model → design and verification
```
