---
subject: oose
unit: 3
topic: class-diagrams
syllabus_ref: CSM3102 Unit-III
status: draft
---
# Class Diagrams
## Overview
A class diagram is a UML structural diagram that shows classes or interfaces, their attributes and operations, and static relationships among them. It answers “what kinds of things exist, what do they know and do, and how are they related?” It is one of the most useful communication tools because it gives developers, analysts, and stakeholders a shared vocabulary.

A good class diagram is not a database schema and not a screen mock-up. It models meaningful types and responsibilities at a chosen level of abstraction. The notation must be precise: visibility, multiplicities, association direction, generalization, dependency, and realization all communicate different facts.

## Explanation
### 1. Class notation
A class box has compartments:
- name, usually in upper case;
- attributes/properties with type and optional visibility (`+` public, `-` private, `#` protected);
- operations with parameters and return type;
- optional constraints, notes, and tagged values.

Example:
```text
+------------------+
| Inspection       |
+------------------+
| - id: UUID       |
| - status: Status |
| + close(reason): Result |
+------------------+
```
A property may also be shown as an attribute; in UML, a derived value can be marked `{derived}` and a read-only property with a visibility/constraint. Choose notation consistent with the tool and audience.

### 2. Class responsibilities
A class should represent a coherent concept and own the state and operations for which it is responsible. Keep analysis domain classes separate from technical classes such as database repositories, controllers, or utility collections. Use interfaces where a capability is needed without shared implementation.

### 3. Associations
An association represents a meaningful relationship between classifiers. It can be named, have role names, and show navigability, multiplicity, aggregation/composition, or constraints. Association semantics are covered in the related association note, but a class diagram must show them consistently.

### 4. Generalization
Generalization is an “is-a” relationship: a child/specialization inherits features from a parent/generalization. Example:
```text
        PaymentMethod
          /       \
   CardPayment   WalletPayment
```
Generalization is not “has-a.” A `Report` does not inherit from `File` merely because a report may be stored in a file. Ensure the child is substitutable and the hierarchy expresses a stable domain relationship.

### 5. Realization and dependency
A class realizes an interface when it promises the interface’s operations. Dependency is a weaker “uses” relationship: one element changes or requires another at compile/design time. Use dependency for a temporary or supporting use, not for every association. A client that calls a service is usually associated with the service or holds a reference; the exact notation depends on the design.

### 6. Visibility and interfaces
Public operations form the stable client contract. Protected operations support subclasses; private operations are internal. A visible mutable collection may break encapsulation; use a read-only view or a method that returns a copy. Do not hide a required public service just because its implementation is a database query.

### 7. Static versus dynamic
A class diagram shows static structure, not message order, state, or algorithm. Add a sequence diagram for collaboration, a state-machine diagram for lifecycle, an activity diagram for workflow, and a component/deployment diagram for runtime structure. The class diagram should not be overloaded with temporal information.

### 8. Object diagrams
An object diagram shows a snapshot of instances, attributes, and links. It is useful for explaining multiplicities and a scenario:
```text
[S12: Site] 1 ──contains── 0..* [I17: Inspection]
[I17] assignedTo → [U04: Inspector]
```
The class diagram defines the general rules; the object diagram demonstrates one possible instance configuration.

### 9. Modeling domain versus implementation
Start with domain concepts: `User`, `Inspection`, `Site`, `Route`, `Waypoint`. Add design classes for services, repositories, interfaces, and UI controllers only when needed. Avoid generating a class for every database column or every screen control. Keep a mapping between analysis and design elements so the design does not lose stakeholder meaning.

### 10. Quality checks
Review a class diagram for:
- clear, singular names and consistent vocabulary;
- one meaningful responsibility per class;
- appropriate visibility and stable public operations;
- correct association direction and multiplicities;
- generalization that represents “is-a”;
- no circular dependencies that are not intentional;
- enough state and operations to satisfy scenarios;
- links to requirements and tests.

## Worked examples
### Example 1: Chat class diagram
```text
User 1 ── 0..* Message >── 0..* Conversation
Conversation 1 ── 0..* Participant
User 1 ── 0..* Notification
```
A user can send/receive messages and receive notifications; a conversation has participants. The diagram can be refined with role names and a message status enumeration. A sequence diagram then shows login and delivery order.

### Example 2: GPS domain
```text
Route * ── 2..* Waypoint
Route ──> MapProvider
Vehicle 1 ── 0..* Route
```
The route owns waypoints only if their lifetime is tied to the route; otherwise use an association. `MapProvider` is an interface, allowing alternate map sources. The multiplicity `2..*` is a requirement-derived rule, not a decorative number.

### Example 3: WMITS design
```text
InspectionService 0..1 ── Inspection * ── Evidence *
Site 1 ── 0..* Inspection
Inspector 1 ── 0..* Inspection
```
A diamond must be labeled and its semantics explained. A reviewer asks whether a site can be deleted while inspections exist; the model becomes more precise or the service adds a rule.

### Example 4: Generalization mistake
`EmailNotification` is a kind of `Notification`, so generalization is reasonable. `EmailNotification` is not a kind of `SMTPClient`; it uses or wraps it. Correcting this prevents a subclass from inheriting connection-management responsibilities that do not belong to notification behavior.

## Key terms & formulas
- **Class diagram:** UML diagram of classifiers, features, and static relationships.
- **Classifier:** a UML element that defines a type of thing, such as a class or interface.
- **Attribute/property:** state/property held by instances.
- **Operation:** behavior available on a classifier; may have parameters and return type.
- **Visibility:** public, private, protected, or package convention.
- **Association:** a meaningful relationship between classifiers.
- **Generalization/specialization:** is-a inheritance relationship.
- **Dependency:** a weaker relationship in which one element relies on another.
- **Realization:** implementation of an interface or abstract contract.
- **Multiplicity:** number of instances allowed at one association end.
- **Derived attribute:** value calculated from other state, not necessarily stored.
- **Class diagram quality:** correctness, clarity, cohesion, coupling, consistency, and traceability.

## Common mistakes
- Drawing a database schema with no behavior or domain meaning.
- Using a rectangle for every noun and no useful relationship direction.
- Misusing generalization for code reuse.
- Leaving multiplicities at the default `1` without checking the requirement.
- Making every operation public or every property mutable.
- Treating a class diagram as a complete functional specification.
- Adding implementation classes too early and losing the domain vocabulary.

## Exam prep
### Likely 2-mark questions
1. **What is a class diagram used for?** Showing classifiers, features, and static relationships in a system.
2. **List the three class compartments.** Name, attributes, and operations; add constraints/notes where relevant.
3. **Differentiate generalization and dependency.** Generalization is is-a inheritance; dependency is a weaker reliance.
4. **What does visibility mean?** Whether a feature is public, protected, private, or package-visible to clients.
5. **What is an object diagram?** A snapshot of particular instances and links.
6. **Why not use a class diagram as a database schema?** Classes express behavior and domain contracts; tables are a persistence representation that may differ.

### Long-answer answer hints
- “Explain class diagrams”: purpose, notation, associations, generalization, realization/dependency, interfaces, object diagrams, and modeling steps.
- “Draw a class diagram for a GPS system”: Vehicle, Route, Waypoint, MapProvider, and relationships; explain multiplicities and ownership.
- “How do you model a domain and implementation separately?” start with domain classes, refine responsibilities, add technical interfaces/services, and trace them.
- “Differentiate class and object diagrams”: general type-level model versus particular runtime snapshot.
- “Review a poor class diagram”: identify naming, responsibility, visibility, multiplicity, coupling, and requirement-traceability problems.

### Sketch
```text
+----------------+        1        *  +---------------+
|    Site        |-------------------->| Inspection    |
+----------------+                     +---------------+
                                        | -id           |
                                        | +submit()     |
                                        +---------------+
```
