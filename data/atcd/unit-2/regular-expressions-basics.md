---
subject: atcd
unit: 2
topic: regular-expressions-basics
syllabus_ref: CSM3203 Unit-II
status: draft
---
# Regular Expressions Basics
## Overview
A regular expression (regex) is a compact description of a regular language. It uses symbols, operators, and grouping to say which strings are allowed without listing every string. Regular expressions are used to specify lexical tokens, search patterns, and the language of a finite automaton. They are not a general mathematical notation for arbitrary languages: their expressive power is exactly that of finite automata.

## Explanation
### Alphabet and basic symbols
For an alphabet `Σ`, the empty set `∅` denotes no strings, the symbol `a` denotes the one-string language `{a}`, and `ε` denotes the one-string language `{ε}`. A character class such as `[a-z]` denotes any one symbol in the range, while `.` often denotes any character other than a newline. A word boundary or anchor such as `^` and `$` is a tool-specific extension, not part of the basic formal language definition.

### Union
Union, written `R|S` or `R+S`, means choose either expression:

`L(R|S)=L(R)∪L(S)`.

For example, `cat|dog` describes either keyword. Parentheses are needed when union appears inside a larger concatenation or repetition.

### Concatenation
Concatenation means place one expression immediately after another. In `ab`, an `a` must be followed by a `b`; the string set is `{ab}`. Concatenation is commonly written by adjacency, while some textbooks use a dot. It is not generally commutative: `ab` and `ba` are different languages.

### Kleene star and plus
`R*` means zero or more repetitions of a string in `L(R)`. It always includes `ε` and is useful for loops. `R+` means one or more repetitions and equals `RR*`. For example, `ab*` means `ε, a, ab, abb, ...`; `a+` means `a, aa, aaa, ...` and does not include `ε`.

### Grouping and repetition
Parentheses change only the order of operations; they do not consume a character. `[A-Za-z][A-Za-z]*` means one letter followed by zero or more letters. Quantifiers such as `?` (zero or one) and `{m,n}` are common extensions that can be expanded using union, concatenation, and star.

### Language and expression equivalence
Two regexes are equivalent when they denote exactly the same set of strings. To test an expression, list representative positive and negative strings and reason about the boundary cases `ε`, one repetition, many repetitions, and the longest possible input. An expression such as `(a|b)*abb` requires the final `abb`, even though the starred prefix can be empty.

### Regular versus context-free patterns
Regexes count only finite-state information. They can express “ends in `01`” or “contains `abc`,” but not “the number of `a`s equals the number of `b`s.” For `a^n b^n`, a stack-based PDA or CFG is needed. This boundary explains why regexes are excellent for token recognition but insufficient for complete program syntax.

### Extended syntax in modern tools
Many programming libraries add lazy quantifiers, backreferences, named groups, Unicode properties, and look-around. These are powerful but may be implemented by a backtracking engine and are not necessarily regular languages. In a compiler course, use the classical operators unless a question specifically asks about a tool.

## Worked examples
### Example 1: strings ending in `a`
Over `{a,b}`, write `(a|b)*a`. The starred part chooses any prefix and the final `a` is mandatory. Test `a` (prefix `ε`), `ba` (prefix `b`), and `aba` (prefix `ab`).

### Example 2: identifiers
A typical identifier regex is `[A-Za-z_][A-Za-z0-9_]*`. The first class prevents an empty identifier and a leading digit; the second permits the remaining characters. Keywords must be recognized as a separate token class so that `if` is not accepted as an identifier.

### Example 3: binary numbers
A binary number can be `0` or a `1` followed by zero or more binary digits:

`0|1[01]*`.

The operator precedence is union lower than concatenation, so the expression is equivalent to `0|(1[01]*)`.

### Example 4: empty versus one occurrence
`a*` includes `ε`; `a+` does not. `ab*` has a mandatory `a` but an optional `b` sequence. `a?b` represents `ε, b, ab` when `?` is available.

## Key terms & formulas
- `R+S = R∪S`; `RS` is concatenation.
- `R* = ⋃_{n≥0}R^n`.
- `R+ = RR*`.
- `ε∈R*` for every regex `R`.
- `[a-z]` is a set union of individual symbols.
- Equivalent expressions satisfy `L(R)=L(S)`.

## Common mistakes
- `a*` does not mean “one or more”; it includes `ε`.
- `ab*` is not `(ab)*`; grouping changes which symbols repeat.
- `+` means union in formal regex notation, not necessarily repetition; repetition is `*` or `+` in some programming-tool syntaxes. State the notation being used.
- A regex cannot enforce arbitrary balanced counts.
- `.` in a tool may have a special meaning; do not silently use it as a literal dot.

## Exam prep
**Likely 2-mark questions**
1. Define union, concatenation, and star. **Hint:** give the corresponding language operation.
2. Write a regex for identifiers. **Hint:** first letter/underscore, then a star.
3. Write a regex for strings ending in `01`. **Hint:** arbitrary prefix followed by `01`.
4. Is `a^n b^n` regular? **Hint:** no; it needs unbounded matching memory.

**Long-answer questions**
1. Explain the meaning of `a(b|c)*d` and list three members. **Hint:** fixed boundary symbols.
2. Compare formal regular expressions with extended programming-language regex features. **Hint:** expressiveness and implementation.
3. Prove `R*` always contains `ε`. **Hint:** the zero-repetition case.
4. Design regexes for comments, decimal numbers, and reserved words. **Hint:** choose boundaries and longest match carefully.
