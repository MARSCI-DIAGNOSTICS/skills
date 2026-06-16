# Fix Workflow and Git Staging Behavior

This reference documents the standard behavior for agents and commands that apply code fixes.

## Core Principle: Unstaged by Default

**All code fixes must leave changes unstaged by default.**

When an agent or command applies fixes via Edit tool:

- Files remain in "Changes not staged for commit" state
- User can review changes with `git diff` before staging
- Prevents unreviewed AI-applied code from being accidentally committed

## Why This Matters

1. **User control**: Users must review AI-applied changes before committing
2. **Safety**: Prevents accidental inclusion of broken or incomplete fixes
3. **Transparency**: Clear separation between "changed" and "ready to commit"
4. **Workflow fit**: Integrates with standard git review workflows

## The `--auto-stage` Flag

Commands that apply fixes SHOULD support an `--auto-stage` flag:

| Flag | Behavior |
| --- | --- |
| (default, no flag) | Leave files unstaged after fixes |
| `--auto-stage` | Stage fixed files with `git add` after verification |

### When Auto-Stage is Appropriate

Only use `--auto-stage` when:

- All fixes have been verified (tests pass, no regressions)
- User explicitly requests automatic staging
- The workflow is part of an automated pipeline

### Implementation Pattern

```text
1. Apply fix via Edit tool
2. Run verification (tests, build, etc.)
3. If verification fails:
   - Report failure
   - Leave files unstaged
   - Exit
4. If verification passes AND --auto-stage:
   - Run: git add <fixed-files>
   - Report which files were staged
5. If verification passes AND no --auto-stage:
   - Report files as "modified (unstaged)"
   - Suggest: "Review with `git diff` then stage manually"
```

## Output Format

Always include git status in output when fixes are applied:

### Without `--auto-stage`

```markdown
### Git Status

**Modified files** (unstaged - review with `git diff`):
- `path/to/fixed-file-1.ext`
- `path/to/fixed-file-2.ext`

To stage after review:
git add path/to/fixed-file-1.ext path/to/fixed-file-2.ext
```

### With `--auto-stage`

```markdown
### Git Status

**Staged files** (ready to commit):
- `path/to/fixed-file-1.ext`
- `path/to/fixed-file-2.ext`

To commit:
git commit -m "fix: [description of fixes]"
```

## Commands and Agents Using This Pattern

| Component | Type | Fix Capability | `--auto-stage` Support |
| --- | --- | --- | --- |
| `debugger` | Agent | Yes (Edit tool) | Via invoking command |
| `/code-quality:debug` | Command | Yes (delegates to debugger) | Yes |
| `code-reviewer` | Agent | No (plan mode) | N/A |
| `/code-quality:review` | Command | No (read-only) | N/A |

## Future: Code Review Fix Mode

If a fix mode is added to code review in the future:

1. Create new agent with Edit capability (not plan mode)
2. Add `--fix` flag to `/code-quality:review` command
3. Support `--auto-stage` to control staging behavior
4. Default behavior: unstaged (user reviews fixes)

Example future usage:

```bash
# Review and apply fixes, leave unstaged (user reviews)
/code-quality:review staged --fix

# Review, apply fixes, and stage (automated pipeline)
/code-quality:review staged --fix --auto-stage
```

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Correct Approach |
| --- | --- | --- |
| Auto-stage without flag | User loses control | Always require explicit `--auto-stage` |
| Stage before verification | Broken code gets staged | Verify first, then stage if requested |
| Silent staging | User doesn't know what happened | Always report what was staged |
| No git status in output | User can't see what changed | Include git status section |

---

**Last Updated:** 2025-12-29
