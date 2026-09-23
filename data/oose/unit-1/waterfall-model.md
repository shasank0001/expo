---
subject: oose
unit: 1
topic: waterfall-model
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Waterfall Model
## Overview
The waterfall model organizes a project into a mostly fixed sequence: requirements, design, implementation, testing, deployment, and maintenance. Work in one phase is intended to be completed and reviewed before the next phase begins. It is easy to schedule and audit, but it assumes that important requirements and design decisions will not change dramatically.

The model is not the same as “no iteration.” Reviews, prototypes, and corrective work can occur, but the central assumption is phase order and documented approval between phases. The model is most suitable when requirements are stable, the system is well understood, and late changes would be unusually expensive.

## Explanation
### 1. The phases
#### 1. Requirements
Stakeholders and customers describe what the system must do. The team elicits, analyzes, specifies, reviews, and baselines requirements. The output may include a requirements specification, use cases, data definitions, constraints, and acceptance criteria.

#### 2. System design
Requirements are converted into a solution. Designers decide the architecture, modules, data structures, interfaces, algorithms, user interface, error handling, and test strategy. The design is reviewed against requirements and quality attributes.

#### 3. Implementation (coding)
The design is translated into source code, database schemas, configuration, and build scripts. Developers may write unit tests alongside the code. The implementation is integrated into a build and checked for conformance with the design.

#### 4. Testing (verification and validation)
The integrated system is tested. Verification asks, “Are we building the product correctly?”—does it meet the design? Validation asks, “Are we building the right product?”—does it meet real user needs? Unit, integration, system, acceptance, and other tests are planned and executed here, although some testing can begin earlier.

#### 5. Deployment
The tested release is installed, configured, and handed to the user. Data migration, training, documentation, and an operational support plan are included. A deployment may be a single release or a controlled release to users.

#### 6. Maintenance
The product is corrected and improved after release. Defect correction, adaptive maintenance, perfective maintenance, and preventive maintenance occur. A change may feed back to requirements, design, and implementation, but the baseline is formally controlled.

### 2. Feedback and controls
Each phase ends with a review, inspection, or approval. Feedback can move backward—for example, testing can expose a design flaw—but the direction is usually from a more detailed phase to a less detailed one. A change-control board may assess the effect of late changes on cost and schedule.

### 3. Strengths
- Simple to understand and communicate.
- Produces a documented sequence of deliverables and approval points.
- Makes budgeting, scheduling, and progress measurement easier.
- Works well when requirements are clear and the technology is familiar.
- Encourages discipline and defined responsibilities.

### 4. Weaknesses
- The customer may see a working product only late, so misunderstandings survive until testing.
- A major requirement discovered after design can force expensive rework.
- Requirements are unlikely to be perfectly stable in many modern applications.
- The model can become a rigid “phase box” in which feedback and prototyping are discouraged.
- It does not naturally show frequent delivery of usable increments.

### 5. When to use it
It fits small, well-understood projects, contractual projects with a stable specification, and systems where documentation and formal approval are important. It is risky for rapidly changing products, exploratory work, and projects where stakeholder learning is central. A modified waterfall or the V-model can add verification links and prototyping.

### 6. Waterfall versus the V-model
The V-model places verification beside development stages. Requirements are checked by acceptance tests, architecture by system/integration tests, detailed design by unit tests, and coding by review and white-box testing. The model still has a development sequence, but it makes “test early” and traceability more visible.

## Worked examples
### Example 1: College mark-entry module
For a stable mark-entry module, the team documents rules, designs the database and screens, implements forms, tests calculations and permissions, deploys them to a training server, and then maintains corrections. A review catches an unclear “best-of” rule before coding, so rework is small.

### Example 2: A late change
A customer asks, after coding, for a completely new mobile workflow. The change may alter the database, interface, security rules, test cases, and documentation. The project manager records the change and estimates its impact. The waterfall model does not forbid the change, but it is much cheaper if the requirement is discovered before the later phases.

### Example 3: A defect loop
The test phase finds that the generated percentage rounds incorrectly for a boundary. The tester links the failure to the requirement and the design, a developer fixes the calculation, and regression tests protect valid cases. This is feedback within the waterfall, not a claim that the model has no iteration.

### Example 4: Choosing a model
A small college attendance form has stable rules and one approved user group; waterfall is reasonable. A startup testing a new recommendation feature with uncertain demand is better served by an evolutionary or spiral approach because it can learn from early releases.

## Key terms & formulas
- **Phase:** a defined group of activities ending in a reviewed deliverable.
- **Stage gate:** a review/approval point before proceeding.
- **Baseline:** an agreed version of a deliverable used as the reference for change control.
- **Verification:** “build the product right”—conformance to specified design and requirements.
- **Validation:** “build the right product”—conformance to actual stakeholder needs.
- **V-model:** a development model with corresponding test levels on the opposite side of the development stages.
- **Rework:** returning to an earlier activity because a later check found a defect or changed assumption.
- **Change impact analysis:** the estimated effect of a change on scope, cost, schedule, quality, dependencies, and risk.

## Common mistakes
- Saying the waterfall model permits no reviews or feedback.
- Forgetting deployment, maintenance, or configuration management in the phase list.
- Claiming it cannot handle change; it can, but change is usually more expensive late.
- Confusing verification with validation.
- Treating a phase label as proof that the work is complete; completion needs exit criteria and review evidence.
- Presenting it as always best or always bad rather than matching it to project conditions.

## Exam prep
### Likely 2-mark questions
1. **List the waterfall phases.** Requirements, design, implementation, testing, deployment, and maintenance (some presentations separate system design and coding).
2. **Give one advantage and one disadvantage.** Advantage: easy planning/control; disadvantage: expensive response to late changing requirements.
3. **When is waterfall suitable?** When requirements are stable and the problem is well understood.
4. **Differentiate verification and validation.** Verification checks the product against the specified design; validation checks that it meets real user needs.
5. **What is a V-model?** A modified waterfall that links each development stage to an appropriate level of testing.

### Long-answer answer hints
- “Explain the waterfall model with a diagram”: draw requirements → design → implementation → testing → deployment → maintenance, add review/feedback arrows, explain each output.
- “Compare waterfall with spiral”: fixed sequence and stable assumptions versus risk-driven loops and early prototypes.
- “Why can waterfall fail on a changing product?” show how a misunderstood requirement propagates into design, code, tests, and rework.
- “Explain the V-model as an improvement”: pair requirements with acceptance tests, architecture with system tests, detailed design with unit tests.
- “When would you select waterfall?” give a suitable example, list its assumptions, and acknowledge its risk if requirements change.

### Sketch to reproduce
```text
Requirements → Design → Implementation → Testing → Deployment → Maintenance
       ↑           ↑             ↑            ↑              ↓             ↓
       └──────── feedback and approved change control ──────┘
```
