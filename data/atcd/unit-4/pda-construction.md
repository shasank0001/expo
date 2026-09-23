---
subject: atcd
unit: 4
topic: pda-construction
syllabus_ref: CSM3203 Unit-IV
status: draft
---
# PDA Construction
## Overview
Constructing a PDA begins with identifying the information the machine must remember. Each piece of unfinished input structure is represented by a stack symbol. A transition then says how to consume a terminal, update the stack, and change control state. A correct construction also specifies what happens on invalid orderings, extra symbols, and the final stack condition.

## Explanation
### Design from the language
Ask: “What fact about the prefix read so far is needed to decide what may come next?” For `a^n b^n`, remember how many `a`s have been seen. For balanced parentheses, remember the unmatched opening delimiters. For a grammar, the stack can store the right-hand side still to be generated. Never push a raw character without deciding what it represents and when it is removed.

### Transition design
A transition is usually written

`δ(q,a,X)=(r,γ)`.

Read `a`, require top `X`, pop `X`, push `γ`, and move to `r`. The string `γ` is written with its top at the left. If the machine can make several choices, put several pairs in braces. An ε-input transition has the form `δ(q,ε,X)={(r,γ)}`.

### Constructing for `a^n b^n`
1. Start in `q0` with stack `Z0`.
2. In `q0`, on `a`, replace `Z0` with `Z0X`; this records one unmatched `a`.
3. On `b`, replace `X` with `ε`; this matches one `a`.
4. On `b` when the top is `Z0`, reject (no unmatched `a`).
5. On `a` after the phase has changed to `b`, reject.
6. On ε with top `Z0`, move to `qf`; accept by final state.

The details can be arranged differently, but the invariant is: in the first phase the stack stores the number of `a`s; in the second phase each `b` removes one.

### Constructing for balanced parentheses
Use stack markers `(` and `{` if more than one delimiter type is allowed. On an opening delimiter, push its type. On a closing delimiter, require the matching top marker and pop it. Accept by empty stack after all input. A closing delimiter with an empty stack has no valid transition.

### Constructing from a CFG
A CFG-to-PDA machine starts with a special symbol `S'`, pushes the start symbol `S`, and repeatedly:

- pop a nonterminal `A` and choose a production `A→α`;
- push the symbols of `α` in reverse order;
- if the top is a terminal, match it with one input symbol and pop it.

Accept when both input and stack are empty. This is a general construction for any context-free language, while a language-specific PDA can be much smaller.

### Nondeterministic branches
If a grammar has alternatives or a PDA must guess whether an operation is push or pop, add separate transitions. An NPDA accepts if one branch succeeds. In a diagram, label branches clearly and never draw two targets for a deterministic transition.

### Verification
Test the empty string, shortest valid string, one invalid ordering, extra input, and a long valid string. Keep an invariant sentence such as “the stack contains exactly one `X` for each unmatched `a`.” If the invariant cannot be stated, the construction may be incomplete.

## Worked examples
### Example 1: `a^n b^n` configuration trace
For `aabb`, a compact configuration trace is:

`q0(aabb,Z0) ⇒ q0(aabb,Z0XX) ⇒ q0(bb,Z0X) ⇒ q0(b,Z0) ⇒ qf(ε,Z0)`.

The machine may use a final-state transition that leaves `Z0`; acceptance is by final state. For empty-stack acceptance, pop `Z0` before `qf`.

### Example 2: palindromes
For a language such as `{w#w^R}`, push symbols while reading the first part. At `#`, switch to a reverse-comparison state; for each input symbol, pop one stack symbol and require equality. The invariant ensures the second half is the reverse of the first.

### Example 3: grammar simulation
For `S→aSb|ab`, initialize stack with `S`. Replace `S` by `aSb` (push in reverse order so `a` is processed), then replace `S` by `ab`; pop `a` against input `a`, replace/pop `S` as `ab`, and finally pop `b` against input `b`. The input is accepted when the stack is empty.

### Example 4: invalid extra `b`
For `a^n b^n`, after all `a`s are read, a `b` transition exists only when `X` is on top. An extra `b` encounters `Z0`, so the branch fails; accepting on an empty stack without this check would be wrong.

## Key terms & formulas
- `δ(q,a,X)=(r,γ)`: read, pop, push, move.
- Stack invariant: a concise statement of what the current stack represents.
- `Z0`: bottom marker; its removal signals completion in many designs.
- Reverse push: for `A→BC`, push `C` then `B` so `B` is processed first.
- NPDA acceptance: at least one successful computation.

## Common mistakes
- Push symbols in the wrong order for a grammar simulation.
- Allow a closing symbol to pop the bottom marker.
- Forget to reject extra opening or closing symbols.
- Mix up stack top convention when writing `γ`.
- Do not draw a final state as the only acceptance condition if the specification uses empty stack.

## Exam prep
**Likely 2-mark questions**
1. Explain a PDA transition. **Hint:** read/pop/push/move.
2. Describe the stack invariant for `a^n b^n`. **Hint:** one marker per unmatched `a`.
3. What is the role of `Z0`? **Hint:** bottom marker and completion check.
4. Why can a PDA be nondeterministic? **Hint:** grammar alternatives or guessed choices.

**Long-answer questions**
1. Construct and trace a PDA for `a^n b^n`. **Hint:** phases and stack symbols.
2. Construct a PDA for balanced parentheses. **Hint:** push/pop matching.
3. Construct a PDA for `{w#w^R}`. **Hint:** store and reverse-compare.
4. Explain the generic CFG-to-PDA construction. **Hint:** inverse push order and terminal matching.
