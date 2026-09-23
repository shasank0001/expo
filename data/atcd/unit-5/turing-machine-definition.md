---
subject: atcd
unit: 5
topic: turing-machine-definition
syllabus_ref: CSM3203 Unit-V
status: draft
---
# Turing Machine Definition
## Overview
A Turing machine is a theoretical computer with a read-write tape that serves as unbounded memory. It reads or writes one tape cell at a time, moves its head left or right (sometimes staying put), and changes control state according to a transition rule. Unlike a finite automaton, a Turing machine can perform arbitrary computation, so it models the power of a general-purpose computer.

## Explanation
### Formal definition
A deterministic Turing machine is a 7-tuple

`M=(Q,Σ,Γ,δ,q0,qaccept,qreject)`

where:

- `Q` is the finite set of control states;
- `Σ` is the input alphabet;
- `Γ` is the tape alphabet and contains `Σ` plus the blank symbol `⊔`;
- `δ: Q×Γ → Q×Γ×{L,R}` (or `{L,R,S}`) is the transition function;
- `q0∈Q` is the start state;
- `qaccept∈Q` is the accepting halting state; and
- `qreject∈Q` is the rejecting halting state.

For a nondeterministic TM, `δ` maps each pair to a set of possible triples. A machine configuration records the current state, tape contents, and head position. The tape is usually one-way infinite to the right, but a two-way infinite tape is an equivalent common model.

### Tape and head
Initially, the input is written on consecutive tape cells and the head points at the first input symbol. All other cells contain blanks. A transition reads the symbol under the head, writes a replacement, moves, and enters a new state. The head can move left, right, or stay in an extended alphabet definition. The tape has no fixed finite capacity, which supplies unbounded working storage.

### Computation and halting
Starting from `(q0,w)`, each transition produces a new configuration. The machine accepts if it reaches `qaccept` and rejects if it reaches `qreject`. It may also loop forever. A language is decidable/recursive if some TM always halts and accepts exactly its members; it is recognizable/recursively enumerable if a TM accepts members but may loop on nonmembers.

### Why the model matters
Finite automata cannot count without bound, PDAs can use a stack, and TMs can use the tape for both data and a simulated program. A TM can simulate a PDA, a finite automaton, and a conventional stored-program computer. This universality is the reason Turing machines are used to define computability and undecidability.

### Common examples
A TM can change a unary string `111` into `000`, decide whether a binary string represents a multiple of a fixed number by storing a remainder on the tape, or simulate another machine. The exact construction may be multi-step, but every step is one transition.

## Worked examples
### Example 1: unary complement
States scan the first nonblank symbol, write its opposite, and move right. A final state accepts when the head reaches a blank. For `110`, the output tape is `001`.

### Example 2: compute `x+1`
Scan right to the last digit, remember whether the machine is already at the end, replace trailing `9`s by `0`s, and replace the first non-9 digit by its successor. If every digit is `9`, write a leading `1` and change all previous `9`s to `0`s. This illustrates tape rewriting.

### Example 3: simulate a finite automaton
Encode the current DFA state in the control state, read each input symbol, follow the transition table, and accept when the DFA final state is reached. The TM uses no extra memory but can still simulate the DFA.

### Example 4: nontermination
A TM can move right forever on blanks without entering a halting state. This is why acceptance and rejection are separate decisions: failure to reach `qaccept` does not automatically mean `qreject`.

## Key terms & formulas
- Configuration: `(q,w,i)` with state `q`, tape `w`, head position `i`.
- `δ(q,a)=(p,b,D)`: read `a`, write `b`, move `D`, enter `p`.
- Tape alphabet: `Γ`, with blank `⊔`.
- Decidable language: decider halts on every input.
- Recognizable language: accepts members; may loop on nonmembers.

## Common mistakes
- The tape is not a fixed array and the head is not limited to input cells.
- A transition can write a different symbol, not merely move.
- A TM that never halts has neither accepted nor rejected.
- `L` and `R` refer to head movement, not left/right input direction semantics.

## Exam prep
**Likely 2-mark questions**
1. Define a Turing machine. **Hint:** 7-tuple and read-write tape.
2. What can the head do in one step? **Hint:** read/write, state change, move.
3. Distinguish decidable and recognizable languages. **Hint:** always halt versus possible loop.
4. Why is the tape unbounded? **Hint:** arbitrary working storage.

**Long-answer questions**
1. Draw a TM that complements a unary string. **Hint:** states and transition table.
2. Explain how a TM can simulate a DFA. **Hint:** DFA state in control state.
3. Compare FA, PDA, and TM memory and power. **Hint:** finite, stack, tape.
4. Describe a machine that increments a binary number. **Hint:** trailing ones and carry.
