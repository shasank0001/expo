---
subject: atcd
unit: 2
topic: regex-to-fsm
syllabus_ref: CSM3203 Unit-II
status: draft
---
# Regular Expression to FSM
## Overview
Every regular expression has an equivalent finite automaton. The standard construction uses small NFAs for atomic symbols and combines them systematically for union, concatenation, and star. This gives an NFA directly. If a deterministic implementation is required, remove ε-moves if necessary and apply subset construction. The construction is central to the course outcome “design a finite-state machine for a given regular expression.”

## Explanation
### Base machines
For a terminal `a`, create a start state and a final state with one `a` edge. For `ε`, create an edge from a start to a final state labeled `ε`. For `∅`, use a machine with a start that cannot reach a final state, or omit the branch when constructing a union.

### Union
To construct an NFA for `R|S`, create a new start `s` and new final `f`. Add ε-edges `s→start(R)`, `s→start(S)`, `final(R)→f`, and `final(S)→f`. The machine guesses which subexpression to use.

### Concatenation
To construct an NFA for `RS`, connect the final state of the machine for `R` to the start state of the machine for `S` with an ε-edge. The input must first be accepted by `R` and then by `S`. Alternatively, identify the final state of `R` with the start state of `S`.

### Kleene star
To construct an NFA for `R*`, create a new start and final state. Add an ε-edge from the new start to the old start, an ε-edge from the new start directly to the new final, an ε-edge from the old final back to the old start, and an ε-edge from the old final to the new final. The direct bypass handles zero repetitions; the loop handles repeated copies.

### Thompson’s construction
Repeating the three rules recursively is Thompson’s construction. It is easy to draw and always yields a small NFA with ε-transitions. Because the construction branches and skips symbols, the result is not generally a DFA.

### From NFA to DFA
After construction:

1. Compute ε-closures of NFA states.
2. Start the DFA with the closure of the NFA start.
3. For each DFA subset `S` and symbol `a`, move to
   `ε-closure(⋃_{q∈S}δ(q,a))`.
4. Mark a subset final if it contains an NFA final state.
5. Continue until no new subset appears.

This is subset construction. The resulting DFA recognizes exactly `L(R)`.

### Direct derivative construction
An alternative builds states as residual languages. If `D_a(R)` denotes the derivative of `R` after reading `a`, a DFA state can represent `R` itself and its residuals. The transition is `D_a(R)`, and a state is accepting if `ε∈D_a(R)`. This method is elegant but less common in hand-written exam solutions than Thompson plus subset construction.

### State and size considerations
Thompson’s NFA is linear in the expression size, but the equivalent DFA can be exponentially larger in the worst case. A regular expression may also be simplified before conversion. The question asks for language equivalence, not necessarily the smallest machine; minimization can be applied afterward.

## Worked examples
### Example 1: `a*`
Start with the machine for `a`. Add new start `s` and final `f`; add `s→oldStart`, `s→f`, `oldFinal→oldStart`, and `oldFinal→f`, all by ε. The accepted strings are `ε,a,aa,...`.

### Example 2: `(a|b)*a`
First make an NFA for `a|b`: a new start branches by ε to the `a` machine and `b` machine, and both old finals lead by ε to a common final. Apply star to that machine, then concatenate a final `a` machine. The resulting NFA accepts exactly strings ending in `a`.

### Example 3: subset conversion
Suppose the NFA for `a|b` has states `s`, `a1`, `b1`, `f`. The DFA start is `{s}`; on `a` it goes to `{a1,f}` and on `b` to `{b1,f}`. From `{a1,f}`, the `a` transition is empty and the `b` transition is empty because no outgoing moves exist; these become a dead DFA state in a complete DFA.

### Example 4: concatenation
For `ab`, build the `a` machine with `a0→a1` and the `b` machine with `b0→b1`. Add `a1→b0` on ε. A path reading `a` reaches `a1`, crosses the ε-edge, and reads `b` to reach the final state.

## Key terms & formulas
- Base: `M(a)` has one symbol edge; `M(ε)` has an ε edge.
- Union construction: new start branches; old finals join at new final.
- Concatenation construction: ε link from final of first to start of second.
- Star construction: bypass plus return loop.
- Subset transition: `move_D(S,a)=ε-closure(⋃_{q∈S}δ_N(q,a))`.

## Common mistakes
- A star needs both a bypass for zero repetitions and a loop for more than one.
- Concatenation order matters: `R·S` is not `S·R` in general.
- Thompson’s result is an NFA, not automatically a DFA.
- A DFA subset is accepting if it contains at least one NFA final state.

## Exam prep
**Likely 2-mark questions**
1. State Thompson’s construction rules. **Hint:** base, union, concatenation, star.
2. What is the DFA transition from a subset state? **Hint:** union then ε-closure.
3. Why can the equivalent DFA be larger than the NFA? **Hint:** exponentially many reachable subsets.

**Long-answer questions**
1. Construct an NFA for `(a|b)*abb`. **Hint:** draw each sub-machine and join them.
2. Convert a given ε-NFA to a DFA using subset construction. **Hint:** list closures and reachable subsets.
3. Explain why a regex can always be represented by a finite automaton. **Hint:** induction over expression operators.
4. Compare Thompson construction and derivative construction. **Hint:** operational recursion versus residual languages.
