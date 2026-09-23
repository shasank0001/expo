---
subject: oose
unit: 1
topic: nature-and-types-of-software
syllabus_ref: CSM3102 Unit-I
status: draft
---
# Nature and Types of Software
## Overview
Software is the set of instructions, data, rules, and tools that tell a computer what to do. A program is only one part of a software product: a useful product also includes the data it processes, its user documentation, configuration files, tests, and the process used to develop and maintain it. Software is intangible, but its effects can be very real—from a bank transfer to a medical decision.

Software matters because it changes quickly, is difficult to understand when it grows, and can fail in ways that hardware does not. A good software-engineering approach makes the behavior visible, tests important assumptions, records decisions, and allows change without losing control. This note covers the nature of software, the common kinds of software, and the features that shape a project.

## Explanation
### 1. Software, programs, and software products
- A **program** is a set of executable instructions. A user rarely runs only the instructions; the program uses data and interacts with an operating system, database, network, and other programs.
- A **software product** is the complete deliverable: source code or configurable components, data and schemas, executable build, documentation, tests, installation instructions, and maintenance procedures.
- Software is a **non-physical** product. Copying it is cheap, but understanding, integrating, and changing it is not cheap. The cost of communication and rework is often larger than the cost of writing the code.
- Software has **behavioral complexity**: even a small program can have many states and interactions. It also has **environmental complexity** because it depends on hardware, operating systems, networks, users, and external services.
- Software is **customizable**. The same general product can often be adapted by changing configuration, rules, or plug-in components instead of rewriting all code.
- Software **evolves** because users discover new needs, laws change, devices change, and defects are found. Maintenance is therefore a major part of its life cycle.

### 2. Important characteristics of software
1. **Intangibility:** progress cannot be judged by counting physical objects. A working executable is not enough; the requirements, design, tests, and documentation matter too.
2. **Complexity:** A team must understand parts, their responsibilities, and their interactions. Reducing coupling and hiding implementation details helps.
3. **Conformity:** The software must fit an organizational process, hardware, language, and external interfaces, not only an algorithm.
4. **Continuity:** A system is changed repeatedly; versions must remain consistent and old data must often be migrated.
5. **Invisibility:** Progress is hard to see. Models, prototypes, demos, and tests make work observable.
6. **Variability:** Two projects that use similar technology may still have different teams, requirements, and risk levels.

### 3. Types of software
**System software** supports other software or the computer itself. Examples include operating systems, device drivers, compilers, utilities, and embedded firmware. Its interface is often a platform for many applications.

**Application software** performs a user task. Word processors, spreadsheets, payroll systems, and student record systems are examples. Business applications usually store and process organizational data.

**Embedded software** runs inside a dedicated device such as a washing-machine controller, an engine controller, or a medical device. It often has strict timing, memory, power, and safety limits. A late or incorrect response can be dangerous.

**Web and mobile software** runs through browsers or app runtimes and is distributed over networks. It must work across screen sizes, browsers, connection speeds, and changing sessions. Client-side code and server-side services have different responsibilities.

**Scientific and engineering software** supports calculations, simulations, data analysis, or design. Numerical accuracy, reproducibility, and validation with trusted reference results are important. A small rounding error can have a large physical consequence.

**Transaction-processing software** handles a stream of business events such as orders, payments, or reservations. It needs consistency, auditability, recovery, and often simultaneous users.

**Real-time and safety-critical software** must respond within a time bound or control a safety-related system. Examples include flight control, industrial control, and an anti-lock braking system. Average performance is not enough; worst-case latency may be the key requirement.

**Library, framework, and reusable component software** provides services to other developers. It is judged by documentation, compatibility, quality, and ease of use. A service library can be embedded in many products.

**Tools and development software** include editors, build systems, version-control systems, static analyzers, test frameworks, and modeling tools. They improve the process used to make other software.

### 4. Product versus service
A **software product** is usually delivered as a versioned release, such as an operating-system update. A **software service** is continuously operated, such as an online banking service. Services have additional concerns—availability, incident response, backup, monitoring, and compatibility—because users depend on them at all times.

### 5. Why the type affects engineering decisions
The type is not just a label. It changes the engineering priorities:
- A safety-critical controller needs traceability, proof of critical conditions, and conservative verification.
- A web application needs threat analysis, browser compatibility, network error handling, and rolling deployment.
- A scientific package needs validated algorithms, unit consistency, reproducibility, and benchmark tests.
- A reusable library needs stable interfaces, backward compatibility, dependency management, and good documentation.
- A transaction system needs database constraints, idempotency, concurrency control, and recovery testing.

## Worked examples
### Example 1: Classifying a system
A college has a web application for students to enter marks, a database, and a mobile notification service. The main application is **web/business application software**; the notification service may be a separate service; the database and web server are supporting system software. Because marks affect records, the application is transaction-processing software. It also has security and usability requirements that are separate from its basic calculation requirement.

### Example 2: Embedded software
Suppose a program controls an automatic door. It is not just a desktop application: it is embedded software. It reads a sensor, decides whether to open the door, and drives a motor. Requirements must include the response deadline, behavior during sensor failure, safe shutdown, and the maximum number of times the door may cycle. Testing only the normal case is unsafe.

### Example 3: Product completeness
A student submits an attendance application. The source code and executable are useful, but the product is incomplete without the student schema, sample data, installation guide, admin procedure, test report, and a rule explaining how absence is calculated. This illustrates why software project plans must include non-code deliverables.

### Example 4: A small quality trade-off
A navigation app may use a simplified map to load quickly on a low-cost phone. That is an efficiency trade-off, not necessarily a defect. The team records the target device and accepts a later map update. Explicitly stating the assumption prevents the customer and tester from using incompatible expectations.

## Key terms & formulas
- **Program:** executable instructions.
- **Software product:** program(s) + data + documentation + configuration + tests + development/maintenance process.
- **System software:** software that supports a computer or other software.
- **Application software:** software that directly supports a user task.
- **Embedded software:** software controlling a device within a larger system.
- **Real-time constraint:** a deadline by which an action or response must occur.
- **Maintainability:** effort and risk required to change a product.
- **Product complexity:** a useful qualitative sum of code, states, interfaces, dependencies, data, and environmental assumptions; it is not normally reduced to one simple number.
- **Quality rule of thumb:** quality must be specified as an attribute plus a measurable criterion, for example, “95% of valid requests return within 2 seconds,” not merely “the system should be fast.”

## Common mistakes
- Calling any source-code file a complete software product.
- Treating software as a one-time build instead of a product that changes throughout its life.
- Confusing an application with the operating system, compiler, or driver on which it runs.
- Assuming all software has the same testing needs; safety-critical and web systems do not.
- Describing embedded software only as “code for a device” and forgetting timing, failure modes, power, and memory limits.
- Saying a service is finished at release when it also needs operation, monitoring, and maintenance.
- Giving a quality label without an observable measure or acceptance criterion.

## Exam prep
### Likely 2-mark questions
1. **Define software product and give two components besides source code.** A versioned set of programs together with data, documentation, configuration, tests, and the process used to operate and change it; examples: schema and user guide.
2. **State two characteristics of software.** Any two of intangibility, complexity, change, conformity, continuity, and environmental dependence, with a one-line explanation.
3. **Differentiate system and application software.** System software supports a platform; application software completes a user goal.
4. **Why is software maintenance important?** Requirements, interfaces, laws, and defects change throughout a product's life, so maintenance preserves value and correctness.
5. **Give one example of safety-critical software and one quality concern.** Engine controller; deadline, sensor-failure behavior, and safe shutdown.

### Long-answer answer hints
- “Explain the nature and types of software”: define program versus product; explain intangibility, complexity, conformity, continuity, and variability; classify system, application, embedded, web/mobile, scientific, transaction, and real-time software; connect each type to a project concern.
- “Compare application, embedded, and scientific software”: give examples, execution environment, data/timing demands, and testing emphasis.
- “Software is intangible—yet why can it be expensive?” explain that the difficult work is understanding, integration, communication, and change, not copying bits.
- “How does software type influence a project plan?” discuss security, timing, validation, compatibility, or recovery priorities.
- “Explain software as a product rather than a program.” Use an attendance-system example and list non-code deliverables.

### One-minute answer frame
Definition → characteristics → classification table → one type-specific engineering decision → example → conclusion.
