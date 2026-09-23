---
subject: oose
unit: 1
topic: introduction-to-object-orientation
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Introduction to Object Orientation
## Overview
Object orientation is a way to model a system as interacting objects. Each object combines data (state) with the operations allowed on that data (behavior). Objects of the same kind share a class definition, but each object can have its own state and identity. This approach supports encapsulation, abstraction, inheritance, and polymorphism, which make large systems easier to understand and change.

Object-oriented software engineering applies these ideas through the whole process: requirements are represented with domain objects and user goals, design uses classes and interactions, implementation maps them to code, and tests exercise their collaborations. The goal is not to add “objects” everywhere; it is to keep responsibility, behavior, and change localized.

## Explanation
### 1. Objects
An **object** is a runtime entity with:
- **identity:** it remains the same entity even when its values change;
- **state:** data describing its condition;
- **behavior:** operations it can perform;
- **invariants/constraints:** conditions that should remain true;
- **lifecycle:** creation, use, change, and destruction.

For example, a `LibraryBook` object may have identity `B-104`, state `available`, and behavior `issueTo(member)`. The title may be “Software Engineering,” but changing the title does not change the book's identity.

### 2. Classes and instances
A **class** is a description of a family of objects: its attributes, operations, relationships, constraints, and applicable behavior. An **instance/class object** is one particular object created from that class. If `Student` has attributes `id` and `name`, `Student("S01", "Asha")` and `Student("S02", "Ravi")` are separate instances with independent state.

The class is not the same as a type in every implementation detail, but conceptually it specifies a family of objects. A well-designed class has a clear responsibility and a stable public interface.

### 3. Abstraction
Abstraction presents the essential behavior while hiding implementation details. A user of `PaymentService` needs to call `charge(amount)`, not know whether the service uses a card gateway, bank transfer, or stored token. Good abstraction reduces coupling, but hiding essential behavior or exposing unrelated internals makes abstraction ineffective.

### 4. Encapsulation
Encapsulation combines state and behavior in an object and controls access to the state. Public operations enforce invariants; private data cannot be changed accidentally. A `BankAccount` should reject an overdraw rather than allowing a client to set its balance directly. Encapsulation makes maintenance safer because changes stay inside the class and callers use the interface.

### 5. Inheritance and specialization
**Inheritance** creates an “is-a” relationship in which a specialized class reuses and extends a generalization class. `SavingsAccount` may inherit common account behavior from `Account` and add interest rules. Inheritance should represent genuine substitutability, not merely shared code. The specialization must obey the base class contract.

### 6. Polymorphism
**Polymorphism** allows one interface to be used with different implementations. A `Notification` variable may refer to `EmailNotification` or `SmsNotification`; the program sends the message without knowing the concrete class. Polymorphism reduces conditional branches and lets a new channel be added without rewriting every caller.

### 7. Messages and collaboration
Objects collaborate by sending messages: one object requests an operation on another. A message has a receiver, operation, arguments, and often a return value. In analysis, messages express what one object needs from another without exposing how it is implemented. In design, the message becomes a method call, message event, or service interface.

### 8. Object-oriented modeling
An object-oriented model identifies domain concepts, responsibilities, and interactions while keeping analysis separate from implementation. A `Place`, `User`, `Route`, and `Inspection` should represent the problem, not just database tables or screen controls. Design later adds technical classes and interfaces.

### 9. Benefits and challenges
Benefits include modularity, reuse, maintainability, clearer communication with domain experts, and the ability to vary behavior through polymorphism. Challenges include excessive coupling, deep inheritance, large “god” classes, premature persistence details, and confusing object identity. Good object-oriented design uses small responsibilities, interfaces, composition where appropriate, and tests of collaboration.

## Worked examples
### Example 1: Library
Classes include `Member`, `Book`, and `Loan`. `Member` does not edit a book's availability directly; it sends an `issue` message to `Book` or `LoanService`. `Book` changes state only through an operation that checks whether it is available. The model can represent several books while keeping the rule in one place.

### Example 2: GPS
`Vehicle`, `Route`, `Map`, and `Waypoint` objects collaborate. A `RoutePlanner` asks a `MapProvider` for data and returns a `Route`. Replacing one map provider with another does not change the caller if both implement the same interface. Identity and encapsulation remain intact.

### Example 3: Inheritance mistake
A `ReportWriter` inherits from `File` only to reuse code. It is not a kind of file, and a change to file deletion could corrupt report behavior. Composition or a separate formatting service is safer. Inheritance should express a stable “is-a” relationship.

### Example 4: Polymorphism
```text
Notification
 ├── EmailNotification
 └── SmsNotification

client → notify(notification)
```
The client sends the same message to either object. A future `PushNotification` can be added if it satisfies the `Notification` interface.

## Key terms & formulas
- **Object = identity + state + behavior + constraints.**
- **Class:** a specification of objects with common structure and behavior.
- **Instance:** one object created from a class.
- **Abstraction:** essential behavior exposed, details hidden.
- **Encapsulation:** state and behavior bundled with controlled access.
- **Inheritance:** an is-a relationship from a specialization to a generalization.
- **Polymorphism:** one interface, multiple possible implementations.
- **Message:** a request from one object to another.
- **Invariant:** a condition that must remain true.
- **Coupling:** the amount of knowledge one element depends on another; favor low coupling.
- **Cohesion:** how closely the responsibilities inside one element belong together; favor high cohesion.

## Common mistakes
- Calling a record or JSON object a full object-oriented model without behavior and interaction.
- Confusing an object with its class or confusing a class with one instance.
- Making every attribute public and thereby breaking encapsulation.
- Using inheritance only to copy code; this creates a fragile “is-a” claim.
- Describing polymorphism as “many objects” only; its important feature is substitutable behavior through one interface.
- Mixing analysis classes with database tables and UI controls before the domain is understood.

## Exam prep
### Likely 2-mark questions
1. **Define an object and list its four common parts.** An identifiable runtime entity with state, behavior, identity, and constraints; list any four with a short explanation.
2. **Differentiate a class and an instance.** A class describes a family; an instance is one particular object with its own state and identity.
3. **Define encapsulation.** Bundling state and behavior and controlling access through a public interface.
4. **Define polymorphism.** The ability to use one interface for different implementations.
5. **What is a message?** A request from a sender object to a receiver object requesting behavior.
6. **What makes inheritance appropriate?** A genuine is-a relationship in which the subtype can replace the base type without violating its contract.

### Long-answer answer hints
- “Explain object orientation”: define objects/classes, then abstraction, encapsulation, inheritance, polymorphism, messages, and an example.
- “Benefits of object-oriented modeling for requirements and design”: domain vocabulary, responsibility, low coupling, reuse, testability, and easier change.
- “Compare composition and inheritance”: inheritance is is-a and couples types to their base; composition uses collaborators and is often more flexible.
- “Why is identity important?” an object may change state while remaining the same entity; ID keys distinguish it from a merely equal value.
- “Design a small class diagram”: classes, attributes, operations, multiplicities, and a message sequence; do not jump straight to database tables.

### Design check
For every class ask: what is its single main responsibility, what state does it own, which messages can it receive, and which invariants must it protect?
