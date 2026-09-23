---
subject: oose
unit: 1
topic: spiral-model
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Spiral Model
## Overview
The spiral model is a risk-driven software process. The team works in repeated loops, and every loop begins by identifying what could go wrong, reducing that risk, and only then investing in the next part of the product. Unlike a purely linear model, it makes uncertainty and risk central to planning. It is especially useful when requirements are unclear, technology is unfamiliar, or failure would be expensive.

A loop is not just another coding sprint. It includes objectives, alternatives, risk analysis, engineering work, planning, and a review with stakeholders. The early loops are often prototypes, models, architecture studies, or paper exercises. Later loops implement and harden the agreed product.

## Explanation
### 1. The four quadrants
A common presentation of Boehm’s spiral divides each loop into four activities:
1. **Determine objectives:** identify what the customer and project need at this stage, such as reducing technical uncertainty, proving feasibility, or delivering a usable function.
2. **Identify and evaluate alternatives:** generate possible ways to meet the objective and evaluate cost, time, risk, and benefit.
3. **Develop and verify the next level:** perform the selected engineering work—model, prototype, code, test, or review—and check that it addresses the risk and objective.
4. **Plan the next iteration:** use results and stakeholder feedback to choose the next objectives, schedule, resources, and risk responses.

Some textbook versions show the quadrants as objectives, risk assessment, development/validation, and planning. The exact labels vary; the risk-driven logic is the essential idea.

### 2. The center and the outer edge
At the center, the team may first understand the problem, stakeholders, and key objectives. Moving outward, loops become progressively more detailed and expensive. Near the outer edge, the product may be implemented, integrated, tested, and released. A project does not always reach every ring: a feasibility project may stop after a model, while a mature product may have several release-oriented loops.

### 3. Risk categories
- **Product risk:** will users need or value the product?
- **Feasibility risk:** can the team build it with the proposed technology?
- **Schedule risk:** can it be delivered in time?
- **Cost risk:** will resources be available and affordable?
- **Quality and safety risk:** could incorrect behavior cause harm or unacceptable loss?
- **Organizational risk:** will stakeholders agree, communicate, and support the change?

For each significant risk, the team records probability, impact, detection difficulty, response, and owner. Testing itself is not the only response; alternatives include a prototype, simulation, training, a smaller scope, or a contract.

### 4. How the team uses a loop
A typical loop starts with a risk such as “Can the GPS service calculate a route in under two seconds on the target phone?” The team builds a small benchmark, compares map algorithms, and measures the result. If performance is poor, it changes the algorithm or narrows the first release. Only after reducing that risk does the team commit to full implementation.

### 5. Strengths
- Makes risk visible and gives it management attention.
- Encourages prototypes and early technical validation.
- Supports changing requirements through feedback.
- Helps stakeholders see progress and participate in decisions.
- Can be tailored: stop when the project is a study, or continue through releases.

### 6. Weaknesses and conditions
- Risk analysis needs skill, data, and time; a weak analysis can create false confidence.
- The model can become expensive and paperwork-heavy if every loop is over-formal.
- It does not eliminate uncertainty; it only makes uncertainty explicit.
- Without strong configuration and change control, repeated loops can produce confusing versions.
- It is not automatically suitable for every routine project; a small stable feature may need a simpler process.

### 7. Stakeholder review and tailoring
At the end of each loop, the team presents results, risks, costs, and proposed next objectives. The customer can approve, reject, or redirect the work. The depth of documentation and the number of loops should match the project’s size and risk. A final planned release may still be necessary, and the spiral can contain waterfall-like or phased-release elements.

## Worked examples
### Example 1: Automobile navigation
A GPS application must work offline and find routes quickly. The first loop tests map data and routing algorithms. The second builds a phone prototype and measures battery use. The third investigates live-traffic integration. Only later does the team commit to a full navigation product. Each loop reduces a different uncertainty.

### Example 2: Medical-like risk
For a clinic dosage-support system, a model-first loop checks whether the rules are safe. A simulation checks unusual combinations. A prototype is reviewed by clinicians. The implementation loop includes traceability and validation. The spiral loop is repeated until critical risks are acceptable; it is not a reason to skip verification.

### Example 3: A cost decision
The team sees two payment providers. One is cheaper but has uncertain API reliability; the other costs more but has a tested sandbox. The team prototypes both, assigns a risk owner, and chooses based on evidence. The decision is recorded before committing the full budget.

### Example 4: Stopping early
A university evaluates a new GIS viewer. After two proof-of-concept loops, users and faculty show little demand. The sponsor stops the project. A successful spiral can produce the valuable answer “do not proceed,” not only a shipped product.

## Key terms & formulas
- **Spiral loop:** one complete cycle of objective setting, risk analysis, development/validation, and planning.
- **Risk probability:** chance of an unwanted event; often qualitative low/medium/high.
- **Risk impact:** consequence if the event occurs; often estimated as cost, delay, safety, or quality effect.
- **Risk exposure:** a simple planning indicator, commonly probability × impact, with a warning that scales and units must be defined before comparing risks.
- **Risk response:** avoid, reduce, transfer, accept, or exploit the opportunity.
- **Prototype:** a simplified or experimental product used to answer a question or obtain feedback.
- **Milestone review:** stakeholder decision to continue, revise, or stop after a loop.
- **Tailoring:** selecting loop depth and artifacts based on risk and project context.

## Common mistakes
- Reducing the spiral to “repeat requirements, design, code” without risk analysis.
- Believing a prototype alone proves the whole system is safe or usable.
- Forgetting stakeholder review and planning at the end of a loop.
- Confusing risk analysis with writing a generic list of unlikely disasters.
- Saying the spiral requires fixed requirements; it is designed to handle uncertainty.
- Treating risk exposure as a universal truth without defining units and qualitative levels.

## Exam prep
### Likely 2-mark questions
1. **What is the central idea of the spiral model?** Repeated loops that identify and reduce risk while producing and validating progressively more of the system.
2. **Name the four loop activities.** Objectives, alternatives, development/validation, and planning (or equivalent risk-driven labels).
3. **Give one use.** A project with uncertain technology or safety/cost risk.
4. **What is a prototype in the spiral?** A deliberately simplified or experimental implementation used to reduce uncertainty or obtain feedback.
5. **State one weakness.** Risk analysis can be costly or unreliable without expertise and evidence.

### Long-answer answer hints
- “Explain the spiral model with diagram”: draw concentric loops, show objectives, risk analysis, engineering, and planning, and explain movement from center to edge.
- “How does a team reduce technical risk in the first loop?” state the hypothesis, alternatives, prototype/benchmark, validation criteria, and planning consequence.
- “Compare spiral with waterfall”: uncertainty/risk-driven versus stable, mostly fixed phase order; cite when each is suitable.
- “Explain risk management in a software project”: identify, analyze, prioritize, respond, monitor, and document; give a GPS or safety example.
- “Why might a project stop after a spiral loop?” The risk or user-value hypothesis was disproved, so continued investment is not justified.

### Text sketch
```text
        Objectives → Alternatives → Develop and verify → Plan next loop
             ↑                                                ↓
             └──────── stakeholder review and new risk data ──┘
        (repeat in smaller, risk-driven loops)
```
