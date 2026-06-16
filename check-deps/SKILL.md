---
name: check-deps
description: Check dependencies for known CVEs and security vulnerabilities
argument-hint: "[--npm|--pip|--dotnet|--cargo|--all]"
allowed-tools: Task
---

# Check Dependencies Command

Analyze project dependencies for known vulnerabilities and security issues.

## Usage

```bash
/security:check-deps               # Auto-detect and check all ecosystems
/security:check-deps --npm         # Check npm dependencies only
/security:check-deps --pip         # Check Python dependencies only
/security:check-deps --dotnet      # Check .NET dependencies only
/security:check-deps --cargo       # Check Rust dependencies only
/security:check-deps --all         # Explicitly check all ecosystems
```

## Execution

Delegate to the `dependency-checker` agent with the following prompt:

**If no arguments or `--all`:**
"Analyze this project's dependencies for known vulnerabilities. Auto-detect the package ecosystem(s) in use (npm, pip, .NET, Rust, etc.) and run appropriate security audits. Generate a dependency security report with CVE details, CVSS scores, fix availability, and prioritized remediation recommendations."

**If `--npm` argument:**
"Analyze npm/Node.js dependencies for known vulnerabilities using npm audit. Generate a dependency security report with CVE details, CVSS scores, fix availability, and prioritized remediation recommendations including upgrade paths and override options."

**If `--pip` argument:**
"Analyze Python dependencies for known vulnerabilities using pip-audit. Generate a dependency security report with CVE details, CVSS scores, fix availability, and prioritized remediation recommendations."

**If `--dotnet` argument:**
"Analyze .NET dependencies for known vulnerabilities using dotnet list package --vulnerable. Generate a dependency security report with CVE details, CVSS scores, fix availability, and prioritized remediation recommendations."

**If `--cargo` argument:**
"Analyze Rust dependencies for known vulnerabilities using cargo audit. Generate a dependency security report with CVE details, CVSS scores, fix availability, and prioritized remediation recommendations."

## Output

The dependency-checker agent produces a report including:

- Summary table by severity (Critical/High/Medium/Low) with fixable counts
- Detailed CVE information for each vulnerability
- Affected dependency paths (direct vs transitive)
- Remediation plan with upgrade recommendations
- Supply chain risk factors (abandoned packages, typosquatting, etc.)
