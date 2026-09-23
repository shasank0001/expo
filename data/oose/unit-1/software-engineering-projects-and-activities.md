---
subject: oose
unit: 1
topic: software-engineering-projects-and-activities
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Software Engineering Projects and Activities
## Overview
A software engineering project is a planned effort that turns a stakeholder need into a useful, tested, and maintainable product. It is not simply a group of programmers typing code. A project coordinates people, scope, schedule, cost, quality, risk, and change so that the result can be delivered in a usable condition.

This note follows the software process from an idea to maintenance. The activities are connected: a decision made during requirements affects design, design affects implementation and testing, and test results may return a change to every earlier activity. A good process makes these dependencies visible and gives the team a way to respond when reality differs from the plan.

## Explanation
### 1. What is a software engineering project?
A project is a temporary effort with a defined beginning and end. A software product may live for years, but a project may deliver one release or a defined set of changes. The project is complete when agreed deliverables and acceptance conditions are met—not merely when all code has been written.

A project normally answers:
- What problem will be solved, and for whom?
- What is included and excluded?
- Which activities and deliverables are required?
- Who is responsible for each result?
- What quality level and schedule are agreed?
- How will changes, risks, and defects be handled?
- How will the product be handed over and maintained?

### 2. Project characteristics and stakeholders
- **Temporary:** a project has a start, milestones, and a planned end.
- **Unique:** the team develops a particular product or adaptation; even repeated work is rarely identical.
- **Constrained:** scope, time, cost, quality, and resources are in tension.
- **Cross-functional:** requirements come from users, design from architects, implementation from developers, and quality assurance from testers and reviewers.
- **Uncertain:** technical answers, stakeholder needs, and external conditions may not be known at the beginning.

Important stakeholders include customers, users, sponsors, product owners, domain experts, developers, operations staff, maintainers, legal/regulatory staff, and external service providers. Each has a different vocabulary and success criterion. Communication is therefore part of engineering, not merely administration.

### 3. Core software-engineering activities
#### Feasibility and project initiation
The team identifies the business need, objectives, constraints, expected value, risks, and possible alternatives. It asks whether the project is technically possible, economically justified, operationally suitable, and legal. The output may be a feasibility report, a business case, an initial risk list, and a go/no-go decision.

#### Planning
Planning turns the idea into a manageable commitment. It defines scope, milestones, activities, resources, schedule, budget, risk responses, quality objectives, and communication rules. Estimates may be expressed in effort (person-hours/days), cost, duration, or team capacity. They should include review, testing, rework, deployment, and maintenance—not only coding.

#### Requirements engineering
Stakeholders' needs are elicited, analyzed, specified, validated, and managed. Requirements engineering produces a shared vision and a traceable baseline. Because requirements errors are expensive to fix late, this activity continues throughout the project.

#### Analysis and modeling
Analysts describe the problem domain, user goals, use cases, data, and constraints. Models and prototypes reduce misunderstanding. For object-oriented work, the analysis may produce classes, responsibilities, associations, and system interfaces that later become a design.

#### Design and architecture
Design turns requirements into a solution structure. It defines modules/classes, responsibilities, data, interfaces, persistence, user interaction, architecture, error handling, and testability. The team compares alternatives against criteria such as performance, security, maintainability, cost, and risk. It records the chosen design and rationale.

#### Implementation
Developers write or configure code, create schemas, build components, integrate libraries, and produce a deployable build. Implementation follows the agreed design, coding conventions, version-control practices, code review, and build pipeline. Implementation reveals design issues; changes must be recorded and reassessed rather than patched silently.

#### Testing and quality assurance
Testing checks behavior with planned inputs and expected results. White-box tests use knowledge of the code; black-box tests use requirements and interfaces; reviews and inspections examine artifacts. Defects are logged, prioritized, fixed, and retested. Testing is planned and managed like any other activity, not left until the end.

#### Deployment and release
The team packages the product, installs or releases it, configures the environment, migrates data when needed, trains users, and verifies operation. A release plan includes rollback, backups, monitoring, and communication. Deployment is not complete until the product works in the intended environment and users can use it.

#### Maintenance and retirement
Maintenance corrects defects, improves performance and usability, adapts the product to new laws or platforms, and adds requested features. Changes are analyzed so that new requirements do not break old behavior. Eventually the product may be retired; data must be archived, dependencies removed, and users notified.

### 4. Process assets and deliverables
A process model is supported by procedures, templates, checklists, tools, training, and lessons learned. Typical deliverables include a vision/scope statement, requirements specification, project plan, model, design document, source code, test plan, test reports, release notes, user documentation, and maintenance plan. A deliverable is useful only when its intended audience and acceptance criteria are clear.

### 5. Process tailoring
No single process fits every project. A student prototype, a safety-critical controller, and a small web service need different levels of formality, documentation, review, and automation. Tailoring changes the order, detail, or emphasis of activities while preserving their intent. The reason for a tailoring decision should be recorded.

## Worked examples
### Example 1: College attendance system
The project begins with the need to record attendance accurately. Activities include interviewing faculty and students, defining attendance rules, modeling roles, selecting a database, implementing screens and reports, testing duplicate submissions and network failures, training staff, and maintaining the policy. A missing data-migration task would be a real planning gap, not a coding detail.

### Example 2: Emergency application
For a waste-management inspection system, safety and auditability matter more than a very attractive interface. The team adds a mobile/offline workflow, immutable inspection records, authorization checks, time-stamped status changes, backup and recovery tests, and a rollback plan. These are project activities derived from requirements and risk.

### Example 3: A change closes the loop
During system testing, a tester finds that an inspection can be marked “closed” without the required photo. The tester records the defect. The analyst updates the rule, the designer changes the state transition, developers implement the check, and regression tests verify old close operations. The project manager schedules the work and assesses its impact. No single activity can be improved in isolation.

### Example 4: Scope control
A client requests live GPS route drawing in version 1. If it is outside the agreed scope, the team records the request, estimates its effort and risk, explains the trade-off, and seeks a change decision. It is not silently absorbed into the current release.

## Key terms & formulas
- **Project:** temporary effort with defined scope, deliverables, and end point.
- **Product:** the reusable result delivered by the project.
- **Stakeholder:** any person or organization affected by or able to affect the project.
- **Milestone:** a significant point used to review progress or make a decision.
- **Deliverable:** a measurable output required by the plan or contract.
- **Traceability:** the ability to link a requirement to design, code, test, and change records.
- **Effort:** work required, commonly person-hours or person-days.
- **Cost estimate:** effort multiplied by the appropriate labor/overhead rate, plus tools, licenses, cloud services, training, and contingency.
- **Schedule estimate:** sequence, dependencies, durations, and available capacity used to predict dates.
- **Scope–time–cost–quality trade-off:** changing one constraint usually affects the others; the decision must be explicit.

## Common mistakes
- Treating a project as completed when code compiles.
- Omitting data, documentation, testing, training, deployment, or maintenance from effort estimates.
- Treating stakeholder communication as optional “management work.”
- Making a plan that has no owner, dependency, or acceptance criterion.
- Hiding a scope change instead of recording its impact.
- Confusing a process model with a fixed schedule; a model organizes activities, while a plan assigns dates and resources.
- Saying “iterative” always means the same thing. Iteration is repeated work on a product increment, not merely repeated meetings.

## Exam prep
### Likely 2-mark questions
1. **Define a software engineering project and list four activities.** A temporary, planned effort to deliver a software product; any four of planning, requirements, design, implementation, testing, deployment, or maintenance.
2. **Differentiate a project and a product.** A project is a temporary effort; a product is the result that may be used and evolved after the project.
3. **Why are stakeholders important?** They supply needs, constraints, decisions, and feedback; their conflicting expectations affect success and risk.
4. **What is traceability?** The ability to link requirements through design and implementation to tests and changes.
5. **Name two deliverables other than source code.** Requirements specification, test report, user guide, release package, or maintenance plan.
6. **What is process tailoring?** Adapting activities and artifacts to project risk, size, and context while keeping their intent.

### Long-answer answer hints
- “Explain software engineering activities”: define the project, draw the lifecycle, and explain each activity's inputs, outputs, controls, and feedback in order. Include a change example.
- “Describe project characteristics and stakeholders”: use temporary, unique, constrained, cross-functional, uncertain; list stakeholders and communication needs.
- “How does a defect move through the process?” tester → defect report → analysis → design/code change → review → regression test → release.
- “Explain process tailoring”: compare a safety-critical system with a student prototype; state which artifacts and reviews differ.
- “How do you plan a software project?” scope, activities, dependencies, estimates, schedule, risks, communication, quality, and acceptance.

### Quick comparison frame
A **deliverable** is an output; a **milestone** is a point in time; a **risk** is an uncertain event; a **change** is a controlled modification to an agreed baseline.
