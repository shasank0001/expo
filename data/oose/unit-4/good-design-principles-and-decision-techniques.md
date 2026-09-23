---
subject: oose
unit: 4
topic: good-design-principles-and-decision-techniques
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# Good-Design Principles and Decision Techniques
## Overview
Good design balances competing qualities while keeping the system understandable, testable, changeable, and aligned with requirements. Design principles provide rules of thumb, not automatic answers. A principle is useful only in context: encapsulation can improve change, but too many layers can make a small feature hard to use.

A design decision technique makes choices more deliberate. It identifies an issue, alternatives, criteria, evidence, trade-offs, and consequences. Recording the reasoning is as important as selecting an option because future maintainers must know what problem the decision solved.

## Explanation
### 1. Principles for good design
#### Divide and conquer
Break a large system into modules, layers, services, classes, and use-case slices. Each part should have a clear responsibility and be understandable at an appropriate level. Divide by cohesion or business capability, not by arbitrary file size.

#### High cohesion
Elements inside a module should work toward one coherent responsibility. A class with authentication, report rendering, and database connection code is difficult to change and test. Cohesion supports local reasoning and reuse.

#### Low coupling
Modules should depend on stable interfaces and minimal knowledge of each other's internals. Reduce shared mutable data, avoid circular dependencies, pass meaningful contracts, and isolate likely variation. Coupling is not always bad:some collaboration is necessary; the goal is to make it explicit and controlled.

#### Abstraction and information hiding
Present essential behavior and hide implementation decisions. An abstraction should be stable enough to protect clients from change. Hide data structures, protocols, devices, and algorithms behind services rather than leaking them to every caller.

#### Modularity and interfaces
A module has one public contract and hides its implementation. Interfaces should be small, coherent, and based on client needs. A large “everything” interface increases coupling and makes replacement difficult.

#### Reuse and generality
Prefer well-tested existing components when they meet the requirement and fit the risk. Reuse is not copying unknown code or forcing a library into an unsuitable problem. Generalize at stable variation points, not everywhere.

#### Increase flexibility
Isolate likely changes—UI framework, database, payment provider, map service, or notification channel. A stable boundary lets a new implementation replace an old one. Avoid speculative flexibility where no evidence exists.

#### Design for testability
Make behavior observable through clear operations, outputs, and error states. Isolate external systems behind replaceable interfaces, provide controlled time/data, and avoid hidden global state. Testability is a design property, not a testing afterthought.

#### Design defensively
Validate inputs and contracts at boundaries, handle failure, and protect invariants. Use assertions where appropriate, but do not assume callers always behave correctly. Defensive design includes timeouts, retries with limits, access checks, and graceful degradation.

#### Simplicity and consistency
Prefer the simplest structure that meets requirements. Use consistent names, interfaces, and error conventions. Remove unnecessary indirection, duplicated state, and speculative generality. Simplicity is not the fewest lines; it is the least unnecessary conceptual burden.

#### Portability and obsolescence
Keep device, OS, protocol, and vendor details behind replaceable layers. A design should identify what is likely to change and isolate it. Portability does not require identical behavior on every platform when requirements differ.

### 2. Quality trade-offs
The design team must balance performance, security, usability, reliability, maintainability, cost, schedule, and portability. A cache improves speed but risks staleness. More layers improve separation but add call overhead and debugging. Strong access checks cost effort but protect critical data. A local cache may improve response but complicate replication.

Make the trade-off explicit using evidence. For a route app, perhaps 95th-percentile latency is more important than first response for background traffic; a safety system may choose conservative memory use over maximum throughput.

### 3. Design decision techniques
#### Issue/alternatives/criteria/decision
Start with a design issue, list at least two viable alternatives, choose criteria, compare them, decide, and record consequences. Criteria should include the requirement and relevant quality attributes, not only implementation convenience.

#### Weighted decision matrix
Assign weights to criteria, rate alternatives, and calculate a total:
`score(a) = Σ(wᵢ × rᵢₐ)`, where `wᵢ` is the importance of criterion i and `rᵢₐ` is the rating of alternative a. Normalize the rating scale and document the evidence. A matrix supports discussion; it does not replace judgment.

#### Scenario analysis and prototypes
Evaluate a design against normal, alternative, failure, security, concurrency, and recovery scenarios. Build a focused prototype when a risk is uncertain. A prototype is evidence for a particular question, not proof of all qualities.

#### Cost–benefit/risk analysis
Estimate implementation, operation, maintenance, and change cost against benefits. For risks, assess probability and impact, then choose avoid, reduce, transfer, or accept responses. Security and safety risks need explicit treatment.

#### Design by contract
Specify preconditions, postconditions, and invariants for operations. Contracts make assumptions visible and support assertions, reviews, and tests. They are most valuable at public or collaboration boundaries.

#### Review and walkthrough
A multidisciplinary review finds defects and alternatives that the author did not see. A design walkthrough follows a use case through the components and checks whether the proposed flow is coherent. Record issues and decisions.

#### Reuse and constraint analysis
Identify existing assets and the constraints they impose. Build adapters or facades when useful, but evaluate quality, licensing, support, and version compatibility. “Already written” is not the same as “suitable.”

### 4. Criteria for good decisions
A good decision is:
- linked to a requirement or quality goal;
- based on evidence or explicit assumptions;
- compared with credible alternatives;
- understandable to the team;
- reversible or given an exit plan when risky;
- accompanied by verification and consequences;
- revisited when evidence changes.

## Worked examples
### Example 1: Layer choice
A team compares direct UI-to-database access with a layered UI → application service → repository design. Criteria: security, testability, reuse, performance, and effort. Direct access has lower call overhead but scatters rules and makes authorization inconsistent. The layered design adds one controlled boundary and is selected. A small benchmark checks that the performance target still holds.

### Example 2: Weighted decision
The team compares two map providers. Weights: coverage 30%, offline support 25%, cost 20%, API reliability 15%, maintenance 10%. Ratings are 4/5, 5/5, 2/5, 5/5, 3/5. The weighted totals show whether the cheaper provider is worth the risk. The team also runs a prototype because scores alone cannot prove offline behavior.

### Example 3: Design by contract
`Inspection.approve(actor, reason)` requires an assigned supervisor, a nonterminal state, and a nonblank reason. On success, status becomes Approved and an audit event is created. Tests use preconditions, valid cases, and invalid boundary cases. A guard check makes the contract visible.

### Example 4: Avoiding speculative design
A team considers supporting three databases although the product will use one for its first two years. It wraps persistence behind a repository interface but implements only the required database. This preserves a reasonable change boundary without building unused drivers. The decision and review date are recorded.

## Key terms & formulas
- **Design principle:** general rule that supports a quality when applied appropriately.
- **Trade-off:** competing benefits and costs.
- **Decision issue:** question that must be resolved.
- **Criterion:** measurable or observable factor used to compare alternatives.
- **Weighted score:** `Σ(weight × rating)`; define scale and weights.
- **Design by contract:** preconditions, postconditions, and invariants.
- **Risk response:** avoid, reduce, transfer, or accept.
- **Prototype evidence:** observed result for a stated question and environment.
- **Reversibility (qualitative):** ease and cost of undoing a decision.
- **Decision latency (project metric):** time from a major decision request to documented decision; useful when delays create uncertainty.

## Common mistakes
- Treating a principle as an absolute command, such as “never duplicate” or “always use inheritance.”
- Choosing a criterion only because it favors a preferred solution.
- Inventing precise ratings without evidence or explaining the scale.
- Hiding trade-offs in a design and claiming all qualities are maximum.
- Confusing abstraction with a layer that has no useful boundary.
- Using design by contract as a substitute for tests and runtime validation.
- Adding reuse and flexibility without a likely change or requirement.

## Exam prep
### Likely 2-mark questions
1. **Define high cohesion and low coupling.** Cohesion is related responsibility within an element; coupling is knowledge/dependency between elements; good design has high cohesion and low coupling.
2. **What is information hiding?** Concealing implementation details behind a stable interface.
3. **Give four design principles.** Divide and conquer, abstraction, information hiding, low coupling, high cohesion, reuse, testability, defensive design, simplicity, portability.
4. **What four parts are in a design decision record?** Issue, alternatives, criteria, decision/rationale, consequences/risks.
5. **Write the weighted-score formula.** `score = Σ(weight × rating)`.
6. **What is design by contract?** Preconditions, postconditions, and invariants specifying an operation's obligations.

### Long-answer answer hints
- “Explain principles leading to good design”: give at least eight principles, benefits, trade-offs, and a GPS/WMITS example.
- “How are good design decisions made?” issue, alternatives, criteria, evidence, trade-off, decision, verification, and consequences.
- “Compare coupling and cohesion”: define, examples, causes, and effects on change/testing.
- “Apply a weighted decision matrix”: show criteria/weights/ratings, calculate totals, discuss uncertainty and judgment.
- “When should you prototype?” unknown user workflow, algorithm, performance, interface, or integration risk; define fidelity and exit criterion.

### Decision sheet
```text
Issue → alternatives → criteria/evidence → decision
       → consequences/risk → verification → revisit condition
```
