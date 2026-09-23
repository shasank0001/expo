---
subject: atcd
unit: 5
topic: three-address-code
syllabus_ref: CSM3203 Unit-V
status: draft
---
# Three-Address Code
## Overview
Three-address code (TAC) is an intermediate instruction format in which an operation refers to at most three addresses. It represents variables, constants, temporaries, and labels in a machine-independent way. Because each arithmetic operation is simple, TAC makes syntax-directed translation, optimization, data-flow analysis, and target code generation straightforward. It is not final assembly; it is a convenient bridge.

## Explanation
### Address forms
An address can be:

- a variable name, such as `x`;
- a constant, such as `10`;
- a temporary, such as `t1`;
- a label, such as `L1`;
- an array base plus index or offset, depending on the IR.

The same address may be both a source and a destination, but a clear temporary name avoids accidental aliasing.

### Common instruction forms
- Assignment/copy: `x = y`.
- Binary arithmetic: `x = y op z`, where `op` is `+`, `-`, `*`, `/`, or a logical operator.
- Unary operation: `x = -y` or `x = not y`.
- Conditional/unconditional jump: `if x goto L`, `goto L`.
- Labels: `L:`.
- Procedure calls: `call p`, `param x`, `return y`.
- Array access: `x = y[i]`, `y[i] = z` in an extended TAC.
- Boolean short circuit: conditional jumps to a logical target, often with a flag or comparison instruction.

“At most three” is the defining restriction. A copy or jump has fewer than three address fields.

### Translation from expressions
Translate an expression recursively:

1. Translate the left operand and return its address.
2. Translate the right operand and return its address.
3. Create a fresh temporary.
4. Emit `temp = left op right`.
5. Return the temporary address.

Parentheses and the tree determine the order. The symbol table supplies the types and storage of named operands; a fresh temporary is used for each intermediate result.

### Control-flow translation
An `if` statement uses labels:

```
if x > 0 goto L1
goto L2
L1: y = 1
L2:
```

A comparison may first generate `t = x > 0`, then branch on `t`. Loops use a test label, body, and exit label. Labels and gotos make control-flow edges explicit for optimization.

### Procedure translation
A call can be represented by parameter instructions followed by `call` and a return label. A caller may save temporaries, pass arguments, receive a result, and continue after the return. The exact representation is implementation-dependent, but the symbol table must maintain parameter types and scope.

### Syntax-directed schemes
A grammar production can have semantic actions. For `E→E1+E2`, actions translate `E1`, translate `E2`, emit `t=E1+E2`, and attach `t` as the value of `E`. For declaration productions, actions allocate names; for statements, actions emit jumps and labels. This makes the parser and code generator work together.

### Utility for optimization
TAC exposes definitions, uses, temporaries, basic blocks, and control-flow edges. Constant folding, copy propagation, dead-code elimination, and common-subexpression elimination are easier when an operation is isolated in one instruction. The optimizer can also merge basic blocks and reorder independent operations.

## Worked examples
### Example 1: arithmetic
`a*b+c` becomes:

```
t1 = a * b
t2 = t1 + c
x = t2
```

`(a+b)*c` becomes `t1=a+b; t2=t1*c`.

### Example 2: conditional
`if a < b x=1 else x=2` can become:

```
if a < b goto L1
x = 2
goto L2
L1: x = 1
L2:
```

The order of the two branches is a design choice as long as labels preserve semantics.

### Example 3: logical short circuit
For `p && q`, do not evaluate `q` if `p` is false:

```
if not p goto Lfalse
t = q
if not t goto Lfalse
t = 1
goto Lend
Lfalse: t = 0
Lend:
```

This illustrates why TAC must include control flow, not just arithmetic.

### Example 4: call
`f(a, b)` may be represented as:

```
param a
param b
call f, Lret
Lret: t = result
```

The exact call form is a convention, but the parameters and return point must be unambiguous.

## Key terms & formulas
- TAC instruction: `x = y op z`.
- Address: variable, constant, temporary, or label.
- Temporary: fresh name for an intermediate result.
- `postorder` expression translation: children first.
- `L:` label and `goto L` control instruction.
- Basic block: maximal straight-line instruction sequence with one entry/exit.

## Common mistakes
- Three-address does not mean exactly three addresses.
- Do not emit an operator before its operands in recursive expression translation.
- A temporary must be fresh enough not to overwrite a live value.
- Branch labels and end markers are part of control-flow correctness.

## Exam prep
**Likely 2-mark questions**
1. Define three-address code. **Hint:** at most three addresses.
2. Give arithmetic, assignment, and jump examples. **Hint:** `t=y+z`, `x=y`, `goto L`.
3. Why use temporaries? **Hint:** store intermediate results safely.
4. What is a basic block? **Hint:** one-entry/one-exit sequence.

**Long-answer questions**
1. Translate an expression grammar into TAC. **Hint:** recursive actions and temporaries.
2. Translate an `if` statement and a loop. **Hint:** labels, gotos, joins.
3. Explain procedure-call TAC. **Hint:** parameters, call, return, result.
4. Show how TAC supports three optimizations. **Hint:** constant, copy, dead code.

**Calculation tip**
For an expression with `n` binary operators, an ordinary nonoptimized translation uses one temporary per operator, subject to the chosen reuse policy.
