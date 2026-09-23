---
subject: atcd
unit: 5
topic: expression-translation
syllabus_ref: CSM3203 Unit-V
status: draft
---
# Three-Address Translation of Expressions
## Overview
Expression translation converts a typed syntax tree into a sequence of simple instructions that evaluates the expression in the source language’s required order. Precedence, associativity, parentheses, short-circuit operators, and side effects all affect the generated code. A recursive syntax-directed scheme is the most reliable approach: translate operands first, then emit the operator into a fresh temporary.

## Explanation
### Grammar and semantic scheme
A conventional expression grammar separates precedence:

`E→E1+T | E1−T | T`
`T→T1*F | T1/F | F`
`F→(E) | id | num | unary-op F`.

Each nonterminal has an attribute `addr` containing the address of its value. For `E→E1+T`, the actions are:

1. `E1.addr = translate(E1)`;
2. `T.addr = translate(T)`;
3. `temp = newtemp`;
4. emit `temp = E1.addr + T.addr`;
5. `E.addr = temp`.

The same idea handles subtraction, multiplication, division, comparisons, and type conversions.

### Recursive algorithm
`translate(node)` returns an address:

- for a constant or variable, return its name/address;
- for a parenthesized expression, translate its child;
- for a unary node, translate the child and emit a unary operation;
- for a binary node, translate left and right, allocate a fresh temporary, and emit the binary operation.

Use a postorder walk when the tree is already built. The temporary order mirrors evaluation order, which is important for exceptions, function calls, and assignments.

### Precedence and associativity
For `a+b*c`, multiplication is translated first, then addition. For `a-b-c`, left recursion and the semantic scheme produce `(a-b)-c`; right recursion would produce `a-(b-c)`. Parentheses create a distinct subtree and override default grouping. A compiler must follow the language’s rules rather than ordinary arithmetic intuition when they differ.

### Assignment and side effects
An assignment expression may return a value as well as update a variable. If the language permits `x=(y=3)`, the translation may assign a temporary and then copy or use it. A call can have side effects, so the compiler cannot freely reorder two calls. Temporary reuse must account for liveness: a temporary holding a live value cannot be overwritten.

### Type and conversions
Semantic analysis annotates each node with a type. Before an operation, the translator may insert conversions, such as integer-to-real, or reject incompatible types. Constant operands may be folded only when evaluation is defined and no observable exception or rounding behavior is lost. The result temporary receives the appropriate type and storage.

### Boolean and short-circuit expressions
For `p && q`, evaluate `p`; if false, do not evaluate `q`. A control-flow translation uses conditional jumps and a result temporary. An ordinary bitwise `&` is different: it evaluates both operands. The grammar or semantic attributes must distinguish logical and bitwise operators.

### Arrays, fields, and calls
An array reference translates to an address calculation, often `t = base + index*size`. A structure field uses a known offset. A function call passes argument addresses or values, emits a call, and receives a return value. These details belong to the surrounding intermediate-code generator but must be integrated with expression translation.

### Expression DAGs
If repeated subexpressions are common, a DAG can reuse a node. The translation cache must be invalidated by assignments, calls, or other writes to any operand. A tree-only translation is always conceptually correct; DAG sharing is an optimization subject to semantic checks.

## Worked examples
### Example 1: `a+b*c`
`T→T*F` gives `t1=a*b`; the surrounding `E→E+T` production then gives `t2=a+t1`; the expression value is `t2`.

### Example 2: `(a+b)*c`
Parentheses force `t1=a+b`; then `t2=t1*c`. The order is visibly different from `a+b*c`.

### Example 3: left associativity
For `a-b-c`, use `E→E−T` and a left-recursive semantic scheme. The instructions are `t1=a−b; t2=t1−c`, not `t1=b−c; t2=a−t1`.

### Example 4: short circuit
For `p && q`, generate a conditional branch on `p` before evaluating `q`. A result temporary is set to true or false on the two paths. This avoids a call or division in `q` when `p` is false.

### Example 5: assignment value
For `r=(x=y+1)`, first generate `t1=y+1`, then `x=t1`, then either use/copy `t1` as the value of `r`. The exact final copy depends on whether the language returns the assigned value.

## Key terms & formulas
- `val(node)`: address of the node’s computed value.
- Semantic rule: `temp = left op right`.
- Postorder: evaluate children before parent.
- `R` for a right-recursive grammar; `L` for left associativity.
- Short-circuit: control flow, not just a Boolean bitwise operator.
- Temporary reuse requires liveness analysis.

## Common mistakes
- Translate the operator before its operands.
- Ignore parentheses or associativity.
- Reorder calls, division, or floating-point operations when the language forbids it.
- Use a temporary name that overwrites a value still needed later.
- Treat `&&` and `&` as interchangeable.

## Exam prep
**Likely 2-mark questions**
1. Explain recursive expression translation. **Hint:** child addresses then operator.
2. Translate `(a+b)*c`. **Hint:** two temporaries in order.
3. Why is postorder useful? **Hint:** operands before operator.
4. Name a type-related action. **Hint:** conversion or checking.

**Long-answer questions**
1. Write semantic rules for an expression grammar. **Hint:** attributes and emitted TAC.
2. Translate `a-(b+c)*d`. **Hint:** show precedence and temporaries.
3. Explain short-circuit translation of `p||q`. **Hint:** conditional branches and result value.
4. Discuss why expression reordering can be unsafe. **Hint:** side effects, exceptions, rounding.
5. Explain common-subexpression sharing in a DAG. **Hint:** cache and invalidation on writes.

**Exam habit**
After each instruction, state which source subexpression the address represents. This catches precedence and temporary-name errors quickly.
