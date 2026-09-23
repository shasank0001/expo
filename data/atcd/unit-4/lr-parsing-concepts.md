---
subject: atcd
unit: 4
topic: lr-parsing-concepts
syllabus_ref: CSM3203 Unit-IV
status: draft
---
# LR Parsing Concepts
## Overview
LR parsing is a deterministic, bottom-up, table-driven method for context-free grammars. It reads input left to right and reduces a stack prefix in a way that corresponds to reversing a rightmost derivation. The parser state summarizes the grammar items that are possible after the stack prefix. The method’s power comes from combining a finite control state, a stack, and lookahead to make precise shift/reduce decisions.

## Explanation
### Meaning of LR
The first `L` means input is processed from left to right. The second `L` means the parser constructs the left-to-right version of a derivation, or more precisely reduces the right-hand side of a production in the order of a rightmost derivation. `R` means reductions proceed in reverse rightmost-derivation order. The numeral specifies the lookahead bound: LR(0), SLR(1), LR(1), and so on.

### LR items
An LR item is a production with a dot:

`A→α·β`.

The portion before the dot has been recognized and the portion after it remains to be recognized. The item is a prediction of what the parser may see next. A completed item `A→α·` is a reduction item. A start item `S'→·S` initializes the canonical collection.

### Closure
Given an item `B→γ·δ` in a set, add every item `A→·α` for each production `A→α` of `B`. This predicts what can follow before `B` is completed. The closure operation is repeated until no new item is added. A completed start item `S'→S·` marks the accepting item.

### Goto
For an item set `I` and terminal `a`, `goto(I,a)` is the set of items obtained by advancing the dot over `a` in every applicable item. For a nonterminal `A`, `goto(I,A)` does the same over `A`. Goto sets form the canonical collection of LR states and define parser-state transitions.

### Viable prefixes
The states in the canonical collection correspond to viable prefixes: prefixes that can appear on a stack during a rightmost derivation. A viable prefix has not crossed a point where a production would need to be reduced in a way incompatible with the grammar. The item construction captures exactly this boundary information.

### Parsing actions
The parser maintains a stack of states and input. For state `i` and lookahead `a`, the action table says `shift j`, `reduce A→β`, `accept`, or `error`. A shift pushes the next input and the state reached by the symbol. A reduce pops the states and symbols represented by the production, pushes the left-hand nonterminal, and follows the corresponding goto. The goto table handles nonterminal transitions.

### Shift-reduce and reduce-reduce conflicts
A conflict occurs when one action cell has more than one possible action. A shift-reduce conflict usually reflects missing precedence/associativity or an ambiguous grammar. A reduce-reduce conflict means two reductions are possible. LR’s strength is not that conflicts are impossible; it is that the table exposes them precisely so the grammar can be corrected.

### Canonical versus practical parsers
Canonical LR construction can produce many states. SLR uses LR(0) items and FOLLOW sets; canonical LR(1) attaches exact lookaheads; LALR merges compatible LR(1) cores. The latter two are covered in the remaining Unit IV notes.

## Worked examples
### Example 1: item notation
For `A→BC`, the items are `A→·BC`, `A→B·C`, and `A→BC·`. The dot shows progress; the last item is a possible reduction.

### Example 2: closure
If the set contains `A→B·C` and the grammar has `B→·DE`, closure adds `B→·DE`. It does not add `C`’s productions yet, because `C` has not been reached by the dot.

### Example 3: goto
From `{A→·aB, B→·b}`, `goto(I,a)={A→a·B}`. The parser has consumed `a` and now expects `B`.

### Example 4: action trace
If state `i` shifts `+` to state `j` and later has a completed item `E→E·+T`, an action cell for `+` can conflict. The grammar’s precedence or associativity decides whether to shift or reduce.

## Key terms & formulas
- Item: `A→α·β`.
- Closure: add predicted productions for the nonterminal after the dot.
- Goto: advance dot over a terminal/nonterminal.
- `S'→·S`: augmented start item.
- `ACTION[i,a]` and `GOTO[i,A]` drive the parser.
- LR conflict: multiple actions in one `ACTION` cell.

## Common mistakes
- The dot does not mean the symbol has been consumed; it marks recognition progress.
- Closure predicts after the dot, not before the production.
- A reduce item is `A→α·`, not `A→·α`.
- LR is bottom-up even though its reductions reverse a rightmost derivation.

## Exam prep
**Likely 2-mark questions**
1. What do L and R mean in LR parsing? **Hint:** input order and reverse derivation.
2. Define an LR item and the dot. **Hint:** production plus progress marker.
3. State closure and goto. **Hint:** predict and advance.
4. What are shift, reduce, accept, and error actions? **Hint:** table operations.

**Long-answer questions**
1. Build an LR(0) item set from a small grammar. **Hint:** start item, closure, goto.
2. Explain viable prefixes and their relation to states. **Hint:** stack-compatible prefixes.
3. Trace an LR parse using ACTION and GOTO tables. **Hint:** show stack and input.
4. Explain how a conflict is detected. **Hint:** one state/lookahead cell with two actions.
