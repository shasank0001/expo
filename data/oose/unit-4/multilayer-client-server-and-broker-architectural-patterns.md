---
subject: oose
unit: 4
topic: multilayer-client-server-and-broker-architectural-patterns
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# Multilayer, Client–Server, and Broker Architectural Patterns
## Overview
Architectural patterns organize a system at a high level. This note covers three patterns in the syllabus: **Multilayer**, which builds a system from levels of abstraction; **Client–Server**, which separates service consumers from providers; and **Broker**, which adds an intermediary that locates and connects distributed objects or services. Architectural patterns are reusable structures with forces and consequences, not rigid recipes.

The right pattern depends on the system's data, interaction, deployment, security, and change requirements. A project may combine patterns—for example, a client-server application with internal layers and a broker for notifications—but the interfaces and responsibilities must remain clear.

## Explanation
### 1. Multilayer architectural pattern
#### Structure
In a layered system, each layer communicates with the layer immediately below it through a defined interface. A higher layer sees lower layers as services and does not depend on their implementation. A typical stack is:

```text
Presentation / user interface
          ↓
Application / use-case services
          ↓
Domain / business rules
          ↓
Persistence / data access
          ↓
Operating system, devices, network
```

The exact names vary. A presentation layer handles interaction; application logic coordinates use cases; domain logic holds business rules; infrastructure provides database, files, network, and other services. Layers may be packages, processes, or services. The pattern is a logical separation even when the code is deployed together.

#### Forces and benefits
- **Divide and conquer:** each layer has a manageable responsibility.
- **Abstraction:** a client requests a service without knowing implementation details.
- **Low coupling:** lower layers do not depend on higher layers; interfaces mediate.
- **High cohesion:** related functions stay in one layer.
- **Reuse:** a database or network layer can serve different applications.
- **Portability/obsolescence:** vendor and platform details are concentrated in lower layers.
- **Testability:** domain and application layers can be tested without a real UI or network.
- **Security and defensive checks:** boundary and service layers validate input and access.

#### Challenges
- Passing data through many layers adds overhead and complexity.
- A change may cross several layers.
- “Any layer may call any lower layer” can destroy the discipline; define allowed dependencies.
- Duplicate domain logic across layers leads to inconsistent rules.
- A too-generic lower layer may not fit the application.

Use a façade or service interface at a layer boundary, keep domain rules in one place, and review dependency direction.

### 2. Client–Server architectural pattern
#### Structure
A **server** provides services; a **client** requests them. The client often handles user interaction and local validation, while the server owns authoritative data, business transactions, or shared services. A server need not know the individual client beyond the request and authorization context. A client may call one or more servers.

```text
Client 1 ─┐
Client 2 ─┼── protocol/RPC/API ──> Server ──> database/services
Client 3 ─┘
```

A request/response interaction usually has:
1. client initialization and connection;
2. server listening/accepting connections;
3. request and authentication;
4. validation and service execution;
5. response or error;
6. connection handling or persistence;
7. disconnection and recovery.

The server may be stateless or stateful, synchronous or asynchronous. Thin clients move more work to the server; fat clients perform more local processing. The choice affects offline capability, latency, security, and maintenance.

#### Benefits
- centralizes authoritative data and business rules;
- permits many clients to share one service;
- separates client and server implementation;
- supports heterogeneous devices and distributed access;
- scales by adding servers, load balancing, or specialized services;
- enables reuse of server-side frameworks.

#### Challenges
- network latency, disconnections, timeouts, and partial failures;
- version compatibility between independently deployed clients and servers;
- server availability and load;
- authentication/authorization on every request;
- duplicate validation or business logic in clients;
- testing distributed interactions and race conditions.

Use versioned protocols, idempotent operations, timeouts, retries with limits, health checks, and clear ownership of rules. A disconnected client must not silently pretend that a write succeeded.

### 3. Broker architectural pattern
#### Structure and purpose
A **broker** is an intermediary that lets a client request a service or locate a remote object without knowing where the implementation is located. A client often uses a proxy or stub; the broker locates/activates the remote object, forwards the request, and returns the result. This transparently distributes aspects of a system across nodes.

```text
Client → Proxy/stub → Broker → Remote object/provider
             ↑            │             ↓
             └── result/exception ───────┘
```

The broker can provide registration, lookup, routing, object activation, security context, and forwarding. CORBA is a classic example; a service registry, message broker, or API gateway may play a related role in a modern system, but a broker pattern is not simply any network proxy.

#### Benefits
- hides remote location and activation details;
- separates client and remote implementation;
- allows independent deployment and reuse of providers;
- centralizes lookup, routing, and sometimes security/quality policy;
- makes a distributed system easier to evolve if the protocol is stable;
- can support multiple clients and dynamic providers.

#### Challenges
- the broker is a potential single point of failure and performance bottleneck;
- location transparency can hide network latency and failures;
- serialization, compatibility, and version issues are difficult;
- debugging a request across proxy, broker, and remote object is harder;
- security and trust must cover every hop;
- overengineering can make a simple local system more complex.

Use replication/failover where availability matters, validate and bound requests, expose status and timeouts, and define what happens when no provider is registered. A broker should not become an untyped “god service.”

### 4. Choosing and combining patterns
- Use **multilayer** when concerns and levels of abstraction must be separated, even in one deployment.
- Use **client–server** when clients need shared remote services or authoritative central data.
- Use **broker** when location transparency, dynamic lookup, or remote object/service distribution is important.
A common design is a layered client-server application: mobile/web clients call a server API; server layers separate application, domain, and persistence; a broker or service registry supports specialized providers. Each pattern should solve a stated force, and interfaces should make the combination understandable.

## Worked examples
### Example 1: Layered WMITS
A mobile UI calls an inspection application service. The service invokes domain validation and authorization, then an audit service and repository. The repository owns database and file storage. No layer directly accesses a lower layer except through its defined service. Unit tests exercise domain rules without a phone; integration tests exercise the repository.

### Example 2: Client–server GPS
A mobile client validates basic input and sends a route request to a route server. The server checks account permissions, calls the route engine and map repository, and returns a result. A timeout is reported; the client does not claim a route was calculated. The server can be scaled behind a load balancer.

### Example 3: Brokered route provider
The application asks a broker for a `MapProvider` with the required region and interface. The broker selects a registered provider and returns a proxy/stub. The client calls the proxy; the broker forwards the remote request. If no provider is available, the route service uses an offline map or returns a clear error.

### Example 4: Layer + broker
A notification service uses a broker so mobile clients can be located across networks. The service itself is layered: application orchestration, domain notification rules, and persistence. This avoids making the mobile client know broker addresses or provider implementations.

### Example 5: Client validation trap
A client checks “age at least 18” but the server accepts the request without repeating the rule. A malicious client bypasses it. The server remains authoritative; client validation is a usability aid, not a security control.

## Key terms & formulas
- **Architectural pattern:** reusable high-level organization with forces and consequences.
- **Layer:** responsibility level communicating through a defined interface.
- **Layer cohesion/coupling:** related behavior within a layer and dependencies between layers.
- **Presentation/application/domain/infrastructure layer:** common logical divisions for UI/use cases/business rules/platform services.
- **Client:** component requesting a service.
- **Server:** component providing a service and often owning shared state.
- **Thin/fat client:** how much presentation/business work is placed on the client.
- **Broker:** intermediary for lookup, routing, activation, and forwarding.
- **Proxy/stub:** client-side representative of a remote object.
- **Location transparency:** client does not need to know the provider's physical location.
- **Round-trip latency:** request travel + processing + response travel; network calls add it to local operation time.
- **Layer dependency rule (ideal):** higher layers may call lower services; lower layers do not depend on higher ones.
- **Availability estimate (qualitative):** fewer single points of failure and redundant providers improve the chance of service; monitoring and recovery are still required.

## Common mistakes
- Calling any folder a layer without a defined interface or responsibility.
- Allowing every layer to call every other layer and creating hidden coupling.
- Assuming client–server means the client is trusted; all important validation and authorization belong server-side.
- Confusing a broker with a load balancer, database, or any network service.
- Hiding network failure and latency behind a proxy without timeouts or status.
- Comparing patterns as if one is always best instead of matching the forces.
- Combining patterns without clear boundaries and data ownership.
- Ignoring protocol versioning and deployment compatibility.

## Exam prep
### Likely 2-mark questions
1. **Define the Multilayer pattern.** A structure of levels of abstraction where each layer uses the service interface of the layer below.
2. **Give two benefits of layers.** Low coupling, abstraction, cohesion, reuse, testability, portability—any two.
3. **Define Client–Server.** An architecture in which clients request services from one or more servers that provide shared functionality/data.
4. **Why must the server validate requests?** Clients are untrusted and may be outdated or malicious; the server owns authoritative rules and data.
5. **Define a broker.** An intermediary that locates, activates, or routes requests between clients and remote objects/services.
6. **Give one broker benefit and one risk.** Benefit: location transparency; risk: bottleneck, latency, or single point of failure.
7. **How can the patterns be combined?** Use layers inside a server and client–server or broker communication between deployments, with clear interfaces.

### Long-answer answer hints
- “Explain Multilayer, Client–Server, and Broker”: structure, responsibilities, interactions, benefits, challenges, and deployment examples.
- “Choose an architecture for WMITS”: layered server, mobile client, repository, broker only if needed; justify with security/offline requirements.
- “Compare client–server and broker”: direct service request versus intermediary lookup/routing and location transparency.
- “Why are layers testable?” each contract can be exercised with substitutes and independent fixtures.
- “Draw architecture sketches”: include components, interfaces, protocols, nodes, and failure paths, not only boxes.

### Sketch
```text
Layered:       UI → Application → Domain → Data/Platform
Client/server: Clients → API/Server → shared data
Broker:        Client → Proxy → Broker → Provider
Combined:      Layered client/server + broker for discovery
```
