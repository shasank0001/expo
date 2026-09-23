---
subject: oose
unit: 5
topic: equivalence-partitions-and-boundary-values
syllabus_ref: CSM3102 Unit-V
status: draft
---
# Equivalence Partitioning and Boundary-Value Analysis
## Overview
**Equivalence partitioning (EP)** divides an input domain into classes whose members are expected to be handled in the same way. A representative value from each class is selected, reducing the number of tests without losing the main behavioral distinction. **Boundary-value analysis (BVA)** tests values at, just below, and just above boundaries where behavior often changes, such as minimum/maximum, inclusive/exclusive limits, or a partition edge.

Both are black-box input techniques. They are simple but powerful when the requirements and input rules are clear. They must include invalid partitions, missing/empty values, and combinations of inputs; one representative per class cannot prove correctness.

## Explanation
### 1. Equivalence partitioning
An equivalence class is a set of inputs for which the expected behavior is the same according to the specification. Typical classes are:
- valid versus invalid;
- lower, middle, and upper ranges;
- present versus missing;
- empty versus non-empty;
- valid format versus malformed format;
- authorized versus unauthorized category;
- ordinary, extreme, and repeated values.

A test suite chooses one or more representatives from each class, with emphasis on valid and invalid behavior. The class must be defined by a rule, not just by a convenient number.

#### Example: age requirement
For “user must be at least 18,” classes are:
- invalid: `age < 18` (if values are restricted to a defined domain);
- valid: `age >= 18`.
A representative might be 17 and 21. If ages are only integers, test exact values around 18 with BVA.

#### Example: string field
For a required inspection code:
- valid nonempty code with allowed characters;
- empty string;
- null/missing;
- too short;
- valid length but forbidden character;
- over maximum length.
A partition with no expected behavior is not complete.

### 2. Choosing representatives
Choose values that are clearly inside the class, plus representative edge values when risk warrants it. Do not choose a value that accidentally belongs to another class. For expensive or destructive operations, use safe synthetic data.

### 3. Boundary-value analysis
BVA focuses on boundaries where the program's behavior changes:
- minimum and maximum allowed values;
- first invalid and last valid values;
- lower/upper range edges;
- just-below/at/just-above a threshold;
- transition between two input formats;
- list length limits;
- date/time boundaries, leap years, and time zones;
- page, file-size, and rate limits.

For an inclusive range `L ≤ x ≤ U`, useful values are:
`L - 1, L, L + 1, U - 1, U, U + 1`, where those values are valid test inputs and the expected result is defined for out-of-range cases. For an exclusive range `L < x < U`, test around `L` and `U` according to the specification. For a maximum `x ≤ M`, use `M-1, M, M+1`.

### 4. Valid and invalid partitions
Most defects occur at boundaries and in invalid input, so a BVA/EP suite normally includes:
- one representative for every valid class;
- at least one for every invalid class;
- boundary values for numeric, size, time, and ordering constraints;
- missing, duplicate, and malformed data;
- combinations that interact.

Invalid input behavior must be specified: reject with a clear message, ignore, default, or quarantine. If no behavior is specified, the test can uncover a requirements gap.

### 5. Combining EP and BVA
A practical table for `1 ≤ score ≤ 100`:

| Class/point | Example | Expected |
|---|---:|---|
| invalid below | 0 | reject |
| lower boundary | 1 | accept |
| valid interior | 50 | accept |
| upper boundary | 100 | accept |
| invalid above | 101 | reject |

EP supplies the classification; BVA supplies the risky points. Together they test behavior changes and representative classes with few cases.

### 6. Input domains beyond numbers
Boundaries also exist for:
- strings (empty, one character, maximum length);
- collections (empty, one, maximum, maximum + 1);
- dates (month/year rollover, leap day, timezone boundary);
- file uploads (zero bytes, maximum size, wrong type);
- search queries (empty, wildcard, very long, special characters);
- permissions (no role, multiple roles, expired role);
- transactions (zero, one, maximum amount, duplicate request).

### 7. Limitations
- The technique depends on a correct specification and known input domain.
- One representative cannot expose every interaction or calculation error.
- Equivalent inputs may still need boundary/state-specific behavior.
- It does not test sequence, timing, concurrency, or usability by itself.
- “Invalid” must have a clear expected response; otherwise the test is an interpretation.

## Worked examples
### Example 1: Password length
Requirement: password 8–20 characters, at least one digit.
Partitions:
- length 0–7;
- length 8–20 with digit;
- length 8–20 without digit;
- length 21+;
- empty/missing.
BVA tests lengths 7, 8, 9, 19, 20, 21, with valid/invalid character patterns. Expected result must distinguish length from character rule; testing 20 no-digit and 20 with digit exercises the combination.

### Example 2: Upload
For a maximum 5 MB image:
- below limit: 1 byte, 4.9 MB;
- at limit: exactly 5 MB;
- above: 5 MB + 1 byte;
- wrong type, empty file, corrupted file, duplicate name.
The test verifies rejection is clear, no partial record is stored, and cleanup occurs.

### Example 3: Date boundary
For a valid year from 2020 to 2030, test 2019, 2020, 2021, 2029, 2030, 2031. For a date field, test 29 February in leap and non-leap years, month 12/13, and the midnight timezone transition where relevant.

### Example 4: Interaction
An input has two valid partitions: country and amount. Selecting one representative from each full cross-product is not necessary if behavior is independent, but if a rule applies only to one country/amount combination, add a targeted pair. EP/BVA and decision tables work together.

## Key terms & formulas
- **Equivalence class:** inputs expected to produce equivalent behavior.
- **Valid partition:** input accepted under the specification.
- **Invalid partition:** input rejected or specially handled.
- **Representative value:** chosen member of a class.
- **Boundary:** point where expected behavior changes.
- **Lower/upper boundary:** minimum/maximum allowed edge.
- **BVA values:** `L-1, L, L+1` and `U-1, U, U+1` for an inclusive range.
- **Partition coverage:** executed representatives ÷ defined partitions × 100%.
- **Boundary coverage:** selected boundary points exercised ÷ selected boundary points × 100%.
- **Robust boundary set:** valid, just-below, at, and just-above values where defined.

## Common mistakes
- Choosing a boundary value that is not in the input domain or whose behavior is undefined.
- Testing only valid values and missing empty, null, malformed, unauthorized, and oversized inputs.
- Assuming all values in an equivalence class are truly equivalent when interaction rules exist.
- Confusing a partition boundary with a numeric boundary value.
- Using “expected result = no error” for every invalid input without checking requirements.
- Reporting test count without showing which partitions and boundaries were covered.

## Exam prep
### Likely 2-mark questions
1. **Define equivalence partitioning.** Dividing an input domain into classes with equivalent expected behavior and testing representatives.
2. **Define BVA.** Testing values at, just below, and just above boundaries where behavior changes.
3. **For an inclusive range 1..100, list BVA values.** 0, 1, 2, 99, 100, 101 (or the relevant subset).
4. **Why include invalid partitions?** Invalid inputs often expose missing validation, security, and error-handling defects.
5. **Give two nonnumeric boundaries.** Empty/one/max collection, date rollover, file size, string length, or permissions.
6. **What is the main limitation of EP?** It assumes members of a class behave equivalently and cannot test all interactions.

### Long-answer answer hints
- “Explain EP and BVA”: definitions, steps, valid/invalid classes, boundary selection, formulas, examples, and limitations.
- “Apply to a password/file/upload requirement”: list partitions, boundaries, expected behavior, and combination cases.
- “Differentiate EP and BVA”: representative classes versus risky transition points; they complement each other.
- “Explain a boundary-value test for a range”: formula, values, domain restrictions, and expected outputs.
- “Why are invalid cases essential?” security, robustness, error messages, side effects, and state preservation.

### Example table
```text
Range: 1 ≤ n ≤ 10
0 (below), 1 (min), 2 (above min), 9 (below max), 10 (max), 11 (above)
```
