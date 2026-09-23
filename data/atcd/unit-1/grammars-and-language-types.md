---
subject: atcd
unit: 1
topic: grammars-and-language-types
syllabus_ref: CSM3203 Unit-I
status: draft
---
# Grammars and Language Types
## Overview
A formal grammar is a finite set of rewrite rules that generates the strings of a language. Chomsky’s classification sorts grammars by how much freedom their productions allow. The restrictions are not arbitrary: they correspond to increasingly powerful machine models. This hierarchy connects compiler syntax, regular-expression tools, and the limits of automatic parsing.

## Explanation
### Formal grammar components
A grammar `G=(V_N,V_T,P,S)` has:

- `V_N`: nonterminals, or variables, used to group strings;
- `V_T`: terminals, the actual symbols of the generated strings;
- `P`: productions, each written `A→α`, with `A∈V_N`;
- `S∈V_N`: the designated start symbol.

A derivation begins with `S` and applies productions. A sentential form may contain nonterminals; a terminal string contains only terminals. The grammar generates `L(G)`. In a compiler, terminals correspond roughly to tokens and nonterminals to grammatical categories.

### Type-0 grammars
A Type-0 or unrestricted grammar allows a production of the form `A→α` without length or context restrictions. Equivalently, a rule can replace a string `α` by a string `β` when `α` contains at least one nonterminal. Type-0 grammars generate recursively enumerable languages. A rewriting system is a useful intuition, but the grammar must still have one designated left-hand string in its formal definition.

### Type-1 grammars
A Type-1 or context-sensitive grammar has productions of the form `αAβ→αγβ`, where the nonterminal occurs in context and the replacement has the same length. The context `αβ` is unchanged. Type-1 grammars generate context-sensitive languages, which can enforce dependencies that a CFG cannot. A classic example is a language that copies matching delimiters or tracks length relations beyond the CFG limit.

### Type-2 grammars
A Type-2 or context-free grammar has exactly one nonterminal on the left:

`A→α`.

The right side may contain any sequence of terminals and nonterminals, and the replacement of `A` is independent of surrounding symbols. Type-2 grammars generate context-free languages. Most programming-language grammars are context-free or close to it, which is why recursive-descent, LL, and LR parsers are useful.

### Type-3 grammars
A Type-3 or regular grammar has a restricted form. In a regular grammar, every production is one of:

- `A→aB` or `A→a` (right-linear), or
- `A→Ba` or `A→a` (left-linear).

It can generate only regular languages. Regular grammars correspond to finite automata, regular expressions, and lexical token patterns. A grammar such as `S→aS|a` is regular and generates `a+`; adding `ε` as an explicit alternative generates `a*`.

### Hierarchy and machines
The classes are nested in expressive power:

`Type-0 ⊃ Type-1 ⊃ Type-2 ⊃ Type-3`

and, in standard terms:

`recursively enumerable ⊃ context-sensitive ⊃ context-free ⊃ regular`.

The correspondence is not a claim that every individual machine is identical; it is a language-class result. Finite automata recognize Type-3 languages, PDAs recognize Type-2 languages, and unrestricted rewriting/Turing computations correspond to the Type-0 setting in the usual curriculum presentation.

### Regular versus context-free examples
`L₁={a^n b^n | n≥0}` is context-free but not regular. A PDA can store the number of `a`s and match each `b`. `L₂={ww | w∈{a,b}*}` is also context-sensitive and not context-free in the usual alphabet encoding. `L₃={strings containing `ab`}` is regular and can be recognized with two or three states.

### Designing a grammar
Start with the start symbol, introduce a nonterminal for each syntactic category, write productions in terms of smaller categories, and include token-level productions. Prefer unambiguous structure, consistent naming, and rules that reflect precedence. For expression grammars, separate levels such as expression, term, factor, and atom.

## Worked examples
### Example 1: classify a grammar
`S→aS|a|ε` has one nonterminal on the left and only forms `aS`, `a`, and `ε`; it is a right-linear Type-3 grammar. It generates `{ε,a,aa,aaa,...}`.

`S→AB; A→a; B→b` is Type-2 because the left side is a single nonterminal, though it also happens to be regular. A grammar is classified by the strongest permitted form, not merely by the example language it generates.

### Example 2: generate balanced parentheses
`S→SS | (S) | ε` generates balanced parenthesis strings. Each pair is introduced by `(S)`, and concatenations are formed by `SS`. It is context-free and unambiguous under this formulation.

### Example 3: context restriction
A rule `aAb→aAAb` changes `A` to `A` while preserving surrounding `a` and `b`; it illustrates a context-sensitive production. A CFG rule would replace `A` without requiring that surrounding `a...b` context.

## Key terms & formulas
- Production: `A→α`.
- Derivation: sequence `S ⇒ ... ⇒ w`, where `w∈V_T*`.
- Type-1 form: `αAβ→αγβ` with `|αAβ|=|αγβ|`.
- Type-2 form: `A→α`.
- Type-3 form: right-linear `A→aB/a` or left-linear `A→Ba/a`.
- `V_N`, `V_T`, `P`, `S`: nonterminals, terminals, productions, start symbol.

## Common mistakes
- Chomsky type is defined by the production form, not by how easy the grammar looks.
- A grammar may be regular even if its example has multiple nonterminals; classification depends on the rules.
- Type-1 is not the same as Type-2: Type-1 preserves surrounding context.
- A context-free rule replaces one nonterminal without considering its neighbors.

## Exam prep
**Likely 2-mark questions**
1. Define a grammar and list its components. **Hint:** `V_N,V_T,P,S`.
2. State the four Chomsky types. **Hint:** 0 unrestricted through 3 regular.
3. Give one machine corresponding to each major type. **Hint:** TM, restricted rewriting, PDA, finite automaton.

**Long-answer questions**
1. Explain the Chomsky hierarchy with production forms and language classes. **Hint:** move from unrestricted to linear restrictions.
2. Classify several supplied grammars and justify each answer. **Hint:** inspect left-hand sides and right-hand forms.
3. Prove `a^n b^n` is not regular but is context-free. **Hint:** pumping intuition and PDA/grammar construction.
4. Design an unambiguous expression grammar. **Hint:** one nonterminal per precedence level.
