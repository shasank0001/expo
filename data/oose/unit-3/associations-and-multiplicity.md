---
subject: oose
unit: 3
topic: associations-and-multiplicity
syllabus_ref: CSM3102 Unit-III
status: draft
---
# Associations and Multiplicity
## Overview
An association is a meaningful relationship between classes. **Multiplicity** states how many instances at one end may be associated with one instance at the other end. UML uses `0..1`, `1`, `0..*`, `1..*`, and exact/lower-upper bounds to make cardinality and optionality explicit. Good associations capture domain facts, not merely table joins.

This topic includes labelled associations, validating associations, and reflexive associations. Each has a specific purpose: labels explain role or purpose, constraints/validation protect business rules, and reflexive associations describe links between instances of the same class.

## Explanation
### 1. Association notation
A line between classifiers is an association. It may be:
- plain association, where instances are connected;
- directed/navigable association, where one role can access the other;
- aggregation, a whole-part relationship with independent part lifetime;
- composition, a strong whole-part relationship in which the part's lifetime is normally owned by the whole;
- association class, a class that adds attributes/operations to the relationship itself.

The meaning of a line must be documented. A line without a name or role can be ambiguous when two classes have more than one relationship.

### 2. Multiplicity
Read multiplicity at an end as “how many instances of the class at that end may be associated with one instance of the class at the opposite end.”

Example:
```text
Department 1 ───── 0..* Employee
```
One department may have zero or more employees; one employee belongs to exactly one department in this model. The `1` is at the department end and describes the employee’s department, not the department’s employee count. Reading direction is a common exam and modeling error.

Common values:
- `1`: exactly one;
- `0..1`: zero or one, optional;
- `*` or `0..*`: zero or many;
- `1..*`: at least one, possibly many;
- `3..5`: a bounded range;
- `2..*`: at least two, as in a route with at least two waypoints.

Multiplicity is a model constraint, not a hint. A value that the domain never permits should not be used merely because the implementation currently behaves that way.

### 3. Labelled associations
An association label names the relationship, often as a verb phrase: `employs`, `contains`, `assignedTo`, `submits`. **Role names** label the two ends from the perspective of each class: a `User` may be `sender` and `receiver` of a `Message`; a `Person` may be `parent` or `child` in a reflexive relationship.

Labels are especially important when:
- the same classes have multiple associations;
- the direction is not obvious;
- a relationship has business meaning or a verb;
- roles differ by viewpoint.

Use clear domain wording. “Has” and “uses” are weak labels if they hide the actual business operation.

### 4. Validating associations
A valid association means more than a syntactically correct line. The model must satisfy:
- **existence:** the relationship is allowed;
- **multiplicity:** the number of links is allowed;
- **role/label correctness:** each end has the intended role;
- **conditional rules:** a link is allowed only when conditions hold;
- **temporal constraints:** a link may have start/end time;
- **uniqueness:** a role may permit only one or many links;
- **business invariants:** the relationship preserves domain rules.

Examples:
- A route may have at least two waypoints.
- A user can send many messages but a message has exactly one sender.
- A site may be associated with an inspection only when the site is active.
- A person may manage at most one current primary department unless the policy permits more.

Some constraints are shown as a note or constraint beside the line, e.g. `{ self.role = manager }` or `{ evidenceRequired }`. Complex conditions may be represented with a decision table or invariant rather than a long label.

### 5. Reflexive associations
A **reflexive (recursive) association** connects instances of the same class. It is useful for tree structures, supervisor relationships, and recursive containment.

```text
Employee 0..1 ── manages ── * Employee
```
A manager may manage zero or many employees, while an employee may have zero or one manager. For a `Person` who is a parent of another `Person`, role names are essential:
```text
Person 0..* ── parentOf ── 0..* Person
```
A person can be a parent and a child at the same time. A recursive association may also be a composition if a child is owned only by one parent, but lifecycle and business meaning must justify it.

### 6. Association classes
When an association itself has data and behavior, model an **association class**. For example, a student enrolls in a course over a time period with a grade. `Enrollment` can hold `term`, `status`, and `grade`, rather than placing the same information ambiguously in `Student` or `Course`.

### 7. Aggregation and composition
Aggregation (“shared whole-part”) says the part can exist independently. Composition (“strong whole-part”) says the part is owned and normally has a lifetime dependent on the whole. A route may compose its waypoints if a waypoint cannot meaningfully exist without the route; a department may aggregate teachers who can be reassigned. These are semantic decisions, not merely symbols.

### 8. Navigability and dependency
A navigable association indicates that one role can reach or refer to the other. A non-navigable association may exist only as a conceptual link. A bidirectional association can increase coupling; the model should reflect the required operations, not assume every object loads every related object.

## Worked examples
### Example 1: Many-to-many with association class
```text
Student 1 ── 0..* Enrollment * ── 1 Course
                  - term
                  - grade
```
A student enrolls in many courses and a course has many students. The relationship data belongs to `Enrollment`, not to either class alone.

### Example 2: Labelled association
A `User` may have both `sentMessages` and `receivedMessages` associations to `Message`. Role names make it clear that the two ends differ. A test checks that a message's sender and receiver are not confused.

### Example 3: Reflexive hierarchy
```text
Employee 0..1 parent ── * Employee
```
An employee has at most one manager, and a manager has zero or more reports. A cycle (A manages B manages A) is a validation constraint. A recursive query or traversal test checks this invariant.

### Example 4: Conditional validation
A `Case` can be assigned to an `Officer` only when the officer's region matches the case's region. The association exists, but a constraint `{ officer.region = case.region }` and a service rule prevent invalid links. The model and validation test agree.

## Key terms & formulas
- **Association:** a relationship between classifiers/instances.
- **Multiplicity:** allowed number of instances at one end per instance at the other.
- **Role name:** a name for a class's role at one end.
- **Association label:** verb/name describing the relationship.
- **Constraint:** condition restricting valid model behavior.
- **Valid association:** one that satisfies domain, multiplicity, role, and conditional rules.
- **Reflexive association:** association from a class to itself.
- **Aggregation:** weak whole-part relationship.
- **Composition:** strong ownership and usually dependent lifetime.
- **Association class:** class modeling data/behavior of an association.
- **Navigability:** whether one end can access/refer to the other.
- **Relationship density (qualitative):** one-to-one, one-to-many, or many-to-many, derived from both multiplicities.

## Common mistakes
- Reading a multiplicity from the wrong end.
- Using `0..*` everywhere without checking the domain.
- Omitting role names when both classes are the same or have several links.
- Calling any connection valid merely because the classes can be linked.
- Treating aggregation and composition as interchangeable.
- Forgetting temporal and conditional constraints.
- Using a recursive association without preventing cycles or specifying direction.

## Exam prep
### Likely 2-mark questions
1. **Define an association.** A meaningful relationship between classes or instances.
2. **What is multiplicity?** The allowed number of instances at one association end for one instance at the other end.
3. **Explain `1 ── 0..*`.** One instance at the left has zero or many instances at the right; one right instance has exactly one left instance in this model.
4. **What is a role name?** A label identifying a class's role in a relationship, especially when roles differ.
5. **Define a reflexive association.** An association in which a class is associated with instances of itself.
6. **Differentiate aggregation and composition.** Aggregation is a weak/shared whole-part; composition gives the whole ownership and normally dependent lifetime.

### Long-answer answer hints
- “Explain associations and multiplicity”: notation, reading direction, cardinality, labels, navigability, aggregation/composition, and examples.
- “How do you validate an association?” existence, multiplicity, role, condition, uniqueness, lifecycle, and domain invariants.
- “Draw a labelled reflexive association”: supervisor/employee or parent/child, role names, multiplicities, and cycle rule.
- “When is an association class used?” when the relationship itself has attributes/behavior, such as enrollment term or grade.
- “Explain composition vs aggregation with a GPS example.” Waypoints owned by a route may be composition; a reusable map region shared by several queries may be aggregation.

### Multiplicity diagram
```text
[Department] 1 -------- 0..* [Employee]
      read: one employee belongs to one department
      read from Employee: a department has zero or more employees
```
