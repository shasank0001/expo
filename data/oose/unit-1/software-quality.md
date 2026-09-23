---
subject: oose
unit: 1
topic: software-quality
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Software Quality
## Overview
Software quality is the degree to which a product satisfies stated needs and is fit for its intended use. It is not just “there are few bugs.” A useful product is correct, reliable, understandable, secure, fast enough, maintainable, portable, and acceptable to real users. Quality is built into requirements, design, implementation, testing, and operations; inspecting code only at the end is too late.

This note covers software quality characteristics, measurable quality criteria, quality assurance and quality control, reviews and tests, and the way quality trades off against cost, time, and scope. A good answer connects an abstract quality word to evidence that a team can check.

## Explanation
### 1. Definition and product perspective
Quality is fitness for use in a stated context. The same application may be high quality for a classroom and unacceptable for emergency dispatch. A quality claim must name:
1. the **characteristic** (for example reliability or usability),
2. the **criterion or measure** (for example 99.9% successful transactions),
3. the **measurement method**,
4. the **environment and target**.

A product can be correct for the specified requirements but still be unusable if the requirements omitted a real user need. Conversely, a technically capable product is not high quality if unauthorized users can see another student's marks.

### 2. Main quality characteristics
#### Correctness
The product produces the required behavior and produces correct results for valid inputs. Correctness is compared with the specification and with approved changes.

#### Reliability
The product performs consistently over time and does not fail unexpectedly under expected conditions. Reliability depends on fault tolerance, recovery, availability, and correct handling of failures. It is different from correctness: software can compute the wrong result once, or it can be correct on every calculation but crash often.

#### Usability and user friendliness
Users can learn and use the product efficiently, effectively, and satisfactorily. Usability includes understandable messages, consistent controls, accessibility, appropriate response time, and recovery from mistakes.

#### Efficiency
The product uses CPU, memory, storage, network, and energy economically. Efficiency has workload and resource measures, not a universal “fastest” goal.

#### Maintainability
A maintainer can repair, improve, or adapt the product with reasonable effort and risk. High modularity, low coupling, clear code, tests, and documentation support maintainability.

#### Portability
The product can move to a different hardware, operating system, database, language, or environment with limited change. Portability is related to but not identical to adaptability or configurability.

#### Reusability and interoperability
A reusable component can be used in another product safely. Interoperability means the product can exchange meaningful data and work with other systems, platforms, or services.

#### Security
The product protects confidentiality, integrity, availability, and appropriate authentication/authorization. Security requirements should be written with threat and abuse cases, not added only after a breach.

#### Testability and observability
Testability indicates whether requirements and design permit meaningful test design. Observability indicates whether behavior and failures can be monitored in operation.

### 3. Quality criteria
A **criterion** turns a characteristic into an observable target. Examples:
- 95% of valid mark-entry requests finish within two seconds on the target network.
- At least 99.5% of scheduled inspections are successfully recorded during a daily window.
- A student can recover a mistaken entry using no more than three screens.
- Every privileged operation produces an audit record containing user, time, and action.
- A critical service can be restored from backup within 30 minutes.

A qualitative target such as “easy to use” should be clarified with a task, user profile, and time/error measure.

### 4. Quality assurance versus quality control
**Quality assurance (QA)** is the set of planned activities that prevent defects and improve the process: standards, training, checklists, reviews, audits, process monitoring, and training. **Quality control (QC)** checks the product: inspections, tests, measurements, and defect detection. The terms are sometimes used loosely, but the useful distinction is prevention versus detection/verification.

### 5. How quality is built in
- **Requirements:** measurable, prioritized, realistic, and testable quality attributes.
- **Design:** modularity, error handling, usability, security, and maintainability decisions.
- **Implementation:** conventions, code review, static analysis, and automated builds.
- **Testing:** unit, integration, system, acceptance, regression, performance, security, and usability checks as appropriate.
- **Deployment:** controlled installation, monitoring, backups, and incident response.
- **Maintenance:** defect data and lessons learned improve both product and process.

### 6. Review and inspection
A review checks a product or process against defined criteria. Walkthroughs let authors explain the artifact; technical reviews examine technical correctness; inspections find defects in a structured way. Reviews are effective because defects found before execution are cheaper to correct, and because teams share knowledge.

### 7. Quality trade-offs and the cost of quality
High quality may require additional design, testing, security, documentation, and time. Poor quality may create cost through support, rework, lost trust, and operation. “Do not test everything thoroughly” is not a quality strategy; it is a risk decision. The team should document the chosen level and the evidence that makes it acceptable.

## Worked examples
### Example 1: Usability criterion
“Easy to use” is vague. For the inspection app, measure “a trained inspector can record a compliant inspection in under three minutes with no critical errors in two user trials.” This is measurable and connected to a real task.

### Example 2: Reliability and availability
An online attendance system may compute totals correctly (correctness) but lose a request during a network failure (reliability problem). Retrying safely, showing status, and recovering the transaction address both quality characteristics.

### Example 3: Security review
Threat modeling asks whether an unauthenticated user can edit another student's record. Encryption alone does not fix an authorization defect. The requirement says only authorized instructors may change marks, and the test attempts the forbidden action. The criterion is “no unauthorized update succeeds.”

### Example 4: Trade-off
A prototype uses a simple map cache to make demonstrations fast. It works for small data, but on a phone it may exhaust memory. The team measures efficiency under the stated workload and chooses a bounded cache. The trade-off is documented rather than hidden.

## Key terms & formulas
- **Quality characteristic:** a broad quality dimension such as correctness or maintainability.
- **Quality criterion:** a measurable target for a characteristic.
- **Quality metric:** the observed value of a measure.
- **Fitness for use:** suitability for a particular user, purpose, environment, and task.
- **QA:** planned prevention and process improvement activities.
- **QC:** inspection and testing of products and outputs.
- **Defect:** a condition that violates a requirement, design, or expected behavior.
- **Productivity:** useful output per unit of effort, not simply lines of code.
- **Reliability availability (simple conceptual relationship):** availability depends on both how often a service is up and how reliably it recovers; high reliability alone does not guarantee availability.
- **Quality objective example:** error density = defects / size, useful only with a defined size and defect severity.

## Common mistakes
- Defining quality as “no bugs” and ignoring usability, security, maintainability, or fitness for use.
- Writing a quality attribute with no criterion, workload, or measurement method.
- Confusing QA with testing alone.
- Assuming more testers always produce higher quality if requirements and design are weak.
- Treating quality as a final gate; prevention and incremental verification are more effective.
- Ignoring the cost and schedule consequences of a quality target without making the trade-off explicit.

## Exam prep
### Likely 2-mark questions
1. **Define software quality.** The degree to which a product conforms to requirements and is fit for its intended use.
2. **Name four quality characteristics.** Any four of correctness, reliability, usability, efficiency, maintainability, portability, security, reusability, or interoperability.
3. **Differentiate QA and QC.** QA prevents and improves process defects; QC detects and verifies product defects.
4. **Turn “the system must be fast” into a criterion.** Example: 95% of valid requests complete within two seconds at the agreed workload.
5. **Why is quality built early?** Early detection is cheaper and prevents downstream propagation of errors.

### Long-answer answer hints
- “Explain software quality”: definition, characteristics, criteria/metrics, QA/QC, reviews/tests, and a practical trade-off example.
- “Quality assurance versus quality control”: give a process example and a product example for each.
- “How can a team measure maintainability?” Combine evidence such as change effort, defect density, time to locate a defect, code complexity, and review findings; do not use LOC alone.
- “Security is a quality attribute”: explain confidentiality, integrity, availability, authorization, threat modeling, and a test.
- “Quality versus cost”: explain prevention, detection, internal and external failure costs, and why skipping quality is not free.

### Quick answer checklist
Attribute → scenario → criterion → measurement → evidence → improvement action.
