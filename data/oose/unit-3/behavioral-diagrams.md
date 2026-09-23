---
subject: oose
unit: 3
topic: behavioral-diagrams
syllabus_ref: CSM3102 Unit-III
status: draft
---
# Behavioral Diagrams
## Overview
Behavioral diagrams describe what a system does, how work flows, how objects interact, and how states change. The syllabus names use-case, activity, state-machine, and sequence diagrams. Each has a different question:
- **Use case:** what goals do actors want from the system?
- **Activity:** what steps, decisions, and parallel work make up a workflow?
- **State machine:** what states can an object be in and what events change them?
- **Sequence:** what messages occur between objects and in what order?

Using the four views together prevents a common mistake: treating a user goal, a workflow, a state, and a method call as the same thing.

## Explanation
### 1. Use-case diagrams
A use case represents a complete goal of an actor or external system interacting with the system. The actor is a role, not necessarily a person. A system boundary, actor, and named use case form a simple diagram. Use cases should be named with a verb phrase and represent meaningful user value.

Use-case descriptions can include preconditions, main flow, alternate flows, exceptions, postconditions, business rules, and related requirements. Inclusion (`<<include>>`) identifies behavior always used by another use case; extension (`<<extend>>`) identifies optional or conditional behavior added at a defined point.

Common mistakes are treating a screen as a use case, making a low-level method a user goal, and drawing a huge list with no scope or priority.

### 2. Activity diagrams
An activity diagram models a workflow or algorithm as nodes connected by control/data flow. Nodes may be:
- **action:** an executable step;
- **decision/merge:** branches and joins;
- **fork/join:** parallel or concurrent paths;
- **start/end:** beginning and termination;
- **object nodes:** data or artifacts produced or used.

Activity diagrams can describe business process, use-case flow, or internal algorithm. Swimlanes show responsibility by actor or organizational unit. A decision diamond has mutually understandable outgoing paths; guards make conditions explicit. Loops and parallel paths need termination and synchronization rules.

### 3. State-machine diagrams
A state-machine diagram models the lifecycle of one class, an object, or a system. Elements include:
- initial and final states;
- states, possibly with entry, exit, do, and activity behavior;
- events/transitions;
- guards;
- effects/actions;
- composite states, orthogonal regions, and history states where needed.

A transition is meaningful only with its event and target. Do not use a state machine for the entire business workflow when an activity diagram is clearer; use it for conditions that affect what an object may do next.

### 4. Sequence diagrams
A sequence diagram shows interactions among objects over time. Vertical lifelines represent participants; horizontal arrows represent messages. Solid arrows commonly represent synchronous calls; filled/open arrow styles vary by notation/tool; dashed arrows represent replies. Activation bars show focus of control, while notes and constraints explain conditions and alternative fragments.

Sequence diagrams can show object creation, destruction, loops, alternatives, and parallel fragments. They are excellent for protocol design, API behavior, and explaining a use-case scenario, but they can become unreadable if every helper call is shown.

### 5. Choosing the correct diagram
- “What does the customer want?” → use case.
- “What steps must the team follow?” → activity.
- “What can this object be and what changes it?” → state machine.
- “Who sends which message, in what order?” → sequence.
A complete analysis often uses all four, linked by scenario and requirement IDs. Names and terminology should agree across diagrams.

### 6. Behavioral scenarios and exception flows
A robust model includes:
- success path;
- alternative user choices;
- invalid or unauthorized action;
- missing data or boundary value;
- timeout and external-service failure;
- cancellation, undo, compensation, and recovery;
- concurrency and duplicate messages;
- audit/security side effects.

This is especially important for WMITS, GPS, and instant messaging, where the normal path alone gives false confidence.

### 7. Consistency and traceability
Link a use case to activity, state, and sequence elements. A `Returned` state should appear in the state machine and the inspector's workflow; a sequence message that changes state should point to the relevant requirement. Names should be stable, and a change in one view should trigger review of related views.

## Worked examples
### Example 1: ATM
- Use case: “Withdraw cash.”
- Activity: authenticate → select withdrawal → check balance → dispense → print receipt, with insufficient-funds branch.
- State machine: `CardAbsent → CardPresent → Authenticated → Dispensing → Complete`, with `Locked` and `Error` states.
- Sequence: ATM sends `validatePin` to AccountService, then `debit` to Ledger, then returns a result.
The four views answer different questions and should not be merged into one diagram.

### Example 2: Inspection workflow
A use case “Submit inspection” has a main flow of entering site and evidence. An activity shows two parallel checks—policy validation and file-virus scan—joined before commit. A state machine adds `Draft`, `Submitted`, `Returned`, and `Approved`. A sequence shows the phone, service, database, and audit log messages.

### Example 3: Optional extension
“Record a violation” includes “Validate evidence” with `<<include>>` because evidence validation is always part of the goal. “Escalate case” may `<<extend>>` “Review inspection” when a supervisor chooses escalation; it is optional, not always executed.

### Example 4: Exception scenario
A message sender can retry, fail, or cancel. An `alt` fragment in the sequence diagram shows each path; the activity diagram shows whether the user or retry worker controls the branch; the state diagram shows `Sending → Delivered | Failed | Cancelled`. This is more complete than a sequence showing only a successful send.

## Key terms & formulas
- **Behavior:** observable actions, interactions, and responses over time.
- **Actor:** external role/person/system that interacts with the system.
- **Use case:** complete user or external-system goal.
- **Activity diagram:** workflow of actions, decisions, and parallel paths.
- **State machine:** states, events, guards, transitions, and effects.
- **Sequence diagram:** time-ordered messages among lifelines.
- **Include:** mandatory behavior used by a use case.
- **Extend:** optional/conditional behavior added to a use case.
- **Swimlane:** responsibility partition in an activity diagram.
- **Lifeline:** participant in a sequence diagram.
- **Synchronous message:** call whose sender waits for a response.
- **Asynchronous message:** message sent without waiting for immediate result.
- **Guard:** condition on a branch or transition.
- **Scenario:** a concrete path through behavior, including exceptions.
- **Interaction coverage:** scenarios with tests ÷ approved scenarios × 100%.

## Common mistakes
- Calling a use case a method, screen, or noun.
- Putting all business steps in a sequence diagram and leaving workflow unclear.
- Showing states without events or transitions.
- Drawing an activity branch without a merge or clear termination.
- Omitting alternate and exception paths.
- Confusing include and extend, or using them for ordinary method calls.
- Using different names for the same actor, use case, or event across diagrams.

## Exam prep
### Likely 2-mark questions
1. **Name four UML behavioral diagrams.** Use case, activity, state-machine, and sequence.
2. **What is a use case?** A complete goal of an actor interacting with the system.
3. **Differentiate activity and state diagrams.** Activity shows workflow/steps; state shows an object's states and event-triggered transitions.
4. **What does a sequence diagram show?** Time-ordered messages between objects/lifelines.
5. **Differentiate include and extend.** Include is mandatory reusable behavior; extend is optional/conditional behavior.
6. **What is a guard?** A condition that determines whether a branch or transition is taken.

### Long-answer answer hints
- “Explain the four behavioral diagrams”: purpose, elements, notation, and one ATM/inspection example for each.
- “Draw a use-case diagram and write a use case”: actors, boundary, main/alternate/exception flows, postconditions, include/extend.
- “Draw an activity diagram with a decision and parallelism”: actions, merge/fork/join, swimlanes, guard labels, and termination.
- “Draw a state machine”: initial/final states, event, guard, action, and invalid transition.
- “Draw a sequence diagram for login/withdrawal/inspection”: lifelines, synchronous/asynchronous messages, returns, alternatives, and notes.

### Comparison sketch
```text
Use case: goal       Activity: workflow       State: condition
Sequence: message order
All four: one consistent scenario and vocabulary
```
