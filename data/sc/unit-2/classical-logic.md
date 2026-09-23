---
subject: sc
unit: 2
topic: classical-logic
syllabus_ref: CSM3202 Unit-II
status: draft
---
# Classical Logic

## Overview

Classical logic represents statements that are either true or false. Its connectives—NOT, AND, OR, implication, and equivalence—follow Boolean rules. A statement may contain variables, and a rule can then be used to derive conclusions from known facts.

Classical logic is the foundation of Boolean control, theorem proving, databases, and crisp expert systems. It is exact and easy to verify, but it cannot naturally express “mostly true,” “slightly high,” or a rule that is only approximately satisfied.

## Explanation

### 1. Propositions and truth values

A **proposition** is a declarative sentence that is either true or false.

Examples:

- \(p\): The temperature is above \(30^\circ C\).
- \(q\): The fan is ON.
- \(r\): \(2+2=4\).

A proposition has one truth value from \(\{T,F\}\). A sentence such as “Close the door” may be an instruction rather than a proposition until a definite truth value can be assigned.

### 2. Basic connectives

#### Negation

\[
\neg p
\]

is false when \(p\) is true and true when \(p\) is false.

| \(p\) | \(\neg p\) |
|---|---|
| T | F |
| F | T |

#### Conjunction

\[
p\land q
\]

is true only if both \(p\) and \(q\) are true.

#### Disjunction

\[
p\lor q
\]

is true if at least one of them is true. Unless stated otherwise, the symbol has inclusive meaning.

#### Implication

\[
p\rightarrow q
\]

is false only when \(p=T\) and \(q=F\).

| \(p\) | \(q\) | \(p\rightarrow q\) |
|---|---|---|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

An implication is a material rule; its truth table does not mean that an implication is a causal relationship.

#### Equivalence

\[
p\leftrightarrow q
\]

is true when both have the same truth value. It is also written

\[
(p\rightarrow q)\land(q\rightarrow p).
\]

### 3. Truth tables

A truth table gives the truth value of a formula for every combination of its atomic variables.

For \(p\lor(\neg p\land q)\):

| \(p\) | \(q\) | \(\neg p\) | \(\neg p\land q\) | \(p\lor(\neg p\land q)\) |
|---|---|---|---|---|
| T | T | F | F | T |
| T | F | F | F | T |
| F | T | T | T | T |
| F | F | T | F | F |

Because it is true whenever \(p\) is true, the formula is valid:

\[
p\lor(\neg p\land q)\equiv p.
\]

A **tautology** is true for every assignment. A **contradiction** is false for every assignment. A formula is **contingent** if it is true for some assignments and false for others.

### 4. Equivalence and normal forms

Two formulas are logically equivalent if they have the same truth value under every assignment, written

\[
p\equiv q.
\]

Common equivalences include:

\[
\neg\neg p\equiv p,
\]

\[
p\lor(q\land r)\equiv(p\lor q)\land(p\lor r),
\]

\[
p\land(q\lor r)\equiv(p\land q)\lor(p\land r),
\]

\[
p\rightarrow q\equiv\neg p\lor q,
\]

\[
p\leftrightarrow q\equiv(p\rightarrow q)\land(q\rightarrow p).
\]

The **conjunctive normal form (CNF)** is an AND of OR clauses, and the **disjunctive normal form (DNF)** is an OR of AND terms. Converting to a standard form makes comparison and automated reasoning easier.

### 5. Predicate logic

Propositional logic treats each whole statement as one symbol. **Predicate logic** exposes objects, properties, and relations.

An atomic formula has the form

\[
P(x)
\]

or

\[
R(x_1,\ldots,x_n).
\]

Examples:

- \(Human(x)\): person \(x\) is human.
- \(Mortal(x)\): person \(x\) is mortal.
- \(Loves(Alice,Bob)\): Alice loves Bob.

A universally quantified statement is

\[
\forall x\,P(x),
\]

meaning \(P\) holds for every object in the domain. An existential statement is

\[
\exists x\,P(x),
\]

meaning \(P\) holds for at least one object.

### 6. Variables, binding, and scope

In

\[
\forall x\,(\exists y\,Loves(x,y)),
\]

the variable \(y\) is bound inside the existential quantifier. A variable not bound by a quantifier is free. Equivalence of formulas depends on preserving meaning and binding, not just on the order of symbols.

### 7. Rules of inference

#### Modus ponens

\[
\frac{p,\quad p\rightarrow q}{q}
\]

If \(p\) is true and “if \(p\), then \(q\)” is true, conclude \(q\).

#### Modus tollens

\[
\frac{\neg q,\quad p\rightarrow q}{\neg p}
\]

If \(q\) is false, the implication is true, and the rule is valid, conclude that \(p\) is false.

#### Hypothetical syllogism

\[
\frac{p\rightarrow q,\quad q\rightarrow r}{p\rightarrow r}
\]

#### Disjunctive syllogism

\[
\frac{p\lor q,\quad \neg p}{q}
\]

#### Simplification and conjunction

\[
\frac{p\land q}{p},\qquad
\frac{p,\quad q}{p\land q}.
\]

A sound rule preserves truth: if all premises are true, the conclusion must be true in a valid interpretation.

### 8. Resolution

A clause is a disjunction of literals. Two complementary literals occur in

\[
p\lor q
\]

and

\[
\neg p\lor r.
\]

Their resolvent is

\[
q\lor r.
\]

Resolution is a sound inference used in theorem proving and expert systems. Repeated resolution can derive a contradiction from \(P\) and \(\neg P\), proving the query through refutation.

### 9. Horn clauses

A Horn clause contains at most one positive literal:

\[
p_1\land\cdots\land p_n\rightarrow q
\]

or, in logic-programming form,

\[
q\leftarrow p_1,\ldots,p_n.
\]

Rules with only one antecedent are definite clauses. Horn logic is efficient for forward and backward chaining and forms the basis of Prolog and many production systems.

### 10. Forward and backward chaining

- **Forward chaining** begins with known facts and applies rules to derive new facts. It is useful for monitoring and forward planning.
- **Backward chaining** begins with a goal and looks for rules whose conclusions match it. It is useful for diagnosis and answering a specific query.

### 11. Knowledge representation with rules

A production rule has the form

\[
\text{IF condition THEN action}.
\]

Conditions may be propositions or predicate-logic statements. The rule base captures domain knowledge, while the inference engine selects and applies rules.

A deterministic system should specify conflict handling when several rules fire, whether facts are monotonic, and how missing or uncertain information is treated.

### 12. Limits of classical logic

Classical logic requires exact truth values. It does not directly represent:

- uncertain measurements;
- partial truth;
- fuzzy linguistic terms;
- varying strength of evidence;
- absence of a crisp threshold.

Fuzzy logic extends this foundation by replacing Boolean truth with values in \([0,1]\) and defining operations for those values. Hybrid systems may still use classical logic for hard constraints and fuzzy logic for gradual conditions.

## Worked examples

### Example 1: Modus ponens

Facts:

\[
\text{CableFaulted}\rightarrow\text{NoSignal}
\]

and

\[
\text{CableFaulted}=T.
\]

Since both premises are true, modus ponens gives

\[
\text{NoSignal}=T.
\]

It does not automatically identify another possible cause unless additional rules are provided.

### Example 2: Modus tollens

Suppose

\[
\text{Rain}\rightarrow\text{GroundWet}
\]

and the ground is not wet. Then

\[
\neg\text{GroundWet}.
\]

By modus tollens,

\[
\neg\text{Rain}.
\]

The inference depends on the implication being accepted as a general rule.

### Example 3: Syllogism

Let

\[
A\rightarrow B,\qquad B\rightarrow C.
\]

Hypothetical syllogism gives

\[
A\rightarrow C.
\]

If \(A\) is true, two applications of modus ponens establish \(B\) and then \(C\).

### Example 4: Resolution

Knowledge base:

\[
Human(x)\rightarrow Mortal(x),
\]

\[
Socrates(Human),
\]

and the goal \(\exists x\,Mortal(x)\). In propositional form, the clauses are

\[
\neg Human\lor Mortal,\qquad Human.
\]

Resolving gives \(Mortal\).

### Example 5: A conclusion that does not follow

Given

\[
Rain\rightarrow WetStreet,\qquad Sun\rightarrow DryStreet,
\]

and the fact Rain, one can conclude WetStreet. One cannot conclude DryStreet or NotWet from these facts alone. A classical argument requires valid premises and a sound rule.

## Key terms & formulas

- **Proposition:** A sentence with truth value \(T\) or \(F\).
- **Tautology:** A formula true for every assignment.
- **Contradiction:** A formula false for every assignment.
- **Predicate:** A property or relation over objects.
- **Quantifiers:** \(\forall x\) and \(\exists x\).
- **Implication:** \(p\rightarrow q\equiv\neg p\lor q\).
- **Equivalence:** \(p\leftrightarrow q\).
- **Sound rule:** True premises guarantee a true conclusion.

Modus ponens:

\[
p,\ p\rightarrow q\ \vdash\ q.
\]

Resolution:

\[
p\lor q,\quad\neg p\lor r\ \vdash\ q\lor r.
\]

## Common mistakes

1. **Treating an imperative as a proposition.** A command is not true or false.
2. **Reading implication as strict cause and effect.** Material implication has only the stated truth-table meaning.
3. **Assuming an implication is false when its premise is false.** Only true-premise/false-conclusion makes material implication false.
4. **Using exclusive OR when OR is intended.** “At least one” is inclusive.
5. **Treating universal and existential statements as interchangeable.** They have very different meanings.
6. **Dropping quantifier scope while replacing a formula.** Variable binding must be preserved.
7. **Claiming a conclusion follows merely because it is plausible.** The inference must be logically valid or based on an explicitly stated rule.
8. **Using fuzzy truth grades in a classical truth table.** Classical values remain binary.

## Exam prep

### Likely 2-mark questions

- **Define a proposition and give two examples.**  
  **Hint:** Definite declarative statements with definite truth values.

- **Write the truth table of implication.**  
  **Hint:** Only the row \(T\rightarrow F\) is false.

- **State modus ponens and modus tollens.**  
  **Hint:** Write both premises and conclusions symbolically.

- **Define a predicate and a quantifier.**  
  **Hint:** Property/relation; \(\forall\) and \(\exists\).

- **What is a tautology?**  
  **Hint:** A formula true under every valuation.

### Likely long-answer questions

- **Explain propositional logic, connectives, truth tables, and equivalences.**  
  **Hint:** Define each connective, complete tables, and discuss validity.

- **Explain predicate logic with quantifiers and an example.**  
  **Hint:** Objects, predicates, \(\forall\), \(\exists\), scope, and instantiation.

- **Discuss rules of inference and modus ponens in a diagnostic system.**  
  **Hint:** Show premise/conclusion and describe forward or backward chaining.

- **Explain resolution for theorem proving.**  
  **Hint:** Clauses, complementary literals, resolvent, refutation, and completeness under standard assumptions.

- **Compare classical logic with fuzzy logic.**  
  **Hint:** Binary truth and hard antecedents versus graded truth and approximate matching.
