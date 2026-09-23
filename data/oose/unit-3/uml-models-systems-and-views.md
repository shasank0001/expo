---
subject: oose
unit: 3
topic: uml-models-systems-and-views
syllabus_ref: CSM3102 Unit-III
status: draft
---
# UML, Systems, Models, and Views
## Overview
UML (Unified Modeling Language) is a standard visual language for describing, analyzing, and documenting software and real-world systems. It is not a programming language and it does not force one development method. A UML model is an organized description built from elements such as classes, objects, use cases, activities, states, messages, components, and nodes.

The central idea is separation of concerns. A **system** is the thing being studied; a **model** is a deliberate, simplified representation of that system for a particular audience and question. A **view** is a presentation of selected model content, such as a static structure, behavior, or deployment view. Several views can be kept consistent while revealing different aspects.

## Explanation
### 1. What UML is used for
UML supports:
- communicating with stakeholders before implementation;
- capturing requirements, domain concepts, architecture, interfaces, and behavior;
- specifying and documenting a design;
- generating or supporting implementation and test cases;
- reviewing a system and tracing requirements to design;
- explaining changes and relationships to a development team.

UML diagrams are not automatically correct just because the notation is valid. The model must be useful, consistent, and connected to the actual question being asked.

### 2. System and subsystem
A **system** is a collection of interacting parts that performs a coherent purpose. A **subsystem** is a distinct part of a larger system with its own responsibilities and interfaces. The boundary matters because “the system” may mean the whole organization’s solution, one application, or only a software component, depending on the context. A context diagram helps show what lies outside the chosen boundary.

### 3. Model and modeling
A **model** is a simplified, structured description of a system. Modeling is selective: it keeps important concepts and relationships and omits details irrelevant to the current purpose. The same real system can have an analysis model centered on user goals, a design model centered on implementation structure, and a test model centered on conditions and observations.

A good model is:
- **purpose-driven:** it answers a stated question;
- **consistent:** names, relationships, and constraints agree across views;
- **complete enough:** it covers the decisions in its scope;
- **maintainable:** changes can be located and updated;
- **traceable:** important elements link to requirements and tests.

### 4. UML views and model organization
Common views in a simple UML system are:
1. **Use-case view:** external actors and user goals.
2. **Logical/structural view:** classes, objects, and their relationships.
3. **Behavioral view:** activities, states, interactions, and events.
4. **Implementation view:** components, interfaces, libraries, and source organization.
5. **Deployment view:** nodes, hardware, runtime environments, and artifacts.

These names vary by textbook and UML version. The important idea is that each view isolates a perspective while diagrams within the model should use a consistent vocabulary and cross-references.

### 5. UML model elements
A model contains **elements** and **relationships**:
- structural elements: classes, interfaces, objects, components, nodes;
- behavioral elements: use cases, activities, states, events;
- relationships: association, dependency, generalization, realization;
- constraints and notes: precise rules or explanatory text;
- stereotypes and tagged values: domain-specific meaning or metadata.

A notation symbol is not enough by itself. For example, a class name must mean one concept across the model, and a dependency should not be used for every ordinary method call.

### 6. UML profiles and extension
A profile adapts UML concepts for a domain or tool without changing the core language. Stereotypes such as `<<entity>>`, `<<control>>`, or `<<boundary>>` can clarify an analysis model, but a team should document their meaning. A custom notation can be useful, yet hidden stereotypes make a model harder for others to read.

### 7. Views, viewpoints, and consistency
A **viewpoint** is the perspective and concern of a viewer; a **view** is the representation produced for that concern. For example, a security architect may view a login system as trust boundaries and threats, while a user views it as sign-in tasks. The representations can differ, but they should not contradict one another. A change to authentication rules should update the use case, sequence, state, data, and test models as appropriate.

### 8. Model-driven and documentation uses
UML can support model-driven development, where a model is refined and partly transformed into code, or it can simply document a design. In either case, the model needs a source of truth and a synchronization policy. Handwritten models are valuable for reasoning and review; generated code needs tool/configuration discipline.

## Worked examples
### Example 1: Three views of chat
- Use-case view: students send messages.
- Structural view: `User`, `Conversation`, `Message`, and associations.
- Behavioral view: message is sent, queued, delivered, or failed.
- Deployment view: mobile client, API server, database, notification service.
- Implementation view: client app, message component, persistence adapter.
The views answer different questions but share the same terms.

### Example 2: A system boundary
The “GPS navigation system” may include route calculation and map storage, but not the road authority that supplies new road data. A context model shows that external provider. Treating the provider as an internal component would hide a network and update dependency.

### Example 3: Model validation
A class diagram says a `Route` has a `Driver`, but a sequence diagram shows the route created before login. The team checks the requirement and either changes the lifecycle or adds a system/anonymous route concept. Consistency review catches a modeling error before code.

### Example 4: A view for stakeholders
Sponsors need a simple use-case and deployment view; engineers need class, sequence, and component views. The model can present a “simple” view without removing detailed views; the difference is audience and purpose.

## Key terms & formulas
- **UML:** standardized graphical modeling language.
- **System:** interacting parts with a coherent purpose.
- **Subsystem:** a distinct part of a system with defined responsibilities/interfaces.
- **Model:** purposeful simplified representation.
- **Modeling:** constructing and refining that representation.
- **View:** organized presentation of model elements for a concern.
- **Viewpoint:** the perspective of the viewer.
- **Model element:** a named concept, behavior, structure, or relationship.
- **Constraint:** a condition that a valid model must satisfy.
- **Stereotype:** an extension label that gives UML elements domain-specific meaning.
- **Model consistency:** agreement of names, semantics, and relationships across views.
- **Traceability:** links from requirement to model element and test.

## Common mistakes
- Treating UML as a programming language or a rigid development lifecycle.
- Calling any picture a model without stating its purpose and boundary.
- Mixing analysis-level domain concepts and implementation classes without explanation.
- Using separate names for the same concept in different views.
- Assuming valid notation guarantees a correct model.
- Drawing every view with no prioritization, so the model is large but not useful.
- Using stereotypes that are not defined in a legend or profile.

## Exam prep
### Likely 2-mark questions
1. **Define UML.** A standardized visual language for modeling and documenting system structure and behavior.
2. **Differentiate a system and a model.** The system is the real or intended whole; the model is a simplified representation for a purpose.
3. **What is a view?** A presentation of selected model content focused on a concern or audience.
4. **Name four UML views.** Use-case, logical/structural, behavioral, implementation, and deployment—any four.
5. **What is a profile?** A standardized adaptation of UML for a domain or tool.
6. **Why use multiple views?** Different stakeholders need different details, while common elements preserve a consistent system description.

### Long-answer answer hints
- “Explain UML, systems, models, and views”: purpose of UML, system boundary, model characteristics, views, elements, profiles, and consistency.
- “Differentiate model and diagram”: a model is the complete organized abstraction; a diagram is one view of selected elements.
- “How do multiple UML views improve communication?” show chat or GPS with use-case, class, sequence, activity, component, and deployment views.
- “What makes a good model?” purpose, audience, boundary, completeness for scope, consistency, traceability, and maintainability.
- “Explain UML profiles and stereotypes”: give an example and warn about undefined custom notation.

### Sketch
```text
Real system → model (purpose + boundary) → views → audiences/decisions
                 ↑                         ↓
             feedback, validation, change control
```
