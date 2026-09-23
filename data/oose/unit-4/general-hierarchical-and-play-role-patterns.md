---
subject: oose
unit: 4
topic: general-hierarchical-and-play-role-patterns
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# General Hierarchical and Play–Role Patterns
## Overview
This note covers two related object-modeling patterns. The **General Hierarchical pattern** represents a tree or hierarchy in which some objects may have subordinates and some may not. The **Play–Role pattern** represents an object that can play different roles in different contexts, with each role carrying its own properties and behavior. Both patterns help model variation without creating one enormous class or a confusing inheritance tree.

## Explanation
### 1. General Hierarchical pattern
#### Context
A hierarchy contains objects with common properties and operations. An object may have one or more superior/parent objects and one or more subordinate/child objects. Some categories of node can have subordinates, while leaf categories cannot.

Examples:
- employee–manager supervision;
- directory–file containment;
- task–subtask decomposition;
- geographic region containing subregions and sites;
- train legs arranged into a scheduled or specific trip.

#### Problem
A simple association between a `Node` and itself does not express which node types may have children. Creating separate classes and duplicate tree logic for every node type is also undesirable. The design must support traversal, common node services, and a constraint that prevents invalid children.

#### Solution
Use a common `Node` classifier, then distinguish whether a node is allowed to be a superior:

```text
                 <<Node>>
             state / name / id
                 /          \
      <<NonSuperiorNode>>  <<SuperiorNode>>
       leaf: no children    superior: 0..1
                             + 0..* subordinates
```

A `SuperiorNode` can have a link to its superior and to its subordinates. A `NonSuperiorNode` inherits common node behavior but has no subordinate link or its multiplicity is constrained to zero. Depending on the domain, a node may have exactly one superior, zero or one superior, or a more complex role such as primary and alternate parent. State the rule explicitly.

#### General Hierarchical services
`Node` can provide:
- identity and common name;
- `getParent()`/`getSubordinates()` where allowed;
- `addSubordinate(node)` and `removeSubordinate(node)`;
- traversal or visitor operations;
- cycle prevention, maximum depth, and permission checks.

The add operation should reject a child under a non-superior and reject a cycle unless the domain allows one. A recursive traversal must be safe for deep or malformed trees.

#### Benefits and limits
The pattern gives a common vocabulary, one implementation for tree operations, and a clear leaf constraint. It can be more complex than a simple tree if there are multiple parents, ordered children, permissions, or different traversal rules. In those cases, use explicit association classes or role names rather than hiding the complexity.

### 2. Play–Role pattern
#### Context
An object may participate in several contexts and play different roles. A person may be a student in one registration, an employee in one organization, and a parent in a family. A role has properties and behavior relevant to that context, while the player remains the same entity.

#### Problem
Merging every role's properties into one `Player` class creates optional fields and unclear responsibilities. Making each role a subclass of the player forces a player to change class or requires multiple inheritance, and it can be impossible for one object to have two roles at once. The model must allow multiple, changeable, context-specific roles without duplicating the player's identity.

#### Solution
Keep a stable `Player` and attach zero or more role objects through an `AbstractRole` interface or common role abstraction:

```text
Player 1 ───── 0..* AbstractRole
                         /       \
                 AttendanceRole  LevelRole
```

The player may own or be linked to roles. Each role stores only the information and operations for its context. A role can be added, removed, activated, or expired. The player need not know the concrete class of every role; it can expose role-specific queries through an interface or service.

#### Role constraints
- A student may have at most one current level role but many attendance records.
- An animal may have one or two habitat roles, depending on the model.
- A person may be both a manager and an employee in different organizations.
- A role may be valid only while a date interval and an organization relationship are active.

Use role names, time bounds, and uniqueness constraints. A role should not become a hidden global bag of unrelated fields.

### 3. General Hierarchical versus Play–Role
A hierarchy is primarily a **containment/supervision structure**: nodes are related by parent/child links. Play–Role is primarily a **contextual classification structure**: one player has role objects that add meaning and behavior. An employee can be a node in an organization hierarchy and also play a worker/manager role; these are different models and may be combined carefully.

### 4. Choosing the pattern
Use General Hierarchical when the main variation is **where an object sits in a tree** and many nodes share traversal/containment behavior. Use Play–Role when the main variation is **what an object does in a context**. Use both when the domain genuinely needs both relationships, but keep them explicit and do not make one pattern stand in for the other.

## Worked examples
### Example 1: Employee hierarchy
`Employee` is a `Node`; a manager is a `SuperiorNode` and may supervise zero or many employees. A technician may be a `NonSuperiorNode` for the supervision relation, while still inheriting common name and employee operations. The system prevents an employee from becoming their own supervisor and checks cycles such as A manages B manages A.

### Example 2: File hierarchy
`FileSystemItem` is the common node. A `Directory` is a `SuperiorNode`; a `File` is a `NonSuperiorNode`. A directory can contain files and subdirectories, while a file cannot. Moving a directory moves its complete descendant tree. Permissions and maximum size are checked by the directory operation.

### Example 3: Student roles
A `Person` player has an `AttendanceRole` for a course and a `LevelRole` such as undergraduate or graduate. Attendance data is not placed in the person, and level is not a new person. A role can end without deleting the person; historical attendance remains linked to the role's course/term identity.

### Example 4: Animal habitat
An `Animal` player may have an `AquaticAnimalRole` and a `HabitatRole` for a particular enclosure. The model can represent role-specific feeding and habitat behavior without making the animal permanently a subclass of every possible habitat category.

### Example 5: WMITS user roles
A user can be an inspector, supervisor, or administrator in different sites. Rather than creating `InspectorUser`, `SupervisorUser`, and `AdministratorUser` subclasses, attach role objects with site and validity. Authorization checks the active role, site, and operation. This supports one person serving different roles while preserving audit history.

## Key terms & formulas
- **General Hierarchical pattern:** a reusable hierarchy structure with a common node and constrained superior/subordinate roles.
- **Superior node:** node allowed to contain or supervise subordinate nodes.
- **Non-superior/leaf node:** node prohibited from having subordinates.
- **Subordinate:** child/dependent node in the hierarchy.
- **Cycle:** path that makes a node its own ancestor; usually an invalid constraint.
- **Play–Role pattern:** a player has role objects that supply context-specific state and behavior.
- **Player:** stable entity whose identity exists across roles.
- **Role:** context-specific responsibility, state, and behavior attached to a player.
- **Role multiplicity:** number of simultaneous roles, such as `0..*` or `0..2`.
- **Tree traversal cost:** roughly O(n) for one complete pass over n nodes; repeated unrestricted traversals can become a performance risk.
- **Role validity interval:** dates during which a role is active and usable.

## Common mistakes
- Calling every parent-child relationship a General Hierarchical pattern without a common node contract.
- Allowing leaves to acquire children because the association is present on the superclass.
- Failing to prevent cycles or unlimited depth.
- Merging all role properties into a Player class.
- Making roles subclasses of Player and then changing the player's class whenever a role changes.
- Ignoring that a player can have multiple roles or that a role can expire.
- Confusing a hierarchy with a role relationship.
- Omitting site/date/permission constraints from a role.

## Exam prep
### Likely 2-mark questions
1. **Define the General Hierarchical pattern.** A structure for common nodes in a hierarchy, distinguishing nodes that may have subordinates from leaf/non-superior nodes.
2. **What is a leaf constraint?** A rule preventing a non-superior/leaf node from having children.
3. **Define the Play–Role pattern.** A pattern in which one player has one or more role objects carrying context-specific properties and behavior.
4. **Why is multiple inheritance avoided in Play–Role?** A player may need several simultaneous roles and should not change class or duplicate its identity.
5. **Differentiate the two patterns.** Hierarchy organizes parent/child structure; Play–Role organizes contextual capabilities and data.
6. **Give one example of a cycle test.** Employee A manages B and B manages A; the operation must reject or report the cycle.

### Long-answer answer hints
- “Explain General Hierarchical”: context, forces, Node/SuperiorNode/NonSuperiorNode, operations, cycle/depth constraints, and an example.
- “Explain Play–Role”: player, abstract role, role classes, multiplicity, lifecycle, authorization, and an example.
- “Compare the patterns”: purpose, structure, constraints, and common UML notation.
- “Model a student or employee with several roles”: identify player, roles, role-specific data, validity, and permissions.
- “Why are common services useful?” provide traversal, naming, and consistency logic once while allowing specialized nodes/roles.

### Sketch
```text
General hierarchy:       Node
                         ├── NonSuperiorNode (leaf)
                         └── SuperiorNode ── 0..* subordinate

Play–Role:               Player 1 ─── 0..* AbstractRole
                                      ├── RoleA
                                      └── RoleB
```
