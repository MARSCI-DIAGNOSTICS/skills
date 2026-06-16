# Git Worktrees for Parallel Sessions

## Overview

Claude Desktop uses Git worktrees to enable **parallel local sessions** in the same repository. Each session gets its own isolated working directory.

## How It Works

1. You start a new local session in Claude Desktop
2. Desktop creates a Git worktree for that session
3. Each session operates independently
4. Changes are isolated until committed and merged

## Requirements

**CRITICAL:** The folder must have **Git initialized**.

- If a folder doesn't have Git initialized, Desktop **will not create a worktree**
- Initialize Git with `git init` before using parallel sessions

## Default Location

**Worktrees are stored in:** `~/.claude-worktrees`

This location is configurable in Desktop settings.

## .worktreeinclude File

The `.worktreeinclude` file specifies which `.gitignore`d files should be **copied** to new worktrees.

### Why This Matters

When you create a worktree, Git doesn't copy files that are in `.gitignore`. But you often need files like `.env` for your application to work.

### File Location

Create `.worktreeinclude` in your **project root** (same level as `.gitignore`).

### Pattern Syntax

Uses `.gitignore`-style patterns:

```gitignore
# Environment files
.env
.env.local
.env.development
.env.production
.env.*

# Claude settings
**/.claude/settings.local.json

# Certificates and keys
*.pem
*.key

# Local configuration
config.local.json
secrets.json
```

### Rules

1. **Patterns must match files in `.gitignore`**
   - Only files matched by BOTH `.worktreeinclude` AND `.gitignore` are copied
   - This prevents accidentally duplicating tracked files

2. **Pattern matching**
   - `*` matches any characters except `/`
   - `**` matches any path including `/`
   - `?` matches single character

### Common Patterns

| Pattern | Matches |
| --- | --- |
| `.env` | Exact file `.env` |
| `.env.*` | `.env.local`, `.env.production`, etc. |
| `**/.env` | `.env` in any subdirectory |
| `*.local.json` | Any file ending in `.local.json` |
| `**/.claude/*` | All files in any `.claude` folder |

### Example .worktreeinclude

```gitignore
# Environment variables (most common)
.env
.env.local
.env.*

# Claude local settings
**/.claude/settings.local.json

# Database seeds (if gitignored)
seeds/*.sql

# Local SSL certificates
certs/*.pem
```

## Best Practices

### Do

- Keep `.worktreeinclude` minimal
- Only include files necessary for the app to run
- Document why each pattern is needed (comments)
- Test that patterns work by creating a new session

### Do Not

- Include large binary files
- Include files that vary per-developer
- Include credentials that should stay per-machine
- Use overly broad patterns (`**/*`)

## Workflow Example

```bash
# 1. Initialize Git (if not already)
git init

# 2. Create .worktreeinclude
echo ".env" > .worktreeinclude
echo ".env.*" >> .worktreeinclude
echo "**/.claude/settings.local.json" >> .worktreeinclude

# 3. Add to Git (the .worktreeinclude file itself)
git add .worktreeinclude
git commit -m "Add worktreeinclude for parallel sessions"

# 4. Start parallel sessions in Claude Desktop
# Each session will get copies of your .env files
```

## Troubleshooting

| Issue | Solution |
| --- | --- |
| Worktree not created | Ensure Git is initialized (`git init`) |
| .env not copied | Check pattern in `.worktreeinclude` AND that file is in `.gitignore` |
| Too many files copied | Make patterns more specific |
| Worktrees filling disk | Configure different location or clean old worktrees |

## Related Topics

- [Setup Guide](setup-guide.md) - Installation and basic configuration
- [Troubleshooting](troubleshooting.md) - Common issues
