---
subject: oose
unit: 1
topic: opportunistic-model
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Opportunistic Model
## Overview
The opportunistic model is a less formal process model in which the team starts with a general idea and uses judgment, experience, and available opportunities to decide the next development steps. Unlike a fixed waterfall plan or a risk-driven spiral, it does not begin with a complete, rigid sequence. It is sometimes called the “chaos model” in Pressman’s classification.

This model can be creative and responsive, especially in exploratory or creative work. It is also risky: without goals, constraints, and quality criteria, the project can become a collection of quick decisions. The process is therefore most defensible when the team makes its assumptions visible, reviews frequently, and keeps enough documentation to make the resulting system understandable.

## Explanation
### 1. Meaning
In an opportunistic process, the team does not first construct a detailed schedule containing every activity. It works toward a broad objective, identifies an opportunity or obstacle, and chooses a response based on experience. A prototype may lead to a feature, a bug may lead to redesign, and a new tool may lead to a new development approach.

The model does not mean “no engineering.” It means the process is **emergent** rather than fully predefined. The team still needs requirements, design, testing, version control, stakeholder communication, and acceptance criteria. What changes is the degree of upfront planning.

### 2. Typical behavior
1. Start with a vision, a broad problem, and a few high-priority goals.
2. Explore the domain and build a rapid prototype or proof of concept.
3. Observe technical, user, and organizational feedback.
4. Select the next opportunity—new functionality, performance improvement, market change, or a discovered defect.
5. Develop and test the selected change.
6. Integrate it with the existing product and review the result.
7. Continue until the product reaches its intended boundary or the opportunity is exhausted.

This resembles reactive programming or opportunistic scheduling, but it is a process choice rather than a programming language feature.

### 3. Appropriate contexts
- A proof of concept where users or sponsors need to see something quickly.
- A research or exploratory project with uncertain technology.
- A creative product where requirements and the best solution emerge through experiment.
- A small startup team that can maintain a working version while learning.
- A reusable component or tool that benefits from trying several technical approaches.

It is less suitable for a safety-critical system, a fixed-price contract with strict deliverables, or any project where auditability and reproducibility are more important than rapid discovery unless the team adds strong controls.

### 4. Strengths
- Reacts quickly to new information and opportunities.
- Encourages innovation, prototypes, and creative problem solving.
- Avoids investing heavily in a plan that may become obsolete.
- Allows a small usable result to appear early.
- Makes direct user feedback part of the process.

### 5. Weaknesses and remedies
- **Unclear scope:** write the vision, current decision horizon, exclusions, and success criteria.
- **Inconsistent architecture:** use interface contracts, architectural principles, code review, and a change board.
- **Lost history:** keep decision logs, issue records, version notes, and a decision log for prototypes.
- **Insufficient testing:** make test design and risk review mandatory, not an afterthought.
- **Team overload:** rotate work, limit work in progress, and assign an integration owner.
- **Hidden technical debt:** track defects, performance, security, and maintainability alongside visible features.

The remedy is not to turn the model into a large waterfall process. It is to add the smallest controls needed for the project’s risk.

## Worked examples
### Example 1: Exploratory GIS viewer
A team wants to show map layers but does not know which visualization will help students. It builds a quick browser prototype, observes how users explore layers, and then chooses a simpler search-and-filter interface. The team preserves the map component, tests large data sets, and records why the second design was selected.

### Example 2: A quick prototype opportunity
A team discovers a library that can generate accessible charts. Instead of redesigning the entire application, it tests the library in a small module. If the module meets accessibility and performance criteria, it is integrated; otherwise the team reverts to the original chart. Configuration and a rollback test make the opportunity safe.

### Example 3: Process failure
A group hears an idea at a meeting, writes code for three weeks, loses the requirements, and never tests security or error handling. They call the result an “opportunistic model,” but it is actually unplanned coding. A better version has a one-page goal, a decision log, a prototype exit criterion, and a review.

### Example 4: Safety-sensitive exception
An emergency dispatch team may use an exploratory prototype for interface ideas, but dispatch decisions cannot run on an unvalidated prototype. The team uses a model to explore, then applies a controlled, documented implementation and verification process for the production system.

## Key terms & formulas
- **Opportunistic process:** an emergent process guided by judgment, experience, and current opportunities rather than a complete predefined plan.
- **Chaos model:** Pressman’s term for a process that begins with general objectives and moves through opportunistic implementation and review.
- **Opportunity:** a new feasible improvement, technology, user need, or market condition worth considering.
- **Proof of concept:** a limited experiment showing that a technical or product idea may work.
- **Decision log:** a record of important choices, alternatives, evidence, and consequences.
- **Work in progress (WIP):** work currently being done; limiting it can reduce context switching and unfinished integrations.
- **Exit criterion:** a condition that tells the team whether a prototype or experiment is good enough to continue.
- **Technical debt:** future rework caused by a quick solution that compromises quality or maintainability.

## Common mistakes
- Equating “opportunistic” with no planning, requirements, or testing.
- Confusing an exploratory prototype with a production architecture.
- Changing the product without recording the reason and impact.
- Calling an uncontrolled, unfinished project a process model.
- Assuming the model is suitable for every safety-critical or contractual project.
- Forgetting that successful opportunism depends on communication and disciplined review.

## Exam prep
### Likely 2-mark questions
1. **Define an opportunistic model.** A flexible process that develops a product through general objectives, judgment, and responses to emerging opportunities rather than a fully predefined plan.
2. **State one advantage.** Rapid response to new information and creative exploration.
3. **State one weakness.** Scope, architecture, and documentation can easily become unclear.
4. **What controls are essential?** Clear goals, prototypes, decision logs, version control, review, and testing.
5. **When is it suitable?** Exploratory or creative work where learning is more important than a rigid upfront plan.

### Long-answer answer hints
- “Explain the opportunistic model”: define it, show the exploration/implementation/feedback cycle, discuss appropriate contexts, and explain how it differs from waterfall and spiral.
- “Why can opportunism fail?” list unclear objectives, uncontrolled change, technical debt, and weak traceability; suggest proportionate controls.
- “Compare opportunistic and spiral models”: both are flexible; spiral explicitly manages risk in planned loops, while opportunistic reacts to opportunity and judgment.
- “Apply to a prototype project”: state the hypothesis, build a small experiment, define an exit criterion, record the decision, and integrate only after review.
- “Is the model always creative?” no; without controls it is simply unplanned work. Creativity needs boundaries and review.

### Text sketch
```text
General goal → explore/prototype → observe → choose opportunity
       ↑                                          ↓
       └──── decision log, review, versioning, tests ────┘
```
