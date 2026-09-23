---
subject: oose
unit: 4
topic: delegation-and-adaptor-patterns
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# Delegation and Adaptor Patterns
## Overview
**Delegation** lets one object forward a request to another object that already provides the needed service. **Adaptation** lets a client use an existing or incompatible class by translating its interface to the one the client expects. Both reuse existing behavior, but delegation is primarily a relationship between collaborating objects, while an adaptor is primarily an interface-conversion wrapper.

## Explanation
### 1. Delegation pattern
#### Context and problem
A class is being designed and another class already has an operation that provides the required behavior. Inheritance may be inappropriate because the “is-a” rule is false, multiple inheritance is unavailable, or the team wants to change the delegate at runtime. Copying the code creates maintenance problems.

#### Structure
```text
<<Delegator>> 1 ───── 1 <<Delegate>>
   + service()             + reusedOperation()
```

The delegator holds a reference to a delegate and implements its public operation by forwarding the request:

```text
service(args) {
    return delegate.reusedOperation(args);
}
```

The delegate may be supplied through a constructor, setter, factory, or dependency-injection mechanism. A stable interface to the delegate is preferable to a concrete dependency when the implementation may vary.

#### Uses
- reuse a collection's `addFirst` to implement a stack's `push`;
- forward a booking's flight number to a specific or regular flight object;
- use a logging, caching, or transaction service behind a domain facade;
- implement a role-specific service without inheritance;
- select a delegate based on configuration or platform.

#### Benefits
- avoids inappropriate inheritance and duplicated logic;
- keeps the delegator focused on its own contract;
- allows the delegate to be replaced or tested independently;
- supports composition and late binding;
- can narrow or adapt the reused operation.

#### Risks and controls
- A forwarding method that does nothing except call one delegate adds noise; use it when it provides a real abstraction, translation, lifecycle, or error policy.
- Avoid chains of forwarding through non-neighboring objects; they hide coupling and make failures hard to trace.
- Define delegate lifetime and whether the delegate may be null.
- Do not expose delegate internals unless that is intentional.
- If the delegator passes through every method, the abstraction may be unnecessary; consider directly using the interface.

#### Delegation versus inheritance
Inheritance gives a subtype implementation and an “is-a” promise. Delegation gives a collaborator and a “uses/has” relationship. Delegation preserves substitutability only at the delegator's public contract; it does not make the delegator a subtype of the delegate.

### 2. Adaptor pattern
#### Context and problem
An existing class (the **adaptee**) has useful behavior, but its operation names, parameters, return types, or semantics do not match the interface expected by a client hierarchy. The client may also be unable to use multiple inheritance. A direct call would force every client to know the legacy detail.

#### Structure
```text
<<Superclass/Target>>       <<Adapter>>       <<Adaptee>>
  + polymorphicMethod()  →  + polymorphicMethod() → + adaptedMethod()
```

The adapter implements the target interface and translates the target request into an adaptee request. It may convert:
- argument types and order;
- return values;
- units and formats;
- exceptions;
- names and default behavior;
- multiple adaptee calls into one target operation.

The client sees the target contract. The adaptee can remain unchanged. This is often called an object adaptor; a class adaptor may use inheritance when the language and design permit it.

#### Example mapping
Suppose `ThreeDShape` defines `volume()`. A `Sphere` already has `calcVolume()` but its signature or class hierarchy does not match. `SphereAdapter` implements `volume()` and calls `sphere.calcVolume()`. `Torus` can have a corresponding adapter. Clients can use `ThreeDShape` polymorphically without knowing the legacy method.

#### Benefits
- reuses existing code without changing it;
- isolates clients from incompatible interfaces;
- provides a migration path for legacy systems;
- supports object composition and runtime selection;
- localizes conversion and error policy.

#### Risks
- An adapter can become a “translation dumping ground” if it contains unrelated logic.
- Semantic mismatches may be hidden: same name does not guarantee same meaning.
- Too many layers can make debugging and performance surprising.
- Error and retry behavior must be defined across the boundary.
- Do not adapt an interface when a direct stable contract is simpler.

#### Adaptor versus delegation
An adaptor is a specialized delegator whose public contract is the target interface and whose job is translation. Ordinary delegation may forward an already compatible request and preserve the delegate as a collaborator. A proxy also delegates, but usually controls access, location, lifetime, or lazy loading rather than converting a signature.

## Worked examples
### Example 1: Stack delegation
A `Stack` needs `push` and `pop`, but a `LinkedList` provides `addFirst` and `removeFirst`. `Stack` delegates those calls instead of inheriting from `LinkedList`. The stack maintains its own invariant and error behavior. A unit test verifies push/pop/empty behavior independently of the list implementation.

### Example 2: Booking and flight
`Booking.flightNumber()` delegates to a `Flight` object. A `SpecificFlight` and `RegularFlight` can each provide the same flight-number service. The booking is not a kind of flight; it uses one. If a booking supports several flights, the cardinality and aggregation rule are explicit.

### Example 3: Legacy sensor
A new application expects `TemperatureSensor.readCelsius(): double`, but the legacy device exposes `getValue(): int` in tenths of a degree. `TemperatureSensorAdapter` converts the value and maps device errors to the new contract. Boundary tests cover overflow, unavailable device, and unit conversion.

### Example 4: Adaptor policy
A payment library returns a status code while the application expects a result object. The adapter maps `DECLINED`, `TIMEOUT`, and `UNKNOWN` to explicit outcomes. It does not hide a timeout as success. The design records which library statuses are unsupported and how they are surfaced.

## Key terms & formulas
- **Delegation:** forwarding a request from a delegator to a delegate.
- **Delegator:** object exposing the desired service and forwarding it.
- **Delegate:** object that supplies the reused implementation.
- **Forwarding method:** method whose body primarily calls the delegate.
- **Late binding:** selecting the delegate at construction/configuration/runtime.
- **Adaptor:** wrapper implementing a target interface using an adaptee.
- **Adaptee:** existing/incompatible class whose behavior is reused.
- **Target interface:** contract expected by the client.
- **Interface translation:** mapping names, types, units, errors, and semantics.
- **Delegation depth:** number of forwarding hops; keep it low to make failures and latency understandable.
- **Conversion identity (for lossless units):** `output = input × factor + offset`, with rounding and range rules.

## Common mistakes
- Using inheritance when the relationship is not “is-a.”
- Creating a forwarding method for every possible operation with no abstraction benefit.
- Calling a delegate through a long chain of unrelated objects.
- Confusing a target interface with the adaptee's method name.
- Forgetting type, unit, error, or semantic conversion in an adaptor.
- Hiding a failed operation by returning a misleading default.
- Assuming an adaptor changes the adaptee's internals or fixes its behavior.

## Exam prep
### Likely 2-mark questions
1. **Define delegation.** A delegator forwards a request to a delegate that supplies the behavior.
2. **When is delegation preferred to inheritance?** When reuse is needed but the is-a relationship is false, or when the collaborator may vary.
3. **Define the Adaptor pattern.** A wrapper that converts an adaptee's interface to a target interface expected by a client.
4. **Name the Adaptor participants.** Target/client, adapter, and adaptee.
5. **List two conversions an adapter may perform.** Argument, return, unit, name, exception, or semantic conversion—any two.
6. **Differentiate delegation and adaptation.** Delegation forwards a compatible service; adaptation translates an incompatible one to a target contract.

### Long-answer answer hints
- “Explain delegation”: context, forces, structure, pseudocode, benefits, risks, and an example.
- “Explain adaptor”: target/adapter/adaptee, object/class variants, conversion table, example, and error handling.
- “Compare adaptor, facade, and proxy”: adaptation changes interface; facade simplifies a subsystem; proxy controls location/access/lifetime while preserving a similar interface.
- “Why not inherit from a legacy class?” false is-a, multiple inheritance limits, coupling, and change isolation.
- “Write an adaptor mapping”: show input type, conversion, output, unsupported case, and tests.

### Pseudocode
```text
// Delegation
service(x) { return delegate.reuse(x); }

// Adaptation
targetOperation(x) { return adaptee.legacyOperation(convert(x)); }
```
