---
subject: atcd
unit: 1
topic: fsm-representations-and-state-identification
syllabus_ref: CSM3203 Unit-I
status: draft
---
# FSM Representations and State Identification
## Overview
A finite-state machine can be specified mathematically, as a transition table, or as a state diagram. The three representations must describe exactly the same machine. State identification is the design step of deciding what each state means, naming it clearly, and assigning transitions without missing an input case. Good representation makes acceptance and dead states obvious and makes later conversion or minimization easier.

## Explanation
### Five-tuple representation
A DFA is formally represented by

`M = (Q, Σ, δ, q0, F)`.

- `Q` is the finite set of states.
- `Σ` is the input alphabet.
- `δ` is the transition function.
- `q0 ∈ Q` is the start state.
- `F ⊆ Q` is the set of final states.

For an NFA, replace the single-valued transition function with a relation to a set of states and allow `ε`. A transition table is a practical display of the same tuple.

### Transition table
Use one row for each state and one column for each input symbol. A cell contains the next state, a set of next states for an NFA, or a dash/`∅` for a missing move. Mark the start state and final states outside or alongside the table. A table entry such as `q2` means `δ(q1,a)=q2`.

Example table for a machine that recognizes strings ending in `1`:

| state | 0 | 1 |
|---|---|---|
| `→q0` | q0 | q1 |
| `*q1` | q0 | q1 |

A star or `*` identifies final states; the arrow identifies the start state.

### State diagram
In a state diagram, circles are states. An arrow enters the start state from nowhere. Final states use a double circle. Label an edge with the input symbol; an NFA may have several edges for the same symbol, and an ε-edge is labeled `ε`. A table entry can be represented by an edge, and an edge can be read as a table entry.

### Mathematical representation
A finite automaton can also be described as a relation or as a regular-language equation. For example, if `R_i` is the set of labels on paths from the start state to state `i`, then `R_i` satisfies equations such as

`R_q0 = ε + aR_q0 + bR_q1`.

These equations are useful for the Arden-theorem method in Unit II. The state names are labels; what matters is the transition structure and final-state set.

### Mealy and Moore representations
A Mealy table gives an output in each transition cell, for example `q1/0`, where `q1` is the next state and `0` the output. A Moore table gives output beside each state. Diagrams label Mealy edges `input/output` and place output labels inside Moore states. This distinction is important when the task asks for an output machine rather than an acceptor.

### State identification procedure
1. Write the specification in plain language and identify what information must be remembered.
2. Assign a state name that summarizes the history so far, such as `seenA` or `oddZeros`.
3. Mark the initial condition with `q0`.
4. For every state and every alphabet symbol, decide the next condition and add a transition.
5. Mark every state in which the complete string is accepted.
6. Check reachability and add a trap state if a total transition function is required.
7. Rename states consistently and cross-check the table against the diagram.

For a DFA, each row must contain one move for every input. For an NFA, several moves are allowed, so “identify the next state” becomes “identify all possible next states.”

### Unreachable and trap states
An unreachable state cannot be entered from the start and can be removed for language-preserving minimization. A trap/dead state is reachable and rejects every continuation. In a complete DFA it is the destination for every missing transition. The two concepts should not be confused.

### Example of identification from a verbal specification
Specification: “accept binary strings whose last two symbols are `01`.” States can be `q0` (nothing useful yet), `q1` (last useful suffix is `0`), and `q2` (last two symbols are `01`, accepting). On input `0`, `q0→q0`, `q1→q1`, `q2→q1`; on input `1`, `q0→q0`, `q1→q2`, `q2→q0`. This suffix-state method works for many pattern-recognition problems.

## Worked examples
### Example 1: table to diagram
Take `Q={q0,q1}`, `Σ={a,b}`, `q0` start, `F={q1}`, and `δ(q0,a)=q1`, `δ(q1,a)=q1`, `δ(q0,b)=q0`, `δ(q1,b)=q0`. Draw `q0` with a start arrow, `q1` as a double circle, and four labeled edges. The table and diagram are equivalent descriptions.

### Example 2: identify an NFA
For “strings ending in `ab`,” use states `q0`, `q1` (last symbol was `a`), and `q2` (accept). From `q0`, `a` can remain in `q0` to allow a later suffix and move to `q1`; from `q1`, `b` moves to `q2`; from `q2`, a new `a` can begin a new candidate. More than one `a` move is legal because this is an NFA.

### Example 3: complete a table
If `δ(q0,a)=q1` is the only defined move and the alphabet is `{a,b}`, first complete the table with a dead state `d`: `δ(q0,b)=d`, `δ(q1,a)=d`, `δ(q1,b)=d`, and `d` loops to itself on both symbols. Then the machine is a complete DFA.

## Key terms & formulas
- 5-tuple: `(Q, Σ, δ, q0, F)`.
- `δ*: Q × Σ* → Q` is the extended transition function.
- Diagram conventions: start arrow, double-circle final state, ε-labeled edge for NFA.
- Trap state: complete-DFA destination for an undefined move.
- State equivalence: states with identical future acceptance behavior.

## Common mistakes
- A start state is not automatically final, and a final state is not automatically the start.
- A missing table cell is not the same as a self-loop unless the specification says so.
- In an NFA, a cell may contain several states; do not force one.
- Do not call an unreachable state a dead state without explaining the difference.

## Exam prep
**Likely 2-mark questions**
1. List ways to represent an FSM. **Hint:** 5-tuple, table, diagram.
2. Mark start and final states in a diagram. **Hint:** incoming arrow and double circle.
3. Define a trap state. **Hint:** complete-DFA sink that cannot accept.

**Long-answer questions**
1. Draw a DFA and its complete transition table for a stated language. **Hint:** identify states and verify every column.
2. Explain how to identify states from a natural-language specification. **Hint:** summarize the relevant history.
3. Convert a table into a state diagram and back. **Hint:** preserve start, final, and labels.
4. Distinguish reachable and unreachable states. **Hint:** reachability from `q0` versus future rejection.
