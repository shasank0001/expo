---
subject: atcd
unit: 3
topic: derivations
syllabus_ref: CSM3203 Unit-III
status: draft
---
# Derivations Using a Grammar
## Overview
A derivation is a step-by-step application of grammar productions that starts at the start symbol and aims to reach a terminal string. Derivations show how a grammar generates language and are the conceptual foundation for top-down and bottom-up parsing. The same terminal string can have different derivations and parse trees when a grammar is ambiguous.

## Explanation
### Sentential forms
A sentential form is any form reachable from `S` by zero or more production applications. It may contain terminals, nonterminals, or both. A string consisting only of terminals is a terminal form or sentence. A derivation that reaches a terminal string proves membership; a parser may stop earlier when it has enough structure.

### One-step and multi-step notation
`α⇒β` means one production is applied to one occurrence in `α`. `α⇒*β` means zero or more steps, and `α⇒+β` means one or more. A sequence such as

`S⇒AB⇒aB⇒ab`

has three applications: `S→AB`, `A→a`, and `B→b`.

### Leftmost derivation
A leftmost derivation always replaces the leftmost nonterminal in the current sentential form. For `S→AB`, `A→a`, `B→b`:

`S⇒AB⇒aB⇒ab`.

Leftmost derivations correspond naturally to top-down parsing because a parser predicts a production for the leftmost unresolved symbol.

### Rightmost derivation
A rightmost derivation always replaces the rightmost nonterminal:

`S⇒AB⇒Ab⇒ab`.

Rightmost derivations are useful for bottom-up parsing: a bottom-up parser reduces the right-hand side of a production in reverse order, effectively constructing a rightmost derivation backward.

### Ambiguity and derivation order
For `E→E+E|T` and `T→id`, the string `id+id+id` can be derived as

`E⇒E+E⇒E+E+E⇒id+E+E⇒id+id+E⇒id+id+id`

or with a different expansion order. These choices produce distinct parse trees and demonstrate ambiguity. Simply changing from leftmost to rightmost does not create a second tree if the same production choices are used; the structure of the grammar determines the tree.

### Derivation trees
The derivation tree or parse tree records which production was applied to each nonterminal. The root is the start symbol, internal nodes are nonterminals with production children, and leaves are terminals. A derivation sequence and its parse tree contain the same structural information, although the tree is easier to inspect.

### Membership and parsing
A general derivation search is exponential because many choices may be tried. Predictive top-down parsing uses lookahead to choose a production, while bottom-up parsing shifts and reduces. Left recursion and conflicts determine whether a practical parser can implement the grammar directly.

### Grammar transformations
A derivation can be used to discover equivalent rules. For example, replacing `A→B` by the right side of `B` can remove a unit production, but only if it does not create harmful cycles. Derivation analysis is also used in ambiguity elimination and parser-table construction.

## Worked examples
### Example 1: leftmost derivation
For `S→AB`, `A→a`, `B→b`:

`S⇒AB⇒aB⇒ab`.

At each step the leftmost nonterminal is replaced.

### Example 2: rightmost derivation
For the same grammar:

`S⇒AB⇒Ab⇒ab`.

The rightmost nonterminal `B` is expanded first.

### Example 3: balanced parentheses
For `S→SS | (S) | ε`, derive `(ε)`: `S⇒(S)⇒(ε)`. Derive `()()` by first expanding the first `S`, then the second. The tree shows the concatenation of two balanced components.

### Example 4: ambiguity witness
For `E→E+E|T`, `T→id`, derive `id+id` in two ways:

- `E⇒E+E⇒id+E⇒id+id`;
- `E⇒E+E⇒E+id⇒id+id`.

The productions differ in which occurrence of `E` is expanded, so the corresponding trees differ.

## Key terms & formulas
- `α⇒β`: one production step.
- `α⇒*β`: zero or more production steps.
- `S⇒*w` iff `w∈L(G)`.
- Leftmost: replace the leftmost nonterminal.
- Rightmost: replace the rightmost nonterminal.
- Parse tree root `S`, internal nonterminals, terminal leaves.

## Common mistakes
- A sentential form is not necessarily a terminal string.
- `⇒*` includes zero steps, so `S⇒*S` is true.
- Leftmost and rightmost refer to which nonterminal is replaced, not which terminal is read.
- One terminal string can have one derivation sequence and still correspond to different tree structures if different productions are used; inspect the structure carefully.

## Exam prep
**Likely 2-mark questions**
1. Define a derivation. **Hint:** sequence of production applications from `S`.
2. Distinguish leftmost and rightmost derivation. **Hint:** position of replaced nonterminal.
3. Define a sentential form. **Hint:** reachable form possibly containing nonterminals.
4. How do leftmost and rightmost derivations relate to parsing? **Hint:** top-down versus reverse bottom-up.

**Long-answer questions**
1. Show leftmost and rightmost derivations for a supplied grammar and string. **Hint:** label each step.
2. Use two derivations to demonstrate ambiguity. **Hint:** choose different production occurrences.
3. Explain why unrestricted derivation search is inefficient. **Hint:** many choices and backtracking.
4. Convert a derivation into a parse tree. **Hint:** production children at each nonterminal.
