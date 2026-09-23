---
subject: oose
unit: 5
topic: graph-based-black-box-testing
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Graph-Based Black-Box Testing
## Overview
Graph-based black-box testing derives tests from a behavioral model rather than source code. The model can be a state-transition graph, decision table, cause-and-effect graph, or another representation of how inputs/events lead to outputs and states. Tests then select paths, transitions, combinations, and invalid sequences that verify externally observable behavior.

The technique is valuable when a system has modes, workflows, permissions, device states, or event sequences. It complements equivalence partitioning and boundary-value analysis: partitions choose representative input classes, boundaries choose risky values, and graph-based methods choose behaviorally meaningful sequences.

## Explanation
### 1. State-transition graph
A state-transition graph represents a system or object as states connected by events/transitions. A transition may have:
- source state;
- event or input;
- guard condition;
- action;
- target state;
- output or postcondition.

For a login subsystem:

```text
LoggedOut --valid credentials--> LoggedIn
LoggedIn  --logout-----------> LoggedOut
LoggedIn  --three bad attempts-> Locked
Locked    --administrator reset--> LoggedOut
```

Tests can cover every state, every transition, valid paths from the initial state, invalid transitions, and sequences that revisit states. A transition not shown may represent an undefined or illegal event; the model should state whether it is ignored, rejected, or a defect.

### 2. Test-generation process
1. Identify the behavioral scope and initial state.
2. Draw states, events, guards, actions, and outputs.
3. Mark required and prohibited transitions.
4. Find paths from the initial state to important terminal/goal states.
5. Select tests for each transition, path, and invalid event.
6. Derive input data, timing, and preconditions.
7. Define expected state, output, side effect, and error.
8. Execute and compare with the model.
9. Update the model when requirements or observed behavior changes.

### 3. Graph coverage
Useful measures include:
- **state coverage:** states visited ÷ modeled states × 100%;
- **transition coverage:** transitions exercised ÷ modeled transitions × 100%;
- **path coverage:** selected paths exercised ÷ selected paths × 100%;
- **event coverage:** event types received ÷ required event types × 100%;
- **condition/guard coverage:** guards true and false where relevant.

State coverage alone is weak: a test can visit every state while missing a critical transition. Report the measure and excluded/unreachable states.

### 4. Decision tables
A decision table is a compact graph/table of conditions and actions. It is useful for permissions, eligibility, pricing, and error behavior. Each column is a rule; each row is a condition or action. Check rules for:
- valid and invalid combinations;
- overlap;
- missing combinations;
- contradictory actions;
- unreachable conditions.

A test set can include one representative test for each rule plus boundary and stress cases.

### 5. Cause-and-effect graphs
A cause-and-effect graph starts with causes (inputs/conditions) and effects (outputs/actions), connects them, and converts the graph into a decision table. It helps find missing relationships and generates combinations that link causes to effects. Not every effect is independent; the technique must respect the business rule and avoid combinatorial explosion.

### 6. Sequence and workflow graphs
A workflow or activity graph can show branches, loops, optional steps, and alternative paths. Test derivation selects:
- each main path;
- each decision branch;
- optional/extension path;
- cancellation, retry, and recovery;
- invalid order and skipped required step;
- loops and boundary repetitions.

For a chat system, a test might cover send, retry, offline queue, recipient unavailable, duplicate delivery, cancellation, and logout. A graph makes the order and state explicit.

### 7. Model quality
A test model is useful only if it is correct and current. Review it with requirements, domain experts, and implementation knowledge. Define whether the model is normative (the system must behave this way) or descriptive (this is what the current system does). A mismatch is a requirement/design finding, not automatically a test failure to be “fixed” by changing the expected result.

### 8. Combining with other techniques
Use equivalence partitioning to choose data for a transition guard, boundary analysis for values at a guard, and condition testing for internal Boolean combinations. Use sequence diagrams or event traces to verify graph paths. A black-box graph test can still use a mock or simulator to reach a state, but the assertion remains based on the external contract.

## Worked examples
### Example 1: Inspection state graph
```text
Draft --submit with evidence--> Submitted
Submitted --assign--> UnderReview
UnderReview --approve--> Approved
UnderReview --return with reason--> Returned
Returned --edit and submit--> Submitted
```
Tests cover each transition, submission without evidence, return without a reason, editing an Approved record, and repeated submission. A state-machine test resets state between cases or uses independent fixtures.

### Example 2: Message delivery graph
```text
Composing --send, online--> Sent
Sent --ack--> Delivered
Sent --timeout--> PendingRetry
PendingRetry --retry success--> Delivered
PendingRetry --max retries--> Failed
```
A graph-based test selects the full retry path, duplicate ack, recipient offline, and cancellation. It checks side effects such as a notification appearing once, not only the final label.

### Example 3: Decision table for closure
| Evidence | Assigned supervisor | Expected action |
|---|---|---|
| Missing | Any | Block |
| Present | No | Block/assign |
| Present | Yes | Allow close |

Add an invalid combination (missing evidence and unauthorized user) and verify the most informative error and audit behavior. Review the table for overlapping or missing rules.

### Example 4: Model mismatch
A test expects an unlocked state after an administrator reset, but the system remains locked. The team determines whether the requirement or the model is wrong. It records the discrepancy, fixes the appropriate artifact, and adds a regression test. It does not simply change the expected result to match a defect.

## Key terms & formulas
- **Graph-based black-box testing:** test derivation from a behavioral model rather than source code.
- **State:** condition in which the system responds in a defined way.
- **Event:** input or occurrence that may trigger a transition.
- **Transition:** event plus guard/action leading to a target state.
- **State coverage:** visited states ÷ modeled states × 100%.
- **Transition coverage:** exercised transitions ÷ modeled transitions × 100%.
- **Decision table:** conditions and actions arranged into rules.
- **Cause-and-effect graph:** graph connecting causes to effects, converted into tests/table.
- **Path:** sequence of transitions from an initial to a goal state.
- **Invalid transition:** event not valid for the current state; expected rejection/ignore/error is specified.
- **Model defect:** discrepancy between the normative model and required behavior; it must be analyzed, not hidden.

## Common mistakes
- Using a state graph without initial/final states or expected outputs.
- Claiming state coverage is sufficient while missing transitions.
- Testing only the shortest happy path.
- Omitting invalid event order, cancellation, loops, and recovery.
- Treating every unspecified transition as an acceptable no-op.
- Combining all combinations without checking feasibility.
- Updating the model merely to make a failing test pass.

## Exam prep
### Likely 2-mark questions
1. **Define graph-based black-box testing.** Deriving black-box tests from a behavioral model such as state transitions, decision tables, or cause-effect graphs.
2. **What is a state-transition graph?** A graph of states connected by events, guards, actions, and outputs.
3. **Name three coverage measures.** State, transition, path, event, or guard coverage—any three.
4. **What is a decision table?** A table of conditions and actions arranged as rules for test generation.
5. **Why test invalid transitions?** To verify safe rejection, error behavior, and state preservation.
6. **Differentiate this technique from flow-graph path testing.** State graph is black-box behavior; flow graph is internal control structure.

### Long-answer answer hints
- “Explain graph-based black-box testing”: model types, process, coverage, invalid paths, model quality, and combination with other techniques.
- “Draw and test an inspection state machine”: states, transitions, guards, errors, and selected test cases.
- “Explain state versus transition coverage” with a simple example and why both matter.
- “Use a decision table for access/closure”: conditions, actions, feasible rules, and boundary/negative tests.
- “Discuss limitations of graph-based testing”: model cost, combinatorics, data values, implementation defects, and model mismatch.

### Coverage reminder
A state graph is meaningful only when the model specifies initial state, transitions, guards, actions, outputs, and what happens on invalid input.
