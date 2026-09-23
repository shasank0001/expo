---
subject: atcd
unit: 2
topic: regex-construction-from-description
syllabus_ref: CSM3203 Unit-II
status: draft
---
# Regex Construction from Description
## Overview
Constructing a regular expression starts by turning a natural-language requirement into precise choices, repetitions, and boundaries. A good expression is not the one with the fewest symbols; it is the one whose accepted strings exactly match the specification. Systematic decomposition makes lexical tokens and machine-to-regex problems much easier to check.

## Explanation
### Step 1: identify the alphabet and boundaries
Write down every symbol or character class that may occur. Decide whether the string may be empty, whether a token needs delimiters, and whether a particular symbol is mandatory. For lexical analysis, boundaries are often supplied by the scanner rather than represented by a formal regex.

### Step 2: split into alternatives
Use union for “or” choices. If a language has two endings, such as `ab` or `ba`, write `(ab|ba)`. Keep alternatives at the same level so a later parser or evaluator can see the choice.

### Step 3: concatenate mandatory parts
Place required pieces next to each other in order. For a two-character prefix `ab`, write `ab`; for a word beginning with a letter and then digits, write `[A-Za-z][0-9]*`.

### Step 4: express repetition
Use `R*` for zero or more and `R+` (or `RR*`) for one or more. Use `R?` for optional. When a group repeats, parenthesize it: `(ab)*`, not `ab*` if the whole `ab` is intended to repeat.

### Step 5: handle character classes and escapes
`[abc]` is one symbol from a set, while `abc` is a sequence. Escape metacharacters when they are literals. A hyphen in a class denotes a range only in the usual convention; a backslash can have tool-specific meaning.

### Step 6: test boundaries
Check the empty string, shortest valid string, longest permitted repetition in a small test, one missing required symbol, and one illegal character. A regex for “at least two letters” could be `[A-Za-z]{2,}` or `[A-Za-z][A-Za-z][A-Za-z]*`; it must reject a one-letter string.

### Common construction patterns
- `a*`: zero or more `a`.
- `a+b*`: one or more `a`, then zero or more `b`.
- `(a|b)*abb`: arbitrary prefix then `abb`.
- `[0-9]+(\.[0-9]+)?`: one or more digits with an optional fractional part.
- `0|1[01]*`: binary numbers without a leading zero except for zero itself.

### Match longest token
In a lexer, several token regexes can match a prefix. The scanner normally chooses the longest overall match; if lengths tie, an earlier rule or explicit priority may win. This is a selection rule for the token specification, not a change to the language of each individual regex.

## Worked examples
### Example 1: identifier
“An identifier begins with a letter or underscore and continues with letters, digits, or underscores.”

`[A-Za-z_][A-Za-z0-9_]*`

The first character class is mandatory; the starred class permits the rest. A keyword such as `while` is lexically matched but assigned a keyword token by the scanner.

### Example 2: even-length binary string
`((00|11)*)` can be written `(00|11)*`; it requires complete pairs, so `ε, 00, 1111, ...` are accepted and `0` is not. If the phrase means an even number of bits rather than a particular pairing, use a parity DFA or construct a regex with two parity states; description clarity matters.

### Example 3: optional decimal fraction
`[0-9]+(\.[0-9]+)?` accepts `12`, `12.30`, and `7`, but not `.5` or `12.`. If leading signs are allowed, add `[+-]?`; if a sign is mandatory, use `[+-]`.

### Example 4: C-style comment
A simplified non-newline comment can be `/\*([^*]|\*+[^*/])*\*+/`; a practical expression needs careful handling of the delimiter and tool syntax. The key method is to express “any character that is not a delimiter, or a delimiter that is not the closing pair” before the final close.

## Key terms & formulas
- Union: choice, `R|S`.
- Concatenation: order, `RS`.
- Star: zero or more, `R*`.
- One-or-more: `R+ = RR*`.
- A character class is a finite union of one-symbol languages.
- Longest match chooses the maximum token length among applicable rules.

## Common mistakes
- `(ab)*` and `ab*` are different.
- A required prefix cannot be represented by a star unless zero repetitions are genuinely allowed.
- Do not put `.*` where a restricted alphabet is required.
- Test invalid strings, not only examples that should be accepted.
- Regex metacharacters may need escaping.

## Exam prep
**Likely 2-mark questions**
1. Explain how to build a regex from a language description. **Hint:** split, group, repeat, test.
2. Write a regex for identifiers. **Hint:** first class plus star.
3. Write a regex for strings with at least one digit. **Hint:** arbitrary prefix/suffix around `[0-9]+`.
4. What is longest-match? **Hint:** maximum token length wins.

**Long-answer questions**
1. Construct and verify regexes for four specified lexical categories. **Hint:** show valid and invalid tests.
2. Derive a regex for words beginning and ending with specified letters. **Hint:** use concatenation and classes.
3. Explain why grouping is essential. **Hint:** compare `ab*` with `(ab)*`.
4. Convert a verbose description into a regular grammar. **Hint:** nonterminal for repeated part and one for mandatory part.
