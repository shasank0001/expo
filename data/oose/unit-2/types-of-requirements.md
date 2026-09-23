---
subject: oose
unit: 2
topic: types-of-requirements
syllabus_ref: CSM3102 Unit-II
status: draft
---
# Types of Requirements
## Overview
Requirements describe different needs of the product and its stakeholders. Functional requirements say what the system must do; nonfunctional requirements say how well and under what constraints it must do it. Other categories classify needs by source, level, interface, security, data, and lifecycle. A good specification uses these categories to avoid missing needs and to resolve disagreement about the product.

Types are not mutually exclusive. A single statement can be a business rule, a functional requirement, and a security requirement. The type helps identify its source, priority, verification method, and owner.

## Explanation
### 1. Functional requirements
Functional requirements describe services, actions, calculations, responses, and state changes.
- “The system shall allow a registered student to view the current semester result.”
- “When a payment is confirmed, the system shall create a receipt and update the balance.”
- “The application shall calculate the total distance from route segments.”

A function should be observable, not just an internal method. “Use a queue” is usually a design decision; “accept up to 1,000 submissions without losing a valid request under the stated workload” is a behavior/quality requirement.

### 2. Nonfunctional requirements
Nonfunctional requirements describe quality attributes and constraints.
- **Performance:** response time, throughput, latency, resource use.
- **Availability/reliability:** uptime, fault tolerance, recovery, consistency.
- **Security/privacy:** authentication, authorization, confidentiality, integrity, audit, retention.
- **Usability/accessibility:** learnability, task completion, screen-reader support, clear errors.
- **Maintainability:** change effort, modularity, documentation, testability.
- **Portability:** supported platforms, environments, data formats.
- **Compatibility/interoperability:** APIs, protocols, browsers, devices, legacy systems.
- **Scalability:** users, volume, geographic or feature growth.
- **Safety/compliance:** required controls and audit behavior.

A category such as performance must include workload, environment, percentile or threshold, and measurement method. “System performance should be high” is incomplete.

### 3. Business and user requirements
A **business requirement** states an organizational outcome, policy, benefit, or constraint. “Reduce inspection turnaround from 48 hours to 12 hours” is a business objective. A **user requirement** states what a user needs to perform a task. “An inspector can capture a photo and submit it even with a weak connection” is a user need. These are translated into system and acceptance requirements.

### 4. System requirements
System requirements describe behavior and qualities of the complete product or a system element. They are more implementation-independent than a design specification but are written for engineering and verification. A system requirement may derive from a business rule, stakeholder need, regulation, interface, or quality strategy.

### 5. Domain and organizational requirements
**Domain requirements** capture domain vocabulary, rules, calculations, and invariants. **Organizational requirements** capture policies, procedures, budgets, contracts, legal rules, and internal standards. In WMITS, “a violation must have a legal category” is a domain requirement; “the report must use the ministry template” is organizational.

### 6. Interface requirements
Interfaces define how the system interacts with users, devices, networks, databases, APIs, messages, or other systems. Specify:
- who or what is at each side;
- data format, units, and required fields;
- sequence, timing, and frequency;
- errors, timeouts, and retries;
- authentication and authorization;
- compatibility and version policy.

### 7. Data and information requirements
These specify which data must be stored, its meaning, format, source, owner, quality, retention, privacy, and movement. They may include schemas, identifiers, validation rules, migration, archival, and audit history. A field called `status` is not fully specified until its allowed values and transitions are known.

### 8. Security and privacy requirements
Security requirements should be threat-informed:
- identify actors and assets;
- state authentication, authorization, confidentiality, integrity, and availability needs;
- include logging, retention, breach response, and lawful use;
- include abuse, misuse, and negative tests.

“Use encryption” is not a complete security requirement unless the data, threat, strength, key handling, and verification conditions are stated.

### 9. Constraint and transition requirements
A **constraint requirement** limits solution choices, such as a required operating system, approved database, response deadline, or legal accessibility standard. **Transition requirements** cover migration, training, cutover, coexistence, data conversion, and retirement. They are often omitted because they are not visible in the product screens, but they determine whether the product can actually be adopted.

### 10. Product and release requirements
A product requirement may be combined with a release constraint: “Version 1 shall support Android 13 and Android 14,” or “offline mode is excluded from Release 1.” Release requirements clarify what users can expect now versus later.

## Worked examples
### Example 1: Navigation requirements
Functional: “The system shall calculate a route between two valid coordinates.”
Nonfunctional: “For a 1,000-route test set on the target phone, 95% of responses shall complete within two seconds.”
Interface: “The route service shall return distance in metres and an ISO-8601 timestamp.”
Business: “The pilot shall reduce average route-planning time by 30%.”

### Example 2: WMITS
Domain: “An inspection with status `closed` shall have required evidence.”
Functional: “A supervisor shall be able to approve or return an inspection.”
Security: “Only an assigned supervisor may change status; the old and new values shall be recorded.”
Data: “Evidence photos shall be retained for the policy period and protected by role-based access.”

### Example 3: User versus design
“The user shall be able to find an inspection by date and site” is a user requirement. “The system shall provide a SQL query with an indexed date column” is a design choice. The first can be met through several interfaces and data designs.

### Example 4: Transition
A legacy register contains 20 years of paper records. The release requirement includes scanning a selected subset, validating names and dates, recording provenance, and making a reconciliation report. This is a transition requirement, not an optional user feature.

## Key terms & formulas
- **Functional:** what the product does.
- **Nonfunctional:** how well and under what constraints.
- **Business requirement:** organizational outcome or policy.
- **User requirement:** a task or need from a user perspective.
- **System requirement:** required complete-system behavior or quality.
- **Domain requirement:** domain rule or vocabulary.
- **Interface requirement:** contract for interaction with an external party/component.
- **Data requirement:** information, format, quality, ownership, and lifecycle.
- **Security requirement:** protection and evidence for assets and threats.
- **Constraint:** permitted boundary or mandated choice.
- **Transition requirement:** migration, training, cutover, or retirement work.
- **Requirement category count:** a requirement may be counted in several categories; do not add categories as if they were independent requirements.

## Common mistakes
- Treating functional and nonfunctional requirements as completely separate products rather than complementary views.
- Giving only the happy-path function and omitting quality, errors, privacy, and recovery.
- Calling a proposed tool or database “a user requirement.”
- Using “fast,” “secure,” or “easy” without context and measure.
- Confusing an interface contract with a screen design.
- Forgetting data migration and operational requirements.
- Assuming one stakeholder’s category is the only legitimate source.

## Exam prep
### Likely 2-mark questions
1. **Differentiate functional and nonfunctional requirements.** Behavior/service versus quality/constraint.
2. **Give four nonfunctional categories.** Performance, security, usability, reliability, maintainability, portability, availability, scalability, or interoperability.
3. **Define a business requirement.** An organizational outcome, policy, or benefit needed by the system.
4. **What is an interface requirement?** An agreement describing data, behavior, timing, errors, and constraints at a system boundary.
5. **Why include transition requirements?** To make migration, training, cutover, or retirement possible in the real organization.
6. **Give one security requirement example.** An actor, protected asset, permitted action, and observable denial/audit condition.

### Long-answer answer hints
- “Classify requirements for a GPS system”: list functional, performance, usability, security, interface, data, operational, and transition examples; explain verification.
- “Differentiate user, business, and system requirements”: give a hierarchy and trace one from need to test.
- “Explain security requirements”: confidentiality, integrity, availability, authentication/authorization, audit, threat cases, and negative tests.
- “Why are data requirements important?” Meaning, format, quality, ownership, migration, retention, and consistency affect every other requirement.
- “Differentiate requirement and design”: what/why/quality versus how/structure/technology.

### Verification mapping
Function → functional test; response time → performance test; access rule → security test; usability → task study; migration → conversion rehearsal.
