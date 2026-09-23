---
subject: oose
unit: 2
topic: requirements-definition
syllabus_ref: CSM3102 Unit-II
status: draft
---
# Requirements Definition
## Overview
Requirements definition turns an approved problem, scope, and domain understanding into a precise, testable statement of what the software must provide. It describes behavior, quality, interfaces, constraints, and acceptance conditions without prescribing an unnecessary implementation. Good requirements let a customer, developer, tester, and manager interpret the same product in the same way.

Definition is a collaborative activity, not a final document written after coding. The team refines requirements through analysis, prototypes, reviews, and change control. Each requirement should be understandable, singular where possible, feasible, necessary, prioritized, and traceable to a source.

## Explanation
### 1. From need to requirement
The process is:
```text
Stakeholder need → problem evidence → scope/objective → candidate requirement
→ analysis and prioritization → specification → review/validation → baseline
```
A candidate statement such as “the system should be secure” is not yet testable. It may become: “Only a user with the Instructor role can modify a mark; every attempt is denied for other roles and recorded in the audit log.” The latter names behavior, actor, outcome, and evidence.

### 2. Requirement qualities
- **Clear:** uses one interpretation and common domain terms.
- **Complete:** covers normal, error, boundary, security, and recovery behavior relevant to the scope.
- **Consistent:** does not contradict another requirement or an organizational rule.
- **Feasible:** can be implemented within the known technology and constraints.
- **Testable/verifiable:** has an observable acceptance condition.
- **Necessary:** can be traced to a stakeholder need or quality/legal concern.
- **Unambiguous:** avoids words such as “fast,” “easy,” and “robust” unless quantified.
- **Prioritized:** has an importance and a reason.
- **Traceable:** has a source, owner, version, and links to design, code, and tests.

### 3. Functional and nonfunctional content
**Functional requirements** describe observable product behavior and services. Examples: validate a login, calculate a route, store an inspection, or notify a supervisor. **Nonfunctional requirements** describe quality and constraints, such as response time, availability, security, usability, maintainability, and interoperability. The distinction is about what is being specified, not about the absence of constraints on functions.

A well-written requirement often combines a functional capability with a quality criterion:
- “The system shall allow an inspector to submit a required photo with an inspection.”
- “For the stated 500 concurrent-user workload, 95% of accepted submissions shall appear in the supervisor list within 2 seconds.”
- “The system shall prevent a user without the Supervisor role from closing an inspection.”

### 4. Requirement categories
- **User/business requirements:** goals and rules from stakeholders and the organization.
- **System requirements:** required behavior of the complete system.
- **Functional:** services, actions, calculations, and responses.
- **Quality/nonfunctional:** measurable attributes.
- **Interface:** external device, API, database, message, or legacy-system interaction.
- **Security/privacy:** identity, access, confidentiality, integrity, audit, and retention.
- **Data/migration:** formats, quality, conversion, retention, and privacy.
- **Operational/environment:** deployment, availability, platform, and monitoring.
- **Transition:** training, cutover, coexistence, and decommissioning.
- **Legal/regulatory/compliance:** mandated records, accessibility, safety, or reporting.

### 5. Requirement formulation
Use a consistent sentence pattern:
`The system shall [actor] [action] [object] [condition] [response/criterion].`
Use “shall” for mandatory behavior and “should” for a preference, if the project convention allows it. Number requirements so they can be reviewed and traced. Split conjunctions: “save and send” may be two requirements with different failure behavior. Avoid implementation words such as “use a hash table” unless the choice is a real constraint.

### 6. Requirement specification
A specification may contain:
1. Introduction, purpose, scope, and stakeholders.
2. Overall product description and domain terms.
3. Functional requirements with IDs and priority.
4. Nonfunctional requirements with measurable criteria.
5. Interface, data, security, and operational requirements.
6. Use cases or user stories and business rules.
7. Assumptions, constraints, dependencies, and open issues.
8. Acceptance criteria, glossary, and traceability references.

The format should serve the audience. A contract specification emphasizes agreement and testability; a user story is concise and paired with acceptance criteria; a use case adds a scenario; a model provides precise structure.

### 7. Validation and baseline
Before baselining, check each requirement with the source stakeholder and domain expert. Use review, prototypes, models, and acceptance-test design. Resolve conflicts and record decisions. Once approved, requirements form a **baseline**; changes go through impact analysis and configuration control, but the baseline still does not prevent learning from legitimate change.

## Worked examples
### Example 1: Turning a request into a requirement
Request: “The GPS system should be fast and show directions.” A better pair is:
- “Given a valid origin, destination, and map, the system shall calculate and display a route.”
- “Under the agreed test map and device workload, 95% of route requests shall return within two seconds.”
The first states behavior; the second states measurable quality.

### Example 2: Functional requirement
“If an inspection is missing required evidence, the system shall prevent closure and display the missing field.” The requirement names the condition, action, and feedback. It can later produce a use case, UI design, and test.

### Example 3: Requirement conflict
The registrar says a mark can be corrected after submission; the instructor says corrections are forbidden. The analyst records both sources, identifies the policy owner, and obtains a decision. Splitting “correction” into authorized amendment and prohibited overwrite resolves the conflict.

### Example 4: Traceability
`FR-AUTH-03` states the instructor authorization rule. It links to use case UC-12, design class `MarkEntry`, implementation commit, and tests TC-AUTH-03/TC-AUTH-04. A change to the role model can therefore be assessed systematically.

## Key terms & formulas
- **Requirement:** a condition or capability needed for a solution to achieve its purpose.
- **Functional requirement:** observable service or behavior.
- **Nonfunctional requirement:** quality, performance, security, usability, reliability, or other constraint/criterion.
- **Specification:** an organized, versioned description of requirements.
- **Baseline:** an approved version used for control and change comparison.
- **Traceability matrix:** links requirements ↔ sources, design, code, tests, and changes.
- **Acceptance criterion:** an observable condition used to decide whether a requirement is satisfied.
- **Priority:** relative importance/urgency used for negotiation and delivery order.
- **Coverage:** implemented/tested applicable requirements ÷ total applicable requirements × 100%; report untestable or deferred items separately.
- **Requirement volatility:** number of approved changes ÷ requirements measured over a period; use with reason and impact, not as a quality score.

## Common mistakes
- Writing requirements as user-interface clicks or code structure.
- Using vague adjectives without a measure.
- Combining several independent behaviors into one numbered requirement.
- Omitting exceptions, security, and data handling.
- Treating a use case title as a complete requirement.
- Writing requirements after the design and calling it a specification.
- Not giving a source, owner, ID, or status, so changes cannot be controlled.
- Claiming a requirement is complete merely because the document is long.

## Exam prep
### Likely 2-mark questions
1. **What is a requirement?** A needed capability or condition for the product to achieve its purpose.
2. **Differentiate functional and nonfunctional requirements.** Functional describes observable behavior; nonfunctional describes quality or constraints.
3. **Give four properties of a good requirement.** Clear, feasible, testable, necessary, prioritized, traceable, complete, or consistent—any four.
4. **Why is “shall” useful?** It distinguishes mandatory behavior from optional preference and gives requirements consistent force.
5. **Define traceability.** The ability to link requirements to sources, design, implementation, tests, and changes.
6. **What is a baseline?** An agreed, versioned set of requirements used as the reference for change control.

### Long-answer answer hints
- “Explain requirements definition”: need → problem/scope → analysis → specification → validation → baseline; include qualities and an example.
- “Write two good requirements from a vague request”: show action, actor, condition, and measurable quality criterion; explain why the original is ambiguous.
- “Differentiate requirements and design”: requirements say what and under which quality/constraint; design chooses how.
- “Explain requirement traceability and its benefits”: source, design, code, test, change; faster impact analysis and coverage evidence.
- “What makes a requirement testable?” an observable input/precondition, action/output or state, and measurable expected result.

### Requirement template
`[ID] The [actor] shall [action] [object] when [condition], producing [result] with [priority/criterion].`
