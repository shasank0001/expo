---
subject: oose
unit: 4
topic: software-architecture-model
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# Software Architecture Model
## Overview
A software architecture is the fundamental organization of a system: its components, responsibilities, interfaces, relationships, data flow, deployment, and governing principles. It is more than a diagram or a list of technologies. It explains the major structural decisions that constrain the rest of design and implementation.

An architecture model is a deliberate, documented view of that organization. Good models make dependencies, boundaries, quality trade-offs, runtime structure, and change points visible before detailed code is written. They also give teams a common language for review and evolution.

## Explanation
### 1. Purpose of architecture
Architecture answers questions such as:
- What major subsystems/components exist?
- What responsibility does each own?
- Which interfaces and data cross the boundaries?
- How do components interact at runtime?
- Where do components run?
- Which qualities does the structure promote or threaten?
- How can the system evolve without rewriting everything?

Architecture is especially important because early structural decisions affect cost, reliability, security, performance, and maintainability. It provides constraints and freedom: a stable architecture does not specify every algorithm, but it prevents local choices from violating system-wide qualities.

### 2. Contents of an architecture model
A useful model contains the following views or descriptions.

#### Logical breakdown
The system is divided into subsystems or packages with high cohesion and low coupling. Each has a responsibility, service, interface, and owned data. A Facade or explicit API may hide internals. The breakdown should follow meaningful variation and change, not just code-file organization.

#### Interfaces
Interfaces describe the operations, messages, events, data formats, errors, security, timing, and compatibility visible between components. An interface is a contract; it should be small, coherent, and versioned. Interfaces are among the most important configuration items because changes can affect many clients.

#### Runtime dynamics
The model describes how components collaborate: request/response, publish/subscribe, event sequences, transaction boundaries, concurrency, failure, timeout, retry, and recovery. Component diagrams alone do not show this.

#### Shared data and ownership
Identify authoritative stores, caches, files, streams, and messages. State who can read/write, consistency, transaction, replication, retention, and migration behavior. Avoid unclear shared mutable state.

#### Components and technology
Record major software components, libraries, frameworks, external services, hardware/platform choices, and likely obsolescence points. Technology selection is a consequence of requirements and constraints, not the architecture itself.

#### Deployment
Show nodes/devices/cloud resources, artifacts, communication paths, trust boundaries, scaling, redundancy, backup, and monitoring. A logical architecture that cannot be deployed or recovered is incomplete.

#### Quality and rationale
Link the structure to performance, security, availability, usability, maintainability, portability, cost, and schedule criteria. Record alternatives, why the model was chosen, and the risks accepted.

### 3. Developing an architecture model
1. Review principal requirements, use cases, domain rules, and nonfunctional criteria.
2. Identify major quality drivers and constraints.
3. Sketch several structural alternatives, possibly with different teams.
4. Choose an architectural style/pattern using the forces in the context.
5. Group classes into cohesive subsystems and define services.
6. Define component interfaces, data ownership, and communication.
7. Map components to processors, devices, and deployment nodes.
8. Walk each major use case through the model, including exceptions.
9. Evaluate performance, security, failure, change, and testability.
10. Review, record decisions, baseline the model, and update it deliberately.

### 4. Stability and evolution
A stable architecture is not frozen. It means new features normally fit through existing components and interfaces, with only small architectural changes. Isolate likely variation: user interface, database, external provider, protocol, and hardware. Keep the model readable and versioned. If every new requirement causes a new cross-cutting dependency, revisit the boundaries.

### 5. Architectural quality criteria
- **Modularity:** responsibilities are separated into understandable parts.
- **Cohesion:** parts are internally related.
- **Coupling:** dependencies are limited and explicit.
- **Abstraction:** clients use stable services rather than internals.
- **Reuse:** suitable components and services can be shared.
- **Flexibility:** likely changes are isolated.
- **Testability:** units and boundaries can be exercised independently.
- **Security:** trust boundaries, identity, authorization, and audit are designed in.
- **Availability/performance:** critical flows, capacity, failure, and recovery are addressed.
- **Traceability:** requirements and risks map to architectural elements.

### 6. Architecture diagrams and documents
Package, component, deployment, and interaction diagrams are useful, but an architecture model also needs prose, interface contracts, data descriptions, quality rationale, and decision records. A single diagram cannot show all views. Keep names consistent across the model.

## Worked examples
### Example 1: GPS architecture
The model shows mobile client, API, route-planning service, map repository, traffic provider, cache, and database. The API owns authentication and request validation; the planning service owns route calculation; the repository owns map access. A cache is introduced for performance with a stated stale-data policy. The deployment view shows offline maps on devices and a fallback when traffic is unavailable.

### Example 2: WMITS architecture
A mobile client submits inspections to an application service. The service authorizes the user, validates domain rules, stores the inspection through a repository, and writes an audit event. A database and object/file storage are separate nodes. The architecture identifies synchronization as a major risk and provides a recovery path. This is more than “client + server”; responsibilities and failure behavior are specified.

### Example 3: Two sketches
One team proposes a single monolithic program; another proposes a layered service architecture. The review finds the monolith is simpler for a small pilot, while the layered design is better for independent security/reuse and future channels. The team chooses a modular monolith for Release 1, with explicit interfaces that permit later extraction. The rationale and revisit trigger are recorded.

### Example 4: Architecture walkthrough
During a use-case walkthrough, the model shows the client directly reading the database for a dashboard. This violates the service ownership and creates an unauthorized-data risk. The model is changed so the dashboard queries a query service, and an access-control test is added.

## Key terms & formulas
- **Software architecture:** fundamental structure and set of principles governing system organization.
- **Architecture model:** documented representation of components, interfaces, interactions, data, deployment, and quality rationale.
- **Subsystem:** cohesive, replaceable group with a service/interface.
- **Component:** modular software unit implementing one or more interfaces.
- **Service:** externally visible behavior provided by a component.
- **Interface contract:** operations, data, errors, timing, and compatibility.
- **Runtime dynamics:** messages, control, concurrency, and failure behavior at execution.
- **Data ownership:** authority and rules for a data element.
- **Trust boundary:** separation with different security assumptions.
- **Architectural stability:** ability to add features with small structural change.
- **Change amplification (qualitative):** the number of artifacts that must change for one requirement; lower is usually better.
- **Architecture coverage (check):** critical use cases with an owned component/interface/path ÷ critical use cases × 100%.

## Common mistakes
- Equating architecture with a technology list or a cloud diagram.
- Showing components but no interfaces, data ownership, or runtime behavior.
- Ignoring deployment, failure, security, and recovery.
- Choosing a style before understanding quality drivers and use cases.
- Hiding decisions and alternatives; the model then looks authoritative but cannot be maintained.
- Making every component a network service and ignoring cost/latency.
- Allowing shared data and circular dependencies that undermine ownership.

## Exam prep
### Likely 2-mark questions
1. **Define software architecture.** The fundamental organization, responsibilities, interfaces, interactions, data, deployment, and principles of a system.
2. **List five contents of an architecture model.** Logical breakdown, interfaces, runtime dynamics, shared data, components/technology, deployment, and rationale.
3. **Why is architecture important?** Early structural decisions strongly affect quality, cost, change, and integration.
4. **What is architectural stability?** New features can be added with small structural changes because boundaries and interfaces are well chosen.
5. **Name two architectural models/views.** Component, deployment, package/subsystem, or interaction diagram; any two.
6. **What is a traceable architecture?** A model whose elements link to requirements, risks, decisions, and tests.

### Long-answer answer hints
- “Explain contents of a software architecture model”: logical subsystems, interfaces, dynamics, data, components/technology, deployment, quality, and rationale; diagram one example.
- “How do you develop an architecture model?” requirements/drivers → alternatives → pattern → decomposition → interfaces/data → deployment → walkthrough/review → baseline/evolution.
- “Differentiate architecture and detailed design”: architecture establishes system-wide structure and constraints; detailed design specifies class/algorithm/local implementation.
- “Apply architecture to WMITS”: mobile client, application, repository, database/storage, audit, auth, sync, deployment, and failure paths.
- “Evaluate an architecture for quality”: modularity, coupling, cohesion, security, performance, testability, flexibility, and evidence.

### Architecture view checklist
```text
Components → interfaces → interactions → data ownership → deployment
           → quality/risk rationale → traceable requirements
```
