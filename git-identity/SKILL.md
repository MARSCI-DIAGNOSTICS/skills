---
name: git-identity
description: Multi-identity Git configuration with directory-scoped isolation. Sets up per-directory user email, GPG signing keys, and SSH keys using includeIf conditional includes. Use when configuring work vs personal Git identities, fixing "Unverified" commits from email/GPG key mismatch, setting up multiple GitHub accounts on one machine, auditing identity isolation, or troubleshooting includeIf, GPG key selection, or SSH key routing issues.
allowed-tools: Read, Bash, Glob, Grep
---

# Git Multi-Identity Configuration

Directory-scoped Git identity isolation: automatic email, GPG key, and SSH key selection based on repository location.

## Table of Contents

- [Overview](#overview)
- [When to Use This Skill](#when-to-use-this-skill)
- [Gather User Details First](#gather-user-details-first)
- [Quick Start](#quick-start)
- [Setup](#setup)
- [Audit](#audit)
- [Troubleshoot](#troubleshoot)
- [Architecture](#architecture)
- [Related Skills](#related-skills)
- [Version History](#version-history)

## Overview

Multi-identity isolation solves the problem of using different Git identities (email, GPG key, SSH key) across different contexts on the same machine. Instead of manually switching configuration or setting per-repo overrides, `includeIf` conditional includes automatically apply the correct identity based on which directory a repository lives in.

**What this provides:**

- Automatic `user.email` and `user.name` per directory tree
- Automatic GPG signing key selection per identity
- Automatic SSH key routing per identity (multiple GitHub accounts)
- Zero manual switching -- commit in any repo and the correct identity applies

## When to Use This Skill

- Setting up work vs personal Git identities on the same machine
- Configuring multiple GitHub/GitLab accounts with different SSH keys
- Fixing "Unverified" commits caused by email/GPG key mismatch
- Auditing that identity isolation is working correctly across directories
- Troubleshooting `includeIf` not matching, wrong GPG key used, or SSH "permission denied"
- Adding a new identity (new employer, new open-source persona)

## Gather User Details First

**Before executing any setup commands**, use `AskUserQuestion` to collect the user's specific details. Every identity setup is unique -- do not assume directory paths, email addresses, or identity names.

**Required information per identity:**

1. **Identity name** (e.g., "work", "personal", "freelance", "open-source")
2. **Directory path** where repos for this identity live (e.g., `~/Projects/work/`)
3. **Git email** for this identity
4. **Git name** (if different per identity, or one shared name)
5. **GPG signing?** Whether they want GPG signing (and whether keys already exist)
6. **SSH key routing?** Whether they need separate SSH keys per identity (e.g., multiple GitHub accounts)
7. **Platform** (Windows, macOS, Linux) -- determines `gitdir:` vs `gitdir/i:` syntax

**Example AskUserQuestion flow:**

- "How many Git identities do you need? What are their names (e.g., work, personal)?"
- "What directory contains your [identity] repositories?"
- "What email address should be used for [identity] commits?"
- "Do you already have GPG keys for each identity, or should we generate them?"
- "Do you use multiple GitHub/GitLab accounts (requiring separate SSH keys)?"

Only proceed with setup commands after collecting these details. Replace all placeholder values in the examples below with the user's actual values.

## Quick Start

Minimal end-to-end setup for two identities (work + personal):

```bash
# 1. Create directory-scoped gitconfig files
cat > ~/.gitconfig-work << 'EOF'
[user]
    email = jane@acme-corp.com
    signingkey = <WORK_GPG_KEY_ID>
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_work
EOF

cat > ~/.gitconfig-personal << 'EOF'
[user]
    email = jane@example.com
    signingkey = <PERSONAL_GPG_KEY_ID>
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_personal
EOF

# 2. Add includeIf directives to ~/.gitconfig
# (Windows: use gitdir/i: for case-insensitive matching)
git config --global --add includeIf."gitdir/i:C:/Projects/work/".path ~/.gitconfig-work
git config --global --add includeIf."gitdir/i:C:/Projects/personal/".path ~/.gitconfig-personal

# 3. Verify
cd ~/Projects/work/any-repo && git config user.email
# Expected: jane@acme-corp.com

cd ~/Projects/personal/any-repo && git config user.email
# Expected: jane@example.com
```

**For complete step-by-step setup**, see [references/identity-setup-guide.md](references/identity-setup-guide.md).

## Setup

### Directory Layout Convention

Organize repositories by identity under a common parent:

```text
~/Projects/
    work/           # All work repositories
        repo-a/
        repo-b/
    personal/       # All personal repositories
        my-project/
        dotfiles/
```

The parent directory (e.g., `work/`, `personal/`) is what `includeIf gitdir` matches against. Ask the user for their actual directory layout -- do not assume paths.

### Per-Identity Gitconfig Files

Create a separate gitconfig file for each identity. Each file overrides `user.email`, `user.name` (if different), `user.signingkey`, and optionally `core.sshCommand`.

**Work identity** (`~/.gitconfig-work`):

```ini
[user]
    email = jane@acme-corp.com
    signingkey = ABC123DEF4567890
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_work
```

**Personal identity** (`~/.gitconfig-personal`):

```ini
[user]
    email = jane@example.com
    signingkey = 1234567890ABCDEF
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_personal
```

### includeIf Directives

Add conditional includes to `~/.gitconfig`:

```ini
[user]
    name = Jane Developer
[commit]
    gpgsign = true

# Identity isolation
[includeIf "gitdir/i:C:/Projects/work/"]
    path = ~/.gitconfig-work
[includeIf "gitdir/i:C:/Projects/personal/"]
    path = ~/.gitconfig-personal
```

**Critical rules:**

- **Trailing slash required** -- `gitdir:C:/Projects/work/` not `gitdir:C:/Projects/work`
- **Windows: use `gitdir/i:`** -- case-insensitive matching (Windows paths are case-insensitive)
- **macOS/Linux: use `gitdir:`** -- case-sensitive matching is fine on case-sensitive filesystems
- The `user.name` in the main config acts as default; per-identity files only need to override what differs

### GPG Key Per Identity

Generate a separate GPG key for each identity email. See **git:gpg-signing** for detailed key generation.

```bash
# Generate work key (use work email)
gpg --full-generate-key
# Email: jane@acme-corp.com

# Generate personal key (use personal email)
gpg --full-generate-key
# Email: jane@example.com

# List keys to get IDs
gpg --list-secret-keys --keyid-format=long
```

Put the corresponding key ID in each identity's gitconfig file under `user.signingkey`.

### SSH Key Per Identity

Generate a separate SSH key for each identity:

```bash
# Work SSH key
ssh-keygen -t ed25519 -C "jane@acme-corp.com" -f ~/.ssh/id_ed25519_work

# Personal SSH key
ssh-keygen -t ed25519 -C "jane@example.com" -f ~/.ssh/id_ed25519_personal
```

**Two routing approaches** (pick one):

**Option A: `core.sshCommand` in per-identity gitconfig** (recommended -- simpler):

```ini
# In ~/.gitconfig-work
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_work
```

**Option B: `~/.ssh/config` Host-based routing** (needed for multiple GitHub accounts):

```text
# ~/.ssh/config
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
    IdentitiesOnly yes

Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes
```

With Host-based routing, use `url.insteadOf` in each identity config to transparently rewrite remote URLs:

```ini
# In ~/.gitconfig-work
[url "git@github-work:"]
    insteadOf = git@github.com:
```

See [references/identity-setup-guide.md](references/identity-setup-guide.md) for complete SSH routing details.

### Adding Keys to GitHub

Each identity's SSH and GPG public keys must be uploaded to the corresponding GitHub account:

1. **SSH key**: Settings > SSH and GPG keys > New SSH key
2. **GPG key**: Settings > SSH and GPG keys > New GPG key (`gpg --armor --export <KEY_ID>`)
3. **Verify email**: The email on the GPG key must be a verified email on the GitHub account

## Audit

Verify identity isolation is working correctly across all directories.

### Check Effective Identity

```bash
# Check effective identity in any directory
cd /path/to/repo
git config user.email
git config user.name
git config user.signingkey
git config core.sshCommand

# Show where each value comes from
git config --show-origin user.email
git config --show-origin user.signingkey
```

### Detect Mismatches

```bash
# Compare Git email vs GPG key email
GIT_EMAIL=$(git config user.email)
KEY_ID=$(git config user.signingkey)
GPG_EMAIL=$(gpg --list-keys "$KEY_ID" 2>/dev/null | grep -oP '<\K[^>]+')
if [ "$GIT_EMAIL" != "$GPG_EMAIL" ]; then
    echo "MISMATCH: Git=$GIT_EMAIL GPG=$GPG_EMAIL"
else
    echo "OK: $GIT_EMAIL"
fi
```

### Audit All Identity Directories

Ask the user which directories to audit, then check each:

```bash
# Check identity directories (replace with user's actual paths)
for dir in ~/Projects/work ~/Projects/personal; do
    echo "=== $dir ==="
    git -C "$dir/$(ls "$dir" | head -1)" config user.email
    git -C "$dir/$(ls "$dir" | head -1)" config user.signingkey
done
```

See [references/verification-commands.md](references/verification-commands.md) for comprehensive verification scripts.

## Troubleshoot

### "Unverified" Commits on GitHub

**Cause:** The email in the commit signature does not match a verified email on the GitHub account, or the GPG public key is not uploaded.

**Diagnosis:**

```bash
# Check what email was used in the commit
git log --format='%ae %GK %G?' -1

# %ae = author email, %GK = signing key, %G? = signature status
# G = good, B = bad, N = no signature, U = untrusted
```

**Fixes:**

1. Upload GPG public key to GitHub (Settings > SSH and GPG keys)
2. Ensure Git email matches GPG key email matches GitHub verified email
3. Re-sign past commits if needed: `git rebase --exec 'git commit --amend --no-edit -S' HEAD~N`

### includeIf Not Matching

**Symptoms:** `git config user.email` shows global default instead of per-directory value.

**Common causes:**

1. **Missing trailing slash**: `gitdir:C:/Projects/work` must be `gitdir:C:/Projects/work/`
2. **Case sensitivity on Windows**: Use `gitdir/i:` instead of `gitdir:`
3. **Path format mismatch**: Use forward slashes on all platforms; Git normalizes internally
4. **Not inside a git repo**: `includeIf gitdir` only activates inside a git repository

**Diagnosis:**

```bash
# Show all config with origins -- look for the includeIf file
git config --list --show-origin | grep -i "user\."

# Verify the includeIf directive
git config --global --list | grep includeIf
```

### Wrong GPG Key Used

**Symptoms:** Commits signed with wrong key; "Unverified" despite key being uploaded.

**Diagnosis:**

```bash
# Check which key Git is using in this directory
git config user.signingkey

# Check which includeIf file is providing it
git config --show-origin user.signingkey

# Verify the key exists
gpg --list-secret-keys --keyid-format=long $(git config user.signingkey)
```

### SSH Permission Denied (Wrong Key Offered)

**Symptoms:** `git push` fails with "Permission denied (publickey)" despite having SSH keys.

**Diagnosis:**

```bash
# Check which SSH command Git is using
git config core.sshCommand

# Test SSH connection with verbose output
ssh -vT git@github.com 2>&1 | grep "Offering"

# If using Host-based routing, test the specific host alias
ssh -vT git@github-work 2>&1 | grep "Offering"
```

**Fixes:**

1. Verify `core.sshCommand` points to correct key file
2. Verify `~/.ssh/config` has `IdentitiesOnly yes` to prevent SSH agent from offering wrong keys
3. Verify the SSH key is added to the correct GitHub account

## Architecture

### How includeIf Works

Git's `includeIf` evaluates conditions when reading configuration. For `gitdir`:

1. Git determines the current repository's `.git` directory path
2. It normalizes the path (resolves symlinks, uses forward slashes)
3. It checks if the normalized path starts with the `gitdir` pattern
4. If matched, the referenced file is included and its settings override earlier values

**Config precedence with includeIf:**

```text
System config (/etc/gitconfig)
  -> Global config (~/.gitconfig)
    -> includeIf matched files (in order they appear)
      -> Local config (.git/config)
```

Local config (`.git/config`) still has highest priority. An `includeIf` file sits between global and local.

### Multiple includeIf Files

If multiple `includeIf` directives match, they are all included in order. Later includes override earlier ones for the same settings.

### gitdir vs gitdir/i

| Variant | Case Sensitivity | Use On |
| --- | --- | --- |
| `gitdir:` | Case-sensitive | macOS (APFS), Linux (ext4) |
| `gitdir/i:` | Case-insensitive | Windows (NTFS), macOS (HFS+) |

Always use `gitdir/i:` on Windows. On macOS, use `gitdir/i:` unless you know the filesystem is case-sensitive.

## Related Skills

- **gpg-signing**: GPG key generation, passphrase caching, platform setup, and troubleshooting
- **git-config**: Configuration hierarchy, aliases, credentials, and performance tuning
- **setup**: Git installation, initial configuration, and platform-specific setup

## Version History

- v1.0.0 (2026-02-16): Initial release -- multi-identity isolation with includeIf, GPG, SSH, audit, and troubleshooting

## Last Updated

**Date:** 2026-02-16
**Model:** claude-opus-4-6
