---
subject: oose
unit: 2
topic: requirements-analysis-techniques
syllabus_ref: CSM3102 Unit-II
status: draft
---
# Requirements Analysis Techniques
## Overview
Requirements analysis turns gathered information into an organized, consistent, prioritized, and testable model of what the system must provide. It separates needs from solutions, finds conflicts and omissions, models normal and exceptional behavior, and establishes a baseline for design and testing.

Analysis is a thinking and modeling activity. The team may use use cases, user stories, domain models, state machines, decision tables, prototypes, data models, and prioritization methods. The output is not one drawing; it is a connected set of requirements and rules whose meaning has been checked with stakeholders.

## Explanation
### 1. Analyze the problem, not just the requests
Start from the problem definition, scope, stakeholder goals, domain glossary, and evidence. Ask whether a request solves the right problem, whether it is necessary, and what happens if it is absent. Avoid choosing a database, framework, or screen before the behavior and constraints are understood.

### 2. Use cases and user stories
A **use case** models a complete user goal, actors, preconditions, main flow, alternate flows, exceptions, postconditions, and business rules. It is useful for functional scope and scenario testing. A **user story** is a compact statement such as “As an inspector, I want to attach evidence so that a case can be reviewed.” It normally needs acceptance criteria. User stories are not requirements by themselves; they need detail and integration with business rules.

### 3. Context and domain modeling
A context diagram shows the system boundary and external actors/systems. A domain model shows important concepts, relationships, responsibilities, and invariants without committing to a database. These models expose missing concepts and terminology inconsistencies. Use nouns for candidate entities, verbs for candidate behavior, and validate the result with domain experts.

### 4. State modeling
Some requirements concern how an entity changes over its lifecycle. A state machine identifies states, events, guards, actions, entry/exit behavior, and illegal transitions. For example:
```text
Draft → Submitted → UnderReview → Approved
                         └──────→ Returned ──→ Draft
```
It reveals requirements such as “only a returned inspection may be edited” and makes invalid cases testable.

### 5. Decision tables and rules
A decision table is useful when several conditions select among several actions. Define conditions, combinations, actions, and whether a combination is allowed, forbidden, or an error. This is more precise than a paragraph when permissions, eligibility, pricing, or validation depend on several inputs.

Example: inspection closure decision:

| Evidence present? | Supervisor assigned? | Action |
|---|---|---|
| No | Any | Block closure; show missing evidence |
| Yes | No | Block closure; assign supervisor |
| Yes | Yes | Allow closure and record audit entry |

Decision tables are analysis artifacts, not necessarily user-interface layouts. They should be reviewed with the rule owner and linked to tests.

### 6. Data and interface analysis
Identify entities, attributes, relationships, identifiers, allowed values, units, and lifecycle. Analyze external interfaces and data flows: input, processing, output, errors, timing, security, and ownership. Check whether data can be validated and whether the source has the quality needed. For a migration, analyze volume, duplicates, missing values, formats, and mapping.

### 7. Prioritization and feasibility
Use value, risk, dependencies, effort, urgency, and stakeholder influence. Techniques include MoSCoW, ranking, weighted scoring, and pairwise comparison. Analyze feasibility technically, economically, operationally, and schedule-wise. A high-value request may still be deferred if it violates a regulation or depends on an unavailable map service.

### 8. Conflict resolution and negotiation
When sources disagree, record both statements, identify the policy owner, determine the impact of each choice, and obtain a decision. Do not average incompatible requirements. Use workshops for shared understanding and a decision log for traceability. Separate the decision from the resulting requirement.

### 9. Prototyping and validation
A prototype can validate a misunderstood workflow, screen, data concept, or response time. Define what the prototype will test, who will review it, and what evidence will lead to a change. It is not automatically production code. Pair it with a walkthrough and acceptance criteria.

### 10. Analysis outputs and quality checks
Outputs may include a prioritized requirements list, use cases, domain and state models, decision tables, interface specifications, data definitions, and an assumptions/open-issues log. Check each candidate for clarity, consistency, completeness, feasibility, testability, necessity, and traceability. The team should revise the problem and scope when analysis reveals a fundamental mismatch.

## Worked examples
### Example 1: GPS routing analysis
Stakeholders ask for “the fastest route.” Analysis finds that they mean different things: shortest distance, shortest driving time, or least fuel. The team defines route modes, map freshness, traffic availability, and response time. A state model handles offline and rerouting cases. The final requirement is precise and testable.

### Example 2: WMITS inspection lifecycle
Observation shows inspections can be saved as drafts, submitted, returned, approved, or escalated. A state model records which transitions require an assigned supervisor. A decision table checks evidence and permissions. A prototype lets inspectors confirm that “returned” clearly means they can edit the record.

### Example 3: Conflict
A registrar says results must be public immediately; privacy policy says some results are embargoed. The analyst models an embargo state and asks the policy owner to approve the rule. The design later enforces the state, and tests cover both normal and embargoed dates.

### Example 4: Prioritization with dependencies
A proposed offline mode is “should have” but the target field team cannot use the product without it. The team makes a minimal offline requirement “must have” for the pilot, while full map downloads remain a later option. The dependency is recorded, not hidden in a priority score.

## Key terms & formulas
- **Analysis:** transforming gathered information into an agreed, testable model.
- **Use case:** a complete user goal with actors, flows, rules, and exceptions.
- **User story:** a concise user-centered need with acceptance criteria.
- **Context diagram:** system and its external actors/interfaces.
- **Domain model:** implementation-independent concepts and relationships.
- **State machine:** states and event-triggered transitions.
- **Decision table:** conditions and actions arranged to express business rules.
- **Data-flow analysis:** movement, transformation, storage, and boundaries of information.
- **Prioritization:** ordering requirements by value, risk, dependencies, effort, or urgency.
- **Weighted score (simple):** score_i = Σ(weight_j × rating_ij); weights and ratings must be agreed and transparent.
- **Coverage:** analyzed/traceable requirements ÷ identified requirements × 100%; unresolved items remain visible.

## Common mistakes
- Using a use case only as a list of screens and forgetting alternate/exception flows.
- Drawing a state machine with states but no events, guards, or postconditions.
- Replacing detailed business rules with a vague sentence.
- Prioritizing before resolving hard conflicts and dependencies.
- Choosing a technical solution during analysis because it is familiar.
- Treating a prototype click-through as proof of all requirements.
- Calling every candidate an approved requirement; “proposed,” “open,” and “deferred” are meaningful statuses.

## Exam prep
### Likely 2-mark questions
1. **What is requirements analysis?** The process of organizing, refining, prioritizing, and validating gathered needs into a testable model.
2. **What are the parts of a use case?** Actor, goal, precondition, main flow, alternate/exception flows, postcondition, and rules.
3. **When is a decision table useful?** When combinations of conditions determine actions or permissions.
4. **What does a state machine add?** It specifies states, events, guards, and valid transitions over time.
5. **Name two prioritization methods.** MoSCoW, weighted scoring, ranking, or pairwise comparison.
6. **How is a requirement conflict resolved?** Record both sources, identify the decision owner, assess impact, and obtain an explicit decision.

### Long-answer answer hints
- “Explain requirements analysis techniques”: use cases, domain/context modeling, state modeling, decision tables, data/interface analysis, prioritization, and prototyping.
- “Construct a use case for withdrawing cash”: actor, precondition, main flow, PIN failure, insufficient balance, machine failure, postconditions, and business rules.
- “Draw and explain a state model for an inspection”: list states, events, guards, actions, and invalid transitions.
- “How do you prioritize a large backlog?” value, risk, dependency, effort, urgency, stakeholder agreement, and re-evaluation.
- “Differentiate validation from analysis”: analysis structures and resolves needs; validation checks with stakeholders and evidence that the result is correct and complete.

### Sketch to reproduce
```text
Need → use case/domain model → rules/state/interface analysis
     → prototype/validation → prioritized, testable requirements
```
