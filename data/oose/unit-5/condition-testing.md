---
subject: oose
unit: 5
topic: condition-testing
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Condition Testing
## Overview
Condition testing examines the truth values of Boolean expressions and the decisions they control. It is a white-box technique that goes beyond merely executing a decision once. A decision may take a true or false outcome, but its component conditions may take combinations that the decision does not distinguish. Condition coverage helps expose missing or incorrectly implemented logic.

The syllabus's “control structure testing” includes condition testing. A practical test set combines branch, condition, and condition/decision coverage with boundary and requirement tests. A high percentage is not a proof, because a condition can be evaluated without the resulting behavior being correct.

## Explanation
### 1. Boolean expressions
A Boolean expression is a predicate such as:

```text
if (age >= 18 && hasConsent && !isBlocked)
```

The **atomic conditions** are `age >= 18`, `hasConsent`, and `!isBlocked`. The **decision** is the entire `if` expression. With short-circuit `&&`, the right side may not be evaluated when the left is false, which affects how tests are designed and observed.

### 2. Branch and decision coverage
- **Decision/branch coverage:** execute each possible outcome of each decision at least once.
- **Condition coverage:** make each atomic condition evaluate to true and false at least once.
- **Condition/decision coverage:** for every atomic condition, find at least one case where it is true and the overall decision is true, and one where it is false and the overall decision is false.
- **Multiple-condition coverage:** execute every possible truth-value combination of the atomic conditions.
- **Short-circuit MC/DC:** each condition is shown to independently affect the overall result while the other conditions are controlled.

These criteria have different strength and cost. Branch coverage does not guarantee that every atomic condition is toggled; condition coverage does not guarantee that the overall decision is correctly combined.

### 3. Why combinations matter
A faulty expression such as `age >= 18 && hasConsent && !isBlocked` may accidentally use `||` for one condition. Tests that only show the overall true and false outcomes may miss the defect. A truth table makes the intended combinations explicit.

For three atomic conditions, multiple-condition coverage has `2^3 = 8` combinations, subject to feasibility and short-circuit evaluation. The number of tests can grow exponentially, so MC/DC or targeted boundary tests are often more practical.

### 4. Deriving condition tests
1. Locate decisions and parse atomic conditions.
2. Identify the intended truth table and short-circuit behavior.
3. Choose criteria: branch, condition, condition/decision, MC/DC, or risk-based combinations.
4. Build inputs satisfying the required values and other domain constraints.
5. Predict the result of every condition and the overall decision.
6. Observe actual evaluation where instrumentation is available.
7. Add boundary values, nulls, invalid types, and authorization cases.
8. Link each test to a requirement and record missed combinations.

### 5. Truth-table example
For `A && B`:

| A | B | A && B |
|---|---|---|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

Branch coverage needs only one T and one F case. Condition coverage also needs A to be T/F and B to be T/F. MC/DC needs cases showing A independently changes the result and B independently changes the result; a compact short-circuit set is often `T,T`, `F,T`, `F,F` (or an equivalent set depending on masking and tool definitions).

For `A || B`, a short-circuit set is `T,F`, `T,T`, `F,T` (or equivalent). The selected set should follow the adopted MC/DC definition and short-circuit semantics.

### 6. Condition/decision and MC/DC
Condition/decision coverage requires:
- for each condition, a case where it is T and overall T;
- for each condition, a case where it is F and overall F.

MC/DC strengthens this by showing that changing one condition can change the overall decision while holding the relevant others constant. For `n` atomic conditions, a two-outcome short-circuit MC/DC test set can often use `n + 1` tests under a particular independence definition, but the exact count depends on masking, short-circuit evaluation, and the tool/standard. State the definition rather than quoting a number blindly.

### 7. Limitations
- It focuses on Boolean logic, not arithmetic correctness or data validity.
- It can encourage mechanical tests that do not represent real users.
- Short-circuiting may prevent a condition from evaluating, so “condition coverage” must define observation.
- Complex conditions, loops, and concurrent state require additional techniques.
- 100% condition/decision coverage does not guarantee all paths, requirements, or side effects.

Use code coverage tools and manual reasoning together. A tool can show that a branch executed, but only a domain expert can judge whether the expected combination and state are meaningful.

## Worked examples
### Example 1: Access rule
```text
if (user.isAuthenticated && user.hasRole("Supervisor") && inspection.isOpen)
```
Test cases:
- authenticated supervisor, open inspection → allow;
- viewer, open inspection → deny (role false, decision false);
- authenticated supervisor, closed inspection → deny (inspection false, decision false);
- unauthenticated supervisor, open inspection → deny (authentication false, decision false).
These cover both decision outcomes and each atomic condition. Additional tests check case sensitivity, missing role, and a closed-by-system state.

### Example 2: Boundary interaction
For `age >= 18 && country == "IN"`, test ages 17, 18, and 19 with valid country values, plus age 18 with another country. The boundary values expose an off-by-one error; condition coverage alone would not necessarily choose 17/18/19.

### Example 3: Short-circuit side effect
```text
if (repository.exists(id) && repository.load(id).isEnabled())
```
A missing ID must not call `load` or throw. A test instrumenting the call verifies short-circuit behavior. This is a semantic requirement, not just a branch count.

### Example 4: MC/DC calculation
A decision has four atomic conditions. A common short-circuit MC/DC target is approximately `n + 1 = 5` tests, but the test author must state the independence/masking definition and show each condition can independently change the result. Do not claim 5 is universal without that assumption.

## Key terms & formulas
- **Condition:** Boolean expression whose truth value can be true or false.
- **Atomic condition:** smallest evaluable Boolean subexpression.
- **Decision:** compound predicate that controls a branch.
- **Branch/decision coverage:** both outcomes of every decision.
- **Condition coverage:** every atomic condition takes both truth values.
- **Condition/decision coverage:** every condition is true with overall true and false with overall false.
- **Multiple-condition coverage:** all truth-value combinations.
- **MC/DC:** each condition independently affects the decision result.
- **Short-circuit evaluation:** later operands may not evaluate after an earlier decisive result.
- **Condition coverage:** `executed condition truth values / required condition truth values × 100%`.
- **MC/DC target (common two-outcome case):** approximately `n + 1` tests; exact count depends on definition.

## Common mistakes
- Calling atomic conditions the same as the whole decision.
- Claiming branch coverage equals condition coverage.
- Testing the overall true/false result only and claiming MC/DC.
- Ignoring short-circuit side effects.
- Using combinations that violate domain rules and calling them feasible tests.
- Assuming a coverage percentage proves the business rule is correct.
- Forgetting the expected state, not just the branch outcome.

## Exam prep
### Likely 2-mark questions
1. **Define condition testing.** White-box testing that analyzes Boolean conditions and the decisions they control.
2. **Differentiate condition and decision coverage.** Condition coverage varies each atomic condition; decision coverage executes each overall branch outcome.
3. **What is condition/decision coverage?** Each condition is true with overall true and false with overall false.
4. **What is MC/DC?** Each condition is shown to independently affect the decision result.
5. **How many combinations for n Boolean conditions?** Up to `2^n`; short-circuit and domain constraints may reduce feasible cases.
6. **Why is short-circuit evaluation important?** It affects which condition executes and whether side effects/errors occur.

### Long-answer answer hints
- “Explain condition testing”: conditions, decisions, coverage criteria, truth tables, test derivation, MC/DC, and limitations.
- “Draw a truth table and derive tests for A && B or A || B.” Show truth values, branch, condition, and MC/DC sets.
- “Compare branch, condition, condition/decision, and multiple-condition coverage.” Give strength and cost for each.
- “Apply to an access rule.” Use roles, authentication, state, authorization, and negative tests.
- “Why does 100% condition coverage not prove correctness?” expressions can be evaluated without meaningful data or correct expected behavior.

### Formula reminder
For `n` atomic Boolean conditions, full truth-table combinations are up to `2^n`; a short-circuit MC/DC suite is often around `n + 1` tests under a stated independence rule.
