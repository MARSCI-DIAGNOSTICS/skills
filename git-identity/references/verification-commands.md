# Verification Commands

Quick-reference for auditing multi-identity Git configuration.

## Check Effective Identity in Any Directory

```bash
# Navigate to a repo and check all identity settings
cd /path/to/repo
echo "Email:      $(git config user.email)"
echo "Name:       $(git config user.name)"
echo "SigningKey:  $(git config user.signingkey)"
echo "SSH Command: $(git config core.sshCommand)"
```

### Expected Output Examples

**Inside a work repo** (e.g., `~/Projects/work/some-repo`):

```text
Email:      jane@acme-corp.com
Name:       Jane Developer
SigningKey:  ABC123DEF4567890
SSH Command: ssh -i ~/.ssh/id_ed25519_work
```

**Inside a personal repo** (e.g., `~/Projects/personal/some-repo`):

```text
Email:      jane@example.com
Name:       Jane Developer
SigningKey:  1234567890ABCDEF
SSH Command: ssh -i ~/.ssh/id_ed25519_personal
```

## Show Configuration Origins

See exactly which file provides each setting:

```bash
git config --show-origin user.email
git config --show-origin user.name
git config --show-origin user.signingkey
git config --show-origin core.sshCommand
```

Example output:

```text
file:/home/jane/.gitconfig-work    jane@acme-corp.com
```

## Audit All Identity Directories

Script to verify all identity directories at once. Replace the paths in `IDENTITY_DIRS` with the user's actual directory layout.

```bash
#!/usr/bin/env bash
# audit-identities.sh -- Check identity isolation across directories

IDENTITY_DIRS=(
    "$HOME/Projects/work"
    "$HOME/Projects/personal"
)

for identity_dir in "${IDENTITY_DIRS[@]}"; do
    if [ ! -d "$identity_dir" ]; then
        echo "SKIP: $identity_dir (not found)"
        continue
    fi

    # Find first repo in the directory
    repo=$(find "$identity_dir" -maxdepth 2 -name ".git" -type d | head -1)
    if [ -z "$repo" ]; then
        echo "SKIP: $identity_dir (no git repos found)"
        continue
    fi
    repo_dir=$(dirname "$repo")

    echo "=== $identity_dir ==="
    echo "  Repo:       $repo_dir"
    echo "  Email:      $(git -C "$repo_dir" config user.email)"
    echo "  Name:       $(git -C "$repo_dir" config user.name)"
    echo "  SigningKey:  $(git -C "$repo_dir" config user.signingkey)"
    echo "  SSH:        $(git -C "$repo_dir" config core.sshCommand)"
    echo ""
done
```

## Detect Email/GPG Key Mismatch

Check that `user.email` matches the email on the configured GPG key:

```bash
#!/usr/bin/env bash
# check-email-gpg-match.sh -- Verify email matches GPG key in current repo

GIT_EMAIL=$(git config user.email)
KEY_ID=$(git config user.signingkey)

if [ -z "$KEY_ID" ]; then
    echo "No signing key configured in this directory"
    exit 1
fi

GPG_EMAIL=$(gpg --with-colons --list-keys "$KEY_ID" 2>/dev/null \
    | grep '^uid' | head -1 | cut -d: -f10 \
    | grep -oP '<\K[^>]+')

if [ -z "$GPG_EMAIL" ]; then
    echo "ERROR: GPG key $KEY_ID not found in keyring"
    exit 1
fi

if [ "$GIT_EMAIL" = "$GPG_EMAIL" ]; then
    echo "OK: Email matches ($GIT_EMAIL)"
else
    echo "MISMATCH:"
    echo "  Git email: $GIT_EMAIL"
    echo "  GPG email: $GPG_EMAIL"
    echo "  Key ID:    $KEY_ID"
    exit 1
fi
```

## Cross-Directory Comparison Table

Generate a comparison table of all identities. Replace the directory paths with the user's actual paths.

```bash
#!/usr/bin/env bash
# identity-table.sh -- Generate comparison table

printf "%-20s %-35s %-20s\n" "Directory" "Email" "SigningKey"
printf "%-20s %-35s %-20s\n" "---" "---" "---"

for identity_dir in ~/Projects/work ~/Projects/personal; do
    name=$(basename "$identity_dir")
    repo=$(find "$identity_dir" -maxdepth 2 -name ".git" -type d 2>/dev/null | head -1)
    if [ -n "$repo" ]; then
        repo_dir=$(dirname "$repo")
        email=$(git -C "$repo_dir" config user.email)
        key=$(git -C "$repo_dir" config user.signingkey)
        printf "%-20s %-35s %-20s\n" "$name" "$email" "$key"
    else
        printf "%-20s %-35s %-20s\n" "$name" "(no repos)" "(n/a)"
    fi
done
```

Example output:

```text
Directory            Email                               SigningKey
---                  ---                                 ---
work                 jane@acme-corp.com                  ABC123DEF4567890
personal             jane@example.com                    1234567890ABCDEF
```

## Verify SSH Key Routing

Test that each SSH Host alias connects with the correct key:

```bash
# Test each SSH host (replace with user's actual host aliases)
ssh -T git@github-work 2>&1
ssh -T git@github-personal 2>&1

# Verbose mode to see which key is offered
ssh -vT git@github-work 2>&1 | grep "Offering"
```

## Verify Recent Commit Signatures

Check that recent commits are signed with the correct key:

```bash
# Show last 5 commits with signature info
git log --format='%h %ae %GK %G? %s' -5

# Column meanings:
# %h  = short hash
# %ae = author email
# %GK = signing key fingerprint
# %G? = signature status (G=good, N=none, B=bad, U=untrusted)
# %s  = subject
```

---

**Last Updated:** 2026-02-16
