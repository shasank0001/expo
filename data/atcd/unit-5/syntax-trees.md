---
subject: atcd
unit: 5
topic: syntax-trees
syllabus_ref: CSM3203 Unit-V
status: draft
---
# Syntax Trees
## Overview
A syntax tree represents the hierarchical structure of a program or expression after parsing. Leaves are tokens or operands, internal nodes are constructors and operators, and the grouping records precedence, associativity, and nesting. Code generation can traverse the tree and emit intermediate code in an order that respects the language’s evaluation rules. A parse tree follows the grammar literally; a syntax tree is usually a compressed and annotated form.

## Explanation
### Tree representation
For an expression, leaves are variables/constants and internal nodes are operators or language constructs. For a statement, nodes can represent assignment, conditional, loop, procedure call, and block. Each node has attributes such as type, scope, storage class, and source position. A tree is not merely a visual parse: it is an interface between syntax analysis and later phases.

### Precedence and associativity
In `a+b*c`, multiplication is the deeper subtree, so it is evaluated first. Parentheses `(a+b)*c` put addition below multiplication. For repeated operators, left associativity makes `a-b-c` a left-leaning tree; right associativity makes it right-leaning. The grammar or parser precedence rules must create exactly the intended tree.

### Parse tree versus syntax tree
A parse tree includes every grammar nonterminal and reflects each production application. A syntax tree omits grammar-only symbols and may combine fields or annotate nodes with semantic information. For example, a parse tree may contain `E`, `T`, and `F` around `a*b`, while an expression AST can contain only an `MUL` node with two operand children.

### DAGs and repeated expressions
A directed acyclic graph can point multiple parents to one common subexpression. If `(a+b)` occurs twice and neither evaluation changes state, one node can be evaluated once. A tree duplicates the node. A DAG requires correct use/def information and must not merge nodes with different types or side effects.

### Traversals
- **Preorder:** emit a node before its children.
- **Postorder:** emit children before the parent.
- **Inorder:** used for some binary-tree tasks, but not the usual expression code-generation order.

For `a+(b*c)`, postorder emits `a`, `b`, `c`, multiplication, then addition. This ensures operands are available before their operator. If the language has short-circuit operators or unspecified evaluation order, code generation must follow the language rules rather than blindly using mathematical intuition.

### Syntax-directed translation
A semantic action can be attached to each grammar production. At `E→E1+E2`, generate code for `E1`, generate code for `E2`, then emit an add instruction. At a declaration, allocate storage; at a function call, pass arguments. Attributes and the symbol table connect tree nodes to memory locations and types.

### Uses in optimization
Tree shape reveals common subexpressions, constant subtrees, reassociation opportunities, and dead values. A DAG makes sharing explicit. The optimizer must still respect type, overflow, exceptions, and side effects.

## Worked examples
### Example 1: precedence
For `a + b * c`, the tree has `+` at the root and `*` below its right child. A postorder traversal produces `t1=b*c; t2=a+t1`.

### Example 2: parentheses
For `(a+b)*c`, `+` is below the root `*`. The traversal produces `t1=a+b; t2=t1*c`. The same token sequence with different parentheses has a different tree and code order.

### Example 3: statement tree
For `if p then x=1 else x=2`, the root is `IF`; its children are condition `p`, then statement `x=1`, and else statement `x=2`. The backend creates labels and conditional branches.

### Example 4: DAG sharing
If an expression contains `(a+b)*c` twice, a tree has two `a+b` subtrees. A DAG can share one `ADD(a,b)` node, but only if the intervening code does not modify `a` or `b`.

## Key terms & formulas
- Syntax tree node: operator/constructor with ordered children.
- Precedence: tree depth/grouping; associativity: direction of repeated operators.
- Postorder code generation: children first.
- DAG: one node, multiple parents, no cycles.
- Tree attributes: type, scope, storage, source location.

## Common mistakes
- A syntax tree is not necessarily identical to a parse tree.
- Parentheses change the tree even when the token sequence is otherwise similar.
- Do not reassociate floating-point or side-effecting expressions without language permission.
- A DAG is not a tree if it shares nodes; call it a common-subexpression representation.

## Exam prep
**Likely 2-mark questions**
1. What does a syntax tree represent? **Hint:** hierarchical program structure.
2. Distinguish syntax tree and parse tree. **Hint:** compressed versus grammar-literal.
3. Why is postorder useful? **Hint:** children/operands before parent/operator.
4. What is a syntax-tree DAG? **Hint:** shared acyclic expression node.

**Long-answer questions**
1. Draw syntax trees for three precedence/associativity examples. **Hint:** show grouping and traversal.
2. Explain syntax-directed code generation. **Hint:** actions on productions and postorder.
3. Discuss common-subexpression sharing and its safety conditions. **Hint:** use/def and no side effects.
4. Compare a parse tree, syntax tree, and DAG in compiler phases. **Hint:** grammar, semantics, optimization.
