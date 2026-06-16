---
name: create-strategy
description: Create a comprehensive test strategy document following IEEE 829 structure. Use for establishing testing approach on new projects or standardizing existing practices.
allowed-tools: Read, Write, Glob, Grep, Skill, Task
argument-hint: [project-context]
---

# Create Test Strategy Command

Generate a comprehensive test strategy document tailored to the project.

## Process

### Step 1: Gather Context

If project context is provided in arguments, use it. Otherwise:

1. Look for existing documentation:
   - Requirements documents
   - Architecture documents
   - Existing test plans
   - Risk assessments

2. Identify project characteristics:
   - Technology stack (.NET, React, etc.)
   - Architecture style (monolith, microservices)
   - Deployment model (cloud, on-prem)
   - Team size and structure

### Step 2: Load Skills

Invoke the `test-strategy:test-strategy-planning` skill for IEEE 829 templates and guidance.

### Step 3: Spawn Strategy Agent

Delegate to the `test-strategist` agent:

```text
Analyze the project context and create a comprehensive test strategy document.

Project Context:
[Gathered context]

Requirements:
1. Follow IEEE 829 structure
2. Include specific test level recommendations
3. Define measurable entry/exit criteria
4. Address identified risks
5. Recommend appropriate tools for the tech stack
```

### Step 4: Review and Validate

Ensure the strategy includes:

- [ ] Clear scope definition (in/out)
- [ ] Test objectives tied to business goals
- [ ] Test levels with responsibilities
- [ ] Test types appropriate for the project
- [ ] Risk-based prioritization
- [ ] Environment requirements
- [ ] Entry/exit criteria
- [ ] Defect management process
- [ ] Deliverables and schedule
- [ ] Roles and responsibilities

### Step 5: Output

Save the strategy document and report location:

```markdown
## Test Strategy Created

**File**: [path to strategy document]

**Summary**:
- Scope: [brief scope]
- Test Levels: [unit, integration, E2E]
- Key Risks: [top 3 risks addressed]
- Tools: [recommended stack]

**Next Steps**:
1. Review strategy with stakeholders
2. Set up test environments
3. Begin test case design
```

## Examples

**Simple invocation:**

```bash
/test-strategy:create-strategy
```

**With context:**

```bash
/test-strategy:create-strategy e-commerce platform with payments, .NET 10, microservices
```
