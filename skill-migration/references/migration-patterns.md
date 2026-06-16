# Migration Patterns Reference

Common patterns encountered when migrating from `.claude/commands/` to `.claude/skills/`.

## Pattern 1: Simple 1:1 Migration

**Before:** `.claude/commands/code-review.md`

```markdown
# Code Review

Review the current git diff for issues...
```

**After:** `.claude/skills/code-review/SKILL.md`

```yaml
---
name: code-review
description: Review code changes for bugs, style issues, and best practices.
allowed-tools: Bash, Read, Glob, Grep
---

# Code Review

Review the current git diff for issues...
```

**Steps:** Create directory, add frontmatter, copy content.

## Pattern 2: Consolidation (N commands -> 1 skill)

**Before:**

- `.claude/commands/test-unit.md`
- `.claude/commands/test-e2e.md`
- `.claude/commands/test-lint.md`

**After:** `.claude/skills/testing/SKILL.md`

```yaml
---
name: testing
description: "Run project tests. Actions: unit, e2e, lint, all."
argument-hint: <action> (unit|e2e|lint|all)
allowed-tools: Bash, Read, Glob
---

# Testing

## Argument Routing

| Action | Description |
|--------|-------------|
| `unit` | Run unit tests |
| `e2e` | Run end-to-end tests |
| `lint` | Run linter checks |
| `all` | Run all test suites |

Parse `$ARGUMENTS` to determine the action. Default to `all`.

---

## Action: unit

<content from test-unit.md>

---

## Action: e2e

<content from test-e2e.md>
```

**When to consolidate:** Commands share a domain and operate on the same resource type.

## Pattern 3: Verb -> Noun Rename

**Before:** `.claude/commands/deploy-staging.md`

**After:** `.claude/skills/deployment/SKILL.md`

The rename follows the noun-phrase convention:

- `deploy-staging` (imperative verb) -> `deployment` (noun-phrase)
- Command body stays the same, just wrapped in proper SKILL.md structure
- If there are multiple deploy commands, consolidate with argument routing

## Pattern 4: Command with $ARGUMENTS

Commands that already use `$ARGUMENTS` translate directly:

**Before:** `.claude/commands/search.md`

```markdown
# Search

Search the codebase for: $ARGUMENTS
```

**After:** `.claude/skills/search/SKILL.md`

```yaml
---
name: search
description: Search the codebase for patterns and code.
argument-hint: <query> [--type <filetype>]
allowed-tools: Grep, Glob, Read
---

# Search

Search the codebase for: $ARGUMENTS
```

The `argument-hint` field provides autocomplete guidance in the CLI.

## Pattern 5: Command with References

If a command references other files, create a `references/` subdirectory:

**Before:**

- `.claude/commands/setup.md` (references `setup-checklist.md`)
- `.claude/commands/setup-checklist.md`

**After:**

- `.claude/skills/setup/SKILL.md`
- `.claude/skills/setup/references/checklist.md`

Update internal references from `setup-checklist.md` to `references/checklist.md`.

## Pattern 6: Plugin Commands

Plugin commands follow the same pattern but live under the plugin:

**Before:** `plugins/my-plugin/commands/my-cmd.md`

**After:** `plugins/my-plugin/skills/my-cmd/SKILL.md`

The invocation changes from `/my-cmd` to `/my-plugin:my-cmd`.

## Reference Update Patterns

After migration, update references across the codebase:

| Context | Old Pattern | New Pattern |
|---------|------------|-------------|
| CLAUDE.md | `.claude/commands/deploy.md` | `.claude/skills/deployment/SKILL.md` |
| Invocation | `/deploy-staging` | `/deployment staging` |
| Memory files | `commands/` directory ref | `skills/` directory ref |
| Cross-references | `See /test-unit` | `See /testing unit` |
| Documentation | "slash commands" | "skills" |

## Pattern 7: Large-Scale Consolidation (20+ commands -> 1 skill)

For repos with many commands operating on the same resource:

**Before:**

- `.claude/commands/user-config-audit.md`
- `.claude/commands/user-config-backup.md`
- `.claude/commands/user-config-reset.md`
- ... (20+ more)

**After:** `.claude/skills/user-config/SKILL.md`

```yaml
---
name: user-config
description: "Manage Claude user configuration. Actions: audit, backup, reset, ..."
argument-hint: <action> (audit|backup|reset|...) [options]
allowed-tools: Bash, Read, Write, Glob
---
```

With argument routing table listing all 20+ actions. Each action section contains the original command content.

**When to use:** 5+ commands share a resource prefix (e.g., `user-config-*`, `db-*`, `deploy-*`).

## Pattern 8: Delegation Chain Preservation

If commands delegate to meta-skills or shared utilities:

**Before:**

```text
/scrape-docs -> calls scripts/scrape.sh directly
```

**After:**

```text
/docs-ops scrape -> delegates to docs-management skill -> scripts
```

Never bypass delegation chains during migration. If the old command called a script directly, and a meta-skill now wraps that script, delegate through the meta-skill.

## Pattern 9: External Repo Migration

When migrating a repo that installed this plugin (not the plugin repo itself):

1. The repo has `.claude/commands/` with project-specific commands
2. The plugin provides skills via `plugins/*/skills/`
3. Migration only touches `.claude/commands/` -> `.claude/skills/`
4. Plugin skills remain untouched

**Key difference:** External repos typically have simpler structures (no plugins/ directory, just `.claude/commands/`).

## Common Pitfalls

1. **Don't delete commands/ before verifying skills work** - Test the new skills first
2. **Don't forget to update CLAUDE.md** - Often has command references
3. **Don't consolidate unrelated commands** - Only merge commands sharing a domain
4. **Don't lose references/ content** - Carry over any supporting files
5. **Don't change external references** - Other tools (Gemini, Cursor) may legitimately use "commands"
6. **Don't rename too aggressively** - If a verb name is well-established, document the exception
7. **Don't hardcode paths in the audit** - Use discovery (glob/find) instead of listing specific skill names
8. **Don't forget git history** - Use `git log --diff-filter=D` to find deleted commands for completeness checks
9. **Don't migrate in a dirty working tree** - Commit or stash first so migration changes are isolated
10. **Don't skip the analyze step** - Rushing to migrate without analyzing consolidation opportunities creates duplicate skills

## Repo Size Estimation

Use this to estimate migration effort:

| Commands | Estimated Effort | Approach |
|----------|-----------------|----------|
| 1-5 | 5 minutes | Manual 1:1 migration |
| 6-20 | 15-30 minutes | Semi-automated with analyze step |
| 21-50 | 30-60 minutes | Full workflow with consolidation |
| 50-100 | 1-2 hours | Team-based parallel migration |
| 100+ | 2-4 hours | Phased migration with intermediate commits |
