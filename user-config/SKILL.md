---
name: user-config
description: "Manage Claude Code user configuration (~/.claude/). Actions: audit, backup, cleanup-agents, cleanup-debug, cleanup-hook-logs, cleanup-sessions, compaction-review, costs, file-versions, global, history, mcp, plans, prompt-extract, prune, reset, reset-plugins, restore, retrospective, session-stats, status, storage, transcript-search."
argument-hint: <action> [options] (audit|backup|cleanup-agents|cleanup-debug|cleanup-hook-logs|cleanup-sessions|compaction-review|costs|file-versions|global|history|mcp|plans|prompt-extract|prune|reset|reset-plugins|restore|retrospective|session-stats|status|storage|transcript-search)
allowed-tools: Bash, Read, Write, Glob, Grep, Skill, AskUserQuestion
---

# User Configuration Management

Unified skill for managing Claude Code user configuration (`~/.claude/` and `~/.claude.json`). Consolidates all user-config operations into a single entry point with action-based routing.

**Related Skill:** Invoke the `claude-ecosystem:user-config-management` skill for the meta-level configuration authority, known-structure manifest, and docs-management delegation patterns.

## Quick Decision Tree

**What do you want to do?**

| Intent | Action | Read-Only? |
|--------|--------|------------|
| Check config health at a glance | `status` | Yes |
| Deep health audit with drift detection | `audit` | Yes (unless `--fix`) |
| See storage breakdown and recommendations | `storage` | Yes |
| View session file counts and trends | `session-stats` | Yes |
| Estimate API costs and token usage | `costs` | Yes |
| Clean up old session files | `cleanup-sessions` | **Destructive** |
| Clean up old agent transcripts | `cleanup-agents` | **Destructive** |
| Clean up old debug files | `cleanup-debug` | **Destructive** |
| Clean up old hook log files | `cleanup-hook-logs` | **Destructive** |
| Comprehensive cleanup (all categories) | `prune` | **Destructive** |
| Backup config to ~/.claude-backups/ | `backup` | No (creates files) |
| Restore config from backup | `restore` | No (overwrites files) |
| Reset Claude Code preserving MCP servers | `reset` | **Destructive** |
| Nuclear plugin reset (cache+registry) | `reset-plugins` | **Destructive** |
| View/edit ~/.claude.json global config | `global` | Depends on mode |
| List/manage MCP server configurations | `mcp` | Depends on mode |
| Search/analyze command history | `history` | Yes (unless `--clear`) |
| List/view/archive plan files | `plans` | Depends on mode |
| Browse file edit history across sessions | `file-versions` | Yes (unless `--restore`) |
| Review compaction information loss | `compaction-review` | Yes |
| Extract successful prompts from sessions | `prompt-extract` | Yes |
| Search across session transcripts | `transcript-search` | Yes |
| Generate session retrospective/postmortem | `retrospective` | Yes |

## Argument Routing Table

| Action | Arguments | Default Behavior | Reference |
|--------|-----------|------------------|-----------|
| `audit` | `[--fix] [--verbose]` | Full audit with summary report | [audit.md](references/audit.md) |
| `backup` | `[--include-history] [--include-sessions]` | Backup essential config only | [backup.md](references/backup.md) |
| `cleanup-agents` | `[days] [--dry-run] [--all-projects]` | Remove agent files >7 days, current project | [cleanup-agents.md](references/cleanup-agents.md) |
| `cleanup-debug` | `[days] [--dry-run]` | Remove debug files >7 days | [cleanup-debug.md](references/cleanup-debug.md) |
| `cleanup-hook-logs` | `[days] [--dry-run]` | Remove hook logs >30 days | [cleanup-hook-logs.md](references/cleanup-hook-logs.md) |
| `cleanup-sessions` | `[days] [--dry-run] [--all-projects]` | Remove session files >7 days, current project | [cleanup-sessions.md](references/cleanup-sessions.md) |
| `compaction-review` | `[session-id] [--current] [--compare]` | Review most recent compaction | [compaction-review.md](references/compaction-review.md) |
| `costs` | `[--days N] [--project] [--breakdown] [--export FILE]` | Summary of recent costs (30 days) | [costs.md](references/costs.md) |
| `file-versions` | `<file-path> [--list] [--diff VER] [--restore VER]` | Show version summary for cwd | [file-versions.md](references/file-versions.md) |
| `global` | `[--view] [--edit SECTION] [--validate]` | View config summary | [global.md](references/global.md) |
| `history` | `<search-term> [--days N] [--stats] [--export FILE] [--clear]` | Show recent history summary | [history.md](references/history.md) |
| `mcp` | `[--list] [--export FILE] [--import FILE] [--add NAME] [--remove NAME]` | Show MCP server summary | [mcp.md](references/mcp.md) |
| `plans` | `[plan-name] [--list] [--archive] [--cleanup N]` | List recent plans | [plans.md](references/plans.md) |
| `prompt-extract` | `[--successful-only] [--category CAT] [--days N] [--export FILE]` | Extract all prompts (30 days) | [prompt-extract.md](references/prompt-extract.md) |
| `prune` | `[days] [--dry-run] [--all-projects] [--include-debug] [--include-todos] [--nuclear]` | Comprehensive cleanup >7 days, current project | [prune.md](references/prune.md) |
| `reset` | `[--backup] [--restore] [--list-backups]` | Interactive reset wizard | [reset.md](references/reset.md) |
| `reset-plugins` | `[--dry-run] [--include-marketplaces] [--force]` | Clear all except marketplaces | [reset-plugins.md](references/reset-plugins.md) |
| `restore` | `[backup-name] [--list] [--mcp-only] [--dry-run]` | Interactive selection from backups | [restore.md](references/restore.md) |
| `retrospective` | `[session-id] [--current] [--days N]` | Analyze most recent session | [retrospective.md](references/retrospective.md) |
| `session-stats` | `[--all-projects]` | Stats for current project | [session-stats.md](references/session-stats.md) |
| `status` | (none) | Unified config overview | [status.md](references/status.md) |
| `storage` | `[--verbose]` | Storage analysis with recommendations | [storage.md](references/storage.md) |
| `transcript-search` | `<query> [--days N] [--project] [--regex] [--context N]` | Search all projects, all time | [transcript-search.md](references/transcript-search.md) |

## Common Argument Patterns

These patterns are shared across multiple actions:

| Pattern | Used By | Description |
|---------|---------|-------------|
| `[days]` | cleanup-agents, cleanup-debug, cleanup-sessions, prune | Remove files older than N days (non-negative integer) |
| `--dry-run` | cleanup-*, prune, reset-plugins, restore | Preview without making changes |
| `--all-projects` | cleanup-agents, cleanup-sessions, prune | Apply to all projects (default: current only) |
| `--days N` | costs, history, prompt-extract, transcript-search | Limit time range for analysis |
| `--export FILE` | costs, history, mcp, prompt-extract | Export results to file |
| `--project` | costs, transcript-search | Limit to current project |

## Safety Classification

### Read-Only Actions (Always Safe)

`audit` (without --fix), `compaction-review`, `costs`, `file-versions` (without --restore), `prompt-extract`, `retrospective`, `session-stats`, `status`, `storage`, `transcript-search`

### Destructive Actions (Require Confirmation)

All destructive actions MUST use `AskUserQuestion` before deletion. Never delete files without explicit user confirmation.

| Action | What Gets Deleted | Reversible? |
|--------|-------------------|-------------|
| `cleanup-agents` | Agent transcript files (agent-*.jsonl) | No |
| `cleanup-debug` | Debug transcript files | No |
| `cleanup-hook-logs` | Hook log .jsonl files | No |
| `cleanup-sessions` | Session .jsonl files | No |
| `prune` | Sessions + agents + statsig + plans + optionally debug/todos/locks | No |
| `reset` | User must manually delete ~/.claude/ (skill only prepares backup) | Partially (backup) |
| `reset-plugins` | Plugin cache, registry, enabledPlugins setting | Partially (reinstall) |
| `history --clear` | Command history entries | No |

### Write Actions (Create/Modify Files)

| Action | What Gets Written |
|--------|-------------------|
| `backup` | Creates backup in ~/.claude-backups/ |
| `restore` | Overwrites config files from backup |
| `global --edit` | Modifies ~/.claude.json |
| `mcp --add/--remove/--import` | Modifies ~/.claude.json mcpServers |
| `plans --archive` | Moves plan files to archive/ subdirectory |

## Protected Files (Never Deleted)

These files are NEVER touched by any cleanup action:

| File | Reason |
|------|--------|
| `~/.claude/CLAUDE.md` | User instructions |
| `~/.claude/settings.json` | User settings |
| `~/.claude/settings.local.json` | Local settings |
| `~/.claude/.credentials.json` | OAuth tokens (never backup either) |
| `~/.claude/history.jsonl` | Command history (use `history --clear` explicitly) |
| `~/.claude/plugins/` | Installed plugins (use `/plugin uninstall`) |
| `~/.claude/file-history/` | Edit undo history (losing this removes /rewind capability) |
| `~/.claude/commands/` | User commands |
| `~/.claude/skills/` | User skills |
| `~/.claude/agents/` | User agents |
| `~/.claude/hooks/` | User hooks |

## Cross-Platform Path Handling

All actions handle paths cross-platform:

**Python:** Use `pathlib.Path.home() / ".claude"` -- never hardcode OS-specific paths.

**Bash:** Use `$HOME/.claude` -- works on macOS, Linux, and Git Bash on Windows.

**Project path encoding:** `pwd | sed 's/[\/:]/-/g' | sed 's/^-//'`

## Execution

### Step 1: Parse Action

Extract the action from `$ARGUMENTS`:

```text
ACTION = first non-flag argument (audit, backup, cleanup-agents, etc.)
REMAINING_ARGS = everything after the action
```

If no action provided or action is unrecognized, show the Quick Decision Tree above and ask user to specify an action.

### Step 2: Load Reference

Load the detailed reference file for the action from `references/{action}.md`. The reference contains the complete operational instructions, workflows, code examples, and output formats.

### Step 3: Execute

Follow the instructions in the reference file, passing `REMAINING_ARGS` as the action's arguments.
