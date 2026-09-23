---
subject: dwdm
unit: 3
topic: multilevel-association-mining
syllabus_ref: CSM3101 Unit-III
status: draft
---
# Multilevel Association Mining

## Overview

A supermarket database may contain `Dell laptop`, `HP laptop`, and the broader category `laptop`. A frequent pattern can include items from different levels of such hierarchies. Multilevel association mining finds associations such as “customers who buy a laptop often buy a printer,” where the two items are at different abstraction levels. The challenge is to balance detail, interest, and the number of candidates.

## Explanation

### 1. Concept hierarchies

A **concept hierarchy** organizes related items from specific to general. For example:

```text
Computer
├── Laptop
│   ├── Dell laptop
│   └── HP laptop
└── Desktop
```

An item at a higher level is an ancestor; a lower-level item is a descendant. If `laptop` is bought, one or more of its descendants may have been bought, but not necessarily all of them. Hierarchy definitions can come from product catalogs, taxonomies, or domain experts.

### 2. Multilevel itemsets and rules

A **multilevel itemset** contains items from different levels. A rule may be:

- same-level: `Dell laptop -> HP laptop`;
- cross-level: `Dell laptop -> laptop accessory`;
- mixed: `printer -> HP laptop -> software`.

A cross-level rule is not automatically less interesting than a same-level rule. It may be exactly what a manager needs, for example `printer -> laptop` to plan compatible bundles.

### 3. Support at a level

For an ancestor item, support must be computed from transactions containing any relevant descendant, subject to the hierarchy's counting definition. The same transaction can contribute once to `laptop` even if it contains several laptop brands. If transactions count every descendant occurrence, that is a different and potentially duplicate-heavy definition, so state the convention.

A common approach treats ancestor and descendant items as distinct encoded items and applies a minimum support at each level. An ancestor with high support can then produce useful generalized patterns, while detailed patterns remain rare.

### 4. Uniform minimum support

A single threshold is applied to every level. This is simple, but high-level items naturally have more support than low-level items. A strict global threshold can miss rare but useful detailed patterns. Conversely, a low threshold can produce many high-level rules.

### 5. Multiple minimum supports

A more flexible method assigns a threshold \(s_l\) to each level. A high-level pattern may require a stronger support threshold, while a lower-level pattern can use a lower threshold. The pattern-mining algorithm must then avoid pruning a lower-level pattern using the high-level threshold. Candidate support and pruning are checked against the applicable level-specific thresholds.

A common idea is to mine high-level patterns first and progressively deepen only promising branches. This is **top-down progressive deepening**: begin with the root category, refine the most promising patterns, and do not enumerate all descendants unless they can meet their threshold.

### 6. Mining considerations

- Encode hierarchy information with the itemset, not only in a separate lookup table.
- Define how ancestor transactions are counted.
- Avoid treating `laptop`, `Dell laptop`, and `HP laptop` as three unrelated products when the hierarchy says they overlap.
- Select thresholds that reflect business value and sample size.
- Evaluate cross-level rules with the same support, confidence, lift, and significance checks as ordinary rules.

## Worked examples

### Example 1: Hierarchy encoding

Hierarchy:

```text
Electronics -> Computer -> Laptop -> {Dell, HP}
```

Transactions:

| Basket | Detailed items | Generalized interpretation |
|---|---|---|
| 1 | Dell laptop, printer | computer, laptop, printer |
| 2 | HP laptop, printer | computer, laptop, printer |
| 3 | Dell laptop | computer, laptop |
| 4 | desktop, monitor | computer, monitor |

With 4 baskets, `computer` occurs in all 4, `laptop` in 3, and `printer` in 2. If the threshold is 2, `{laptop,printer}` is frequent. If `minconf=0.60`, then

\[
\operatorname{conf}(laptop\rightarrow printer)=2/3=0.667,
\]

so it passes. `Dell laptop -> printer` has confidence 1/2=0.50 and fails that threshold, even though it is a meaningful low-level pattern. This is why level-specific support and business rules can be useful.

### Example 2: Two minimum supports

Let `electronics` be a high-level item and `wireless mouse` a lower-level item, with \(s_1=0.30\) for level 1 and \(s_2=0.10\) for level 2. A candidate containing `electronics` must be checked against 30% support, while `wireless mouse` may pass at its 10% threshold. A pruning rule that declares every item below 30% infrequent would incorrectly remove the detailed pattern before level-specific processing.

### Example 3: Progressive deepening

Suppose high-level mining finds:

```text
computer -> software       support 0.25, lift 1.4
laptop -> software         support 0.20, lift 1.3
```

The algorithm may refine `laptop -> software` to `Dell laptop -> software` and `HP laptop -> software`. If each brand has support 0.08 and its level threshold is 0.10, neither is retained. No need exists to test every brand under unrelated `desktop` branches.

## Key terms & formulas

- **Concept hierarchy:** tree/partial order of general and specific concepts.
- **Ancestor/descendant:** upper/lower item in the hierarchy.
- **Multilevel itemset:** items from more than one hierarchy level.
- **Cross-level rule:** antecedent and consequent are at different abstraction levels.
- **Uniform support:** one minimum support for all levels.
- **Level-specific support:** threshold \(s_l\) for level \(l\).
- **Top-down progressive deepening:** mine broad levels, then refine promising branches.
- **Hierarchy-aware support:** support calculated with the declared ancestor/descendant counting rule.
- **Generalized item:** an item representing a concept such as `laptop`.

## Common mistakes

1. **Counting a descendant transaction twice:** a basket containing several brands should normally contribute one count to the ancestor.
2. **Using one high threshold for all levels:** detail patterns may be unnecessarily suppressed.
3. **Pruning descendants using an ancestor's threshold:** level-specific rules require the correct threshold and direction.
4. **Ignoring hierarchy overlap:** `laptop` and `Dell laptop` are not independent products.
5. **Reporting a high-level rule as a detailed recommendation:** label its abstraction level explicitly.

## Exam prep

**Likely 2-mark questions**
1. Define a concept hierarchy and a multilevel itemset. *Hint: general-to-specific relations and items at multiple levels.*
2. What is top-down progressive deepening? *Hint: mine general patterns first and refine selected branches.*
3. Why use level-specific minimum support? *Hint: high-level items are naturally more frequent than detail items.*

**Likely long-answer questions**
1. Explain multilevel association mining with a product hierarchy and a complete support calculation. *Hint: define ancestor counts, rules, thresholds, and mining strategy.*
2. Compare uniform and multiple minimum-support approaches. *Hint: simplicity and pruning versus detail discovery and complexity.*
3. Discuss semantic issues in representing ancestor and descendant items. *Hint: overlapping transactions, double counting, and rule interpretation.*
