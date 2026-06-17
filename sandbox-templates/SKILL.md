---
description: Use this skill when setting up Docker sandbox environments for courses. Provides language-specific Dockerfile templates with compilers, linters, debuggers, and test frameworks. Trigger phrases include "sandbox template", "Dockerfile", "setup sandbox", "create container", "development environment".
---

# Sandbox Templates - Language-Specific Docker Configurations

Pre-configured Dockerfile templates for different programming languages with all necessary tools for compiling, testing, linting, and debugging course code.

## Template Selection

Choose the appropriate template based on the course's primary language:

| Language | Template | Base Image | Size |
|----------|----------|------------|------|
| C++ | `cpp-sandbox` | Ubuntu 24.04 | ~1.5GB |
| Rust | `rust-sandbox` | Rust Official | ~1.2GB |
| Python | `python-sandbox` | Python 3.12 | ~800MB |
| Go | `go-sandbox` | Go Official | ~900MB |
| C | `c-sandbox` | Ubuntu 24.04 | ~1.2GB |
| Multi-language | `multi-sandbox` | Ubuntu 24.04 | ~2.5GB |

---

## C++ Sandbox Template

For C++ courses (C++17/20/23 support).

### Dockerfile
```dockerfile
# C++ Development Sandbox
# Supports: C++17, C++20, C++23 (partial)
# Tools: GCC 13, Clang 17, CMake, GDB, Valgrind, clang-tidy, cppcheck

FROM ubuntu:24.04

LABEL maintainer="course-builder"
LABEL description="C++ development sandbox for course materials"

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install compilers and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Compilers
    g++-13 \
    gcc-13 \
    clang-17 \
    clang++-17 \
    # Build tools
    cmake \
    ninja-build \
    make \
    # Debugging
    gdb \
    lldb-17 \
    valgrind \
    # Linting
    clang-tidy-17 \
    clang-format-17 \
    cppcheck \
    # Testing frameworks
    libgtest-dev \
    libgmock-dev \
    catch2 \
    # Utilities
    git \
    curl \
    wget \
    unzip \
    pkg-config \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Set up alternatives for gcc/g++
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 100 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 100 \
    && update-alternatives --install /usr/bin/clang clang /usr/bin/clang-17 100 \
    && update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-17 100 \
    && update-alternatives --install /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-17 100 \
    && update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-17 100

# Build and install Google Test (if not available as package)
RUN cd /usr/src/gtest && cmake . && make && cp lib/*.a /usr/lib/

# Create non-root user for safety
RUN useradd -m -s /bin/bash sandbox
USER sandbox

WORKDIR /workspace

# Default command keeps container running
CMD ["tail", "-f", "/dev/null"]
```

### Common Commands
```bash
# Compile with GCC (C++20)
g++ -std=c++20 -Wall -Wextra -Werror -o /tmp/prog source.cpp

# Compile with Clang (C++20)
clang++ -std=c++20 -Wall -Wextra -Werror -o /tmp/prog source.cpp

# Compile with sanitizers
g++ -std=c++20 -fsanitize=address,undefined -g -o /tmp/prog source.cpp

# Run clang-tidy
clang-tidy source.cpp -- -std=c++20

# Run cppcheck
cppcheck --enable=all --std=c++20 source.cpp

# Debug with GDB
gdb /tmp/prog

# Memory check with Valgrind
valgrind --leak-check=full /tmp/prog

# CMake build
cmake -B build -G Ninja && cmake --build build

# Run tests
ctest --test-dir build --output-on-failure
```

---

## Rust Sandbox Template

For Rust courses (stable and nightly support).

### Dockerfile
```dockerfile
# Rust Development Sandbox
# Supports: Stable, Beta, Nightly Rust
# Tools: rustc, cargo, clippy, rustfmt, rust-analyzer, miri

FROM rust:1.83-bookworm

LABEL maintainer="course-builder"
LABEL description="Rust development sandbox for course materials"

# Install additional toolchains
RUN rustup component add \
    clippy \
    rustfmt \
    rust-src \
    rust-analyzer

# Install nightly for miri and advanced features
RUN rustup toolchain install nightly \
    && rustup component add --toolchain nightly miri rust-src

# Install useful cargo extensions
RUN cargo install \
    cargo-watch \
    cargo-expand \
    cargo-audit \
    cargo-outdated \
    cargo-tarpaulin

# Install system dependencies for common crates
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libssl-dev \
    gdb \
    lldb \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash sandbox
USER sandbox

# Set up cargo home for non-root user
ENV CARGO_HOME=/home/sandbox/.cargo
ENV PATH="${CARGO_HOME}/bin:${PATH}"

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"]
```

### Common Commands
```bash
# Compile single file
rustc -o /tmp/prog source.rs

# Build with cargo
cargo build

# Build release
cargo build --release

# Run
cargo run

# Run tests
cargo test

# Run specific test
cargo test test_name

# Lint with clippy
cargo clippy -- -D warnings

# Format code
cargo fmt

# Check without building
cargo check

# Expand macros
cargo expand

# Run with miri (memory safety)
cargo +nightly miri run

# Run tests with miri
cargo +nightly miri test

# Security audit
cargo audit

# Test coverage
cargo tarpaulin
```

---

## Python Sandbox Template

For Python courses (3.12+ with type checking and testing tools).

### Dockerfile
```dockerfile
# Python Development Sandbox
# Supports: Python 3.12
# Tools: pytest, mypy, ruff, black, coverage, ipython

FROM python:3.12-slim-bookworm

LABEL maintainer="course-builder"
LABEL description="Python development sandbox for course materials"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python development tools
RUN pip install --no-cache-dir \
    # Testing
    pytest \
    pytest-cov \
    pytest-xdist \
    pytest-mock \
    hypothesis \
    # Type checking
    mypy \
    # Linting and formatting
    ruff \
    black \
    isort \
    # Interactive
    ipython \
    # Documentation
    pdoc \
    # Debugging
    pdbpp \
    # Utilities
    rich \
    typer

# Create non-root user
RUN useradd -m -s /bin/bash sandbox
USER sandbox

WORKDIR /workspace

# Set Python to unbuffered mode
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["tail", "-f", "/dev/null"]
```

### Common Commands
```bash
# Run script
python3 script.py

# Run with unbuffered output
python3 -u script.py

# Run module
python3 -m module_name

# Run tests
python3 -m pytest -v

# Run tests with coverage
python3 -m pytest --cov=. --cov-report=term-missing

# Run parallel tests
python3 -m pytest -n auto

# Type check
mypy script.py

# Type check strict
mypy --strict script.py

# Lint with ruff
ruff check .

# Fix linting issues
ruff check --fix .

# Format with black
black script.py

# Check formatting
black --check script.py

# Sort imports
isort script.py

# Interactive REPL
ipython
```

---

## Go Sandbox Template

For Go courses (latest stable version).

### Dockerfile
```dockerfile
# Go Development Sandbox
# Supports: Go 1.23+
# Tools: go, gofmt, golint, staticcheck, delve

FROM golang:1.23-bookworm

LABEL maintainer="course-builder"
LABEL description="Go development sandbox for course materials"

# Install additional tools
RUN go install golang.org/x/lint/golint@latest \
    && go install honnef.co/go/tools/cmd/staticcheck@latest \
    && go install github.com/go-delve/delve/cmd/dlv@latest \
    && go install golang.org/x/tools/cmd/goimports@latest \
    && go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdb \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash sandbox
USER sandbox

# Set up Go paths for non-root user
ENV GOPATH=/home/sandbox/go
ENV PATH="${GOPATH}/bin:${PATH}"

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"]
```

### Common Commands
```bash
# Run single file
go run main.go

# Build
go build -o /tmp/prog .

# Build with race detection
go build -race -o /tmp/prog .

# Run tests
go test ./...

# Run tests verbose
go test -v ./...

# Run tests with coverage
go test -cover ./...

# Run tests with race detection
go test -race ./...

# Run benchmarks
go test -bench=. ./...

# Format code
gofmt -w .

# Format and organize imports
goimports -w .

# Lint
golint ./...

# Static analysis
staticcheck ./...

# Comprehensive lint
golangci-lint run

# Debug with delve
dlv debug

# Vet code
go vet ./...
```

---

## C Sandbox Template

For C courses (C11/C17/C23 support).

### Dockerfile
```dockerfile
# C Development Sandbox
# Supports: C11, C17, C23
# Tools: GCC 13, Clang 17, Make, GDB, Valgrind

FROM ubuntu:24.04

LABEL maintainer="course-builder"
LABEL description="C development sandbox for course materials"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Compilers
    gcc-13 \
    clang-17 \
    # Build tools
    make \
    cmake \
    ninja-build \
    # Debugging
    gdb \
    lldb-17 \
    valgrind \
    # Linting
    clang-tidy-17 \
    cppcheck \
    # Utilities
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up alternatives
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 100 \
    && update-alternatives --install /usr/bin/clang clang /usr/bin/clang-17 100 \
    && update-alternatives --install /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-17 100

# Create non-root user
RUN useradd -m -s /bin/bash sandbox
USER sandbox

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"]
```

### Common Commands
```bash
# Compile with GCC (C17)
gcc -std=c17 -Wall -Wextra -Werror -o /tmp/prog source.c

# Compile with Clang
clang -std=c17 -Wall -Wextra -Werror -o /tmp/prog source.c

# Compile with debugging symbols
gcc -std=c17 -g -O0 -o /tmp/prog source.c

# Compile with sanitizers
gcc -std=c17 -fsanitize=address,undefined -g -o /tmp/prog source.c

# Run cppcheck
cppcheck --enable=all --std=c17 source.c

# Debug with GDB
gdb /tmp/prog

# Memory check
valgrind --leak-check=full --show-leak-kinds=all /tmp/prog

# Track origins of uninitialized values
valgrind --track-origins=yes /tmp/prog
```

---

## Multi-Language Sandbox Template

For courses covering multiple languages or comparisons.

### Dockerfile
```dockerfile
# Multi-Language Development Sandbox
# Supports: C, C++, Python, Go, Rust
# Full toolchain for each language

FROM ubuntu:24.04

LABEL maintainer="course-builder"
LABEL description="Multi-language development sandbox for course materials"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install C/C++ tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc-13 g++-13 clang-17 clang++-17 \
    cmake ninja-build make \
    gdb lldb-17 valgrind \
    clang-tidy-17 clang-format-17 cppcheck \
    libgtest-dev catch2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python tools
RUN pip3 install --break-system-packages --no-cache-dir \
    pytest pytest-cov mypy ruff black ipython

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . /root/.cargo/env \
    && rustup component add clippy rustfmt rust-src

# Install Go
RUN curl -LO https://go.dev/dl/go1.23.4.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz \
    && rm go1.23.4.linux-amd64.tar.gz

# Set up paths
ENV PATH="/usr/local/go/bin:/root/.cargo/bin:${PATH}"
ENV GOPATH="/root/go"

# Set up alternatives
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 100 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 100 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.12 100

# Install Go tools
RUN go install golang.org/x/lint/golint@latest \
    && go install honnef.co/go/tools/cmd/staticcheck@latest

# Create non-root user
RUN useradd -m -s /bin/bash sandbox \
    && cp -r /root/.cargo /home/sandbox/ \
    && chown -R sandbox:sandbox /home/sandbox/.cargo
USER sandbox

ENV PATH="/home/sandbox/.cargo/bin:/usr/local/go/bin:${PATH}"

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"]
```

---

## Sandbox Directory Structure

When a sandbox is set up, the following structure is created in the course directory:

```
course-name/
├── .sandbox/
│   ├── Dockerfile          # Language-specific Dockerfile
│   ├── docker-compose.yml  # Optional: for complex setups
│   ├── .dockerignore       # Files to exclude from build
│   └── scripts/
│       ├── setup.sh        # Post-creation setup script
│       ├── validate.sh     # Code validation script
│       └── cleanup.sh      # Cleanup script
├── chapters/
├── exercises/
├── projects/
└── ...
```

### docker-compose.yml (Optional)
```yaml
version: '3.8'

services:
  sandbox:
    build:
      context: .
      dockerfile: .sandbox/Dockerfile
    container_name: course-sandbox-${COURSE_ID:-default}
    volumes:
      - ..:/workspace
    working_dir: /workspace
    stdin_open: true
    tty: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2'
    network_mode: none
```

### .dockerignore
```
# Ignore build artifacts
build/
target/
__pycache__/
*.pyc
*.o
*.a
*.so

# Ignore IDE files
.idea/
.vscode/
*.swp
*.swo

# Ignore git
.git/
.gitignore

# Ignore large files
*.pdf
*.zip
*.tar.gz
```

---

## Customization Guidelines

### Adding Course-Specific Dependencies

Extend the base template with additional packages:

```dockerfile
# Base template
FROM course-sandbox-cpp:latest

# Add course-specific libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libboost-all-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*
```

### Environment Variables

Set course-specific environment variables:

```dockerfile
# Compiler settings
ENV CXX=g++
ENV CC=gcc
ENV CXXFLAGS="-std=c++20 -Wall -Wextra"

# Course-specific paths
ENV COURSE_LIB_PATH=/workspace/lib
ENV COURSE_INCLUDE_PATH=/workspace/include
```

### Mount Points

Configure additional volume mounts for shared resources:

```bash
docker run -d \
  --name course-sandbox-cpp-fundamentals \
  -v "$(pwd):/workspace" \
  -v "/shared/test-data:/data:ro" \
  -v "/shared/reference:/reference:ro" \
  course-sandbox-cpp:latest
```
