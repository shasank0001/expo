---
subject: atcd
unit: 3
topic: parse-trees
syllabus_ref: CSM3203 Unit-III
status: draft
---
# Parse Trees
## Overview
A parse tree is a diagram of one complete derivation. Its root is the grammar’s start symbol, internal nodes represent nonterminals and the productions used to expand them, and leaves are the terminal input symbols. Parsers use the tree—or a compressed syntax tree—to preserve grouping, perform semantic checks, and guide intermediate-code generation. A key distinction is that a parse tree includes grammar scaffolding, while a syntax tree usually keeps only useful language constructs.

## Explanation
### Tree structure
For a production `A→BC`, the node `A` has children `B` and `C` in left-to-right order. If a child is a nonterminal, it is expanded using one of its productions. If it is a terminal, it becomes a leaf. The yield, read from left to right at the leaves, is the input string.

### Parse tree versus derivation
A derivation lists forms such as `S⇒AB⇒aB⇒ab`; a parse tree shows the same applications spatially. Leftmost and rightmost derivations of the same tree give the same tree shape. Different production choices can give different trees for the same yield, which is the definition of ambiguity.

### Parse tree versus syntax tree
A parse tree follows the grammar literally, so it may contain many nonterminals used only to express precedence. A syntax tree is a compressed representation: it may omit grammar-only nodes and label operators, variables, and literals directly. Both preserve structure, but the parse tree is more directly tied to grammar membership.

### Constructing a tree
1. Put the start symbol at the root.
2. Choose a production for each nonterminal.
3. Add the right-hand-side symbols as children.
4. Continue until every leaf is a terminal.
5. Read leaves left-to-right and compare with the input.

A complete tree is also evidence that the token sequence is in `L(G)`, provided the tree was constructed according to valid productions.

### Ambiguity
If a grammar has two parse trees with the same root and same leaf string, it is ambiguous. A tree alone does not prove ambiguity; one must find a second tree with a different shape. Expression grammars often become ambiguous when `+` and `*` are not separated into different nonterminals.

### Use in compilers
A parser can attach semantic actions at grammar symbols, infer types for identifiers, generate intermediate code after children are available, and report the line associated with a node. A tree also makes syntax-directed translation systematic. However, huge parse trees consume memory, so production compilers may build a compact AST directly.

### Tree traversal
Preorder visits a node before its children; postorder visits children before the node. Expression code generation usually needs postorder semantics so operands are translated before the operator. Left-to-right leaf order must be preserved for side effects and evaluation order.

## Worked examples
### Example 1: simple tree
Grammar `S→AB`, `A→a`, `B→b` gives:

```
       S
      / \
     A   B
     |   |
     a   b
```

The yield is `ab`, the root is `S`, and each internal node is expanded by one production.

### Example 2: precedence tree
For `E→E+T|T`, `T→T*F|F`, `F→id`, the tree for `a+b*c` has the multiplication subtree below the addition subtree. It encodes `a+(b*c)`. If the grammar had only `E→E+E|T` and treated `*` as an `E` operator, the tree could group the string differently.

### Example 3: ambiguous string
The grammar `E→E+E|T`, `T→id` has two parse trees for `id+id+id`: one groups the first addition, and the other groups the last. The leaves are identical, but the tree shapes differ.

### Example 4: semantic action
At the `T→T*F` node, a postorder action can first generate code for both `T` and `F`, then emit a multiplication. The action at the parent can use the resulting temporary. This is syntax-directed translation.

## Key terms & formulas
- Root: `S`; leaves: terminal yield.
- Production `A→α`: children of `A` are symbols of `α`.
- Ambiguity: two distinct parse trees for one terminal string.
- Preorder: parent first; postorder: children first.
- `yield(T)` is the left-to-right sequence of terminal leaves.

## Common mistakes
- A parse tree is not the string of sentential forms used during derivation.
- The start symbol is not automatically a terminal leaf.
- A single parse tree does not establish ambiguity; find a second distinct tree.
- A syntax tree and parse tree are related but not identical structures.

## Exam prep
**Likely 2-mark questions**
1. What does a parse tree represent? **Hint:** one derivation and its terminal yield.
2. State the roles of root, internal nodes, and leaves. **Hint:** start symbol, productions, terminals.
3. Define ambiguity using parse trees. **Hint:** same yield, different trees.
4. Distinguish parse tree from syntax tree. **Hint:** full grammar versus compressed structure.

**Long-answer questions**
1. Draw parse trees for two strings under a supplied grammar. **Hint:** show all productions.
2. Demonstrate ambiguity with two trees for `id+id+id`. **Hint:** different grouping.
3. Explain how postorder traversal helps code generation. **Hint:** operands before operators.
4. Describe semantic actions attached to a parse tree. **Hint:** type checking and translation.
