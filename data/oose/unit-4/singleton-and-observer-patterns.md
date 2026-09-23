---
subject: oose
unit: 4
topic: singleton-and-observer-patterns
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# Singleton and Observer Patterns
## Overview
The **Singleton** pattern controls creation of a class so that only one instance exists and provides a common access point. The **Observer** pattern defines a one-to-many dependency: when a subject changes, its registered observers are notified. The patterns solve different problems—controlled unique state and event-based decoupling—but both are useful when global or changing relationships must be handled carefully.

## Explanation
### 1. Singleton pattern
#### Context and problem
Some resources are intentionally unique for an application or runtime: a configuration service, a central cache, a license manager, a connection pool, or a system-wide event coordinator. A public constructor alone cannot prevent multiple instances. Singleton makes the restriction explicit and gives all clients a controlled way to obtain the instance.

#### Structure
```text
<<Singleton>>
  - instance: Singleton
  - Singleton()   // private
  + getInstance(): Singleton
  + domain operations
```

The class stores the one instance, hides construction, and exposes `getInstance()` (or an equivalent factory). Initialization may be eager when the application starts or lazy on first access. The implementation must be thread-safe in a concurrent system; a simple unsynchronized check can create two instances.

#### Responsibilities
- prevent construction through a public constructor or other bypass;
- create/return the one permitted instance;
- define initialization and failure behavior;
- expose only the operations that all clients may use;
- manage lifetime, shutdown, and test reset if needed;
- avoid hidden configuration changes that make behavior unpredictable.

#### Benefits
- guarantees a single instance within the defined scope;
- centralizes access to shared state;
- can be lazy and save resources;
- gives a controlled global service point.

#### Risks
- hidden global state makes tests interfere;
- initialization order and dependencies become difficult;
- the class may grow into a “god object” with unrelated responsibilities;
- replacing the singleton is harder if code depends on the concrete class;
- multi-process or distributed systems may have one instance per process, not one globally.

Use an interface or dependency injection when the client needs replaceability. Singleton is appropriate only for a truly process-wide unique responsibility, not for every service.

### 2. Observer pattern
#### Context and problem
A subject often needs to inform several interested objects when its state changes. If the subject holds direct references to every display, printer, logger, and auditor, the classes become tightly coupled. A new observer requires changing the subject, and a subject reused elsewhere carries unwanted collaborators.

#### Structure
```text
<<Observable>>                 <<Observer>>
  + addObserver(o)             + update(change)
  + removeObserver(o)          + ...
  + notifyObservers()

<<ConcreteObservable>>          <<ConcreteObserver>>
```

The observable maintains a collection of observers implementing a common `Observer` interface. `addObserver` registers, `removeObserver` unregisters, and `notifyObservers` sends a change notification. The concrete observable changes its own state and then notifies. Each observer decides what to do.

#### Push versus pull notification
- **Push:** the subject includes changed data in the notification, convenient but may expose too much or make many notification types.
- **Pull:** the observer receives a subject reference and queries the state after notification, simpler notification but more queries.
Choose based on information exposure, performance, and consistency.

#### Notification timing
Notify after the state change is complete, or specify a consistent snapshot. Avoid notifying while the subject is partially initialized. Define whether observers can add/remove observers during notification, whether exceptions are isolated, and whether notification is synchronous or asynchronous.

#### Benefits
- reduces direct coupling between subject and observers;
- supports many independent reactions;
- observers can be added or removed at runtime;
- supports multiple views of one model, as in MVC.

#### Risks
- notification storms or slow observers;
- memory leaks from strong references;
- unexpected update order;
- cascading updates and cycles (A observes B and B observes A);
- testing and debugging are harder when behavior is event-driven;
- an observer may act on stale state if notification is asynchronous.

Use weak references, unregister lifecycle, bounded queues, and idempotent observers where appropriate. Do not use Observer to hide a required direct relationship; if the client must always make a request, a service call may be clearer.

### 3. Relationship between Singleton and Observer
A singleton configuration manager can be an observable subject, and screens or services can register as observers. The two patterns solve separate forces; combining them is valid but increases hidden coupling. Avoid making every service a singleton merely because it publishes events.

## Worked examples
### Example 1: Configuration singleton
`AppConfiguration.getInstance()` returns the one active configuration for the process. Clients request it through an interface. Tests inject a test configuration or reset the runtime scope. The application does not create a second configuration when a plugin calls the factory.

### Example 2: Price-list observer
`PriceList` is a concrete observable. `DisplayBoard`, `InvoicePrinter`, and `SearchIndex` implement `Observer`. When a price changes, `setPrice` updates the value and notifies. The printer can query the new price; the display can refresh. Removing a display before shutdown prevents stale callbacks.

### Example 3: MVC
The model is the observable subject. Views subscribe to the model and update when model state changes. A controller changes the model in response to user events. The model does not import a particular screen, so the UI can change without rewriting domain logic. A notification test checks that two views update and a removed view does not.

### Example 4: Cascading failure
A model change triggers three observers; one throws an exception. A robust implementation records the failure, continues or stops according to policy, and exposes a diagnostic. The policy is tested. Simply letting an arbitrary observer exception corrupt the subject is poor defensive design.

### Example 5: Scope warning
In a two-server system, a Singleton configuration instance exists independently in each server process. It is not a globally synchronized singleton. Use a configuration service or replicated store for cross-process consistency.

## Key terms & formulas
- **Singleton:** a class/pattern with one permitted instance in a defined scope.
- **Instance scope:** process, application, class loader, thread, or distributed system boundary; state the scope.
- **Lazy initialization:** create the instance on first request.
- **Eager initialization:** create it at application startup.
- **Observable/subject:** object maintaining state and notifying registered observers.
- **Observer/listener:** object implementing an update/notification contract.
- **Push notification:** subject sends changed data.
- **Pull notification:** observer obtains state after notification.
- **Notification fan-out:** number of observers notified by one change.
- **Observer coupling reduction:** direct collaborators replaced by one common interface; measure conceptually, not as a universal number.
- **Thread-safe singleton initialization:** use language/runtime guarantees such as static synchronization, an initialization-on-demand holder, or an equivalent mechanism.

## Common mistakes
- Making every service a Singleton and creating hidden global state.
- Publishing a public constructor that bypasses the singleton rule.
- Claiming a distributed system has exactly one in-memory instance.
- Forgetting to unregister observers and causing memory leaks.
- Making observers depend on concrete subject internals instead of the interface.
- Notifying before the state is valid or allowing cascading updates without a policy.
- Treating Observer as a guarantee of immediate, ordered, or exactly-once delivery.

## Exam prep
### Likely 2-mark questions
1. **Define Singleton.** A pattern ensuring a class has one instance within a defined scope and providing controlled access.
2. **Name two Singleton implementation concerns.** Private constructor, thread-safe initialization, lifecycle, testability, and scope—any two.
3. **Define Observer.** A one-to-many dependency in which a subject notifies registered observers of a change.
4. **What are the main Observer participants?** Observable/subject, Observer interface, and concrete observers; plus concrete subject.
5. **Differentiate push and pull notification.** Subject sends changed data versus observer queries the subject after notification.
6. **State two risks of Observer.** Memory leaks, update storms, ordering/cascades, stale/asynchronous state, or exceptions.

### Long-answer answer hints
- “Explain Singleton and Observer”: context, structure, participants, benefits, risks, and a shared example.
- “Draw a Singleton class diagram”: private constructor, static instance, `getInstance`, and domain operations; discuss thread safety.
- “Draw an Observer sequence”: subject registers observers, state changes, subject notifies, observers update/remove.
- “Apply Observer to MVC”: model subject, views observers, controller modifies model; explain reduced coupling.
- “Compare the patterns”: unique access versus change notification; they solve different forces and can be combined cautiously.

### Sketch
```text
Singleton:  Client → getInstance() → the one instance
Observer:   Subject ──registers──> Observer
                 └──notify──change──> each Observer
```
