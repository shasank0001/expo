---
subject: atcd
unit: 1
topic: fsm-minimization
syllabus_ref: CSM3203 Unit-I
status: draft
---
# FSM Minimization
## Overview
DFA minimization finds the smallest DFA that recognizes exactly the same language as a given complete DFA. It is both a practical way to reduce hardware and a theoretical expression of the idea of indistinguishable states. Two states are equivalent when no continuation can make one accepting and the other rejecting. Partition refinement discovers and merges such states.

## Explanation
### What optimization means
A DFA may contain states that are never reached, states that have identical futures, and unnecessary details in its diagram. Minimization removes or merges them without changing `L(M)`. The result is unique up to renaming when the original DFA is complete and accessible. The minimum-state DFA is the canonical recognizer for the language.

### Myhill–Nerode viewpoint
Two prefixes `u` and `v` are equivalent when, for every suffix `z`, `uz∈L` exactly when `vz∈L`. If some suffix distinguishes them, the prefixes lead to distinguishable states. The maximum number of distinguishable residual languages is the minimum number of DFA states. This is a conceptual justification for the partition algorithm.

### Remove unreachable states
Start from `q0` and mark states reachable by paths. Delete every unmarked state and its transitions. A complete DFA may have a reachable trap state; do not delete it merely because it never accepts.

### Initial partition
Put final states in one block and non-final states in another. The key observation is that a final/non-final distinction is visible with the empty continuation: one state accepts now and the other does not.

### Table-filling algorithm
For a complete DFA with `n` states:

1. Mark every pair `(p,q)` with one final and one non-final.
2. For every unmarked pair and every `a∈Σ`, mark the pair if `(δ(p,a),δ(q,a))` is already marked.
3. Repeat until no new mark is added.
4. Merge each unmarked equivalence class.

The algorithm is especially easy to show in an exam. A marked pair has a distinguishing symbol or suffix.

### Partition-refinement / table-filling equivalence
The table-filling algorithm and Moore’s partition refinement are the same idea in different presentations. Start with `{F, Q−F}` and repeatedly split a block when two states go to different blocks on the same symbol. Stop when a stable partition is reached.

### Example of a split
Suppose `p` and `q` are both non-final. On `a`, `p` goes to a final state and `q` goes to a non-final state. They must be separated because the suffix `ε` distinguishes the resulting states. If transitions land in states already known to be equivalent, no new split is needed.

### Minimization versus NFA
DFA minimization is directly defined for a complete DFA. An NFA can first be converted to a DFA and then minimized, or specialized algorithms can be used. “Removing a loop” is not a general minimization method unless equivalence is proved.

## Worked examples
### Example 1: minimize a parity DFA
For a DFA accepting strings with an even number of `a`s, `q0` is even/start/final and `q1` is odd/non-final. Both transitions on `a` swap the states; on `b`, each stays. The two states are not equivalent: the empty suffix distinguishes them. The DFA is already minimal.

### Example 2: merge equivalent states
Consider a completed DFA with `q0` start, final `qf`, and a non-final `qd` that loops on every symbol. If `q0` also loops on every symbol, then `q0` and `qd` have exactly the same future behavior (both reject every continuation) and may be merged; being the start state does not prevent equivalence. If their transitions differ on even one symbol, they must remain separate. This illustrates why final/non-final membership and complete transition behavior, not the state’s name or role, decide equivalence.

### Example 3: table-filling trace
Suppose `p` and `q` are both final, `δ(p,a)=r`, `δ(q,a)=s`, and `r` is final while `s` is non-final. The pair `(p,q)` is unmarked initially because both are final, but it becomes marked when examining `a`; hence the two states are distinguishable.

### Example 4: minimized machine construction
After classes `C1={q0,q2}` and `C2={q1,q3}`, create states `[C1]` and `[C2]`. For each input `a`, set `δ([Ci],a)=[Cj]` if every state in `Ci` goes to a state in `Cj` on `a`. The start class is the class containing `q0`; final classes are those containing an original final state.

## Key terms & formulas
- Equivalent states: `δ*(p,z)∈F ⇔ δ*(q,z)∈F` for every `z∈Σ*`.
- Initial partition: `P0={F,Q−F}`.
- Refinement: split block `B` when `δ(B,a)` intersects more than one current block.
- `δ*`: zero or more transitions.
- Minimal DFA: accessible, complete, and all states pairwise distinguishable.

## Common mistakes
- A dead state and an unreachable state are different; a dead state is often reachable and required for completeness.
- States cannot be merged merely because they have the same number of outgoing edges.
- Use FOLLOW-like continuation logic for reductions, not only the immediate next input.
- The empty suffix means final and non-final states are always distinguishable.

## Exam prep
**Likely 2-mark questions**
1. Define equivalent DFA states. **Hint:** same acceptance behavior for every continuation.
2. What is the initial partition? **Hint:** final versus non-final.
3. State the purpose of DFA minimization. **Hint:** smallest equivalent recognizer.

**Long-answer questions**
1. Apply table-filling to a complete DFA. **Hint:** mark final/non-final pairs first, then recursively mark successors.
2. Explain partition refinement with a state-splitting example. **Hint:** `δ(B,a)` must lie in one block.
3. Minimize a supplied DFA and draw the result. **Hint:** remove unreachable states, partition, merge.
4. Relate Myhill–Nerode equivalence to minimal-state construction. **Hint:** distinguishable residuals.
