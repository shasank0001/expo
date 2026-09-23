---
subject: atcd
unit: 4
topic: pda-to-cfg
syllabus_ref: CSM3203 Unit-IV
status: draft
---
# PDA to CFG
## Overview
A PDA that recognizes a context-free language can be converted algorithmically into a CFG. The grammar variables represent states and state/stack pairs, and productions summarize PDA transitions from one control point to an accepting configuration. The construction can be large, but it is systematic and does not require guessing a language-specific grammar.

## Explanation
### Variables
Let the PDA be `M=(Q,Σ,Γ,δ,q0,Z0,F)`. Create variables for each control state `A_q∈V_N` and for each pair consisting of a state and a stack symbol, written `A_{q,Z}`. `A_{q,Z}` is intended to generate the input that can take the PDA from state `q`, with `Z` as the current top stack marker, to an accepting situation according to the PDA’s control and stack behavior. Add a new start variable `S`.

### Start productions
Add

`S → A_{q0,Z0}`

and `S→ε` if the empty input is accepted by the chosen construction. In a common formal presentation, `A_{q0,Z0}` represents paths from the start state, and the new `S` avoids confusion with a state variable. Some textbooks use `S→A_{q0,Z0}` only; follow the convention used in the course when listing the construction.

### Transition productions
For a transition

`δ(q,a,Z) = {(r,γ)}`

where `a` may be `ε` and `γ=Z1Z2...Zk`, add

`A_{q,Z} → a A_{r,Zk} A_{r,Z(k−1)} ... A_{r,Z1}`.

The stack symbols are reversed because the first symbol `Z1` is the new top and will be processed first. If `k=0`, add `A_{q,Z}→a`. If the transition reads a terminal, `a` is that terminal; if it is an ε-transition, `a` is omitted.

### Acceptance productions
For each final state `p∈F` and each stack symbol `Z`, add `A_{p,Z}→ε`. These productions say that reaching a final state with no further input is an accepting completion for that state/stack configuration. If the PDA uses empty-stack acceptance, the construction is adjusted to introduce an accepting state and force the original stack to be emptied; the final-state version is simpler to present.

### State-variable convention
Some texts write productions such as `A_q→a A_r A_s` by treating a transition as a path from one state to another, and then add productions for stack changes. The safest exam answer names the variables explicitly and follows the selected textbook’s notation. The essential points are: one variable per state/stack configuration, one production per transition, reverse stack order, and ε for an empty pushed string.

### Correctness
A path through the PDA can be decomposed into transitions. Each transition contributes its consumed input symbol and a sequence of variables for the newly pushed stack symbols. Induction on path length shows that a variable derives exactly the labels of a valid accepting path. Thus the generated language is the PDA language.

### Complexity and use
The number of variables is `|Q| + |Q||Γ| + 1`, and the number of productions depends on the number and lengths of transitions. The resulting grammar is rarely minimal, but it can be simplified afterward.

## Worked examples
### Example 1: push transition
Suppose `δ(q,a,Z)={(r,AX)}`. The new stack top is `A`, followed by `X`. The production is

`A_{q,Z} → a A_{r,A} A_{r,X}`.

It is not simply `A_q→aAr`, because the old stack symbol `Z` is replaced and the pushed symbols need their own state/stack variables.

### Example 2: no push
If `δ(q,a,Z)={(r,ε)}`, add `A_{q,Z}→a`. The machine reads `a`, pops `Z`, and changes to `r` without leaving a new marker.

### Example 3: ε transition
If `δ(q,ε,Z)={(r,Z)}`, add `A_{q,Z}→A_{r,Z}`. This production consumes no input but changes the state while preserving the top marker.

### Example 4: final state
If `p∈F` and `Z∈Γ`, add `A_{p,Z}→ε`. A path that reaches `p` can finish without consuming more input, subject to the acceptance convention.

## Key terms & formulas
- Variables: `A_q` and `A_{q,Z}` plus new start `S`.
- Transition: `δ(q,a,Z)={(r,γ)}`.
- For `γ=Z1...Zk`: `A_{q,Z}→a A_{r,Zk}...A_{r,Z1}`.
- Empty push: `A_{q,Z}→a`.
- Final state: `A_{p,Z}→ε`.
- Complexity: roughly quadratic variable count in state and stack sizes.

## Common mistakes
- Do not forget to include a variable for every stack symbol.
- The pushed stack string is reversed in the production.
- An ε transition contributes no terminal `a`.
- A final-state variable’s ε production does not mean every PDA transition is automatically accepting.
- Follow the textbook’s acceptance convention; final-state and empty-stack versions differ.

## Exam prep
**Likely 2-mark questions**
1. Outline PDA-to-CFG conversion. **Hint:** variables, transitions, finals.
2. What production is made for `δ(q,a,Z)={(r,γ)}`? **Hint:** reverse `γ` and use state/stack variables.
3. Why introduce state/stack variables? **Hint:** summarize paths from a configuration.
4. What is added for a final state? **Hint:** ε production.

**Long-answer questions**
1. Convert a small PDA to a CFG. **Hint:** list every variable and production.
2. Explain why stack symbols are reversed. **Hint:** top-of-stack processing order.
3. Handle an ε transition and an empty push. **Hint:** omit input or produce `ε`.
4. Compare PDA-to-CFG with CFG-to-PDA. **Hint:** path summary versus derivation simulation.
