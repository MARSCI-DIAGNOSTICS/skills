# Secrets Scanning Reference

This reference provides detailed setup and configuration for secrets scanning tools.

## Tool Comparison

| Tool | Language | Strengths | Weaknesses | Best For |
|------|----------|-----------|------------|----------|
| gitleaks | Go | Fast, good patterns, SARIF output | May miss custom formats | Pre-commit, CI/CD |
| TruffleHog | Go | Verifies secrets are live | Slower, network calls | Deep audits |
| detect-secrets | Python | Baseline support, plugins | More false positives | Existing codebases |
| git-secrets | Bash | AWS patterns, simple | AWS-focused, limited | AWS-heavy projects |
| GitHub Secret Scanning | Cloud | Automatic, partner alerts | GitHub-only | GitHub repos |
| GitLab SAST | Cloud | Integrated, SAST suite | GitLab-only | GitLab repos |

## Gitleaks

### Installation

```bash
# macOS
brew install gitleaks

# Linux
wget https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_8.18.0_linux_x64.tar.gz
tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/

# Windows (scoop)
scoop install gitleaks

# Docker
docker pull ghcr.io/gitleaks/gitleaks:latest
```

### Basic Usage

```bash
# Scan current directory
gitleaks detect --source . -v

# Scan specific commit range
gitleaks detect --source . --log-opts="origin/main..HEAD"

# Scan entire git history
gitleaks detect --source . --log-opts="--all"

# Output to file (SARIF format for GitHub)
gitleaks detect --source . --report-format sarif --report-path results.sarif

# Output to JSON
gitleaks detect --source . --report-format json --report-path results.json
```

### Custom Configuration

```toml
# .gitleaks.toml
title = "Custom Gitleaks Config"

[allowlist]
  description = "Allowlisted patterns"
  paths = [
    '''\.gitleaks\.toml$''',
    '''(.*?)(png|jpg|gif|doc|pdf|bin|svg)$''',
    '''go\.sum$''',
    '''package-lock\.json$''',
  ]

# Custom rule for internal API keys
[[rules]]
  id = "internal-api-key"
  description = "Internal API Key"
  regex = '''INTERNAL_API_KEY['"]*\s*[:=]\s*['"]?([A-Za-z0-9]{32,})['"]?'''
  keywords = ["INTERNAL_API_KEY"]
  secretGroup = 1

# Override severity for specific rules
[[rules]]
  id = "generic-api-key"
  description = "Generic API Key"
  regex = '''(?i)api[_-]?key['"]*\s*[:=]\s*['"]?([A-Za-z0-9]{20,})['"]?'''
  keywords = ["api_key", "apikey", "api-key"]
  secretGroup = 1

# Allow specific false positives
[[rules.allowlist]]
  regexes = [
    '''example\.com''',
    '''test_api_key''',
    '''dummy_secret''',
  ]
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

### GitHub Actions

```yaml
# .github/workflows/gitleaks.yml
name: Gitleaks

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0  # Full history for accurate scanning

      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}  # Optional, for enterprise

      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```

## TruffleHog

### Installation

```bash
# macOS
brew install trufflehog

# Linux/macOS (binary)
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin

# Docker
docker pull trufflesecurity/trufflehog:latest

# pip
pip install trufflehog
```

### Basic Usage

```bash
# Scan git repository
trufflehog git https://github.com/myorg/myrepo --only-verified

# Scan local directory
trufflehog filesystem /path/to/code

# Scan with full history
trufflehog git file://. --since-commit HEAD~100

# Output JSON
trufflehog git file://. --json > results.json

# Scan specific branch
trufflehog git file://. --branch develop

# Scan S3 bucket
trufflehog s3 --bucket mybucket

# Scan GitHub organization
trufflehog github --org myorg --token $GITHUB_TOKEN
```

### Key Features

**Verification**: TruffleHog can verify if detected secrets are actually valid by making API calls.

```bash
# Only report verified (live) secrets
trufflehog git file://. --only-verified

# Report all findings (verified + unverified)
trufflehog git file://. --results verified,unknown
```

**Supported Detectors**: 800+ credential types including:

- AWS keys
- GCP service accounts
- Azure credentials
- API keys (Stripe, Twilio, SendGrid, etc.)
- Database connections
- JWT tokens
- Private keys

### GitHub Actions

```yaml
# .github/workflows/trufflehog.yml
name: TruffleHog Secrets Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: TruffleHog Scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.pull_request.base.sha }}
          head: ${{ github.sha }}
          extra_args: --only-verified
```

### Custom Detectors

```yaml
# custom-detectors.yaml
detectors:
  - name: InternalAPIKey
    keywords:
      - "INTERNAL_API"
    regex:
      secretGroup: 1
      pattern: 'INTERNAL_API_KEY[=:]\s*([A-Za-z0-9]{32})'
    verify:
      - endpoint: https://api.internal.example.com/verify
        headers:
          Authorization: "Bearer {secret}"
        successRanges:
          - 200-299
```

## detect-secrets

### Installation

```bash
pip install detect-secrets
```

### Basic Usage

```bash
# Scan and create baseline
detect-secrets scan > .secrets.baseline

# Scan with existing baseline (only new secrets)
detect-secrets scan --baseline .secrets.baseline

# Audit baseline interactively
detect-secrets audit .secrets.baseline

# Update baseline after audit
detect-secrets scan --baseline .secrets.baseline --update .secrets.baseline
```

### Baseline File

```json
// .secrets.baseline
{
  "version": "1.4.0",
  "plugins_used": [
    {"name": "AWSKeyDetector"},
    {"name": "AzureStorageKeyDetector"},
    {"name": "Base64HighEntropyString", "limit": 4.5},
    {"name": "BasicAuthDetector"},
    {"name": "CloudantDetector"},
    {"name": "GitHubTokenDetector"},
    {"name": "HexHighEntropyString", "limit": 3.0},
    {"name": "JwtTokenDetector"},
    {"name": "PrivateKeyDetector"},
    {"name": "SlackDetector"},
    {"name": "StripeDetector"}
  ],
  "filters_used": [
    {"path": "detect_secrets.filters.allowlist.is_line_allowlisted"},
    {"path": "detect_secrets.filters.common.is_baseline_file"},
    {"path": "detect_secrets.filters.heuristic.is_likely_id_string"}
  ],
  "results": {}
}
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock\.json
```

### Custom Plugins

```python
# my_detector.py
from detect_secrets.plugins.base import RegexBasedDetector

class InternalAPIKeyDetector(RegexBasedDetector):
    """Detect internal API keys."""

    secret_type = "Internal API Key"

    denylist = [
        r'INTERNAL_API_KEY[=:]\s*[\'"]?([A-Za-z0-9]{32})[\'"]?',
    ]

# Usage
detect-secrets scan --list-all-plugins  # Verify plugin loaded
detect-secrets scan --plugin my_detector.InternalAPIKeyDetector
```

### Inline Allowlisting

```python
# Mark false positives inline
api_key = "test_key_for_unit_tests"  # pragma: allowlist secret

# Or for specific secret types
password = "mock_password"  # pragma: allowlist-secret password
```

## git-secrets

### Installation

```bash
# macOS
brew install git-secrets

# Linux
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets && make install

# Windows (manual)
# Download and add to PATH
```

### Setup

```bash
# Install hooks in repository
git secrets --install

# Add AWS patterns
git secrets --register-aws

# Add custom patterns
git secrets --add 'PRIVATE_KEY[=:]\s*[A-Za-z0-9+/]{40,}'
git secrets --add --literal 'MyCompanyInternalToken'

# Allow specific patterns (false positives)
git secrets --add --allowed 'example_api_key'
git secrets --add --allowed '.*_test_.*'
```

### Global Configuration

```bash
# Apply to all new repositories
git secrets --install ~/.git-templates/git-secrets
git config --global init.templateDir ~/.git-templates/git-secrets

# Register AWS patterns globally
git secrets --register-aws --global
```

## CI/CD Integration Patterns

### Multi-Tool Strategy

```yaml
# .github/workflows/secrets-scan.yml
name: Secrets Scanning

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 0 * * *'  # Daily full scan

jobs:
  # Fast scan on every commit
  quick-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: Gitleaks (fast)
        uses: gitleaks/gitleaks-action@v2
        with:
          args: --log-opts="origin/main..HEAD"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # Deep scan on main branch and schedule
  deep-scan:
    if: github.ref == 'refs/heads/main' || github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: TruffleHog (verified only)
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified

      - name: Gitleaks (full history)
        uses: gitleaks/gitleaks-action@v2
        with:
          args: --log-opts="--all"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - security

secrets-scan:
  stage: security
  image: ghcr.io/gitleaks/gitleaks:latest
  script:
    - gitleaks detect --source . --log-opts="$CI_COMMIT_BEFORE_SHA..$CI_COMMIT_SHA" --report-format sarif --report-path gitleaks.sarif
  artifacts:
    paths:
      - gitleaks.sarif
    reports:
      sast: gitleaks.sarif
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### Azure DevOps

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.x'

  - script: |
      pip install detect-secrets
      detect-secrets scan --baseline .secrets.baseline
    displayName: 'Secrets Scan'

  - script: |
      curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/scripts/install.sh | sh -s v8.18.0
      ./bin/gitleaks detect --source . -v
    displayName: 'Gitleaks Scan'
```

## Remediation Workflow

### When Secrets Are Found

```bash
# 1. Immediately rotate the compromised credential
#    - Cloud console, API dashboard, etc.

# 2. Determine exposure scope
git log -p --all -S "exposed_secret" -- .

# 3. Remove from history (if needed)
# WARNING: This rewrites history!
git filter-repo --invert-paths --path secrets.txt

# Or use BFG (faster for large repos)
bfg --delete-files secrets.txt
bfg --replace-text replacements.txt

# 4. Force push (after coordination with team)
git push --force-with-lease

# 5. Audit access logs for the compromised credential

# 6. Document incident
```

### Preventing Recurrence

```bash
# 1. Install pre-commit hooks
pre-commit install

# 2. Add to CI/CD pipeline

# 3. Enable GitHub/GitLab secret scanning

# 4. Train team on secrets management

# 5. Implement secrets manager (Vault, AWS SM, etc.)
```

## Best Practices

### Scanning Strategy

| Phase | Tool | Scope | Frequency |
|-------|------|-------|-----------|
| Pre-commit | gitleaks | Staged changes | Every commit |
| PR/MR | gitleaks | Branch diff | Every PR |
| Main branch | gitleaks + TruffleHog | Full commit | Every merge |
| Scheduled | TruffleHog (verified) | Full history | Daily/weekly |
| Audit | TruffleHog + manual | Full history | Quarterly |

### False Positive Management

1. **Baseline files**: Use `.secrets.baseline` (detect-secrets) or `.gitleaksignore`
2. **Inline comments**: `# pragma: allowlist secret`
3. **Path exclusions**: Exclude test fixtures, documentation
4. **Regular audits**: Review and update exclusions quarterly

### Metrics to Track

- Time to detection (how long secrets exist before caught)
- False positive rate (tune configs to reduce noise)
- Mean time to rotation (how fast compromised secrets are rotated)
- Coverage (% of repos with scanning enabled)

## Security Checklist

### Implementation

- [ ] Pre-commit hooks installed
- [ ] CI/CD scanning enabled
- [ ] Multiple tools for defense in depth
- [ ] Baseline file maintained
- [ ] False positives documented

### Operations

- [ ] Alerts route to security team
- [ ] Rotation runbook documented
- [ ] Regular full-history scans scheduled
- [ ] Coverage metrics tracked
- [ ] Team trained on remediation

### Governance

- [ ] Scanning policy documented
- [ ] Incident response plan includes secrets
- [ ] Regular audits of exclusions
- [ ] Secrets findings in security reports
