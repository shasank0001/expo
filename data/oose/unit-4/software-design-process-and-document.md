---
subject: oose
unit: 4
topic: software-design-process-and-document
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# Software Design Process and Design Document
## Overview
Software design turns the validated requirements and analysis model into a solution that can be implemented, tested, deployed, and changed. It chooses responsibilities, structures data and control, defines interfaces, selects patterns and architecture, and addresses quality attributes. Design is not just drawing class diagrams: it is making and recording deliberate decisions.

A design process gives the team a way to move from the problem to a coherent design, evaluate alternatives, refine the solution against quality goals, and preserve the reasoning for future maintainers. A good design document records the important decisions and their alternatives, not every line of code.

## Explanation
### 1. Inputs and outputs
Inputs include:
- problem and scope;
- stakeholder needs and use cases;
- functional and nonfunctional requirements;
- domain and analysis models;
- constraints, assumptions, risks, and existing assets;
- organizational and technology standards.

Outputs include:
- architecture and subsystem/component design;
- class, interface, sequence, state, activity, and deployment models as needed;
- data and persistence design;
- UI and interaction design;
- security and access-control design;
- testability and verification strategy;
- design decisions and trade-off rationale;
- a design document and traceability links.

### 2. The design process
#### Step 1: Establish design goals
Translate requirements into qualities the design should optimize. A requirement such as “95% of route requests complete within two seconds” is a constraint; a goal such as “minimize unnecessary data loading” guides alternatives. State priorities because performance, security, usability, cost, and maintainability can compete.

#### Step 2: Review the analysis model
Walk through use cases and scenarios. Identify entities, boundary/interface objects, control objects, domain rules, and exceptions. Check that every requirement is represented and that the model is not already biased toward an implementation.

#### Step 3: Choose an architecture
Decide the overall organization of the system: layers, client/server, services, repository, broker, pipeline, or another style. Select a style because of its forces and consequences, not because it is fashionable. Sketch alternatives before committing.

#### Step 4: Decompose into subsystems and components
Group related responsibilities into cohesive subsystems with clear services and interfaces. Minimize coupling across boundaries. Identify which parts can be implemented/reused independently and which parts require close coordination.

#### Step 5: Design classes and interfaces
Assign responsibilities to classes, define attributes and operations, and protect invariants. Create interfaces at unstable or variable boundaries. Use information hiding, low coupling, polymorphism, and composition when appropriate. Keep domain concepts separate from UI and persistence details.

#### Step 6: Design data and persistence
Identify persistent entities, identifiers, relationships, validation, transactions, concurrency, retention, migration, and recovery. Decide where data is owned and how it is accessed. A class diagram is a conceptual model; it may not map one-to-one to tables.

#### Step 7: Design user interaction and control flow
Define screens/commands, workflows, validation, error messages, accessibility, and state transitions. Choose procedure-driven, event-driven, or concurrent control where the use cases require it. Model normal and failure flows.

#### Step 8: Address nonfunctional qualities
Use design techniques and measures for performance, reliability, security, usability, maintainability, portability, and capacity. Make trade-offs explicit. For example, caching improves response time but may make data stale and complicate concurrency.

#### Step 9: Make and record decisions
For each major decision, record the issue, alternatives, criteria, decision, rationale, consequences, and risks. A decision record prevents a later maintainer from unknowingly reversing a deliberate choice.

#### Step 10: Review and refine
Conduct design reviews and walk through each important use case through the design. Check completeness, consistency, feasibility, testability, security, and alignment with requirements. Refine the model and update traceability. Design is iterative because evaluation exposes missing information.

#### Step 11: Prepare for implementation and verification
Turn the design into implementation units, APIs, build/deployment artifacts, test cases, prototypes, and a plan. Ensure developers can implement the design without guessing and testers can derive meaningful checks.

### 3. Design principles in practice
Good design emphasizes:
- **divide and conquer:** split a large problem into understandable parts;
- **abstraction and information hiding:** expose what is needed, hide decisions;
- **modularity and high cohesion:** keep related responsibilities together;
- **low coupling:** limit knowledge shared between modules;
- **reuse:** prefer reliable existing components when they fit;
- **increase flexibility:** isolate likely variation;
- **design for testability/defensiveness:** make behavior observable and validate inputs;
- **anticipate obsolescence:** contain technologies likely to change.

These principles are not a substitute for context. A highly reusable design that is costly to understand or cannot meet a security requirement may be poor.

### 4. Design document
A design document is a controlled explanation of a system or feature. Lethbridge and Langanière recommend recording:
- **purpose and requirements trace**;
- **general priorities**;
- **outline of the design**;
- **major design issues**, alternatives, decision, and rationale;
- **other important details**.

A fuller document can contain architecture, diagrams, interfaces, data, error handling, security, performance, deployment, tests, risks, and open issues. Tailor the depth to the audience and risk. A skilled implementer needs stable contracts and rationale, not automatically derivable method lists. Code comments are better for local implementation detail.

### 5. Review criteria
A design is ready to implement when:
- every applicable requirement and scenario is represented;
- responsibilities and interfaces are clear;
- alternatives and trade-offs are documented;
- invariants and error behavior are explicit;
- quality goals have measurable verification approaches;
- components can be implemented and tested independently where intended;
- deployment, migration, security, and maintenance concerns are addressed;
- no unresolved high-risk decision is hidden.

## Worked examples
### Example 1: WMITS design process
The team starts from inspection use cases and state rules. It chooses a client/server architecture with a mobile UI, application service, repository, and central database. `Inspection` owns status invariants; `AuthorizationService` checks roles; a repository isolates persistence. Alternatives include a direct client-to-database design (rejected for security) and a fully remote service (deferred for offline field work). The document records each decision.

### Example 2: SimpleChat feature design
For commands such as `#block`, the design issue is where to store blocked users. Storing them in a connected client is invalid because a client may be offline. The team stores the list with the server-side client record, defines the message protocol, updates the UI, and adds tests for unknown, self, duplicate, and offline targets. The rationale is recorded.

### Example 3: Performance trade-off
A route search is slow because every request recalculates map data. The team considers caching, indexing, or precomputation. It measures each option, chooses a bounded cache, and records the possible stale-data consequence. The design links the change to performance requirements and tests.

### Example 4: Design review finds a gap
A use case for returning an inspection exists, but no class owns the return reason or state transition. The design review adds a domain operation, an audit event, and an integration test. The defect is fixed before three teams implement incompatible interpretations.

## Key terms & formulas
- **Design:** creation of a solution architecture and implementation model satisfying requirements and quality goals.
- **Design goal:** desirable quality used to guide choices.
- **Requirement:** mandatory, measurable target; it constrains the design.
- **Subsystem:** cohesive, replaceable group of classes/services with a defined interface.
- **Interface contract:** operations, data, errors, timing, and compatibility visible across a boundary.
- **Trade-off:** benefit gained at the cost of another quality or resource.
- **Design rationale:** reason an alternative was chosen, with evidence and consequences.
- **Traceability:** links among requirement, design element, implementation, and test.
- **Testability:** ease of observing and exercising the design with meaningful checks.
- **Design volatility:** frequency/cost of design changes after baseline; use to improve boundaries, not to hide learning.
- **Decision value (qualitative):** benefit of a decision minus implementation and maintenance cost; compare with risk and urgency.

## Common mistakes
- Treating design as writing code in advance and never revisiting the analysis.
- Drawing a class diagram without a responsibility, interface, or quality goal.
- Choosing architecture before reviewing use cases and constraints.
- Recording only the final choice and losing the rationale.
- Putting every low-level detail in the design document and none of the important trade-offs.
- Claiming a component is reusable or decoupled without evidence.
- Declaring design complete while exception, security, migration, and operational paths are absent.
- Using a pattern because its name is famous rather than because its forces fit.

## Exam prep
### Likely 2-mark questions
1. **Define software design.** The process of turning requirements and analysis into a solution structure, interfaces, behavior, and implementation decisions.
2. **List four design-process activities.** Establish goals, review analysis, choose architecture, decompose subsystems, design classes/interfaces, address quality, review, and document.
3. **What is a design decision record?** A record of the issue, alternatives, criteria, choice, rationale, consequences, and owner/date.
4. **Why trace requirements to design?** To check coverage and understand the effect of a change on the solution.
5. **Differentiate a design goal and a requirement.** A goal guides optimization; a requirement is an agreed acceptance target.
6. **What makes a design document useful?** It communicates important structure, decisions, interfaces, rationale, and quality/verification information to implementers and maintainers.

### Long-answer answer hints
- “Explain the software design process”: goals → analysis → architecture → decomposition → classes/data/control → nonfunctional design → review → document → test handoff.
- “Explain how to make a good design document”: purpose, priorities, outline, major issues/alternatives, rationale, details, traceability, and what to omit.
- “Apply design process to WMITS”: list use cases, identify subsystem boundaries, choose persistence/authorization, address offline/security, and record decisions.
- “Differentiate analysis and design model”: problem/what versus solution/how, with an example.
- “How do you review a design?” coverage, consistency, responsibilities, interfaces, quality goals, failure handling, testability, deployment, and risk.

### Design loop
```text
Requirements + analysis → goals/alternatives → architecture/components
          ↑                    ↓
          └──── review, evidence, refinement ← class/data/control/quality design
```
