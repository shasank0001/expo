---
subject: oose
unit: 2
topic: requirements-reviewing
syllabus_ref: CSM3102 Unit-II
status: draft
---
# Requirements Reviewing
## Overview
Requirements reviewing is the systematic check that a requirements document is correct, complete, consistent, feasible, necessary, prioritized, and understandable before it is used as a design and testing basis. It is both **validation**—does it represent the real stakeholder need?—and a quality inspection of the document itself.

Reviewing is more than proofreading. A review walks through normal and exceptional scenarios, checks business rules, questions ambiguous words, traces requirements to sources and tests, and records disagreements. A document is not approved merely because the author or a manager likes it.

## Explanation
### 1. Purposes of requirements review
- Find defects early: omissions, contradictions, ambiguity, incorrect terminology, and untestable statements.
- Confirm that the product solves the intended problem and stays within scope.
- Involve customers, users, domain experts, developers, testers, operations, security, and legal representatives.
- Resolve conflicts and assign decisions to authorized people.
- Establish confidence that requirements can be designed, estimated, implemented, and tested.
- Create a reviewed baseline and evidence for later change control.

### 2. Validation versus verification
- **Validation:** “Are we specifying the right product?” Compare the requirements with stakeholder needs, domain rules, business objectives, regulations, and realistic scenarios.
- **Verification of the requirements:** “Are the requirements clear, complete, consistent, and testable?” Inspect the document as an artifact.
Later product testing verifies the implementation against the approved requirements; it does not replace requirements review.

### 3. Review inputs
A useful packet includes the problem/scope statement, stakeholder goals, glossary, requirements with IDs, use cases, domain/state models, interface/data descriptions, assumptions, risk list, prototypes, and prior review comments. Reviewers should have enough time and the actual system context, not just a link to a huge document.

### 4. Review techniques
#### Walkthrough
The author explains the document and scenario flow. Participants ask questions and identify issues. A walkthrough is good for shared understanding and early discovery, but the author should not control all answers.

#### Technical/analytical review
Reviewers examine models, rules, interfaces, calculations, and consistency from different specialist perspectives. A security reviewer checks threats and permissions; a domain expert checks rules; a tester checks observability and edge cases.

#### Inspection
An inspection uses a defined process, roles (e.g., moderator, producer, author, readers), entry/exit criteria, defect log, and rework. The team inspects the artifact for classes of defects rather than only reading for style.

#### Prototyping and scenario testing
A prototype or paper scenario exposes assumptions that words hide. For example, stakeholders may approve a login screen but discover during a walkthrough that they forgot password recovery. The prototype is evidence for a change, not a substitute for the complete specification.

#### Formal consistency/model checking
For critical rules, use a decision table, state machine, or a consistency check to detect missing or contradictory combinations. A rule table can reveal that a state/event pair has no defined action.

### 5. Review criteria
#### Correctness
Does the requirement agree with the domain expert, policy, regulation, and agreed problem?
#### Completeness
Are all functions, quality attributes, interfaces, errors, data, security, transition, and exception cases in scope covered?
#### Consistency
Do requirements use the same terms and avoid contradictions?
#### Feasibility
Can the team build and operate the requested behavior within technology, time, budget, skill, and constraints?
#### Necessity
Is each item traceable to a real need or a stated quality/risk requirement?
#### Testability
Can an observer or test determine whether the requirement is met?
#### Priorities and trade-offs
Are must/should/could/won’t decisions clear and realistic?

### 6. The review workflow
1. Set the review purpose, scope, reviewers, date, and exit criteria.
2. Give reviewers the artifacts and questions in advance.
3. Walk through the problem, scope, glossary, and end-to-end scenarios.
4. Inspect each requirement against criteria; record defects, questions, and source links.
5. Separate blockers, major issues, minor issues, and suggestions.
6. Assign an owner and due date to every defect or decision.
7. Revise the document and repeat affected reviews.
8. Obtain approval, record the baseline/version, and link tests and design.

### 7. Defect examples
- **Ambiguity:** “The system shall handle errors appropriately.”
- **Contradiction:** one requirement allows negative values while another rejects them.
- **Omission:** no requirement for password reset or data backup.
- **Unverifiable:** “The interface shall be intuitive.”
- **Nonfunctional gap:** no response-time workload or security authorization rule.
- **Scope confusion:** an explicitly out-of-scope feature appears as a “shall.”

## Worked examples
### Example 1: GPS scenario review
Reviewers walk through a route request from a moving vehicle, a no-signal area, a closed road, and an invalid destination. They find no requirement for offline fallback, stale map data, or rerouting. The team adds candidates, assigns priority, and updates acceptance tests.

### Example 2: WMITS security review
The review asks whether an inspector can close their own inspection, whether a removed user keeps access, and whether a failed image upload is recorded. The security and domain reviewers add role rules, revocation behavior, and audit requirements. A developer asks whether an image can be retried; a new exception flow is added.

### Example 3: Contradictory requirements
One requirement says a returned record is editable; another says all submitted records are locked. The reviewer links both to a scenario, asks the policy owner, and changes the wording to “returned records are editable until resubmitted.” The state model and tests are updated.

### Example 4: Review metric
A team has 80 applicable requirements. Before review, only 52 have linked acceptance tests and 5 have unresolved questions. The review highlights these gaps rather than declaring a high score based on document length. After correction, the team can report traceability coverage of 100% and zero unresolved blockers.

## Key terms & formulas
- **Review:** structured evaluation of an artifact against criteria.
- **Validation:** confirmation that requirements represent actual stakeholder needs.
- **Walkthrough:** guided presentation and scenario discussion.
- **Inspection:** defect-focused review with roles and defined process.
- **Defect class:** recurring category such as ambiguity or omission.
- **Blocking issue:** issue that prevents approval or further design.
- **Entry criterion:** evidence required before review, such as a draft and source data.
- **Exit criterion:** evidence required to finish, such as no blockers, agreed priorities, and linked tests.
- **Traceability coverage:** requirements linked to tests and validation evidence ÷ applicable requirements × 100%.
- **Review effectiveness (simple):** defects found before implementation ÷ total defects found, used to compare process effectiveness.

## Common mistakes
- Reviewing grammar while missing a missing business rule.
- Letting the most senior person end every disagreement without recording the decision.
- Calling a meeting a review when there is no checklist, artifact, defect log, or exit criteria.
- Reviewing only happy paths.
- Approving requirements that are not testable.
- Skipping review after a major change or merging only the changed paragraphs without checking consistency.
- Confusing a prototype review with stakeholder acceptance of every nonfunctional requirement.

## Exam prep
### Likely 2-mark questions
1. **Define requirements reviewing.** Structured evaluation of a requirements document for correctness, completeness, consistency, feasibility, necessity, and testability.
2. **Differentiate validation and verification.** Validation asks whether the right needs are specified; verification checks the document/product against those specifications.
3. **List three review techniques.** Walkthrough, technical review, inspection, prototype/scenario walkthrough, or formal analysis.
4. **What is an exit criterion?** Evidence that a review is complete, such as no blockers, agreed priorities, and traceability to tests.
5. **Why include testers in review?** They expose missing states, errors, edge cases, and unverifiable requirements early.
6. **Give one review defect class.** Ambiguity, contradiction, omission, incorrect behavior, or untestable quality.

### Long-answer answer hints
- “Explain requirements reviewing and validation”: purpose, inputs, participants, techniques, criteria, workflow, exit criteria, and evidence.
- “How do you conduct a requirements review?” prepare, walk through scenarios, inspect, log/assign defects, revise, and approve a baseline.
- “Differentiate review, inspection, and walkthrough”: purpose, roles, process, and defect emphasis.
- “Why is early review valuable?” defects become more expensive as they propagate to architecture, code, data, and tests.
- “How can a reviewer test usability and security requirements?” use representative tasks, role/abuse scenarios, measurable criteria, and trace each to an acceptance test.

### Reviewer checklist
Correct? Complete? Consistent? Feasible? Necessary? Testable? Prioritized? Traceable? Exceptions covered? Decisions recorded?
