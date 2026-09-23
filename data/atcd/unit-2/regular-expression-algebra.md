---
subject: atcd
unit: 2
topic: regular-expression-algebra
syllabus_ref: CSM3203 Unit-II
status: draft
---
# Regular Expression Algebra
## Overview
Regular-expression algebra gives identities that transform equivalent descriptions without changing the language. These rules are useful for simplifying specifications, checking answers, and solving state equations. Unlike ordinary arithmetic, concatenation and star have some special laws, and notation varies between textbooks and tools, so every proof should be based on the languages denoted by the expressions.

## Explanation
### Notation
Use `+` or `|` for union, adjacency or a dot for concatenation, `*` for Kleene star, `∅` for the empty language, and `ε` for the empty string. If `+` is used for union in a formal course, do not confuse it with the programming-tool `+` quantifier meaning one-or-more.

### Elementary identities
For any regex `R`:

- `R + R = R` (idempotence);
- `R + ∅ = R` and `R ∅ = ∅`;
- `R ε = ε R = R`;
- `R* = (R*)*`;
- `∅* = ε`;
- `(R+ε)* = R*`.

These hold because they preserve exactly the set of strings.

### Associative and commutative laws
Union is associative and commutative:

`R+S = S+R`, `(R+S)+T = R+(S+T)`.

Concatenation is associative:

`R(ST) = (RS)T`,

but is not commutative in general. For example, `ab` denotes only `{ab}`, while `ba` denotes `{ba}`.

### Distributive laws
Concatenation distributes over union:

`R(S+T)=RS+RT`,
`(R+S)T=RT+ST`.

These identities are central when expanding an expression or deriving a regular-language equation. There is no corresponding general commutativity law for concatenation.

### Star identities
The zero-repetition case gives `R* = ε + RR* = ε + R*R`. Therefore, a loop can be represented either as “nothing” followed by repetitions or as a repetition followed by nothing. Some useful simplifications are:

- `R** = R*`;
- `(R+S)* = (R* S*)*`, an equivalent grouping of a sequence of `R` or `S` blocks;
- `(R*)* = R*`;
- `(R+ε)* = R*` because `R*` already includes `ε`.

Be cautious with identities such as `(RS)* = R*S*`; it is not true in general because the final partial `R` can occur without a following `S`.

### Algebra versus semantic minimization
An algebra rule removes syntax while preserving language. A minimized regular expression may still have several equivalent forms, and the shortest textual expression is not always the simplest automaton. To prove a transformation, show both inclusions: every old string is in the new language and every new string was already in the old language.

### Boolean and derivative tools
Finite-alphabet regexes can be converted to equivalent finite expressions using Boolean operations and derivatives. If `D_a(R)` is the derivative with respect to symbol `a`, then

`D_a(RS)=D_a(R)S`,
`D_a(R*)=D_a(R)R*`.

A state in an automaton corresponds to a residual/derivative language. This is a useful advanced link to DFA construction.

## Worked examples
### Example 1: simplify a union
`R + ∅ + R + S = R+S` by idempotence and identity.

### Example 2: distribute
`a(b|c) = ab|ac` because a string is either `ab` or `ac`.

### Example 3: empty star
`∅* = ε`, because the only possible repetition count is zero and the empty concatenation is `ε`.

### Example 4: prove noncommutativity
Take `a` and `b`. `ab={ab}`, while `ba={ba}`. Since these sets differ, concatenation cannot be commutative.

### Example 5: derivative
For `R=(a|b)*a`, `D_a(R)=ε`, while `D_b(R)=R`. The derivative for `a` says that after reading `a`, the residual language accepts the empty suffix.

## Key terms & formulas
- `R+S = R∪S`; `RS` is concatenation.
- `R* = ε+RR*`.
- `R+ε` has the same language as `R` followed by empty string.
- `D_a(RS)=D_a(R)S`; `D_a(R*)=D_a(R)R*`.
- Equivalence is language equality: `L(R)=L(S)`.

## Common mistakes
- Do not apply commutativity to concatenation.
- `R+` is ambiguous across notations; define whether it means union or one-or-more.
- `(RS)*` is not generally `R*S*`.
- A star applies to the preceding grouped expression, not an arbitrary later symbol.

## Exam prep
**Likely 2-mark questions**
1. State three regular-algebra identities. **Hint:** `R+∅`, `Rε`, `R**`.
2. Is concatenation commutative? Prove briefly. **Hint:** compare `{ab}` and `{ba}`.
3. State the distributive law. **Hint:** `R(S+T)=RS+RT`.
4. Expand `(a+ε)*`. **Hint:** `a*`.

**Long-answer questions**
1. Prove `R* = ε+RR*`. **Hint:** split by zero or at least one repetition.
2. Simplify a supplied expression step by step and justify every law. **Hint:** cite idempotence, identity, and distributivity.
3. Explain why `(RS)*` does not equal `R*S*` in general. **Hint:** find a string accepted by one side only.
4. Relate derivatives to residual languages and DFA states. **Hint:** after reading a symbol, what remains possible?
