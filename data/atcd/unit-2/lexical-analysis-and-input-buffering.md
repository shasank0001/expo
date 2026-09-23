---
subject: atcd
unit: 2
topic: lexical-analysis-and-input-buffering
syllabus_ref: CSM3203 Unit-II
status: draft
---
# Lexical Analysis and Input Buffering
## Overview
Lexical analysis is the compiler’s source-to-token phase. Its scanner reads characters, skips separators, matches the longest legal token pattern, converts literal text to values, and reports illegal input. Input buffering makes this practical: source text is read in blocks, and a small lookahead window keeps scanner decisions correct when a token crosses a buffer boundary. The output is a token stream for the parser, not a parse tree.

## Explanation
### Role of the lexical analyzer
The scanner recognizes the smallest meaningful units of a programming language. Typical token classes are identifiers, keywords, integer and real constants, operators, punctuation, and comments. It may maintain a symbol-table entry for an identifier and attach source line/column information for diagnostics. It does not decide whether a complete statement follows the grammar; that is the parser’s job.

### Buffering problem
A compiler cannot assume that the entire source file fits in memory. A buffer is a fixed-size array filled from an input stream. If a token begins near the end of a buffer, the scanner needs characters from the next buffer to decide whether the token continues. A **lookahead buffer** retains unread characters, while a **lookback buffer** can preserve recently consumed characters for context and error reporting.

### Buffer-refill strategies
A common strategy refills the buffer when the forward pointer reaches its end. A more efficient strategy refills when only a small number of unread characters remain, often by shifting the remaining characters to the beginning and appending new input. The exact threshold is an implementation choice, but it must never lose an unread part of a token.

### Character streams and delimiters
The scanner often reads a continuous character stream, removes whitespace, handles line comments beginning with `//`, and handles block comments such as `/* ... */`. A comment terminator split across two buffers must be recognized correctly. Escape sequences and string literals can also cross a boundary.

### Token specification and recognition
A token specification is a mapping from regular patterns to token classes and actions. A scanner repeatedly:

1. finds the next nonseparator position;
2. tries the enabled patterns at that position;
3. selects the longest match (with a stated tie rule);
4. executes the associated action; and
5. returns `(tokenClass, attribute, position)`.

A failed match produces a lexical error. The scanner should not silently skip an unknown character because that can hide a source error.

### Interaction with the parser
The parser consumes tokens through a common interface. It can ask for the next token, inspect its class and attribute, and report the position of a syntax error. Keeping the scanner interface abstract makes it possible to generate scanners and parsers independently.

### Error recovery
The scanner can skip an unexpected character, report it, and continue. A parser can discard tokens until a synchronization token. Recovery policies differ because a character-level mistake can create many invalid tokens, while a parser error may be localized to one statement.

## Worked examples
### Example 1: token stream
For `if x>=10 { total=total+x; }`, return `IF`, `ID(x)`, `RELOP(>=)`, `INT(10)`, `LBRACE`, `ID(total)`, `ASSIGN`, `ID(total)`, `PLUS`, `ID(x)`, `SEMI`, `RBRACE`. Spaces and line breaks disappear, but their positions can be retained for diagnostics.

### Example 2: boundary split
Suppose a buffer ends after `co` and the next buffer starts with `mment ...`. A scanner that only examines the current buffer might report an identifier `co`; a lookahead buffer keeps the `m` available so the comment rule can match `comment`. The refill logic must preserve unread characters.

### Example 3: longest match
At input `>=`, a rule for `>` alone and a rule for `>=` both match a prefix. The longest-match rule chooses `>=`. If a keyword rule and identifier rule match `if`, the keyword rule wins when its length is at least as long and its priority is higher.

## Key terms & formulas
- Scanner output: `(token type, attribute, source position)`.
- Longest match: choose the pattern with greatest matched length; ties use rule priority.
- Forward pointer: next unread character; lookahead buffer preserves unread data.
- Token stream: ordered sequence consumed by the parser.
- Lexical error: no legal token starts at the current position.

## Common mistakes
- The scanner checks individual tokens, not the grammar of a whole statement.
- Refilling a buffer must not discard characters that are part of an unfinished token.
- A comment is not a token in most languages; it is discarded after recognition.
- First-match is not always longest-match; the specification must state the rule.

## Exam prep
**Likely 2-mark questions**
1. State the role of a lexical analyzer. **Hint:** characters to tokens.
2. Why is input buffering needed? **Hint:** large source files and token-boundary lookahead.
3. What is longest match? **Hint:** maximum token length wins.
4. Give three token examples. **Hint:** identifier, constant, operator.

**Long-answer questions**
1. Explain buffer refill with a token crossing a boundary. **Hint:** retain unread characters.
2. Describe the scanner’s token-recognition loop. **Hint:** skip, match, choose, act, return.
3. Distinguish lexical and syntax error recovery. **Hint:** character/token versus grammar synchronization.
4. Design a token specification for identifiers, integers, and comments. **Hint:** patterns, classes, priorities, and actions.
