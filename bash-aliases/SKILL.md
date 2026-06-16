---
name: bash-aliases
description: Manage git and Claude Code bash aliases. Run without flags for interactive wizard.
argument-hint: "[--setup] | --status | --audit | --uninstall"
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion
---

# Bash Aliases Management

Manage git shortcuts (g, gco, gb, etc.) and Claude Code aliases (claude-yolo, claude-cont, etc.) with bash tab completion.

## Usage

```text
/git:bash-aliases                # Interactive setup wizard
/git:bash-aliases --setup        # Same as above
/git:bash-aliases --status       # Check installation status
/git:bash-aliases --audit        # Comprehensive health check
/git:bash-aliases --uninstall    # Show uninstall instructions
```

## Workflow

### Step 1: Parse Arguments

Parse `$ARGUMENTS` to determine operation mode:

- **No arguments or `--setup`** -> Interactive mode (Step 2)
- **Direct flag** (`--status`, `--audit`, `--uninstall`) -> Direct mode (Step 3)

### Step 2: Interactive Mode (no flag or --setup)

Use AskUserQuestion to let user select alias sets:

```text
Use AskUserQuestion with:
- question: "Which bash aliases do you want to install?"
- header: "Alias Sets"
- multiSelect: true
- options:
  1. "Git aliases" - "Shortcuts (g, gco, gb, gm, etc.) with tab completion"
  2. "Claude aliases" - "Claude Code shortcuts (claude-yolo, claude-cont, etc.)"
```

Based on user selections, execute corresponding script operations:

- Git aliases selected -> Run script with `--install-git-aliases`
- Claude aliases selected -> Run script with `--install-claude-aliases`

Report aggregate results.

### Step 3: Direct Mode

Execute the script with the specified flag:

| Flag | Script Operation |
| ---- | ---------------- |
| `--status` | `--status` |
| `--audit` | `--audit` |
| `--uninstall` | `--uninstall` |

### Step 4: Report Results

Show operation results to user. Include next steps if applicable:

- After install: "Run `source ~/.bashrc` or restart your shell"
- For audit warnings: Suggest remediation

## Script Location

The underlying bash script is at:

```text
plugins/git/skills/setup/scripts/bash-aliases.sh
```

Execute using:

```bash
bash "plugins/git/skills/setup/scripts/bash-aliases.sh" <operation>
```

## Alias Sets

### Git Aliases

Common shortcuts with tab completion:

| Alias | Command |
| ----- | ------- |
| `g` | `git` |
| `gs` | `git status` |
| `gco` | `git checkout` |
| `gb` | `git branch` |
| `gm` | `git merge` |
| `gp` | `git pull` |
| `gps` | `git push` |
| `gd` | `git diff` |
| `gl` | `git log --oneline --graph --decorate` |
| `gst` | `git stash` |
| `ga` | `git add` |
| `gcm` | `git commit` |
| `gr` | `git rebase` |
| `gcp` | `git cherry-pick` |

### Claude Code Aliases

| Alias | Command |
| ----- | ------- |
| `claude-cont` | `claude -c` |
| `claude-cont-yolo` | `claude -c --dangerously-skip-permissions` |
| `claude-yolo` | `claude --dangerously-skip-permissions` |
| `claude-plan` | `claude --permission-mode plan` |
| `claude-opus` | `claude --model opus` |
| `claude-sonnet` | `claude --model sonnet` |
| `claude-opus-yolo` | `claude --model opus --dangerously-skip-permissions` |
| `claude-headless` | `claude -p --output-format json` |

## Examples

### Interactive Setup

```text
/git:bash-aliases
-> "Which bash aliases do you want to install?"
  [x] Git aliases
  [x] Claude aliases
-> Installing selected alias sets...
-> Done! Run: source ~/.bashrc
```

### Check Status

```text
/git:bash-aliases --status

Bash Aliases Status
-------------------

Git Aliases:
[OK] Configured in ~/.bashrc
    Aliases: g, gs, gco, gb, gm, gp, gps, gd, gl, gst, ga, gcm, gr, gcp

Claude Code Aliases:
[OK] Configured in ~/.bashrc
    Aliases: claude-cont, claude-yolo, claude-plan, claude-opus, claude-sonnet
```

### Audit

```text
/git:bash-aliases --audit

Bash Aliases Audit Report
=========================
[OK] Git aliases: PASS - Configured
[OK] git-completion.bash: PASS - Found
[OK] Claude aliases: PASS - Configured
[OK] claude CLI: PASS - Found

Overall: PASS
```

## Notes

- Aliases are added to ~/.bashrc with idempotent markers
- Git aliases include tab completion via git-completion.bash
- Safe to run multiple times (won't duplicate entries)
- Requires `source ~/.bashrc` or new shell to take effect
