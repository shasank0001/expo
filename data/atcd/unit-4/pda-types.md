---
subject: atcd
unit: 4
topic: pda-types
syllabus_ref: CSM3203 Unit-IV
status: draft
---
# Types of Pushdown Automata
## Overview
PDAs can be classified by determinism and by how they signal acceptance. A nondeterministic PDA (NPDA) may choose among moves; a deterministic PDA (DPDA) has at most one legal move for each state, input symbol, and stack top. A PDA can accept by final state or by empty stack. These classifications describe different aspects of the same formal model, and the two acceptance notions are language-equivalent for nondeterministic PDAs.

## Explanation
### Deterministic PDA
A PDA is deterministic when, for every `q∈Q`, `a∈Σ∪{ε}`, and `X∈Γ∪{ε}`, the transition set has at most one pair `(r,γ)`. The condition must hold even for ε-input and ε-stack cases. Determinism is stronger than saying that each ordinary input symbol has one move; the machine cannot require an ε-move and an input move on the same triple in a way that creates alternatives.

### Nondeterministic PDA
An NPDA may have several target pairs for one configuration. It can guess a production, choose which stack symbol to process, or take an ε-transition before consuming input. A computation is successful if at least one sequence of choices accepts the complete string.

### Final-state acceptance
A PDA accepts by final state if, after consuming all input, its current state is in `F`. The stack may contain arbitrary symbols. This definition is convenient for mechanical machines that need a recognizable completed state.

### Empty-stack acceptance
A PDA accepts by empty stack if it consumes all input and the stack is empty. It may be in any state. This definition is natural for CFG simulation, because a production expansion ends when no pending symbols remain.

### Equivalence of acceptance notions
For nondeterministic PDAs, every language accepted by final-state acceptance is accepted by an empty-stack PDA and vice versa. To convert a final-state machine to empty-stack acceptance, add a new initial stack marker and use a fresh acceptance phase: after the original input is consumed, use ε-moves to pop the remaining stack, then enter a new final state. To convert in the other direction, add a new start/final arrangement that forces a final state only after the stack has become empty. The extra moves may be nondeterministic and can be carefully designed to avoid accepting prematurely.

### Language power
Both NPDA and DPDA variants recognize context-free languages in the standard theorem, but the deterministic class is smaller: some context-free languages have no equivalent DPDA. For example, a deterministic PDA cannot freely guess among several production expansions when the same lookahead can lead to different required continuations.

### Relationship to parsers
A grammar-driven PDA is usually nondeterministic. LL and LR parsing tables simulate selected deterministic choices using lookahead and conflict resolution. A DPDA-style parser is attractive because it avoids backtracking, but the grammar and language must satisfy the corresponding restrictions.

## Worked examples
### Example 1: final-state PDA for `a^n b^n`
The machine pushes `X` on `a`, pops on `b`, and enters `qf` only when the input is exhausted and the stack is at the bottom marker. It may leave `Z0` on the stack, so it uses final-state acceptance.

### Example 2: empty-stack PDA
Use a special stack bottom symbol `Z0`. When the top is `Z0` and input is exhausted, pop `Z0` with an ε-move. The machine accepts by empty stack; the state at that moment need not be in a final set.

### Example 3: nondeterministic choice
Suppose a stack has two identical-looking possible transitions with different state results. Both pairs belong in the transition set. The machine is NPDA even if only one branch will eventually accept.

### Example 4: deterministic restriction
A machine that must decide, with the same top `X` and lookahead `a`, whether to push or pop cannot be deterministic. Redesign the states or use a richer stack encoding to make the decision from the current state/top pair.

## Key terms & formulas
- DPDA: `|δ(q,a,X)|≤1` for every relevant triple.
- NPDA: transition relation may contain multiple pairs.
- Final-state acceptance: `f∈F` after complete input; stack arbitrary.
- Empty-stack acceptance: input exhausted and stack `ε`.
- NPDA acceptance notions are language-equivalent; DPDA language class is a proper subset of CFLs.

## Common mistakes
- Determinism concerns state, input, and stack top together.
- Final-state acceptance does not imply an empty stack.
- Empty-stack acceptance does not require a final state.
- Do not say every context-free language has a DPDA.

## Exam prep
**Likely 2-mark questions**
1. Define a deterministic PDA. **Hint:** at most one move per triple.
2. Distinguish final-state and empty-stack acceptance. **Hint:** state versus stack.
3. Are NPDA acceptance notions equivalent? **Hint:** yes, with conversions.
4. Which language class do PDAs recognize? **Hint:** context-free languages.

**Long-answer questions**
1. Compare DPDA and NPDA with an example of a required choice. **Hint:** push/pop on same configuration.
2. Prove the NPDA acceptance notions are equivalent. **Hint:** add ε-stack-clearing and fresh-state machinery.
3. Explain why the DPDA class is smaller. **Hint:** nondeterministic grammar simulation cannot always be made deterministic.
4. Relate PDA types to parser generators. **Hint:** grammar choices versus tables.
