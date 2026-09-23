---
subject: oose
unit: 5
topic: data-flow-and-loop-testing
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Data-Flow and Loop Testing
## Overview
Control-structure testing examines how data values and control loops affect a program. **Data-flow testing** looks for cases where a variable is defined, used, redefined, or killed in a suspicious way. **Loop testing** checks that loops execute zero times, the maximum permitted number, and typical/relevant counts. Both techniques find defects that simple path or branch coverage can miss.

These are white-box techniques. They require source-level or flow-graph knowledge, but they do not replace black-box boundary, use-case, performance, or usability tests.

## Explanation
### 1. Data-flow terminology
A **definition** creates or assigns a value to a variable. A **use** reads the value. A **kill** or **redefinition** overwrites a previous definition so that later paths may use the wrong value. A **def-use chain** links a definition to a use that can receive that value.

A **live variable** has a future use on some path before being overwritten. An **uninitialized data item** may be used before any definition. **Constant propagation** follows a fixed value through assignments; **constant partition** groups uses that may receive the same definition.

### 2. Data-flow anomalies
Common anomalies include:
- a variable is defined but never used;
- a variable is used before being defined;
- a variable is defined and then overwritten without an intervening use;
- a value is used after an incorrect or unexpected redefinition;
- a parameter or object field is not initialized on every path;
- a loop-carried value has a wrong initial or terminal value;
- a variable is live longer than necessary, increasing the chance of an incorrect value.

The analyzer should distinguish a real defect from a deliberately unused result or a valid constant. A data-flow test chooses a path and values that make the anomaly observable.

### 3. Data-flow test derivation
1. Draw a control-flow graph and annotate variable definitions and uses.
2. Build a definition/use table or reaching-definitions analysis.
3. Identify suspicious definitions, uses, redefinitions, and live ranges.
4. Select feasible paths that reach the suspicious pair.
5. Choose input and initial state values.
6. Predict the value at the use and the expected side effect.
7. Execute and check the value, output, and downstream state.
8. Add regression tests after correction.

A coverage goal may be stated as a percentage of selected definition-use pairs exercised, not simply “the program was run.”

### 4. Loop testing
A loop may execute:
- zero times;
- one time;
- many typical times;
- the maximum allowed times;
- one more than the maximum (when the code permits it);
- a value that causes an off-by-one or overflow problem.

The basic **LTEST** approach derives a test for zero, one, and typical/greater-than-one iterations. **LTEST2** adds the maximum and minimum boundary iterations. Nested loops require tests that vary inner and outer loops independently. Unstructured loops may need manual path analysis or refactoring.

### 5. Absolute and relative bounds
An **absolute bound** is an exact value, such as 0, 1, 2, 5, or 100. A **relative bound** is based on a variable or input, such as “maximum list size minus one,” “number of records,” or “one more than the limit.” A robust test includes both valid and invalid relative values, for example `n`, `n-1`, and `n+1`.

### 6. Loop-control and state testing
For each loop, identify:
- initial value of the control variable;
- update expression;
- termination condition;
- values accumulated or mutated;
- work performed per iteration;
- behavior after normal exit and forced failure;
- interaction with other loops and state.

A loop may pass a simple count test but fail after the tenth iteration because an index is never reset, a collection is modified during iteration, or a resource is exhausted. Test observable state, not only the count.

### 7. Relationship with other techniques
Data-flow and loop testing can reveal defects missed by basis paths because a path may execute with an innocuous value while a definition-use relationship is wrong. Conversely, data-flow analysis can report an anomaly in unreachable code; first check reachability and feasibility. Combine with:
- equivalence partitions and boundary values for input classes;
- condition testing for Boolean rules;
- path testing for control sequences;
- stress/concurrency tests for timing and shared state;
- black-box tests for user-visible results.

## Worked examples
### Example 1: Uninitialized use
```text
read x
if (ready) {
    y = x + 1
    output(y)
}
```
If `ready` is true without an input, `x` may be undefined. A data-flow test sets `ready=true` with no `x` and checks the output/error. The test reveals a missing default or validation rule, not merely a branch defect.

### Example 2: Redefinition
```text
total = 0
for item in items:
    tax = taxRate(item)
    total = total + tax
    tax = 0
output(tax)
```
The final tax may be zero because it is reset each iteration. A def-use test checks the value of `tax` at the final use and the expected last-item value. The fix moves the reset or changes the output semantics.

### Example 3: LTEST
For `for (i=0; i<limit; i++)`, derive tests with:
- zero iterations: empty input;
- one iteration: one item;
- typical: several items;
- maximum: exactly `limit`;
- boundary: `limit - 1` and `limit + 1` where invalid behavior is defined.

A test with 10 iterations checks that all 10 items are processed, not merely that the loop exits.

### Example 4: Nested loops
A grid has `rows` and `columns`. Test outer-zero/inner-zero, outer-one/inner-one, typical rectangular data, and a ragged input. Count total iterations with the expected formula for rectangular data:

`total inner visits = outer iterations × inner iterations`.

A mismatch identifies reset or indexing defects.

### Example 5: Live resource
A loop opens a file or network connection on every iteration but closes it only after the loop. A long-running test detects resource exhaustion. The loop test checks resource cleanup after each or final iteration, not just the returned count.

## Key terms & formulas
- **Definition:** assignment/creation of a value.
- **Use:** read of a value.
- **Kill:** definition that overwrites a prior value.
- **Def-use pair:** definition that may reach a use.
- **Reaching definition:** definition that can reach a use along a feasible path.
- **Data-flow anomaly:** suspicious definition/use/redefinition/live-range relationship.
- **Live variable:** variable whose current value may be used before being overwritten.
- **LTEST:** loop tests for zero, one, and typical/more-than-one iterations.
- **LTEST2:** extended loop tests including minimum and maximum bounds.
- **Absolute bound:** exact iteration/value boundary.
- **Relative bound:** bound derived from an input or computed limit.
- **DF-pair coverage:** selected definition-use pairs exercised ÷ selected pairs × 100%.
- **Loop-bound coverage:** selected loop boundary cases exercised ÷ selected loop boundary cases × 100%.
- **Expected nested visits:** `outer count × inner count` for rectangular full traversal.

## Common mistakes
- Calling every assignment a defect or ignoring feasible reachability.
- Testing only a loop's exit count and not the values/state after iterations.
- Assuming one test with a large count covers zero, one, and boundary cases.
- Forgetting to reset loop variables or shared collections.
- Testing an invalid relative bound without a defined expected result.
- Ignoring resource cleanup, exceptions, or concurrent termination.
- Reporting data-flow coverage without stating how pairs were selected.

## Exam prep
### Likely 2-mark questions
1. **Define a data-flow anomaly.** A suspicious definition/use/redefinition/live-range relationship that may cause a wrong value.
2. **Differentiate definition, use, and kill.** Definition assigns, use reads, kill overwrites a prior value.
3. **What is LTEST?** A loop test set including zero, one, and typical or greater-than-one iterations.
4. **What does LTEST2 add?** Minimum and maximum boundary iterations in addition to basic cases.
5. **Differentiate absolute and relative bounds.** Exact fixed values versus values derived from an input/limit.
6. **Why test nested loops independently?** An error in either dimension can be hidden by testing only a rectangular total count.

### Long-answer answer hints
- “Explain data-flow testing”: definitions, uses, kills, live variables, def-use pairs, anomalies, path/value derivation, and coverage.
- “Explain loop testing”: zero/one/typical/max, absolute/relative bounds, nested loops, state, resources, and limitations.
- “Apply LTEST to a list-processing loop”: list empty, one item, several, exact limit, and one beyond/under with expected results.
- “Find a data-flow defect in pseudocode”: show a variable defined, overwritten, then used; explain the selected path and expected value.
- “Why do these techniques complement path testing?” paths may execute with the wrong value; data-flow/loop tests focus on value and iteration behavior.

### Pseudocode annotations
```text
d1: x = read()       // definition
u1: y = x + 1        // use
d2: x = 0            // kill/redefinition
u2: print(x)         // use
```
Select a feasible path and assert the expected value at each use.
