---
description: Use this skill when executing, testing, linting, debugging, or validating code in course materials. Provides Docker-based isolated sandbox infrastructure for safe code execution. Trigger phrases include "run code", "test code", "lint", "debug", "validate examples", "sandbox", "execute", "compile".
---

# Course Sandbox - Docker-Based Code Execution

Isolated development environment for safely executing, testing, linting, and debugging code examples in course materials. Each course shares a single persistent Docker container as its sandbox.

## Overview

The sandbox system provides:
- **Isolated Execution**: All code runs in Docker containers, protecting the host system
- **Persistent Environment**: One container per course, maintaining state across sessions
- **Language Support**: Pre-configured environments for C++, Rust, Python, Go, and more
- **Full Toolchain**: Compilers, linters, debuggers, and test frameworks pre-installed
- **Volume Mounting**: Course files are mounted for easy access and modification

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Host System                             │
│                                                              │
│  ┌─────────────────┐    ┌─────────────────────────────────┐ │
│  │  Course Files   │    │     Docker Container            │ │
│  │                 │◄──►│  ┌─────────────────────────────┐│ │
│  │ /courses/       │    │  │  /workspace (mounted)       ││ │
│  │   cpp-fund/     │    │  │    - chapters/              ││ │
│  │   rust-intro/   │    │  │    - exercises/             ││ │
│  │                 │    │  │    - projects/              ││ │
│  └─────────────────┘    │  │    - .sandbox/              ││ │
│                         │  └─────────────────────────────┘│ │
│                         │                                  │ │
│                         │  Tools: gcc, clang, gdb, lldb   │ │
│                         │  Linters: clang-tidy, cppcheck  │ │
│                         │  Test: gtest, catch2            │ │
│                         └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Container Lifecycle

### Container Naming Convention
```
course-sandbox-{course-id}
```

Example: `course-sandbox-cpp-fundamentals`

### Container States

1. **Not Created**: No sandbox exists for the course
2. **Stopped**: Sandbox exists but is not running
3. **Running**: Sandbox is active and ready for commands

### Persistence Model

- Containers are created once and reused for the entire course
- Course files are mounted as volumes (changes persist)
- Container state (installed packages, compiled binaries) persists
- Containers can be stopped when not in use to save resources
- Full reset available via container rebuild

## Sandbox Operations

### Check Sandbox Status
```bash
# Check if container exists and its state
docker ps -a --filter "name=course-sandbox-{course-id}" --format "{{.Names}}: {{.Status}}"

# Check if running
docker inspect -f '{{.State.Running}}' course-sandbox-{course-id}
```

### Create Sandbox
```bash
# Build image from course-specific Dockerfile
docker build -t course-sandbox-{course-id}:latest -f .sandbox/Dockerfile .

# Create and start container with mounted workspace
docker run -d \
  --name course-sandbox-{course-id} \
  -v "$(pwd):/workspace" \
  -w /workspace \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --memory=2g \
  --cpus=2 \
  --network=none \
  course-sandbox-{course-id}:latest \
  tail -f /dev/null
```

### Execute Commands in Sandbox
```bash
# Run a command in the sandbox
docker exec course-sandbox-{course-id} <command>

# Run with timeout (prevents infinite loops)
timeout 30s docker exec course-sandbox-{course-id} <command>

# Run interactively (for debugging)
docker exec -it course-sandbox-{course-id} /bin/bash
```

### Stop/Start Sandbox
```bash
# Stop to save resources
docker stop course-sandbox-{course-id}

# Start when needed again
docker start course-sandbox-{course-id}
```

### Reset Sandbox
```bash
# Remove and recreate for clean slate
docker rm -f course-sandbox-{course-id}
# Then run create steps again
```

## Code Execution Patterns

### Compile and Run (C++)
```bash
# Compile
docker exec course-sandbox-cpp-fundamentals \
  g++ -std=c++20 -Wall -Wextra -Werror -o /tmp/prog /workspace/example.cpp

# Run
docker exec course-sandbox-cpp-fundamentals /tmp/prog

# Or combined with timeout
docker exec course-sandbox-cpp-fundamentals \
  bash -c "g++ -std=c++20 -Wall -Wextra -o /tmp/prog /workspace/example.cpp && timeout 10s /tmp/prog"
```

### Compile and Run (Rust)
```bash
# Compile
docker exec course-sandbox-rust-intro \
  rustc -o /tmp/prog /workspace/example.rs

# Run
docker exec course-sandbox-rust-intro /tmp/prog

# Or with cargo
docker exec course-sandbox-rust-intro \
  bash -c "cd /workspace/project && cargo run"
```

### Run Script (Python)
```bash
docker exec course-sandbox-python-basics \
  timeout 10s python3 /workspace/example.py
```

### Run Tests
```bash
# C++ with Google Test
docker exec course-sandbox-cpp-fundamentals \
  bash -c "cd /workspace && cmake -B build && cmake --build build && ctest --test-dir build --output-on-failure"

# Rust with cargo
docker exec course-sandbox-rust-intro \
  bash -c "cd /workspace && cargo test"

# Python with pytest
docker exec course-sandbox-python-basics \
  bash -c "cd /workspace && python -m pytest -v"
```

### Lint Code
```bash
# C++ with clang-tidy
docker exec course-sandbox-cpp-fundamentals \
  clang-tidy /workspace/example.cpp -- -std=c++20

# C++ with cppcheck
docker exec course-sandbox-cpp-fundamentals \
  cppcheck --enable=all --std=c++20 /workspace/example.cpp

# Rust with clippy
docker exec course-sandbox-rust-intro \
  bash -c "cd /workspace && cargo clippy -- -D warnings"

# Python with ruff
docker exec course-sandbox-python-basics \
  ruff check /workspace/example.py
```

### Debug Code
```bash
# Start GDB session (interactive)
docker exec -it course-sandbox-cpp-fundamentals \
  gdb /tmp/prog

# Run with sanitizers (compile with flags)
docker exec course-sandbox-cpp-fundamentals \
  bash -c "g++ -std=c++20 -fsanitize=address,undefined -g -o /tmp/prog /workspace/example.cpp && /tmp/prog"

# Valgrind memory check
docker exec course-sandbox-cpp-fundamentals \
  valgrind --leak-check=full /tmp/prog
```

## Security Constraints

All sandbox containers run with restricted permissions:

| Constraint | Setting | Purpose |
|-----------|---------|---------|
| Capabilities | `--cap-drop=ALL` | Remove all Linux capabilities |
| Privileges | `--security-opt=no-new-privileges` | Prevent privilege escalation |
| Memory | `--memory=2g` | Limit memory usage |
| CPU | `--cpus=2` | Limit CPU usage |
| Network | `--network=none` | Disable network access |
| Read-only | Optional `--read-only` | Prevent filesystem modifications |

## Output Capture

### Capturing Stdout/Stderr
```bash
# Capture output to variable
output=$(docker exec course-sandbox-{course-id} ./prog 2>&1)

# Capture with exit code
docker exec course-sandbox-{course-id} ./prog > output.txt 2>&1
exit_code=$?

# Separate stdout and stderr
docker exec course-sandbox-{course-id} ./prog > stdout.txt 2> stderr.txt
```

### Comparing Expected Output
```bash
# Run and compare
actual=$(docker exec course-sandbox-{course-id} ./prog 2>&1)
expected="Hello, World!"

if [ "$actual" = "$expected" ]; then
  echo "PASS: Output matches"
else
  echo "FAIL: Expected '$expected', got '$actual'"
fi
```

## Timeout Handling

Always use timeouts to prevent infinite loops:

```bash
# Command timeout (10 seconds)
timeout 10s docker exec course-sandbox-{course-id} ./prog

# Check timeout exit code
if [ $? -eq 124 ]; then
  echo "ERROR: Execution timed out (possible infinite loop)"
fi
```

## Temporary Files

Use `/tmp` inside the container for compiled binaries:

```bash
# Compile to /tmp (always writable)
docker exec course-sandbox-{course-id} \
  g++ -o /tmp/example /workspace/example.cpp

# Run from /tmp
docker exec course-sandbox-{course-id} /tmp/example

# Clean up (optional, /tmp clears on container restart)
docker exec course-sandbox-{course-id} rm /tmp/example
```

## Error Handling

### Compilation Errors
```bash
# Capture compiler output
compile_output=$(docker exec course-sandbox-{course-id} \
  g++ -std=c++20 -Wall -Wextra -o /tmp/prog /workspace/example.cpp 2>&1)
compile_status=$?

if [ $compile_status -ne 0 ]; then
  echo "Compilation failed:"
  echo "$compile_output"
fi
```

### Runtime Errors
```bash
# Capture runtime output with exit code
run_output=$(docker exec course-sandbox-{course-id} /tmp/prog 2>&1)
run_status=$?

case $run_status in
  0) echo "Success" ;;
  139) echo "Segmentation fault (signal 11)" ;;
  134) echo "Abort (signal 6)" ;;
  124) echo "Timeout" ;;
  *) echo "Exit code: $run_status" ;;
esac
```

## Batch Validation

For validating all code examples in a course:

```bash
#!/bin/bash
# validate-all-examples.sh

course_id="cpp-fundamentals"
container="course-sandbox-$course_id"

# Find all code files
find /workspace -name "*.cpp" | while read file; do
  echo "Testing: $file"

  # Compile
  if docker exec $container g++ -std=c++20 -Wall -o /tmp/test "$file" 2>&1; then
    echo "  Compile: PASS"

    # Run with timeout
    if timeout 10s docker exec $container /tmp/test > /dev/null 2>&1; then
      echo "  Execute: PASS"
    else
      echo "  Execute: FAIL (exit code $?)"
    fi
  else
    echo "  Compile: FAIL"
  fi
done
```

## Integration with Course Workflow

### Before Content Review
1. Ensure sandbox is running
2. Extract code blocks from markdown
3. Write to temporary files in mounted volume
4. Compile and execute each
5. Compare output to stated expectations

### During Content Creation
1. Write code in content
2. Test in sandbox immediately
3. Capture actual output for documentation
4. Verify error examples produce expected errors

### For Student Exercises
1. Student writes solution
2. Solution tested in sandbox
3. Output compared to expected
4. Feedback provided

## Best Practices

1. **Always use timeouts** - Prevent infinite loops from blocking the sandbox
2. **Compile to /tmp** - Avoids permission issues with mounted volumes
3. **Capture both streams** - Always capture both stdout and stderr
4. **Check exit codes** - Don't assume success, verify return codes
5. **Clean up periodically** - Remove compiled binaries to save space
6. **Stop when idle** - Stop containers when not actively developing
7. **Rebuild regularly** - Rebuild containers to get security updates
8. **Log operations** - Keep logs for debugging validation issues
