---
name: coverage-report
description: Generate test coverage reports with HTML visualization and threshold enforcement
argument-hint: "[--format <format>] [--threshold <percent>] [--open]"
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
---

# /dotnet:coverage-report

Generate comprehensive test coverage reports with HTML visualization, threshold enforcement, and coverage gap analysis.

## Arguments

Parse arguments from `$ARGUMENTS`:

| Flag | Description | Default |
|------|-------------|---------|
| `--format <format>` | Output format (cobertura, opencover, html, all) | html |
| `--threshold <percent>` | Fail if line coverage below threshold | None |
| `--project <path>` | Target specific test project | All test projects |
| `--output <path>` | Output directory for reports | ./coverage |
| `--open` | Open HTML report in browser | false |
| `--history` | Include historical trends (if available) | false |

## Prerequisites

This command requires coverage tools. If not installed, will prompt:

```text
Coverage tools not found. Install now?

Required:
  - dotnet-coverage (collection)
  - reportgenerator (HTML reports)

Run: /dotnet:install-tool --tool coverage
Run: /dotnet:install-tool --tool reportgen --global
```

## Workflow

### Step 1: Check Tool Availability

```bash
# Check for coverage tools
dotnet tool list | grep -E "dotnet-coverage|reportgenerator"

# Check global tools
dotnet tool list --global | grep reportgenerator
```

If missing, offer to install via `/dotnet:install-tool`.

### Step 2: Find Test Projects

```bash
# Find test projects by convention
find . -name "*.Tests.csproj" -o -name "*.Test.csproj" -o -name "*Tests.csproj"

# Or by reference to test frameworks
grep -l "Microsoft.NET.Test.Sdk" **/*.csproj
```

### Step 3: Run Tests with Coverage

**Using dotnet-coverage (recommended for .NET 6+):**

```bash
dotnet-coverage collect \
  --output coverage.cobertura.xml \
  --output-format cobertura \
  dotnet test --no-build
```

**Using coverlet (alternative):**

```bash
dotnet test \
  --collect:"XPlat Code Coverage" \
  --results-directory ./coverage
```

### Step 4: Generate HTML Report

```bash
reportgenerator \
  -reports:coverage.cobertura.xml \
  -targetdir:./coverage/html \
  -reporttypes:Html \
  -assemblyfilters:"-*.Tests;-*.Test" \
  -classfilters:"-*Migrations*"
```

### Step 5: Analyze Coverage

Parse coverage report for metrics:

- Line coverage percentage
- Branch coverage percentage
- Method coverage percentage
- Uncovered lines by file

### Step 6: Threshold Check

If `--threshold` specified:

```text
Coverage threshold check:
  Required: 80%
  Actual: 72.5%

  Status: FAILED

  Files below threshold:
    - src/MyApp/Services/PaymentService.cs (45%)
    - src/MyApp/Handlers/OrderHandler.cs (52%)
    - src/MyApp/Controllers/ReportController.cs (61%)
```

## Output Format

**Summary Report:**

```text
Test Coverage Report

Generated: 2026-01-18 11:00:00 UTC
Test Projects: 3
Tests Run: 247 passed, 0 failed

═══════════════════════════════════════════════════════════════
                    COVERAGE SUMMARY
═══════════════════════════════════════════════════════════════

  Metric              Coverage    Target    Status
  ─────────────────────────────────────────────────
  Line Coverage       78.5%       80%       WARN
  Branch Coverage     65.2%       70%       WARN
  Method Coverage     85.3%       80%       PASS

═══════════════════════════════════════════════════════════════

Coverage by Project:
  Project                    Lines      Branches   Methods
  ─────────────────────────────────────────────────────────
  MyApp.Core                 92.1%      88.5%      95.0%
  MyApp.Api                  75.3%      62.1%      82.4%
  MyApp.Infrastructure       68.2%      55.0%      78.6%

Top Uncovered Files:
  File                                    Coverage  Uncovered
  ────────────────────────────────────────────────────────────
  Services/PaymentService.cs              45.2%     87 lines
  Handlers/OrderHandler.cs                52.1%     64 lines
  Controllers/ReportController.cs         61.8%     45 lines
  Repositories/AuditRepository.cs         64.5%     38 lines
  Services/NotificationService.cs         67.2%     31 lines

Coverage Gaps (uncovered code patterns):
  - Exception handlers: 23 catch blocks untested
  - Edge cases: 15 null checks untested
  - Error paths: 12 error branches untested

HTML Report: ./coverage/html/index.html
```

**Detailed Per-File Report:**

```text
Coverage Details: src/MyApp/Services/PaymentService.cs

  Overall: 45.2% (78/172 lines covered)

  Covered Methods:
    ✓ ProcessPayment()         100% (15/15 lines)
    ✓ ValidateCard()           100% (12/12 lines)
    ✓ GetPaymentStatus()       95%  (19/20 lines)

  Partially Covered Methods:
    ~ RefundPayment()          42%  (8/19 lines)
    ~ HandleFailure()          35%  (7/20 lines)

  Uncovered Methods:
    ✗ RetryPayment()           0%   (0/25 lines)
    ✗ ProcessBatchPayments()   0%   (0/31 lines)
    ✗ HandleWebhook()          0%   (0/30 lines)

  Uncovered Line Ranges:
    Lines 145-169: RetryPayment() - retry logic
    Lines 180-210: ProcessBatchPayments() - batch processing
    Lines 220-249: HandleWebhook() - webhook handling

  Recommendations:
    1. Add tests for retry scenarios
    2. Add tests for batch payment edge cases
    3. Add tests for webhook validation
```

**Threshold Failure:**

```text
COVERAGE THRESHOLD FAILED

  Required: 80% line coverage
  Actual: 72.5% line coverage
  Gap: 7.5%

  To reach 80% coverage, add tests for ~150 more lines

  Quick wins (highest impact):
    1. PaymentService.cs: +27 lines = +1.5%
    2. OrderHandler.cs: +24 lines = +1.3%
    3. ReportController.cs: +18 lines = +1.0%

  Exit code: 1 (threshold not met)
```

## Report Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `cobertura` | XML format | CI/CD integration, Azure DevOps |
| `opencover` | XML format | SonarQube, older tools |
| `html` | Interactive HTML | Local review, PR reviews |
| `lcov` | LCOV format | GitHub Actions, Codecov |
| `all` | Generate all formats | Comprehensive reporting |

## Integration Examples

**Azure DevOps:**

```yaml
- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: Cobertura
    summaryFileLocation: '$(Build.SourcesDirectory)/coverage/coverage.cobertura.xml'
```

**GitHub Actions:**

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage/coverage.cobertura.xml
```

**SonarQube:**

```bash
dotnet sonarscanner begin \
  /k:"project-key" \
  /d:sonar.cs.opencover.reportsPaths="coverage/coverage.opencover.xml"
```

## Examples

```bash
# Generate HTML coverage report
/dotnet:coverage-report

# Generate report with threshold enforcement
/dotnet:coverage-report --threshold 80

# Generate Cobertura XML for CI
/dotnet:coverage-report --format cobertura

# Generate all formats
/dotnet:coverage-report --format all

# Target specific test project
/dotnet:coverage-report --project MyApp.Tests

# Open report in browser
/dotnet:coverage-report --open

# Custom output directory
/dotnet:coverage-report --output ./artifacts/coverage
```

## Filtering

Exclude from coverage analysis:

- Test projects (`*.Tests`, `*.Test`)
- Generated code (Migrations, designer files)
- Third-party code

Configure in reportgenerator call:

```bash
-assemblyfilters:"-*.Tests;-*.Test;-*.Migrations"
-classfilters:"-*Generated*;-*Designer*"
```

## Historical Trends

If `--history` and previous reports exist:

```text
Coverage Trend (last 5 runs):

  Date          Line%   Branch%   Change
  ──────────────────────────────────────
  2026-01-18    78.5%   65.2%     +2.1%
  2026-01-15    76.4%   63.8%     +1.5%
  2026-01-12    74.9%   62.1%     +0.8%
  2026-01-10    74.1%   61.5%     -0.5%
  2026-01-08    74.6%   62.0%     --

  Trend: Improving (+3.9% over 10 days)
```
