---
subject: oose
unit: 5
topic: managing-software-testing
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Managing Software Testing
## Overview
Testing becomes unreliable when it is treated as a final, unplanned phase. Test management provides a strategy, plan, people, environment, data, schedule, budget, defect process, and release criteria. It coordinates the activities in the syllabus—inspection, unit, integration, system, usability, and acceptance testing—and manages regression, automation, and model-based work.

Management is a control activity: compare actual progress with the plan, identify risk early, adjust resources or scope, and keep evidence. A green test run is meaningful only when the build, environment, data, coverage, skipped cases, and defect status are known.

## Explanation
### 1. Test strategy
A **test strategy** states the overall approach: what will be tested, at which levels, with which techniques, by whom, in what environment, and with what exit criteria. It reflects product risk and quality goals. A strategy might emphasize:
- requirement and risk coverage;
- white-box control/data-flow coverage;
- black-box partitions/boundaries/combinatorial tests;
- OO state and collaboration tests;
- security, performance, usability, and recovery;
- exploratory testing for unknown risks;
- automation and continuous integration.

The strategy should name important quality attributes and residual-risk policy, not just tools.

### 2. Test planning
A **test plan** turns the strategy into an executable plan. It includes:
- objectives and scope, including out-of-scope items;
- test levels and deliverables;
- requirements/risk traceability;
- techniques and coverage goals;
- test cases, data, fixtures, and oracles;
- environment, tools, devices, network, and security controls;
- roles, responsibilities, training, and independence;
- schedule, milestones, estimates, and dependencies;
- entry/exit criteria and defect thresholds;
- automation, regression, and model-based approach;
- risks, assumptions, deliverables, and approval.

The plan is a living controlled document. Record changes and reasons; a changed requirement or environment can invalidate tests.

### 3. Documenting testing
Maintain:
- test strategy and plan;
- test case specifications and scripts;
- test data and setup/teardown instructions;
- requirement-to-test traceability;
- execution logs and coverage reports;
- defect reports and change history;
- test summary and release evidence;
- reusable procedures, lessons learned, and risk register.

A test report should state what ran, against which build, in which environment, with what data, what was skipped, what defects remain, and what risks are accepted. A simple “all passed” statement is insufficient.

### 4. Assigning responsibilities
Common roles include:
- **test manager/lead:** strategy, plan, coordination, metrics, and risk;
- **test designer/analyst:** derive cases and data from requirements/risk;
- **tester/executor:** execute, record, diagnose, and maintain tests;
- **developers:** unit tests, defect diagnosis, and fixes;
- **domain/security/operations specialists:** review and execute specialized scenarios;
- **independent test team:** unbiased system/acceptance evaluation for high risk;
- **product/customer representative:** acceptance and usability evidence.

Responsibility must be explicit. A developer should not be the only reviewer of a critical security requirement, and a tester should not decide a requirement's business meaning alone.

### 5. Test environments and data
Define development, integration, system, performance, security, and production-like environments. Control versions, configuration, clocks, locale, devices, network conditions, credentials, and external-service substitutes. Use representative data volume and distribution, but protect privacy. Refresh or reset state between tests; record which data is synthetic, sanitized, or production-derived.

### 6. Defect management
A defect record should include severity, priority, environment, build, steps, actual/expected result, evidence, affected requirement, reproducer, owner, status, and fix version. Triage separates:
- **severity:** impact of failure;
- **priority:** urgency of fixing it;
- **risk:** likelihood and consequence in the intended context.
A release may tolerate a known low-risk defect if the owner accepts and documents it; a critical security or data-loss defect usually cannot.

### 7. Entry and exit criteria
**Entry criteria** may include approved requirements, an integrated build, test environment readiness, test data, and resolved blocking setup defects. **Exit criteria** may include executed planned tests, agreed coverage, no unresolved critical/blocker defects, regression pass, performance/security thresholds, documentation, and stakeholder acceptance. A percentage of tests passed is not enough without coverage and defect status.

### 8. Regression testing
Regression checks that a change or fix did not break existing behavior. Select tests by:
- changed code and requirement impact;
- dependency and call-graph analysis;
- defect history;
- critical business and safety paths;
- recent releases and flaky tests.

Run a focused suite on every change and a broader suite before release. Keep regression tests stable, fast enough for continuous integration, and separate from exploratory tests. A new feature requires new tests and regression protection for old behavior.

### 9. Automating testing
Automation is valuable for repeated, deterministic, high-volume checks:
- unit and component tests;
- API/contract and integration smoke tests;
- build, static analysis, and deployment checks;
- regression suites;
- load/performance baselines;
- data migration and deployment checks.

Do not automate a test with no stable oracle or rapidly changing interface without addressing maintenance. Record automation coverage, runtime, flake rate, and maintenance cost. Keep exploratory and usability testing human-centered.

### 10. Model-based testing management
A model-based approach derives tests from a requirements/state/behavior model. Manage the model as a controlled configuration item with an owner, version, review, and link to requirements. Define model coverage, generated test count, seed/random strategy, and oracle. Reconcile model, code, and test discrepancies; do not update the model merely to pass a failing generated case.

## Worked examples
### Example 1: Test plan for a GPS app
The plan includes route functional cases, map/GP S boundaries, offline/network failures, performance at stated device load, location-permission tests, security of stored route data, and user navigation tasks. Unit tests cover route algorithms; integration tests cover map-provider contracts; system tests run on target phones. Exit requires no critical defects and the response-time threshold.

### Example 2: Regression selection
A change to a shared authentication library affects login, inspection submission, and supervisor access. The team uses dependency analysis to select auth unit tests, API contract tests, two end-to-end flows, and a negative authorization suite. Unrelated map rendering tests run nightly rather than blocking every commit. The risk-based selection is recorded.

### Example 3: Defect triage
A route calculation fails only on one supported device. Severity is high for that device but not for the whole system; priority depends on the number of users and workaround. The team records the build, logs, data, and reproducer, fixes it, runs device-specific regression, and updates the supported-device matrix.

### Example 4: Automation
A flaky timing test fails randomly and causes engineers to ignore CI. The team separates deterministic unit tests from performance tests, seeds data, controls clocks, and moves long load tests to a scheduled job. It does not simply rerun until green; the defect and test reliability issue are tracked.

## Key terms & formulas
- **Test strategy:** high-level approach to testing based on risk and goals.
- **Test plan:** controlled, executable plan of objectives, levels, resources, schedule, data, and criteria.
- **Test management:** planning, staffing, environment, execution, defect, metrics, and release control.
- **Entry criterion:** condition required before testing starts.
- **Exit criterion:** condition required before the level/release is accepted.
- **Regression test:** test that checks existing behavior after change.
- **Test automation:** executable tool/script execution of tests without manual steps.
- **Model-based testing:** test generation/selection from a system model.
- **Flake rate:** tests that fail intermittently without a code defect ÷ executed tests × 100%; a reliability metric.
- **Automation coverage:** automated tests ÷ selected repeatable tests × 100%.
- **Defect removal efficiency:** escaped defects ÷ total discovered defects × 100%; define escape point.
- **Test effectiveness (simple):** defects found before release ÷ total defects found × 100%.
- **Risk-based test selection score (qualitative):** likelihood × impact × coverage gap, used to prioritize cases.

## Common mistakes
- Writing a test plan with no entry/exit criteria or defect threshold.
- Assigning “everyone” without a named owner for each deliverable.
- Running all tests indiscriminately instead of using impact-based regression.
- Treating a passing automation job as proof when tests are skipped or flaky.
- Not recording environment/build/data, making failures impossible to reproduce.
- Automating unstable tests without fixing the oracle or synchronization.
- Updating a model to match a defect instead of investigating the requirement.
- Accepting an untested critical requirement because the average pass rate is high.

## Exam prep
### Likely 2-mark questions
1. **Define a test strategy.** Overall approach describing what, how, where, when, and why testing occurs.
2. **What is a test plan?** A controlled plan of test objectives, levels, cases, resources, schedule, environment, and criteria.
3. **Differentiate regression and smoke testing.** Regression checks old behavior after change; smoke checks a critical build can start and run basic paths.
4. **Why use risk-based regression?** Prioritize tests by impact, dependency, criticality, and change exposure.
5. **When is automation useful?** For stable, repeatable, high-volume checks; it reduces manual effort and supports CI.
6. **Define a test oracle.** A mechanism/source for expected results.
7. **Name four test-management activities.** Planning, documenting, staffing/assigning, defect management, regression, automation, metrics, or release control.

### Long-answer answer hints
- “Explain managing software testing”: strategy, plan, documentation, roles, environment/data, defects, regression, automation, model-based work, and release criteria.
- “Prepare a test plan for WMITS”: scope, levels, risks, cases, environment, people, schedule, metrics, entry/exit.
- “Explain regression testing and selection”: impact/dependency analysis, critical paths, defect history, focused and broad suites.
- “When should a test be automated?” stable oracle, repeatability, cost, maintainability, and CI benefit; mention limits.
- “Differentiate QA/QC and test management”: QA improves process; QC checks product; management coordinates resources and decisions.

### Management loop
```text
Plan → document → staff/environment → execute → report
  ↑                                              ↓
  └──── review metrics, defects, risk, change ───┘
```
