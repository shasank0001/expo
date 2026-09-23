---
subject: atcd
unit: 1
topic: compiler-phases
syllabus_ref: CSM3203 Unit-I
status: draft
---
# Compiler Phases
## Overview
A compiler translates a program written in a source language into a target program that a computer can execute. Because checking every detail in one giant step is difficult, a compiler is organized into phases. Each phase receives a structured representation, performs one job, and passes an enriched representation to the next phase. This “front end–middle–back end” design makes compilers easier to build, test, reuse, and optimize.

## Explanation
### Source program and translation
A source program is a finite sequence of characters written in a source language such as C, Java, or a small teaching language. The compiler must preserve the meaning of that program while producing an equivalent target program. A compiler may stop at assembly, intermediate code, or another implementation language; the final machine-code generator is only one possible target stage.

### The standard phases
1. **Lexical analysis (scanner):** reads characters and groups them into tokens. It removes whitespace/comments, converts literals, and attaches attributes and source positions. A token example is `INT` with value `42`.
2. **Syntax analysis (parser):** checks the token sequence against the grammar and constructs a parse tree or an equivalent syntax tree. It enforces precedence and pairing of constructs.
3. **Semantic analysis:** checks meaning that syntax cannot express: declarations, scopes, types, operator compatibility, return types, and intermediate representation constraints. It may annotate the tree with types and offsets.
4. **Intermediate-code generation:** lowers the checked tree into a simple, machine-independent representation, commonly three-address code. Temporaries make data flow explicit.
5. **Code optimization:** transforms the intermediate or target representation to improve speed, size, memory use, or I/O while preserving observable behavior. Optimization can occur after intermediate generation and again before emission.
6. **Code generation (assembler/backend):** selects registers and instructions, lays out data, resolves addresses, and emits target code or assembly.

The source-to-target pipeline can be shown as:

`characters → token stream → syntax tree → annotated tree → intermediate code → optimized code → target code`

### Front end, middle, and back end
The **front end** includes lexical analysis, syntax analysis, and semantic analysis. It is mostly independent of a particular processor and can be reused for multiple targets. The **middle** represents and optimizes the program in a form convenient for translation. The **back end** performs target-dependent code generation and machine-specific optimization. This separation is one reason a compiler can support several architectures without rewriting the parser.

### Symbol table and error handling
The symbol table stores identifiers and useful facts such as kind, type, scope, storage location, and value. It is created and queried by several phases. A lexical error is an illegal character or token; a syntax error violates the grammar; a semantic error is a well-formed but meaningless or ill-typed construct. Good compilers report the earliest useful error, continue when possible, and synchronize recovery at a safe token.

### Intermediate representation and passes
A compiler may be implemented as a sequence of passes, with a pass consuming one representation and producing another. A pass can be revisited or run in parallel when dependencies permit. The intermediate representation hides target details, makes control flow and data flow visible, and makes optimization easier than direct rewriting of assembly.

### Review of compiler structure
A single-pass compiler combines translation with checking and may be small, but it has limited optimization choices. A multi-pass compiler separates analysis, synthesis, and optimization, making the design clearer. A bootstrap compiler is written in a language it can compile; for example, a compiler for language `L` may be written in `L` after an earlier version is available. Self-hosting is evidence of implementation maturity, not a requirement for every compiler.

### Control-flow example
For `if (x > 0) y = x; else y = 0;`, the parser forms an `if` node with two statement children. The backend can create a conditional branch, two basic blocks, and joins. This illustrates why a tree is more useful than a flat token list.

## Worked examples
### Example 1: trace the phases
Source: `total = price * (1 + tax);`

- Scanner: `ID(total)`, `ASSIGN`, `ID(price)`, `MUL`, `LPAREN`, `INT(1)`, `PLUS`, `ID(tax)`, `RPAREN`, `SEMI`.
- Parser: builds an expression tree with `price * (1 + tax)`.
- Semantic analysis: checks that `price` and `tax` have compatible numeric types and that `total` is assignable.
- Intermediate generator: `t1 = 1 + tax; t2 = price * t1; total = t2`.
- Optimizer may fold the constant only when the language permits it; it cannot change rounding or overflow behavior.
- Target generator maps each operation to legal instructions.

### Example 2: detect the phase of an error
`x = 1 + ;` has valid tokens but a missing operand, so the error is syntactic. `x = "text" * 2;` can be syntactically valid but is usually rejected by semantic type checking. `@` where an identifier is expected is lexical unless the grammar explicitly allows it.

### Example 3: front-end reuse
A compiler for a small language can use one lexical/syntactic front end and two back ends, one for a RISC processor and one for a virtual machine. The back ends differ in instruction selection and calling convention; the grammar does not need to be duplicated.

## Key terms & formulas
- Token: smallest meaningful lexical unit.
- AST/syntax tree: structured representation of a program.
- Symbol table: compiler database of identifiers and attributes.
- IR: intermediate representation; often three-address code.
- Front end: language analysis; middle: IR/optimization; back end: target generation.
- Translation preserves observable semantics, not necessarily instruction sequence or timing.

## Common mistakes
- Lexical analysis does not check the whole statement; parsing does.
- Syntax valid does not mean semantically valid.
- A compiler is not required to emit operating-system machine instructions directly.
- Optimization must preserve defined behavior, including exceptions, overflow, and side effects.
- The symbol table is shared state across phases; it is not just a list of variable names.

## Exam prep
**Likely 2-mark questions**
1. List the main compiler phases. **Hint:** scanner, parser, semantic analyzer, intermediate generator, optimizer, code generator.
2. Distinguish syntax and semantic errors. **Hint:** grammar violation versus meaning/type violation.
3. What is a symbol table? **Hint:** identifiers plus types, scopes, and addresses.

**Long-answer questions**
1. Draw and explain the complete compiler pipeline. **Hint:** include representations flowing between phases.
2. Explain why a compiler is split into front end and back end. **Hint:** target independence and reuse.
3. Trace `x = 1 + 2 * 3` through the phases. **Hint:** show tokens, tree, and three-address instructions.
4. Compare single-pass and multi-pass compiler organization. **Hint:** speed/simplicity versus separation and optimization.
