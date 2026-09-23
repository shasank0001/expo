---
subject: atcd
unit: 1
topic: finite-state-machine-types
syllabus_ref: CSM3203 Unit-I
status: draft
---
# Finite State Machine Types
## Overview
Finite state machines model systems whose future behavior depends on a finite summary of the past. The summary is the current state; the next state is selected by an input symbol and sometimes an output. In automata theory, DFA and NFA are the principal recognizer types. In compiler and hardware design, Mealy and Moore machines describe transition/output behavior. The distinction is about determinism and whether output depends on the current state or also on the input.

## Explanation
### Basic finite-state machine
A finite-state machine has a finite set of states, an input alphabet, a transition function, and a start state. Some variants also have final states or an output alphabet. A machine reads symbols in order; after each symbol it changes state. A **recognizer** accepts or rejects a complete string. A **transducer** produces output while processing input.

### DFA
A deterministic finite automaton is a 5-tuple

`M = (Q, Σ, δ, q0, F)`

where `Q` is the finite state set, `Σ` the input alphabet, `δ: Q × Σ → Q`, `q0` the start state, and `F ⊆ Q` the final states. For every `(q,a)`, exactly one next state is specified. An incomplete table is often completed with a dead state before it is called a complete DFA.

A DFA recognizes `a^n b^n`? No: it cannot do so, because it has no unbounded counter. It can recognize parity, occurrence of a substring, or strings ending in a particular pattern.

### NFA
A nondeterministic finite automaton has the same broad components, but its transition relation may be a set-valued function:

`δ: Q × (Σ ∪ {ε}) → 2^Q`.

For a given state and input, the machine may have zero, one, or several possible next states. It may also move without consuming input on `ε`. Acceptance means that **at least one** computation reaches a final state after the entire input is consumed. An NFA is useful for compactly expressing “choose one of several paths” and for constructing machines from regular expressions.

### DFA versus NFA
DFA execution follows one definite path. NFA execution may branch, and we can think of it as searching for a successful path. Every regular language accepted by an NFA has an equivalent DFA, obtained by subset construction. A DFA can be exponentially larger in the worst case, so NFA-to-DFA conversion can be expensive.

### Mealy machine
A Mealy machine is `M = (Q, Σ, Γ, δ, λ, q0)`, with output alphabet `Γ`. Its output is

`λ(q,a)`,

so output depends on the current state and the input symbol. A transition can be labeled `a/z`, meaning read `a` and output `z`. The output is produced when the transition is taken; the machine need not have a separate accepting state.

Example: a one-state machine labeled `0/0, 1/1` outputs each input bit unchanged.

### Moore machine
A Moore machine is `M = (Q, Σ, Γ, δ, λ, q0)`, with output

`λ(q)`,

depending only on the state. Each state is associated with an output. A Moore machine is often easier to represent in synchronous hardware, while a Mealy machine can respond one transition earlier.

Example: a divider-control machine may output `BUSY` while in a wait state and `DONE` after entering a completed state.

### DFA/NFA versus Mealy/Moore
The pairs classify different questions. DFA/NFA ask “which strings are accepted?”; Mealy/Moore ask “what output is produced?” A deterministic finite automaton can be viewed as a restricted Moore/Mealy transducer by ignoring output, but the terms should not be mixed when answering an exam question.

### Machine classes in the hierarchy
Finite automata recognize regular languages. Adding a stack gives a pushdown automaton for context-free languages. Adding a read-write tape gives a Turing machine for general computation. This progression is a useful way to remember why a compiler uses an automaton for tokens and a PDA/CFG-style parser for nested syntax.

## Worked examples
### Example 1: parity DFA
`Q={even,odd}`, `q0=even`, `F={odd}`. On `0`, swap the states; on `1`, remain in the same state. It accepts binary strings with an odd number of zeros.

### Example 2: substring NFA
To recognize strings containing `ab`, use a start state that can begin a candidate `a` and a final state reached after `b`. On `a`, the NFA can stay in the start state and also move to a “saw a” state. This compactly represents both possible histories.

### Example 3: Mealy versus Moore
For the language “strings ending in `1`,” a DFA has two states and accepts the final state. A Mealy version can output `1` on the transition that consumes the last `1`; a Moore version stores the accepting status as the output of the state after that transition.

## Key terms & formulas
- DFA transition: `δ(q,a) = r`, one result.
- NFA transition: `δ(q,a) ⊆ Q`, possibly empty or multiple.
- Epsilon closure: `ε-closure(q)` includes every state reachable using only ε-moves.
- Mealy output: `λ(q,a)`.
- Moore output: `λ(q)`.
- Acceptance: end state belongs to `F` (recognizer).

## Common mistakes
- Determinism means one move for each state-symbol pair, not one total outgoing edge per state.
- An NFA does not accept as soon as any partial path reaches a final state; the entire input must be consumed.
- Mealy output depends on transition; Moore output depends on state.
- DFA/NFA and Mealy/Moore are separate classification axes.

## Exam prep
**Likely 2-mark questions**
1. Define DFA and NFA. **Hint:** give the transition-function difference.
2. Define Mealy and Moore machines. **Hint:** `λ(q,a)` versus `λ(q)`.
3. State the language class of finite automata. **Hint:** regular languages.

**Long-answer questions**
1. Compare DFA, NFA, Mealy, and Moore machines in a table-like explanation. **Hint:** memory, determinism, output, and use.
2. Construct a DFA and NFA for strings ending in `01`. **Hint:** show states and transitions.
3. Explain why every NFA has an equivalent DFA. **Hint:** subset construction.
4. Give a small Mealy and Moore machine that computes parity. **Hint:** label transitions/states with outputs.
