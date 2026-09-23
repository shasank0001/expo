---
subject: atcd
unit: 4
topic: slr-parsing
syllabus_ref: CSM3203 Unit-IV
status: draft
---
# SLR Parsing
## Overview
SLR (Simple LR) parsing is a bottom-up method that builds the LR(0) item-set collection and uses FOLLOW sets to choose reductions. It is less powerful than canonical LR(1) and LALR, but it often produces small tables and is easy to construct by hand. Its central rule is simple: for an item `A→γ·`, reduce on every terminal in `FOLLOW(A)`.

## Explanation
### Augmented grammar
Add a new start production `S'→S`. The parser starts with item `S'→·S` and stack state 0. The accepting item is `S'→S·`. The augmented grammar makes the initial stack context explicit and prevents accepting before the original start symbol is complete.

### LR(0) item sets
An LR(0) item is `A→α·β`; it does not carry a lookahead terminal. Build the collection using closure and goto, exactly as in canonical LR parsing, but record only item cores. The states represent viable prefixes. The collection is canonical for the grammar, though later parsers may merge some states.

### Reduction lookaheads
For a completed item `A→γ·`, SLR uses `FOLLOW(A)` as the set of terminals on which the reduction is valid. A terminal is placed in the ACTION row for a lookahead `a` as `reduce A→γ` when `a∈FOLLOW(A)`. A shift action is filled from `goto(I,a)`. The `S'→S·` item contributes `accept` on `$`.

### Parsing algorithm
At each step, inspect the top state `i` and next input `a`.

- If `ACTION[i,a]=shift j`, push `a` and `j`.
- If it is `reduce A→β`, pop `|β|` states and symbols, push `A`, then follow `GOTO`.
- If it is `accept`, stop successfully.
- If it is `error`, invoke recovery.

The stack always has a sequence of grammar symbols below the state entries. The top state summarizes the items possible for that prefix.

### SLR conflict conditions
A shift-reduce conflict occurs if a state has a shift on `a` and a completed item whose FOLLOW set includes `a`. A reduce-reduce conflict occurs if two completed items in one state put reductions on the same lookahead. A conflict-free table means the grammar is SLR(1). Conflict presence does not mean the language is invalid; it means this parsing method cannot make the required decision from the available information.

### Why FOLLOW can be too broad
Two different completed items may be valid after the same prefix, but their legitimate lookaheads differ. SLR uses the FOLLOW set of each left-hand nonterminal independently, so it may mark a reduction on a terminal that is not actually valid in that particular state. This creates conflicts for some grammars that LR(1) can parse.

### SLR versus grammar power
SLR handles many practical grammars and is a useful first method in an exam. If a conflict appears, do not immediately add random precedence; check whether the grammar can be rewritten, whether LR(1) would distinguish the contexts, or whether the intended language needs a clearer nonterminal design.

## Worked examples
### Example 1: reduction item
If the state contains `E→T·`, reduce `E→T` on terminals in `FOLLOW(E)`. If `E` can be followed by `+` or `;`, the reduction is valid on both, not just on the first symbol of `T`.

### Example 2: shift-reduce
If the same state has `E→T·` and a shift on `+`, a conflict occurs because `+∈FOLLOW(E)`. The grammar may be ambiguous, or a precedence/associativity rule may be needed.

### Example 3: no conflict
Suppose the completed item is `T→F·` and the state has no shift on `FOLLOW(T)`. The SLR action table can reduce on every FOLLOW terminal without conflict.

### Example 4: a conflict-free SLR table fragment
Use the standard grammar

`S'→S`
`S→aAd | bAe | aBe | bAd`
`A→c`
`B→d`

with terminals `a,b,c,d,e,$`. In the LR(0) state reached from the start state on `a`, the items include `S→a·Ad`, `S→a·Be`, `A→·c`, and `B→·d`. Its useful ACTION entries are `shift 5` on `c` and `shift 6` on `d`. The state reached on `c` contains `A→c·`; since `FOLLOW(A)={d}`, its ACTION row has `reduce A→c` on `d`. The state reached on `d` similarly reduces `B→d` on `FOLLOW(B)={e}`. The completed `S` items reduce on `$`, and the state containing `S'→S·` has `accept` on `$`. Because the lookahead sets are separated, this grammar has no SLR conflict.

For input `acd`, the driver shifts `a`, shifts `c`, reduces `A→c` on lookahead `d`, shifts `d`, and then reduces `S→aAd` at `$`. The ACTION and GOTO tables, not just the item diagram, make this sequence deterministic.

## Key terms & formulas
- SLR(1): LR(0) items plus one lookahead chosen from FOLLOW.
- `FOLLOW(A)`: terminals that can follow `A`.
- `ACTION[i,a]=reduce A→γ` for `A→γ·` and `a∈FOLLOW(A)`.
- `ACTION[i,$]=accept` for `S'→S·`.
- SLR conflict: multiple actions in one state/lookahead cell.

## Common mistakes
- Use FIRST(A) for reductions; SLR uses FOLLOW(A).
- Put the completed dot on the wrong side.
- Forget the end marker `$` in the accept action.
- Assume every conflict proves the grammar is not context-free; it may only be outside SLR’s class.

## Exam prep
**Likely 2-mark questions**
1. Define SLR parsing. **Hint:** LR(0) collection and FOLLOW reductions.
2. State the SLR reduction rule. **Hint:** completed item plus FOLLOW.
3. What is a shift-reduce conflict? **Hint:** both actions in one cell.
4. What does `$` represent? **Hint:** end-of-input.

**Long-answer questions**
1. Construct the SLR ACTION and GOTO tables for a small grammar. **Hint:** item sets, shifts, FOLLOW reductions.
2. Trace an SLR parse of an expression. **Hint:** show state stack and actions.
3. Explain why SLR can fail where LR(1) succeeds. **Hint:** FOLLOW sets are too broad.
4. Diagnose and repair a conflict. **Hint:** precedence, associativity, or grammar rewrite.
