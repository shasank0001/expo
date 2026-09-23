---
subject: oose
unit: 2
topic: managing-requirement-changes
syllabus_ref: CSM3102 Unit-II
status: draft
---
# Managing Change in Requirements
## Overview
Requirements change because users learn, the business changes, laws and technology evolve, defects are found, and plans are revised. Change management provides a controlled way to request, analyze, decide, implement, and verify a change without losing the agreed product vision. It does not mean refusing change; it means making the cost and consequences visible and keeping the baseline and stakeholders informed.

The core practice is traceability. A requirement change should be connected to its source, affected design and code, tests, data, documentation, schedule, cost, risks, and release. This allows a change control board or product owner to decide whether, when, and how to accept it.

## Explanation
### 1. Why requirements change
- New user or stakeholder needs emerge after a prototype or release.
- A business objective or budget changes.
- A regulation, policy, interface, device, or platform changes.
- Testing reveals a misunderstood or missing requirement.
- Performance, security, or usability evidence invalidates an assumption.
- A dependency becomes unavailable or a new technology appears.
- Defects, support tickets, and operational experience show that a rule is wrong.

The change may be a **corrective** change (fix an incorrect requirement), **adaptive** change (fit a new environment), **perfective** change (improve the product), or **preventive** change (reduce future risk).

### 2. Baselines and configuration control
A **baseline** is an approved requirements version used as the reference. After baseline, each proposed change receives an ID and is evaluated against the baseline. The project keeps version history, status, author, approver, date, and reason. A change to one requirement is checked for effects on other requirements; local editing can create hidden inconsistency.

### 3. Change-control workflow
1. **Identify:** a stakeholder submits a change request with the need, evidence, and urgency.
2. **Record:** the analyst assigns an ID, source, description, requested priority, and affected release.
3. **Analyze:** assess impact on scope, design, code, data, interfaces, tests, documentation, schedule, cost, quality, training, and risk.
4. **Decide:** the authorized product owner or Change Control Board (CCB) accepts, rejects, defers, or negotiates it.
5. **Update the plan:** add the accepted work, revise the baseline, adjust dependencies, and communicate the decision.
6. **Implement:** update requirements first, then analysis/design, code/data, tests, and documentation in a controlled order.
7. **Verify and close:** test the changed behavior, update traceability, release it, and measure whether the intended need was met.

### 4. Change request information
A useful change request states:
- current requirement and proposed requirement;
- reason and evidence;
- affected users, business objective, and risk;
- urgency and desired release;
- dependencies, alternatives, and estimated effort/cost;
- impact on compatibility, security, data, quality, and operations;
- recommendation and decision owner.

A one-line “add a button” request is not enough to assess impact.

### 5. Impact analysis
Analyze:
- **Scope:** new or removed behavior and affected interfaces.
- **Architecture/design:** components, dependencies, and patterns.
- **Implementation/code:** modules, reusable components, and migration.
- **Data:** schema, conversion, retention, privacy, and existing records.
- **Testing:** new, changed, regression, performance, security, and acceptance tests.
- **Operations:** deployment, monitoring, support, training, and documentation.
- **Plan:** effort, cost, schedule, resources, and critical path.
- **Quality/risk:** new vulnerabilities, failure modes, and stakeholder expectations.

The result is a decision, not just a list. Estimate effort and schedule uncertainty, and state assumptions.

### 6. Prioritization and change authority
A product owner or CCB uses agreed criteria: value, risk reduction, urgency, effort, dependencies, contractual commitment, and effect on current users. In an agile context, the product owner orders a backlog and the team estimates the work; a formal CCB may still be required by a contract or regulated project. Authority must be clear so informal pressure does not bypass impact analysis.

### 7. Traceability and change propagation
Use links from source to requirement, use case, design, code, test, defect, release, and documentation. A changed authorization rule may require updating:
- glossary or policy;
- use-case and state model;
- access-control design;
- database permissions;
- security tests and regression suite;
- user documentation and training.

Traceability prevents the common failure of changing only the document or only the code.

### 8. Communication and release control
Communicate the decision, reason, effective version, impact, and date to affected stakeholders. Freeze a release candidate only after agreed changes are integrated and regression-tested. Keep old interfaces compatible or publish a migration plan. Store rejected/deferred requests so the same idea is not endlessly re-opened without new evidence.

## Worked examples
### Example 1: New evidence requirement
After the first inspection release, users report that photos without captions are hard to review. A stakeholder submits CR-014. The analyst traces FR-INSP-07 and its tests. The impact includes a caption field, mobile screen, validation, API, database migration, user guide, and new tests. The product owner defers it to Release 2 because existing metadata is sufficient for the pilot. The decision is recorded, and the backlog remains visible.

### Example 2: Regulation change
A new policy requires an audit record to be retained for seven years. The team identifies a data-retention requirement change, migration and storage-cost impact, access rules, deletion-job changes, and legal review. It updates the baseline before coding and adds a migration rehearsal and deletion test.

### Example 3: Conflicting urgent requests
A customer asks for a live traffic layer, while the security team reports a critical access-control defect. The defect is not merely another backlog item; it blocks release. The team pauses new feature work, fixes the authorization issue, expands the regression suite, and records the deferred feature request. This is controlled change rather than uncontrolled scope growth.

### Example 4: Version migration
A new GPS route format must be introduced. The change affects mobile clients, servers, cached routes, tests, and old devices. The team defines version negotiation, supports old clients for a stated period, publishes a migration date, and monitors error rates. A rollback path protects users who have not updated.

## Key terms & formulas
- **Requirements change:** a proposed or approved modification to an agreed requirement.
- **Baseline:** the approved version used for comparison and control.
- **Change request (CR):** a controlled proposal containing reason, impact, and requested action.
- **CCB:** Change Control Board; an authority that reviews and decides changes.
- **Impact analysis:** the assessed effect on scope, design, implementation, data, tests, plan, quality, and risk.
- **Traceability:** links that show source-to-implementation-to-test relationships.
- **Corrective/adaptive/perfective/preventive change:** types based on the reason for change.
- **Change failure rate (project indicator):** changes that caused rework, rollback, or incident ÷ total changes; use to improve—not to suppress legitimate learning.
- **Scope stability:** accepted baseline scope minus pending/accepted changes ÷ baseline scope × 100%, reported with reasons.
- **Lead time:** time from change request to verified production release; a useful process metric, not a reason to skip controls.

## Common mistakes
- Accepting a verbal request without recording it.
- Changing the code before the requirement and updating the baseline.
- Looking only at implementation effort and forgetting data, tests, documentation, and operations.
- Letting every stakeholder approve changes independently.
- Calling a rejected change “deleted” instead of recording the decision and reason.
- Failing to rerun regression tests after a small change.
- Treating change control as bureaucracy that prevents necessary learning.

## Exam prep
### Likely 2-mark questions
1. **What is requirements change management?** A controlled process to request, analyze, approve, implement, and verify changes to an agreed baseline.
2. **List the main steps.** Record, impact-analyze, decide, update baseline/plan, implement, verify, and communicate.
3. **What is a CCB?** A group or authority that evaluates and decides proposed changes against agreed criteria.
4. **Why perform impact analysis?** To see effects on scope, design, code, data, tests, schedule, cost, quality, and risk.
5. **What is a baseline?** An approved, versioned requirements set used as the reference for control.
6. **Name one change type and example.** Corrective: correct a misunderstood rule; adaptive: support a new platform; perfective: improve usability; preventive: add a safeguard.

### Long-answer answer hints
- “Explain managing change in requirements”: causes, types, baseline, request, impact analysis, decision, propagation, verification, and communication.
- “Draw a change-control workflow”: submit → log → analyze → CCB accept/reject/defer → update → implement → regression test → close.
- “Explain impact analysis for a new GPS feature”: route data, client/server interface, map cache, performance, migration, testing, and security.
- “Why is traceability important during change?” identifies all affected artifacts and helps ensure consistency and coverage.
- “Compare controlled change and scope creep”: controlled change is recorded, assessed, approved, and tested; scope creep is untracked unauthorized expansion.

### Mini change record
```text
CR: What changes? Why? Who requested it? Which baseline?
Impact: design / code / data / tests / docs / cost / schedule / risk
Decision: accept / reject / defer, owner, date
Verification: test and release evidence
```
