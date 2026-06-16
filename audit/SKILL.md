---
name: audit
description: Run security audit on code for OWASP Top 10, CWE vulnerabilities, and security anti-patterns
argument-hint: "[files|directory|--staged|--pr]"
allowed-tools: Task
---

# Security Audit Command

Run a comprehensive security audit on specified code to identify vulnerabilities.

## Usage

```bash
/security:audit                    # Audit current directory
/security:audit src/               # Audit specific directory
/security:audit --staged           # Audit staged git changes
/security:audit --pr               # Audit changes in current PR
/security:audit api.py utils.js    # Audit specific files
```

## Execution

Delegate to the `security-auditor` agent with the following prompt:

**If no arguments provided:**
"Perform a security audit on the current working directory. Focus on OWASP Top 10 vulnerabilities, CWE weaknesses, and security anti-patterns. Generate a structured security audit report."

**If `--staged` argument:**
"Perform a security audit on staged git changes (git diff --staged). Focus on OWASP Top 10 vulnerabilities, CWE weaknesses, and security anti-patterns in the changed code. Generate a structured security audit report."

**If `--pr` argument:**
"Perform a security audit on the current PR changes (git diff main...HEAD). Focus on OWASP Top 10 vulnerabilities, CWE weaknesses, and security anti-patterns in the changed code. Generate a structured security audit report."

**If files/directory specified:**
"Perform a security audit on $ARGUMENTS. Focus on OWASP Top 10 vulnerabilities, CWE weaknesses, and security anti-patterns. Generate a structured security audit report."

## Output

The security-auditor agent produces a structured report including:

- Executive summary with severity counts
- Critical/High/Medium/Low findings with CWE references
- Remediation guidance with code examples
- Positive security findings (properly implemented controls)
