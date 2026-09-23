---
subject: oose
unit: 3
topic: abstract-classes
syllabus_ref: CSM3102 Unit-III
status: draft
---
# Abstract Classes
## Overview
An abstract class is a class defined at a more general level whose complete behavior is not specified or cannot be used directly. It organizes common features and establishes a contract for specialized classes. Subclasses add or refine operations and may implement abstract operations. UML uses an abstract classifier and italicized text to show that an element is abstract.

Abstract classes are different from interfaces. An interface primarily specifies what a collaborator can do; an abstract class may provide state and implemented behavior as well as abstract operations. The right choice depends on the relationship and the amount of shared implementation, not on a personal preference.

## Explanation
### 1. Purpose
An abstract class captures a common concept when the concept is meaningful even though no direct object should be created for the general form. For example, `PaymentMethod` can define the operation `authorize(amount)` and common logging, while `CardPayment` and `WalletPayment` provide the method-specific implementation. Creating a generic `PaymentMethod` with no concrete behavior may be wrong.

An abstract class can:
- define a family of related classes;
- provide common state and operations;
- declare an operation that subclasses must implement;
- enforce shared invariants;
- support polymorphic use through the base type.

### 2. Abstract operation and abstract class
An **abstract operation** has no implementation in the abstract class (or intentionally leaves behavior for specialization). A subclass must supply an implementation unless it is also abstract. In some languages an abstract method has no body; in UML, an operation marked `{abstract}` has no specified realization. An abstract class is a classifier that cannot be instantiated directly, though a concrete subclass can be.

Not every UML class with a stereotype such as `<<abstract>>` is an abstract class in the programming-language sense; the notation and tool semantics should be defined by the project. Use a standard UML abstract operation/italicized operation when the meaning is inheritance and specialization.

### 3. Abstract class versus interface
- **Abstract class:** can contain attributes, concrete operations, constructors, and protected behavior; supports inheritance and shared implementation.
- **Interface:** primarily a public contract with operations and possibly constants; a class implements it and supplies behavior. Interfaces are often used for capability and polymorphism.
- A class may implement several interfaces and extend one abstract class in many languages, though the exact language restrictions vary.
Use an interface when the capability is unrelated to a shared data representation, and an abstract class when specialization naturally shares state and implementation.

### 4. Generalization and substitutability
The generalized type defines the common contract. A subtype is valid only if it can be used wherever the generalized type is expected without breaking the client’s assumptions. This is the **Liskov substitution** idea: a `CardPayment` must honor the behavior promised by `PaymentMethod`. Changing the meaning of a base operation or adding a precondition can make an existing subclass invalid.

### 5. Templates and parameterized abstract classes
A **template class** has type parameters, such as `Repository<T>`, and can be specialized to `Repository<User>` or `Repository<Inspection>`. It is useful for a family whose implementation depends on a type while keeping a common contract. A template operation may be abstract, with the specialization supplying the actual type-specific behavior.

### 6. Abstract classes in analysis and design
In analysis, an abstract concept represents a meaningful generalization even if the first release has one concrete subtype. In design, it can protect a common algorithm and extension point. Avoid creating deep abstract hierarchies only to share a few lines; composition, interfaces, or a focused helper may be clearer. Every level should have a stable reason to exist and a coherent variation axis.

### 7. Constraints and operations
A base class may specify an invariant such as “all payments have a nonzero amount” and a template operation `validate()` implemented as a sequence of steps. Subclasses supply hooks such as `authorizeWithProvider()`. The base algorithm can be stable while the details vary, which is often safer than duplicating the entire algorithm in every subclass.

## Worked examples
### Example 1: Payment hierarchy
```text
<<abstract>> PaymentMethod
  - amount: Money
  + authorize(m: Money): Result
  + describe(): String {abstract}

CardPayment        WalletPayment
  authorize(...)     authorize(...)
```
A client can use a `PaymentMethod` reference, but the team does not instantiate the base class. Each concrete class must implement the contract and preserve the amount invariant.

### Example 2: Common algorithm
`ReportGenerator` defines a template method `generate()` that validates input, calls abstract `loadData()` and `render()`, then records an audit entry. `CsvReport` and `PdfReport` implement the varying parts. The base class owns the fixed workflow.

### Example 3: Interface alternative
A `Notification` capability can be implemented by email, SMS, and push classes that share no state or base algorithm. An interface is often more flexible than making all of them inherit a large abstract `Notification` class. The design depends on the relationship, not the pattern name.

### Example 4: Invalid subclass
`PaymentMethod.authorize` promises that a failed authorization leaves the balance unchanged. A subclass that charges before checking provider response violates substitutability. The review finds the bug even if the classes compile.

## Key terms & formulas
- **Abstract class:** a non-instantiable generalization that may define common state/behavior and abstract operations.
- **Abstract operation:** an operation with no complete implementation in the defining classifier.
- **Concrete class:** an instantiable class with complete behavior for its contract.
- **Subclass/specialization:** a more specific type satisfying the generalized contract.
- **Generalization:** the relationship from a specific type to a more general type.
- **Substitutability:** the ability to use a subtype wherever its generalization is expected.
- **Template class:** a parameterized class with placeholders for type-specific behavior.
- **Hook operation:** an operation intended for a subclass to override or refine.
- **Abstract instantiation rule:** do not create an instance of an abstract class; create a concrete specialization.
- **Hierarchy depth (guideline):** keep specialization levels shallow enough that the client understands the contract; no universal numerical limit.

## Common mistakes
- Treating an abstract class as an interface with a different label.
- Making an abstract class instantiable or leaving a concrete class with an unimplemented contract.
- Adding abstract methods to a base class without considering all subclasses.
- Violating substitutability through changed preconditions or meanings.
- Building a deep hierarchy for code reuse rather than a meaningful domain relationship.
- Forgetting that an abstract class may contain implementation and state.
- Marking a class abstract only because it is conceptually broad; verify the modeling purpose.

## Exam prep
### Likely 2-mark questions
1. **Define an abstract class.** A non-instantiable classifier that defines common features/contract and may contain abstract operations for specialized classes.
2. **Differentiate an abstract class and an interface.** An abstract class can provide shared state and implementation; an interface primarily specifies a capability contract.
3. **What is an abstract operation?** An operation declared without complete behavior in the abstract class and implemented by concrete subclasses.
4. **What is substitutability?** The guarantee that a subtype can replace its generalized type without violating client expectations.
5. **Why avoid deep abstraction hierarchies?** They make contracts and change propagation difficult to understand; variation may be better modeled with interfaces or composition.
6. **What is a template class?** A class parameterized by one or more types, with operations specialized for each type.

### Long-answer answer hints
- “Explain abstract classes”: purpose, abstract operations, concrete specialization, notation, invariants, and an example.
- “Differentiate abstract class, concrete class, and interface”: instantiation, implementation, state, and relationship.
- “How do you preserve substitutability?” keep postconditions/preconditions and semantic meaning; test through the generalized type.
- “When is an abstract class better than an interface?” when there is a meaningful is-a family with common state or a stable algorithm; otherwise prefer capability interfaces/composition.
- “Explain a template method with an abstract class”: fixed base workflow, abstract hooks, concrete subclasses, and benefits/risks.

### Sketch
```text
          <<abstract>> PaymentMethod
          validate() / log()       authorize() {abstract}
                         /                 \
                CardPayment               WalletPayment
```
