---
subject: oose
unit: 5
topic: flow-graphs-and-path-testing
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Flow Graphs and Path Testing
## Overview
A control-flow or flow graph is a directed graph that represents the possible transfer of control through a program. Nodes represent regions or statements, and edges represent possible control transfers. A predicate node has more than one outgoing edge and represents a decision. A path follows connected edges from the entry to the exit.

Path testing uses this structure to choose tests that exercise important control paths. It can reveal logic defects, unreachable code, missing decisions, and incorrect loop exits. It cannot normally execute every complete path because loops create infinitely many paths, so basis or independent paths are selected.

## Explanation
### 1. Constructing a flow graph
1. Identify the entry and exit.
2. Convert statements and closely connected blocks into regions/nodes.
3. Draw directed edges for sequential control.
4. For every decision, create a predicate node and separate outgoing edges for each possible outcome.
5. Label edges with conditions such as `true`, `false`, or `x > 0`.
6. Check that every reachable statement and branch is represented.

A node may be a single statement, a basic block with one entry and one exit, or a region. The graph should make control decisions visible, not copy every punctuation mark.

### 2. Terms
- **Flow/edge:** a possible transfer of control.
- **Node/region:** a statement or group of statements with limited entry/exit.
- **Predicate node:** a decision with two or more successors.
- **Path:** a sequence of connected nodes/edges from entry to exit.
- **Complete path:** includes every possible branch decision from entry to exit.
- **Feasible path:** a path that can execute under some allowed input.
- **Unreachable node:** no path from entry to it.
- **Dead code:** unreachable or impossible code under the stated domain.

### 3. Cyclomatic complexity
For a connected flow graph with one entry and one exit, McCabe cyclomatic complexity is commonly:

`V(G) = P + 1`, where `P` is the number of predicates (decision nodes).

The equivalent graph formula is `V(G) = E − N + 2P`, where `E` is the number of edges, `N` nodes, and `P` connected components. For ordinary single-entry/single-exit control flow, `P` is often 1, so `V = E − N + 2`.

Complexity is a structural measure, not a quality score. A high value suggests many control combinations and a need for more testing or simplification; a low value does not prove correctness.

### 4. Graph matrix notation
A **graph matrix** has one row for source node and one column for destination node. An entry is 1 (or an edge label) when control can transfer from the source row to the destination column, and 0 otherwise. The matrix helps count paths, identify nodes with no predecessor, and check whether a path exists to the exit.

For example, with nodes `1=start`, `2=valid?`, `3=process`, `4=retry`, `5=stop`:

```text
      1  2  3  4  5
1     0  1  0  0  0
2     0  0  1  1  0
3     0  0  0  0  1
4     0  1  0  0  0
5     0  0  0  0  0
```

The exact matrix depends on the graph. Tools can use adjacency or reachability matrices to enumerate paths; the student should be able to explain the notation rather than memorize one fixed table.

### 5. Path testing process
1. Draw/inspect the flow graph.
2. Count predicates and calculate cyclomatic complexity.
3. Identify feasible independent/basis paths.
4. Derive input data and expected results for each path.
5. Execute tests and record which edges/nodes were covered.
6. Add tests for boundaries, exceptions, invalid values, and paths discovered during review.
7. After a defect, determine whether other paths or regression cases are affected.

### 6. Limitations
A loop creates paths such as `repeat 0`, `repeat 1`, `repeat 2`, … times. Even without loops, independent condition combinations can grow quickly. Path testing also depends on the control-flow model and may miss a wrong calculation on a path, missing UI behavior, or a data problem. Use it alongside black-box, data-flow, integration, and requirement tests.

## Worked examples
### Example 1: Login flow graph
```text
Start → read PIN → [valid?]
             ├─ yes → open account → End
             └─ no → [attempts < 3?]
                          ├─ yes → read PIN
                          └─ no → block → End
```
There are two predicates, so `V(G) = 2 + 1 = 3`. A basis set includes: valid PIN, invalid first attempt followed by valid retry, and invalid until blocked. The graph reveals a missing transition if the block edge is not connected to the exit.

### Example 2: Matrix path check
Using the matrix above, a reachability search from node 1 reaches 1, 2, 3, 4, and 5. Node 5 has no outgoing edge, as expected. If a node has a row of zeros but is not the entry, it is unreachable. If a node has no path to exit, the code may not complete normally.

### Example 3: Boundary path versus value boundary
A path test can choose a value below, at, and above a loop limit, but it does not automatically test a numeric boundary such as 64, 65, and 66. Those are boundary-value tests. Combining techniques gives stronger evidence.

### Example 4: Defect discovery
A review of a refund graph shows that the “amount > 0” false edge jumps to the success exit rather than the error path. Path testing with a zero amount follows the false edge and reveals that the program reports success for an invalid refund. The fix changes the graph and regression tests cover both values.

## Key terms & formulas
- **Flow graph:** directed graph of control regions and transfers.
- **Node/region:** statement or basic block.
- **Edge/flow:** possible control transfer.
- **Predicate:** decision node selecting an outgoing flow.
- **Path:** connected sequence of edges from entry to exit.
- **Complete path:** all decisions on a particular entry-to-exit route.
- **Feasible path:** executable under at least one permitted input.
- **Unreachable code:** code with no path from entry.
- **Cyclomatic complexity:** `V(G) = P + 1` (single-entry/single-exit graph), or `E − N + 2P`.
- **Graph matrix:** row/column adjacency table of graph edges.
- **Path coverage:** executed independent paths ÷ selected independent paths × 100%.
- **Edge coverage:** executed edges ÷ total reachable edges × 100%.

## Common mistakes
- Counting every sequential statement as a decision and inflating complexity.
- Using `P` as the number of outgoing edges instead of predicate nodes.
- Forgetting the `+1` in `V = P + 1`.
- Calling every graph path a distinct test without checking feasibility.
- Assuming a loop can be exhaustively tested by complete path enumeration.
- Drawing a graph whose entry or exit is missing, then applying the formula without checking the preconditions.
- Claiming path coverage means every data value or requirement was tested.

## Exam prep
### Likely 2-mark questions
1. **Define a flow graph and predicate.** A directed graph of control regions/edges; a node selecting one of multiple outgoing control paths.
2. **State the cyclomatic-complexity formula for a connected graph.** `V(G) = P + 1`, or the equivalent `E − N + 2P` form with the correct number of components.
3. **What is an independent path?** A path that introduces at least one new predicate decision/outcome not introduced by earlier selected paths.
4. **Why is exhaustive path testing impractical?** Loops create infinitely many paths and predicate combinations can grow rapidly.
5. **What is a graph matrix?** A table indicating which source nodes can transfer control to which destination nodes.
6. **Name two uses of path testing.** Finding logic errors, unreachable code, missing branch behavior, or estimating required tests.

### Long-answer answer hints
- “Explain flow graphs and path testing”: construction, notation, predicates, paths, matrix, cyclomatic complexity, test process, and limitations.
- “Draw a flow graph for login and derive V(G).” Count two predicates, show formula, list basis paths.
- “How does a graph matrix help?” count successors, detect unreachable nodes, find paths, and check exit reachability.
- “Why is path testing not enough?” loops, data values, requirements, oracles, and integration defects are not covered by control paths alone.
- “Explain unreachable code detection.” identify entry-reachability in the graph and verify source/domain constraints.

### Worked formula example
For a graph with `P = 4` predicates, `V(G) = 4 + 1 = 5`. A basis test set should normally contain at least five feasible independent paths, though the final suite may include more tests for data, exception, and quality concerns.
