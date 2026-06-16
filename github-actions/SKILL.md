---
name: github-actions
description: GitHub Actions workflow design, job structure, triggers, reusable workflows, and best practices. Use when creating or reviewing CI/CD pipelines.
allowed-tools: Read, Write, Glob, Grep, mcp__perplexity__search, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# GitHub Actions Skill

Design and implement GitHub Actions workflows for CI/CD automation.

## When to Use This Skill

**Keywords:** github actions, ci/cd, workflow, pipeline, build, deploy, continuous integration, continuous deployment, yaml workflow, job, step, runner, matrix, reusable workflow

**Use this skill when:**

- Creating new GitHub Actions workflows
- Reviewing existing workflow files
- Designing CI/CD pipelines for repositories
- Setting up build/test/deploy automation
- Implementing reusable workflow patterns

## MANDATORY: Documentation-First Approach

Before creating workflows:

1. **Verify syntax** via MCP servers (context7 for GitHub Actions docs)
2. **Check for existing patterns** in the repository
3. **Use official actions** where possible (actions/checkout, actions/setup-node, etc.)

## Workflow Structure Overview

```yaml
name: Workflow Name

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Step name
        run: echo "Hello"
```

## Key Concepts

### Triggers (on)

| Trigger | Use Case |
|---------|----------|
| `push` | Run on every push to specified branches |
| `pull_request` | Run on PR events |
| `workflow_dispatch` | Manual trigger |
| `schedule` | Cron-based scheduling |
| `workflow_call` | Called by other workflows (reusable) |

### Job Configuration

| Setting | Purpose |
|---------|---------|
| `runs-on` | Runner environment (ubuntu-latest, windows-latest, macos-latest) |
| `needs` | Job dependencies |
| `if` | Conditional execution |
| `strategy.matrix` | Matrix builds |
| `environment` | Deployment environment with protection rules |

### Common Actions

| Action | Purpose |
|--------|---------|
| `actions/checkout@v4` | Checkout repository |
| `actions/setup-node@v4` | Setup Node.js |
| `actions/setup-python@v5` | Setup Python |
| `actions/setup-dotnet@v4` | Setup .NET |
| `actions/cache@v4` | Cache dependencies |
| `actions/upload-artifact@v4` | Upload build artifacts |

## Best Practices

### Security

```yaml
permissions:
  contents: read  # Minimal permissions

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4  # Pin to specific version
```

### Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Matrix Builds

```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
    os: [ubuntu-latest, windows-latest]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
    secrets:
      NPM_TOKEN:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci && npm test
```

**Calling reusable workflow:**

```yaml
jobs:
  call-test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
    secrets: inherit
```

## Workflow Patterns

### PR Validation

```yaml
name: PR Validation
on:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
```

### Release Workflow

```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Permission denied | Add `permissions` block with required access |
| Action not found | Check action version and repository |
| Cache not working | Verify `key` pattern matches file paths |
| Job dependency failed | Check `needs` references and job names |

## MCP Research

For current GitHub Actions patterns:

```text
perplexity: "GitHub Actions best practices 2026"
context7: "github-actions" (for official documentation)
```

## Version History

- **v1.0.0** (2026-01-17): Initial release

---

**Last Updated:** 2026-01-17
