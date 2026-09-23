---
subject: atcd
unit: 4
topic: cfg-to-pda
syllabus_ref: CSM3203 Unit-IV
status: draft
---
# CFG to PDA
## Overview
Every context-free grammar can be simulated by a pushdown automaton. The PDA stack holds the symbols that the grammar derivation still has to process. Terminals are matched with input, while nonterminals are replaced by a chosen production. This is a standard proof that PDAs recognize exactly the context-free languages and a conceptual model for parser stack behavior.

## Explanation
### PDA components for the construction
Start with a PDA whose input alphabet is the grammar terminal alphabet, whose stack alphabet contains the grammar terminals and nonterminals plus a new bottom marker `Z0`. Use an initial state `q0` and an ε-transition to push the start symbol `S` above `Z0`. When the input is exhausted and `Z0` is on top, add an ε-transition that pops `Z0`; the machine then accepts by empty stack. A real start symbol can be used instead of `Z0` directly, but the extra marker makes the completion condition clear.

### Replacing a nonterminal
For every production `A→α`, the machine has a transition that pops `A` and pushes the symbols of `α` in reverse stack order. If

`α=X1 X2 ... Xk`,

push `Xk` first and then ... then `X1`, so `X1` is on top and is processed first. If `α=ε`, pop `A` and push nothing.

For `A→BC`, the replacement is “pop `A`, push `C`, then push `B`.” This is a common source of marks lost in exams.

### Matching a terminal
If the top stack symbol is a terminal `a` and the next input symbol is also `a`, transition with an ε-input move, pop `a`, and push nothing. If the symbols differ, that computation branch fails. The PDA accepts only when all input has been consumed and the stack is empty.

### Nondeterminism
If `A` has several productions, the PDA has several possible stack-replacement moves. It nondeterministically guesses the correct production. This is why the generic construction is an NPDA, not normally a DPDA.

### Acceptance and correctness
Every accepting computation corresponds to a sequence of grammar production applications followed by terminal matches, so it yields a derivation. Conversely, any leftmost derivation can be simulated by choosing the corresponding production in the PDA. Therefore the PDA accepts exactly `L(G)`.

### Conversion to a parser
An LL parser maintains an expectation stack similar to this PDA, but chooses productions with a predictive table. An LR parser maintains a state stack and shifts/reduces. The CFG-to-PDA construction is still useful for understanding why a stack is enough for context-free parsing and why grammar choices can create conflicts.

## Worked examples
### Example 1: one production
For `S→aSb|ε`, initialize the stack with `S`. The PDA may replace `S` by `aSb`, yielding top-to-bottom stack `a S b` above `Z0`. It reads `a` and pops it, then may replace `S` by `ε`, then reads `b` and empties the stack. It accepts `ab`.

### Example 2: `S→AB`
Starting with `S`, pop `S` and push `B` then `A`. The top-to-bottom stack is `A B`. The machine processes `A` and `B` in the order required by the grammar, finally matching their terminals.

### Example 3: `A→aBc|ε`
When `A` is on top, choose the nonempty production and push in reverse order: `c`, then `B`, then `a`. The top is `a`, so the next input can be matched. If the other input is not a valid continuation, the machine tries the ε production or fails.

### Example 4: derivation trace
For `S→AB`, `A→a`, `B→b`, a derivation can be simulated by stack forms:

`S → AB → aB → ab`.

At the first replacement, `A` is placed above `B`; terminal matching removes each symbol after it is exposed.

## Key terms & formulas
- Push order for `A→X1...Xk`: `Xk,...,X1`.
- Initial transition: `δ(q0,ε,Z0)={(q,SZ0)}` (or equivalent).
- Terminal match: read `a`, pop `a`, push nothing.
- Accept when input `ε` and stack `ε`.
- `L(PDA)=L(G)`.

## Common mistakes
- Push the production’s symbols left-to-right and process them backwards.
- Treat terminal replacement as an ordinary input move; matching is a pop with no push.
- Consume input when taking an ε production.
- Assume a deterministic choice exists when several productions share a prefix.

## Exam prep
**Likely 2-mark questions**
1. Explain the CFG-to-PDA construction. **Hint:** stack stores pending symbols.
2. What happens for `A→BC`? **Hint:** push `C` then `B`.
3. How are terminals matched? **Hint:** compare stack top with next input and pop.
4. What is the acceptance condition? **Hint:** input and stack empty.

**Long-answer questions**
1. Construct a PDA from a supplied CFG. **Hint:** show all production transitions and stack order.
2. Trace the PDA on a terminal string using a derivation. **Hint:** show both derivation and stack.
3. Prove the construction recognizes `L(G)`. **Hint:** simulation in both directions.
4. Compare the PDA stack with an LL parser expectation stack. **Hint:** same pending-symbol idea, different selection mechanism.
