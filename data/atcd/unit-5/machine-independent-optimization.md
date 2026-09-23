---
subject: atcd
unit: 5
topic: machine-independent-optimization
syllabus_ref: CSM3203 Unit-V
status: draft
---
# Machine-Independent Code Optimization
## Overview
Machine-independent code optimization improves a program using language-level facts rather than a particular processor’s registers or instruction set. It works on a control-flow graph or three-address code, finds redundant calculations and ineffective control flow, and applies transformations that are valid for any legal target. The key requirement is behavior preservation: outputs, errors, side effects, and termination must remain the same.

## Explanation
### Basic blocks and CFG
A basic block is a maximal straight-line sequence with one entry and one exit. A control-flow graph has basic blocks as nodes and possible transfers as edges. Optimizations first identify leaders, build the graph, and compute reachability. A block with no path to program exit may be unreachable; a block with no predecessor may be dead unless it is the entry.

### Local optimization
Local optimization works within one basic block and examines a short window of instructions. Examples include constant folding, copy propagation, algebraic simplification, common-subexpression elimination within the block, and deleting a jump to the next instruction. Local analysis is fast but cannot use facts across blocks.

### Global optimization
Global optimization uses data-flow facts across blocks. A definition reaches a use if it is the only possible reaching definition along every path, considering kills. A variable is live at a point if its current value may be used before being overwritten. Live-variable analysis, available-expression analysis, reaching definitions, and constant propagation are standard global analyses.

### Constant folding and propagation
Constant folding replaces an operation whose operands are known constants:

`t=2+3 → t=5`.

Constant propagation copies a known value to uses:

`x=5; y=x → y=5`.

A constant expression must fit the declared type and must not change defined overflow, exception, or floating-point behavior. Unknown external or volatile values are not constants.

### Copy propagation
When a variable is assigned only from another stable value, uses of the copy can be replaced by the original. The analysis tracks whether the source changes. A chain `a=b; b=c` can become `a=c` only if reaching definitions permit it; otherwise a later write to `b` matters.

### Common-subexpression elimination
If the same expression is computed from unchanged operands and has no intervening side effects, later identical computations can reuse the earlier temporary. This is often implemented on expression trees or DAGs and is safer for pure arithmetic than for calls, memory reads, or assignments. Constant and copy propagation often creates extra opportunities.

### Dead-code and dead-store elimination
A computation whose result is never used and has no side effects can be deleted. A store to a variable that is dead afterward can sometimes be removed, but only if the language does not expose the store through aliases, volatile access, exceptions, or observable memory. “Unused” is not sufficient by itself.

### Loop optimization
Loop-invariant code motion moves a calculation out of a loop when its operands are unchanged. Induction-variable analysis identifies variables that increase by a constant; strength reduction replaces expensive multiplications with additions. Unrolling duplicates a small loop body, trading code size for fewer branch overheads. Loop transformations require careful control- and data-flow checks.

### Control-flow optimization
Remove unreachable blocks, merge blocks with a single predecessor and no conflict, eliminate redundant gotos, and reorder blocks when safe. Avoid duplicating a block with side effects merely to eliminate a branch. Infinite loops and termination behavior must be preserved.

### Dependence and side effects
An expression can be moved or removed only if it has no required side effects and no data dependence that changes the result. Calls, I/O, volatile memory, exceptions, and pointer aliasing can make an apparently local expression observable. Machine-independent means processor-independent, not semantics-free.

## Worked examples
### Example 1: constant folding
`t1=2+3; t2=t1*4` becomes `t1=5; t2=t1*4` and, after propagation, may become `t2=20`, provided integer overflow behavior permits it.

### Example 2: copy propagation
```
a = b
c = a
use(c)
```

If `b` is not changed between definitions and uses, `c=a` and `use(c)` can use `b`. The reaching-definition and live analysis determine whether this is safe.

### Example 3: dead code
`x = f();` can be removed only if `f` has no side effects and its result is unused. A call to `print()` cannot be removed merely because its return value is unused.

### Example 4: loop-invariant motion
```
while (i < n) {
  t = a + b;
  use(t);
  i = i + 1;
}
```

If `a` and `b` do not change, `t=a+b` can be moved before the loop, subject to the language’s evaluation/exception rules.

### Example 5: common subexpression
For `x=a+b; y=a+b` with no writes to `a` or `b` and pure addition, generate `t=a+b; x=t; y=t`. If `a` or `b` can be modified by a call, the second computation may not be redundant.

## Key terms & formulas
- Basic block: one entry, one exit, no internal branch.
- CFG: `(blocks, edges)`.
- Reach definition: a definition that can reach a use along a path without being killed.
- Live variable: current value may be used before a redefinition.
- Constant folding: `const op const → const`.
- `L = A − A` is not always valid for floating-point or exception-producing arithmetic.

## Common mistakes
- Machine-independent does not mean language-semantics-independent.
- Do not remove calls, loads, or stores solely because a result appears unused.
- Use reaching definitions before copy propagation or common-subexpression elimination.
- Do not move a side-effecting or exception-producing expression out of a loop.
- A local optimization can miss a definition/use in another block; call it global when analysis is cross-block.

## Exam prep
**Likely 2-mark questions**
1. Define machine-independent optimization. **Hint:** target-independent semantic improvement.
2. Distinguish local and global optimization. **Hint:** basic block versus CFG.
3. Name three techniques. **Hint:** folding, propagation, dead-code elimination.
4. What is a live variable? **Hint:** value may be read before redefinition.

**Long-answer questions**
1. Explain data-flow analysis for reaching definitions and liveness. **Hint:** equations/transfer functions and fixed point.
2. Optimize a supplied basic block. **Hint:** show each transformation and safety condition.
3. Explain loop-invariant code motion. **Hint:** invariant operands and no harmful effects.
4. Compare common-subexpression elimination with copy propagation. **Hint:** expression versus value definitions.
5. Discuss why dead-code elimination is difficult in real languages. **Hint:** side effects, exceptions, aliasing, volatile state.

**Exam habit**
For every optimization, write a one-line preservation argument: which source values, side effects, and error behavior remain unchanged.
