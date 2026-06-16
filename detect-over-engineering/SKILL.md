---
name: detect-over-engineering
description: Detect unnecessary complexity, speculative generality, and over-engineered solutions in code
allowed-tools: Read, Glob, Grep, Task
argument-hint: "[path-or-pattern]"
---

# Detect Over-Engineering Command

Analyze code to identify unnecessary complexity, speculative generality, and over-engineered solutions.

## Usage

```text
/enterprise-architecture:detect-over-engineering [path-or-pattern]
```

## Arguments

- `path-or-pattern` (optional): Path to analyze
  - If provided: Analyze the specified path or pattern
  - If omitted: Analyze the entire codebase

## Examples

```text
/enterprise-architecture:detect-over-engineering
/enterprise-architecture:detect-over-engineering src/services/
/enterprise-architecture:detect-over-engineering **/*.cs
```

## Workflow

1. **Scan for Complexity Indicators**
   - Search for patterns indicating over-engineering
   - Identify abstraction layers
   - Find unused flexibility points

2. **Spawn Over-Engineering Detector Agent**
   Use the `over-engineering-detector` agent to analyze. The agent detects:
   - **Speculative Generality** - Abstractions without multiple implementations
   - **Premature Abstraction** - Complexity before demonstrated need
   - **Gold Plating** - Features beyond requirements
   - **Astronaut Architecture** - Excessive layers and indirection

3. **Present Findings**
   Display findings organized by:
   - **Critical** - Significant complexity with no benefit
   - **Warning** - Potential over-engineering
   - **Info** - Minor simplification opportunities

## Detection Categories

### Speculative Generality

- Abstract classes with single implementation
- Interfaces with only one implementer
- Generic type parameters never varied
- Configuration options never used
- Plugin architectures with no plugins

### Premature Abstraction

- Factory patterns for single object creation
- Strategy patterns with one strategy
- Excessive dependency injection
- Over-normalized data structures

### Gold Plating

- Features beyond documented requirements
- Configurability that's never configured
- Extensibility points never extended

## Output Format

```text
## Over-Engineering Detection Report

### Summary
- Files analyzed: [N]
- Issues found: [N] (Critical: X, Warning: Y, Info: Z)

### Critical Issues

#### [Issue Type]: [Location]
**Pattern:** [What was found]
**Problem:** [Why it's over-engineered]
**Simplification:** [How to simplify]
**Effort:** [Low/Medium/High]

### Warnings

[Same structure]

### Info

[Same structure]

### Simplification Roadmap
1. [Quick win] - [Impact]
2. [Medium effort] - [Impact]
3. [Larger refactor] - [Impact]

### Metrics
- Estimated lines removable: [N]
- Abstraction layers reducible: [N]
- Complexity score improvement: [X]%
```
