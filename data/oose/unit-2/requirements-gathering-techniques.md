---
subject: oose
unit: 2
topic: requirements-gathering-techniques
syllabus_ref: CSM3102 Unit-II
status: draft
---
# Requirements Gathering Techniques
## Overview
Requirements gathering (elicitation) collects facts, needs, constraints, and vocabulary from stakeholders and the real environment. It is an investigation, not merely a list of “requirements.” The analyst must understand current work, goals, exceptions, laws, systems, and disagreements, then confirm the findings with the people who can authorize and use them.

No single technique finds everything. Interviews are efficient for explanations, observation reveals workarounds and timing, documents show formal rules, surveys provide breadth, and prototypes expose misunderstandings. Triangulation—comparing several sources—reduces the risk of trusting one person's memory or one organization's formal rule.

## Explanation
### 1. Stakeholders
Gather from primary users, administrators, managers, customers, domain experts, support staff, legal/regulatory people, security staff, and external-system owners. A stakeholder may supply, approve, be affected by, or be blocked by the product. Record their role, goals, influence, vocabulary, and decision authority.

### 2. Interviews
An interview is a planned conversation with prepared questions, probes, and recorded outcomes. Use open questions for discovery and closed questions to confirm facts:
- “Walk me through the last inspection you handled.”
- “What must be true before you can close it?”
- “What happens if the network is unavailable?”
- “Is this rule always true, or does an exception require approval?”

Separate needs from solutions. Ask for examples, frequencies, volumes, time spent, errors, and consequences. Summarize the answer and ask the stakeholder to confirm it. Interviews are efficient for domain experts but can be biased by status, memory, or a dominant stakeholder.

### 3. Observation and contextual inquiry
Observation watches users perform work in context. It reveals undocumented steps, shadow work, informal systems, waiting time, workarounds, and physical/safety constraints that users may not mention. It is especially useful for GPS navigation, inspection work, and cashier or registration processes.

The observer should record events without exposing personal data, avoid interfering with work, and compare observation with interviews. Observation alone can show what people do, not whether the workarounds are desired or legally permitted.

### 4. Workshops, brainstorming, and focus groups
A workshop brings users, developers, designers, and domain experts together to build a shared model. Brainstorming generates many ideas without immediately judging them. A focus group explores attitudes and vocabulary, but it is not a substitute for representative operational observation. Facilitate equal participation, separate facts from opinions, and record decisions and open questions.

### 5. Questionnaires and surveys
Surveys collect consistent answers from many users. Use clear, unbiased questions, optional “other” choices, and a pilot test. They are useful for frequency, priority, training needs, and demographic differences, but written questions may not reveal the actual workflow. Do not use a survey to ask a vague question when a walkthrough can produce better evidence.

### 6. Documents and artifact analysis
Study forms, reports, manuals, policies, laws, contracts, bills, training material, legacy database schemas, API specifications, logs, and prior incident reports. Compare the documented policy with actual practice. A document may be outdated or aspirational; the analyst records its authority and date.

### 7. Prototypes and scenarios
A prototype—sketches, screens, storyboards, or a small executable demonstration—lets stakeholders react to a possible solution. It is most useful during elicitation when a requirement is hard to express in words. The team must label the prototype's purpose and not treat a visual mock-up as a complete specification.

Scenarios describe a situation, actors, goal, events, and expected result. Ask stakeholders to walk through normal, alternative, failure, and recovery paths. Scenario walkthroughs often expose missing boundary and exception requirements.

### 8. Analysis of existing systems and data
Inspect current forms, database tables, logs, support tickets, and code when authorized. Measure real volumes, response times, and error rates. For a migration, profile the data: completeness, duplicates, format, missing values, referential integrity, and privacy. Existing systems are evidence of needs but may contain poor or obsolete behavior.

### 9. Choosing a technique
Use a combination based on risk and question:
- unclear goals → interviews/workshops/prototypes;
- actual workflow → observation;
- many users → survey;
- formal rules → documents/regulations;
- performance/volume → logs and measurements;
- disagreements → facilitated workshop and decision owner;
- safety/legacy risk → expert review and artifact analysis.

### 10. Record and verify findings
For every finding, capture source, date, scenario, affected stakeholder, priority, assumption, and open question. Use a glossary and requirement candidate list. Verify high-impact facts with a second source or a domain expert. Separate a need (“reduce duplicate entry”) from a proposed feature (“add a scanner”).

## Worked examples
### Example 1: Canteen token system
The analyst observes queueing, interviews students and cooks, examines the register, and surveys payment preferences. Observation shows that students wait because the cook must write tokens manually. Interviews reveal that card payment failed during a network outage. A document says tokens are optional, but current policy and management agreement clarify that they are required. The requirements include offline-safe payment behavior and a queue-friendly workflow.

### Example 2: GPS navigation
An interview asks drivers to compare a proposed route screen with the current paper/GPS process. Observation shows drivers need the next turn early, not merely a complete route. A log analysis shows that routes near certain map versions are slow. Prototypes test voice versus visual guidance. The team verifies the target device and driving conditions with users.

### Example 3: WMITS
Forms reveal that inspectors photograph violations from two different devices. The legacy database has duplicate site names. A workshop with inspectors and legal staff clarifies that a site is identified by a registration number, not a free-text address. A prototype of evidence capture reveals a need to attach a caption and timestamp.

### Example 4: Conflicting sources
The written policy says every inspection needs one photo; frontline practice often records zero when no violation exists. The team investigates the reason, confirms the policy owner, and models “photo required for a violation, optional contextual image for a compliant inspection.” The discrepancy becomes an explicit, validated rule.

## Key terms & formulas
- **Elicitation:** discovering and documenting stakeholder needs and constraints.
- **Interview:** planned question-and-answer elicitation with a stakeholder.
- **Observation:** studying real work in its natural context.
- **Workshop:** facilitated collaborative session to create or validate a shared model.
- **Questionnaire/survey:** structured collection of answers from a sample or group.
- **Artifact/document analysis:** inspection of forms, policies, reports, schemas, logs, and legacy systems.
- **Prototype:** a model used to explore requirements or user reaction.
- **Scenario:** a concrete situation used to elicit, specify, and validate behavior.
- **Triangulation:** confirming a finding with multiple independent sources.
- **Information gain (simple qualitative guide):** value of a technique depends on uncertainty reduced per unit of time/cost; interviews are strong for explanations, observation for workarounds, surveys for breadth.

## Common mistakes
- Asking “Would you like this feature?” before understanding the problem.
- Treating the loudest stakeholder as the only source of truth.
- Using observation without asking whether the observed workaround is a requirement.
- Copying legacy forms without questioning outdated or conflicting rules.
- Writing a survey with leading or double-barreled questions.
- Failing to record source, date, and open questions.
- Treating a prototype approval as final approval of every hidden requirement.

## Exam prep
### Likely 2-mark questions
1. **List four elicitation techniques.** Interviews, observation, workshops, surveys, document analysis, or prototypes.
2. **Differentiate interviews and observation.** Interviews collect stated explanations and needs; observation reveals actual behavior and context.
3. **Why triangulate sources?** Independent confirmation reduces errors, bias, and memory gaps.
4. **What is a scenario?** A concrete situation with actors, goal, events, and expected outcome used to discover and validate requirements.
5. **Give one strength of a workshop.** It creates shared understanding and resolves conflicts among stakeholders.
6. **What should be recorded after elicitation?** Source, finding, affected stakeholder, priority, evidence, and open question.

### Long-answer answer hints
- “Explain requirements gathering techniques”: define elicitation, list stakeholders, describe each technique with strengths/limits, and recommend a combination.
- “Compare interview and observation”: stated versus actual behavior, sample bias, context, cost, and triangulation.
- “How would you gather requirements for WMITS?” inspectors, supervisors, legal staff, forms, legacy data, workshop, mobile observation, prototype, and validation.
- “Why are prototypes useful?” expose hidden assumptions, clarify workflow, and create a common artifact; state their limitations.
- “How do you turn information into requirements?” record evidence, separate need from solution, identify conflicts, model scenarios, prioritize, and confirm with the source owner.

### Evidence table template
Finding | Source/date | Stakeholder | Scenario | Evidence | Candidate requirement | Open question.
