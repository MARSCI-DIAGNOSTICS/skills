# Claude Code Component Detection and Validation

**Tier:** 4b (Claude Code Ecosystem)
**Load When:** Changed files match Claude Code component patterns
**Token Cost:** ~1,500 tokens

## Overview

This reference provides detection patterns for Claude Code ecosystem files and maps them to specialized auditor agents from the `claude-ecosystem` plugin.

## Orchestration Responsibility

**IMPORTANT:** Auditor spawning is handled by the `/code-quality:review` command, NOT by the code-reviewer agent.

The code-reviewer agent lacks Task tool access and CANNOT spawn subagents. When reviewing Claude Code files:

| Component | Responsibility |
| --- | --- |
| **Review Command** | Detects CC files, spawns auditors via Task tool, integrates findings |
| **Code-Reviewer Agent** | Basic syntax checks only (YAML, JSON, markdown structure) |
| **Auditor Agents** | Comprehensive validation via development skills → docs-management |

The detection patterns and auditor mappings in this document are used BY THE REVIEW COMMAND to orchestrate validation.

## Detection Patterns

Use these Glob patterns to detect Claude Code components in changed files:

| Component Type | Detection Patterns |
| --- | --- |
| Agent | `.claude/agents/**/*.md`, `agents/*.md` |
| Hook | `.claude/hooks/**`, `hooks.json` |
| Skill | `.claude/skills/**`, `skills/*/SKILL.md` |
| Memory | `CLAUDE.md`, `.claude/memory/**/*.md` |
| Output Style | `output-styles/*.md` |
| MCP Config | `.mcp.json`, `mcp.json` |
| Settings | `settings.json`, `.claude/settings.json`, `.claude/settings.local.json` |
| Plugin | `plugin.json`, `.claude-plugin/**` |
| Status Line | Scripts in skill directories with status line naming patterns |

## Auditor Mapping

Each Claude Code component type maps to a specialized auditor agent:

| Component Type | Auditor Agent | Plugin | Skills Used |
| --- | --- | --- | --- |
| Agent | `claude-ecosystem:agent-auditor` | claude-ecosystem | subagent-development |
| Command | `claude-ecosystem:skill-auditor` | claude-ecosystem | skill-development |
| Hook | `claude-ecosystem:hook-auditor` | claude-ecosystem | hook-management |
| Skill | `claude-ecosystem:skill-auditor` | claude-ecosystem | skill-development |
| Memory | `claude-ecosystem:memory-component-auditor` | claude-ecosystem | memory-management |
| Output Style | `claude-ecosystem:output-style-auditor` | claude-ecosystem | output-customization |
| MCP Config | `claude-ecosystem:mcp-auditor` | claude-ecosystem | mcp-integration |
| Settings | `claude-ecosystem:settings-auditor` | claude-ecosystem | settings-management |
| Plugin | `claude-ecosystem:plugin-component-auditor` | claude-ecosystem | plugin-development |
| Status Line | `claude-ecosystem:statusline-auditor` | claude-ecosystem | status-line-customization |

## Detection Workflow

### Step 1: Identify Claude Code Files

```bash
# Get list of changed files (staged or PR)
git diff --staged --name-only
# OR
git diff --name-only main...HEAD
```

### Step 2: Match Against Detection Patterns

For each changed file, check against detection patterns using Glob:

```text
For each pattern in Detection Patterns table:
  If file matches pattern:
    Add to component group
    Note component type
```

### Step 3: Check Plugin Availability

Before spawning auditors, verify `claude-ecosystem` plugin is installed:

```text
Attempt to spawn one auditor agent (e.g., skill-auditor)
If spawn succeeds:
  Plugin is available - proceed with full validation
If spawn fails:
  Plugin not installed - use fallback behavior
```

### Step 4: Spawn Auditors (Batched)

To prevent context exhaustion, batch auditor invocations:

```text
Round 1: Spawn 2-3 auditors for highest-priority component types
         Wait for completion
Round 2: Spawn next 2-3 auditors
         Wait for completion
Continue until all component types processed
```

**Priority Order:**

1. Memory (CLAUDE.md) - affects all other components
2. Skills - defines behavior and validation criteria
3. Agents - uses skills
4. Commands - invokes agents/skills
5. Hooks - runtime behavior
6. Others (MCP, Settings, Plugin, Output Style, Status Line)

## Plugin Unavailable - REVIEW FAILS

**CRITICAL:** When Claude Code files are detected but the `claude-ecosystem` plugin is not installed, the review FAILS. There is no silent degradation.

### Failure Behavior

The review command will:

1. **STOP** the review process
2. **FAIL** with a clear error message
3. **Provide installation instructions**

### Failure Message

```markdown
## REVIEW FAILED: Claude Code Validation Required

Claude Code files were detected but cannot be validated:
- [list of detected CC files by type]

**Reason**: The `claude-ecosystem` plugin is not installed.

**Required Action**: Install the plugin to enable CC validation:
`/plugin install claude-ecosystem@claude-code-plugins`

**Why This Matters**: Claude Code components (skills, agents, hooks, etc.)
require specialized validation via auditor agents. Without proper validation:
- Invalid YAML frontmatter fields may be introduced
- Tool configurations may reference non-existent tools
- Components may violate official documentation requirements

After installing the plugin, re-run the review.
```

### Rationale

Silent degradation (logging a warning and continuing) was removed because:

1. **Partial validation is dangerous** - Users may think CC files passed review when they weren't validated
2. **Invalid components cause runtime failures** - Unvalidated CC files may break Claude Code
3. **Docs-driven validation is essential** - Auditors delegate to docs-management for official validation criteria

### Basic Syntax Checks (Code-Reviewer Agent)

The code-reviewer agent still performs basic structural checks as documented in its Tier 4b section, but these do NOT constitute full CC validation.

## Auditor Finding Integration

Map auditor findings to code review severity levels:

| Auditor Score | Auditor Result | Review Severity |
| --- | --- | --- |
| < 70 | FAIL | CRITICAL |
| 70-84 | PASS WITH WARNINGS | MAJOR |
| 85-100 | PASS | MINOR (if issues flagged) |

### Finding Format

Include auditor source in findings:

```markdown
### [Issue Title]

**File**: `path/to/file.md:line`
**Severity**: MAJOR
**Category**: Claude Code Compliance
**Source**: claude-ecosystem:skill-auditor

**Problem**: [Description from auditor]

**Impact**: [Why this matters for CC ecosystem]

**Fix**: [Auditor recommendation]
```

## Component-Specific Validation Points

### Agents

- YAML frontmatter: name, description, tools, model, color, skills, permissionMode
- Tool restrictions appropriate for agent purpose
- Model selection (opus for complex, haiku for simple)
- Skills reference valid skills

### Commands

- YAML frontmatter: description, allowed-tools, argument-hint
- Description is clear and action-oriented
- Tool restrictions match command purpose
- Argument handling ($ARGUMENTS, $1, $2)

### Skills

- SKILL.md has YAML frontmatter
- References directory structure
- Progressive disclosure patterns
- Delegation to docs-management for official docs

### Hooks

- Valid JSON syntax in hooks.json
- Correct event types (PreToolUse, PostToolUse, etc.)
- Matcher patterns valid regex/glob
- Hook scripts executable and correct shebang

### Memory

- CLAUDE.md at correct location
- Import syntax correct (@.claude/memory/...)
- No circular imports
- Size guidelines respected

### MCP Config

- Valid JSON syntax
- Server configurations complete
- Transport types valid
- Environment variables properly referenced

### Settings

- Valid JSON syntax
- Permission rules properly formatted
- No exposed secrets
- Environment variables for sensitive values

### Output Styles

- YAML frontmatter with name, description
- Valid markdown structure
- Formatting instructions clear

### Plugins

- plugin.json manifest complete
- All referenced files exist
- Namespace conventions followed
- Version properly formatted

## References

- Agent format: `docs-management` → "agent frontmatter"
- Command format: `skill-development` skill
- Hook events: `hook-management` skill
- Memory syntax: `memory-management` skill
- MCP config: `mcp-integration` skill
- Settings format: `settings-management` skill
- Skill format: `skill-development` skill
- Output styles: `output-customization` skill
- Plugin format: `plugin-development` skill

---

**Last Updated:** 2025-12-29
