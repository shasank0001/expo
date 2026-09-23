---
subject: oose
unit: 2
topic: problem-definition-and-scope
syllabus_ref: CSM3102 Unit-II
status: draft
---
# Problem Definition and Scope
## Overview
Problem definition turns a broad request into a clear statement of the problem, the intended users, the business objective, the boundary of the system, and the conditions for success. Scope says what the solution will and will not do for the first release. These are high-leverage decisions: a clear scope lets a team estimate, design, test, and decide whether a change is justified.

A good problem statement describes the need without prematurely choosing a solution. “Build an AI dashboard” is a proposed solution, not a problem. A better statement says who needs what, why the current situation is inadequate, what outcome matters, and which constraints apply.

## Explanation
### 1. Problem definition
A project problem definition should answer:
- **Who** has the problem or needs the improvement?
- **What** situation is painful, slow, risky, or impossible today?
- **Why** does the organization want to solve it now?
- **What evidence** shows that the problem exists?
- **What outcome** will indicate success?
- **What constraints, policies, and deadlines** must be respected?
- **Which stakeholders** can confirm or prioritize the needs?

Use a neutral description: “Inspectors spend repeated hours re-entering paper violations, causing delays and incomplete evidence,” rather than “We need a web form.” The first statement leaves room for several possible solutions.

### 2. Vision, objectives, and success criteria
The **vision** describes the desired future in broad terms. **Objectives** are the major outcomes the project intends to achieve. Each objective should be specific enough to evaluate.

Examples:
- Vision: make field inspections traceable and timely.
- Objective: reduce duplicate data entry by 40% for a normal inspection.
- Objective: provide authorized supervisors with current status within five minutes.
- Success criterion: 95% of trials complete the primary task without facilitator help.

A wish is not an objective. “Make the app excellent” needs measurable behavior or a user-study target.

### 3. Scope
**Scope** is the set of features, users, environments, and conditions included in the planned product. It creates a boundary and supports estimates and acceptance.

**In scope** examples:
- registered inspectors record inspections on mobile or web;
- capture required evidence and status;
- supervisors review and assign follow-up;
- users can search assigned records.

**Out of scope** for version 1:
- automated satellite imagery;
- legal-court filing;
- public citizen reporting;
- native offline synchronization;
- predictive risk scoring.

An item can be out of scope now and still appear in a future roadmap. The important part is to state the decision and its reason.

### 4. Product scope versus project scope
**Product scope** describes what the delivered software will do. **Project scope** describes the work needed to create it, such as migration, training, testing, and documentation. A product may have few features but a large project scope if data must be migrated from a legacy system. Confusing the two causes poor estimates.

### 5. Constraints and assumptions
A **constraint** limits the solution: budget, deadline, technology, regulation, device, skill, or an existing interface. An **assumption** is something treated as true but not yet confirmed. Both belong in the problem definition.

- Constraint: marks must be stored in the existing student-management database.
- Assumption: existing student IDs are unique.
- Risk if wrong: duplicate records or unusable imports.
- Action: verify the assumption with the data owner before coding.

### 6. Scope negotiation and prioritization
Prioritize by business value, user value, risk reduction, dependencies, effort, and urgency. A useful technique is a MoSCoW classification:
- **Must have:** system is not acceptable without it.
- **Should have:** important but a usable release may defer it.
- **Could have:** useful when capacity exists.
- **Won’t have now:** explicitly excluded from this release.

Prioritization is not the same as silently removing a requirement. Record the decision, reason, owner, and consequences.

### 7. Feasibility and success
Assess feasibility in at least four ways: technical, economic, operational, and schedule/legal. A small prototype or proof of concept can reduce uncertainty. The final problem definition is approved by an authorized stakeholder and becomes the reference for later requirements and change control.

## Worked examples
### Example 1: Chat system
Weak request: “Make a real-time chat app.” Problem definition: “Students need to exchange short messages during lab work when they cannot use personal messaging, but the current shared board is delayed and has no delivery status.” Scope might include one-to-one text, login, delivery status, and moderation; group calls and voice are later.

### Example 2: WMITS scope
The team includes inspectors, supervisors, and administrators, but only inspectors submit new inspections in version 1. Public reporting, court integration, and satellite analysis are excluded. The scope explicitly includes evidence photos, status history, and an audit trail because they are needed for trust and compliance.

### Example 3: Constraint and assumption
The hospital wants a navigation system for a specific handset model, but network connectivity may be unreliable. The fixed device is a constraint; “GPS data will always be available” is an assumption. The team tests offline behavior rather than accepting the assumption.

### Example 4: Prioritization
A client requests a map, live traffic, and an AI route score. A field pilot says basic routing and downloadable maps are needed to collect inspections. The team makes those must-have items, labels live traffic and AI scoring as later options, and records the decision so the absence is not mistaken for an accidental omission.

## Key terms & formulas
- **Problem statement:** a stakeholder-centered description of the current deficiency and desired outcome.
- **Scope:** the included and excluded product boundaries and conditions.
- **In-scope item:** work or behavior explicitly included in the current release.
- **Out-of-scope item:** behavior deliberately excluded for a stated release or reason.
- **Objective:** a specific intended result.
- **Constraint:** a limit imposed on the solution or process.
- **Assumption:** a proposition believed true for planning but requiring confirmation.
- **Feasibility:** practical ability to build and operate the proposed solution.
- **MoSCoW:** must, should, could, and won't-have-now prioritization.
- **Scope stability:** proportion of agreed scope not yet subject to pending changes; useful as a trend, not a target to game.

## Common mistakes
- Writing a solution as the problem statement and closing off alternatives too early.
- Listing features without users, outcomes, constraints, or evidence.
- Failing to state exclusions; stakeholders then assume everything is included.
- Treating scope as only features and forgetting migration, training, testing, and operations.
- Calling an assumption a fact or a constraint a preference.
- Prioritizing everything as “must have,” making trade-offs impossible.
- Measuring success only by whether the code was delivered, not whether the problem improved.

## Exam prep
### Likely 2-mark questions
1. **Differentiate a problem statement and a solution.** The first describes a need and deficiency; the second proposes a way to address it.
2. **What is scope?** The set of included and excluded features, users, environments, and conditions for a release.
3. **Differentiate a constraint and an assumption.** A constraint limits choices; an assumption is an unconfirmed belief used for planning.
4. **List four feasibility questions.** Can it be built, funded, operated by available people, and delivered legally/by the deadline?
5. **What does MoSCoW stand for?** Must, should, could, and won't-have-now.
6. **Why document out-of-scope items?** To prevent silent expectations and make future changes visible.

### Long-answer answer hints
- “Define problem and scope for a GPS system”: current users/problem, vision, objectives, in/out scope, constraints, assumptions, success criteria, and approval.
- “Differentiate product and project scope”: product behavior versus work and deliverables; give a migration example.
- “How do you negotiate scope?” gather needs, prioritize, evaluate dependencies/value, document decisions, and obtain stakeholder approval.
- “What is feasibility analysis?” technical, economic, operational, schedule/legal checks and a go/no-go decision.
- “Explain MoSCoW”: categories, strengths, and the danger of labeling every item Must.

### Problem statement template
For **[users]**, **[current problem]** causes **[measurable effect]**. The project will **[desired outcome]**, constrained by **[limits]**, and will be successful when **[criteria]**. This release includes **[scope]** and excludes **[out of scope]**.
