---
subject: atcd
unit: 2
topic: regular-grammar
syllabus_ref: CSM3203 Unit-II
status: draft
---
# Regular Grammar
## Overview
A regular grammar is a context-free grammar whose productions have a restricted linear form, so it generates only regular languages. Regular grammars connect the generative description of a language with finite automata and regular expressions. They are especially useful when a problem asks for a grammar rather than an automaton, and they help explain why token-level language rules are easier to implement than arbitrary syntax.

## Explanation
### Definition and forms
A right-linear regular grammar has every production in one of the forms

`A→aB` or `A→a`

where `A,B` are nonterminals and `a` is a terminal (some conventions allow `A→ε`). A left-linear regular grammar has forms

`A→Ba` or `A→a`.

The two forms generate the same class of regular languages, although their derivations and corresponding automata are easier to read in one form or the other.

### How a regular grammar generates strings
A nonterminal represents unfinished work, and each production moves the unfinished work one terminal at a time to the right (right-linear form). A base production terminates the string. For example,

`S→aS|b`

generates zero or more `a`s followed by one `b`; repeatedly applying `S→aS` puts the `a`s before the base production `S→b`. A second simple example is `S→aS|ε`, which generates `a*`.

### Conversion to regular expressions
Each regular grammar can be viewed as a system of regular-language equations. For example, `S→aS|b` gives `S=aS+b`, and Arden’s theorem yields a regular expression for the language. A grammar-to-expression conversion is systematic; the resulting expression can then be converted to an NFA or DFA.

### Conversion to finite automata
For a right-linear grammar, create a state for each nonterminal. For `A→aB`, draw an `a` edge from `A` to `B`; for `A→a`, draw an `a` edge from `A` to a new final state. The grammar start state is the automaton start state, with final states for completed productions. Left-linear forms are handled by reversing the direction of the constructed paths.

### Regular grammar versus regular expression
A regular expression describes strings by operators; a regular grammar describes strings by productions. They can denote the same language, but a grammar is often more natural when a parser or instructional example needs a nonterminal hierarchy. A regular grammar cannot express `a^n b^n`, because it cannot make one nonterminal remember an unbounded count of `a`s.

### Restrictions and ambiguity
A regular grammar must not contain a nonterminal with arbitrary context on the left or a right side with more than one trailing nonterminal in right-linear form. Productions such as `A→BC` are context-free but not regular. A regular language may have both regular and context-free grammars; classify the grammar by its rule shape, not by the language’s name.

## Worked examples
### Example 1: `a*`
Grammar `S→aS|ε` is right-linear. Starting at `S`, choose `S→aS` any number of times and finish with `S→ε`, generating `ε,a,aa,...`.

### Example 2: strings ending in `b`
`S→aS|bS|b` is right-linear and generates exactly the strings over `{a,b}` that end in `b`. The recursive choices consume any prefix, and the final production `S→b` supplies the last symbol. A corresponding regex is `(a|b)*b`. If the empty string must also be included, use a separate language or a carefully designed final-state nonterminal; simply adding `S→ε` to this grammar would generate every string.

### Example 3: even-length strings
A pair of nonterminals can enforce length parity:

`S→aT|bT|ε`
`T→aS|bS|ε`.

Starting at `S`, every two symbols return to `S`; hence the grammar generates exactly the even-length strings over `{a,b}`, including `ε`. A single nonterminal with `S→aS|bS|ε` would generate all lengths, not just even lengths.

### Example 4: conversion
For `S→aS|bS|b`, create a start state `S`. Add `a` and `b` self-loops for the two recursive productions, and add a `b` edge from `S` to a new final state for `S→b`. The final state is reached only when the last input symbol is `b`; the recursive `b` loop does not itself make the state final.

### Example 5: rejecting a CFG shape
`S→aSb|ε` is context-free but not regular. Its production has two nonterminals on the right and can generate `a^n b^n`, which finite automata cannot recognize. This is a quick classification test.

## Key terms & formulas
- Right-linear: `A→aB` or `A→a` (plus permitted ε form).
- Left-linear: `A→Ba` or `A→a`.
- Regular grammar language class: regular languages.
- `S→aS|ε` generates `a*`.
- `S→aSb|ε` is not regular.
- Arden can solve equations such as `S=aS+b`.

## Common mistakes
- Do not call any grammar with a simple-looking rule regular; inspect every production.
- `A→aB` is regular in right-linear form, but `A→aBC` is not.
- A regular grammar can generate `ε`; the empty production is not automatically useless.
- Regular grammar and regular expression are not identical notations, though they describe the same class.

## Exam prep
**Likely 2-mark questions**
1. Define right-linear and left-linear regular grammars. **Hint:** state production forms.
2. Give a regular grammar for `a*`. **Hint:** `S→aS|ε`.
3. Give a regular grammar for strings ending in `b`. **Hint:** repeat then append `b`.
4. Why is `S→aSb|ε` not regular? **Hint:** generates unbounded paired strings.

**Long-answer questions**
1. Convert a regular grammar to a finite automaton. **Hint:** state per nonterminal and final states.
2. Derive a regular expression using Arden’s theorem. **Hint:** equation from a recursive production.
3. Compare regular grammar, regex, NFA, and DFA. **Hint:** generation versus recognition and equivalence.
4. Classify several grammars as regular or context-free. **Hint:** inspect production shape and language evidence.
