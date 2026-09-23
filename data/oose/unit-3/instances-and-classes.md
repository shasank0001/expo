---
subject: oose
unit: 3
topic: instances-and-classes
syllabus_ref: CSM3102 Unit-III
status: draft
---
# Instances and Classes
## Overview
A class describes a family of objects with common structure, behavior, and constraints. An instance is one particular object created from that class, with its own identity, state, and lifecycle. The distinction lets a model represent “all inspections” as a class while still distinguishing the inspection with ID 104 from the inspection with ID 205.

In UML, a class is a classifier; an object is an instance of a classifier. This note explains the class/instance distinction, object identity, state and behavior, lifecycle, object identity versus equality, and how to model classes without prematurely choosing implementation details.

## Explanation
### 1. Class
A UML class commonly shows:
- name;
- attributes/properties with types and visibility;
- operations/methods with parameters and return type;
- constraints, notes, and tagged values;
- associations, generalization, or interface realization.

A class should capture a meaningful responsibility and the rules it owns. `Book` may own loan-status transitions, but `LoanPolicy` may own the rules for how long a book may be borrowed. A class with unrelated attributes and operations has low cohesion.

### 2. Instance
An instance is a concrete occurrence of a class. It has:
- **identity:** a distinction from all other objects, even if all attribute values match;
- **state:** a value for each applicable property at a moment;
- **behavior:** the operations defined by its class and interfaces;
- **lifecycle:** creation, initialization, use, state changes, and destruction.

The notation `objectName : Class` is common in UML object snapshots. A snapshot shows a particular state at a point in time, not the class definition.

### 3. Identity and equality
An object may change its name, location, or status while remaining the same entity. A student who changes their name is still the same student; two students with identical displayed values may still be different people. This is **object identity**. **Equality** asks whether values are equivalent according to a business rule. The model should state which identifiers are stable and which attributes are mutable.

For persistent data, a database key is often used to recover identity, but a key is an implementation aid, not the whole definition of domain identity. A change in a student's phone number must not make the system create a new student.

### 4. State and behavior
State is the condition of an object at a time, represented by property values and sometimes a lifecycle state. Behavior is the computation and collaboration that changes or observes state. A `Route` may have states `unplanned`, `calculating`, and `ready`; a `Message` may change from `queued` to `delivered` after an operation. A state is not the same as a class: classes describe the type, while states describe phases of an instance.

### 5. Construction and destruction
A class may specify creation semantics, initial state, and destruction constraints. Some objects are created only by a factory, while others have a public constructor. A route may require waypoints before it can be calculated; a temporary connection may be destroyed when the user logs out. Modeling lifecycle prevents invalid partially initialized objects.

### 6. Class responsibilities
A good class has a coherent reason to change. A class should usually own:
- the state it can directly maintain;
- invariants over that state;
- operations that use the state;
- messages it receives or sends to collaborators.

Do not make a class responsible for unrelated UI, database, business, and network details. Split responsibilities when change pressure or failure isolation demands it. The design process may use a class's public interface to define a role or an abstract type.

### 7. Class and object modeling
A class diagram describes the type-level model. An object diagram shows representative instances and their links, which is useful for explaining a scenario. For example:
```text
Inspection I17: status=Returned, site=S12
Inspector U04: role=Inspector
I17 →assignedTo→ U04
```
The object snapshot helps stakeholders see whether multiplicities and labels make sense. It is not a substitute for the class definition.

### 8. Common relationships of instances
Instances can be associated with other instances through a link. A class-level association may say `Inspection` is assigned to `Inspector`; an object diagram may show the particular link between I17 and U04. Composition or aggregation constrains lifecycle; aggregation alone should not be used for every “has-a” phrase.

## Worked examples
### Example 1: Student class and instances
```text
class Student
  id: StudentId
  name: String
  status: StudentStatus
  register(): void
```
`S01: Student(id=S01, name=Asha, status=Active)` and `S02: Student(id=S02, name=Asha, status=Active)` can have equal names but different identity. A name update does not change S01's ID.

### Example 2: Route lifecycle
```text
Route R7: status=Unplanned
→ setWaypoints([A, B]) → status=Planned
→ calculate() → status=Ready
```
If an event arrives in `Ready` that tries to change waypoints without reset, the operation rejects it or resets according to a stated invariant. The state is not encoded by creating a new class for every phase.

### Example 3: Factory and invariant
A `Route` constructor accepts a list of waypoints and validates non-empty, valid coordinates. Without this control, a route can exist in a state no map service can handle. The class owns its construction invariant.

### Example 4: Object diagram
```text
[U04: Inspector] 1 ─── assignedTo ─── 1 [I17: Inspection]
[S12: Site]       1 ─── contains ───── 0..* [I17]
```
The object diagram shows a particular assignment. It makes it clear that a site may have zero inspections in a new system, while a class diagram states the general multiplicity.

## Key terms & formulas
- **Class:** type-level description of attributes, operations, and constraints.
- **Instance/object:** concrete occurrence with state and identity.
- **Classifier:** UML element that classifies features; a class is a classifier.
- **Identity:** the property that distinguishes one occurrence from another over time.
- **Equality:** whether two values are equivalent under a specified rule.
- **State:** condition represented by an instance's current property/lifecycle values.
- **Behavior:** operations and collaborations through which an instance responds.
- **Lifecycle:** creation through destruction, including state transitions.
- **Attribute:** property whose value is held by an instance.
- **Operation:** behavior available to a client; it is not necessarily a programming-language method.
- **Class responsibility:** reason for the class to exist and change.

## Common mistakes
- Confusing a class with one object or drawing only examples.
- Treating a class as a database table with no behavior or invariant.
- Using a mutable name as object identity.
- Representing every lifecycle phase as a separate class.
- Giving a class unrelated responsibilities and calling it “reusable.”
- Showing attributes without types, visibility, or meaningful constraints.
- Assuming a class diagram describes runtime instances without an object diagram.

## Exam prep
### Likely 2-mark questions
1. **Differentiate a class and an instance.** A class specifies a family; an instance is one concrete object with its own state and identity.
2. **What is object identity?** The property that distinguishes an object from others even when attribute values change.
3. **Differentiate state and behavior.** State is the current condition/data; behavior is what the object does or responds to.
4. **Why use a factory or controlled construction?** To establish required initial state and prevent invalid objects.
5. **What is a UML object diagram?** A snapshot of particular instances and their links at a time.
6. **What is a cohesive class responsibility?** A coherent reason for change and related state/behavior owned together.

### Long-answer answer hints
- “Explain classes and instances”: definitions, notation, identity, state, behavior, lifecycle, and a class/object diagram.
- “Why is identity different from equality?” two objects can have equal attributes yet represent different entities; identity persists through state changes.
- “Model a Route class”: attributes, operations, invariants, lifecycle, and an object snapshot.
- “How do you improve class design?” single responsibility, encapsulation, low coupling, high cohesion, stable public operations, and meaningful domain types.
- “Differentiate a class diagram and object diagram”: type-level structure versus a particular runtime example.

### Notation reminder
```text
ClassName       InstanceName : ClassName
---------------------------------------------  object snapshot
[attributes]   [attribute = current value]
[operations]   [links to other instances]
```
