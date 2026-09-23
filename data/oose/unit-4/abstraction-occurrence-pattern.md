---
subject: oose
unit: 4
topic: abstraction-occurrence-pattern
syllabus_ref: CSM3102 Unit-IV
status: draft
---
# Abstraction–Occurrence Pattern
## Overview
The Abstraction–Occurrence pattern represents a family of related objects when the members share common information but also have important individual differences. It separates the **abstraction**—the concept and information common to a set—from the **occurrences**, which are the particular members and their occurrence-specific attributes or behavior.

This is useful when duplicating common fields in every occurrence would cause inconsistency or when each occurrence type has different details. The pattern creates a meaningful association between a set-level abstraction and its members without forcing an awkward inheritance hierarchy.

## Explanation
### 1. Context and problem
A domain often contains sets such as:
- a TV series and its episodes;
- a book title and its library copies or editions;
- a product family and its models;
- a route type and individual trips;
- a collection and its items.

The set-level object has properties shared by the whole set. Each member has additional properties or behavior. For example, a `TVSeries` has a series name and producer, while each `Episode` has an episode number and story synopsis. If the series is renamed, the change should not require editing every episode.

A naïve model duplicates `seriesName` and `producer` in every episode. Another naïve model puts episode details on the series, which cannot represent a different story synopsis for every episode. The design must express both levels clearly.

### 2. Forces addressed
- Store common information once, in the abstraction.
- Keep occurrence-specific information with the occurrence.
- Allow multiple occurrences for one abstraction.
- Let an occurrence specialize when several occurrence kinds share further properties.
- Avoid copying common data and avoid one giant class with irrelevant fields.
- Make the relationship navigable in the directions clients need.

### 3. Solution structure
The pattern uses two classifier kinds:

```text
«Abstraction» 1 ───── 0..* «Occurrence»
      common data          occurrence data
      common services      occurrence-specific services
```

The abstraction exposes common queries and operations. An occurrence holds a link or reference to its abstraction, plus its own state. The relationship is often modeled as an association, not generalization, because an episode **belongs to** a series but is not necessarily a kind of series. If occurrence types share properties, an ordinary specialization can be added below the occurrence classifier.

A class diagram can look like:

```text
                 +--------------------+
                 |     TVSeries       |
                 +--------------------+
                 | - seriesId         |
                 | - seriesName       |
                 | - producer         |
                 | + addEpisode()     |
                 +--------------------+
                           1
                           |
                           | 0..*
                 +--------------------+
                 |      Episode       |
                 +--------------------+
                 | - episodeNumber    |
                 | - storySynopsis    |
                 | + duration()       |
                 +--------------------+
```

The exact arrows and multiplicities depend on navigation and lifetime, but the semantic separation must be clear.

### 4. Abstraction responsibilities
An abstraction may:
- identify the set and its common attributes;
- maintain a collection of occurrences when collection behavior is required;
- provide common calculations or policies;
- add/remove occurrences only when the domain allows it;
- expose queries that do not require the client to know every occurrence type.

It should not contain state that belongs to one member. For example, `TVSeries` should not store “episode 4’s synopsis.”

### 5. Occurrence responsibilities
An occurrence may:
- store its unique or occurrence-specific data;
- access common data through its abstraction link;
- perform behavior that depends on its particular type;
- enforce local invariants;
- participate in a subtype hierarchy if occurrence varieties share structure.

The occurrence can expose the common name as a delegated/query result rather than copying it. If the abstraction is deleted, the lifetime rule must state what happens to occurrences: delete them, reject deletion, or transfer them.

### 6. When to use specialization
If all occurrences have the same structure, one `Occurrence` class is enough. If occurrences naturally fall into types, add subclasses of the occurrence classifier. For example, `LibraryItem` could be an occurrence of `Title`, and `BookCopy`/`DVDRentalCopy` could be occurrence subtypes. Do not create a separate abstraction class for every tiny variation unless it has a stable common responsibility.

### 7. Difference from ordinary association and inheritance
The pattern is more specific than a generic association because it deliberately identifies set-level versus member-level information. It is not the same as generalization: a `TVSeries` is not an `Episode`. A normal association could represent the link, but the pattern gives the shared abstraction a defined responsibility and often a controlled collection/navigation. Use it when the common/occurrence distinction is part of the domain language.

### 8. Object identity and lifetime
Each occurrence has its own identity even if its values equal another occurrence. For example, two library copies of the same title share a `Title` but are different `LibraryItem` occurrences. The model should define whether an occurrence can move between abstractions, whether the abstraction owns occurrences, and how deletion/archival works.

### 9. Persistence and implementation concerns
The pattern is a design idea, not a demand for two database tables or two classes in every language. A mapping layer may store shared fields in a table and occurrence fields in another; a document may embed both. Preserve the conceptual boundary and constraints in the domain model and public interface. Do not let persistence optimization erase the common-set semantics.

### 10. Benefits and limitations
Benefits include no duplication of common data, clearer domain vocabulary, a natural place for set-level policy, and support for varied occurrence types. Limitations include extra navigation, lifecycle decisions, and possible over-modeling. Use it when the abstraction is real; avoid it for a one-off grouping with no stable meaning.

## Worked examples
### Example 1: TV series and episodes
A college media system models `TVSeries` as the abstraction and `Episode` as occurrences. A series can have zero or more episodes; every episode belongs to exactly one series. Moving a series to a new producer changes one record, not every episode. Deleting a series is blocked while episodes exist unless the product explicitly archives both.

### Example 2: Library title and copies
`Title` stores author, ISBN metadata, and catalog number. `LibraryCopy` occurrences store barcode, shelf location, condition, and loan status. A title can have many copies, and a copy can be checked out. Two copies can have equal display text but different barcodes and identity. The pattern prevents borrowing state from being copied into the title.

### Example 3: Product family
`VehicleModel` is the abstraction with manufacturer and family-level attributes. `VehicleVariant` occurrences have engine, color, and production batch. A variant belongs to one model; a model can have no variants in a newly planned catalog. A new variant type can be added without changing the model’s common contract.

### Example 4: Falsifying the model
A stakeholder says an episode can belong to two series in a crossover. The original `1 → 0..*` model is falsified. The team introduces a separate `SeriesAppearance` association with its own roles and dates, rather than forcing the episode to have a duplicate series name. The pattern is adjusted to represent a many-to-many business fact.

## Key terms & formulas
- **Abstraction:** set-level concept containing common information/behavior.
- **Occurrence:** one member of the set with individual information/behavior.
- **Abstraction–occurrence association:** a one-to-many or explicitly constrained link between them.
- **Common information:** attributes/services meaningful for the whole set.
- **Occurrence-specific information:** data belonging to one member.
- **Set-level policy:** rule managed by the abstraction, such as adding a valid member.
- **Occurrence identity:** distinct identity of a member even when values are equal.
- **Lifetime rule:** rule for creation, movement, and deletion of occurrences.
- **Common-data duplication:** avoided when each member refers to one abstraction; measure as fields repeated across a family.
- **Family completeness (check):** occurrences with a valid abstraction link ÷ all occurrences × 100%.

## Common mistakes
- Copying the abstraction’s fields into every occurrence.
- Treating an occurrence as a subclass of the abstraction without a genuine “is-a” relationship.
- Putting occurrence-specific state in the abstraction.
- Omitting the zero case when a new set may have no members.
- Ignoring what happens when an abstraction is deleted.
- Using the pattern for a temporary grouping with no stable domain meaning.
- Treating it as a database-table rule rather than a domain design principle.

## Exam prep
### Likely 2-mark questions
1. **Define the Abstraction–Occurrence pattern.** A design pattern that separates common set-level information from individual occurrence information in a related family.
2. **State the main problem it solves.** Avoiding duplication while representing members that share common data but have different individual data.
3. **Give one example.** A TV series and its episodes, or a book title and library copies.
4. **What relationship is normally used?** An association, commonly one abstraction to zero or more occurrences, with lifetime and navigation rules.
5. **Why is it not ordinary inheritance?** An occurrence belongs to or is associated with an abstraction; it is not necessarily a kind of it.
6. **What lifetime decision must be made?** What happens to occurrences when their abstraction is deleted, archived, or changed.

### Long-answer answer hints
- “Explain Abstraction–Occurrence”: context, problem, forces, structure, responsibilities, specialization, lifetime, benefits, and a class diagram.
- “Apply it to a library system”: title abstraction, copy occurrences, common vs copy-specific data, deletion and borrowing rules.
- “Differentiate it from ordinary association”: the pattern gives a deliberate set/member semantic and usually a controlled relationship; it is more than an arbitrary link.
- “How does it avoid duplication?” common data is stored once and accessed through the abstraction link; occurrence data remains local.
- “What happens when a new occurrence type is added?” add a subtype or a compatible occurrence class and update behavior/queries, without changing common data.

### Diagram template
```text
«Abstraction» 1 ─── 0..* «Occurrence»
  common state/services      individual state/services
  + add/remove member         + local operation
```
