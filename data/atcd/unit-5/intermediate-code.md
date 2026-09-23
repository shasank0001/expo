---
subject: atcd
unit: 5
topic: intermediate-code
syllabus_ref: CSM3203 Unit-V
status: draft
---
# Intermediate Code
## Overview
Intermediate code is a simple representation placed between the source program and target machine code. It exposes arithmetic operations, variables, temporaries, and control flow while hiding processor-specific details. A compiler can analyze and optimize this form once and then generate code for several targets. Three-address code, postfix notation, and syntax trees are common intermediate representations.

## Explanation
### Need for an intermediate form
Directly translating source constructs to a particular processor mixes language analysis with instruction selection. An intermediate form separates those concerns. The front end produces a target-independent program; the back end maps its operations to registers, memory, branches, and machine instructions. This supports portability, testing, and optimization.

### Three-address instructions
A typical three-address instruction has the form

`x = y op z`.

The operands may be variables, constants, labels, or temporaries. Related forms include `x=y`, `x=y+z`, `if x goto L`, `goto L`, `L:`, parameter passing, array access, and procedure return. Each operation has a simple meaning that is easy to analyze.

### Postfix and prefix forms
In postfix notation, an operator follows its operands:

`a+b*c → a b c * +`.

A stack evaluates the expression without parentheses. Prefix places the operator before its operands: `+ a * b c`. These forms are compact but make control flow and named variables less explicit unless extended.

### Syntax trees and DAGs
A syntax tree represents expression structure. A directed acyclic graph (DAG) can share repeated subexpressions: two uses of `a+b` can point to one node. DAGs expose common subexpressions and reduce code size, but care is needed with assignments and side effects.

### Control-flow representation
An intermediate program can use labels and gotos, basic blocks, or a structured control-flow graph. Labels identify targets; gotos transfer control. A basic block has one entry and one exit. The control-flow graph is useful for reachability, liveness, and loop analysis.

### Advantages
Intermediate code makes optimization easier because expressions and uses are explicit. It supports multiple back ends, machine-independent transformations, and a simple symbolic execution model. It also gives a useful intermediate debugging view. A disadvantage is that a very low-level or poorly designed IR can lose useful information, while a very high-level IR may not expose enough for target optimization.

### Selection criteria
A good IR is expressive enough for all language constructs, simple enough for analysis, unambiguous about types and side effects, and easy to lower to a target. Designers balance a small instruction set against preserving source-level information needed for optimization.

## Worked examples
### Example 1: expression IR
For `x = (a+b)*c + d`, three-address code can be:

```
t1 = a + b
t2 = t1 * c
x = t2 + d
```

The same three-address program can be lowered to a RISC processor, a stack VM, or another backend.

### Example 2: postfix evaluation
For `(a+b)*(c+d)`:

`a b + c d + *`.

A stack machine pushes `a`, `b`, adds, pushes `c`, `d`, adds, then multiplies the two results.

### Example 3: DAG sharing
If both `x=a+b` and `y=a+b` appear without intervening changes, one computation node can be shared:

`t=a+b; x=t; y=t`.

This is valid only when evaluation order and side effects permit it.

### Example 4: control-flow IR
A structured `while` can be lowered to labels:

```
L1:
  if not condition goto L2
  body
  goto L1
L2:
```

The intermediate form makes the loop and its exit explicit.

## Key terms & formulas
- IR: `source → IR → target`.
- Three-address form: at most three address fields.
- Postfix: `operands operator`.
- DAG: acyclic sharing of expression nodes.
- Basic block: one-entry/one-exit instruction sequence.
- Machine independence: no processor register or address-mode assumptions.

## Common mistakes
- Intermediate code is not final machine code.
- `t = a + b` has three addresses, but `x=y` is still a valid three-address instruction.
- Postfix changes representation, not the expression’s value or evaluation order.
- Sharing a DAG node can be unsafe when an operand is assigned between uses.

## Exam prep
**Likely 2-mark questions**
1. Define intermediate code. **Hint:** target-independent representation between source and target.
2. Name two IR forms. **Hint:** TAC, postfix, syntax tree.
3. Give one use of an IR. **Hint:** optimization or portability.
4. What is a basic block? **Hint:** one entry and one exit.

**Long-answer questions**
1. Compare three-address, postfix, and syntax-tree IRs. **Hint:** structure, analysis, and control flow.
2. Explain why an IR supports multiple back ends. **Hint:** target-independent lowering.
3. Show an IR for an expression and a loop. **Hint:** temporaries, labels, gotos.
4. Discuss the trade-offs in choosing an IR. **Hint:** expressiveness versus simplicity.

**Model answer tip**
Always state that an IR must preserve source semantics and make data/control flow visible; an expression example alone is not a complete comparison.
