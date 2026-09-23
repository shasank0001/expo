---
subject: atcd
unit: 1
topic: compilers-and-language-processors
syllabus_ref: CSM3203 Unit-I
status: draft
---
# Compilers and Language Processors
## Overview
A language processor is any program that reads, transforms, checks, or executes text written in a language. A compiler is a language processor that translates a source program into another program, often intermediate code or machine code. The distinction matters because a compiler translates ahead of time, an interpreter executes while translating, and tools such as assemblers, linkers, and loaders process different layers of a software system.

## Explanation
### Compiler as a translator
A compiler takes a source program `P`, analyzes it, and produces a target program `T` such that executing `T` has the same intended meaning as executing `P`. The target may be assembly, object code, bytecode, or another high-level language. Translation can be one pass or several passes. A compiler may also report errors and create tables used by later stages.

### Interpreter
An interpreter reads a representation of the program and performs the source-language actions directly, usually statement by statement or expression by expression. It generally does not need to produce a complete separate target program. A compiler/interpreter hybrid, such as a Java implementation, may compile source into bytecode and then execute that bytecode with a virtual machine.

### Language processors in the execution path
A practical tool chain can contain:

1. **Editor or preprocessor:** handles text and source-level directives.
2. **Compiler/translator:** produces an intermediate or target program.
3. **Assembler:** converts assembly mnemonics into machine instructions.
4. **Linker:** combines object files and resolves external symbols.
5. **Loader:** places the executable in memory and prepares it for execution.
6. **Interpreter/JIT:** executes an intermediate representation, sometimes compiling hot code just in time.

A compiler does not necessarily perform loading, linking, or execution. Those are separate language-processing activities.

### Source, intermediate, and target languages
A source language is the notation used by the programmer. An intermediate language is a compiler-created representation that is convenient for analysis and optimization. A target language is the notation expected by a processor or virtual machine. One source front end can feed many target back ends. The same intermediate language can also make a compiler portable.

### Compiler versus interpreter
The main distinction is when translation happens and whether a separate target program is normally produced. Compilation usually offers faster repeated execution because translation is done ahead of time. Interpretation is convenient for teaching, scripting, debugging, and dynamic environments, but may spend time translating repeatedly. The distinction is not absolute: a compiler can emit code interpreted by a VM, and an interpreter can use a JIT compiler.

### Bootstrapping and portability
A compiler written in the language it compiles is self-hosting. A bootstrapping sequence often uses an earlier compiler, written in another language, to compile a new compiler written in the target language; that new compiler then compiles itself. Portability is achieved by keeping the front end and intermediate representation stable while replacing the back end.

### Language processors versus editors and search tools
A formatter, spell checker, and syntax highlighter are language-aware tools but are not necessarily compilers because they do not translate a complete program into an executable equivalent. The phrase “language processor” is broad; a compiler is its important translating case.

## Worked examples
### Example 1: Java execution
A Java compiler usually produces platform-neutral bytecode. The Java Virtual Machine loads and executes the bytecode, using a JIT compiler to turn frequently used bytecode methods into native instructions. Both compilation and interpretation appear in one implementation.

### Example 2: C program
A C compiler translates source to assembly or object code. The assembler translates assembly to object instructions, the linker combines objects and libraries, and the loader prepares the executable. No single one of these tools is the whole compiler.

### Example 3: scripting
A Python script may be parsed to an internal syntax tree and interpreted by the Python runtime. It is still language processing even though it does not produce a standalone `.exe` file.

## Key terms & formulas
- Compiler: `source + input → target program + diagnostics`.
- Interpreter: `source representation → execution of actions`.
- Source language → IR → target language is a common pipeline.
- Ahead-of-time (AOT), interpreter, and just-in-time (JIT) are implementation strategies, not strict language categories.

## Common mistakes
- A compiler does not always produce machine code; intermediate code is a valid target.
- An interpreter is not merely a slower compiler; it executes a representation according to language rules.
- Linker and loader are not synonyms for compiler.
- A language processor may perform only analysis or transformation, not execution.

## Exam prep
**Likely 2-mark questions**
1. Define compiler and language processor. **Hint:** translation versus any language-aware processing.
2. State two differences between compiler and interpreter. **Hint:** timing and target-program production.
3. What is an assembler and linker? **Hint:** instruction conversion and object combination.

**Long-answer questions**
1. Explain compiler, interpreter, assembler, linker, and loader with a tool-chain diagram. **Hint:** follow a source file to execution.
2. Describe AOT, interpretation, and JIT using one example each. **Hint:** Java, scripting, and a VM compiler.
3. Explain bootstrapping and why it is useful. **Hint:** earlier compiler compiles a self-hosting compiler.
4. Why is an intermediate language helpful for portability? **Hint:** replace only the target back end.
