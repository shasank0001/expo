---
subject: oose
unit: 4
topic: transaction-processing-pipe-filter-and-mvc-architectural-patterns
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# Transaction Processing, Pipe-and-Filter, and MVC Architectural Patterns
## Overview
These architectural patterns suit different system shapes. **Transaction Processing** handles a stream of commands that change stored state. **Pipe-and-Filter** passes a stream of data through independent transformations. **Model–View–Controller (MVC)** separates domain data, presentation, and user-interaction control. The patterns may be combined, but their data flow and responsibilities differ.

A good design chooses a pattern by matching the problem: transactions need consistency and dispatch, pipelines need composable transformations, and MVC needs changing interfaces over shared model state.

## Explanation
### 1. Transaction-Processing pattern
#### Structure
A process reads a sequence of inputs one at a time. Each input describes a **transaction**, usually a command that changes stored data. A transaction dispatcher examines the transaction type and dispatches it to a specialized handler. Handlers execute the operation and produce a result or exception.

```text
Input stream → Transaction dispatcher
                  ├→ Reservation handler
                  ├→ Cancellation handler
                  ├→ Payment handler
                  └→ Audit handler
                         ↓
                   data/state + result
```

A transaction is more than a function call. It may need atomicity, validation, authorization, logging, idempotence, and a response. A dispatcher can route by type/code, while handlers own the transaction-specific rules.

#### Benefits
- clear division between dispatching and transaction logic;
- new transaction types can be added as handlers;
- handlers are cohesive and independently testable;
- a stream can be processed consistently and sequentially;
- central dispatcher can provide logging, validation, and monitoring;
- good fit for orders, payments, reservations, commands, and event feeds.

#### Challenges
- a central dispatcher can become a bottleneck or a switchboard with tangled conditions;
- transaction ordering and concurrency must be defined;
- retries can repeat a side effect unless operations are idempotent;
- partial failure requires rollback, compensation, or a recovery log;
- response correlation and back-pressure matter in a stream;
- adding a handler changes protocol and deployment assumptions.

Use a clear transaction type contract, atomic boundaries, idempotency keys where appropriate, audit records, and dead-letter/error handling. Test duplicate, out-of-order, invalid, and retry cases.

### 2. Pipe-and-Filter pattern
#### Structure
A relatively simple data stream passes through a series of processes. Each **filter** transforms data and writes to one or more outputs. A **pipe** connects an output to an input. Filters know the format and content of their input, but normally do not need to know which filter produced it.

```text
input → [validate] → [normalize] → [enrich] → [store/output]
          pipe         pipe          pipe
```

Filters may run sequentially or concurrently; streams can be split, merged, and routed. The arrangement is flexible: a filter can be removed, replaced, inserted, or reordered if the data contract permits it.

#### Benefits
- strong divide-and-conquer and functional cohesion;
- filters can be independently developed and tested;
- low coupling through a simple data contract;
- reuse in different pipelines;
- easy to add, replace, or reorder transformations;
- suitable for compilers, media processing, data cleaning, ETL, and log processing.

#### Challenges
- a complex interactive workflow does not fit a simple stream;
- data format and schema evolution affect every connected filter;
- buffering, back-pressure, ordering, and throughput must be designed;
- a bad or failing filter can block or corrupt the stream;
- debugging requires tracing data and pipeline state;
- parallel filters need safe partitioning and synchronization.

Define the data contract, validation at each boundary, error side channels, buffering limits, ordering guarantees, and a dead-letter path. A filter should transform data, not hide unrelated business orchestration.

### 3. Model–View–Controller pattern
#### Structure and responsibilities
MVC separates the user-interface concerns from the domain model:
- **Model:** underlying domain classes/state and business behavior; it is independent of a particular view/controller.
- **View:** renders model data for a user; it displays state and reports user events.
- **Controller:** receives user events, coordinates interaction, invokes model operations, and selects/updates views.

```text
Actor ↔ View ⇄ Controller → Model
              ↑             │
              └──── notify ───┘
```

A controller changes the model; the model notifies subscribed views when state changes; views update their presentation. The Observer pattern commonly provides model-to-view notification. MVC is especially useful when one model has multiple views, such as a table, chart, and map.

#### Benefits
- separation of model, presentation, and interaction control;
- model can be tested without a UI;
- UI can be changed or replaced more easily;
- multiple views can stay consistent with one model;
- reusable UI and domain components;
- clearer ownership of changes.

#### Challenges
- event flow and update order can be confusing;
- controllers can accumulate business logic;
- models can become UI-aware if boundaries are not enforced;
- multiple views may refresh inefficiently;
- MVC variants use the terms differently, so the project must define direction and ownership;
- a model notification storm can affect performance.

Keep domain rules in the model/application service, keep views passive enough to display, and make controller actions thin and use-case oriented. Define whether a controller can modify the model directly or must call a service.

### 4. Comparing the patterns
- Transaction processing is **command-oriented** and often changes durable state.
- Pipe-and-filter is **data-stream oriented** and transforms records.
- MVC is **interactive UI-oriented** and separates model, view, and control.
A pipeline may feed a transaction handler, and an MVC controller may invoke a service, but one pattern should not be forced to perform another pattern’s primary job.

## Worked examples
### Example 1: WMITS transaction processing
Commands such as `RegisterInspection`, `ReturnInspection`, and `ApproveInspection` arrive with a transaction type. A dispatcher routes each to a handler. `ApproveInspection` checks authorization and evidence, updates the record atomically, and writes an audit event. Retrying the same command with an idempotency key does not approve twice.

### Example 2: Data-cleaning pipeline
Incoming navigation telemetry passes through validation, removal of impossible coordinates, normalization to a coordinate system, aggregation, and storage. Each filter has a contract and can be tested with sample streams. A malformed record goes to an error stream rather than stopping all valid data.

### Example 3: MVC inspection dashboard
The model contains `Inspection`, `Site`, and status rules. The table view shows current inspections, the map view plots sites, and a detail view shows evidence. Controllers handle filters, selection, and approval actions. When the model changes, subscribed views refresh without the model importing a screen class.

### Example 4: Combined MVC and service
A controller receives a submit action and calls an application service, not a database directly. The service handles authorization, transaction processing, persistence, and audit. The model/view layer displays the result. This keeps MVC from becoming a hidden business-logic container.

### Example 5: Failure behavior
A filter detects an unsupported map format. It sends the record to a quarantine stream, increments an error metric, and continues if policy allows. The transaction processor rejects an invalid command with a stable error code. The pipeline test covers back-pressure and a failed downstream filter.

## Key terms & formulas
- **Transaction:** command/request that changes or queries system state according to an atomic business operation.
- **Transaction dispatcher:** routes a transaction to the appropriate handler.
- **Transaction handler:** cohesive component implementing one transaction type/rule set.
- **Atomicity:** all required changes commit or none do.
- **Idempotence:** repeating an operation has the same intended effect as performing it once.
- **Pipe:** connection carrying a data stream from a filter output to a filter input.
- **Filter:** component that reads input, transforms it, and writes output.
- **Back-pressure:** downstream slowness signal that throttles upstream production.
- **Dead-letter stream:** isolated channel for records that cannot be processed normally.
- **Model:** domain state and behavior independent of a particular view.
- **View:** presentation of model data.
- **Controller:** interaction handler that coordinates input and model/service actions.
- **Model notification:** model change propagated to subscribed views, often via Observer.
- **Throughput (conceptual):** records or transactions processed per unit time; measure with latency, error rate, and resource use.
- **Atomicity check (qualitative):** every transaction test must assert that a forced failure leaves no partial committed change.

## Common mistakes
- Calling any command queue transaction processing without a transaction boundary and handler dispatch.
- Allowing a pipe/filter to depend on the identity of its upstream filter rather than a data contract.
- Ignoring back-pressure, ordering, dead letters, or format evolution.
- Putting all domain rules in a controller and leaving the model as a data bag.
- Letting the model depend directly on a particular view or screen.
- Forgetting that MVC names and event directions vary by framework; define the contract.
- Combining MVC, pipeline, and transactions without clear ownership of side effects.

## Exam prep
### Likely 2-mark questions
1. **Define the Transaction-Processing pattern.** A dispatcher reads transactions and routes them to specialized handlers that perform state-changing operations.
2. **What is a transaction handler?** A cohesive component implementing the rules for one transaction type or group.
3. **Differentiate a filter and a pipe.** A filter transforms data; a pipe carries the data stream between filters.
4. **Name two Pipe-and-Filter benefits.** Reuse, independent testing, flexibility, low coupling, functional cohesion—any two.
5. **Define MVC's three parts.** Model for domain state/behavior, View for presentation, Controller for user interaction coordination.
6. **Which pattern is most suitable for interactive multiple views?** MVC.
7. **What is idempotence?** Repeating a transaction has the same intended effect as executing it once.

### Long-answer answer hints
- “Explain transaction processing”: input, dispatcher, handlers, atomicity, response, errors, logging, and an example.
- “Explain pipe-and-filter”: stream, filters, pipes, transforms, concurrency, flexibility, and a diagram.
- “Explain MVC”: roles, event flow, Observer notification, multiple views, and testability.
- “Compare all three patterns”: transaction = commands/state; pipe/filter = data transformation; MVC = UI interaction separation.
- “Apply to WMITS”: choose a transaction handler for approvals, a filter for imported evidence, and MVC for the supervisor dashboard; explain boundaries.

### Sketches
```text
Transaction: input → dispatcher → handler → state/result
Pipe/filter: input → F1 → F2 → F3 → output
MVC:          View ⇄ Controller → Model → notify View
```
