---
subject: atcd
unit: 3
topic: cfg-definition-and-design
syllabus_ref: CSM3203 Unit-III
status: draft
---
# Context-Free Grammar Definition and Design
## Overview
A context-free grammar (CFG) is a formal grammar whose production replaces one nonterminal independently of its surrounding symbols. CFGs describe the nested and hierarchical structure of programming languages: balanced blocks, expressions with precedence, and statements containing statements. Designing a good CFG is both a language-definition task and a parser-design task; ambiguous or left-recursive rules may be correct generators but awkward or impossible for a chosen top-down parser.

## Explanation
### Formal components
A CFG is the tuple

`G=(V_N,V_T,P,S)`.

- `V_N` is the finite set of nonterminals or variables.
- `V_T` is the finite terminal alphabet.
- `P` is a finite set of productions `A→α`, where `A∈V_N` and `α∈(V_N∪V_T)*`.
- `S∈V_N` is the start symbol.

A derivation begins with `S` and repeatedly replaces one nonterminal. A sentential form may contain nonterminals; a terminal string is a sentence. The language is `L(G)={w∈V_T* | S⇒*w}`.

### Context-free meaning
The replacement of `A` does not depend on symbols immediately before or after it. Thus a production `A→BC` can apply wherever `A` occurs. This is more expressive than a regular grammar and is exactly the level needed for many constructs such as nested `if` statements and balanced parentheses.

### Grammar design from a language
1. Identify the start symbol, usually `program` or `S`.
2. Divide the language into meaningful categories (`statement`, `expression`, `term`, `factor`, `identifier`).
3. Write the broad production first, then define each nonterminal.
4. Add lexical productions that connect grammar symbols to tokens or token classes.
5. Decide how to encode precedence, associativity, and optional parts.
6. Test the grammar on valid and invalid strings and check for ambiguity.

For example:

`E → E + T | T`
`T → T * F | F`
`F → (E) | id | number`

separates addition from multiplication and leaves parentheses to force grouping.

### Recursive and base rules
A nonterminal may appear on its right-hand side to describe repetition. Direct left recursion such as `E→E+T` is useful for a bottom-up parser but causes a naive recursive-descent top-down parser to recurse forever. A right-recursive rule such as `A→aA|ε` can be handled by a loop with a changed production. Base rules terminate derivations and connect a category to terminals.

### Terminals versus tokens
A formal CFG often uses characters as terminals, while a compiler grammar uses token classes such as `ID`, `NUM`, `IF`, and `LPAREN`. Lexical analysis has already recognized those tokens. A grammar can also use a notation such as `id` to mean the token class, not a particular identifier spelling.

### Parsability considerations
An LL(1) grammar needs distinct FIRST sets for alternatives and no left recursion. An LR grammar generally permits more left recursion and local ambiguity can be handled through precedence or grammar design. A grammar can generate a language yet be unsuitable for a particular parser; grammar design and parser choice must be considered together.

## Worked examples
### Example 1: simple grammar
Let `V_N={S,A}`, `V_T={a,b}`, `P={S→AB,A→a,B→b}`, and `S` be the start symbol. The only derivation is `S⇒AB⇒aB⇒ab`, so `L(G)={ab}`.

### Example 2: list grammar
`S→aS | b` generates one or more `a`s followed by `b`: `b, ab, aab, ...`. A start rule `S→aS|ε` would instead generate `a*`, so the choice of base production changes the language.

### Example 3: expression precedence
For `a+b*c`, the grammar `E→E+T|T` and `T→T*F|F` forces `*` inside `T`, so the tree groups `a+(b*c)`. With `E→E+E|T` alone, the grouping would be ambiguous.

## Key terms & formulas
- `S⇒*w`: zero or more derivation steps reach terminal string `w`.
- `α⇒β`: one production application.
- Context-free production: exactly one nonterminal on the left.
- FIRST and FOLLOW sets guide LL(1) decisions.
- `L(G)` includes every terminal string reachable from `S`.

## Common mistakes
- The left side must contain one nonterminal for a context-free production.
- A nonterminal is an abbreviation, not an input character.
- A grammar can be correct but unsuitable for a chosen parser.
- Precedence must be encoded in productions or parser rules, not merely hoped for.

## Exam prep
**Likely 2-mark questions**
1. Define a CFG and list its components. **Hint:** `V_N,V_T,P,S`.
2. Give a grammar for `a^n b^n`. **Hint:** a matching pair of recursive rules.
3. Define FIRST and FOLLOW. **Hint:** possible beginnings and possible followers.
4. Why can left recursion hurt top-down parsing? **Hint:** parser may recurse without consuming input.

**Long-answer questions**
1. Design a CFG for arithmetic expressions with precedence. **Hint:** expression, term, factor.
2. Design a CFG for a small statement language. **Hint:** separate assignment, conditional, loop, and block.
3. Derive a valid and invalid sentence from a supplied grammar. **Hint:** show sentential forms and terminal string.
4. Discuss how a grammar can be made LL(1)-friendly. **Hint:** left recursion, common prefixes, FIRST sets.
