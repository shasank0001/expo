---
subject: oose
unit: 1
topic: concurrent-engineering-model
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Concurrent Engineering Model
## Overview
The concurrent engineering model runs several software-engineering activities at the same time rather than waiting for one phase to finish. Requirements, architecture, code, testing, manufacturing or deployment planning, and customer feedback are coordinated by cross-functional teams. The goal is to discover problems earlier and shorten the time needed to turn an idea into a usable product.

Concurrency does not mean doing everything without order. It means managing dependencies and intermediate results deliberately. A team may model a user interface while another team develops a data service, provided interfaces, assumptions, and review points are explicit. This model is also called integrated product development or parallel development in many textbooks.

## Explanation
### 1. Meaning and goal
In a sequential process, requirements are “finished” before design, design before coding, and coding before testing. In concurrent engineering, work streams overlap:
- requirements specialists discuss user goals with designers and developers;
- architects and implementers exchange information early;
- test engineers plan tests while requirements and design are being written;
- operational and support staff plan deployment and maintenance;
- customers see early prototypes and influence the next decisions.

The primary goal is **early defect discovery and shorter feedback cycles**. A late design error is more expensive because it affects many downstream artifacts.

### 2. Integration mechanisms
Concurrency needs more than a group chat. The team uses:
- interface specifications and prototypes;
- shared models and terminology;
- incremental baselines and configuration management;
- cross-functional reviews and walkthroughs;
- issue and risk lists;
- a build-and-test pipeline;
- scheduled integration points and a decision owner;
- shared quality criteria across design, code, and test.

A result is not integrated merely because it exists. It is integrated when its interface, dependencies, version, and acceptance status are known.

### 3. Typical activities
1. **Product and requirement definition:** domain experts, users, and engineers identify goals, constraints, and critical scenarios.
2. **Architecture and subsystem work:** component interfaces and data contracts are defined before all implementations are complete.
3. **Iterative prototype construction:** each team builds a slice that can be integrated and demonstrated.
4. **Continuous verification:** reviews, tests, simulations, and inspections run as artifacts appear.
5. **Integration management:** teams assemble components in a controlled environment, identify conflicts, and test end-to-end behavior.
6. **Release and operational planning:** deployment, training, monitoring, support, and maintenance are prepared in parallel.
7. **Feedback and replanning:** actual user and system data inform the next increment.

### 4. Advantages
- Problems and dependencies are found earlier.
- Stakeholders can give feedback before the entire product exists.
- Work can be parallelized when activities are separable.
- Integration problems are exposed before release.
- Teams can reuse models, components, and test assets across iterations.

### 5. Challenges
- Communication overhead increases; experts may work at different speeds.
- Concurrent changes can create incompatible assumptions.
- Integration can become a “big-bang” event if no working integration is maintained.
- Ownership of cross-component requirements and interfaces can be unclear.
- A fast prototype may tempt the team to skip documentation, quality work, or safety analysis.
- Resource loading can be unbalanced; one team may wait for another team’s interface.

### 6. Difference from agile iteration
Concurrent engineering is a broad process characteristic: overlapping work. Agile and incremental development can be concurrent, but the concepts are not identical. A concurrent model may be iterative, evolutionary, or plan-driven. It may have fixed milestones and a long integration phase, while an agile approach favors short iterations and frequent working increments.

## Worked examples
### Example 1: GPS navigation
A requirements team defines destinations and route accuracy; an algorithm team tests routing; a UI team builds screens; a database team handles maps; a test team creates safety and performance tests; operations staff plan updates. They share route-service interfaces and integrate a thin end-to-end path early. This exposes a slow map-loading problem before the complete product is finished.

### Example 2: Waste-management inspection
Inspectors use mobile screens, a central server records inspections, supervisors view dashboards, and analysts generate reports. Front-end, back-end, security, and testing work overlap, but the team fixes the inspection identifier and synchronization rules first. A weekly integration build catches a mismatch between mobile status values and supervisor displays.

### Example 3: A failed concurrent attempt
Two teams independently decide that a status is a number in one part and a string in another. No interface contract or integration test exists. The parallel work appears fast, but integration is delayed and a large defect emerges. The remedy is an agreed contract, shared examples, and frequent integration—not “more concurrency.”

### Example 4: Parallel release preparation
While developers stabilize the final GPS route algorithm, documentation writers prepare user instructions, the operations team creates backup procedures, and the security team performs a threat review. The release is more coherent because these activities are planned together.

## Key terms & formulas
- **Concurrency:** overlapping execution of activities or work streams.
- **Cross-functional team:** people with different specialties working together on a product outcome.
- **Integrated product development:** coordinated parallel development of product, process, and supporting activities.
- **Interface contract:** an agreed definition of data, services, errors, timing, and compatibility between components.
- **Integration point:** a planned point at which independently developed parts are combined and verified.
- **Build-and-test pipeline:** automated sequence that compiles, tests, and packages a working candidate.
- **Concurrency time savings (conceptual):** elapsed time can fall when work streams overlap, but savings occur only if dependencies and coordination are managed.
- **Dependency:** work that cannot start or safely finish until another artifact or decision is available.

## Common mistakes
- Assuming concurrency means every team starts at the same time regardless of dependencies.
- Calling a group of people a cross-functional team without shared goals or decision rights.
- Integrating only at the end.
- Allowing parallel teams to use inconsistent models, terminology, or version numbers.
- Confusing overlap with less planning; concurrent work needs more interface and configuration control.
- Claiming concurrency always reduces schedule; unresolved communication can increase it.

## Exam prep
### Likely 2-mark questions
1. **What is the concurrent engineering model?** A process in which multiple engineering activities and specialist teams work in parallel with coordination.
2. **State one main benefit.** Early discovery of interface, design, and dependency problems.
3. **How are teams coordinated?** Through shared models, interface contracts, frequent integration, reviews, and configuration management.
4. **Differentiate concurrency from incremental delivery.** Concurrency concerns overlapping activities; incremental delivery concerns successive usable releases.
5. **Give one GPS example.** Route, map, interface, testing, and deployment teams develop against a common route-service contract.

### Long-answer answer hints
- “Explain concurrent engineering with diagram”: show parallel requirements, design, code, test, and deployment streams joining at an integration/release node; explain controls.
- “Compare concurrent engineering with waterfall”: overlap and early feedback versus mostly sequential phases; discuss risk and coordination.
- “How can a team avoid big-bang integration?” stable contracts, working increments, automated tests, frequent integration, and version control.
- “Advantages and challenges of cross-functional teams”: speed and shared ownership versus communication and resource problems.
- “Apply to a WMITS case study”: list parallel work streams and the interface that must be agreed first.

### Text sketch
```text
Requirements ─┐
Architecture ─┼─ shared contracts → integration build → system/release
Implementation┤
Testing ──────┘
Deployment/maintenance preparation ───────────────↑
```
