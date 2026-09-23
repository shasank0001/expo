---
subject: atcd
unit: 3
topic: ambiguity
syllabus_ref: CSM3203 Unit-III
status: draft
---
# Ambiguity
## Overview
A context-free grammar is ambiguous if at least one string in its language has two or more distinct parse trees. Ambiguity is a property of the grammar, not necessarily of the language: a language may have one ambiguous grammar and another unambiguous grammar. In a compiler, ambiguity can produce different meanings for the same token sequence, so it should be removed when a practical parser requires a unique structure.

## Explanation
### Definition
A grammar `G` is ambiguous if there is a terminal string `w` and two different parse trees with root `S` and leaf yield `w`. Equivalently, `w` has two different leftmost derivations whose production choices create different trees. The two trees must be structurally distinct; merely writing the same derivation in a different order is not enough.

### Inherent versus avoidable ambiguity
A language can be **inherently ambiguous** if no unambiguous context-free grammar generates it. Many common languages are not inherently ambiguous: balanced parentheses, arithmetic with fixed precedence, and most programming constructs can be described unambiguously. Before rewriting a grammar, check whether the intended language itself is inherently ambiguous.

### Expression ambiguity
The grammar

`E→E+E | T`
`T→id`

does not encode precedence or associativity. The string `id+id+id` can be grouped as `(id+id)+id` or `id+(id+id)`. Even a binary string with two operators can be ambiguous, so the problem appears quickly.

### Ambiguity tests
A direct test is to find a string with two parse trees. For grammars with ε-productions, unit productions, or repeated nonterminals, inspect these cases first. The classic “E and I” test applies to a restricted grammar family: first check whether the grammar can derive a string containing two different E-type nonterminals in a way that exposes two trees; then check whether one such E can derive the terminal string `i`. It is a quick screen, not a general algorithm for every CFG.

### Dangling-ε and associativity
An expression grammar such as

`E→E+E | E*E | id`

has two kinds of problems: precedence ambiguity between `+` and `*`, and associativity ambiguity for repeated operators. Separating expression levels solves precedence; using left recursion with a base case fixes left associativity. Right recursion gives right associativity only when the language explicitly requires it.

### Why ambiguity harms parsing
A deterministic predictive parser normally needs to choose one production from a table cell. Ambiguity can appear as multiple entries, or a bottom-up parser can face shift/reduce or reduce/reduce conflicts. A parser generator may resolve conflicts by precedence, but the language meaning should ideally be fixed in the grammar.

### Language versus grammar
If a grammar is ambiguous, first find the witness and identify what structural information is missing. Sometimes the language description is incomplete: it may not specify precedence, associativity, declaration rules, or whether a construct is left recursive. Rewriting the grammar should preserve exactly the intended language.

## Worked examples
### Example 1: `E→E+E|T`
The string `id+id` has a left grouping and a right grouping. The two parse trees both have leaves `id + id` but place the first or second expansion at different levels, proving ambiguity.

### Example 2: associative distinction
A grammar with `E→E-E|id` is ambiguous between `id-id-id` groupings. A left-associative grammar is

`E→E-T|T`, `T→id`, which forces `(id-id)-id`. A right-associative grammar uses `E→T-E|T` and forces `id-(id-id)`.

### Example 3: ε ambiguity
For `S→A | ε` and `A→S|ε`, the empty string has more than one derivation/tree: `S⇒ε` and `S⇒A⇒ε` (or through `S`). Removing the redundant cycle can eliminate this ambiguity.

### Example 4: screening with E and I
For a grammar containing nonterminals `E` and `I`, if a derivation can place two different E symbols in a sentential form and one E can derive `i`, there is a common ambiguity witness in the standard test. Always explain the trees in the final answer.

## Key terms & formulas
- Ambiguous grammar: one yield, at least two distinct parse trees.
- `S⇒*w`: membership derivation.
- Inherently ambiguous language: no unambiguous CFG exists.
- Associativity is the grouping rule for repeated same-precedence operators.
- Conflict symptoms: multiple table entries, shift/reduce, reduce/reduce.

## Common mistakes
- Ambiguity belongs to a grammar, although it can reflect an underspecified language.
- A string with two different textual derivations is not automatically ambiguous if both derive the same tree.
- Precedence and associativity are separate issues.
- Not every conflict is caused by ambiguity; parser implementation details can also matter.

## Exam prep
**Likely 2-mark questions**
1. Define an ambiguous grammar. **Hint:** two distinct parse trees for one string.
2. Why is `E→E+E|T` ambiguous? **Hint:** repeated `+` has two groupings.
3. Distinguish grammar ambiguity from inherent language ambiguity. **Hint:** rewrite may or may not be possible.
4. Name two parser conflicts caused by ambiguity. **Hint:** shift/reduce and reduce/reduce.

**Long-answer questions**
1. Find a witness string and draw two parse trees. **Hint:** same leaves, different shape.
2. Explain the E-and-I ambiguity test. **Hint:** two E occurrences and a derivable terminal.
3. Discuss why `a^n b^n` is unambiguous in a standard CFG. **Hint:** unique matching structure.
4. Explain how precedence and associativity create ambiguity. **Hint:** separate levels and recursion direction.
