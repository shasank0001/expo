---
subject: oose
unit: 1
topic: evolutionary-model
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Evolutionary Model
## Overview
The evolutionary model develops a system in successive versions while requirements and design continue to change from user and technical feedback. The first version implements a useful subset; later versions add functions and improve quality. Unlike a fixed waterfall plan, the model expects the product to mature through repeated delivery and use.

Evolutionary development is valuable when a domain is difficult to specify completely before implementation. It gives stakeholders something concrete to react to and helps the team discover hidden requirements. The cost is continual planning, compatibility work, and the need to control scope and quality.

## Explanation
### 1. Meaning
An **evolutionary model** treats a software product as something that changes through a sequence of valid versions. Each version may be:
- a complete early product for a small scope,
- an operational release with a few features,
- a prototype converted into production incrementally, or
- a maintenance release that fixes defects and adds functions.

The team does not wait until every requirement is perfect. It delivers a baseline, observes real use, and uses the evidence to revise the product.

### 2. Basic steps
1. Establish the overall problem, constraints, and long-term vision.
2. Select an initial scope that is valuable, demonstrable, and technically plausible.
3. Develop the first version through requirements, design, coding, and testing.
4. Deliver it to a controlled group of users or a target environment.
5. Collect feedback, defect reports, performance data, and new requirements.
6. Analyze and prioritize the proposed changes.
7. Develop the next version while maintaining the architecture and data of earlier versions.
8. Repeat until the agreed product boundary is reached or maintenance takes over.

### 3. Evolutionary versus incremental development
**Incremental** delivery usually has a planned order of features; **evolutionary** delivery permits the product and its requirements to change based on learning. Many real projects use both: they release planned increments, then evolve the backlog after feedback.

### 4. Prototyping and prototypes
A prototype is an early model used to explore a hard requirement or technology. A throwaway prototype answers a question and may be discarded. An evolutionary prototype is refined into the product, so its code, data model, interfaces, and tests must be controlled. The team should state the purpose before building so that a quick demonstration is not mistaken for production-ready software.

### 5. Strengths
- Users can react to a working system rather than only documents.
- Hidden requirements and technical constraints are discovered early.
- The team can prioritize high-value functions using evidence.
- A usable increment can be delivered before the entire product is complete.
- Feedback can improve usability, architecture, and test cases.

### 6. Weaknesses
- Requirements, schedule, and cost can change continually.
- Poorly controlled versions may become difficult to maintain.
- A prototype may be mistaken for a finished system and deployed without hardening.
- Frequent changes can destabilize the architecture and data.
- Teams can focus on visible features and postpone security, performance, and maintenance work.
- Without a baseline and version policy, users may not know what is supported.

### 7. Controls needed
Use an architecture that is modular and open to extension, a prioritized backlog, release baselines, configuration management, automated regression tests, migration plans, and a clear definition of “done.” A product owner or change authority decides whether a proposed change is worth the cost. The team should maintain traceability from each release decision to feedback and requirements.

## Worked examples
### Example 1: Chat system
Release 1 supports login and one-to-one text messages. Students report that group messages and delivery status are more valuable than voice calls. The team adds group chat in Release 2 and delays voice until network capacity is proven. The system evolves while preserving message compatibility.

### Example 2: GIS inspection application
An initial version lets inspectors submit forms online. Field users show that offline operation is essential. The next version adds local storage and synchronization. Because later versions will depend on the same inspections, the team defines stable IDs and conflict rules early.

### Example 3: Prototype trap
A manager likes a colorful prototype that performs simulated GPS routing. It has no real map data, no error handling, and no secure user accounts. It is useful for discussing screens but not for deployment. The team labels it a prototype, tests the navigation service separately, and plans production work.

### Example 4: Scope decision
Users request video, chat, maps, and payments for a student app. The team ranks value and risk, delivers the core navigation and inspection functions first, and records later requests in the backlog. A change is not rejected; it is scheduled when its value and dependencies justify it.

## Key terms & formulas
- **Evolutionary development:** repeated delivery and refinement in response to feedback and learning.
- **Version:** a distinguishable, documented product state.
- **Prototype:** a model used to explore, demonstrate, or validate behavior.
- **Evolutionary prototype:** a prototype deliberately evolved toward the real product.
- **Throwaway prototype:** a prototype created for learning and not intended for production.
- **Backlog:** an ordered list of desired changes and defects.
- **Change impact:** the effect of a new version on users, data, interfaces, tests, and operations.
- **Feedback loop:** deploy → observe → decide → change → test → deploy again.
- **Release frequency:** number of releases in a period; it is a delivery indicator, not by itself a quality measure.

## Common mistakes
- Calling every iterative model evolutionary without explaining feedback-driven change.
- Assuming evolution means requirements never need a baseline.
- Building a prototype and releasing it without production testing, security, and support.
- Confusing a user-visible change with a complete, maintainable version.
- Ignoring backward compatibility and data migration between versions.
- Promising a final date despite the model’s intentionally open scope.

## Exam prep
### Likely 2-mark questions
1. **Define the evolutionary model.** A process that develops a system in successive versions as requirements and design are refined through feedback.
2. **Give two advantages.** Early usable delivery, user feedback, discovery of hidden requirements, and prioritization of value.
3. **What is a throwaway prototype?** A prototype built to answer a question and then replaced by a production implementation.
4. **Why is configuration management important?** Versions, code, data, and tests must remain identifiable and compatible as the product changes.
5. **How does evolution differ from a fixed waterfall plan?** It explicitly accepts change and learns from delivered versions rather than assuming requirements remain stable.

### Long-answer answer hints
- “Explain the evolutionary model with diagram”: vision → first version → feedback → next version; mention architecture, testing, configuration, and maintenance.
- “Compare evolutionary and incremental development”: fixed planned increments versus learning-driven changes; state that real projects combine them.
- “Advantages and disadvantages of evolutionary development”: user feedback and early value versus scope drift, instability, and maintenance cost; give controls.
- “How can a prototype support evolution?” explain prototype purpose, validation, evolution into production, or replacement with production code.
- “Use the chat/GPS case study”: show a sequence of releases and justify the next version from evidence.

### Text sketch
```text
Initial scope → Version 1 → user/technical feedback → Version 2 → feedback → Version 3
      ↑             │               │                  │              │
   scope/architecture controls, configuration management, regression testing, support
```
