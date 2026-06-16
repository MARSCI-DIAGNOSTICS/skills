---
name: kiro-sync
description: "Synchronize specifications with AWS Kiro format (requirements.md, design.md, tasks.md)."
argument-hint: "<spec file or directory> [--direction import|export|bidirectional]"
allowed-tools: Read, Glob, Grep, Write, Edit, Skill, Task
---

# Kiro Specification Sync

Synchronize specifications with AWS Kiro IDE format.

## Kiro File Structure

AWS Kiro uses a specific file structure:

```text
.kiro/
├── steering/
│   ├── requirements.md    # Project-wide requirements
│   ├── design.md          # Overall design
│   └── tasks.md           # Current tasks
├── specs/
│   └── {feature-name}/
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
└── kiro.json              # Configuration
```

## Sync Directions

| Direction | Description |
| --- | --- |
| `import` | Kiro → Canonical (read from Kiro) |
| `export` | Canonical → Kiro (write to Kiro) |
| `bidirectional` | Two-way sync with conflict detection |

## Workflow

1. **Detect Structure**
   - Check for existing .kiro/ directory
   - Identify canonical specifications
   - Determine sync direction

2. **Execute Sync**
   - Spawn `spec-converter kiro` agent
   - Compare content hashes
   - Identify changes

3. **Handle Conflicts**
   - If bidirectional and both changed:
     - Flag conflicts
     - Present diff
     - Prompt for resolution

4. **Apply Changes**
   - Write updated files
   - Preserve formatting
   - Update timestamps

5. **Report**
   - Show sync summary
   - List changes made
   - Note any conflicts

## Arguments

- `$1` - Specification file or .kiro/ directory
- `--direction` - Sync direction: import, export, bidirectional (default)
- `--force` - Overwrite without conflict check
- `--dry-run` - Show what would change without writing

## Examples

```bash
# Export canonical to Kiro
/spec-driven-development:kiro-sync .specs/auth/spec.md --direction export

# Import from Kiro
/spec-driven-development:kiro-sync .kiro/specs/auth/ --direction import

# Bidirectional sync
/spec-driven-development:kiro-sync .specs/auth/spec.md

# Dry run to see changes
/spec-driven-development:kiro-sync .specs/auth/spec.md --dry-run
```

## Mapping: Canonical ↔ Kiro

### requirements.md

| Canonical | Kiro |
| --- | --- |
| Problem Statement | Context |
| Scope | Context/Scope |
| FR-X | REQ-X |
| NFR-X | REQ-NX |
| AC-X.Y | AC-X.Y |

### design.md

| Canonical | Kiro |
| --- | --- |
| Design Overview | Overview |
| Components | Components |
| Data Model | Data Model |
| API Design | API Design |

### tasks.md

| Canonical | Kiro |
| --- | --- |
| Task List | Task List |
| TASK-X | TASK-X |
| Dependencies | Dependency graph |

## EARS Compatibility

Kiro uses EARS syntax natively, so requirements pass through unchanged:

**Canonical:**

```markdown
## FR-1: User Login

WHEN the user submits valid credentials,
the system SHALL authenticate the user.
```

**Kiro (requirements.md):**

```markdown
### REQ-1: User Login

WHEN the user submits valid credentials,
the system SHALL authenticate the user.
```

Only the ID prefix changes (FR-X → REQ-X).

## Sync Report

```markdown
# Kiro Sync Report

**Direction:** Bidirectional
**Timestamp:** 2024-01-15T10:30:00Z

## Summary

| Type | Added | Updated | Unchanged | Conflicts |
| --- | --- | --- | --- | --- |
| Requirements | 1 | 2 | 5 | 0 |
| Design | 0 | 1 | 0 | 0 |
| Tasks | 3 | 0 | 2 | 0 |

## Changes

### Added
- REQ-8 (new requirement in canonical)

### Updated
- REQ-2: Updated acceptance criteria
- REQ-5: Clarified EARS statement

## Generated Files

- .kiro/specs/auth/requirements.md (updated)
- .kiro/specs/auth/design.md (updated)
- .kiro/specs/auth/tasks.md (created)
```

## Related Commands

- `/spec-driven-development:convert` - General format conversion
- `/spec-driven-development:speckit-run` - Full Spec Kit workflow
- `/spec-driven-development:specify` - Generate specification
