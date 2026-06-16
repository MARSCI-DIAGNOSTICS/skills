# Security Gates Reference

Comprehensive implementation guide for security gates in CI/CD pipelines.

## Gate Architecture

### Pipeline Security Gate Flow

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                         Security Gate Pipeline                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐             │
│  │  SAST   │    │   SCA   │    │ Secrets │    │ License │             │
│  │ Semgrep │    │  Snyk   │    │Gitleaks │    │  Check  │             │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘             │
│       │              │              │              │                   │
│       └──────────────┴──────────────┴──────────────┘                   │
│                              │                                         │
│                              ▼                                         │
│                    ┌─────────────────┐                                 │
│                    │  Aggregator &   │                                 │
│                    │  Policy Engine  │                                 │
│                    └────────┬────────┘                                 │
│                             │                                          │
│              ┌──────────────┼──────────────┐                          │
│              ▼              ▼              ▼                          │
│         ┌────────┐    ┌─────────┐    ┌─────────┐                      │
│         │  PASS  │    │  WARN   │    │  FAIL   │                      │
│         └────────┘    └─────────┘    └─────────┘                      │
│                             │              │                          │
│                             ▼              ▼                          │
│                       ┌─────────┐    ┌─────────┐                      │
│                       │ Notify  │    │  Block  │                      │
│                       │  Team   │    │ Deploy  │                      │
│                       └─────────┘    └─────────┘                      │
│                                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Complete Gate Implementation

### Policy Configuration

```yaml
# security-policy.yml
version: "1.0"

# Global settings
settings:
  fail_on_error: true
  allow_bypass: false
  bypass_approvers:
    - security-team
    - cto

# Gate configurations by environment
environments:
  development:
    sast:
      critical: warn
      high: warn
      medium: ignore
    sca:
      critical: warn
      high: ignore
    secrets:
      action: warn
    licenses:
      action: ignore

  staging:
    sast:
      critical: fail
      high: warn
      medium: ignore
    sca:
      critical: fail
      high: warn
      cvss_threshold: 8.0
    secrets:
      action: fail
    licenses:
      action: warn
      forbidden:
        - GPL-3.0
        - AGPL-3.0

  production:
    sast:
      critical: fail
      high: fail
      medium: warn
    sca:
      critical: fail
      high: fail
      medium: warn
      cvss_threshold: 7.0
    secrets:
      action: fail
    licenses:
      action: fail
      forbidden:
        - GPL-3.0
        - AGPL-3.0
        - LGPL-3.0
    dast:
      critical: fail
      high: fail
```

### Gate Engine Implementation

```csharp
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using YamlDotNet.Serialization;

/// <summary>
/// Security gate engine for CI/CD pipelines.
/// </summary>
public enum GateAction { Pass, Warn, Fail, Ignore }
public enum FindingSeverity { Critical, High, Medium, Low, Info }

public sealed record Finding(
    string Scanner,
    FindingSeverity Severity,
    string Title,
    string Description,
    string? Location = null,
    string? Cwe = null,
    string? Cve = null,
    double? Cvss = null,
    bool FixAvailable = false);

public sealed class GateResult
{
    public GateAction Action { get; set; } = GateAction.Pass;
    public List<Finding> Findings { get; set; } = [];
    public List<string> Reasons { get; set; } = [];
    public Dictionary<string, Dictionary<string, int>> Metrics { get; set; } = [];
    public int SecretsCount { get; set; }
}

public sealed class PolicyConfig
{
    public GateAction SastCritical { get; init; } = GateAction.Fail;
    public GateAction SastHigh { get; init; } = GateAction.Fail;
    public GateAction SastMedium { get; init; } = GateAction.Warn;
    public GateAction ScaCritical { get; init; } = GateAction.Fail;
    public GateAction ScaHigh { get; init; } = GateAction.Warn;
    public double ScaCvssThreshold { get; init; } = 7.0;
    public GateAction SecretsAction { get; init; } = GateAction.Fail;
    public GateAction LicenseAction { get; init; } = GateAction.Warn;
    public HashSet<string> ForbiddenLicenses { get; init; } = [];
    public GateAction DastCritical { get; init; } = GateAction.Fail;
    public GateAction DastHigh { get; init; } = GateAction.Fail;

    public static PolicyConfig FromYaml(string configPath, string environment)
    {
        var yaml = File.ReadAllText(configPath);
        var deserializer = new DeserializerBuilder().Build();
        var config = deserializer.Deserialize<Dictionary<string, object>>(yaml);

        var envConfig = GetNestedDict(config, "environments", environment);
        var sast = GetNestedDict(envConfig, "sast");
        var sca = GetNestedDict(envConfig, "sca");
        var secrets = GetNestedDict(envConfig, "secrets");
        var licenses = GetNestedDict(envConfig, "licenses");
        var dast = GetNestedDict(envConfig, "dast");

        return new PolicyConfig
        {
            SastCritical = ParseAction(sast, "critical", GateAction.Fail),
            SastHigh = ParseAction(sast, "high", GateAction.Fail),
            SastMedium = ParseAction(sast, "medium", GateAction.Warn),
            ScaCritical = ParseAction(sca, "critical", GateAction.Fail),
            ScaHigh = ParseAction(sca, "high", GateAction.Warn),
            ScaCvssThreshold = GetDouble(sca, "cvss_threshold", 7.0),
            SecretsAction = ParseAction(secrets, "action", GateAction.Fail),
            LicenseAction = ParseAction(licenses, "action", GateAction.Warn),
            ForbiddenLicenses = GetStringList(licenses, "forbidden").ToHashSet(),
            DastCritical = ParseAction(dast, "critical", GateAction.Fail),
            DastHigh = ParseAction(dast, "high", GateAction.Fail)
        };
    }

    private static Dictionary<string, object> GetNestedDict(
        Dictionary<string, object>? dict, params string[] keys)
    {
        var current = dict;
        foreach (var key in keys)
        {
            if (current?.TryGetValue(key, out var value) == true &&
                value is Dictionary<object, object> nested)
                current = nested.ToDictionary(k => k.Key.ToString()!, v => v.Value);
            else
                return [];
        }
        return current ?? [];
    }

    private static GateAction ParseAction(Dictionary<string, object>? dict, string key, GateAction def) =>
        dict?.TryGetValue(key, out var v) == true && Enum.TryParse<GateAction>(v?.ToString(), true, out var a) ? a : def;

    private static double GetDouble(Dictionary<string, object>? dict, string key, double def) =>
        dict?.TryGetValue(key, out var v) == true && double.TryParse(v?.ToString(), out var d) ? d : def;

    private static List<string> GetStringList(Dictionary<string, object>? dict, string key) =>
        dict?.TryGetValue(key, out var v) == true && v is List<object> list
            ? list.Select(x => x.ToString()!).ToList() : [];
}

public sealed class SecurityGateEngine(PolicyConfig policy)
{
    private readonly List<Finding> _findings = [];
    private readonly HashSet<string> _licenses = [];

    private static readonly HashSet<string> SastScanners = ["semgrep", "codeql", "sonarqube"];
    private static readonly HashSet<string> ScaScanners = ["npm-audit", "snyk", "pip-audit", "dotnet-audit"];
    private static readonly HashSet<string> DastScanners = ["zap", "burp"];

    public void LoadSarif(string sarifPath, string scanner = "unknown")
    {
        var json = File.ReadAllText(sarifPath);
        var sarif = JsonNode.Parse(json);

        foreach (var run in sarif?["runs"]?.AsArray() ?? [])
        {
            var toolName = run?["tool"]?["driver"]?["name"]?.GetValue<string>() ?? scanner;

            foreach (var result in run?["results"]?.AsArray() ?? [])
            {
                var severity = SarifToSeverity(result?["level"]?.GetValue<string>() ?? "warning");
                string? location = null;

                var locations = result?["locations"]?.AsArray();
                if (locations?.Count > 0)
                {
                    var loc = locations[0]?["physicalLocation"];
                    var artifact = loc?["artifactLocation"]?["uri"]?.GetValue<string>() ?? "";
                    var line = loc?["region"]?["startLine"]?.GetValue<int>() ?? 0;
                    location = $"{artifact}:{line}";
                }

                string? cwe = null;
                var tags = result?["properties"]?["tags"]?.AsArray();
                if (tags is not null)
                    cwe = tags.Select(t => t?.GetValue<string>()).FirstOrDefault(t => t?.StartsWith("CWE-") == true);

                _findings.Add(new Finding(
                    Scanner: toolName,
                    Severity: severity,
                    Title: result?["ruleId"]?.GetValue<string>() ?? "Unknown",
                    Description: result?["message"]?["text"]?.GetValue<string>() ?? "",
                    Location: location,
                    Cwe: cwe));
            }
        }
    }

    public void LoadNpmAudit(string auditPath)
    {
        var json = File.ReadAllText(auditPath);
        var audit = JsonNode.Parse(json);

        foreach (var (name, vuln) in audit?["vulnerabilities"]?.AsObject() ?? [])
        {
            var severityStr = vuln?["severity"]?.GetValue<string>() ?? "low";
            var severity = Enum.TryParse<FindingSeverity>(severityStr, true, out var s) ? s : FindingSeverity.Low;

            foreach (var via in vuln?["via"]?.AsArray() ?? [])
            {
                if (via is JsonObject viaObj)
                {
                    _findings.Add(new Finding(
                        Scanner: "npm-audit",
                        Severity: severity,
                        Title: viaObj["title"]?.GetValue<string>() ?? name,
                        Description: viaObj["url"]?.GetValue<string>() ?? "",
                        Cve: viaObj["cve"]?.GetValue<string>(),
                        Cvss: viaObj["cvss"]?["score"]?.GetValue<double>(),
                        FixAvailable: vuln?["fixAvailable"]?.GetValue<bool>() ?? false));
                }
            }
        }
    }

    public void LoadGitleaks(string gitleaksPath)
    {
        var json = File.ReadAllText(gitleaksPath);
        var findings = JsonNode.Parse(json)?.AsArray() ?? [];

        foreach (var finding in findings)
        {
            _findings.Add(new Finding(
                Scanner: "gitleaks",
                Severity: FindingSeverity.Critical,
                Title: finding?["RuleID"]?.GetValue<string>() ?? "Secret",
                Description: $"Secret found in {finding?["File"]?.GetValue<string>() ?? "unknown"}",
                Location: $"{finding?["File"]?.GetValue<string>()}:{finding?["StartLine"]?.GetValue<int>()}"));
        }
    }

    public void LoadLicenseScan(string licensePath)
    {
        var json = File.ReadAllText(licensePath);
        var data = JsonNode.Parse(json);

        foreach (var package in data?["packages"]?.AsArray() ?? [])
        {
            var license = package?["license"]?.GetValue<string>() ?? "Unknown";
            _licenses.Add(license);
        }
    }

    public GateResult Evaluate()
    {
        var result = new GateResult { Findings = [.. _findings] };

        var counts = new Dictionary<string, Dictionary<string, int>>
        {
            ["sast"] = new() { ["critical"] = 0, ["high"] = 0, ["medium"] = 0, ["low"] = 0 },
            ["sca"] = new() { ["critical"] = 0, ["high"] = 0, ["medium"] = 0, ["low"] = 0 },
            ["dast"] = new() { ["critical"] = 0, ["high"] = 0, ["medium"] = 0, ["low"] = 0 }
        };
        var secretsCount = 0;

        foreach (var finding in _findings)
        {
            var sev = finding.Severity.ToString().ToLowerInvariant();

            if (SastScanners.Contains(finding.Scanner))
                counts["sast"][sev]++;
            else if (ScaScanners.Contains(finding.Scanner))
                counts["sca"][sev]++;
            else if (finding.Scanner == "gitleaks")
                secretsCount++;
            else if (DastScanners.Contains(finding.Scanner))
                counts["dast"][sev]++;
        }

        result.Metrics = counts;
        result.SecretsCount = secretsCount;

        // Evaluate thresholds
        EvaluateThreshold(result, "SAST Critical", counts["sast"]["critical"], 0, policy.SastCritical);
        EvaluateThreshold(result, "SAST High", counts["sast"]["high"], 0, policy.SastHigh);
        EvaluateThreshold(result, "SAST Medium", counts["sast"]["medium"], 5, policy.SastMedium);
        EvaluateThreshold(result, "SCA Critical", counts["sca"]["critical"], 0, policy.ScaCritical);
        EvaluateThreshold(result, "SCA High", counts["sca"]["high"], 0, policy.ScaHigh);

        var highCvss = _findings.Count(f => ScaScanners.Contains(f.Scanner) && f.Cvss >= policy.ScaCvssThreshold);
        if (highCvss > 0)
            EvaluateThreshold(result, $"SCA CVSS >= {policy.ScaCvssThreshold}", highCvss, 0, GateAction.Fail);

        if (secretsCount > 0)
            EvaluateThreshold(result, "Secrets", secretsCount, 0, policy.SecretsAction);

        var forbidden = _licenses.Intersect(policy.ForbiddenLicenses).ToList();
        if (forbidden.Count > 0)
            EvaluateThreshold(result, $"Forbidden Licenses ({string.Join(", ", forbidden)})", forbidden.Count, 0, policy.LicenseAction);

        EvaluateThreshold(result, "DAST Critical", counts["dast"]["critical"], 0, policy.DastCritical);
        EvaluateThreshold(result, "DAST High", counts["dast"]["high"], 0, policy.DastHigh);

        return result;
    }

    private static void EvaluateThreshold(GateResult result, string checkName, int count, int threshold, GateAction action)
    {
        if (count <= threshold) return;

        if (action == GateAction.Fail)
        {
            result.Action = GateAction.Fail;
            result.Reasons.Add($"FAIL: {checkName} = {count} (threshold: {threshold})");
        }
        else if (action == GateAction.Warn)
        {
            if (result.Action != GateAction.Fail)
                result.Action = GateAction.Warn;
            result.Reasons.Add($"WARN: {checkName} = {count} (threshold: {threshold})");
        }
    }

    private static FindingSeverity SarifToSeverity(string level) => level switch
    {
        "error" => FindingSeverity.High,
        "warning" => FindingSeverity.Medium,
        "note" => FindingSeverity.Low,
        _ => FindingSeverity.Info
    };
}

public static class SecurityGateReport
{
    public static string GenerateMarkdown(GateResult result)
    {
        var sb = new StringBuilder();
        sb.AppendLine("# Security Gate Report");
        sb.AppendLine();
        sb.AppendLine($"## Status: {result.Action.ToString().ToUpperInvariant()}");
        sb.AppendLine();

        if (result.Reasons.Count > 0)
        {
            sb.AppendLine("## Findings Summary");
            sb.AppendLine();
            foreach (var reason in result.Reasons)
                sb.AppendLine($"- {reason}");
            sb.AppendLine();
        }

        sb.AppendLine("## Metrics");
        sb.AppendLine();
        sb.AppendLine("| Scanner | Critical | High | Medium | Low |");
        sb.AppendLine("|---------|----------|------|--------|-----|");

        foreach (var scanner in new[] { "sast", "sca", "dast" })
        {
            var m = result.Metrics.GetValueOrDefault(scanner, []);
            sb.AppendLine($"| {scanner.ToUpperInvariant()} | {m.GetValueOrDefault("critical")} | {m.GetValueOrDefault("high")} | {m.GetValueOrDefault("medium")} | {m.GetValueOrDefault("low")} |");
        }

        if (result.SecretsCount > 0)
        {
            sb.AppendLine();
            sb.AppendLine($"**Secrets Found:** {result.SecretsCount}");
        }

        return sb.ToString();
    }
}

// CLI usage
var policy = File.Exists("security-policy.yml")
    ? PolicyConfig.FromYaml("security-policy.yml", "staging")
    : new PolicyConfig();

var engine = new SecurityGateEngine(policy);

foreach (var sarif in Directory.GetFiles(".", "*.sarif"))
    engine.LoadSarif(sarif);

if (File.Exists("npm-audit.json"))
    engine.LoadNpmAudit("npm-audit.json");

if (File.Exists("gitleaks.json"))
    engine.LoadGitleaks("gitleaks.json");

var result = engine.Evaluate();
var report = SecurityGateReport.GenerateMarkdown(result);

await File.WriteAllTextAsync("security-report.md", report);
Console.WriteLine(report);

return result.Action == GateAction.Fail ? 1 : 0;
```

## GitHub Actions Complete Gate

```yaml
# .github/workflows/security-gate.yml
name: Security Gate
on:
  pull_request:
    branches: [main, release/*]
  push:
    branches: [main]

env:
  ENVIRONMENT: ${{ github.event_name == 'push' && 'production' || 'staging' }}

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: auto
          generateSarif: true

      - name: Upload SARIF
        uses: actions/upload-artifact@v4
        with:
          name: sast-sarif
          path: semgrep.sarif

  sca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: npm audit
        if: hashFiles('package-lock.json') != ''
        run: |
          npm audit --json > npm-audit.json || true

      - name: pip-audit
        if: hashFiles('requirements.txt') != ''
        run: |
          pip install pip-audit
          pip-audit -r requirements.txt --format json > pip-audit.json || true

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: sca-results
          path: |
            npm-audit.json
            pip-audit.json

  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        continue-on-error: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_ENABLE_COMMENTS: false

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: secrets-results
          path: gitleaks-report.json
        if: always()

  licenses:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: License check
        run: |
          npm install -g license-checker
          license-checker --json > licenses.json

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: license-results
          path: licenses.json

  evaluate:
    needs: [sast, sca, secrets, licenses]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: scan-results

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyyaml

      - name: Evaluate Security Gate
        id: gate
        run: |
          python scripts/security_gate.py \
            --policy security-policy.yml \
            --environment ${{ env.ENVIRONMENT }} \
            --sarif scan-results/sast-sarif/semgrep.sarif \
            --npm-audit scan-results/sca-results/npm-audit.json \
            --gitleaks scan-results/secrets-results/gitleaks-report.json \
            --licenses scan-results/license-results/licenses.json \
            --output security-report.md

      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: security-report.md

      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('security-report.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: report
            });
```

## Break Glass Procedure

### Emergency Bypass Workflow

```yaml
# .github/workflows/bypass-gate.yml
name: Security Gate Bypass
on:
  workflow_dispatch:
    inputs:
      reason:
        description: 'Reason for bypass'
        required: true
      approver:
        description: 'Security team approver'
        required: true
      ticket:
        description: 'Associated ticket number'
        required: true
      expiry_hours:
        description: 'Bypass expiry (hours)'
        required: true
        default: '24'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Verify approver
        run: |
          ALLOWED_APPROVERS="security-lead,cto,vp-engineering"
          if [[ ! ",${ALLOWED_APPROVERS}," =~ ",${{ github.event.inputs.approver }}," ]]; then
            echo "Error: ${{ github.event.inputs.approver }} is not authorized"
            exit 1
          fi

      - name: Create bypass record
        run: |
          cat << EOF > bypass-record.json
          {
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "requester": "${{ github.actor }}",
            "approver": "${{ github.event.inputs.approver }}",
            "reason": "${{ github.event.inputs.reason }}",
            "ticket": "${{ github.event.inputs.ticket }}",
            "expiry": "$(date -u -d '+${{ github.event.inputs.expiry_hours }} hours' +%Y-%m-%dT%H:%M:%SZ)",
            "commit": "${{ github.sha }}"
          }
          EOF

      - name: Store bypass
        run: |
          # Store in secure location (e.g., S3, Vault)
          aws s3 cp bypass-record.json s3://security-audit-trail/bypasses/

      - name: Notify security team
        run: |
          # Send notification to security team
          echo "Security gate bypass requested by ${{ github.actor }}"
```
