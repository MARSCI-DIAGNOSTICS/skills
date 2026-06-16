---
name: skill-migration
description: "Migrate legacy .claude/commands/ to .claude/skills/ directory structure. Actions: discover, analyze, migrate, audit, validate, fix."
argument-hint: <action> (discover|analyze|migrate|audit|validate|fix) [options]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion
---

# Commands-to-Skills Migration

Migrate legacy `.claude/commands/*.md` flat files to the modern `.claude/skills/*/SKILL.md` directory structure introduced in Claude Code v2.1.3+. This skill is designed to work in **any repository** -- whether it has this plugin installed or is a standalone project with legacy commands.

## Background

Claude Code unified commands and skills in v2.1.3. The key differences:

| Concept | Old (Commands) | New (Skills) |
|---------|---------------|--------------|
| Directory | `.claude/commands/` | `.claude/skills/` or `plugins/*/skills/` |
| File | `command-name.md` (flat file) | `skill-name/SKILL.md` (directory with optional references/) |
| Frontmatter | Minimal or none | YAML: `name`, `description`, `argument-hint`, `allowed-tools` |
| Invocation | `/command-name` | `/skill-name` or `/plugin:skill-name [args]` |
| Arguments | Not supported | `$ARGUMENTS` parsed by skill, `argument-hint` in frontmatter |
| Discovery | User-invocable only | `user-invocable` field controls `/` menu visibility |
| Context | Always main thread | `context: fork` for isolated execution |

Both formats still work at runtime (backwards compatible), but skills are the recommended pattern going forward. This skill helps migrate any codebase from commands to skills.

## Portability

This skill works in any repo:

- **Plugin repos** with `plugins/*/commands/` directories
- **Project repos** with `.claude/commands/` only
- **Mixed repos** with both project and plugin commands
- **Already-migrated repos** (audit/validate modes confirm health)

## Argument Routing

| Action | Description |
|--------|-------------|
| `discover` | Find all commands/ directories and legacy command files in the current repo |
| `analyze` | Map commands to skill consolidation groups and suggest naming |
| `migrate` | Execute the migration: create skill directories, convert files, update references |
| `audit` | Comprehensive post-migration health check using parallel agents |
| `validate` | Quick validation that no commands were lost in migration |
| `fix` | Auto-remediate findings from `audit` (stale refs, naming, missing frontmatter) |

Parse `$ARGUMENTS` to determine the action. Default to `discover` if no action specified.

### Action Workflow

The typical migration workflow is:

```text
discover -> analyze -> migrate -> audit -> fix (if needed) -> validate
```

For repos that have already been partially migrated:

```text
audit -> fix -> validate
```

---

## Action: discover

Scan the current repository for legacy command files and directories.

### Step 1: Find commands/ directories

Search for any `commands/` directories in the repo:

```text
Glob patterns to check:
  .claude/commands/**/*.md
  plugins/*/commands/**/*.md
  **/commands/**/*.md (broader sweep)
```

### Step 2: Identify command files

For each commands/ directory found, catalog every `.md` file:

- File name (without extension) = command name
- Check for YAML frontmatter (some commands had minimal frontmatter)
- Check for `$ARGUMENTS` usage (indicates argument-aware command)
- File size (helps estimate migration effort)
- Check if a corresponding skill already exists

### Step 3: Check for existing skills

For each command found, check if a skill with the same or similar name already exists:

```text
Check paths:
  .claude/skills/<command-name>/SKILL.md
  plugins/*/skills/<command-name>/SKILL.md
```

### Step 4: Report discovery results

Present a table summarizing findings:

```markdown
## Discovery Report

**Commands found:** N files across M directories

| # | Command | Location | Size | Has Frontmatter | Has $ARGUMENTS | Skill Exists |
|---|---------|----------|------|-----------------|----------------|--------------|
| 1 | deploy  | .claude/commands/deploy.md | 2.4 KB | Yes | No | No |
| 2 | test    | .claude/commands/test.md   | 1.1 KB | No  | No | No |

**Directories to migrate:**
- .claude/commands/ (N files)
- plugins/my-plugin/commands/ (M files)

**Already migrated:** K commands have corresponding skills
**Remaining:** J commands need migration
```

---

## Action: analyze

Analyze discovered commands and recommend consolidation groups and naming.

### Step 1: Run discover (if not already done)

If no discovery data exists in the conversation, run the discover action first.

### Step 2: Read each command file

For every command file found, read the content and extract:

- **Purpose**: What does this command do?
- **Domain**: What area does it belong to? (e.g., testing, deployment, docs)
- **Verb or noun**: Is the name a verb (imperative) or noun-phrase?
- **Related commands**: Are there other commands that operate on the same resource?
- **Complexity**: Simple (< 50 lines) vs complex (> 50 lines, multiple sections)

### Step 3: Identify consolidation opportunities

Group commands that share a domain and operate on the same resources:

**Consolidation candidates** (merge into one skill with argument routing):

```text
Example groups:
  deploy, deploy-staging, deploy-prod  ->  deployment <env>
  test-unit, test-e2e, test-lint       ->  testing <type>
  db-migrate, db-seed, db-reset        ->  database <action>
```

**Rename candidates** (verb-form -> noun-phrase):

```text
  run-tests      ->  test-runner
  deploy-app     ->  deployment
  check-types    ->  type-checking
  lint-code      ->  code-linting
  build-docs     ->  documentation-build
```

**Keep as-is** (already noun-phrase or standalone):

```text
  code-review    ->  code-review (already noun-phrase)
  onboarding     ->  onboarding (already noun-phrase)
```

### Step 4: Present analysis

```markdown
## Migration Analysis

### Consolidation Groups

| Group | Commands to Merge | Suggested Skill Name | Actions |
|-------|-------------------|---------------------|---------|
| Testing | test-unit, test-e2e, test-lint | `testing` | unit, e2e, lint |
| Deployment | deploy, deploy-staging | `deployment` | staging, prod |

### Renames (Verb -> Noun-Phrase)

| Current Name | Suggested Name | Reason |
|-------------|----------------|--------|
| run-tests | test-runner | Noun-phrase convention |
| build-docs | documentation-build | Noun-phrase convention |

### Keep As-Is

| Command | Reason |
|---------|--------|
| code-review | Already noun-phrase |
| onboarding | Already noun-phrase |

### Migration Plan Summary
- **Total commands:** N
- **Will consolidate:** M commands into K skills
- **Will rename:** J commands
- **Keep as-is:** L commands
- **Final skill count:** X skills (from N commands)
```

Ask the user to review and approve the plan before proceeding to migrate.

---

## Action: migrate

Execute the migration based on the analysis. This action creates skill directories, converts command files, and updates references.

### Prerequisites

- Run `analyze` first to have an approved migration plan
- Ensure working tree is clean (`git status` shows no uncommitted changes)
- If working tree is dirty, ask user to commit or stash first

### Step 1: Create skill directories

For each command being migrated:

```bash
# For standalone commands
mkdir -p .claude/skills/<skill-name>

# For plugin commands
mkdir -p plugins/<plugin>/skills/<skill-name>
```

### Step 2: Convert command files to SKILL.md

For each command file, create a proper SKILL.md:

#### 2a: Generate YAML frontmatter

```yaml
---
name: <skill-name>
description: "<one-line description of what this skill does>"
argument-hint: <hint based on $ARGUMENTS usage or consolidation>
allowed-tools: <infer from command content - Bash, Read, Write, etc.>
---
```

**Frontmatter inference rules:**

- `name`: Use the skill directory name (kebab-case, noun-phrase)
- `description`: Extract from first paragraph or heading of command file
- `argument-hint`: If command used `$ARGUMENTS`, preserve the pattern. If consolidating, add `<action>` routing
- `allowed-tools`: Scan command body for tool references (Bash, Read, Write, Glob, Grep, etc.)
- `user-invocable`: Default `true` unless command was clearly internal-only

#### 2b: Transform content

1. Copy command content as the skill body
2. If consolidating multiple commands, create an argument routing table
3. If command had references to other commands, update to skill references
4. Preserve any `references/` content

#### 2c: Handle consolidation

For consolidated skills (multiple commands -> one skill):

```markdown
## Argument Routing

| Action | Description |
|--------|-------------|
| `unit` | Run unit tests |
| `e2e` | Run end-to-end tests |
| `lint` | Run linter |

Parse `$ARGUMENTS` to determine the action. Default to `<most-common-action>` if no action specified.

---

## Action: unit

<content from old test-unit command>

---

## Action: e2e

<content from old test-e2e command>
```

### Step 3: Update references across the codebase

Search for and update stale references:

**Patterns to find and replace:**

| Find | Replace With |
|------|-------------|
| `.claude/commands/<name>.md` | `.claude/skills/<name>/SKILL.md` |
| `/old-command-name` (invocations) | `/new-skill-name` or `/new-skill-name <action>` |
| `commands/` directory references | `skills/` directory references |

**Files to search:**

- `CLAUDE.md` and any `.claude/` config files
- `README.md` and documentation files
- Memory files (`.claude/memory/`)
- Other skill files that cross-reference

**Exclusions (do NOT change):**

- Third-party documentation in `canonical/` directories
- References to external tools that genuinely use "commands" (Gemini CLI, Cursor, etc.)
- Historical audit logs
- This skill file itself

### Step 4: Verify migration

After all files are created and references updated:

1. Count new skills vs old commands (should match or consolidation explains difference)
2. Run `validate` action to confirm nothing was lost
3. Present migration summary to user

### Step 5: Clean up (with user approval)

Ask user before deleting old command files:

```text
Migration complete. N skills created from M commands.

The old commands/ directories still exist:
  .claude/commands/ (M files)

Delete the old commands/ directories? (The content has been migrated to skills/)
```

Only delete after explicit user approval.

---

## Action: audit

Comprehensive post-migration health check. Auto-discovers the repo structure (no hardcoded paths) and validates everything using parallel agents.

### How It Works

The audit dynamically discovers what exists in the repo:

1. **Auto-discover** all `commands/` and `skills/` directories
2. **Build old-to-new mapping** from git history (deleted commands -> current skills)
3. **Run 7 parallel checks** via agent team
4. **Compile structured report** with PASS/FAIL per check

### Checks Performed

#### Check 1: No commands/ directories remain

```bash
# Search for any commands/ directories in the repo
find . -type d -name "commands" -not -path "*/node_modules/*" \
  -not -path "*/.git/*" -not -path "*/canonical/*" 2>/dev/null
```

Expected: No output. If any remain, the migration is incomplete.

**Exclusions (do NOT flag):**

- `canonical/` directories (scraped third-party docs)
- `node_modules/` (dependencies)
- External tool references (Gemini CLI `~/.gemini/commands/`, Cursor, etc.)

#### Check 2: No stale deleted skill directories

If the repo has consolidation history, verify no orphaned skill directories remain from deleted/merged skills.

```bash
# Check git log for deleted skill directories
git log --all --diff-filter=D --name-only -- "*/skills/*/SKILL.md" 2>/dev/null | \
  grep "SKILL.md$" | sort -u
```

For each deleted skill, verify the directory no longer exists on disk.

#### Check 3: All skills have proper YAML frontmatter

For every `SKILL.md` found in the repo, validate:

- `name` field exists and matches directory name
- `description` field is non-empty
- `allowed-tools` field is non-empty
- `argument-hint` field exists (if skill body references `$ARGUMENTS`)
- No duplicate `name` values across skills (within same plugin)

Use Glob to find all SKILL.md files:

```text
.claude/skills/*/SKILL.md
plugins/*/skills/*/SKILL.md
```

#### Check 4: No stale invocation references

Search for old `/command-name` invocations that should now be `/skill-name`:

**Discovery approach:**

1. Build the list of deleted command names from git history
2. Search all `.md` files for `/deleted-command-name\b` patterns
3. Exclude: `canonical/`, `.prompts/`, agent names (e.g., `user-config-auditor`), external CLI flags, Python variables, audit logs

**Files to search:**

- `.claude/` (memory, config)
- `plugins/` (skills, agents, hooks)
- `CLAUDE.md`, `README.md`

#### Check 5: No stale path references

Search for `commands/` path references that should be `skills/`:

```text
Grep pattern: \.claude/commands/
Scope: all .md files
Exclusions: canonical/, external tools (Gemini, Cursor, Codex), TAC plugin
```

Also check for `plugins/*/commands/` path references.

#### Check 6: Naming convention compliance

Auto-detect naming convention issues:

- Scan all skill directory names
- Flag imperative verb names (e.g., `deploy-app` should be `deployment`)
- Check `name` frontmatter matches directory name
- Common verb prefixes to flag: `run-`, `create-`, `build-`, `deploy-`, `setup-`, `check-`, `manage-`, `audit-`, `prep-`, `get-`, `set-`, `make-`
- Report as WARNING (not FAIL) since some imperative names are intentional exceptions

#### Check 7: Completeness -- no commands lost

Build old-to-new mapping from git history:

```bash
# Find all historically deleted command files
git log --all --diff-filter=D --name-only -- \
  ".claude/commands/*.md" "plugins/*/commands/*.md" 2>/dev/null | \
  grep "\.md$" | sort -u

# Also find commands that still exist (not yet migrated)
find . -path "*/commands/*.md" -not -path "*/canonical/*" \
  -not -path "*/node_modules/*" 2>/dev/null
```

For each old command, verify a corresponding skill exists:

- Exact name match: `deploy` -> `skills/deploy/SKILL.md`
- Noun-form match: `deploy-app` -> `skills/deployment/SKILL.md`
- Consolidated match: `test-unit` -> `skills/testing/SKILL.md` (check argument routing)

### Audit Execution: Agent Team

Create a team named `migration-audit-<timestamp>` with parallel agents:

| Agent | Checks | Agent Type | Description |
|-------|--------|------------|-------------|
| fs-checker | 1, 2 | Bash | Filesystem integrity: no stale dirs |
| frontmatter-auditor | 3 | general-purpose | YAML frontmatter validation |
| reference-scanner | 4, 5 | general-purpose | Stale invocation and path refs |
| naming-auditor | 6 | general-purpose | Naming convention compliance |
| completeness-auditor | 7 | general-purpose | No commands lost |

**Dependencies:** All 5 agents run in parallel. No dependencies between them.

After all agents complete, compile the report in the main thread.

### Audit Report Template

```markdown
# Migration Audit Report

**Date:** <current date>
**Repository:** <repo name>
**Commit:** <current HEAD>

## Summary

| Check | Status | Details |
|-------|--------|---------|
| 1. No commands/ dirs | PASS/FAIL | N found |
| 2. No stale skill dirs | PASS/FAIL | N stale |
| 3. Frontmatter valid | PASS/FAIL | N/M valid |
| 4. No stale invocations | PASS/FAIL | N stale refs |
| 5. No stale path refs | PASS/FAIL | N stale refs |
| 6. Naming conventions | PASS/WARN/FAIL | N/M compliant |
| 7. Completeness | PASS/FAIL | N/M mapped |

## Findings

(Detail any failures with file:line and suggested fix)

## Recommendation

[ ] All checks pass - migration is complete
[ ] Fixes needed - run `/skill-migration fix` to auto-remediate
[ ] Manual intervention needed - see findings above
```

---

## Action: fix

Auto-remediate findings from `audit`. Run this after `audit` identifies issues.

### Prerequisites

- Run `audit` first to identify what needs fixing
- Audit findings should be in the conversation context
- Working tree should be clean (commit or stash first)

### Fix Categories

#### Fix 1: Stale commands/ directories

If `commands/` directories still exist with content:

1. For each command file in the directory, check if a corresponding skill exists
2. If skill exists: the command is redundant -- delete the command file
3. If skill does NOT exist: run a mini-migration for that single command
4. After all files handled, delete the empty `commands/` directory

```bash
# Verify directory is empty before deleting
rmdir <commands-dir>  # Fails safely if not empty
```

#### Fix 2: Missing YAML frontmatter

For skills missing required frontmatter fields:

1. Read the SKILL.md content
2. Infer missing fields:
   - `name`: from directory name
   - `description`: from first heading/paragraph
   - `allowed-tools`: from content patterns (see inference table below)
   - `argument-hint`: from `$ARGUMENTS` usage
3. Add or update the YAML frontmatter block

**IMPORTANT:** Always show the user what frontmatter will be added before writing.

#### Fix 3: Stale invocation references

For each stale `/old-command-name` reference:

1. Read the file containing the stale reference
2. Determine the correct replacement:
   - Simple rename: `/old-name` -> `/new-name`
   - Consolidation: `/test-unit` -> `/testing unit`
   - Plugin-scoped: `/scrape-docs` -> `/docs-ops scrape`
3. Use Edit tool to replace the reference
4. Verify the replacement is correct by re-reading the file

#### Fix 4: Stale path references

For each `commands/` path reference:

1. Replace `.claude/commands/<name>.md` with `.claude/skills/<name>/SKILL.md`
2. Replace `plugins/*/commands/` with `plugins/*/skills/`
3. Preserve any path that references external tools (Gemini, Cursor, etc.)

#### Fix 5: Naming convention violations

For imperative verb skill names:

1. Present suggested noun-phrase rename to user
2. If user approves:
   - Rename the skill directory
   - Update the `name` frontmatter field
   - Update all references to the old name
3. If user declines: document as intentional exception

### Fix Execution

Apply fixes sequentially (not parallel) since fixes may affect each other:

```text
1. Fix stale directories (Check 1 findings)
2. Fix missing frontmatter (Check 3 findings)
3. Fix stale invocations (Check 4 findings)
4. Fix stale paths (Check 5 findings)
5. Fix naming (Check 6 findings) -- ask user per rename
6. Re-run validate to confirm nothing was lost
```

### Fix Report

After all fixes applied:

```markdown
## Fix Report

**Fixes applied:** N
**Manual intervention needed:** M

| # | Category | File | Action Taken |
|---|----------|------|-------------|
| 1 | Stale dir | .claude/commands/ | Deleted (all content migrated) |
| 2 | Frontmatter | .claude/skills/deploy/SKILL.md | Added name, description, allowed-tools |
| 3 | Stale ref | CLAUDE.md:42 | /deploy-staging -> /deployment staging |

**Re-validation result:** PASS/FAIL
```

---

## Action: validate

Quick validation that no commands were lost. Lighter than `audit` -- focuses only on completeness.

### Step 1: Inventory old commands

Find all command files that exist or have been tracked by git:

```bash
# Current commands (if any remain)
find .claude/commands -name "*.md" 2>/dev/null
find plugins/*/commands -name "*.md" 2>/dev/null

# Historical commands (from git history)
git log --all --diff-filter=D --name-only -- \
  ".claude/commands/*.md" "plugins/*/commands/*.md" 2>/dev/null | \
  grep "\.md$" | sort -u
```

### Step 2: Inventory current skills

```bash
# Project skills
find .claude/skills -maxdepth 2 -name "SKILL.md" 2>/dev/null

# Plugin skills
find plugins/*/skills -maxdepth 2 -name "SKILL.md" 2>/dev/null
```

### Step 3: Map old to new

For each old command, check if a corresponding skill exists:

- Exact name match: `deploy` -> `.claude/skills/deploy/SKILL.md`
- Consolidated match: `test-unit` -> `.claude/skills/testing/SKILL.md` (with `unit` action)
- Renamed match: `run-tests` -> `.claude/skills/test-runner/SKILL.md`
- Plugin match: `plugins/foo/commands/bar.md` -> `plugins/foo/skills/bar/SKILL.md`

### Step 4: Report

```markdown
## Validation Report

**Old commands found:** N (current) + M (deleted from git history)
**Current skills found:** K (project) + J (plugin)

| Old Command | Location | Current Skill | Status |
|------------|----------|---------------|--------|
| deploy | .claude/commands/ | deployment | FOUND |
| test-unit | .claude/commands/ | testing (unit action) | FOUND |
| run-tests | .claude/commands/ | test-runner | FOUND |
| unknown-cmd | .claude/commands/ | ??? | MISSING |

**Result:** N/M commands accounted for
```

---

## Naming Convention Reference

When migrating, follow these naming patterns:

### Verb -> Noun-Phrase Conversions

| Verb Form (Old) | Noun-Phrase (New) | Pattern |
|-----------------|-------------------|---------|
| `run-tests` | `test-runner` | verb-noun -> noun-agent |
| `deploy-app` | `deployment` | verb-noun -> nominalization |
| `build-docs` | `documentation-build` | verb-noun -> noun-noun |
| `check-types` | `type-checking` | verb-noun -> gerund |
| `lint-code` | `code-linting` | verb-noun -> gerund |
| `create-user` | `user-creation` | verb-noun -> nominalization |
| `manage-config` | `config-management` | verb-noun -> management |
| `audit-security` | `security-auditing` | verb-noun -> gerund |
| `setup-env` | `environment-setup` | verb-noun -> noun-noun |
| `prep-interview` | `interview-skills` | verb-noun -> noun-skills |

### Consolidation Patterns

| Pattern | Example | When to Use |
|---------|---------|-------------|
| `<resource> <action>` | `/user-config audit` | Multiple actions on same resource |
| `<domain> <mode>` | `/testing unit` | Related but distinct operations |
| `<tool> <subcommand>` | `/docs-ops scrape` | Lifecycle management of a resource |

### Exceptions (Imperative Names OK)

Some skill names are intentionally imperative when the action IS the skill:

- `track-win` - The action of tracking is the skill
- `plan-career-goals` - Planning is the core activity
- `push` - Direct git operation

---

## Frontmatter Template

Every migrated skill needs this YAML frontmatter:

```yaml
---
name: <skill-directory-name>
description: "<concise description of what this skill does>"
argument-hint: <action> [options]  # Only if skill accepts arguments
allowed-tools: Bash, Read, Write  # Tools this skill needs
user-invocable: true  # Set false for model-only skills
---
```

### allowed-tools Inference

Scan the command body to determine which tools the skill needs:

| Content Pattern | Inferred Tool |
|-----------------|---------------|
| `bash`, `shell`, `run`, `execute`, backtick code blocks | `Bash` |
| `read`, `file`, `cat` references | `Read` |
| `write`, `create file`, `save` references | `Write` |
| `edit`, `modify`, `replace` references | `Edit` |
| `find`, `glob`, `search files` | `Glob` |
| `grep`, `search content` | `Grep` |
| `agent`, `task`, `parallel` | `Task` |
| `ask`, `prompt`, `question` | `AskUserQuestion` |
| `skill`, `invoke`, `/skill-name` | `Skill` |
| `web`, `fetch`, `url` | `WebFetch` |
