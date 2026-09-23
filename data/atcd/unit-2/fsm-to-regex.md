---
subject: atcd
unit: 2
topic: fsm-to-regex
syllabus_ref: CSM3203 Unit-II
status: draft
---
# FSM to Regular Expression
## Overview
Every finite automaton recognizes a regular language, so its language can be described by a regular expression. The usual method is state elimination: progressively remove intermediate states while preserving all possible paths, then solve for the start-to-final expression. The result is a regular expression over the same alphabet and can be converted back to a machine for verification.

## Explanation
### Preparation
For an NFA with ε-transitions, either remove ε first or use generalized state-elimination equations that account for ε. Multiple final states can be connected to one new final state, and multiple start states can be connected to one new start. For a complete DFA, label every edge by its symbol; parallel edges are combined with union.

### Basic path algebra
A path label is a regular expression. Parallel paths use union, consecutive paths use concatenation, and a cycle that can be repeated uses star. For example, a loop labeled `ab*` followed by an edge labeled `a` has expression `ab*a`.

### State-elimination rule
When eliminating state `r`, consider all paths that enter `r` from `i` and leave it for `j`. If the edge labels are `R_ij`, `R_ir`, `R_rr`, and `R_rj`, replace the direct path by

`R'_ij = R_ij + R_ir (R_rr)* R_rj`.

Also add paths from `i` to any other state and from any other state to `j`. The `R_rr*` portion allows zero or more trips through `r`. Eliminating states one at a time eventually leaves only a start and final state.

### Handling loops and omitted states
A self-loop `r→r` appears in `R_rr*`; it must be starred. A path that leaves `r` and never returns appears once, so it is not starred. If an edge is labeled `ε`, use `ε`; if there is no edge, use `∅`. A direct edge and an indirect path are alternatives and therefore joined by `+`.

### Arden’s theorem
State equations can be solved systematically. If `X = YX*` and `ε∉Y`, then `X=Y*`; similarly `X=XY*` gives `X=Y*`. This is the algebraic version of solving a loop equation and is especially useful in the FSM-to-regex syllabus problem. A separate file gives a detailed treatment.

### Multiple final states
A regex must describe paths that end in any accepting state. Add a new final state `f` with ε-transitions from every old final state, then eliminate all old states. Alternatively, take the union of expressions from the start to each final state, taking care to account for the new start.

### Validation
After obtaining `R`, check several accepted and rejected strings. The expression should include paths that revisit states as many times as the automaton permits, not just simple paths. If the original automaton is deterministic, the conversion is still valid; determinism is not required after conversion.

## Worked examples
### Example 1: star loop
Suppose the only path is `q0 --a→ q1`, `q1 --b*→ q1`, and `q1 --a→ qf`. The expression is `ab*a`: read `a`, repeat `b` zero or more times, then read final `a`.

### Example 2: eliminate a middle state
Let `q0 --a→ q1`, `q1 --b→ q1`, `q1 --c→ qf`, and there is no direct `q0→qf` path. Eliminating `q1` gives `ab*c`.

### Example 3: alternatives and loop
If `q0 --a→ q1` and `q0 --b→ q1`, then the edge from `q0` to `q1` is `a+b`. If `q1 --c→ q1` and `q1 --d→ qf`, eliminating `q1` yields `(a+b)c*d`. The parentheses show that the prefix alternatives happen before the repeated suffix.

### Example 4: two final states
If `q0` reaches `f1` by `a` and `f2` by `b`, connect both finals to a new final by ε and eliminate the old finals. The result is `a+b`, not just one branch.

## Key terms & formulas
- State-elimination update: `R'_ij=R_ij+R_ir(R_rr)*R_rj`.
- Missing edge label: `∅`; zero-length edge: `ε`.
- Multiple paths: `+`; sequential paths: concatenation.
- Arden: `X=YX*` implies `X=Y*` when `ε∉Y`.
- A regular expression is complete only if it includes every accepting path.

## Common mistakes
- Forget to star a self-loop when eliminating a state.
- Use concatenation for alternatives instead of union.
- Omit a path that reaches one of several final states.
- Treat a cycle as traversable only once; star is what permits repetition.
- Do not claim the expression is shortest unless a minimization step was actually performed.

## Exam prep
**Likely 2-mark questions**
1. Explain state elimination in FSM-to-regex conversion. **Hint:** replace paths through an intermediate state.
2. State Arden’s theorem. **Hint:** solve a regular-language equation under the ε condition.
3. What do union, concatenation, and star represent? **Hint:** alternatives, order, and repetition.

**Long-answer questions**
1. Convert a supplied NFA to a regular expression. **Hint:** prepare finals, eliminate states, simplify.
2. Derive a regex for `a(b|c)*a` from a machine. **Hint:** loop and boundary labels.
3. Show how a self-loop is represented. **Hint:** `R_rr*`.
4. Verify a converted expression with sample strings. **Hint:** test shortest, repeated, and rejected cases.
