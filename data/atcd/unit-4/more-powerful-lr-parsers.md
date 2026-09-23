---
subject: atcd
unit: 4
topic: more-powerful-lr-parsers
syllabus_ref: CSM3203 Unit-IV
status: draft
---
# More Powerful LR Parsers
## Overview
Canonical LR(1) and LALR parsing use more precise lookahead than SLR. LR(1) records the exact terminal that can follow each item in a particular state; LALR merges compatible LR(1) states to obtain smaller tables. Both parse more grammars than SLR and retain the deterministic bottom-up advantages of LR parsing, but their table construction and conflict behavior are more involved.

## Explanation
### Canonical LR(1)
An LR(1) item is

`[A→α·β, a]`.

The production and dot describe recognition progress; `a` is the exact lookahead terminal for that occurrence of the item. The initial item is `[S'→·S, $]`. Closure adds items for the symbol after the dot, with lookaheads from `FIRST` of the remaining suffix, including `$` where appropriate. Goto advances the dot and retains the relevant lookahead set.

The canonical collection may have many states. Its ACTION table uses a reduction `A→β` only on the lookaheads attached to a completed item, which is more precise than SLR’s global FOLLOW set. A canonical LR(1) table is conflict-free for every LR(1) grammar.

### LALR parsing
LALR begins with the canonical LR(1) collection and merges states having the same LR(0) item core. The lookaheads of states with a common core are combined. The resulting states are compatible, so the ACTION and GOTO tables have the same parsing behavior for the usual LALR construction while using fewer states than canonical LR(1). Yacc/Bison traditionally generate LALR(1) parsers.

### SLR, LR(1), and LALR comparison
SLR uses LR(0) cores and FOLLOW sets; it is the smallest and simplest of the three. Canonical LR(1) is the most precise and can accept the largest grammar set, but its table may be large. LALR lies between them: its states are obtained by merging compatible canonical LR(1) states, so it usually has fewer states while retaining the same parsing behavior when the merge is conflict-free. It can introduce a reduce-reduce conflict when incompatible lookaheads are merged. In the usual hierarchy, a conflict-free LALR table is a practical LR(1)-style compromise; it is not correct to say that LALR simply “adds entries” to SLR.

### Why merging can introduce conflicts
Two LR(1) states may have the same production cores but different lookaheads. Each state alone is conflict-free. Merging their lookaheads can place two different reductions in one state/lookahead cell, creating an LALR conflict. Thus a table can be smaller but detect a conflict that canonical LR(1) does not have.

### Practical parser generation
A parser-generator specification includes terminals, nonterminals, productions, precedence/associativity declarations, start symbol, and user actions. The generator constructs the item collection, tables, and a driver. The driver maintains a state stack, shifts input, reduces productions, and invokes semantic actions after the appropriate reduction.

### Comparison with LL parsing
LR parsing is bottom-up and can handle left recursion naturally. LL parsing is top-down, often easier to read, but usually needs a more restricted grammar. LALR is widely used because its table size and grammar coverage are a practical compromise.

## Worked examples
### Example 1: LR(1) item
`[E→E+T·, $]` is a completed item with end lookahead; `[E→E·+T, +]` expects to shift `+`. The lookahead is part of the item, not a label on the whole state.

### Example 2: closure lookahead
If `[A→x·B, a]` is present, closure adds `[B→·γ, b]` for every `b∈FIRST(β)` where `B→β`; if `β` is nullable, include `a` as well. This is the mechanism that makes reductions more precise than SLR.

### Example 3: LALR merge
States I and J have cores `{S→·A, A→·a}`. If their lookahead sets differ, LALR merges them and unions the sets. If the union places two different reductions on the same terminal, the merged state has a reduce-reduce conflict.

### Example 4: table size intuition
A grammar with many LR(1) distinctions can produce two states for the same core but different future lookaheads. LALR keeps one combined state, reducing table entries. SLR would use the whole FOLLOW set in a single core state and may create a shift-reduce conflict earlier.

## Key terms & formulas
- LR(1) item: `[A→α·β, a]`.
- Initial item: `[S'→·S, $]`.
- LALR merge: same LR(0) core, union lookaheads.
- Canonical LR(1): precise, potentially large.
- LALR(1): compact, commonly generated, possible merge conflicts.
- SLR: LR(0) + FOLLOW reductions.

## Common mistakes
- LR(1) lookahead is part of each item, not a global state property.
- LALR is not simply SLR with extra table entries.
- Merging states can introduce conflicts.
- Do not claim LALR is always strictly weaker than canonical LR(1) in language power without specifying table construction and conflicts.

## Exam prep
**Likely 2-mark questions**
1. Compare SLR, canonical LR(1), and LALR by precision and table size. **Hint:** FOLLOW versus exact lookaheads versus merge.
2. Define an LR(1) item. **Hint:** production, dot, lookahead.
3. What does LALR merge? **Hint:** same LR(0) cores.
4. Why are LALR parsers common? **Hint:** smaller tables and broad grammar coverage.

**Long-answer questions**
1. Construct an LR(1) closure and goto for a small grammar. **Hint:** propagate lookaheads with FIRST.
2. Explain how LALR is obtained from canonical LR(1). **Hint:** core equivalence and lookahead union.
3. Discuss how merging can create a conflict. **Hint:** incompatible reductions share a cell.
4. Compare LR and LL parsing for compiler design. **Hint:** direction, left recursion, table size.

**Long-answer model outline**
A good answer should show an LR(1) item, calculate a lookahead, state the canonical collection, merge equal cores for LALR, and conclude with a table-size/precision comparison.
