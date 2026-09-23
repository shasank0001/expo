---
subject: oose
unit: 3
topic: objects-events-and-messages
syllabus_ref: CSM3102 Unit-III
status: draft
---
# Objects, Events, and Messages
## Overview
An object is a runtime entity with identity, state, and behavior. It responds to events and communicates with other objects through messages. A message says what a sender needs a receiver to do, while an event is a significant occurrence that can change state, trigger behavior, or be recorded. These ideas connect analysis language to interaction diagrams, state machines, and implementation.

The same real-world action can be described at different levels. A user “submits an inspection” in a use case, sends a `submit` message to an inspection object, and produces a `Submitted` event. UML notation helps keep those levels consistent.

## Explanation
### 1. Objects at analysis and design levels
An **analysis object** represents a problem-domain responsibility or participant and may deliberately avoid implementation details. A **design object** includes technical responsibility, interface, persistence, and collaboration needed to build the solution. The same conceptual object may be split into several design objects if that improves coupling or testing, but the model should preserve traceability.

An object has:
- identity and lifetime;
- state, expressed by properties;
- behavior, expressed by operations;
- an identity that survives state changes;
- interactions through messages.

### 2. Events
An **event** is a significant occurrence at a particular time and place. It may be internal or external. An event can be a point in time (“deadline reached”), a change in an external condition (“button clicked”), a signal, a message, or a completion of an operation. Events are named in past tense in state-machine notation, for example `PINEntered`, `RequestApproved`, or `ConnectionLost`.

An event does not necessarily change state, but it can trigger a transition, action, or asynchronous action. A signal is an event used for asynchronous communication; a message may carry data and have a sender, receiver, and operation.

### 3. Event classes
An **event class** groups events with common meaning, data, and handling. An event instance is one occurrence. For example:
```text
Event class: PaymentFailed
  instance: PaymentFailed(payment=P17, reason=insufficientFunds)
```
Separating event class from instance makes models reusable and helps distinguish the event's type from its particular data. Event classes may be represented in a class diagram or a domain model; the exact notation depends on the UML diagram and tool.

### 4. Messages
A **message** is a communication from one object to another that requests an operation or delivers information. In a sequence diagram, the arrow is a message; the named operation can include arguments and a return message. A synchronous message generally waits for a result in the calling execution, while an asynchronous message does not require immediate return. A reply is a message returning information.

Messages are useful in analysis because they state a needed collaboration without committing to a method, network call, or class structure. “A route planner requests a map from a provider” is a message; “the provider is a singleton with a static method” is a design decision.

### 5. State changes and events
When an object receives an event, it may inspect the event and its current state, run a guard, perform a transition, and invoke an operation. A state-machine diagram uses:
- **state:** condition during which the object waits;
- **event:** trigger;
- **guard:** Boolean condition;
- **transition:** movement;
- **effect/action:** work performed.

Example:
```text
ATM: Ready --[insertCard]--> CardPresent
CardPresent --[invalidPIN after 3 attempts]--> Locked
```

### 6. Asynchronous and concurrent interactions
Objects may operate at different times. An asynchrony marker in a sequence diagram shows a message that does not immediately return. Timelines, forks/joins, and state machines help model concurrency. The design must define ordering, timeouts, duplicate messages, and failure recovery when multiple objects can act at once.

### 7. Objects, events, and use cases
A use case names a user goal, not one message. A single use case may involve many object messages. Conversely, one message can be reused by several use cases. A use case should be decomposed into scenarios, and a sequence diagram can show the representative collaboration for one scenario without becoming the entire product specification.

### 8. Object identity and equality in events
An event can refer to an object by identity, not just by a displayed value. A message such as `cancel(P-104)` should not accidentally cancel another payment with the same label. Use stable IDs, equality rules, and validation at the receiving boundary. This is especially important for retries and duplicate asynchronous events.

## Worked examples
### Example 1: Login sequence
```text
User → LoginForm: submit(PIN)
LoginForm → AccountService: authenticate(PIN)
AccountService → UserStore: findUser(id)
UserStore → AccountService: user / notFound
AccountService → LoginForm: success / failure
```
The click is an initiating event; `authenticate` is a message; `success` or `failure` is a result that may change the form's state. The sequence diagram should not confuse these with use-case actors.

### Example 2: Inspection event class
```text
Event class: EvidenceAttached
  eventId, inspectionId, fileName, capturedAt
```
An occurrence `EvidenceAttached(E-88, I-17, photo.jpg, 10:30)` is one event instance. The event handler can update an aggregate and write an audit record.

### Example 3: Asynchronous delivery
`publish(MessageReady)` is sent to a notification queue. The sender does not wait for delivery; the queue may retry. The receiver must be idempotent or detect duplicates, otherwise reconnecting can create two notifications. The test covers duplicate and timeout events.

### Example 4: Guarded transition
A `Loan` in `Requested` state changes to `Approved` only when `requesterIsEligible` is true. Otherwise it changes to `Rejected` or remains pending according to the business rule. The message is `evaluate()`, the event may be `ReviewCompleted`, and the guard is part of the contract.

## Key terms & formulas
- **Object:** runtime entity with identity, state, behavior, and lifecycle.
- **Event:** significant occurrence that may trigger behavior or state change.
- **Event class:** type/group of events; **event instance:** one occurrence.
- **Signal:** event used for asynchronous communication.
- **Message:** request from a sender object to a receiver object.
- **Synchronous message:** sender waits for the requested operation/result.
- **Asynchronous message:** sender continues without waiting for a reply.
- **Reply/return message:** response to a request.
- **Guard:** condition that determines whether a transition or operation is allowed.
- **State transition:** movement from one state to another due to event and optional guard/effect.
- **Object-message count (test estimate):** a representative scenario can be summarized as actors × objects × meaningful interactions, but not every interaction is independent.

## Common mistakes
- Calling a normal method call an event without distinguishing the occurrence from the operation.
- Using an event name for a state or an action.
- Confusing a use-case goal with a message sequence.
- Omitting sender, receiver, direction, or return value from an interaction.
- Assuming asynchronous delivery happens exactly once or in order.
- Using a mutable label instead of identity in a message.
- Adding a message to a diagram without showing what state and data it changes.

## Exam prep
### Likely 2-mark questions
1. **Define an event.** A significant occurrence in time that may trigger an action or state change.
2. **Differentiate an event and a message.** An event is an occurrence; a message is communication from one object to another that may carry or request behavior.
3. **Define an event class and event instance.** The class groups common event properties; the instance is one occurrence with specific data.
4. **What is a synchronous message?** A request whose sender waits for the receiver's operation result.
5. **Why use identity in messages?** It identifies the exact object even if displayed attributes are equal or change.
6. **What are the parts of a state transition?** Source state, event, guard, target state, and effect/action.

### Long-answer answer hints
- “Explain objects, events, and messages”: definitions, properties, event classes, synchronous/asynchronous messages, state change, and analysis/design use.
- “Draw a sequence diagram for login”: objects, lifelines, message order, return, conditions, and a note about the initiating user event.
- “Differentiate use case, activity, state machine, and sequence”: goal, workflow, states/transitions, and message order.
- “How are asynchronous messages tested?” duplicate, out-of-order, timeout, retry, and recovery scenarios.
- “Explain a guarded event transition”: event, condition, action, target state, and an invalid-event case.

### Text sketch
```text
User --submit--> Controller --authenticate--> Service --lookup--> Store
          (message)          (message)          (message)    (result)
```
