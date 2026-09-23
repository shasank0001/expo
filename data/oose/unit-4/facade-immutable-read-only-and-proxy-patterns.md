---
subject: oose
unit: 4
topic: facade-immutable-read-only-and-proxy-patterns
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# Façade, Immutable, Read-Only Interface, and Proxy Patterns
## Overview
These four patterns solve different interface and control problems. A **Façade** gives clients a simple unified entry point to a complex subsystem. An **Immutable** object cannot change after construction. A **Read-Only Interface** gives ordinary clients observation access while allowing selected privileged collaborators to mutate a separate mutable representation. A **Proxy** stands in for another object or service to control access, location, loading, or lifecycle.

They are often combined: a façade can hide a proxy and immutable domain objects, while a read-only interface can protect privileged views. Each pattern has a specific contract; the goal is not merely to add extra classes.

## Explanation
### 1. Façade pattern
#### Context and problem
A subsystem contains many interacting classes, services, data structures, and ordering rules. If every client knows all of them, clients become coupled to implementation details. A change inside the package may require changes throughout the application, and a simple operation requires complex orchestration.

#### Solution
Introduce a `Façade` class with a small, coherent set of higher-level operations. The façade delegates to package classes and hides their structure. Package internals may call one another directly; external clients use the façade.

```text
Client → Airline Façade
             ├→ RegularFlight
             ├→ Booking
             └→ Payment/Reservation services
```

A façade does not necessarily remove subsystem access for specialized clients; it provides a preferred simple entry point. It can expose transactions, validation, authorization, and error translation in addition to delegation.

#### Benefits
- reduces client knowledge and coupling;
- hides subsystem orchestration and ordering;
- provides a stable high-level API;
- supports reuse and replacement of internals;
- gives one place for cross-cutting policy such as logging or security.

#### Risks
- a façade can become a “god object” if it contains all business logic;
- adding every internal operation defeats simplification;
- a façade that exposes mutable internals leaks encapsulation;
- additional indirection can affect performance and debugging;
- clients that bypass it may create inconsistent workflows.

### 2. Immutable pattern
#### Intent
An immutable object’s state never changes after it is created. This is different from an object that is only *mostly* unchanged or that exposes no setters to a particular client.

#### Solution rules
- initialize all required state in the constructor or factory;
- do not expose mutable fields or mutable internal collections;
- do not provide mutators that alter the object;
- return defensive copies or immutable views of collections;
- make query methods side-effect free;
- when a “change” is required, return a new instance (often called a persistent or functional update).

```text
old = new Point(1, 2)
new = old.withX(5)   // old remains (1, 2)
new.getX() == 5
```

All values used in construction should themselves be safe to retain. If an immutable object stores a mutable list and returns it, a client can change the object indirectly, creating a loophole.

#### Benefits
- simple reasoning about identity and state;
- safe sharing across threads when the class is safely published;
- fewer temporal bugs because values do not change unexpectedly;
- safe map/set keys and audit facts;
- easier caching and rollback when historical values matter.

#### Risks
- frequent “updates” may create many short-lived objects and increase allocation;
- identity-sensitive code may expect mutation;
- nested mutable collaborators can break immutability;
- construction and validation can be more involved;
- “Immutable” must be enforced by design, not just a naming convention.

### 3. Read-Only Interface pattern
#### Context and problem
Some clients should observe a value but not change it, while a smaller set of privileged classes must update it. Ordinary public/private visibility may be too broad or too narrow: making a setter public exposes mutation to everyone, while making it private prevents the authorized mutator. A read-only interface can give unprivileged clients a getter-only contract while the mutable implementation remains available to trusted mutators.

#### Solution
```text
<<ReadOnlyInterface>>
  + getName()
  + getAge()

<<Mutable>> implements ReadOnlyInterface
  - firstName
  - lastName
  + setFirstName(...)
  + setLastName(...)
  + getName()

Unprivileged client → ReadOnlyInterface
Mutator / trusted service → Mutable
```

The read-only interface exposes only observation operations. The mutable class implements it and may provide additional mutators to authorized users. The pattern is a **view of capability**, not a promise that the underlying object is globally immutable.

#### Benefits and risks
- selective access without exposing all internals;
- clients depend on a narrow, stable contract;
- supports different views of the same data;
- can separate read-only consumers from controlled writers.

Risks include a client obtaining the concrete mutable type and casting it, an implementation leaking mutable nested state, and authorization being confused with visibility. Enforce access at service and security boundaries too. Do not create a read-only subclass that merely throws exceptions for every mutator; prefer interface capability and a controlled implementation.

### 4. Proxy pattern
#### Context and problem
A client needs an object or service that is expensive to create, located remotely, protected, cached, persistent, or not yet available. Directly depending on the heavyweight object couples every client to its creation and location.

#### Solution
Define an interface that the client uses. A `Proxy` implements that interface and holds a `RealSubject`/heavyweight object. It handles the request itself when possible or forwards to the real object. Common proxy variants are:
- **virtual/proxy:** creates the real subject lazily;
- **remote proxy:** represents an object across a network;
- **protection proxy:** checks access before forwarding;
- **cache/storage proxy:** keeps a local copy or persistent representation;
- **firewall/smart proxy:** applies policy or routing.

```text
Client → <<SubjectIF>> ← Proxy ← RealSubject
                 ↘ controls creation/access/location
```

The proxy should be transparent for valid behavior but may add policy, caching, lazy loading, and error handling. It must not silently change the subject's domain invariants.

#### Benefits
- reduces client coupling to heavyweight/remote details;
- controls expensive resources;
- protects access and supports distributed location;
- enables caching, lazy loading, persistence, and virtual objects;
- gives a stable local interface.

#### Risks
- proxy behavior can be hard to distinguish from real behavior;
- extra network/cache calls affect latency and failure modes;
- stale cache data and identity mapping are difficult;
- security checks can be bypassed if clients receive the real object;
- a proxy may become a second large class with duplicated business logic.

## Worked examples
### Example 1: Airline façade
`Airline` exposes `findFlight`, `makeBooking`, and `deleteBooking`. It coordinates flight search, seat reservation, customer data, and payment. Clients do not need to know the order or internal classes. The façade is kept high-level; the booking rules remain in the appropriate domain/service classes.

### Example 2: Immutable coordinate
`Coordinate` stores latitude and longitude once and exposes `getLatitude`, `getLongitude`, and `distanceTo`. It has no setters. `withLatitude(10)` returns a new validated coordinate. A collection stores coordinates safely, and a test proves that an old coordinate is unchanged.

### Example 3: Read-only person view
An instructor receives `ReadOnlyPerson` and can view a name and ID. A registrar service receives a `MutablePerson` capability and can change the name under authorization. The public response does not expose a setter. An audit test confirms every change, and a cast/endpoint test confirms an ordinary client cannot update it.

### Example 4: Virtual route proxy
A `Route` proxy stores only the route ID and origin/destination summary. When segments are requested, it loads the heavyweight `RealRoute` from a repository, caches it if appropriate, and forwards the operation. Creating many route summaries does not load all map segments. Deletion or replacement is controlled by the proxy policy.

### Example 5: Protection proxy
A `PortfolioProxy` checks whether the current broker is assigned to a portfolio before delegating. An unauthorized request is denied and audited; the real portfolio is not loaded. This is a security boundary, not merely a performance helper.

### Example 6: Combining patterns
A WMITS façade exposes `submitInspection` to a mobile client. It validates the input, invokes a domain service, and stores an immutable audit event. A read-only query interface returns inspection summaries to a dashboard, while a remote proxy hides the server boundary. Each wrapper has one clear responsibility.

## Key terms & formulas
- **Façade:** high-level interface simplifying a subsystem.
- **Subsystem package:** related classes/services with a broader internal interface.
- **Immutable object:** object whose observable state cannot change after construction.
- **Defensive copy:** copy returned to prevent a client from mutating internal state.
- **Persistent update:** operation returning a new object rather than changing the old one.
- **Read-only interface:** capability exposing observation but not mutation.
- **Mutator:** authorized operation that changes state.
- **Proxy:** object implementing the subject interface and controlling access to a real subject.
- **Real subject/heavyweight subject:** actual implementation behind a proxy.
- **Virtual proxy:** lazy-creation proxy.
- **Protection proxy:** access-checking proxy.
- **Cache proxy:** proxy storing a local representation.
- **Transparency:** client sees the expected contract despite proxy behavior.
- **Cache hit ratio:** cache hits ÷ total requests × 100%; measure alongside staleness and invalidation cost.
- **Immutability invariant:** for all valid time `t` after construction, `state(t) = state(construction)`.

## Common mistakes
- Building a façade that contains all business logic instead of providing a high-level entry point.
- Calling a class immutable while it exposes a mutable list or setter.
- Returning a new object from an “immutable update” but mutating the old object anyway.
- Using a read-only interface and then exposing the concrete mutable class to everyone.
- Confusing a proxy with an adapter: a proxy preserves/controls a subject contract; an adapter translates a different one.
- Making a proxy duplicate all business rules instead of delegating.
- Ignoring cache invalidation, remote timeouts, authorization, and identity in proxies.
- Allowing clients to bypass a façade and mutate subsystem internals.

## Exam prep
### Likely 2-mark questions
1. **Define Façade.** A unified high-level interface that simplifies access to a complex subsystem.
2. **Define an immutable object.** An object whose state cannot change after construction.
3. **How is an immutable object updated?** It returns a new instance; it does not mutate the old one.
4. **Define a read-only interface.** An interface exposing observation operations to ordinary clients while a separate privileged capability permits mutation.
5. **Define a proxy.** An object that implements the subject interface and controls creation, access, location, caching, or lifecycle of a real subject.
6. **Name four proxy variants.** Virtual, remote, protection, cache/storage, firewall/smart—any four.
7. **Differentiate façade and proxy.** Façade simplifies a subsystem API; proxy controls a subject behind a compatible interface.

### Long-answer answer hints
- “Explain all four patterns”: intent, structure, participants, benefits, risks, and examples for each.
- “How do you enforce immutability?” constructor-only initialization, no mutators, defensive copies, immutable nested values, safe publication, and tests.
- “How does a read-only interface protect data?” narrow interface, controlled concrete type, authorization, no mutable leakage, and audit.
- “Compare façade, adapter, and proxy”: simplify, translate, and control respectively.
- “Design a virtual proxy for GPS routes”: interface, lightweight summary, lazy load, cache/invalidation, error behavior, and tests.

### Comparison table
| Pattern | Main job | Client sees | Typical concern |
|---|---|---|---|
| Façade | simplify subsystem | new simpler API | coupling/orchestration |
| Immutable | prevent change | stable values | state consistency |
| Read-only interface | selective capability | getters only | access separation |
| Proxy | control subject | compatible subject API | location/lifecycle/access/cache |
