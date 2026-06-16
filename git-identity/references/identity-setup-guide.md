# Identity Setup Guide

Complete step-by-step reference for multi-identity Git configuration.

## Prerequisites

- Git 2.13+ (for `includeIf` support)
- GPG installed (see **git:gpg-signing** for platform-specific installation)
- SSH client (included with Git on all platforms)

## Step 1: Plan Your Directory Layout

Organize all repositories under identity-scoped parent directories:

```text
~/Projects/
    work/                    # Work identity (company repos)
        project-alpha/
        project-beta/
    personal/                # Personal identity (open-source, side projects)
        my-app/
        dotfiles/
    freelance/               # Optional: per-client identity
        client-portal/
```

**Convention:** One parent directory per identity. All repos cloned inside inherit that identity automatically.

**Important:** Ask the user for their actual directory layout before proceeding. The paths in this guide are examples only.

## Step 2: Generate GPG Keys Per Identity

Generate a separate GPG key for each email identity:

```bash
# Work key
gpg --full-generate-key
# Select: (9) ECC (sign and encrypt) -> Curve 25519
# Name: Jane Developer
# Email: jane@acme-corp.com
# Passphrase: strong unique passphrase

# Personal key
gpg --full-generate-key
# Name: Jane Developer
# Email: jane@example.com
# Passphrase: different strong passphrase

# List all keys to get key IDs
gpg --list-secret-keys --keyid-format=long
```

Example output:

```text
sec   ed25519/ABC123DEF4567890 2025-01-15 [SC]
      ABCDEF1234567890ABCDEF1234567890ABCDEF12
uid           [ultimate] Jane Developer <jane@acme-corp.com>

sec   ed25519/1234567890ABCDEF 2025-01-15 [SC]
      1234567890ABCDEF1234567890ABCDEF12345678
uid           [ultimate] Jane Developer <jane@example.com>
```

Record the key IDs (e.g., `ABC123DEF4567890` and `1234567890ABCDEF`).

## Step 3: Generate SSH Keys Per Identity

```bash
# Work SSH key
ssh-keygen -t ed25519 -C "jane@acme-corp.com" -f ~/.ssh/id_ed25519_work
# Enter passphrase when prompted

# Personal SSH key
ssh-keygen -t ed25519 -C "jane@example.com" -f ~/.ssh/id_ed25519_personal
# Enter passphrase when prompted
```

This creates four files:

- `~/.ssh/id_ed25519_work` (private) + `~/.ssh/id_ed25519_work.pub` (public)
- `~/.ssh/id_ed25519_personal` (private) + `~/.ssh/id_ed25519_personal.pub` (public)

## Step 4: Create Per-Identity Gitconfig Files

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

**What to include:**

| Setting | Purpose | Required? |
| --- | --- | --- |
| `user.email` | Commit author email | Yes |
| `user.name` | Commit author name (if different per identity) | Only if different |
| `user.signingkey` | GPG key for signing | Yes (if signing) |
| `core.sshCommand` | SSH key for push/pull | Yes (if multiple SSH keys) |

## Step 5: Configure includeIf in ~/.gitconfig

Add conditional includes to your main `~/.gitconfig`:

```ini
[user]
    name = Jane Developer

[commit]
    gpgsign = true

[tag]
    gpgSign = true

[gpg]
    program = C:/Program Files (x86)/GnuPG/bin/gpg.exe

# --- Identity Isolation ---
[includeIf "gitdir/i:C:/Projects/work/"]
    path = ~/.gitconfig-work

[includeIf "gitdir/i:C:/Projects/personal/"]
    path = ~/.gitconfig-personal
```

### Platform-Specific includeIf Syntax

**Windows:**

```ini
# MUST use gitdir/i: (case-insensitive) because NTFS is case-insensitive
[includeIf "gitdir/i:C:/Projects/work/"]
    path = ~/.gitconfig-work
```

**macOS:**

```ini
# Use gitdir/i: on default HFS+ (case-insensitive)
# Use gitdir: only if filesystem is case-sensitive (APFS case-sensitive)
[includeIf "gitdir/i:/Users/jane/Projects/work/"]
    path = ~/.gitconfig-work
```

**Linux:**

```ini
# Use gitdir: (case-sensitive) -- ext4 is case-sensitive
[includeIf "gitdir:/home/jane/Projects/work/"]
    path = ~/.gitconfig-work
```

### includeIf Rules

| Rule | Correct | Incorrect |
| --- | --- | --- |
| Trailing slash | `gitdir:~/Projects/work/` | `gitdir:~/Projects/work` |
| Forward slashes | `gitdir/i:C:/Projects/work/` | `gitdir/i:C:\Projects\work\` |
| Case on Windows | `gitdir/i:` | `gitdir:` |
| Glob patterns | `gitdir:**/work/` | N/A (also valid) |

## Step 6: SSH Config for Multiple GitHub Accounts

If you have multiple GitHub accounts (e.g., work org + personal), you need Host-based SSH routing because GitHub identifies you by SSH key, not username.

**Create or edit `~/.ssh/config`:**

```text
# Work GitHub account
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
    IdentitiesOnly yes

# Personal GitHub account
Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes
```

**Key settings:**

- `IdentitiesOnly yes` -- prevents SSH agent from offering other keys
- `User git` -- GitHub always uses `git` as the SSH user
- `HostName github.com` -- actual hostname (the `Host` alias is what you use in URLs)

### Transparent URL Rewriting

Add `url.insteadOf` to each identity config so you can clone with normal GitHub URLs:

**In `~/.gitconfig-work`:**

```ini
[url "git@github-work:"]
    insteadOf = git@github.com:
```

**In `~/.gitconfig-personal`:**

```ini
[url "git@github-personal:"]
    insteadOf = git@github.com:
```

**How it works:**

1. You clone normally: `git clone git@github.com:org/repo.git` inside `~/Projects/work/`
2. `includeIf` loads `~/.gitconfig-work`
3. `url.insteadOf` rewrites the URL to `git@github-work:org/repo.git`
4. SSH config routes `github-work` to `github.com` using the work SSH key
5. GitHub authenticates you as the work account

### Testing SSH Routing

```bash
# Test work identity
ssh -T git@github-work
# Expected: Hi work-username! You've successfully authenticated...

# Test personal identity
ssh -T git@github-personal
# Expected: Hi personal-username! You've successfully authenticated...
```

## Step 7: Upload Keys to GitHub

For each identity/account:

### SSH Public Key

```bash
# Copy work SSH public key
cat ~/.ssh/id_ed25519_work.pub
# Paste at: https://github.com/settings/keys -> "New SSH key"
# Title: "My Machine - Work Identity"

# Copy personal SSH public key
cat ~/.ssh/id_ed25519_personal.pub
# Paste at: https://github.com/settings/keys -> "New SSH key"
# Title: "My Machine - Personal Identity"
```

### GPG Public Key

```bash
# Export work GPG public key
gpg --armor --export <WORK_GPG_KEY_ID>
# Paste at: https://github.com/settings/keys -> "New GPG key"

# Export personal GPG public key
gpg --armor --export <PERSONAL_GPG_KEY_ID>
# Paste at: https://github.com/settings/keys -> "New GPG key"
```

### Verify Email Match

For each GitHub account, ensure:

1. The GPG key's email is listed as a verified email in GitHub Settings > Emails
2. The `user.email` in the per-identity gitconfig matches the GPG key email
3. The `user.email` matches a verified email on that GitHub account

**Email chain:** `gitconfig user.email` = `GPG key email` = `GitHub verified email`

If any link breaks, commits show as "Unverified."

## Complete Example Configuration

This shows a three-identity setup (two work contexts + personal).

### ~/.gitconfig

```ini
[user]
    name = Jane Developer
[commit]
    gpgsign = true
[tag]
    gpgSign = true
[gpg]
    program = C:/Program Files (x86)/GnuPG/bin/gpg.exe
[init]
    defaultBranch = main
[core]
    autocrlf = true

# Identity isolation
[includeIf "gitdir/i:C:/Projects/acme-corp/"]
    path = ~/.gitconfig-acme
[includeIf "gitdir/i:C:/Projects/globex/"]
    path = ~/.gitconfig-globex
[includeIf "gitdir/i:C:/Projects/personal/"]
    path = ~/.gitconfig-personal
```

### ~/.gitconfig-acme

```ini
[user]
    email = jane@acme-corp.com
    signingkey = ABC123DEF4567890
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_acme
[url "git@github-acme:"]
    insteadOf = git@github.com:
```

### ~/.gitconfig-globex

```ini
[user]
    email = jane.developer@globex.io
    signingkey = FED987CBA6543210
[core]
    sshCommand = ssh -i ~/.ssh/id_ed25519_globex
[url "git@github-globex:"]
    insteadOf = git@github.com:
```

### ~/.ssh/config (relevant entries)

```text
Host github-acme
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_acme
    IdentitiesOnly yes

Host github-globex
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_globex
    IdentitiesOnly yes

Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes
```

---

**Last Updated:** 2026-02-16
