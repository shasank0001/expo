---
subject: oose
unit: 5
topic: orthogonal-array-testing-and-testing-activities
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Orthogonal Array Testing and Testing Activities
## Overview
Orthogonal-array testing (OAT) and pairwise/combinatorial testing choose a compact set of combinations when many inputs or configurations must work together. The second half of this note covers the syllabus testing activities: component inspection, usability testing, unit testing, integration testing, and system testing. Each activity has a different scope, object, environment, and evidence.

These topics are combined in one file because both concern efficient, planned coverage across test levels. OAT is not a replacement for domain-specific boundary, security, usability, or failure tests; it is a way to explore combinations economically.

## Explanation
### 1. Orthogonal-array testing
#### Context
A system may depend on many factors: browser, operating system, locale, screen size, database, payment provider, or user role. Testing every Cartesian combination is impossible. Orthogonal arrays choose runs in which levels of different factors are distributed evenly and, ideally, every pair of levels occurs.

#### Strength
For an orthogonal array of strength `t`, every combination of levels for any `t` factors appears at least once. **Pairwise testing** is the common case `t = 2`: every pair of factor levels is covered. This catches interaction defects much more efficiently than one-factor-at-a-time testing.

#### Factors and levels
A **factor** is an input/configuration dimension. Its **levels** are possible values. Examples:
- browser: Chrome, Firefox, Safari;
- locale: en-IN, hi-IN;
- network: fast, slow, offline;
- user role: inspector, supervisor.

A run selects one level for every factor. The array must respect dependencies and illegal combinations; an invalid combination is not made “valid” merely because the array includes it.

#### Selecting an array
1. List factors and levels from requirements and risk analysis.
2. Remove duplicates or fixed factors and identify dependencies.
3. Choose the desired strength, usually pairwise for configuration testing.
4. Find a standard array of the required size or construct one.
5. Remove invalid runs and add targeted valid cases.
6. Run the matrix, record failures, and add boundary/edge/security tests.
7. Treat a failure as a possible defect, not as an invalid test automatically.

A simple pairwise example with two factors and two levels can be:

| Run | Browser | Locale |
|---:|---|---|
| 1 | Chrome | en-IN |
| 2 | Chrome | hi-IN |
| 3 | Firefox | en-IN |
| 4 | Firefox | hi-IN |

Four runs cover every browser/locale pair. With three factors and two levels, four pairwise runs may cover all pairs, but not all eight three-way combinations; state the strength honestly.

#### Limitations
- Pairwise coverage may miss three-way or higher interactions.
- Invalid or impossible combinations complicate construction.
- A factor may have many levels, increasing the array.
- Real workloads, timing, and data distributions are not represented by level labels.
- Critical business rules need dedicated scenarios and security tests.

### 2. Testing activities
The testing activities are organized by scope. A defect found early is usually cheaper to fix, and evidence should accumulate from local behavior to complete-system fitness.

#### Component inspection
Inspection examines a component's code, design, interfaces, and test material without executing it. It can include:
- code review for logic, security, performance, and style;
- design/interface review;
- checklist and walkthrough;
- static analysis;
- peer inspection.

Inspection is effective for defects that are easier to see in structure than in a particular input, such as an unreachable branch, duplicated validation, or unsafe API. Inspections need defined entry/exit criteria and defect records; a casual read is not a quality process.

#### Usability testing
Usability testing observes representative users performing realistic tasks with the product. Prepare:
- participant profile and consent/ethics;
- realistic tasks and environment;
- task instructions that do not lead the user;
- measures: completion, time, errors, assistance, satisfaction, accessibility;
- observations, comments, and severity of usability problems.

Test early prototypes and final builds. Do not confuse a preference survey with task observation. A user who cannot complete a required task is evidence of a usability defect even if they say the screen looks attractive.

#### Unit testing
Unit/component tests exercise a class, function, or module in isolation. They are written close to the code, use stubs/mocks/fakes for collaborators, and focus on:
- normal and exceptional operations;
- boundary values;
- invariants and error handling;
- state transitions and inheritance/polymorphism;
- performance or security checks when locally relevant.

A good unit test is fast, repeatable, isolated, named by behavior, and asserts an observable result. A test that only mirrors the implementation or uses excessive mocking can be brittle.

#### Integration testing
Integration tests verify interactions among components and subsystems. They focus on:
- interface signatures, data formats, units, and error mapping;
- order and timing of messages;
- database transactions and persistence;
- authentication/authorization across boundaries;
- resource cleanup and error recovery;
- behavior when a service is slow, unavailable, or returns an invalid response.

Strategies:
- **top-down:** build/control from the upper level with stubs for lower components, then replace stubs;
- **bottom-up:** test lower components first and integrate upward;
- **sandwich/big-bang:** combine both approaches, often with a controlled integration build; pure big-bang delays discovery.
The strategy depends on dependencies, risk, and ability to create test doubles.

#### System testing
System testing treats the integrated product as a complete system in an environment close to production. It includes:
- end-to-end functional use cases;
- external interfaces and interoperability;
- performance, load, stress, volume, and resource behavior;
- security and privacy;
- reliability, recovery, backup, and failover;
- installation, configuration, compatibility, and upgrade/migration;
- usability and operational acceptance where relevant.

System tests require a production-like environment, controlled data, independent expected results, and a release decision. A system test that only repeats happy-path unit tests misses integration and operational risk.

### 3. Activity sequence and evidence
A plan may progress from inspection → unit → integration → system → usability/acceptance, but activities overlap in iterative processes. Each level has:
- scope and risks;
- entry criteria;
- test cases and data;
- environment and tools;
- responsibilities;
- exit criteria and defect threshold;
- evidence and traceability.

## Worked examples
### Example 1: Orthogonal array for WMITS
Factors: device (phone/tablet), network (fast/offline), user role (inspector/supervisor), photo format (JPEG/PNG). A pairwise array of 8 runs covers every pair of levels. Illegal combinations, such as a supervisor submitting a new field inspection if the requirement forbids it, are removed and replaced with a valid targeted case. A separate test checks a large image and unauthorized access.

### Example 2: Component inspection
A reviewer finds that a repository method updates an inspection but does not write the required audit event. The issue is visible in the component contract and exception path. The team adds an inspection checklist and a unit test before integration, reducing later rework.

### Example 3: Unit-to-integration defect
Unit tests for `Inspection` pass. Integration reveals that the service returns a status enum name while the UI expects a numeric code. A contract test fails and the interface is corrected. This demonstrates why levels are complementary.

### Example 4: Top-down integration
The mobile login flow is tested with a fake identity server. Once the boundary is stable, the real test server is substituted. The team can validate control flow early without waiting for every lower subsystem, but it also checks that the fake accurately represents the protocol.

### Example 5: System performance
A system test runs 500 concurrent users, measures response time, errors, memory, and database saturation. The release is blocked if 95% of requests fail the agreed threshold. A stress test increases load until the limit is identified, and a recovery test verifies the system returns to service.

## Key terms & formulas
- **Factor:** independent input/configuration dimension.
- **Level:** one possible value of a factor.
- **Orthogonal array:** test matrix with balanced level combinations.
- **Strength `t`:** every combination of `t` factor levels appears at least once.
- **Pairwise testing:** strength-2 coverage.
- **Run:** one selected level for every factor.
- **Cartesian product:** all combinations; for `k` factors with `nᵢ` levels, size `∏ nᵢ`.
- **Component inspection:** static review of a component and its artifacts.
- **Unit test:** isolated module/class test.
- **Integration test:** interaction test among components.
- **System test:** complete-product test in a realistic environment.
- **Pairwise coverage:** pairs executed ÷ pairs required × 100%.
- **Unplanned test percentage:** unplanned tests ÷ total executed tests × 100%; investigate rather than hide.
- **Test level defect escape rate:** defects found at a level ÷ defects found at or after that level × 100%, used to improve planning.

## Common mistakes
- Assuming pairwise coverage includes every three-way interaction.
- Including impossible combinations without a rule for expected behavior.
- Calling one-factor-at-a-time testing orthogonal.
- Treating inspection as optional or unstructured.
- Testing a unit with so many real dependencies that it is an integration test.
- Delaying all integration until a big-bang release.
- Running system tests in a development environment with unrealistic data or load.
- Reporting pass counts without scope, environment, coverage, and defects.

## Exam prep
### Likely 2-mark questions
1. **What is orthogonal-array testing?** Selecting a compact set of combinations so factor levels are balanced and pairs (or higher-order combinations) are covered.
2. **Define pairwise testing.** A combinatorial method that covers every pair of factor levels.
3. **List five testing activities.** Component inspection, usability, unit, integration, and system testing—any five.
4. **Differentiate unit and integration testing.** Unit tests one component in isolation; integration tests interactions between components.
5. **What is top-down integration?** Integrates from the upper/control level, using stubs for lower components and replacing them later.
6. **What does system testing examine?** The complete integrated product against requirements and quality criteria in a realistic environment.
7. **Why inspect components?** Find structural, interface, security, and logic defects before execution and at lower cost.

### Long-answer answer hints
- “Explain OAT”: factors, levels, strength, pairwise coverage, array construction, invalid combinations, and limitations.
- “Explain testing activities”: scope, technique, environment, evidence, and defects for inspection, usability, unit, integration, and system.
- “Compare top-down, bottom-up, and sandwich integration”: stub/driver use, dependency order, timing, and risk.
- “Design a test strategy for WMITS”: array for configurations, inspection, unit rules, integration contracts, system/load/security, usability.
- “Explain why no single level is enough”: local correctness, collaboration, complete behavior, and real-user/operation are different questions.

### Pairwise sketch
```text
Factor A: a1 a2
Factor B: b1 b2
Factor C: c1 c2
Choose a standard array so each pair (A,B), (A,C), (B,C) occurs.
```
