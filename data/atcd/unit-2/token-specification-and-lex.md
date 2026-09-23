---
subject: atcd
unit: 2
topic: token-specification-and-lex
syllabus_ref: CSM3203 Unit-II
status: draft
---
# Token Specification and LEX
## Overview
A token specification tells a lexical analyzer the legal spellings of each token, its category, and the action to perform after a match. Regular expressions are the usual spelling language. LEX (and its POSIX-compatible counterpart Flex) reads these specifications and generates scanner code, reducing hand-written character handling. The specification is part of the language definition: an incorrect pattern can cause valid programs to be rejected or invalid text to be accepted.

## Explanation
### Token specification components
A specification normally contains:

- declarations of literal strings and character classes;
- a set of regular-expression rules;
- an optional start condition for contexts such as comments or strings;
- auxiliary functions for values and actions;
- user code copied into the generated scanner.

Each rule associates a pattern with a token name. The generated DFA/NFA recognizes the pattern; the action supplies semantic information, such as converting matched digits to an integer.

### Regular patterns for common tokens
For a small language:

- identifier: `[A-Za-z][A-Za-z0-9_]*`;
- unsigned integer: `[0-9]+`;
- assignment: `=`;
- relational operators: `<=|>=|==|!=|<|>`;
- whitespace: `[ \t\n]+`.

Keywords such as `if` and `while` can be literal rules. A practical scanner uses longest match and then rule order or an explicit priority to distinguish a keyword from an identifier.

### Longest match and rule priority
At a position, all active rules are considered. The rule producing the greatest match length is selected. If two rules match the same length, the earlier rule (or the tool’s stated priority convention) wins. This is how `>=` is preferred to `>`, and how `if` can be a keyword rather than an identifier. A scanner should not stop at a shorter prefix merely because its rule appears first.

### Regular actions
A regular action copies the matched text with `yytext`/`yylex` conventions and returns a token. Example pseudocode for an integer rule is:

```
[0-9]+ {
    yylval.number = convert_to_integer(yytext);
    return NUM;
}
```

Identifier actions can insert or look up a symbol-table entry. Whitespace and comments perform no token return.

### Start conditions
LEX start conditions let the scanner recognize different token sets in different contexts. After seeing `"`, the scanner can enter a `STRING` condition where quotes and escapes are handled; after the closing quote it returns to `INITIAL`. This is a convenient way to describe lexical modes without confusing the grammar with ordinary tokens.

### Generated scanner structure
A generated scanner generally contains transition tables or code for the DFA, a start-condition selector, the action switch, and helper routines. The parser calls the scanner repeatedly. The scanner’s output is stable even if the implementation changes, which is why Lex and Yacc are often used together.

### Token versus pattern
A pattern is a regular expression over characters. A token is the semantic class returned for a matched pattern, plus attributes. The pattern `42` is not itself the semantic token `INT(42)` until the action assigns the value and returns the class.

## Worked examples
### Example 1: longest match
At input `>=`, the rule `>=` matches two characters and `>` matches one. The scanner returns `GE`. At input `=`, only the assignment rule matches. At `==`, the equality rule wins over two assignment prefixes.

### Example 2: keyword versus identifier
Both `while` and the identifier pattern match the text `while`. If the keyword rule is placed before the identifier rule and both have the same length, the keyword rule returns `WHILE`. If the language permits a keyword as an identifier, the priority policy must be changed deliberately.

### Example 3: numeric action
For source `x=007`, the text match is `007`. The action can return `INT` and an integer value `7`; the exact source spelling can be retained separately if diagnostics need it. The parser sees a token attribute, not the raw characters.

### Example 4: comments
A start condition can skip `/* ... */` without exposing comment characters as tokens. The scanner must recognize the closing delimiter even if it crosses an input buffer. A malformed unterminated comment produces a lexical error.

## Key terms & formulas
- Pattern: regular expression describing token spelling.
- Longest match: maximize matched length, then apply priority.
- Start condition: scanner context controlling active rules.
- `yytext`: common name for matched text in Lex-like tools.
- Token `(type, semantic-value)`.

## Common mistakes
- A rule’s order alone does not justify stopping at a short prefix; longest match comes first.
- Keywords and identifiers can have identical spelling, so priorities must be explicit.
- `yytext` is text; converting it to a value is the action’s responsibility.
- A scanner specification should not contain grammar rules for complete statements.

## Exam prep
**Likely 2-mark questions**
1. Define a token specification. **Hint:** pattern-to-token mapping and action.
2. Explain longest-match selection. **Hint:** maximum length, then priority.
3. What is LEX? **Hint:** scanner generator from regular specifications.
4. Give patterns for an identifier and integer. **Hint:** character classes and `+`.

**Long-answer questions**
1. Write a small LEX specification for identifiers, numbers, assignment, and comments. **Hint:** definitions, rules, actions, and tie handling.
2. Explain how keyword rules override identifier rules. **Hint:** equal-length priority.
3. Describe start conditions for strings or comments. **Hint:** enter and leave scanner contexts.
4. Explain the interaction between generated scanner and parser. **Hint:** `yylex` returns tokens to the parser.
