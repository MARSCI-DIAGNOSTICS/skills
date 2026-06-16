---
name: check-context
description: Analyze current context window usage and provide optimization recommendations
allowed-tools: Read, Bash
---

# Check Context

Analyze the current context window state and provide recommendations for optimization. This helps identify when context is becoming bloated and action is needed.

## Usage

```text
/check-context
```

## What Gets Analyzed

1. **Current Context Size** - Estimated token usage
2. **Context Composition** - What's consuming tokens
3. **Health Assessment** - Whether action is needed
4. **Optimization Options** - Available remediation

## Context Health Thresholds

| Usage | Status | Action |
|-------|--------|--------|
| < 50% | HEALTHY | No action needed |
| 50-75% | MONITOR | Consider /compact soon |
| 75-85% | WARNING | Run /compact or /clear |
| > 85% | CRITICAL | Immediate action required |

## Context Composition (Typical)

Claude Code's context typically includes:

| Component | Typical Size | Notes |
|-----------|--------------|-------|
| System prompt | 15-25k tokens | Base instructions |
| CLAUDE.md files | 5-15k tokens | Memory files |
| Loaded skills | 1-5k tokens | Active skills |
| Conversation history | Variable | Grows with turns |
| Tool results | Variable | Can be large |
| File contents | Variable | From Read operations |

## Workflow

### Step 1: Estimate Context Usage

Note: Exact context usage is internal to Claude Code. This command provides estimates based on observable factors:

```text
Factors to consider:
- Conversation length (turns)
- Recent file reads
- Tool output volume
- Loaded skills/memory
```

### Step 2: Assess Health

Based on observable signals:

**Healthy Indicators:**

- Quick response times
- No truncation warnings
- Accurate recall of early context

**Warning Indicators:**

- Slower responses
- Occasional memory gaps
- Auto-compact messages appearing

**Critical Indicators:**

- Very slow responses
- Frequent context rot
- Truncation warnings
- Failed operations

### Step 3: Provide Recommendations

```text
Context Window Analysis
=======================

Estimated Status: {HEALTHY | MONITOR | WARNING | CRITICAL}

Observable Indicators:
  Conversation turns: {count}
  Recent file reads: {count} files
  Tool invocations: {count}
  Skills loaded: {list}

Assessment:
  {description of current state}

Recommendations:
  {prioritized actions}

Available Commands:
  /clear    - Complete context reset (nuclear option)
  /compact  - Intelligent summarization (preserves key info)
  /cost     - View token usage and costs

Tips for Context Management:
  - Use /clear between major task switches
  - Prefer focused, specific queries over broad exploration
  - Let Claude use sub-agents for large operations
  - Break large tasks into smaller sessions
```

## Example Output

### Healthy Context

```text
Context Window Analysis
=======================

Estimated Status: HEALTHY

Observable Indicators:
  Conversation turns: 8
  Recent file reads: 3 files
  Tool invocations: 12
  Skills loaded: 2 (docs-management, skill-development)

Assessment:
  Context appears healthy. Responses are quick and
  accurate. No signs of degradation.

Recommendations:
  No action needed. Continue as normal.

Tips:
  - Current session is efficient
  - Consider /clear before starting a new major task
```

### Warning State

```text
Context Window Analysis
=======================

Estimated Status: WARNING

Observable Indicators:
  Conversation turns: 47
  Recent file reads: 23 files
  Tool invocations: 156
  Skills loaded: 5

Assessment:
  Context is getting full. You may notice:
  - Slightly slower responses
  - Occasional gaps in recalling earlier context
  - Auto-compaction may trigger soon

Recommendations:
  1. Run /compact to summarize and free space
  2. Or run /clear if starting a new task
  3. Save important context to a temp file first

Warning Signs to Watch:
  - If responses slow further, act immediately
  - Watch for truncation or "I don't recall" responses
```

### Critical State

```text
Context Window Analysis
=======================

Estimated Status: CRITICAL

Observable Indicators:
  Conversation turns: 89
  Recent file reads: 45 files
  Tool invocations: 312
  Skills loaded: 7
  Auto-compact triggered: 3 times

Assessment:
  Context is near capacity. Significant degradation likely:
  - Very slow responses expected
  - Poor recall of earlier context
  - Risk of failed operations

IMMEDIATE ACTION REQUIRED:

  Option 1 (Preserve Progress):
    1. Document current task state to file
    2. Run /compact
    3. Resume with focused context

  Option 2 (Clean Start):
    1. Run /clear
    2. Reload only essential context
    3. Continue with fresh context

  Option 3 (New Session):
    1. Note session ID for /resume if needed
    2. Start new Claude Code session
    3. Fresh 200k token context
```

## Notes

- This command provides estimates - exact token counts are internal
- Observable signals are good proxies for context health
- When in doubt, /compact is safer than continuing
- Sub-agents help by isolating context-heavy operations
