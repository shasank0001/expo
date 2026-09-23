---
subject: dwdm
unit: 1
topic: evolution-of-it-into-dbms
syllabus_ref: CSM3101 Unit-I
status: draft
---
# Evolution of IT into DBMS

## Overview

Information technology (IT) began as a way to record and process small amounts of routine information. Punched cards, paper files, and manual registers preceded electronic systems. Early computer systems stored data in separate application files. As organizations accumulated more records and more users, file-based systems became slow, inconsistent, and difficult to maintain.

The Database Management System (DBMS) introduced a structured way to store, retrieve, update, and control data. Instead of placing data separately inside every application program, a DBMS provides a common service for defining, storing, querying, and protecting data. SQL later made relational database operations more standardized. Data warehousing and data mining developed on this foundation: a data warehouse organizes large historical data for analysis, while data mining searches that data for useful patterns.

These notes follow the introductory treatment in Han, Kamber, and Pei and the data-object and measurement treatment in Tan, Steinbach, and Kumar. The main exam emphasis should be the change from isolated files to managed, integrated, and queryable databases.

## Explanation

### 1. From records and punched cards to electronic files

The earliest business records were written on paper or encoded on punched cards. Machines could read these records and perform simple calculations, but storage capacity was limited and the same information could be recorded in several incompatible formats.

Electronic file systems improved processing speed, but each application usually created its own files. For example, a college might have one file for student registration, another for attendance, and another for marks. Each file could contain fields such as student name, roll number, and course, but copies could differ.

A file-based system has several weaknesses:

- **Redundancy:** the same fact is stored repeatedly.
- **Inconsistency:** one copy is updated while another is not.
- **Update anomaly:** a change must be made in many places.
- **Program-data dependence:** an application is closely tied to the layout of its files.
- **Limited sharing:** different departments may define and store the same entity differently.
- **Weak concurrency control:** two users can update the same record in conflicting ways.
- **Poor integrity control:** file formats and valid values are not centrally enforced.

Suppose a student's phone number appears in the registration file, hostel file, and library file. A correction to the library file does not automatically correct the other files. The organization now has conflicting information.

### 2. Why the DBMS was introduced

A DBMS is software that controls a database. It separates the management of data from the business logic of individual applications. An application requests data through the DBMS; the DBMS locates, retrieves, updates, protects, and controls concurrency.

A conventional DBMS has important elements:

1. **Hardware:** storage, processors, memory, and input/output devices.
2. **Software:** the DBMS, operating system, and application programs.
3. **Data:** stored records, metadata, and constraints.
4. **Procedures:** rules for operating, backup, recovery, and administration.
5. **Users:** database administrators, application developers, analysts, and ordinary users.

The main functions of a DBMS are:

- define schemas using data-definition facilities;
- store and retrieve records using a data-manipulation language;
- control transactions and concurrency;
- enforce integrity constraints;
- authorize access and provide recovery;
- maintain a data dictionary or metadata repository;
- provide backup, logging, and recovery facilities.

The key change is not merely faster storage. It is **centralized control and reduced dependence on individual programs**.

### 3. Data models and major DBMS generations

A data model describes the structure of data and the relationships among data objects. The main historical stages are:

- **Hierarchical DBMS:** records are arranged as a tree. It suits many-to-one structures but can make unrelated queries difficult.
- **Network DBMS:** records form a graph with explicit links. It is more flexible than the hierarchical model, but navigation and maintenance are complex.
- **Relational DBMS:** data is represented by tables of rows and columns. Tables are related through keys, and SQL is used to query and update them.
- **Object and object-relational DBMS:** support complex objects, media, or object-oriented concepts while retaining relational facilities where useful.

The relational model organizes data by attributes in tuples. A relation is conceptually a set of tuples having the same attributes. For example:

```text
STUDENT(RollNo, Name, Branch, Programme)
COURSE(CourseID, CourseName, Credits)
ENROLLMENT(RollNo, CourseID, Marks)
```

`STUDENT` contains student records. `ENROLLMENT` connects a student to a course and stores the mark. Foreign keys preserve valid links between the tables.

Normalization decomposes relations to reduce redundancy. A simple functional dependency is written as

\[
X \rightarrow Y
\]

meaning that knowledge of all values in attribute set \(X\) determines the values in \(Y\). For example,

\[
\text{RollNo} \rightarrow \text{Name, Branch}
\]

If a student's branch can change, keeping it only in the student table avoids multiple update anomalies. The trade-off is that valid queries may need joins.

### 4. DBMS properties: data independence, consistency, integrity, and security

**Physical data independence** means that the internal storage layout can be changed without changing the conceptual schema or application programs. For example, a table can be moved from an old disk file to a partitioned table without changing the SQL query that reads student names.

**Logical data independence** means that the conceptual schema can change without requiring changes to application programs and external views. For example, two separate `PHONE` attributes could be replaced conceptually by a `CONTACT` entity with related contact records.

Other important properties are:

- **Integrity:** correct and valid data is maintained through constraints.
- **Consistency:** a fact has one agreed meaning and representation.
- **Security:** only authorized operations are allowed.
- **Concurrency control:** concurrent transactions produce valid results.
- **Recovery:** the database returns to a correct state after failure.
- **Authorization:** privileges control read and write actions.
- **Metadata:** the DBMS stores descriptions of schemas, relationships, constraints, and permissions.

Transactions normally obey ACID properties:

- **Atomicity:** all transaction operations occur or none do.
- **Consistency:** the transaction moves the database from one valid state to another valid state.
- **Isolation:** concurrent transactions behave as if properly separated, subject to the chosen isolation level.
- **Durability:** a committed transaction survives later failure.

### 5. The role of SQL and database processing

SQL, or Structured Query Language, provides declarative operations for data definition, retrieval, insertion, update, deletion, and access control. A query states **what** result is required; the DBMS determines an efficient plan for obtaining it.

A college may need all students whose marks exceed a threshold:

```sql
SELECT RollNo, Name
FROM Student, Enrollment
WHERE Student.RollNo = Enrollment.RollNo
  AND Enrollment.Marks >= 80;
```

The DBMS must retrieve the required rows, verify relationships, and return the requested columns. The application does not need to know whether the data is stored in an index, a partition, or a particular file arrangement.

### 6. From DBMS to data warehousing and data mining

An operational DBMS is tuned for transactions such as recording an order, registering a student, or updating a bank balance. A data warehouse is organized for analysis over many related subjects and historical time periods. It normally stores large volumes of detailed data in a consistent, time-variant form.

Data mining then applies statistical, database, visualization, and machine-learning techniques to discover patterns. The progression can be summarized as:

```text
paper records
  -> application-specific electronic files
  -> managed databases and SQL
  -> integrated, time-oriented data warehouses
  -> analytical processing and pattern discovery
```

This progression also expands the purpose of data: from merely recording a fact to using collections of facts for evidence, prediction, and decision support.

### 7. Why the DBMS matters for data mining

A modern data-mining system depends heavily on database infrastructure:

- large datasets must be stored and accessed efficiently;
- analytical queries and index structures reduce repeated computation;
- transaction logs and snapshots support reproducibility;
- integrity and quality constraints protect analytical inputs;
- query optimization makes interactive exploration practical;
- distributed storage and parallel processing support large-scale mining.

A mining model can be built from a data-warehouse table, but preprocessing and evaluation must also preserve the data meaning. A fast query is not automatically valid analysis. The database must support both technical efficiency and trustworthy interpretation.

## Worked examples

### Example 1: File storage versus DBMS storage

A college stores student details in two independent files.

**File 1**

```text
1, Asha, CSE, 22
2, Bilal, ECE, 21
```

**File 2**

```text
1, Asha, 9876543210
2, Bilal, 9812345678
```

A correction changes the first student's phone number. Under file-based processing, the administrator must locate and update every copy. A missing update produces conflicting records.

In a DBMS, the design can be:

```text
STUDENT(RollNo PK, Name, Branch, Age, Phone)
```

One update changes the single stored phone value:

```sql
UPDATE STUDENT
SET Phone = '9876500000'
WHERE RollNo = 1;
```

This reduces redundancy and makes the corrected value available consistently to all applications.

### Example 2: Relating three tables

A marks report requires students, courses, and enrollments.

```text
STUDENT
RollNo | Name
1      | Asha
2      | Bilal

COURSE
CourseID | CourseName
C101     | DBMS
C102     | Data Mining

ENROLLMENT
RollNo | CourseID | Marks
1      | C101     | 86
1      | C102     | 78
2      | C101     | 74
```

A join condition is necessary because no single table contains the complete report:

```sql
SELECT s.Name, c.CourseName, e.Marks
FROM STUDENT AS s
JOIN ENROLLMENT AS e ON s.RollNo = e.RollNo
JOIN COURSE AS c ON e.CourseID = c.CourseID
WHERE e.Marks >= 80;
```

The result is:

```text
Asha | DBMS | 86
```

The foreign key `ENROLLMENT.RollNo` references `STUDENT.RollNo`, while `ENROLLMENT.CourseID` references `COURSE.CourseID`. This structure avoids storing a student's name repeatedly in every enrollment record.

### Example 3: Physical data independence

Suppose attendance data is first stored in three small files, then reorganized into one monthly partitioned table.

Before:

```text
attendance_jan.txt
attendance_feb.txt
attendance_mar.txt
```

After:

```text
ATTENDANCE(RollNo, Date, Present)
PARTITION BY Month(Date)
```

The application still issues the same logical query:

```sql
SELECT RollNo, COUNT(*)
FROM ATTENDANCE
WHERE Present = TRUE
GROUP BY RollNo;
```

The internal physical organization has changed, but the application query and conceptual records do not. This demonstrates physical data independence.

### Example 4: A transaction and ACID

A bank transfer has two operations:

1. deduct ₹5,000 from account A;
2. credit ₹5,000 to account B.

If the database crashes after operation 1, a system without atomicity could lose ₹5,000. The DBMS uses a transaction and a log. If the crash prevents a commit, the incomplete transaction is rolled back. If both operations are committed, durability ensures that they remain recorded after a later failure.

## Key terms & formulas

- **Information technology (IT):** the use of computing, communication, storage, and software to collect, process, store, and distribute information.
- **Data object or record:** a representation of one real-world case, such as one student, sale, or transaction.
- **Attribute or field:** a property measured for a data object.
- **Schema:** the structural description of a database, including relations, attributes, types, and constraints.
- **Metadata:** data about data, such as definitions, formats, ownership, and relationships.
- **DBMS:** software that manages databases and controls access, consistency, transactions, and recovery.
- **File system:** stores and retrieves files, but normally lacks centralized database-wide constraints and semantic structure.
- **Data redundancy:** repeated storage of the same fact.
- **Update anomaly:** unnecessary repetition of a fact causes inconsistent or difficult updates.
- **Data independence:** separation of logical data description from physical storage so that one can change with less effect on the other.
- **Normalization:** decomposition of relations to reduce redundancy and update anomalies.
- **Functional dependency:** \(X \rightarrow Y\), meaning that \(X\) functionally determines \(Y\).
- **SQL:** a declarative language for defining, accessing, and controlling relational databases.
- **Transaction:** a logical unit of work whose operations succeed or fail as one.
- **ACID:** Atomicity, Consistency, Isolation, and Durability.
- **Concurrency control:** coordination of simultaneous user operations to prevent conflicts.
- **Recovery:** restoration of the database to a consistent state after failure.
- **Redundancy reduction:** removing unnecessary repeated facts, often through normalization.

No single numerical formula defines a DBMS. The central logical test is whether a design reduces repeated data, preserves valid relationships, and permits correct, safe, and independent updates.

## Common mistakes

1. **Calling a DBMS only a database.** A database is the organized collection; a DBMS is the software that manages it.
2. **Assuming every file is a database.** A collection of files does not automatically provide shared schemas, integrity constraints, transactions, or security.
3. **Confusing physical and logical data independence.** Physical independence allows internal storage changes; logical independence permits conceptual-schema changes with less effect on applications.
4. **Ignoring metadata.** A reliable database also stores definitions, data types, constraints, lineage, and ownership.
5. **Treating normalization as the only concern.** Decomposition must preserve correct relationships and support required queries.
6. **Confusing SQL with a query result.** SQL is the language; the result is the table returned after execution.
7. **Believing ACID is optional in serious systems.** Financial and record-update operations commonly depend on transactional guarantees.
8. **Equating a DBMS with data mining.** A DBMS primarily stores and processes data; mining analyzes data to discover patterns and support decisions.

## Exam prep

### Likely 2-mark questions

1. **What is a DBMS?**  
   *Hint:* Define it as software that stores, retrieves, updates, and controls databases while enforcing integrity, security, transactions, and recovery.

2. **Give two weaknesses of file-based systems.**  
   *Hint:* Mention redundancy and inconsistency, followed by their effect on updates and sharing.

3. **What is data redundancy?**  
   *Hint:* The unnecessary repetition of the same fact in multiple places.

4. **Define physical data independence.**  
   *Hint:* The ability to change physical storage without changing the conceptual schema or application programs.

5. **Expand ACID.**  
   *Hint:* Atomicity, consistency, isolation, and durability.

6. **Differentiate a database from a DBMS.**  
   *Hint:* Database = organized data; DBMS = software that manages and controls that data.

7. **Why is SQL useful?**  
   *Hint:* It supplies a standard declarative way to define, query, update, and control relational data.

8. **What is metadata?**  
   *Hint:* Descriptive information about data, schemas, types, constraints, sources, and usage.

### Likely long-answer questions

1. **Trace the evolution from paper/file-based IT to database systems and data mining.**  
   *Answer hint:* Begin with manual and punched-card records, then electronic application-specific files, their limitations, centralized DBMS services, SQL and relational modeling, data warehouses, and finally data mining. Include the change in purpose from recording transactions to discovering patterns.

2. **Explain the functions of a DBMS with an example.**  
   *Answer hint:* Cover storage, retrieval, schema definition, integrity, concurrency, security, recovery, metadata, and backup. Use a bank transfer or student record to connect each function to ACID and controlled updates.

3. **Discuss data independence and normalization.**  
   *Answer hint:* Distinguish physical from logical independence, show how a physical table can be reorganized, explain functional dependencies and update anomalies, and discuss the benefit and query trade-off of decomposition.

4. **Compare a file-based system, an operational DBMS, a data warehouse, and data mining.**  
   *Answer hint:* Compare purpose, data orientation, time horizon, integration, schema control, and analytical behavior. End by showing that they are complementary rather than interchangeable.

5. **Explain how database technology supports large-scale data mining.**  
   *Answer hint:* Mention efficient storage, indexing and query optimization, integrity, snapshots and reproducibility, distributed execution, parallel processing, and the need to preserve correct semantics.
