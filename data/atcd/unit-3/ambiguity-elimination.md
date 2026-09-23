---
subject: atcd
unit: 3
topic: ambiguity-elimination
syllabus_ref: CSM3203 Unit-III
status: draft
---
# Ambiguity Elimination
## Overview
Ambiguity elimination rewrites a grammar so that every generated string has one intended parse tree. The usual methods are separate nonterminals for precedence and associativity, removal of duplicate or unreachable rules, and careful redesign of constructs whose structure was not specified. A rewrite is successful only if the generated language remains the same and the intended structure becomes unique.

## Explanation
### Preserve the language
Before changing a grammar, write down the intended meaning and a set of valid/invalid examples. After rewriting, check that no old valid string is lost and no invalid string is introduced. Removing ambiguity must not accidentally restrict a valid construct.

### Separate precedence levels
Start with an ambiguous expression grammar:

`E→E+E | E*E | id`.

Introduce one nonterminal per precedence level:

`E→E+T | T`
`T→T*F | F`
`F→(E) | id`.

Now `+` is parsed at the `E` level and `*` at the deeper `T` level, so `id+id*id` has only the grouping `id+(id*id)`.

### Encode associativity
Left-associative repeated operators use left recursion:

`E→E+T | T`.

The left recursive branch allows the current `E` to combine with another `T`, forcing `(a+b)+c`. Right recursion,

`E→T+E | T`,

forces `a+(b+c)`. Parentheses can override the default grouping.

### Remove duplicate and unreachable alternatives
If a production is never used, remove it. If two alternatives generate exactly the same language, retain one. If a nonterminal is unreachable from the start, delete it. These steps may remove obvious ambiguity, but they are not enough when the same terminal string can be grouped in two structural ways.

### Restructure statements
A dangling `if` grammar can be ambiguous:

`S→if E then S | S`
`S→other`.

The two `S` positions allow the `else` to attach to different nested `if`s. A common unambiguous convention is:

`S→if E then S else S | matched`
`matched→if E then matched else matched | other`.

This binds each `else` to the nearest unmatched `if`. A language may choose a different convention, but the rule must be explicit.

### Resolve conflicts in parser tools
A parser generator can sometimes use operator-precedence declarations or associativity directives to resolve shift/reduce conflicts. This is useful operationally, but it is better to understand the grammar’s intended structure. Reduce/reduce conflicts usually indicate a deeper design problem and should not be hidden by arbitrary priority.

### Inherent ambiguity
If the language itself is inherently ambiguous, no grammar rewrite will make it unambiguous under the CFG model. In that case, the compiler may need extra semantic information, a different formalism, or an explicitly chosen interpretation.

## Worked examples
### Example 1: expression precedence
Start with `E→E+E|E*E|id`. Rewrite as the three-level grammar above. The string `id+id*id` now has one tree: the `*` subtree is inside `T`, and the `+` node is the root of the expression. The string `(id+id)*id` still has parentheses forcing the desired structure.

### Example 2: left associativity
For `a-b-c`, use `E→E-T|T`. The first `E` on the left combines with another `T`, giving `(a-b)-c`. A parser can implement it with a loop that accumulates the left term.

### Example 3: dangling else
For `if a then if b then x else y`, the unambiguous nearest-if grammar attaches `else` to the inner `if b`. The tree has a nested matched statement, and the outer `if` has no else. A naïve grammar could attach the else to the outer if, producing a different tree.

### Example 4: duplicate production
`S→A | A` has two identical alternatives. Removing one preserves `L(G)` and leaves one production for the same tree shape. This is a simple syntactic ambiguity/duplication case.

## Key terms & formulas
- Precedence grammar levels: `E`, `T`, `F`, ...
- Left associativity: `E→E op T | ...`.
- Right associativity: `E→T op E | ...`.
- `matched` nonterminal binds `else` to nearest unmatched `if`.
- Rewrite condition: `L(G_old)=L(G_new)` and one intended tree per string.

## Common mistakes
- Adding precedence symbols to a grammar without changing productions does not remove ambiguity.
- Removing all unit productions blindly can create undesirable recursion or cycles.
- Associativity direction must match the language’s intended convention.
- An inherent ambiguity cannot be fixed by merely renaming a nonterminal.

## Exam prep
**Likely 2-mark questions**
1. Give the standard three-level expression grammar. **Hint:** `E`, `T`, `F`.
2. How does left recursion enforce left associativity? **Hint:** `E→E+T`.
3. What is the dangling-`else` problem? **Hint:** two possible attachment points.
4. State one condition for a valid grammar rewrite. **Hint:** same language.

**Long-answer questions**
1. Remove ambiguity from an expression grammar and explain the resulting precedence. **Hint:** use levels and recursion direction.
2. Rewrite a dangling-`else` grammar. **Hint:** introduce `matched`.
3. Distinguish a grammar that is ambiguous from an inherently ambiguous language. **Hint:** existence of an alternative grammar.
4. Explain how a parser generator’s conflict resolutions relate to grammar design. **Hint:** precedence directives versus true structure.
