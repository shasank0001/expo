---
subject: atcd
unit: 5
topic: machine-dependent-optimization
syllabus_ref: CSM3203 Unit-V
status: draft
---
# Machine-Dependent Optimization
## Overview
Machine-dependent optimization uses the instruction set, registers, address modes, timing, and pipeline behavior of a particular processor to improve target code. It selects efficient instructions, reduces copies and memory traffic, schedules operations, and rewrites short instruction patterns. Unlike machine-independent optimization, it may produce a different result for each architecture, but every rewrite must preserve the target language’s observable behavior.

## Explanation
### Target information
A backend may use instruction latency and throughput, available registers, load/store cost, branch prediction behavior, alignment rules, calling conventions, and memory hierarchy. A shorter instruction is not always faster; an instruction that stalls on memory may be worse than several cheap arithmetic operations. Target information also includes legal operand sizes and restrictions on flag use.

### Peephole optimization
A peephole optimizer scans a short sliding window of target instructions. For each window, it looks for a pattern that can be replaced by an equivalent shorter, faster, or safer sequence. The window moves forward after a rewrite. It is local, inexpensive, and easy to add after instruction selection.

Typical peephole rules include:

- remove a move whose source is already in the destination;
- replace `add r, #0` with a no-op when flags are dead;
- remove a redundant load followed immediately by a use of the loaded register;
- combine adjacent shifts or arithmetic operations when legal;
- replace a long immediate load with a shorter target form;
- remove a jump to the immediately following instruction.

Every rule must account for flags, exceptions, memory aliasing, and branch semantics.

### Register allocation
Register allocation assigns frequently used values to registers, minimizing loads and stores. A simple graph-coloring allocator models interference between simultaneously live values; a more advanced allocator uses live ranges and spilling. A spilled value is stored temporarily in memory. A register may be reserved for a target convention or special instruction.

### Instruction selection
The code generator chooses among target instructions that implement the same IR operation. A multiply-add, conditional move, indexed load, or compare-and-branch may be available on one processor and not another. Selection must consider operand types, overflow, alignment, and the cost of computing an address.

### Instruction scheduling
Independent instructions can be reordered to hide latency or avoid pipeline stalls. A dependent instruction cannot generally move across the instruction that produces its operand. Scheduling can reduce branch hazards and improve instruction-level parallelism, but it must preserve exceptions, memory order, and volatile accesses.

### Instruction encoding and layout
Target-specific choices include choosing shorter encodings, aligning branches or data, selecting a range for a displacement, and arranging frequently executed code. A target assembler may perform some of these tasks, but the compiler must provide enough information and obey restrictions.

### Relation to machine-independent code
The intermediate code is usually optimized first with general transformations. Target-dependent optimization then lowers or annotates the result with register, instruction, and control-flow costs. Some transformations cross the boundary, such as replacing a high-level loop with a target decrement-and-branch instruction.

### Correctness
Target optimization must preserve language-visible values, control flow, exceptions, volatile memory behavior, and calling conventions. Hardware flags are often part of the target contract, so an apparently redundant arithmetic instruction may be observable. Testing should include boundary and aliasing cases and compare against an unoptimized reference.

## Worked examples
### Example 1: redundant move
If the target contract says flags are dead and the source is still live:

```
MOV r1, r0
MOV r2, r1
```

can become `MOV r2, r0`, or be removed if `r2` already contains `r0`. If the first move changes a condition flag used later, it is not redundant.

### Example 2: load/use
```
LOAD r1, [x]
ADD r1, r0
```

can use a memory-add instruction on a target that has one. On a target without it, the sequence may be retained; this is target dependence, not a language transformation.

### Example 3: branch scheduling
If `t=a*b` and `u=c+d` are independent, a scheduler can issue them in either order to fill pipeline slots. It cannot move a load after a store to an aliasing address unless memory ordering permits it.

### Example 4: immediate encoding
If an address fits in a short displacement, a target may use a compact load instruction instead of loading the address into a register first. The general IR is unchanged; only the backend representation differs.

## Key terms & formulas
- Peephole window: `k` adjacent target instructions.
- Register allocation: assign live values to a finite register set; spill if impossible.
- Instruction scheduling: reorder independent operations for latency/throughput.
- Target cost model: estimated time/size of an instruction sequence.
- Valid rewrite: preserves observable behavior for the target contract.

## Common mistakes
- Fewer instructions is not always faster.
- Removing arithmetic can remove flags or an exception.
- A register copy may be needed because a calling convention or interrupt can observe it.
- Scheduling cannot reorder dependent or volatile memory operations freely.
- Target optimization should not change the source language’s defined precision or overflow behavior.

## Exam prep
**Likely 2-mark questions**
1. Define machine-dependent optimization. **Hint:** target-specific improvement.
2. What is peephole optimization? **Hint:** short sliding window.
3. Name two target facts used. **Hint:** registers, instructions, timing, modes.
4. What is register spilling? **Hint:** store a value temporarily in memory.

**Long-answer questions**
1. Explain peephole optimization with three rules. **Hint:** pattern, replacement, safety checks.
2. Describe register allocation and its trade-offs. **Hint:** interference, live ranges, spills.
3. Explain instruction scheduling and pipeline hazards. **Hint:** independence and dependencies.
4. Compare machine-dependent and machine-independent optimization. **Hint:** target facts versus general IR.
5. Show a target rewrite and list the facts that must be verified. **Hint:** flags, aliasing, exceptions, calling convention.

**Exam habit**
Write the target contract beside every proposed peephole rule. This prevents accepting a transformation that is only valid for an idealized instruction set.
