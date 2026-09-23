---
subject: atcd
unit: 3
topic: top-down-parser-types
syllabus_ref: CSM3203 Unit-III
status: draft
---
# Top-Down Parser Types
## Overview
Top-down parsers are classified mainly by how they choose a production. Recursive-descent parsers use procedures, backtracking parsers try alternatives and undo them, and predictive parsers use a table or equivalent logic to choose directly from lookahead. LL(1) is the important conflict-free predictive class in the syllabus. Understanding the types helps select a practical parser and diagnose grammar problems.

## Explanation
### Recursive-descent parser
A recursive-descent parser represents each nonterminal as a procedure. The procedure examines lookahead and executes the code corresponding to a production. It may be **predictive** when its hand-written decisions are equivalent to an LL(1) table, or **backtracking** when it tries a branch and restores the input position after failure. It is readable and easy to debug for small languages.

### Backtracking parser
A backtracking parser attempts a production, recursively parses its right side, and returns to the previous choice if the input does not match. It can handle more grammars than a one-token predictive parser, but repeated trials can cause exponential time. It also makes error reporting and action ordering harder because speculative parses may execute actions that must later be undone.

### Predictive parser
A predictive parser uses a table `M[A,a]`, where `A` is a nonterminal and `a` the current lookahead terminal. The table entry gives the production to use, or an error. A table-based predictive parser is equivalent to a carefully written LL(1) recursive-descent parser, but it is easier to generate and inspect.

### LL(1) grammar
An LL(1) grammar can be parsed with one lookahead symbol without conflicts. The `L` means input is read left to right; the first `L` means the derivation is leftmost; `1` means one token of lookahead. Conditions include no conflicts in the parsing table, no harmful left recursion for the selected implementation, and correct FIRST/FOLLOW calculations.

### LL(k) and lookahead
LL(k) permits `k` tokens of lookahead and can parse a larger class than LL(1), but tables and implementations become larger. A grammar may be LL(2) because two-token lookahead distinguishes alternatives that share a first token. LL(1) is the usual classroom and parser-generator baseline.

### Parsing-table conflicts
Two types are common:

- **Multiple-production conflict:** two alternatives have overlapping FIRST/FOLLOW table entries.
- **Nullable conflict:** a nullable production competes with another production on a lookahead in FOLLOW.

A conflict means the grammar needs rewriting, more lookahead, or a deliberate parser-generator resolution. It is not valid to choose an arbitrary entry without understanding the intended language.

### Parser generators
Yacc/Bison and similar tools commonly generate LALR parsers, while ANTLR can generate LL(*) and other adaptive parsers. The generator does not remove the need to specify precedence, associativity, and error productions.

## Worked examples
### Example 1: predictive choice
Grammar `S→A|b`, `A→a`. At lookahead `a`, table `M[S,a]=S→A`; at lookahead `b`, `M[S,b]=S→b`. There is no choice, so the parser is predictive.

### Example 2: common-prefix conflict
If `E→E+T|E-T` and the parser is supposed to choose by one-token lookahead, both alternatives begin with `E`; a naive top-down table cannot choose based only on the current token. Separate the grammar by operator levels or use a different parser.

### Example 3: backtracking
For `S→A|BC`, `A→a|ab`, `B→b`, `C→c`, a backtracking parser may first try `A→a`, then discover that the remaining input begins with `b` rather than the required continuation, and retry `A→ab`. A predictive grammar would be redesigned to avoid the unnecessary trial.

### Example 4: nullable FOLLOW entry
If `A→aB|ε` and `B` derives `b`, then `A→aB` is selected on `a`; if `A` can end a statement followed by `;`, `A→ε` is selected on `;`. The FOLLOW set, not FIRST, supplies the second entry.

## Key terms & formulas
- LL(1): left-to-right, leftmost, one-symbol lookahead.
- `M[A,a]`: predictive parsing-table cell.
- Conflict: more than one production/action in a cell.
- Backtracking: save input position, try, restore on failure.
- Parser generator: software that reads a grammar/specification and emits tables or recognizer code.

## Common mistakes
- Recursive descent is not automatically LL(1); it may backtrack.
- `LL(1)` does not mean one token of total input; it means one lookahead decision.
- A table conflict is a grammar/lookahead issue, not merely a coding bug.
- Do not call a bottom-up LALR table an LL(1) table.

## Exam prep
**Likely 2-mark questions**
1. Compare recursive-descent and predictive parsing. **Hint:** procedures versus table/lookahead.
2. What is backtracking? **Hint:** try and undo.
3. What does LL(1) mean? **Hint:** three L/1 properties.
4. Name one parser-generator conflict. **Hint:** multiple alternatives or nullable overlap.

**Long-answer questions**
1. Explain the three top-down parser types with diagrams. **Hint:** procedure, trial, table.
2. Determine whether a grammar is LL(1) using FIRST/FOLLOW. **Hint:** list all table cells.
3. Discuss trade-offs between LL(1), LL(k), and backtracking. **Hint:** grammar coverage, table size, time.
4. Explain how a generated parser handles syntax errors. **Hint:** error entries and recovery actions.
