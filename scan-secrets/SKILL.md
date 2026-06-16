---
name: scan-secrets
description: Scan codebase for hardcoded secrets, API keys, credentials, and sensitive data
argument-hint: "[path|--all|--staged]"
allowed-tools: Task
---

# Scan Secrets Command

Scan code for hardcoded secrets, API keys, tokens, and credentials.

## Usage

```bash
/security:scan-secrets             # Scan current directory
/security:scan-secrets src/        # Scan specific directory
/security:scan-secrets --all       # Scan entire repository
/security:scan-secrets --staged    # Scan staged git changes only
```

## Execution

Delegate to the `secrets-scanner` agent with the following prompt:

**If no arguments provided:**
"Scan the current working directory for hardcoded secrets, API keys, credentials, tokens, and sensitive data patterns. Report findings with severity classification, file locations, and remediation guidance. Validate findings to minimize false positives."

**If `--all` argument:**
"Scan the entire repository for hardcoded secrets, API keys, credentials, tokens, and sensitive data patterns. Exclude common false positive locations (node_modules, vendor, .git). Report findings with severity classification, file locations, and remediation guidance."

**If `--staged` argument:**
"Scan staged git changes (git diff --staged) for hardcoded secrets, API keys, credentials, tokens, and sensitive data patterns. This is a pre-commit check. Report findings with severity classification and remediation guidance."

**If path specified:**
"Scan $ARGUMENTS for hardcoded secrets, API keys, credentials, tokens, and sensitive data patterns. Report findings with severity classification, file locations, and remediation guidance. Validate findings to minimize false positives."

## Output

The secrets-scanner agent produces a report including:

- Summary of findings by severity
- Each finding with file, line, pattern type, and confidence
- Remediation steps (rotate credential, move to environment variable, etc.)
- False positive analysis where applicable
