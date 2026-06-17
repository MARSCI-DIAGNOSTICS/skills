---
description: Use this skill as a base profile for systems programming courses in C, C++, Rust, or Zig. Provides core concepts for memory management, performance awareness, safety considerations, and low-level understanding. Language-specific profiles inherit from this. Trigger when user mentions "systems programming", "low-level programming", or "performance-critical development".
---

# Systems Programming - Base Course Profile

**Category:** Low-level programming, memory management, performance-critical development
**Applicable Languages:** C, C++, Rust, Zig

## Overview

This is a base profile for systems programming courses. Language-specific profiles (like C++ Fundamentals) inherit from this and customize for their specific language and audience.

## Core Concepts (All Systems Languages)

### Memory Management
- Stack vs heap allocation
- Object lifetime and ownership
- Memory layout and alignment
- Manual vs automatic memory management

### Performance Awareness
- Understanding what code compiles to
- Cache-friendly data structures
- Avoiding unnecessary copies
- Profiling and optimization

### Safety Considerations
- Buffer overflows and bounds checking
- Use-after-free and dangling references
- Data races and thread safety
- Undefined behavior awareness

### Low-Level Understanding
- How the CPU executes code
- System calls and OS interaction
- File I/O at the system level
- Network programming basics

## Pedagogical Approach

### Visualization is Critical
Systems programming deals with invisible concepts. Make them visible:
- Memory layout diagrams for every pointer topic
- Stack frame illustrations
- Heap allocation visualizations
- Data structure memory representations

### Compile-Time vs Runtime
Help students distinguish:
- What the compiler does vs what happens at runtime
- Static vs dynamic properties
- Compile-time errors vs runtime errors

### Error-Driven Learning
Compiler errors and crashes are learning tools:
- Show what broken code looks like
- Teach students to read error messages
- Build pattern recognition for common issues

## Framework-Free Teaching

Systems programming courses should typically:
- Focus on standard library only
- Build fundamental understanding first
- Avoid abstractions that hide important details
- Let students feel the "weight" of manual management

## Lab Structure

### Environment Requirements
- Must compile and run locally (not just online)
- Debugger access is essential
- Students need to see memory state

### Challenge Design
- Start with working code to modify
- Include "break this code" exercises
- Require debugging exercises
- Test with edge cases and invalid input

## Assessment Considerations

### Compilation is Non-Negotiable
- Code that doesn't compile fails
- Partial credit for compiling code with bugs
- Full error messages must be understood

### Memory Safety Checks
- Use sanitizers (ASan, MSan, UBSan) in testing
- Valgrind for memory leak detection
- Points deducted for memory errors

### Performance Requirements (When Applicable)
- Specify complexity requirements
- Test with large inputs
- Compare against reference implementation

## Sandbox Configuration

Systems programming courses require robust sandbox environments with full debugging and memory analysis tooling.

### Required Container Capabilities

All systems programming sandboxes must include:

| Category | Tools | Purpose |
|----------|-------|---------|
| Compilers | GCC 13+, Clang 17+ | Compilation with latest standards |
| Debuggers | GDB, LLDB | Interactive debugging |
| Memory Analysis | Valgrind, ASan, MSan, UBSan | Memory error detection |
| Thread Analysis | ThreadSanitizer, Helgrind | Race condition detection |
| Static Analysis | clang-tidy, cppcheck | Code quality checks |
| Profiling | perf, flamegraph | Performance analysis |

### Sandbox Commands

```bash
# Initialize sandbox
/setup-sandbox {course-id}

# Compile and run with full warnings
/run-code source.cpp

# Run with memory sanitizers
/debug-code source.cpp sanitize

# Memory leak check
docker exec course-sandbox-{course-id} \
  valgrind --leak-check=full --show-leak-kinds=all /tmp/prog

# Thread safety check
docker exec course-sandbox-{course-id} \
  g++ -std=c++20 -fsanitize=thread -g -o /tmp/prog source.cpp && /tmp/prog

# Performance profiling
docker exec course-sandbox-{course-id} \
  perf record /tmp/prog && perf report
```

### Validation Requirements

Before publishing content:

1. **All code must compile** - Zero tolerance for compile errors
2. **All code must pass sanitizers** - ASan, UBSan, and TSan (for threaded code)
3. **Memory must be clean** - Valgrind should report no leaks for completed examples
4. **Error examples must fail** - Verify intentional errors produce expected failures

### Security Constraints

Systems programming sandboxes need special security consideration:

```bash
docker run -d \
  --name course-sandbox-{course-id} \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --security-opt=seccomp=default \
  --memory=2g \
  --cpus=2 \
  --network=none \
  --read-only \
  --tmpfs /tmp:size=512m \
  course-sandbox-{course-id}:latest
```

Key restrictions:
- **No network access** - Prevents exfiltration
- **Read-only filesystem** - Prevents persistent changes
- **Dropped capabilities** - Minimal privileges
- **Resource limits** - Prevents resource exhaustion
- **Seccomp filtering** - Restricts system calls
