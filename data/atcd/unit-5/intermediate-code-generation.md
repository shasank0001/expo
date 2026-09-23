---
subject: atcd
unit: 5
topic: intermediate-code-generation
syllabus_ref: CSM3203 Unit-V
status: draft
---
# Intermediate Code Generation
## Overview
Intermediate code generation lowers an annotated syntax tree into a target-independent program, most often three-address code. The generator uses the symbol table to find names, types, scopes, and storage locations; it creates temporaries for values; and it emits labels and jumps for control flow. The output is deliberately simple so that optimization and several back ends can operate on it.

## Explanation
### Input and output
The input is a checked and annotated syntax tree, together with a symbol table and source-language rules. The output is an intermediate program containing assignments, arithmetic, comparisons, labels, gotos, calls, returns, and declarations. Semantic analysis has already checked that the tree is well-typed and that names are declared.

### Symbol table information
For every identifier, the generator may need its type, memory class, offset, scope, and whether it is a parameter or global. A local variable can be assigned a stack offset; a global has a static label; a temporary gets a fresh name. The generator should not invent storage that conflicts with the language’s visibility or lifetime rules.

### Declarations
A declaration action allocates or labels storage. For `var x: integer;`, the symbol table records `x` and its type; the IR may emit `x = 0` only if the language specifies initialization. A function declaration records an entry point and parameter information. Uninitialized values must not be assumed to be zero unless the language says so.

### Expression generation
For a binary operator, generate code for the left and right children, allocate a fresh temporary, and emit the operation. The syntax-tree traversal is usually postorder. A logical short-circuit operator uses conditional control flow; an ordinary arithmetic operator uses one instruction. Type conversions are inserted before the operation when required.

### Assignment generation
For `x = y`, look up the address of `x` and `y` in the symbol table. For an indexed or field assignment, generate the address calculation first. If the expression has a value, preserve the assigned or computed value according to the language definition. An assignment to a variable and a declaration are different actions.

### Selection statements
For `if E then S1 else S2`, generate:

1. code for `E`;
2. a conditional branch to `Ltrue`;
3. code for `S2`;
4. `goto Lend`;
5. `Ltrue:` and code for `S1`;
6. `Lend:`.

Branch order may be swapped, but labels and the empty alternative must be handled. Constant conditions can be folded only when evaluation has no required side effects.

### Iteration statements
For `while E do S`, use a test label, a body, and an exit label. For a `repeat` loop, the test label occurs after the body. For a `for` loop, generate initialization, condition testing, increment, and exit edges. Scope and variable lifetime around a loop must remain correct.

### Procedure calls
A call translation may use explicit parameter instructions, a call instruction, and a return label. Save live values around the call according to the calling convention. A function result is assigned to a temporary or caller variable. Recursive calls require stack-frame management in the back end.

### Boolean values and short circuit
A Boolean expression can be represented by a temporary containing 0/1 or by control-flow labels. Short-circuit `&&` and `||` must not evaluate the right operand when the result is already determined. This is a semantic requirement, not an optimization.

### Arrays and structures
An array reference requires a base address, index, element size, and bounds semantics. Bounds checking may emit a branch to an error routine. Structure fields use offsets computed by the symbol table. These examples show why the IR should preserve enough type and layout information.

### Interface with optimization
The generator should produce explicit temporaries and control-flow edges. An optimizer can then build a control-flow graph, identify basic blocks, perform data-flow analysis, and rewrite instructions. If the generator hides control flow inside opaque procedures, later optimization is harder.

## Worked examples
### Example 1: simple declaration and assignment
For:

```
var x: integer;
begin x = 4; end
```

the symbol table records `x`; the IR may be `x = 4`. No `x=0` instruction is emitted unless initialization is specified.

### Example 2: if statement
For `if x>0 then y=1 else y=2`:

```
if x > 0 goto L1
y = 2
goto L2
L1: y = 1
L2:
```

The labels make both incoming and outgoing control-flow edges visible.

### Example 3: while loop
For `while x<10 do x=x+1`:

```
L1:
if not (x < 10) goto L2
t1 = x + 1
x = t1
goto L1
L2:
```

The back edge forms the loop; the exit edge leaves it.

### Example 4: short circuit
For `p && q`, branch on `p` before translating/evaluating `q`; use separate labels to set the result to 0 or 1. A straight-line `t=p & q` is correct only for a non-short-circuit language.

## Key terms & formulas
- Input: annotated AST + symbol table; output: IR.
- Fresh temporary: one new name per computed intermediate value.
- Basic block: one entry/one exit.
- Control-flow edge: fall-through, true branch, false branch, or jump.
- Calling convention: rules for parameter passing, result return, and saved values.
- Postorder: children before parents.

## Common mistakes
- Semantic analysis must precede reliable code generation; do not ignore type/scope attributes.
- Do not emit an uninitialized zero unless the language defines it.
- Put the loop test in the correct place for `while`, `repeat`, and `for`.
- Translate short-circuit operators with control flow.
- Do not allocate a temporary before its value’s operands are available.

## Exam prep
**Likely 2-mark questions**
1. State the purpose of intermediate-code generation. **Hint:** AST to target-independent code.
2. Name two symbol-table attributes used. **Hint:** type, offset, scope, label.
3. How are if-statements represented? **Hint:** labels and gotos.
4. What is a calling convention? **Hint:** parameter/result/saved-value rules.

**Long-answer questions**
1. Generate TAC for an if/else statement. **Hint:** condition, branch, bodies, join.
2. Generate TAC for while and for loops. **Hint:** initialization, test, body, increment.
3. Explain procedure-call generation. **Hint:** parameters, call, return, temporaries.
4. Discuss arrays/structures and type information. **Hint:** base, offset, size, bounds.
5. Explain why explicit temporaries help optimization. **Hint:** definitions, uses, liveness, basic blocks.

**Exam habit**
Draw the source tree or a control-flow sketch before writing instructions. Then check that every branch has a target and every label is used consistently.
