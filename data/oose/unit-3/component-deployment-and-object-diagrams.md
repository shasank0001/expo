---
subject: oose
unit: 3
topic: component-deployment-and-object-diagrams
syllabus_ref: CSM3102 Unit-III
status: draft
---
# Component, Deployment, and Object Diagrams
## Overview
Component, deployment, and object diagrams describe different levels of a system. A **component diagram** shows the major replaceable or deployable software pieces and the interfaces between them. A **deployment diagram** shows where software artifacts run on nodes such as servers, devices, or containers, and the communication paths between them. An **object diagram** shows a snapshot of particular instances and their links.

Together they answer: What software pieces exist? Where do they run? What do the pieces or nodes need from one another? What does a representative runtime state look like? The diagrams should use the same components, interfaces, and domain terms as the class and behavior models.

## Explanation
### 1. Component diagrams
A **component** is a modular, replaceable part of a system that realizes one or more interfaces and contains its implementation details. It may be a subsystem, application module, service, library, executable, database access component, or deployable unit. The component diagram is a high-level static view; it does not show every class.

A **provided interface** is offered by a component. A **required interface** is expected by it. A connector (assembly connector or delegation connector) shows how requirements and provisions meet. Examples of interfaces include `Search`, `Payment`, `Notification`, and `MapData`.

A component diagram should be at a useful abstraction level. Showing every Java class turns it into a class diagram; showing only “the system” gives no information. The component name should represent responsibility or deployable role.

### 2. Component types and packaging
Components can be categorized by deployment or responsibility, such as application, service, library, database adapter, UI, or external provider. Packaging (`<<package>>`) groups related elements, while a component is a replaceable implementation unit. A deployment artifact is a file, package, executable, or image containing components. Keep these concepts distinct in notes and diagrams.

### 3. Deployment diagrams
A **node** represents an execution environment or device: server, workstation, mobile device, database server, virtual machine, cluster, or cloud service. Nodes can be nested to show deployment hierarchy. An **artifact** is a physical representation of a component or model placed on a node. A **communication path** shows connectivity and may carry a protocol such as HTTPS, JDBC, or TCP.

A deployment diagram can include:
- clients and user devices;
- web, application, service, and database tiers;
- message brokers and caches;
- network zones, trusted/untrusted boundaries, and security connections;
- replicas, availability zones, and failover targets;
- environment or deployment-unit labels.

It answers runtime topology and communication, not the internal algorithm of a component.

### 4. Node types and communication
A node may be physical or virtual. A client node may call an application node over HTTPS; the application node may query a database over an internal protocol; mobile clients may reach a broker for notifications. The protocol and data contract should match the interface requirements. Show network boundaries and trust levels when security or failure behavior depends on them.

### 5. Object diagrams
An object diagram is a snapshot of particular classifier instances, their property values, and links. It can show:
- a representative valid configuration;
- an invalid or boundary configuration for analysis;
- links created by a scenario;
- identity and multiplicity in action;
- collections and association instances.

Object diagrams are useful for teaching, reviews, and debugging a model. They are not normally the primary specification of all possible runtime states, and a large production object graph is not usually drawn.

### 6. Connecting the diagrams
A class `RouteService` may be implemented by component `RouteServiceImpl`; that component is deployed as artifact `route-service.war` on an application node. A `Notification` interface is a provided interface; the broker component requires it. A test scenario produces object links between `Route` instance R7 and `MapProvider` instance P2. These links preserve traceability.

### 7. Boundaries, security, and failure
Deployment diagrams should show trust boundaries and sensitive interfaces where relevant. A mobile client is outside the trusted boundary; a database may be reachable only from an application node. If the diagram shows a public direct database path, it reveals a design/security issue. Failure paths, load balancers, backups, and replica relationships can be shown when they affect availability or recovery.

### 8. Quality checks
- Does each component have a clear responsibility and replaceable boundary?
- Are provided and required interfaces compatible and named consistently?
- Are deployment nodes and artifacts distinguishable?
- Do communication paths match the real protocol and trust model?
- Are replicas, queues, and external providers visible where they matter?
- Do object diagrams use the same names, multiplicities, and invariants as class diagrams?

## Worked examples
### Example 1: GPS deployment
```text
[Mobile device] --HTTPS--> [Web/API node]
                         --> [Route service]
                         --> [Map database]
                         --> [Traffic API (external)]
```
The mobile app and route service are components on nodes; the traffic provider is an external system. A test covers an offline map and an unavailable traffic API, so the diagram's path is tied to behavior.

### Example 2: WMITS component diagram
```text
[Inspection UI] --<<uses>>--> [InspectionService]
[InspectionService] --<<realizes>>--> [Audit interface]
[InspectionService] --> [Repository] --> [Database adapter]
```
The service may replace the repository implementation without changing the UI. The audit requirement is a provided/required interface, not an arbitrary line.

### Example 3: Object snapshot
```text
[U04: Inspector] ──assignedTo──> [I17: Inspection]
[S12: Site]       ──contains────> [I17]
[E88: Evidence]   ──attachedTo──> [I17]
```
The diagram confirms that a site can contain many inspections and that evidence belongs to one inspection. It can be used to ask whether an evidence file can exist without an inspection.

### Example 4: Availability design
A broker node has two consumer nodes connected by separate communication paths. The deployment diagram marks a failure/replication relationship and the sequence diagram shows retry. Without that information, a simple single-node picture can hide a single point of failure.

## Key terms & formulas
- **Component:** modular/replaceable software unit implementing interfaces.
- **Provided interface:** interface a component offers to clients.
- **Required interface:** interface a component expects from another.
- **Connector:** relationship showing interface satisfaction/use.
- **Node:** execution environment or device in a deployment.
- **Artifact:** physical/deployable representation of a component.
- **Deployment diagram:** nodes, artifacts, communication, and runtime structure.
- **Object diagram:** snapshot of instances and links.
- **Trust boundary:** separation between components/nodes with different security assumptions.
- **Replacement test (qualitative):** can one component be swapped for another conforming to the same interface without changing clients? If not, the boundary may be too coupled.
- **Deployment coverage (project check):** components with a defined deployment placement / total deployable components × 100%.

## Common mistakes
- Using a component diagram as a detailed class diagram.
- Showing nodes but no artifacts or communication protocols.
- Calling every folder a component or every server a component.
- Mixing physical nodes and logical classes without explaining the level.
- Using object diagrams as if they show every possible runtime object.
- Omitting external systems and trust boundaries, making the architecture look simpler than reality.
- Using different names for an interface in the component, class, and deployment views.

## Exam prep
### Likely 2-mark questions
1. **Differentiate a component and a node.** A component is a software unit; a node is a runtime environment/device.
2. **What is a component diagram?** A structural diagram of software components and their interfaces/connectors.
3. **What is a deployment diagram?** A diagram of nodes, artifacts, and communication paths showing where software runs.
4. **Define a provided/required interface.** An interface a component offers / an interface it expects from a collaborator.
5. **What is an object diagram used for?** Showing a snapshot of instances, values, and links for a scenario or review.
6. **Why show trust boundaries?** Security, access, and failure assumptions can change across runtime locations.

### Long-answer answer hints
- “Explain component and deployment diagrams”: definitions, elements, purpose, relationships, and a GPS/WMITS example.
- “Draw a component diagram for a web application”: UI, services, repository, database adapter, external API, and interfaces.
- “Draw a deployment diagram for a chat system”: mobile/web clients, API, broker, database, cache, and protocols; mark trust boundaries.
- “Differentiate component, node, artifact, and interface”: logical software unit, execution place, physical representation, and contract.
- “Use an object diagram to explain multiplicities”: show particular instances and links, then compare with the class rule.

### Sketch
```text
Component view:  [UI] --uses--> [Service] --realizes--> [Repository]
Deployment view: [phone] --HTTPS--> [app node] --SQL--> [DB node]
Object view:     [I17] ──assignedTo──> [U04]
```
