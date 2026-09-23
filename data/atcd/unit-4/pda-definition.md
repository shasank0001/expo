---
subject: atcd
unit: 4
topic: pda-definition
syllabus_ref: CSM3203 Unit-IV
status: draft
---
# Pushdown Automata Definition
## Overview
A pushdown automaton (PDA) is a finite automaton with a stack. The stack gives it unbounded auxiliary memory, so it can remember a growing amount of information while reading left to right. PDAs recognize exactly the context-free languages. They are the conceptual machine behind CFG parsing, although a practical parser may use tables rather than an explicit stack machine.

## Explanation
### Formal definition
A PDA is a 7-tuple

`M=(Q,Σ,Γ,δ,q0,Z0,F)`

where:

- `Q` is the finite set of control states;
- `Σ` is the input alphabet;
- `Γ` is the stack alphabet;
- `δ: Q × (Σ∪{ε}) × (Γ∪{ε}) → 2^(Q×Γ*)` is the transition function;
- `q0∈Q` is the start state;
- `Z0∈Γ` is the initial stack symbol; and
- `F⊆Q` is the set of final states.

A transition `δ(q,a,X)={ (r,γ) }` means that in state `q`, with `a` as the next input symbol and `X` at the top of the stack, the machine may move to state `r`, replace `X` by the string `γ`, and consume `a` if `a≠ε`. The top of `γ` is the new top. If `a=ε`, no input is consumed. If `X=ε`, the top of the stack is not tested; this convention must be stated consistently.

### Stack operation
A pushdown stack is last-in, first-out. A transition can pop `X`, push a string `γ`, or both. It can also be nondeterministic, with several target pairs for one configuration. The stack is unbounded in the theoretical model, so it can store a long prefix of the input.

### Acceptance by final state
In **final-state acceptance**, the machine accepts if, after consuming all input, it is in a state in `F`, regardless of the remaining stack. The stack need not be empty.

### Acceptance by empty stack
In **empty-stack acceptance**, the machine accepts if it consumes all input and empties the stack. It need not enter a designated final state. To model this with final-state notation, one can add a new final state and an ε-transition from every accepting configuration to it.

### Why a stack is needed
A finite automaton has only a fixed number of control states and cannot remember an unbounded count. A PDA can push one marker for each opening symbol and pop it for each closing symbol. This is why `a^n b^n`, balanced parentheses, and many expression/statement structures are context-free.

### PDA versus grammar
A CFG generates strings by replacing nonterminals; a PDA recognizes strings by using its stack to remember pending grammar symbols. The CFG-to-PDA construction simulates a leftmost derivation, and the PDA-to-CFG construction creates a grammar from the PDA’s state/stack behavior.

### Determinism and nondeterminism
An NPDA may have several moves for the same input, stack top, and state. A DPDA has at most one move for each such triple. Some context-free languages have no equivalent DPDA, although their NPDA descriptions are often simple.

## Worked examples
### Example 1: `a^n b^n`
Use stack symbol `X`. On `a`, push `X`; on `b`, pop one `X`; in the final state, accept only if input is exhausted and the stack contains no `X`. The machine prevents a `b` before an `a` and prevents missing or extra `b`s.

### Example 2: balanced parentheses
On `(`, push a left-parenthesis marker. On `)`, pop one. At the end, accept by empty stack if every close matched. A transition that tries to pop from an empty stack fails.

### Example 3: transition notation
`δ(q,a,X)={(r,YX)}` means read `a`, pop `X`, push `Y` then `X` so `X` remains on top. The order in `γ` is top-to-bottom; a common mistake is reversing it.

### Example 4: two acceptance styles
A machine may reach final state `qf` while holding `X` and use final-state acceptance. Another machine may pop all `X` and use empty-stack acceptance. They can be transformed into one another with extra ε-moves.

## Key terms & formulas
- `M=(Q,Σ,Γ,δ,q0,Z0,F)`.
- `δ(q,a,X)⊆Q×Γ*`.
- Stack top: leftmost symbol of `γ` in a transition.
- `Σε=Σ∪{ε}`; `Γε=Γ∪{ε}`.
- Final-state acceptance versus empty-stack acceptance.
- PDA language class: context-free languages.

## Common mistakes
- The stack is not an ordinary queue; operations are LIFO.
- `ε` in the input field does not consume a character.
- `ε` in the stack field is not the same as a literal empty-stack marker.
- Final-state acceptance does not require an empty stack.
- The PDA is not equivalent to every grammar implementation without nondeterministic choice.

## Exam prep
**Likely 2-mark questions**
1. Define a PDA and list its components. **Hint:** 7-tuple and stack.
2. Explain a PDA transition. **Hint:** read, pop, push, move.
3. Why is a stack useful? **Hint:** unbounded memory for matching.
4. Distinguish final-state and empty-stack acceptance. **Hint:** state versus stack.

**Long-answer questions**
1. Draw a PDA for `a^n b^n`. **Hint:** push on `a`, pop on `b`, final check.
2. Draw a PDA for balanced parentheses. **Hint:** one marker per open delimiter.
3. Prove the two PDA acceptance notions are equivalent. **Hint:** add ε-transitions.
4. Explain why PDAs correspond to context-free languages. **Hint:** stack simulates derivation.
