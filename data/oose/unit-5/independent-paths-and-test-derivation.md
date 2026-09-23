---
subject: oose
unit: 5
topic: independent-paths-and-test-derivation
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Independent Paths and Test-Case Derivation
## Overview
Basis-path testing selects a set of **independent paths** through a flow graph and derives one or more test cases for each. Independent paths are selected so that each new path introduces at least one new predicate decision or outcome that earlier paths did not. The resulting set is a practical approximation to exhaustive path testing, especially when loops make complete enumeration impossible.

The method is most effective for conventional control flow with understandable predicates. It must be combined with boundary, data, exception, and requirement tests because a path can be executed with many different data values and still hide a calculation defect.

## Explanation
### 1. Terminology
- **Predicate:** a decision node in the flow graph.
- **Path:** a sequence of edges from entry to exit.
- **Independent path:** a path containing at least one predicate outcome not present in any previously selected path.
- **Basis set:** a selected set of independent paths intended to represent the major control combinations.
- **Test case:** inputs, preconditions, execution steps, expected result, and coverage target.
- **Feasible:** executable with legal data and state.

An independent path is not simply the shortest, longest, or first path. Selection must consider decisions and their outcomes.

### 2. Basis-path procedure
1. Draw a flow graph with a clear entry and exit.
2. Count predicates and calculate cyclomatic complexity `V(G) = P + 1`.
3. Identify the decision nodes and possible outcomes.
4. Start with a straightforward path.
5. Add paths that introduce new predicate outcomes while avoiding redundant combinations.
6. Check that every selected path is feasible under the domain.
7. Derive input data and state for each path.
8. Determine expected output/state and record the path.
9. Execute and update coverage; add exceptional or boundary tests as needed.

### 3. Deriving test data
For each independent path, work backwards from the path constraints. A path might require `age >= 18`, `status == Active`, and `retryCount < 3`. Choose values satisfying all constraints simultaneously. For an infeasible path, investigate the code or requirements rather than forcing a bad test.

A test case should identify:
- requirement/use case and path ID;
- initial objects, database, and system state;
- input values and their boundary meaning;
- steps or method/UI actions;
- expected return, state, side effect, and error;
- priority, environment, and automation status.

### 4. Independent-path selection heuristics
- Cover both outcomes of every predicate.
- Keep the path count close to the cyclomatic complexity.
- Vary a decision that can be changed independently.
- Combine decisions when they represent meaningful behavior.
- Avoid repeating the same set of outcomes.
- Do not choose an impossible path only to reach a count.
- Include paths for denied, invalid, and recovery behavior when required.

### 5. Path feasibility and constraints
Feasibility can be limited by:
- contradictory guards;
- data dependencies;
- state-machine rules;
- database constraints;
- loops with a zero-iteration restriction;
- security/authorization rules;
- nonfunctional or timing conditions.

If a graph path is syntactically connected but violates a domain invariant, it is not a valid test path. A good test plan records the discrepancy and feeds it back to requirements/design review.

### 6. Limits of cyclomatic complexity as a test count
`V(G)` is a structural lower-bound-like guide, not a guarantee of adequacy. A module may need more tests for:
- boundary values;
- equivalent data classes;
- state and message order;
- invalid combinations;
- performance, usability, and security;
- external failures and recovery;
- regression.

It is also possible to reach a complexity number with poor tests. A path’s test data and expected result still require intelligent analysis.

### 7. Coverage interpretation
Report independent-path coverage, but also state:
- predicates/outcomes covered;
- unexecuted or infeasible paths;
- boundary and requirement tests outside the basis set;
- environment and data assumptions.

A “100% independent paths” claim is narrow evidence, not a statement that the product is defect-free.

## Worked examples
### Example 1: Login basis paths
Graph:

```text
Start → read PIN → [valid?]
                  ├─ true → show account → End
                  └─ false → [attempt < 3?]
                                ├─ true → read PIN
                                └─ false → block → End
```

`P = 2`, `V(G) = 3`. Select:
1. valid PIN first attempt;
2. invalid first attempt, valid second attempt;
3. invalid three times, blocked.
Test data:
- `1111` for valid first;
- invalid, then valid for retry;
- three invalid values and verify lockout. Expected states and side effects are documented for each.

### Example 2: Deriving simultaneous constraints
Path P1 requires `isMember = true`, `balance >= 100`, and `country = IN`. A test input must satisfy all three; testing members with low balance follows a different path. The analyst records the selected value and why it is legal. A contradictory path (member and nonmember simultaneously) is marked infeasible.

### Example 3: Loop
A retry loop has paths for zero, one, and two attempts. The graph may show a loop edge, so complete paths continue indefinitely. The basis set covers the no-retry, one-retry, and exit-after-limit cases. A separate boundary test checks exactly the maximum allowed attempt and one beyond it.

### Example 4: Defect and regression
A basis test follows the `amount > 0` true path and finds that the program never records an audit event. After the fix, the test suite runs every independent path plus the audit regression check. The test report shows the new path coverage and the side-effect assertion.

### Example 5: Requirement link
`FR-PAY-02: A valid payment shall update the account or report a recoverable failure.` Basis paths include successful processing, provider timeout, retry, and final failure. A path test checks the control route; an integration/mock test checks the provider contract and the account state.

## Key terms & formulas
- **Independent path:** path introducing a new predicate outcome relative to selected paths.
- **Basis path set:** practical collection of independent paths.
- **Predicate count:** `P`.
- **Cyclomatic complexity:** `V(G) = P + 1` for a connected single-entry/single-exit graph.
- **Test path ID:** stable identifier for a selected path and its constraints.
- **Feasible path:** executable with valid inputs/state.
- **Path test case:** data, steps, expected result, and coverage target.
- **Path coverage:** executed selected independent paths ÷ selected independent paths × 100%.
- **New-outcome count (for a path):** number of predicate outcomes not in previously selected set; must be at least one for an independent path.
- **Path length:** number of nodes/edges on a path; not a quality measure by itself.

## Common mistakes
- Calling any distinct sequence an independent path.
- Selecting a path that cannot execute under the domain rules.
- Using one arbitrary input for a path without checking all guards.
- Forgetting expected side effects and only checking the return value.
- Assuming `V(G)` tests are sufficient or that the shortest paths are best.
- Ignoring loops, exception paths, and state reset between tests.
- Claiming 100% path coverage while many predicates or requirements are untested.

## Exam prep
### Likely 2-mark questions
1. **Define an independent path.** A path with at least one predicate decision/outcome not exercised by previously selected paths.
2. **State the basis-path procedure.** Draw graph → count predicates/complexity → select independent paths → derive feasible data/expected results → execute/measure.
3. **What is cyclomatic complexity in this method?** `P + 1`, used to estimate the number of independent paths.
4. **Why derive inputs backwards from a path?** To satisfy all guards/state constraints simultaneously and produce a feasible test.
5. **Give one reason path testing is incomplete.** Loops, data boundaries, state, requirements, or external failures are not fully covered.
6. **What is path coverage?** Executed selected independent paths divided by the total selected independent paths.

### Long-answer answer hints
- “Explain independent-path testing”: definitions, selection rule, cyclomatic complexity, test derivation, feasibility, coverage, and limitations.
- “Draw a graph and select basis paths for ATM/withdrawal”: label predicates, count complexity, list paths and input constraints.
- “Differentiate independent and complete paths”: independent is a coverage criterion; complete enumerates all possible entry-to-exit sequences, often infinite.
- “Derive a test case from a path”: state path constraints, choose data, setup, steps, expected state, and link to requirement.
- “Why is path count not a coverage guarantee?” explain structural versus behavioral and quality-oriented testing.

### Selection table
| Path | New decision/outcome | Feasible data | Expected result | Defect link |
|---|---|---|---|---|
| P1 | first valid branch | … | … | FR/UC |
| P2 | retry branch | … | … | FR/UC |
