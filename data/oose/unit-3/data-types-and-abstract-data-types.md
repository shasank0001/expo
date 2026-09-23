---
subject: oose
unit: 3
topic: data-types-and-abstract-data-types
syllabus_ref: CSM3102 Unit-III
status: draft
---
# Data Types and Abstract Data Types
## Overview
A data type defines a set of allowed values and the operations that can be performed on them. An abstract data type (ADT) describes what a client can do with data while hiding how the data is represented and implemented. Together they provide a contract: the representation may change, but clients that use the operations should continue to work.

In object-oriented modeling, an ADT is commonly represented by a class or interface with attributes/operations, constraints, and a clear boundary. Good ADTs protect invariants and reduce coupling. They are useful in requirements and design because they describe a meaningful domain capability before database tables, frameworks, or algorithms are chosen.

## Explanation
### 1. Data type
A data type specifies:
- the domain of possible values;
- representation or allowed internal structure;
- the operations and their inputs/outputs;
- preconditions, postconditions, and errors;
- equality, ordering, and lifetime rules, where relevant.

Simple examples include integer, date, string, and boolean. Domain-specific examples include `Money`, `Coordinate`, `InspectionStatus`, and `RouteSegment`. A type is more than a storage slot: it carries meaning and legal operations. A string “abc” may be a poor representation for a currency amount because arithmetic and rounding rules are unclear.

### 2. Abstract data type
An **ADT** specifies the values and observable operations of a data type without exposing representation. The client can construct or obtain a value, apply operations, and observe the contract; it cannot depend on hidden fields or private algorithms. For example, a `PriorityQueue` exposes `enqueue`, `dequeue`, and `peek`; whether it uses an array, tree, or heap is an implementation choice.

An ADT is defined by three parts:
1. **Set of abstract values** or valid state descriptions.
2. **Set of operations** available to clients.
3. **Preconditions/postconditions and invariants** that define correct use.

### 3. Encapsulation and information hiding
The ADT hides representation behind operations. A `Date` should not expose a raw day integer if clients could create an invalid date. It might provide `withYear`, `compareTo`, and `isLeapYear`, while controlling internal fields. The implementation can later change from days-since-epoch to a field structure if the public contract stays the same.

Information hiding reduces the number of decisions a client must know. It also localizes change: a new validation rule can be implemented inside the type rather than copied across every caller.

### 4. Data types versus classes
Every class may define a type, but an ADT emphasizes the abstraction contract rather than implementation. A class can be an ADT when its clients rely on its public operations and cannot safely manipulate its representation. A class that exposes all fields and contains unrelated behavior is not a strong ADT.

### 5. Primitive versus composite and value versus reference types
A primitive type has a small built-in representation, such as an integer or boolean. A composite type is built from other values, such as a date, address, or route. A **value type** is defined by its contents; two equal values are interchangeable, and changing it normally creates a new value. A **reference/object type** has identity; two objects can contain equal state but remain different entities. Modeling the distinction correctly prevents identity and mutation bugs.

### 6. Operations and contracts
An operation can be a constructor, query, mutator, observer, or conversion. A good contract states:
- valid arguments and preconditions;
- the result and postconditions;
- whether the object changes;
- errors or exceptions;
- invariants that remain true.

Example:
```text
deposit(amount)
Precondition: amount > 0 and account is open
Postcondition: balance_after = balance_before + amount
Exception: reject non-positive amount or closed account
```
The contract is more useful than only an implementation such as `self.balance += amount`.

### 7. Type safety
Type safety prevents an operation from being applied to an inappropriate value. Use specific domain types rather than a collection of interchangeable strings and magic numbers. `Money(currency, amount)` makes adding different currencies impossible without an explicit conversion policy. `Coordinate` can enforce valid latitude and longitude. Strong types improve readability and make tests more precise.

### 8. ADTs in analysis and design
During requirements analysis, an ADT captures domain concepts and rules. During design, it becomes a class/interface, with responsibility for state and operations. During implementation, it becomes a module, class, record, or service. The same concept may be represented at different levels, but the meaning should remain consistent.

## Worked examples
### Example 1: Money
```text
Money = currency + nonnegative decimal amount
Operations: add, subtract, compare, format
Invariant: amount has currency's allowed scale
```
Adding USD and INR should be rejected or explicitly converted at a stated exchange rate/date. A floating-point total without a currency model is not a safe ADT.

### Example 2: Priority queue
The ADT contract says `enqueue` adds an item, `dequeue` returns the highest-priority item, and `peek` observes it. An array implementation is a heap in one release and a balanced tree in another. Tests use the interface, so the replacement does not change client behavior.

### Example 3: Date boundary
A `Date` ADT can prevent February 30 and correctly handle leap years. A boundary test checks 29 February in leap and non-leap years. If the raw integer is exposed, callers can bypass validation and corrupt the value.

### Example 4: Route domain type
A `Route` exposes `distance`, `estimatedTime`, and `segments`; it hides the route algorithm and map-cache representation. The representation may change from a linked list to an array without changing a display client, provided the contract is stable.

## Key terms & formulas
- **Data type:** allowed values plus operations and rules.
- **ADT:** values and observable operations with hidden representation.
- **Encapsulation:** protection of representation and invariants.
- **Information hiding:** deliberate concealment of design decisions.
- **Invariant:** condition true after valid operations.
- **Precondition:** condition required before an operation.
- **Postcondition:** promised result/state after an operation.
- **Value type:** equality based on content, no independent identity.
- **Reference type:** equality/identity includes a distinct object instance.
- **Type safety:** prevention of meaningless or unchecked value combinations.
- **Representation independence:** client behavior does not depend on internal representation.
- **Constructor/query/mutator:** create, observe without change, and alter an object respectively.

## Common mistakes
- Treating an ADT as just a collection of getters and setters.
- Exposing a public mutable field and claiming information hiding.
- Using a primitive type where a domain concept needs invariants.
- Writing operations without preconditions, postconditions, or error behavior.
- Confusing an ADT with a database table; the ADT is the contract, not its storage.
- Assuming a data type has identity simply because it is stored in a row.
- Changing a public contract casually and breaking all clients.

## Exam prep
### Likely 2-mark questions
1. **Define an abstract data type.** A specification of values, operations, and contracts that hides representation.
2. **Differentiate a data type and a class.** A type defines values/operations; a class is a language construct that can implement a type/ADT.
3. **What is information hiding?** Concealing design decisions so clients depend on a stable contract.
4. **Give two benefits of an ADT.** Invariant protection, lower coupling, representation independence, and easier maintenance.
5. **Define value and reference types.** Value equality is content-based; reference types have identity.
6. **State one invariant for a BankAccount ADT.** The balance must not become negative without an approved overdraft rule.

### Long-answer answer hints
- “Explain data types and ADTs”: values, operations, representation, contracts, encapsulation, and an example.
- “How does an ADT support change?” show queue representation change while interface and tests remain stable.
- “Design an ADT for Money”: state, operations, pre/postconditions, currency and rounding rules, invalid cases, and tests.
- “Differentiate ADT and implementation class”: abstraction/contract versus concrete fields, algorithms, and storage.
- “What is type safety and why is it useful?” domain-specific types prevent invalid combinations and improve error detection.

### Template
```text
ADT name:
Valid values:
Operations:
Preconditions:
Postconditions/invariants:
Hidden representation:
Errors and boundary cases:
```
