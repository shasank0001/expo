---
subject: atcd
unit: 4
topic: bottom-up-parsing
syllabus_ref: CSM3203 Unit-IV
status: draft
---
# Bottom-Up Parsing
## Overview
A bottom-up parser starts with the input tokens and repeatedly combines them according to grammar productions until only the start symbol remains. It constructs a parse tree in the reverse direction of a rightmost derivation. The central operations are shift, reduce, and error handling; conflicts between a shift and a reduce are resolved by grammar design, operator precedence, associativity, or parser-table methods such as LR parsing.

## Explanation
### Shift and reduce
A **shift** takes the next input token and pushes it onto the parser stack. A **reduce** applies a production `A→β` to a matching right-hand-side sequence `β` at the top of the stack, pops those symbols, and pushes `A`. The parser repeatedly shifts and reduces while the input remains. If the stack becomes just the start symbol and input is empty, it accepts.

### Reverse derivation
A bottom-up parse constructs a rightmost derivation in reverse. For grammar `E→E+T`, reading `E`, `+`, `T` and reducing `E+T` to `E` undoes the final expansion of that production. The parser does not need to guess the entire parse tree at the beginning; it uses the grammar and current stack context.

### Shift-reduce conflict
A shift-reduce conflict occurs in one state and lookahead when the table has both a shift action and a reduce action. For example, a parser may be able to reduce `T→F` before reading a higher-precedence operator, or shift the operator first. The intended grammar meaning chooses one. For the ambiguous expression grammar `E→E+E|E*E|id`, every unresolved operator can be either shifted or reduced, producing precedence and associativity conflicts.

### Reduce-reduce conflict
A reduce-reduce conflict occurs when two different productions can reduce the same stack pattern on the same lookahead. It often signals that two nonterminals describe overlapping language fragments. A grammar should normally be redesigned rather than hiding the conflict with an arbitrary rule.

### Operator precedence
A common non-LR technique assigns each terminal a precedence and associativity. When the top operator has higher precedence than the incoming operator, reduce; when it has lower precedence, shift; for equal precedence, use left or right associativity. This resolves the intended expression tree but does not make the original grammar unambiguous by itself.

### LR family
LR parsing is a systematic bottom-up method. It uses a stack of parser states and input symbols, a table of shift/reduce/accept actions, and a table of goto states. The `k` in LR(k) indicates how much lookahead is used. The syllabus develops SLR and more powerful LR parsers in separate notes.

### Error handling
On an error, the parser can pop stack symbols, discard input, or use a table-driven repair. A good error message identifies the unexpected lookahead and a nearby expected token. Recovery should not reduce a prefix that is needed to interpret later input.

## Worked examples
### Example 1: simple reduction
Grammar `E→E+T`, `T→id`. For input `id+id`, the parser shifts `id`, reduces `T→id`, shifts `+`, shifts `id`, reduces `T→id`, and then reduces `E→E+T`. The stack and input evolve as:

`[E] id+T → [E, +] T → [E, +] id → [E, +] T → [E]`.

### Example 2: shift/reduce choice
For `id+id*id` with a flat expression grammar, after reading the first `id+id`, the parser can reduce `E→E+E` or shift `*`. The conflict is resolved by giving `*` higher precedence so it shifts and forms the multiplication subtree.

### Example 3: associativity
For `id-id-id`, after the first subtraction, the parser can reduce the left-associative production or shift the next `-`. Left associativity chooses reduce, yielding `(id-id)-id`.

### Example 4: reduce-reduce
Suppose two productions `A→a` and `B→a` are both possible with lookahead `;`. A table cannot choose one without an explicit priority, and the grammar’s intended structure should be clarified.

## Key terms & formulas
- Shift: push input token and advance.
- Reduce `A→β`: pop `|β|` symbols, push `A`.
- Accept: stack contains start symbol and input is exhausted.
- Conflict: two actions for one state/lookahead cell.
- LR(k): left-to-right, rightmost-derivation reverse, `k` lookahead symbols.

## Common mistakes
- Reduction uses the right side of a production; expansion uses the left side.
- A shift-reduce conflict is not automatically a syntax error in the input; it is a parser-design issue.
- Higher-precedence operators should form deeper subtrees.
- Do not confuse a bottom-up stack with the PDA’s input/stack machine; the roles are related but not identical.

## Exam prep
**Likely 2-mark questions**
1. Define shift and reduce. **Hint:** push input versus apply a production.
2. What is a shift-reduce conflict? **Hint:** two actions in one table cell.
3. How does operator precedence help? **Hint:** decides shift versus reduce.
4. What does bottom-up parsing construct? **Hint:** start symbol from leaves.

**Long-answer questions**
1. Trace a bottom-up parse of an expression. **Hint:** show stack, input, and actions.
2. Explain associativity conflict resolution. **Hint:** left versus right rule.
3. Distinguish shift-reduce and reduce-reduce conflicts. **Hint:** one versus two reductions.
4. Compare bottom-up parsing with top-down parsing. **Hint:** reduction versus expansion.
