---
description: Use this skill when creating content for the C++ Fundamentals course. Provides course-specific context including target audience (junior developers), technical stack (GCC/Clang, CMake), modern C++ focus (C++17/20), and content style guidelines. Trigger when user mentions "C++ course", "C++ fundamentals", "cpp-fundamentals", or "C++ for junior developers".
---

# C++ Fundamentals - Course Profile

**Course:** C++ Fundamentals for Junior Developers
**Level:** Beginner to Intermediate
**Duration:** 12-16 weeks

## Course Overview

A comprehensive introduction to C++ for junior developers who want to deepen their understanding of low-level programming, memory management, and systems-level thinking. This course builds a strong foundation in C++ without relying on frameworks, focusing on the language itself and the standard library.

## Target Audience

**Primary:** Junior developers (1-2 years experience) looking to:
- Understand how programming works "under the hood"
- Learn a systems programming language
- Prepare for performance-critical development
- Build foundations for game development, embedded systems, or systems programming

**Prerequisites:**
- Basic programming experience in any language
- Understanding of variables, functions, loops, conditionals
- Familiarity with using a terminal/command line
- Basic understanding of what compilation means

**Not assumed:**
- Prior C or C++ experience
- Deep understanding of memory management
- Experience with pointers or manual memory management
- Knowledge of object-oriented programming in C++

## Learning Philosophy

### Core Principles

1. **Build Understanding from the Ground Up**
   - Start with what the computer actually does
   - Show how high-level concepts map to low-level operations
   - Make memory and execution visible through diagrams

2. **Modern C++ First**
   - Teach C++17/20 idioms from the start
   - Introduce smart pointers before raw pointers
   - Use standard library containers before arrays
   - Then show the "old way" to understand legacy code

3. **Compile-Run-Debug Cycle**
   - Every concept demonstrated with compilable code
   - Compiler errors are learning opportunities
   - Debugging is taught explicitly, not assumed

4. **No Framework Dependency**
   - Standard library only (no Boost, Qt, etc.)
   - Focus on language fundamentals
   - Students understand what they're using

5. **Professional Practices Throughout**
   - Version control from day one
   - Testing introduced early
   - Code organization and documentation

## Technical Stack

### Required Tools
- **Compiler:** GCC 11+ or Clang 14+ (support C++20)
- **Build System:** CMake 3.20+
- **Editor/IDE:** VS Code with C/C++ extension (recommended) or CLion
- **Debugger:** GDB or LLDB
- **Version Control:** Git

### Development Environment
- Primary: Local development on Linux, macOS, or WSL2
- Alternative: Compiler Explorer (godbolt.org) for quick experiments
- Testing: Google Test or Catch2 for unit testing

### Standard Library Focus
- `<iostream>` - I/O operations
- `<string>` - String handling
- `<vector>`, `<array>` - Containers
- `<memory>` - Smart pointers
- `<algorithm>` - Standard algorithms
- `<filesystem>` - File operations (C++17)
- `<optional>`, `<variant>` - Modern type handling

## Content Style

### Writing Tone
- Technical but approachable
- Direct and clear explanations
- Acknowledge when things are complex
- Compare to languages students might know (Python, JavaScript)
- Avoid unnecessary jargon, but introduce proper terminology

### Code Examples
- Always complete and compilable
- Include `#include` statements
- Show compilation commands
- Display actual output
- Use consistent formatting (clang-format style)

### Example Code Block Format
```cpp
// filename: example.cpp
// Compile: g++ -std=c++20 -Wall -o example example.cpp
// Run: ./example

#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers{1, 2, 3, 4, 5};

    for (const auto& n : numbers) {
        std::cout << n << " ";
    }
    std::cout << "\n";

    return 0;
}
```

**Output:**
```
1 2 3 4 5
```

### Diagrams and Visualizations
- Memory layout diagrams for every pointer/reference topic
- Stack vs heap visualizations
- Object lifetime diagrams
- Call stack illustrations during recursion
- Use ASCII art or simple diagrams that work in markdown

### Error Examples
Always show common errors with full compiler output:
```cpp
// Common mistake: using uninitialized variable
int x;
std::cout << x;  // Undefined behavior!
```

**Compiler warning (with -Wall):**
```
warning: 'x' is used uninitialized [-Wuninitialized]
```

## Course Structure

### Module 1: Getting Started
- Development environment setup
- Hello World and compilation process
- Basic I/O with iostream
- Variables and fundamental types
- **Lab:** Build and run your first C++ programs

### Module 2: Control Flow and Functions
- Conditionals (if, switch)
- Loops (for, while, range-based for)
- Functions: declaration, definition, overloading
- Pass by value vs reference
- **Lab:** Functions and control flow exercises

### Module 3: Memory Model Fundamentals
- Stack vs heap (conceptual)
- Object lifetime and scope
- References vs pointers (introduction)
- Why memory management matters
- **Lab:** Exploring scope and lifetime

### Module 4: Classes and Objects
- Defining classes
- Constructors and destructors
- Member functions and data
- Access specifiers (public, private)
- The `this` pointer
- **Lab:** Building your first class

### Module 5: Standard Library Containers
- `std::vector` in depth
- `std::array` vs C arrays
- `std::string` operations
- Iterators basics
- **Lab:** Working with containers

### Module 6: Modern Memory Management
- Smart pointers: `unique_ptr`, `shared_ptr`
- RAII principle
- When to use which smart pointer
- Raw pointers: when and why
- **Lab:** Memory management patterns

### Module 7: Deeper into Pointers
- Pointer arithmetic
- Arrays and pointers relationship
- C-style strings (for legacy code)
- Common pointer pitfalls
- **Lab:** Pointer exercises and debugging

### Module 8: Object-Oriented Programming
- Inheritance and polymorphism
- Virtual functions
- Abstract classes and interfaces
- Composition vs inheritance
- **Lab:** OOP design exercise

### Module 9: Templates Basics
- Function templates
- Class templates
- Template argument deduction
- Standard library algorithm templates
- **Lab:** Generic programming exercises

### Module 10: Error Handling
- Exceptions: try, catch, throw
- Exception safety guarantees
- `std::optional` for nullable types
- `std::expected` (C++23) / error handling patterns
- **Lab:** Robust error handling

### Module 11: Modern C++ Features
- Auto and type deduction
- Lambda expressions
- Move semantics (introduction)
- Structured bindings
- **Lab:** Modernizing legacy code

### Module 12: Building Larger Programs
- Header files and compilation units
- Namespaces
- CMake project structure
- Unit testing with Catch2
- **Project:** Capstone project

## Lab Structure

**Duration:** 90 minutes
**Format:** Individual or pair programming

### Part A: Guided Practice (35-40 minutes)
- TA walks through key concepts
- Students follow along and run code
- Immediate feedback on understanding
- Building up to a working example

### Part B: Independent Challenges (40-45 minutes)
- 4-6 progressive challenges
- Students work independently or in pairs
- Challenges build on Part A concepts
- Extension challenges for fast finishers

### Part C: Wrap-up (10 minutes)
- Review key concepts
- Address common issues encountered
- Preview next session

## Assessment Philosophy

### Code Must Compile
- Non-compiling code receives minimal credit
- Partial credit for code that compiles but has bugs
- Students must test locally before submission

### Testing Required
- Submissions should include basic tests
- Demonstrates understanding of expected behavior
- Teaches professional practice

### Code Review Component
- Readability and style matter
- Proper use of modern C++ features
- Memory safety considerations

## Quality Standards

**Before finalizing any content:**
- [ ] All code compiles with `-std=c++20 -Wall -Wextra -Werror`
- [ ] Output shown matches actual program output
- [ ] Memory diagrams are accurate
- [ ] Error examples show real compiler messages
- [ ] Exercises are solvable with taught concepts only
- [ ] Modern C++ idioms used appropriately
- [ ] Code follows consistent formatting
- [ ] Code validated in sandbox with sanitizers

## Sandbox Configuration

**Container Name:** `course-sandbox-cpp-fundamentals`
**Template:** C++ Sandbox (Ubuntu 24.04)

### Docker Setup

```bash
# Build sandbox image
docker build -t course-sandbox-cpp-fundamentals:latest -f .sandbox/Dockerfile .

# Create and start container
docker run -d \
  --name course-sandbox-cpp-fundamentals \
  -v "$(pwd):/workspace" \
  -w /workspace \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --memory=2g \
  --cpus=2 \
  --network=none \
  course-sandbox-cpp-fundamentals:latest \
  tail -f /dev/null
```

### Installed Tools

| Tool | Version | Purpose |
|------|---------|---------|
| GCC | 13+ | Primary compiler |
| Clang | 17+ | Alternative compiler |
| CMake | 3.20+ | Build system |
| GDB | Latest | Debugger |
| LLDB | 17 | Alternative debugger |
| Valgrind | Latest | Memory checking |
| clang-tidy | 17 | Static analysis |
| clang-format | 17 | Code formatting |
| cppcheck | Latest | Additional analysis |
| Google Test | Latest | Unit testing |
| Catch2 | Latest | Alternative testing |

### Quick Commands

```bash
# Compile single file
docker exec course-sandbox-cpp-fundamentals \
  g++ -std=c++20 -Wall -Wextra -o /tmp/prog /workspace/example.cpp

# Run program
docker exec course-sandbox-cpp-fundamentals /tmp/prog

# Compile with sanitizers
docker exec course-sandbox-cpp-fundamentals \
  g++ -std=c++20 -fsanitize=address,undefined -g -o /tmp/prog /workspace/example.cpp

# Run tests
docker exec course-sandbox-cpp-fundamentals \
  bash -c "cd /workspace && cmake -B build && cmake --build build && ctest --test-dir build --output-on-failure"

# Lint code
docker exec course-sandbox-cpp-fundamentals \
  clang-tidy /workspace/example.cpp -- -std=c++20

# Memory check
docker exec course-sandbox-cpp-fundamentals \
  valgrind --leak-check=full /tmp/prog

# Debug session
docker exec -it course-sandbox-cpp-fundamentals gdb /tmp/prog
```

### Validation Workflow

Before publishing any content:

1. **Run validation on all examples:**
   ```bash
   /validate-examples cpp-fundamentals
   ```

2. **Check specific chapter:**
   ```bash
   /validate-examples cpp-fundamentals chapter-05
   ```

3. **Lint all code for style:**
   ```bash
   /lint-code src/
   ```

4. **Run with sanitizers for memory safety:**
   ```bash
   /debug-code example.cpp sanitize
   ```

## Callout Box Types

Use these throughout content:

**Important:** Critical concept or common mistake
```markdown
> **Important:** Always initialize your variables in C++. Unlike some languages,
> C++ does not automatically initialize local variables to zero.
```

**Why This Matters:** Connect to real-world relevance
```markdown
> **Why This Matters:** Understanding the stack vs heap distinction is crucial
> for writing efficient C++ code and avoiding memory leaks.
```

**Coming From [Language]:** Help students transfer knowledge
```markdown
> **Coming From Python:** Unlike Python lists, C++ vectors store elements
> contiguously in memory, which makes random access O(1) but insertions O(n).
```

**Under the Hood:** Deeper technical explanation
```markdown
> **Under the Hood:** When you call a function, the compiler generates code
> that pushes parameters onto the stack, jumps to the function address, and
> sets up a new stack frame.
```
