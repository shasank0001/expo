---
subject: atcd
unit: 3
topic: cfg-minimization
syllabus_ref: CSM3203 Unit-III
status: draft
---
# CFG Minimization
## Overview
A context-free grammar may contain nonterminals and productions that do not contribute to the language generated from its start symbol. CFG minimization removes such useless material while preserving `L(G)`. The usual steps identify unreachable and non-generating (useless) nonterminals, remove their productions, and handle unit productions carefully. A simplified grammar is easier to read, parse, and optimize, but it must generate exactly the same strings.

## Explanation
### Unreachable nonterminals
A nonterminal is **unreachable** if no derivation from the start symbol `S` can contain it. Build a reachability graph whose vertices are nonterminals and whose edges follow right-hand sides of productions, then search from `S`. Any vertex not reached is unreachable. Its productions can be deleted because they can never participate in a derivation of a generated sentence.

### Useless or non-generating nonterminals
A nonterminal is **generating** if it can derive at least one terminal string, possibly `ε`. A nonterminal is **non-generating** if every derivation from it leaves at least one nonterminal forever. Compute the generating set by starting with nonterminals that have a production containing only terminals or ε, then repeatedly adding any nonterminal whose production has an already-generating right side.

Any nonterminal reachable from `S` but non-generating is useless. If a derivation from `S` enters such a nonterminal, it cannot reach a complete terminal string, so its productions can be removed. The order matters: remove useless symbols first or recompute reachability afterward.

### Removing useless productions
A production is useless if it belongs to an unreachable or non-generating part. Delete it along with dependent productions. The remaining grammar may still contain nonterminals that generate only very long strings; those are not automatically removable because they may be needed for the language.

### Unit productions
A unit production has a nonterminal on the right: `A→B`. Unit productions can sometimes be removed by replacing `A` with the non-unit productions derived from `B`, but the process must account for cycles such as `A→B`, `B→A`. A standard algorithm first removes unit cycles and then computes unit closures. Removing every unit production without preserving the language can remove required derivations or create ambiguity.

### Nullable and terminal-only rules
A production `A→ε` is not useless when `ε` is part of the intended language; for example, it makes a grammar generate the empty string or optional clauses. A terminal-only rule is a base case that usually makes its left side generating. Minimization is not simply “remove empty productions.”

### Equivalence and parsing
The simplified grammar should have the same start symbol and language. It may have fewer nodes, but it can accidentally become more ambiguous if rules are merged carelessly. After minimization, recompute FIRST/FOLLOW or parser tables because nonterminal names and productions have changed.

## Worked examples
### Example 1: unreachable nonterminal
Given

`S→AB`
`A→a`
`B→b`
`C→c`,

no production reachable from `S` uses `C`. Delete `C→c`; the language remains `{ab}`.

### Example 2: non-generating nonterminal
Given

`S→AC`
`A→a`
`C→CD`
`D→C`,

`A` generates `a`, but `C` and `D` can only keep producing each other and never reach terminals. `C` is useless, and the branch `S→AC` cannot produce a sentence. Removing that branch leaves the empty language, because there is no other production for `S`; if `S→a` were also present, the remaining language would instead be `{a}`.

### Example 3: unit production
For `S→A`, `A→B`, `B→b`, the unit chain can be collapsed safely to `S→b` (with any other alternatives preserved), because the only terminal derivation is `b`. If `A→B` and `B→A` form a cycle, collapse the cycle first rather than substituting indefinitely.

### Example 4: preserve ε
Grammar `S→A B`, `A→a|ε`, `B→b|ε` generates `ε, a, b, ab`. Removing either ε rule would change the language, so it is not minimization.

## Key terms & formulas
- Reachable from `S`: appears in some sentential form derived from `S`.
- Generating: `A⇒*w` for some `w∈V_T*`.
- Useful nonterminal: reachable and generating.
- Unit production: `A→B` with `B` a nonterminal.
- Simplification condition: `L(G_new)=L(G_old)`.

## Common mistakes
- “Unreachable” and “non-generating” are different conditions.
- Remove useless nonterminals, not every nonterminal that appears only in ε rules.
- Unit production elimination requires cycle handling.
- A smaller grammar can be more ambiguous; verify the intended parse structure.

## Exam prep
**Likely 2-mark questions**
1. Define unreachable and useless nonterminals. **Hint:** no path from start versus cannot derive terminals.
2. Name two CFG simplification operations. **Hint:** delete useless symbols and unit productions.
3. Why must ε-productions not always be removed? **Hint:** empty string may be in the language.
4. State the preservation condition. **Hint:** same start language.

**Long-answer questions**
1. Simplify a supplied CFG. **Hint:** reachability, generating set, then unit rules.
2. Explain how to detect a non-generating cycle. **Hint:** no terminal base case.
3. Discuss when unit-production elimination is safe. **Hint:** substitute closures and handle cycles.
4. Compare CFG minimization with DFA minimization. **Hint:** symbol reachability/generation versus state equivalence.
