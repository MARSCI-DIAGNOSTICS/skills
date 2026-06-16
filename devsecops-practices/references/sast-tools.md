# SAST Tools Reference

Detailed configuration and usage guides for Static Application Security Testing tools.

## Semgrep Deep Dive

### Installation and Setup

```bash
# Install via pip
pip install semgrep

# Install via Homebrew
brew install semgrep

# Docker
docker run --rm -v "${PWD}:/src" semgrep/semgrep semgrep scan --config auto
```

### Custom Rule Development

```yaml
# custom-rules/sql-injection.yml
rules:
  # Python SQLAlchemy injection
  - id: sqlalchemy-raw-query-injection
    patterns:
      - pattern-either:
          - pattern: |
              $SESSION.execute($QUERY % ...)
          - pattern: |
              $SESSION.execute($QUERY.format(...))
          - pattern: |
              $SESSION.execute(f"...")
          - pattern: |
              text($QUERY % ...)
          - pattern: |
              text($QUERY.format(...))
          - pattern: |
              text(f"...")
    message: |
      Potential SQL injection in SQLAlchemy. Use parameterized queries:
      session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
    severity: ERROR
    languages: [python]
    metadata:
      cwe: "CWE-89"
      owasp: "A03:2021 - Injection"
      category: security
      technology:
        - sqlalchemy

  # Django ORM raw query injection
  - id: django-raw-sql-injection
    patterns:
      - pattern-either:
          - pattern: |
              $MODEL.objects.raw($QUERY % ...)
          - pattern: |
              $MODEL.objects.raw($QUERY.format(...))
          - pattern: |
              $MODEL.objects.raw(f"...")
          - pattern: |
              connection.cursor().execute($QUERY % ...)
          - pattern: |
              connection.cursor().execute($QUERY.format(...))
    message: |
      SQL injection in Django raw query. Use parameterized queries:
      Model.objects.raw("SELECT * FROM table WHERE id = %s", [user_id])
    severity: ERROR
    languages: [python]
    metadata:
      cwe: "CWE-89"
      owasp: "A03:2021 - Injection"

  # Node.js SQL injection
  - id: nodejs-sql-injection
    patterns:
      - pattern-either:
          - pattern: |
              $POOL.query($QUERY + ...)
          - pattern: |
              $POOL.query(`... ${...} ...`)
          - pattern: |
              $CONNECTION.query($QUERY + ...)
          - pattern: |
              $CONNECTION.query(`... ${...} ...`)
    message: |
      SQL injection vulnerability. Use parameterized queries:
      pool.query("SELECT * FROM users WHERE id = $1", [userId])
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe: "CWE-89"

  # Command Injection
  - id: command-injection-subprocess
    patterns:
      - pattern-either:
          - pattern: subprocess.call($CMD, shell=True, ...)
          - pattern: subprocess.run($CMD, shell=True, ...)
          - pattern: subprocess.Popen($CMD, shell=True, ...)
          - pattern: os.system($CMD)
          - pattern: os.popen($CMD)
      - pattern-not: subprocess.call("...", shell=True, ...)
      - pattern-not: subprocess.run("...", shell=True, ...)
    message: |
      Potential command injection. Avoid shell=True with user input.
      Use subprocess with list arguments: subprocess.run(["cmd", arg1, arg2])
    severity: ERROR
    languages: [python]
    metadata:
      cwe: "CWE-78"
      owasp: "A03:2021 - Injection"

  # Path Traversal
  - id: path-traversal
    patterns:
      - pattern-either:
          - pattern: open(os.path.join($BASE, $INPUT), ...)
          - pattern: pathlib.Path($BASE) / $INPUT
      - pattern-not-inside: |
          if ".." in $INPUT:
              ...
      - pattern-not-inside: |
          $SAFE = os.path.normpath(...)
          ...
    message: |
      Potential path traversal. Validate input doesn't contain ".." and
      use os.path.realpath() to resolve the path within allowed directory.
    severity: WARNING
    languages: [python]
    metadata:
      cwe: "CWE-22"

  # Insecure Deserialization
  - id: insecure-pickle
    patterns:
      - pattern-either:
          - pattern: pickle.loads(...)
          - pattern: pickle.load(...)
          - pattern: cPickle.loads(...)
          - pattern: cPickle.load(...)
    message: |
      Pickle deserialization is unsafe with untrusted data.
      Use JSON or a safe serialization format instead.
    severity: WARNING
    languages: [python]
    metadata:
      cwe: "CWE-502"
      owasp: "A08:2021 - Software and Data Integrity Failures"

  # SSRF
  - id: ssrf-requests
    patterns:
      - pattern-either:
          - pattern: requests.get($URL, ...)
          - pattern: requests.post($URL, ...)
          - pattern: requests.put($URL, ...)
          - pattern: requests.delete($URL, ...)
          - pattern: urllib.request.urlopen($URL)
      - pattern-not: requests.get("...", ...)
      - pattern-not: requests.post("...", ...)
      - metavariable-regex:
          metavariable: $URL
          regex: '^[^"''].*$'  # Not a string literal
    message: |
      Potential SSRF vulnerability. Validate and allowlist URLs before making requests.
      Consider using a URL validation library.
    severity: WARNING
    languages: [python]
    metadata:
      cwe: "CWE-918"
      owasp: "A10:2021 - Server-Side Request Forgery"
```

### Semgrep CI Configuration

```yaml
# .semgrep.yml - Project configuration
rules: []  # Use rulesets below

# Rulesets to use
# semgrep --config p/python --config p/security-audit --config p/owasp-top-ten

# Rule severity overrides
severity:
  - rule: python.lang.security.audit.dangerous-subprocess-use
    level: error
  - rule: python.lang.security.audit.hardcoded-password
    level: error

# Paths to scan
include:
  - "src/"
  - "app/"
  - "lib/"

# Paths to exclude
exclude:
  - "tests/"
  - "vendor/"
  - "**/node_modules/**"
  - "**/*.min.js"
  - "**/migrations/**"
```

```yaml
# .github/workflows/semgrep-full.yml
name: Semgrep Full Analysis
on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 4 * * *'  # Daily 4 AM

jobs:
  semgrep:
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep

    steps:
      - uses: actions/checkout@v5

      - name: Run Semgrep with multiple rulesets
        run: |
          semgrep scan \
            --config p/python \
            --config p/javascript \
            --config p/typescript \
            --config p/security-audit \
            --config p/owasp-top-ten \
            --config p/secrets \
            --config ./custom-rules/ \
            --sarif --output semgrep.sarif \
            --json --output semgrep.json

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif

      - name: Check for high severity findings
        run: |
          HIGH_COUNT=$(jq '[.results[] | select(.extra.severity == "ERROR")] | length' semgrep.json)
          if [ "$HIGH_COUNT" -gt 0 ]; then
            echo "Found $HIGH_COUNT high severity findings"
            jq '.results[] | select(.extra.severity == "ERROR") | {path: .path, line: .start.line, message: .extra.message}' semgrep.json
            exit 1
          fi

      - name: Generate report
        run: |
          echo "## Semgrep Security Scan Results" > security-report.md
          echo "" >> security-report.md
          echo "| Severity | Count |" >> security-report.md
          echo "|----------|-------|" >> security-report.md
          for sev in ERROR WARNING INFO; do
            COUNT=$(jq "[.results[] | select(.extra.severity == \"$sev\")] | length" semgrep.json)
            echo "| $sev | $COUNT |" >> security-report.md
          done

      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: semgrep-report
          path: |
            semgrep.sarif
            semgrep.json
            security-report.md
```

## CodeQL Advanced Configuration

### Custom CodeQL Queries

```ql
// queries/sql-injection.ql
/**
 * @name SQL injection
 * @description Building SQL queries from user input enables SQL injection
 * @kind path-problem
 * @problem.severity error
 * @security-severity 9.8
 * @precision high
 * @id py/sql-injection
 * @tags security
 *       external/cwe/cwe-89
 */

import python
import semmle.python.security.dataflow.SqlInjectionQuery
import DataFlow::PathGraph

from SqlInjectionConfiguration config, DataFlow::PathNode source, DataFlow::PathNode sink
where config.hasFlowPath(source, sink)
select sink.getNode(), source, sink, "SQL query depends on $@.", source.getNode(),
  "user-provided value"
```

```ql
// queries/hardcoded-credentials.ql
/**
 * @name Hardcoded credentials
 * @description Credentials stored in source code
 * @kind problem
 * @problem.severity error
 * @security-severity 9.0
 * @precision high
 * @id py/hardcoded-credentials
 * @tags security
 *       external/cwe/cwe-798
 */

import python

predicate isCredentialName(string name) {
  name.regexpMatch("(?i).*(password|passwd|pwd|secret|api_key|apikey|token|auth).*")
}

from Assign assign, Name target, StringLiteral value
where
  target = assign.getATarget() and
  value = assign.getValue() and
  isCredentialName(target.getId()) and
  value.getText().length() > 8 and
  not value.getText().regexpMatch("(?i).*(example|test|dummy|placeholder).*")
select assign, "Hardcoded credential assigned to variable '" + target.getId() + "'"
```

### CodeQL Query Suite

```yaml
# .github/codeql/security-extended.qls
- description: Extended security queries
- queries: .
- include:
    kind: problem
    tags contain: security
- include:
    kind: path-problem
    tags contain: security
- exclude:
    precision:
      - low
      - medium
```

### CodeQL Database Creation for Custom Builds

```yaml
# .github/workflows/codeql-custom.yml
name: CodeQL Custom Analysis
on:
  push:
    branches: [main]
  pull_request:

jobs:
  analyze:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        language: [python, javascript]

    steps:
      - uses: actions/checkout@v5

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          config-file: .github/codeql/codeql-config.yml
          queries: +security-extended,+security-and-quality

      # Custom build steps for compiled languages
      - name: Build Python package
        if: matrix.language == 'python'
        run: |
          pip install -e .
          pip install -r requirements.txt

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
          upload: true
          output: codeql-results
```

```yaml
# .github/codeql/codeql-config.yml
name: "CodeQL Security Config"

# Disable default queries and use specific ones
disable-default-queries: false

queries:
  - uses: security-extended
  - uses: security-and-quality
  - uses: ./custom-queries  # Local custom queries

# Additional paths to scan
paths:
  - src
  - lib

# Paths to exclude
paths-ignore:
  - tests
  - "**/test_*.py"
  - "**/*_test.go"
  - node_modules
  - vendor
```

## SonarQube Advanced Configuration

### Quality Profile Customization

```xml
<!-- sonar-quality-profile.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<profile>
  <name>Security-Focused</name>
  <language>py</language>
  <rules>
    <!-- SQL Injection -->
    <rule>
      <repositoryKey>python</repositoryKey>
      <key>S3649</key>
      <priority>BLOCKER</priority>
    </rule>
    <!-- Command Injection -->
    <rule>
      <repositoryKey>python</repositoryKey>
      <key>S4721</key>
      <priority>BLOCKER</priority>
    </rule>
    <!-- Hardcoded Credentials -->
    <rule>
      <repositoryKey>python</repositoryKey>
      <key>S2068</key>
      <priority>CRITICAL</priority>
    </rule>
    <!-- LDAP Injection -->
    <rule>
      <repositoryKey>python</repositoryKey>
      <key>S4817</key>
      <priority>BLOCKER</priority>
    </rule>
    <!-- XPath Injection -->
    <rule>
      <repositoryKey>python</repositoryKey>
      <key>S4817</key>
      <priority>CRITICAL</priority>
    </rule>
  </rules>
</profile>
```

### SonarQube Scanner Configuration

```properties
# sonar-project.properties
sonar.projectKey=my-project
sonar.projectName=My Project
sonar.projectVersion=1.0

# Source encoding
sonar.sourceEncoding=UTF-8

# Source code location
sonar.sources=src,lib
sonar.tests=tests

# Exclusions
sonar.exclusions=**/node_modules/**,**/*.min.js,**/vendor/**,**/migrations/**

# Test exclusions
sonar.test.exclusions=**/test_*.py,**/*_test.go

# Coverage
sonar.python.coverage.reportPaths=coverage.xml
sonar.javascript.lcov.reportPaths=coverage/lcov.info

# Security hotspots
sonar.security.hotspots.review.priority=HIGH,MEDIUM

# Branch analysis
sonar.branch.name=${GITHUB_REF_NAME}

# Pull request analysis
sonar.pullrequest.key=${GITHUB_PR_NUMBER}
sonar.pullrequest.branch=${GITHUB_HEAD_REF}
sonar.pullrequest.base=${GITHUB_BASE_REF}
```

### SonarQube Webhook for CI

```csharp
// SonarQube quality gate webhook handler - ASP.NET Core Minimal API
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<IQualityGateNotifier, QualityGateNotifier>();

var app = builder.Build();

app.MapPost("/sonar/webhook", async (
    HttpRequest request,
    [FromServices] IConfiguration config,
    [FromServices] IQualityGateNotifier notifier,
    [FromServices] ILogger<Program> logger) =>
{
    // Read raw body for signature verification
    request.EnableBuffering();
    using var reader = new StreamReader(request.Body, leaveOpen: true);
    var body = await reader.ReadToEndAsync();
    request.Body.Position = 0;

    // Verify webhook signature
    var signature = request.Headers["X-Sonar-Webhook-HMAC-SHA256"].FirstOrDefault();
    var secret = config["SonarQube:WebhookSecret"] ?? throw new InvalidOperationException("Webhook secret not configured");

    var expectedSignature = ComputeHmacSha256(body, secret);
    if (!CryptographicOperations.FixedTimeEquals(
        Encoding.UTF8.GetBytes(signature ?? ""),
        Encoding.UTF8.GetBytes(expectedSignature)))
    {
        return Results.Json(new { error = "Invalid signature" }, statusCode: 401);
    }

    // Parse webhook payload
    var data = JsonNode.Parse(body)?.AsObject();
    if (data is null)
        return Results.BadRequest(new { error = "Invalid JSON payload" });

    var project = data["project"]?.AsObject();
    var qualityGate = data["qualityGate"]?.AsObject();
    var status = qualityGate?["status"]?.GetValue<string>();
    var conditions = qualityGate?["conditions"]?.AsArray() ?? [];

    if (status == "ERROR")
    {
        // Quality gate failed - collect failed conditions
        var failedConditions = conditions
            .Where(c => c?["status"]?.GetValue<string>() == "ERROR")
            .Select(c => new FailedCondition(
                Metric: c?["metric"]?.GetValue<string>() ?? "unknown",
                Value: c?["value"]?.GetValue<string>() ?? "N/A",
                ErrorThreshold: c?["errorThreshold"]?.GetValue<string>() ?? "N/A"))
            .ToList();

        // Notify team (messaging platform, email, etc.)
        await notifier.NotifyQualityGateFailureAsync(
            project?["key"]?.GetValue<string>() ?? "unknown",
            failedConditions);

        // Block deployment if in CD pipeline
        // ... integration with deployment system
    }

    return Results.Json(new { status = "processed" });
});

app.Run();

static string ComputeHmacSha256(string data, string secret)
{
    using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
    var hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(data));
    return Convert.ToHexString(hash).ToLowerInvariant();
}

public sealed record FailedCondition(string Metric, string Value, string ErrorThreshold);

public interface IQualityGateNotifier
{
    Task NotifyQualityGateFailureAsync(string project, List<FailedCondition> conditions, CancellationToken ct = default);
}

public sealed class QualityGateNotifier(ILogger<QualityGateNotifier> logger) : IQualityGateNotifier
{
    public Task NotifyQualityGateFailureAsync(string project, List<FailedCondition> conditions, CancellationToken ct = default)
    {
        var message = new StringBuilder($"Quality Gate Failed for {project}\n\n");
        foreach (var condition in conditions)
        {
            message.AppendLine($"- {condition.Metric}: {condition.Value} (threshold: {condition.ErrorThreshold})");
        }

        // Send to messaging platform, email, etc.
        logger.LogWarning("Quality gate failure: {Message}", message.ToString());
        return Task.CompletedTask;
    }
}
```

## Tool Comparison Matrix

| Feature | Semgrep | CodeQL | SonarQube |
|---------|---------|--------|-----------|
| **Speed** | Fast | Slow (deep analysis) | Medium |
| **Language Support** | 30+ | 10+ | 25+ |
| **Custom Rules** | YAML (easy) | QL (complex) | Java (plugin) |
| **CI Integration** | Excellent | GitHub native | Good |
| **IDE Support** | VS Code, IntelliJ | VS Code | SonarLint |
| **Data Flow** | Pattern-based | Full taint tracking | Limited |
| **License** | LGPL (Community) | MIT (OSS) | LGPL (Community) |
| **Cloud Option** | Semgrep App | GitHub CodeQL | SonarCloud |
| **False Positive Rate** | Low | Very Low | Medium |
| **Setup Complexity** | Low | Medium | High |

## Integration Patterns

### Combined SAST Pipeline

```yaml
# .github/workflows/combined-sast.yml
name: Combined SAST Analysis
on:
  pull_request:
    branches: [main]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: semgrep/semgrep-action@v1
        with:
          config: auto
          generateSarif: true

      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
          category: semgrep

  codeql:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v5
      - uses: github/codeql-action/init@v3
        with:
          languages: python, javascript
      - uses: github/codeql-action/analyze@v3

  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0
      - uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

  aggregate:
    needs: [semgrep, codeql, sonarqube]
    runs-on: ubuntu-latest
    steps:
      - name: Check all passed
        run: |
          echo "All SAST tools completed successfully"
          # Add custom aggregation logic here
```
