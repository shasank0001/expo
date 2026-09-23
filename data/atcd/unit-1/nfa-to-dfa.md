---
subject: atcd
unit: 1
topic: nfa-to-dfa
syllabus_ref: CSM3203 Unit-I
status: draft
---
# NFA to DFA Conversion
## Overview
An NFA may have several possible moves for one input symbol, while a DFA must choose one move for every state-symbol pair. The subset construction removes this nondeterminism: each DFA state represents a set of NFA states that could be active after reading the same prefix. The resulting DFA recognizes exactly the same language. This is the formal “indefinite state machine to definite state machine” step in the syllabus.

## Explanation
### Start with the NFA
Let the NFA have states `Q`, alphabet `Σ`, transition relation `δ`, start state `q0`, and final set `F`. If it has ε-transitions, first calculate ε-closures or incorporate them into every move. The DFA alphabet is the same `Σ`.

### DFA states are subsets
A DFA state is a subset `S⊆Q`. It represents all NFA states that can be active after the same input prefix. The DFA start state is

`D0 = E(q0)`

where `E` is the ε-closure. A DFA subset `S` is final iff

`S∩F≠∅`.

There is no need to create every one of the `2^|Q|` subsets. Create only subsets reachable from `D0`.

### Transition between subsets
For a DFA subset `S` and input symbol `a`, first take every ordinary NFA move from every state in `S`:

`move(S,a) = ⋃_{q∈S} δ(q,a)`.

Then take the ε-closure if ε-moves were not removed:

`D = E(move(S,a))`.

The DFA transition is `δ_D(S,a)=D`. If `move(S,a)=∅`, the transition goes to an empty/dead subset; this can be represented as a rejecting trap state or simply as an error transition in an incomplete DFA.

### Algorithm
1. Remove ε-transitions, or calculate closures during the algorithm.
2. Mark `D0=E(q0)` as a DFA state.
3. Put `D0` in a work list.
4. For every unprocessed subset `S` and symbol `a`, compute `D=E(move(S,a))`.
5. Add `D` if it is new and mark it final if it contains an NFA final.
6. Continue until no new subset is found.
7. Draw the transition table/diagram; complete it with a dead state if required.

The number of reachable subsets can be exponential in the number of NFA states, so the construction may produce a much larger DFA.

### Correctness
By induction on input length, after reading a prefix `w`, the current DFA subset is exactly the set of NFA states reachable after `w` (including ε-closure). Thus `w` is accepted by the DFA iff that subset contains an NFA final state, which is equivalent to acceptance by the NFA.

### Connection to ε removal and minimization
Epsilon removal eliminates zero-input transitions; subset construction eliminates nondeterminism. A practical sequence is Thompson construction, ε removal, subset construction, optional DFA completion, and DFA minimization. Each step preserves the language.

## Worked examples
### Example 1: subset state
Suppose an NFA start state has `a` moves to `q1` and `q2`. The DFA state `{q0}` on `a` moves to `{q1,q2}`. The set is one DFA state because the parser does not need to know which NFA path will eventually succeed.

### Example 2: final subset
If `{q1,q2}` contains final state `q2`, the subset is a DFA final state. A string reaches acceptance if any NFA path in that set is final.

### Example 3: dead subset
If no NFA state in `S` has a move on `a`, the result is `∅`. In a complete DFA, add a non-final sink `Ddead` with self-loops on every symbol.

### Example 4: full small conversion
NFA: `q0 --a→ q1,q2`, `q1 --b→q3`, `q2 --b→q3`, `q3` final. DFA states are `{q0}`, `{q1,q2}`, `{q3}`. Transitions: `{q0} --a→ {q1,q2}`; `{q1,q2} --b→ {q3}`; all other moves go to `∅`. It accepts exactly `ab`.

### Example 5: epsilon-aware move
If the NFA start closure is `{q0,q1}` and ordinary `a` moves from `q1` to `q2`, the DFA on `a` includes the closure of `{q2}`. Reading no input may already enable several NFA states.

## Key terms & formulas
- DFA state: a subset of NFA states.
- `D0=E(q0)`.
- `δ_D(S,a)=E(⋃_{q∈S}δ(q,a))`.
- Final condition: `S∩F≠∅`.
- Reachable subsets only; worst case `2^|Q|`.
- Empty subset is the dead state in a complete DFA.

## Common mistakes
- Do not treat a subset as a single NFA state or combine transitions by choosing only one successor.
- Include ε-closure in the start state and destination when ε moves exist.
- Mark a subset final if it contains at least one final NFA state.
- A dead subset is not the same as an unreachable NFA state; it is a reachable rejection condition for a completed DFA.

## Exam prep
**Likely 2-mark questions**
1. What is the start state of the subset-construction DFA? **Hint:** ε-closure of the NFA start.
2. How is a DFA state marked final? **Hint:** intersection with NFA finals.
3. State the subset transition formula. **Hint:** union then closure.
4. Why can the DFA be exponentially large? **Hint:** many reachable subsets.

**Long-answer questions**
1. Convert a given NFA to a DFA. **Hint:** list reachable subsets and all symbol moves.
2. Convert an ε-NFA directly using ε-closures. **Hint:** start closure and closure after each move.
3. Prove the construction preserves the language. **Hint:** induction on prefix length.
4. Explain the sequence ε removal, subset construction, and minimization. **Hint:** remove different kinds of nondeterminism/surplus states.
