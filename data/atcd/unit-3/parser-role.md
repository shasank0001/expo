---
subject: atcd
unit: 3
topic: parser-role
syllabus_ref: CSM3203 Unit-III
status: draft
---
# Role of the Parser
## Overview
The parser is the syntax-analysis phase of a compiler. It receives tokens from the lexical analyzer, checks whether their order follows the language grammar, and produces a parse tree or syntax tree for later phases. It is the bridge between token recognition and meaning/code generation: it shows which constructs are nested, where statements begin and end, and which production supplied each piece of structure.

## Explanation
### Input and output
The parser receives a sequence of token classes and attributes, not a raw character stream. It may need lookahead to choose a production or decide whether an expression is complete. Its output can be a full parse tree, a compact abstract syntax tree, actions executed during parsing, or an annotated tree for semantic analysis.

### Grammar checking
The parser applies productions from the language grammar. If the next token cannot be predicted from the current nonterminal and lookahead, it reports a syntax error. A successful parse establishes membership in the grammar language but does not by itself check types, declarations, or runtime values.

### Parse structure for a compiler
For `if x > 0 then y=1 else y=0;`, the parser can build:

- an `if-statement` node;
- a condition subtree for `x>0`;
- a then subtree and an else subtree.

This structure allows semantic analysis to mark the condition as Boolean, generate conditional jumps, and calculate the type of each assignment. A flat token list would lose the nesting.

### Error detection and recovery
A good parser detects an error as early as possible and reports a useful line/column and expected token. Recovery may discard tokens until a synchronization point such as `;`, `end`, or a statement keyword. Panic-mode recovery is simple; error productions and local repair can be more precise but require careful grammar design.

### Predictive and bottom-up choices
A top-down parser expands the start symbol and predicts productions from the left. A bottom-up parser shifts input tokens and reduces patterns. Both use grammar knowledge, but bottom-up parsers can usually handle more languages and left recursion. The syllabus covers top-down parsing in Part 1 and bottom-up/LR parsing in Part 2.

### Semantic actions
The parser can execute syntax-directed actions when a production is recognized. Actions may build an AST, annotate types, check symbol-table entries, or emit intermediate code. Actions must obey the evaluation order required by the language; a tree-building action should normally run after the children are available.

### Parser interface
A practical interface includes `currentToken`, `advance()`, and error routines. The parser should not depend on how the scanner stored whitespace or comments. This separation allows a generated scanner and parser to be tested independently and replaced independently.

## Worked examples
### Example 1: token validation
Input tokens `ID(x) ASSIGN INT(1) SEMI` match a rule such as `statement→ID ASSIGN expression SEMI`. If the token stream is `INT(1) SEMI`, the parser reports an expected identifier at the start.

### Example 2: nested structure
For `begin if p then x:=1 end`, the parser groups the `if` inside the block. Semantic analysis can then check that `p` is Boolean and that `x` is assignable. The same tokens with a different grammar attachment could represent a different language, so the tree matters.

### Example 3: error recovery
On `x := 1 + ; y := 2`, the parser reports a missing operand and synchronizes at `;` or the next identifier, allowing a later statement to be checked. It must not silently treat the semicolon as an operand.

### Example 4: syntax versus semantics
`x := 1 + 2;` is syntactically valid. `x := 1 + "two";` may also be syntactically valid but is rejected by semantic type checking if strings cannot be added to integers.

## Key terms & formulas
- Parser input: token stream; output: parse/AST plus diagnostics.
- Lookahead: tokens inspected without consuming them.
- Panic mode: discard tokens until a synchronization point.
- Syntax error: token sequence not derivable by the grammar.
- Semantic error: syntactically valid but ill-typed or ill-scoped.

## Common mistakes
- The parser does not receive spaces, comments, or raw characters from the scanner.
- A successful parse is not proof that variable names are declared or types match.
- Error recovery must not consume the synchronization token if the caller expects it.
- Parsing and semantic analysis are related but separate phases.

## Exam prep
**Likely 2-mark questions**
1. State the role of a parser. **Hint:** token sequence to structured syntax.
2. What are parser input and output? **Hint:** tokens; tree/annotated representation.
3. Give one syntax error and one semantic error. **Hint:** missing semicolon versus undeclared variable.
4. What is panic-mode recovery? **Hint:** skip to synchronization token.

**Long-answer questions**
1. Trace a statement through the parser and semantic analyzer. **Hint:** tokenization, tree, type check.
2. Explain why parse structure is needed for code generation. **Hint:** nesting and control-flow meaning.
3. Describe two error-recovery strategies. **Hint:** panic mode, local repair, or error productions.
4. Distinguish top-down and bottom-up parser behavior. **Hint:** expansion versus reduction.
