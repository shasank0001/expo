---
subject: oose
unit: 5
topic: software-testing-overview
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Software Testing Overview
## Overview
Software testing is the systematic process of showing, as far as practical, that a product meets its intended requirements and behaves correctly under relevant conditions. Testing is not proof that software has no defects; it is planned evidence about risk, behavior, and quality. Defects can still remain, but important requirements and failure risks should be exercised and the results understood.

Testing includes reviews and inspections as well as executing a program. It uses black-box knowledge from requirements, white-box knowledge of code and control flow, and—when useful—gray-box knowledge of implementation. The level of testing moves from components to the integrated system, and the strategy must fit the application type, architecture, and quality goals.

## Explanation
### 1. Goals of testing
Testing aims to:
- determine whether specified behavior is implemented correctly;
- find failures before release;
- measure quality and risk;
- provide information for defect correction and process improvement;
- verify that changes did not break existing behavior;
- support acceptance, certification, and contractual decisions;
- increase confidence in security, performance, usability, and reliability.

Testing cannot prove the absence of all defects. It can only identify conditions under which the product fails and document the evidence gathered.

### 2. Verification and validation
- **Verification:** “Are we building the product right?” Compare the product with the design, specifications, and standards—does the implemented function meet its intended structure and behavior?
- **Validation:** “Are we building the right product?” Check the product with real users and real tasks in the intended environment—does it satisfy the need?
Both are needed. A correctly calculated result can be the wrong result for the user’s goal.

### 3. Testing levels
#### Component/unit testing
Tests an individual class, function, module, or component in isolation. Stubs and mocks provide collaborators. It finds local logic and boundary defects quickly.

#### Integration testing
Tests interactions among components and subsystems. It catches interface, data-format, sequencing, transaction, and assumption errors that unit tests cannot.

#### System testing
Tests the complete integrated product against its requirements and quality criteria, including functional, performance, security, reliability, recovery, installation, and compatibility behavior.

#### Acceptance testing
Users or authorized stakeholders decide whether the product is suitable for its purpose. Alpha, beta, user-acceptance, and operational-acceptance testing differ in who conducts them and what they decide.

#### Usability testing
Observes representative users performing realistic tasks. It measures learnability, time, errors, satisfaction, accessibility, and recovery, not merely preference.

### 4. Black-box, white-box, and gray-box testing
**Black-box testing** derives tests from requirements, interfaces, scenarios, and expected outputs. It does not require the source code and is useful for acceptance and black-box contracts.

**White-box testing** uses internal structure: statements, branches, conditions, data flow, loops, and paths. It derives test cases from code/flow graphs and is especially useful for unit and control-flow coverage.

**Gray-box testing** combines a black-box requirement view with limited white-box knowledge, such as a database schema, query, or code path. It can find issues hidden by a pure black-box test without depending on every implementation detail.

### 5. Static and dynamic testing
- **Static testing/reviews:** inspect requirements, models, code, documents, and plans without running the program. Examples: walkthrough, inspection, static analysis.
- **Dynamic testing:** execute the software with inputs and observe outputs, states, timing, resources, and side effects.
Both catch different defect classes; static review is often cheaper for requirements and design defects, while dynamic tests are needed to observe actual behavior.

### 6. The testing process
A practical process is:
1. define test objectives, scope, risks, and quality criteria;
2. review requirements and design to derive tests;
3. plan levels, environments, data, people, schedule, and entry/exit criteria;
4. implement test cases, scripts, fixtures, and test oracles;
5. execute and record results;
6. report and prioritize defects;
7. correct the product and rerun affected/regression tests;
8. summarize evidence, residual risk, and release recommendation;
9. archive tests and feed lessons into the next process.

### 7. Test case and test oracle
A test case states purpose, preconditions, inputs/data, steps, expected result, priority, environment, and requirement links. A **test oracle** determines the expected result and compares it with actual behavior. An oracle may be a known value, invariant, mathematical formula, reference implementation, database constraint, or human judgment. A weak oracle makes test execution hard to interpret.

### 8. Coverage
Coverage is the extent to which a test set exercises specified behavior or structure. Examples:
- statement coverage;
- branch/decision coverage;
- condition and condition/decision coverage;
- path coverage;
- data-flow/definition-use coverage;
- use-case and requirement coverage;
- security, performance, and usability scenario coverage.

Coverage percentage alone is not proof of quality. A high-coverage test set may miss an important requirement, while a low percentage may intentionally exclude untestable or low-risk code. State what was measured, what was excluded, and what risk remains.

### 9. Testing conventional and object-oriented applications
Conventional applications often have procedures, single-path control flow, and traditional black-box/white-box techniques. Object-oriented systems add:
- state distributed across collaborating objects;
- inheritance and dynamic dispatch;
- polymorphism and late binding;
- shared services and side effects;
- reuse that can propagate a defect;
- event/message and concurrency behavior.

OO testing therefore combines scenario/use-case tests, class/contract tests, state and interaction tests, subsystem tests, and regression/impact analysis. Testing only a method in isolation can miss an invalid collaboration.

### 10. Testing ethics and evidence
A tester should not hide failures, weaken a test to make a schedule, or report a green result without noting skipped/disabled cases. Test evidence is meaningful only if the environment, build, data, and coverage are known. A release decision includes residual risk, not just a pass count.

## Worked examples
### Example 1: Requirements test
For “95% of route requests complete within two seconds,” a test creates the stated workload and records response times. A functional test verifies the route, a boundary test uses maximum supported waypoints, and a failure test uses an unavailable map provider. A black-box tester can derive most cases; a white-box tester checks the timeout and error branches.

### Example 2: Unit and integration defect
A `Route` class calculates distance correctly in unit tests, but an integration test finds that the route API returns kilometres while the view expects metres. The defect is an interface/unit mismatch. The team adds a contract test and clarifies the data schema. The lesson is that unit success is not system correctness.

### Example 3: Usability evidence
Five representative inspectors attempt a standard inspection. Four complete it without assistance; one cannot recover from a rejected photo. The result is evidence for usability improvement, not a single subjective “the UI is good.” Test records include tasks, participants, time, errors, and comments.

### Example 4: Regression risk
Changing a shared validation component may affect registration, inspection submission, and login. The team traces its clients and runs a targeted regression suite plus representative end-to-end tests. Broad regression is selected by impact analysis, not by running every test blindly.

## Key terms & formulas
- **Test:** an activity with a controlled input and observed result.
- **Test case:** documented conditions and expected outcome.
- **Test oracle:** mechanism for deciding expected correctness.
- **Verification:** conformance to specified design/requirements.
- **Validation:** fitness for actual user need.
- **Defect/fault/bug:** a condition causing a departure from required behavior; terminology may distinguish a latent fault from its observed failure.
- **Coverage:** measured proportion of specified behavior/structure exercised.
- **Cyclomatic complexity:** often `V(G) = predicates + 1` for a connected flow graph.
- **Statement coverage:** executed statements / total statements × 100%.
- **Branch coverage:** decision outcomes exercised / total decision outcomes × 100%.
- **Defect density:** defects ÷ size, with severity and size metric stated.
- **DRE (Defect Removal Efficiency):** escaped defects ÷ (pre-release + escaped defects) × 100%; use with a consistent escape definition.
- **Test adequacy risk:** untested requirement/condition count ÷ applicable requirement/condition count × 100%, preferably severity-weighted.

## Common mistakes
- Saying testing proves a program is defect-free.
- Confusing verification and validation or unit and system testing.
- Testing only the happy path and normal inputs.
- Calling code executed “covered” without stating statement, branch, path, or requirement coverage.
- Writing tests with no expected result or no requirement link.
- Treating a passing unit test suite as proof of a working integrated system.
- Running every regression test without considering impact and risk.
- Hiding skipped tests and environmental failures from release evidence.

## Exam prep
### Likely 2-mark questions
1. **Define software testing and state its limitation.** Systematic evidence of behavior against requirements; it cannot prove absence of all defects.
2. **Differentiate verification and validation.** Verification checks conformance to specified design; validation checks fitness for real user need.
3. **Name three testing levels.** Unit/component, integration, system, acceptance, or usability—any three.
4. **Differentiate black-box and white-box testing.** Requirements/interfaces versus internal code/control structure.
5. **What is a test oracle?** A source of expected results used to compare actual behavior.
6. **Give two kinds of coverage.** Statement, branch, condition, path, data-flow, use-case, security—any two.
7. **What is gray-box testing?** Black-box requirements plus limited internal knowledge such as schema or code paths.

### Long-answer answer hints
- “Explain software testing overview”: goals, verification/validation, levels, methods, process, oracle, coverage, defects, and OO considerations.
- “Compare black-box, white-box, and gray-box”: basis, strengths, limitations, and appropriate levels.
- “Explain test planning”: objectives, scope, levels, techniques, data, environment, people, schedule, entry/exit, and risks.
- “Why does OO testing need different techniques?” state, polymorphism, collaboration, side effects, reuse, and dynamic dispatch.
- “Why is coverage not quality?” describe what it does and does not prove, and pair it with risk and requirement coverage.

### Test evidence frame
```text
Requirement/risk → test level/technique → data + oracle → result
              → defect/change → regression evidence → residual risk
```
