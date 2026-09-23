---
subject: oose
unit: 2
topic: domain-analysis
syllabus_ref: CSM3102 Unit-II
status: draft
---
# Domain Analysis
## Overview
Domain analysis studies the area in which a software product will operate before the team commits to detailed requirements or implementation. It builds a shared vocabulary and a model of the important concepts, rules, actors, data, processes, constraints, and exceptions. The result is not a database design or a Java class list; it is a clear understanding of the problem domain.

Domain analysis reduces expensive misunderstandings. If a team uses “route,” “trip,” “vehicle,” and “inspection” without shared meanings, every later document and test will inherit the confusion. The analyst observes real practice, interviews domain experts, studies documents and existing systems, and checks assumptions with stakeholders.

## Explanation
### 1. What is a domain?
A domain is the subject area or environment in which a system operates and the rules that govern it. It can be narrow, such as college marks, or broad, such as transportation, waste management, or geographic information. The domain includes human roles, physical things, processes, policies, terminology, and exceptions—not just the screens in the proposed application.

For example, in a GPS navigation system the domain includes roads, routes, vehicles, traffic, maps, drivers, restrictions, and location services. In WMITS, it includes inspectors, sites, violations, photographs, compliance status, and the legal process for escalation.

### 2. Goals of domain analysis
- Build a common vocabulary and glossary.
- Identify the system boundary and the surrounding environment.
- Find the important domain concepts and their relationships.
- Discover business rules, policies, calculations, and invariants.
- Separate what is essential from what is merely a preference.
- Reveal exceptions, edge cases, regulations, and risks.
- Provide a stable model for requirements, design, and tests.
- Find disagreements early and obtain a decision from an owner.

### 3. Steps
1. **Define the domain and purpose:** state the problem, target organization, users, and the questions the analysis must answer.
2. **Collect sources:** interviews, observation, workshops, forms, laws, manuals, reports, databases, legacy software, and measurements.
3. **Identify stakeholders and experts:** include frontline users, managers, administrators, regulators, and people who handle exceptions.
4. **Create a glossary:** record each term, definition, synonym, owner, and source.
5. **Find concepts and relationships:** use noun/verb analysis, concept maps, domain models, and use-case scenarios.
6. **Extract rules and constraints:** write decision rules, formulas, permissions, lifecycle states, and legal constraints.
7. **Model the current and future domain:** note what exists, what should change, and what remains outside scope.
8. **Validate with scenarios:** walk through normal, failure, boundary, security, and recovery situations.
9. **Record assumptions and open questions:** assign owners and deadlines instead of hiding uncertainty.
10. **Maintain the model:** domain knowledge changes as the system evolves.

### 4. Domain model
A domain model is a simplified representation of the important domain concepts, their responsibilities, and relationships. It is language-oriented, not implementation-oriented. For instance:
```text
Inspection ──performed at──> Site
Inspector ──performs───────> Inspection
Inspection ──may contain──> Evidence
Inspection ──has status───> Open | Closed | Escalated
```
A domain model may later inspire classes, but it should not be prematurely constrained by tables, screens, or a particular framework.

### 5. Rules and invariants
A rule states what should happen under a condition. Examples:
- An inspection cannot be marked closed without the required evidence.
- A route must begin and end at valid map locations.
- A user with the viewer role cannot change a mark.
Distinguish a **business rule** (inherent policy) from a **user-interface rule** (how the rule is presented). Ask the domain expert what happens if the policy changes; that reveals whether the model captured the policy rather than one screen.

### 6. Scope and boundaries
Domain analysis helps define the boundary: the system receives data and sends services, while actors and external systems remain outside. It also separates **as-is** and **to-be** processes. For instance, a paper register can be the current domain process, while a digital inspection app is the future process.

### 7. Validation
Validate the domain model through walkthroughs with experts and by replaying real cases. Ask whether every term has one meaning, whether rules cover exceptions, and whether the model explains why a result occurs. A model that is elegant but cannot explain a real case is incomplete.

## Worked examples
### Example 1: GPS domain
The analyst records road types, map providers, route preferences, restrictions, traffic timestamps, and units of distance. “Fastest” may mean shortest travel time, not shortest distance. The term is clarified before a route algorithm is selected. Weather data is out of scope for the first version, but the interface can leave room for it.

### Example 2: WMITS domain
Interviews with inspectors reveal that a “violation” is not the same as a “site”: one site can have many violations, and a violation can receive several evidence photos. A violation has a legal category and a status history. This prevents an incorrect one-to-one database assumption.

### Example 3: Glossary conflict
Operations staff use “closed” to mean “site visit finished,” while supervisors use it to mean “legal case resolved.” The analyst does not choose a name arbitrarily. The team agrees that `visitCompleted` and `caseResolved` are separate states and models them separately.

### Example 4: Domain walkthrough
An expert walks through a disputed inspection. The rule and evidence requirements are discovered only when the process is traced step by step. The analyst then tests the model against that scenario, avoiding a requirements document that handles only successful inspections.

## Key terms & formulas
- **Domain:** the subject area and environment of a system.
- **Domain analysis:** study of domain concepts, rules, actors, processes, constraints, and language before detailed solution design.
- **Domain model:** simplified, implementation-independent representation of the domain.
- **Domain expert:** a person with authoritative knowledge of the subject area.
- **Concept:** a meaningful idea, object, event, role, or relationship in the domain.
- **Rule:** a condition and prescribed action or result.
- **Invariant:** a condition that must remain true.
- **System boundary:** the line separating the system under development from external actors and systems.
- **As-is model:** description of the current process; **to-be model:** description of the intended future process.
- **Glossary coverage:** agreed terms / important terms identified; a project should resolve unexplained terms before baseline.

## Common mistakes
- Starting domain analysis by choosing tables, frameworks, or screen layouts.
- Recording stakeholder jargon without defining it.
- Assuming every noun is a class or every verb is a method.
- Ignoring policy, legal rules, exceptions, and existing workarounds.
- Confusing the current process with the future requirements.
- Building a model that is too detailed to understand or too vague to validate.
- Treating an unresolved conflict as a minor documentation issue.

## Exam prep
### Likely 2-mark questions
1. **Define domain analysis.** Study of a problem area to understand its concepts, rules, actors, relationships, and constraints before detailed solution design.
2. **Give two sources of domain information.** Interviews, observation, documents, workshops, legacy systems, laws, or measurements.
3. **What is a domain model?** A simplified, implementation-independent representation of important domain concepts and relationships.
4. **Why is a glossary useful?** It gives one meaning to terms and prevents misunderstandings across requirements, design, and tests.
5. **Name one domain-analysis output.** Glossary, as-is/to-be model, domain model, rule list, scope boundary, or open-question list.

### Long-answer answer hints
- “Explain domain analysis”: purpose, steps, sources, model, rules, validation, and an example from GPS/WMITS.
- “How do you conduct a domain investigation?” define the domain, collect sources, interview experts, observe work, build a glossary/model, walk through cases, and record open questions.
- “Domain model versus class diagram”: domain analysis is language and problem focused; a design class diagram adds technical responsibilities, interfaces, and implementation constraints.
- “Why are exceptions important?” Real operations are defined by failure and edge cases; ignoring them produces a system that works only for happy paths.
- “How do you validate a domain model?” expert walkthroughs, real scenarios, rule tests, boundary cases, and agreement on definitions.

### Exam checklist
Domain purpose → sources → concepts → rules → relationships → boundary → validation.
