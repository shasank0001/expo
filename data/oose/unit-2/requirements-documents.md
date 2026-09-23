---
subject: oose
unit: 2
topic: requirements-documents
syllabus_ref: CSM3102 Unit-II
status: draft
---
# Requirements Documents
## Overview
A requirements document is a controlled, audience-appropriate description of a product's required behavior, qualities, interfaces, data, constraints, and acceptance conditions. It is a communication and verification tool, not an end in itself. The right amount of detail depends on stakeholders, project risk, regulatory needs, and the team's process.

Common artifacts include a software requirements specification (SRS), use-case descriptions, user stories with acceptance criteria, a requirements traceability matrix, a glossary, interface specifications, and a prototype or model. A good document set makes decisions searchable, links each requirement to its source and test, and records open issues instead of hiding uncertainty.

## Explanation
### 1. Purpose of requirements documentation
Documentation supports:
- a shared understanding among customer, analyst, architect, developer, tester, and manager;
- scope and contract negotiation;
- planning, estimating, and prioritization;
- design and test derivation;
- review, validation, and change impact analysis;
- training, operation, maintenance, and audit;
- historical traceability of why a requirement exists.

A document is valuable when it answers questions quickly. A long document that is hard to navigate or lacks IDs and priorities can be less useful than a concise, well-linked set.

### 2. Software Requirements Specification
A typical SRS contains:
1. **Introduction:** purpose, product perspective, definitions, and references.
2. **Overall description:** users, environment, assumptions, constraints, and external interfaces.
3. **Product functions:** functional requirements, use cases, and business rules.
4. **Nonfunctional requirements:** performance, security, usability, reliability, maintainability, and other criteria.
5. **External interface requirements:** hardware, software, communications, and data formats.
6. **Data requirements:** entities, identifiers, validation, retention, and migration.
7. **Operational and transition requirements:** deployment, support, training, and cutover.
8. **Acceptance criteria and traceability links.**
9. **Glossary, open issues, and change history.**

The structure can vary. A small project may combine these sections; a safety-critical or contractual system may need separate controlled documents.

### 3. Use-case documents
For each use case, record:
- use-case ID and name;
- primary and secondary actors;
- goal and scope;
- preconditions and postconditions;
- triggering event;
- main success flow;
- alternate and exception flows;
- business rules and data;
- related requirements and tests.

The use case describes user-visible behavior, not the code's private method sequence.

### 4. User stories and acceptance criteria
A user story is intentionally small and is not a complete specification. A useful bundle is:
```text
Story ID: US-17
As an inspection supervisor, I want to return an incomplete inspection
so that the inspector can correct it before approval.

Acceptance:
1. Given the supervisor is assigned, when Return is selected,
   then a reason is required and the state becomes Returned.
2. The action is denied for an unassigned user and recorded as denied.
```
The story is valuable when kept with business rules, interface requirements, and tests.

### 5. Traceability matrix
A traceability matrix links requirements to:
- stakeholder/source or business objective;
- use case and scenario;
- design element and implementation component;
- unit, integration, system, or acceptance test;
- defects and change requests.

It answers “Where is this requirement implemented?”, “How do we know it is tested?”, and “What is affected by this change?” A matrix need not contain every implementation detail, but it should be maintained at an appropriate level.

### 6. Models, prototypes, and diagrams
Models make complex relationships precise: a context diagram, domain model, state machine, sequence diagram, data schema, or decision table. A prototype is useful for validating interaction, but its purpose and limits should be recorded. Diagrams are requirements aids; they are not automatically specifications unless their semantics and authority are stated.

### 7. Tailoring and standards
Document depth depends on risk, size, audience, and regulatory context. A student prototype may need a short vision, backlog, and acceptance criteria. A safety system needs detailed traceability, configuration control, and independent review. A contract may require a formal baseline and signature. Consistency in IDs, terminology, and status is more important than copying a template.

### 8. Document quality
A good document is:
- **correct:** technically and semantically sound;
- **complete for scope:** includes functions, quality, interfaces, errors, and constraints;
- **consistent:** no contradictions or unexplained terms;
- **unambiguous:** one clear interpretation;
- **verifiable:** acceptance conditions can be tested or reviewed;
- **traceable:** source, owner, version, and related artifacts are known;
- **maintainable:** change history and open issues are visible.

## Worked examples
### Example 1: SRS entry
`NFR-PERF-04: Under the agreed 500-user workload and test network, 95% of accepted route requests shall produce a response within 2 seconds.` This is more useful than “navigation must be fast.” It identifies scope, workload, measure, and threshold.

### Example 2: Use case
For ATM withdrawal, the main flow is insert card, authenticate, select withdrawal, check account/limits, dispense cash, print receipt, and update balance. An alternate flow handles insufficient funds; an exception flow handles a machine failure. These flows become state and integration test cases.

### Example 3: Traceability
`FR-INSP-07: only an assigned supervisor may approve an inspection` links to UC-06, class `InspectionService`, method `approve`, tests TC-INSP-07-01/02, and CR-014. When roles change, the matrix identifies all affected work.

### Example 4: Tailoring
A GPS student project may use user stories, a context diagram, and a testable backlog. A WMITS project facing legal audit adds a formal SRS, state model, data dictionary, and signed requirement baseline. Both documents can be valid; they are tailored to risk.

## Key terms & formulas
- **SRS:** Software Requirements Specification; controlled description of required system behavior and qualities.
- **Use case:** structured description of a user goal and flows.
- **User story:** concise user-centered need with acceptance criteria.
- **Traceability matrix:** cross-reference table among requirements, design, implementation, tests, and changes.
- **Requirement ID:** stable identifier used in reviews, tests, and change control.
- **Glossary:** controlled definitions of domain and technical terms.
- **Baseline:** approved version of a requirements document or set.
- **Document completeness:** covered applicable topics ÷ expected topics × 100%; completeness also requires quality, not just headings.
- **Traceability coverage:** requirements with at least one linked test and design artifact ÷ applicable requirements × 100%.

## Common mistakes
- Copying a large template without tailoring it to risk and audience.
- Writing only function lists and omitting quality, interfaces, data, and errors.
- Giving a use case only a happy path.
- Using diagrams as decoration without IDs, semantics, or links.
- Calling a document final while open questions and conflicts remain.
- Failing to record version, author, reviewer, approval, and change history.
- Treating a prototype screenshot as a complete requirement.

## Exam prep
### Likely 2-mark questions
1. **What is an SRS?** A controlled specification of a system's required functions, qualities, interfaces, constraints, and acceptance conditions.
2. **List six SRS sections.** Introduction, overall description, functions, nonfunctional requirements, interfaces, data/operational requirements, or traceability.
3. **What is a traceability matrix?** A table linking requirements to sources, design, code, tests, and changes.
4. **Why tailor a requirements document?** Different project size, risk, audience, and regulation need different detail and control.
5. **Differentiate a use case and user story.** A use case gives complete flows and rules; a user story gives a concise need with acceptance criteria.
6. **State two document-quality properties.** Clear, complete, consistent, testable, traceable, or maintainable—any two.

### Long-answer answer hints
- “Explain requirements documents”: purpose, SRS contents, use cases/stories, traceability, tailoring, and quality.
- “Design a requirements document for WMITS”: sections, IDs, functional/nonfunctional examples, security/data/migration, and traceability.
- “Why is traceability important?” locate implementation and tests, assess change impact, measure coverage, and preserve rationale.
- “Compare SRS, prototype, and user story”: precision, feedback value, and concision; explain how they work together.
- “How do you review a requirements document?” check structure, semantics, consistency, feasibility, testability, coverage, sources, and open issues.

### Quick document rule
If a reader cannot tell **what**, **why**, **who**, **when**, **what quality**, **how it is checked**, and **where it came from**, the document is not yet study-ready.
