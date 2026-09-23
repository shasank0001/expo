---
subject: oose
unit: 1
topic: phased-release-model
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Phased-Release Model
## Overview
The phased-release model develops a system in a planned sequence of releases. Each release adds a usable portion of the product, often called an increment. The first release may solve a narrow problem; later releases add functions, improve quality, and broaden the user base. Planning defines what belongs to each release, while user and operational feedback influences the next one.

It is a practical middle ground between a single, late delivery and continuous prototyping. The product can be deployed incrementally, but the team should preserve a stable architecture and control compatibility. The approach is especially useful for systems that can be valuable with only part of the full feature set.

## Explanation
### 1. Meaning of phased release
A release is a coherent, tested version delivered to users or a deployment environment. In a phased-release process, the team decomposes the required system into functionally complete phases. Each phase is planned, developed, tested, accepted, and then followed by another phase.

Phases may be:
- **Incremental:** each release extends the previous one.
- **Evolutionary:** requirements and design continue to change as the team learns.
- **Scheduled or planned releases:** delivery dates and functionality are fixed in advance.

The terminology is sometimes used loosely. The important idea is controlled evolution through usable versions, not merely sending a different build every week.

### 2. Steps in the process
1. **Identify the total product vision:** list essential goals, constraints, and future possibilities.
2. **Select the first usable release:** choose the smallest coherent set of functions that solves a valuable problem.
3. **Order requirements by value and dependency:** place foundational services before functions that depend on them.
4. **Design for change:** use interfaces, modular structure, database migration strategies, and compatibility rules so later releases can add behavior.
5. **Develop and test one phase:** apply requirements, design, implementation, and tests for that release.
6. **Release and observe:** collect usage, defect, performance, and user feedback.
7. **Plan the next phase:** update the backlog, risk list, and release criteria; obtain approval; repeat.

### 3. Planning a phase
Each release needs an entry criterion, a scope, exclusions, dependencies, acceptance criteria, quality thresholds, rollback plan, and data-migration plan. For example, Release 1 may support text-only chat and single-device login, while voice/video and group administration are explicitly deferred. This prevents “phase 1” from becoming an accidental promise of the whole system.

### 4. Advantages
- Users receive value earlier instead of waiting for the entire system.
- Stakeholders can react to real behavior before all decisions are made.
- Delivery is divided into manageable increments.
- Early releases can reveal technical, adoption, and performance risks.
- The team can prioritize urgent, high-value requirements.

### 5. Difficulties and safeguards
- **Scope creep:** use a visible product backlog, release baselines, and change control.
- **Architecture churn:** establish architectural principles and an extensible foundation early.
- **Data migration:** preserve old data, write conversion scripts, and test upgrade and rollback.
- **Duplicate effort:** an early release may need rework if a core design is weak.
- **Operational complexity:** support, monitoring, security, and user training must be ready for every release.
- **Compatibility:** clients and servers may be temporarily out of step; use versioned interfaces and migration rules.

### 6. Relationship to other models
A phased-release model is a planned form of incremental development. It is more predictable than an entirely opportunistic or uncontrolled evolutionary process, but less formal than a single fixed waterfall release. A spiral model may add risk-driven planning around each release. In practice, teams often combine a stable architecture with iterative releases.

## Worked examples
### Example 1: Instant messaging system
Release 1 offers registration, login, one-to-one text messages, and delivery status. Release 2 adds group chats. Release 3 adds file sharing and online status. A new message table and an API version are designed early so the team can add features without replacing all data.

### Example 2: GPS navigation
Release 1 supports map browsing and route calculation for one region. Release 2 adds live traffic and voice guidance. The team must decide whether an older client can use a new routing service. It keeps the route interface backward compatible and tests a device with limited memory.

### Example 3: Bad phased plan
A team calls a partially implemented system “Release 1” but does not test failure handling, authorization, or data upgrade. Users cannot register existing students, so the release is not coherent. A phase should be usable and accepted, not just a date on a slide.

### Example 4: Feedback
After the first release, few students use the mobile interface. The team investigates navigation and performance, then reprioritizes the next phase. The change is a controlled response to evidence, not an excuse to abandon planning.

## Key terms & formulas
- **Release:** an accepted, deployable version of a product.
- **Phase:** one planned part of a multi-release delivery.
- **Increment:** a functional slice added to the product.
- **Product backlog:** an ordered, visible list of candidate requirements and fixes.
- **Release baseline:** the agreed set of features and behavior for a release.
- **Backward compatibility:** a new version can work with an older interface or data format.
- **First usable release:** the smallest coherent release that delivers measurable value.
- **Release burndown:** the planned scope remaining for a release; it should be visible, not hidden.
- **Change acceptance rate (a simple project measure):** accepted changes ÷ proposed changes; track alongside quality, not as a target to maximize blindly.

## Common mistakes
- Treating a release as a collection of half-finished functions.
- Delaying all user feedback until the final product.
- Forgetting that a release includes documentation, migration, security, and support.
- Assuming phased release means no planning or no architecture.
- Promising a feature in a later phase without dependencies or acceptance criteria.
- Confusing a phased release model with a waterfall model: the former delivers in usable versions; the latter emphasizes a mostly fixed phase sequence.

## Exam prep
### Likely 2-mark questions
1. **Define a phased-release model.** A process that develops and delivers a system in planned, usable releases or increments.
2. **Give two advantages.** Earlier value, better feedback, manageable work, and earlier risk discovery are valid.
3. **How is the first release selected?** From a valuable coherent set of functions with clear dependencies and acceptance criteria.
4. **Name one technical safeguard for later changes.** Versioned interfaces, modular architecture, data migration tests, or backward compatibility.
5. **Differentiate a phased release from a single final delivery.** A phased release gives users working versions at planned intervals.

### Long-answer answer hints
- “Explain the phased-release model”: show phases from vision to first usable release, subsequent releases, feedback, and replanning; include inputs and outputs.
- “Compare phased release with waterfall”: incremental usable delivery and learning versus fixed sequential phases; discuss control and rework.
- “How do you plan Release 2?” re-evaluate backlog value, dependencies, defects, risks, architecture, capacity, and acceptance criteria.
- “Challenges of phased delivery”: scope creep, architecture churn, migration, compatibility, support, and testing; suggest safeguards.
- “Use an example from the syllabus”: split a chat or GPS system into credible phases and justify the order.

### Simple release text sketch
```text
Vision → Release 1 (core use) → feedback → Release 2 (more value) → feedback → …
              ↑ test, deploy, measure, support ↑ test, deploy, measure, support
```
