---
subject: atcd
unit: 3
topic: top-down-parsing
syllabus_ref: CSM3203 Unit-III
status: draft
---
# Top-Down Parsing
## Overview
Top-down parsing starts with the grammar’s start symbol and works toward the input. It repeatedly chooses a production for the leftmost unresolved nonterminal, matching terminals as they are encountered. A successful parse constructs a leftmost derivation. The method is intuitive and useful for LL(1) grammars, but left recursion and insufficient lookahead can cause failure or infinite recursion.

## Explanation
### Basic algorithm
Maintain a stack or a set of expected nonterminals, initially containing `S`. At each step:

1. If the top is a terminal, compare it with the next input token and consume it on a match.
2. If the top is a nonterminal, choose one of its productions using lookahead.
3. Push the production’s right-hand side in reverse order so the leftmost symbol is processed next.
4. If no production fits, report a syntax error.

The input is accepted if the expected-symbol stack becomes empty exactly when all input is consumed.

### Recursive-descent implementation
A common implementation writes one procedure for each nonterminal. `expression()` calls `term()`, and `term()` matches factors and multiplication. Local variables can hold the next token, and helper procedures can test the lookahead symbol. A hand-written recursive-descent parser can be easy to read, but it must avoid left recursion and should avoid hidden backtracking unless the grammar is small.

### Predictive parsing
A **predictive parser** uses a parsing table indexed by nonterminal and lookahead token. For an LL(1) grammar, the table has at most one production in each relevant cell. The table is constructed from FIRST and FOLLOW sets:

- If `A→α` is placed in a cell for terminals in `FIRST(α)`.
- If `α` is nullable, also place it in cells for terminals in `FOLLOW(A)`.

No conflicts means the grammar is LL(1) with respect to the table.

### Backtracking
A backtracking parser tries a production, parses as far as possible, and returns to try another choice if failure occurs. This is conceptually simple but can be exponentially slow. It can handle some grammars that are not LL(1), but compiler generators normally prefer predictive tables to avoid hidden retries.

### Left recursion
Direct left recursion `A→Aα|β` causes a recursive-descent procedure for `A` to call itself before consuming input. Indirect left recursion can have the same effect. It can be transformed for LL parsing, for example:

`A→βA'`
`A'→αA' | ε`.

A top-down parser should also avoid unnecessary common-prefix alternatives unless lookahead can distinguish them.

### Error handling
A parser reports the expected token or nonterminal and may recover by consuming input until a follow set member. FOLLOW sets help identify safe synchronization points. Error messages are most useful when they include the unexpected token and a source position.

## Worked examples
### Example 1: successful parse
Grammar `S→A|b`, `A→a`. For input `a`, the parser chooses `S→A` because lookahead is `a`, then chooses `A→a` and consumes it. The accepted derivation is `S⇒A⇒a`.

### Example 2: failure
For the same grammar and input `b`, the parser chooses `S→b` and accepts. For input `c`, no production begins with `c`; the parser reports an expected `a` or `b` at position 1.

### Example 3: table prediction
Suppose `E→E+T|T`. This is left recursive, so a naive recursive-descent call to `expression()` recurses on itself. A predictive table can describe the reduction only in a bottom-up parser; for top-down parsing, rewrite the grammar into a right-recursive or precedence-separated form.

### Example 4: a small LL(1) table
Consider `S→aA|b` and `A→c|ε`, with `S` as the start symbol. `FIRST(S)={a,b}`, `FIRST(A)={c,ε}`, and if `S` ends the input, `FOLLOW(A)=FOLLOW(S)={$}`. The predictive table is:

| nonterminal | a | b | c | $ |
|---|---|---|---|---|
| `S` | `S→aA` | `S→b` | error | error |
| `A` | error | error | `A→c` | `A→ε` |

For input `ac`, the parser chooses `S→aA`, matches `a`, chooses `A→c`, and accepts. For input `a$`, it chooses the nullable `A→ε` only when `$` is the lookahead.

## Key terms & formulas
- Top-down: `S` to terminal input; leftmost derivation.
- `FIRST(α)`: terminals that can begin a derivation of `α`.
- `FOLLOW(A)`: terminals that can follow `A` in a sentential form.
- LL(1): left-to-right, leftmost derivation, one-token lookahead.
- Parsing-table conflict: more than one action for one `(nonterminal, lookahead)` cell.

## Common mistakes
- Top-down parsing expands the start symbol; bottom-up parsing reduces input.
- Direct left recursion must be removed for ordinary recursive descent.
- `FOLLOW(A)`, not `FIRST(A)`, determines nullable-production table entries.
- A parser that tries alternatives blindly is backtracking, not necessarily predictive.

## Exam prep
**Likely 2-mark questions**
1. Explain the working of top-down parsing. **Hint:** expand start and match input.
2. Define FIRST and FOLLOW. **Hint:** possible beginnings and followers.
3. Why is left recursion a problem? **Hint:** recursion without consuming lookahead.
4. What is LL(1)? **Hint:** one-token predictive top-down parsing.

**Long-answer questions**
1. Construct a recursive-descent parser for a small expression grammar. **Hint:** one procedure per nonterminal.
2. Fill an LL(1) table for a supplied grammar. **Hint:** FIRST, FOLLOW, nullable alternatives.
3. Transform a left-recursive grammar. **Hint:** introduce a helper nonterminal and ε base.
4. Compare predictive parsing with backtracking. **Hint:** table choice versus trial and undo.
