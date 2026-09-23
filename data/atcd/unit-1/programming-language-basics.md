---
subject: atcd
unit: 1
topic: programming-language-basics
syllabus_ref: CSM3203 Unit-I
status: draft
---
# Programming Language Basics
## Overview
Programming languages give programmers a precise vocabulary for algorithms and data. A compiler needs to know both the spelling of a program and what its constructs mean. This note introduces alphabets, tokens, grammar, syntax, semantics, declarations, scopes, and common language styles so that later lexical, syntax, semantic, and code-generation work has a clear foundation.

## Explanation
### Alphabet, character, and token
A language’s **alphabet** is the finite set of characters from which source text is written: letters, digits, punctuation, and special symbols. A **character** is one alphabet symbol. A **token** is a meaningful lexical class or instance, such as an identifier, integer constant, keyword, operator, or delimiter. The scanner converts a character stream into tokens and attaches attributes such as a literal’s numeric value or a name’s spelling.

Example tokens in `if x >= 10 then` are `IF`, `ID(x)`, `RELOP(>=)`, `INT(10)`, and `THEN`. Whitespace is usually skipped, but its presence may be used to separate tokens.

### Syntax and grammar
Syntax is the arrangement of tokens allowed by the language. A context-free grammar (CFG) is a common formal description:

`G = (V_N, V_T, P, S)`

where `V_N` is the nonterminal set, `V_T` the terminal set, `P` the production set, and `S` the start symbol. A production has the form `A → α`. A parser uses such rules to decide whether a token sequence is well formed and to build a tree.

### Semantics
Semantics gives meaning to syntactically valid constructs. It answers questions such as: What type does an expression have? Which declaration does an identifier refer to? When is a variable initialized? What does a function return? Semantic analysis checks type compatibility, scope, declaration order, operator legality, and other rules. `x = 1 + "A"` may be syntactically valid but semantically invalid in a numeric-only language.

### Declarations, identifiers, bindings, and scopes
An **identifier** names an object, procedure, type, or other entity. A **declaration** introduces a name and its attributes. **Binding** associates a name with an entity. **Scope** is the portion of the program in which a binding is visible. Lexical/static scope follows the grammar and nesting; dynamic scope follows the sequence of calls. Compiler symbol tables store the scope and attributes needed to resolve names.

### Types and expressions
A type describes the values an expression may have and the operations allowed on them. Common types include integer, real, character, Boolean, array, pointer, record, and function types. Expression evaluation must respect precedence, associativity, coercions, and short-circuit behavior. Parentheses can change grouping even when every token is the same.

### Declarative and imperative styles
An **imperative** language describes changes to a program state through assignments and control flow. A **functional** language emphasizes functions, inputs, and outputs, often avoiding mutable state. A **logic** language states facts and relations from which a proof or answer is derived. A **object-oriented** language adds objects, classes, encapsulation, inheritance, and dynamic dispatch. These styles use different implementation techniques, but all have lexical structure and semantics.

### Translation concerns
The compiler must preserve lexical structure while removing irrelevant characters, enforce syntactic structure while recording grouping, and enforce semantic rules while choosing representations. These concerns map to scanner, parser, and semantic analyzer respectively.

## Worked examples
### Example 1: token classification
For `total = 42;`, the scanner may return:
- `ID(total)`, attribute `total`;
- `ASSIGN`;
- `INT`, attribute `42`;
- `SEMI`.

The parser then checks whether those tokens fit the grammar rule `statement → ID ASSIGN expression SEMI`.

### Example 2: scope resolution
In a language with block scope, a local `x` in an inner block hides an outer `x` only inside that block. A parser creates the tree; the symbol table and semantic rules determine which declaration each occurrence refers to.

### Example 3: precedence and associativity
`a + b * c` means `(a + (b*c))`; `a - b - c` normally means `(a-b)-c` because subtraction is left-associative. A grammar must encode these decisions rather than relying on a linear token list.

## Key terms & formulas
- Token: lexical unit with optional attributes.
- CFG tuple: `(V_N, V_T, P, S)`.
- Syntax: legal form; semantics: meaning.
- Scope: visibility region of a binding.
- Static/lexical scope: determined by program structure; dynamic scope: by call chain.
- Precedence controls grouping; associativity controls repeated same-level operators.

## Common mistakes
- A character is not necessarily a token, and a token is not necessarily a complete statement.
- Syntax validity does not guarantee semantic validity.
- A keyword cannot ordinarily be used as a user identifier.
- Do not assume all languages use braces, semicolons, or the same precedence rules.

## Exam prep
**Likely 2-mark questions**
1. Define token and syntax. **Hint:** token is a lexical unit; syntax is legal arrangement.
2. Distinguish syntax from semantics. **Hint:** form versus meaning.
3. What is scope? **Hint:** region where a name binding is visible.

**Long-answer questions**
1. Explain the roles of alphabet, tokens, grammar, and symbol table in compilation. **Hint:** character-to-token-to-tree-to binding.
2. Define a CFG and show a grammar for an assignment statement. **Hint:** list all four CFG components.
3. Compare imperative, functional, and logic programming styles. **Hint:** state, functions, and facts/proofs.
4. Illustrate precedence and associativity using two expressions. **Hint:** draw parse trees.
