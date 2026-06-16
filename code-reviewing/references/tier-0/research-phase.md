# Research Phase - Tier 0 (MANDATORY)

**Token Budget:** ~2,000 tokens | **Load Type:** Always-loaded (first step, mandatory)

This phase runs BEFORE any code analysis. Its purpose is to build an accurate understanding of the technology stack and current best practices using MCP servers. **This is not optional.**

## Core Rules

1. **Research BEFORE analysis** - Query MCP servers to understand current patterns before reviewing code
2. **Perplexity is ALWAYS required** - Training data is stale; always cross-validate
3. **Dual validation for Microsoft tech** - Always pair microsoft-learn with perplexity
4. **Every claim needs a source** - No finding without authoritative validation
5. **Exhaustive detection** - Scan ALL changed files for technology indicators

## When to Run

**ALWAYS.** Every code review starts with this research phase. There are no exceptions.

---

## Step 0a: Technology Detection

Scan ALL changed files to build a complete technology profile.

### Configuration Override Priority

Technology detection can be overridden or augmented by repository configuration. Check for config FIRST:

```text
Priority Chain (highest to lowest):

1. .claude/code-review.md "## Tech Stack" section
   └── Found: Use as AUTHORITATIVE tech stack (skip auto-detect for declared items)
   └── Items not declared: Fall through to auto-detect

2. Package manifests (*.csproj, package.json, requirements.txt, Cargo.toml, etc.)
   └── Parse for exact versions and dependencies
   └── Most reliable for version accuracy

3. File extension detection
   └── Fallback when manifests unavailable
   └── Lowest confidence for versions
```

**Why Config Override?**

- User may know their stack better than auto-detection
- Prevents false positives from test dependencies
- Allows declaring technologies not in changed files
- Enables targeted MCP queries with exact versions

### Checking for Config Override

**Step 1**: Check if `.claude/code-review.md` exists:

```bash
ls .claude/code-review.md 2>/dev/null
```

**Step 2**: If exists, read and extract `## Tech Stack` section:

```markdown
## Tech Stack

- **Runtime**: .NET 10
- **Frameworks**: ASP.NET Core 10, Entity Framework Core 10
- **Packages**: MediatR 12, FluentValidation 11, Polly 8
- **Frontend**: React 19, TypeScript 5.7
- **Database**: SQL Server 2022
```

**Step 3**: Parse config tech stack:

- Each line starting with `- **` is a category
- Text before `:` is the category name
- Text after `:` contains technologies (comma-separated)

**Step 4**: For declared items, skip auto-detection and use config values directly.

**Step 5**: For categories NOT declared, proceed with auto-detection below.

### File Extension Detection

| Extension | Technology | MCP Route |
| --- | --- | --- |
| `.cs`, `.csproj`, `.sln` | .NET/C# | microsoft-learn + perplexity |
| `.fs`, `.fsproj` | F# | microsoft-learn + perplexity |
| `.vb`, `.vbproj` | VB.NET | microsoft-learn + perplexity |
| `.ts`, `.tsx` | TypeScript | context7 + ref |
| `.js`, `.jsx` | JavaScript | context7 + ref |
| `.py` | Python | context7 + ref |
| `.go`, `go.mod` | Go | context7 + ref |
| `.rs`, `Cargo.toml` | Rust | context7 + ref |
| `.java`, `pom.xml`, `build.gradle` | Java | context7 + ref |
| `.rb`, `Gemfile` | Ruby | context7 + ref |
| `.php` | PHP | context7 + ref |
| `Dockerfile`, `docker-compose.yml` | Docker | perplexity |
| `.tf`, `.tfvars` | Terraform | perplexity |
| `.bicep`, `.arm.json` | Azure IaC | microsoft-learn + perplexity |
| `azure-pipelines.yml` | Azure DevOps | microsoft-learn + perplexity |
| `.github/workflows/**` | GitHub Actions | context7 + perplexity |

### Package Manifest Detection

| File | Extract | Technology |
| --- | --- | --- |
| `*.csproj` | `<TargetFramework>`, `<PackageReference>` | .NET version, NuGet packages |
| `package.json` | `dependencies`, `devDependencies` | npm packages |
| `requirements.txt`, `pyproject.toml` | package list | Python packages |
| `go.mod` | `require` statements | Go modules |
| `Cargo.toml` | `[dependencies]` | Rust crates |
| `pom.xml`, `build.gradle` | dependency blocks | Java/Maven/Gradle |
| `Gemfile` | gem declarations | Ruby gems |

### Import Statement Detection

Scan source files for import statements to identify frameworks:

| Language | Pattern | Extract |
| --- | --- | --- |
| C# | `using Microsoft.*` | ASP.NET Core, Azure SDK, EF Core |
| C# | `using System.Text.Json` | JSON serialization patterns |
| TypeScript | `import * from 'react'` | React framework |
| TypeScript | `import { Injectable } from '@angular/core'` | Angular framework |
| Python | `from django.* import` | Django framework |
| Python | `from flask import` | Flask framework |
| Python | `import fastapi` | FastAPI framework |

### Framework Detection Patterns

| Indicator | Framework | Version Detection |
| --- | --- | --- |
| `Program.cs` + `app.MapGet` | ASP.NET Minimal API | `<TargetFramework>` |
| `Startup.cs` + `services.AddMvc` | ASP.NET MVC | `<TargetFramework>` |
| `next.config.js` | Next.js | `package.json` |
| `nuxt.config.ts` | Nuxt.js | `package.json` |
| `App.tsx` + `react-dom` | React | `package.json` |
| `angular.json` | Angular | `package.json` |
| `manage.py` + `django.*` | Django | `requirements.txt` |

---

## Step 0b: MCP Research Queries

Based on the Technology Profile from Step 0a, query appropriate MCP servers. **Run queries in parallel where possible.**

### Microsoft Technologies (.NET, Azure, C#, F#)

#### Dual Validation with Perplexity

```text
PARALLEL BATCH 1:
  microsoft-learn: microsoft_docs_search("{framework} {version} best practices")
  microsoft-learn: microsoft_code_sample_search("{framework} {api}", language="csharp")
  perplexity: search("{framework} latest version patterns December 2025")

PARALLEL BATCH 2:
  microsoft-learn: microsoft_docs_search("{framework} security patterns")
  perplexity: search("{framework} breaking changes {detected-version}")
```

**High-Risk Technologies (Extra Validation Required):**

| Technology | Risk | Additional Query |
| --- | --- | --- |
| .NET 10 | HIGH (very new) | perplexity: ".NET 10 known issues December 2025" |
| .NET Aspire | HIGH (fast-moving) | perplexity: ".NET Aspire latest version December 2025" |
| Azure AI Foundry | HIGH (new platform) | perplexity: "Azure AI Foundry current patterns 2025" |
| Hybrid Cache | HIGH (new in .NET 9/10) | perplexity: "HybridCache .NET 10 patterns" |
| Microsoft.Extensions.AI | HIGH (new) | perplexity: "Microsoft.Extensions.AI patterns December 2025" |

### npm/PyPI/Other Package Ecosystems

```text
PARALLEL:
  context7: resolve-library-id("{package-name}")

THEN (with resolved ID):
  context7: query-docs(id="{resolved-id}", topic="{relevant-topic}", mode="code")

OPTIONAL (cross-reference):
  ref: ref_search_documentation("{package} {api} documentation")
  perplexity: search("{package} security vulnerabilities 2025")
```

### Security-Sensitive Code Detection

When code contains security patterns (auth, crypto, secrets), query OWASP:

```text
PARALLEL:
  perplexity: search("OWASP {category} prevention best practices 2025")
  perplexity: reason("Compare {implementation} against OWASP guidelines")
```

| Security Pattern Detected | Query Template |
| --- | --- |
| password, bcrypt, argon2, hash | "OWASP password storage 2025" |
| jwt, token, oauth, auth | "{framework} authentication OWASP 2025" |
| sql, query, DbContext | "SQL injection prevention {framework} 2025" |
| encrypt, decrypt, AES, RSA | "cryptography best practices 2025" |
| CORS, headers, CSP | "OWASP security headers 2025" |

### Version Validation Queries

**Always validate version claims with perplexity:**

```text
perplexity: search("{package} latest stable version December 2025")
perplexity: search("{framework} {detected-version} deprecated features")
perplexity: search("{library} version {X} end of life")
```

---

## Step 0c: Build Current Truth Context

From MCP responses, extract and store the following for use during analysis:

### Technology Profile Output

```markdown
## Technology Research Summary

### Configuration Source

**Config File**: `.claude/code-review.md` (found) | CLAUDE.md (fallback) | None (auto-detect only)
**Override Active**: Yes/No

### Detected Stack

| Category | Technology | Version | Source | Detection |
| --- | --- | --- | --- | --- |
| Runtime | .NET | 10 | .claude/code-review.md | config override |
| Framework | ASP.NET Core | 10 | .claude/code-review.md | config override |
| ORM | Entity Framework Core | 10 | *.csproj | manifest |
| Frontend | React | 19 | package.json | manifest |
| Auth | IdentityServer | - | PackageReference | manifest |

### Current Best Practices (MCP-Validated)

| Area | Current Recommendation | Source |
| --- | --- | --- |
| Password Hashing | Argon2id preferred, bcrypt cost 12+ acceptable | perplexity (OWASP) |
| .NET DI | AddScoped for request-scoped services | microsoft-learn |
| EF Core Queries | Use compiled queries for hot paths | microsoft-learn + perplexity |
| React State | useReducer for complex state, Zustand/Jotai for global | context7 |

### Version Validation

| Package | Detected | Current Stable | Status | Source |
| --- | --- | --- | --- | --- |
| .NET | 10 | 10 | Current | perplexity |
| React | 18.2 | 19.0 | Outdated | perplexity |
| EF Core | 9.0 | 10.0 | Outdated | perplexity |

### Security Baseline (OWASP-Validated)

| Category | Requirement | Source |
| --- | --- | --- |
| Authentication | Use standard libraries, not custom impl | OWASP via perplexity |
| Passwords | Argon2id/bcrypt, min cost 12, salt per user | OWASP via perplexity |
| SQL | Parameterized queries only, no string concat | OWASP via perplexity |
| JWT | Validate alg, exp, iss, aud; use asymmetric keys | OWASP via perplexity |
```

---

## MCP Query Best Practices

### Parallel Query Strategy

Group independent queries for efficiency:

```text
BATCH 1 (can run in parallel):
- microsoft-learn queries (technology-specific)
- context7 library resolution
- perplexity security queries

BATCH 2 (after Batch 1):
- context7 docs fetch (needs resolved IDs from Batch 1)
- perplexity validation queries
- ref API lookups
```

### Query Formulation Tips

| Goal | Query Pattern |
| --- | --- |
| Current version | "{package} latest stable version December 2025" |
| Best practices | "{framework} {topic} best practices 2025" |
| Security | "OWASP {category} {framework} prevention" |
| Breaking changes | "{framework} {version} breaking changes from {previous}" |
| Deprecation | "{api} deprecated alternative {framework}" |

### MCP Server Capabilities

| MCP Server | Best For | Limitations |
| --- | --- | --- |
| microsoft-learn | MS tech docs, code samples | Can return stale docs, always pair with perplexity |
| perplexity | Current info, versions, security | Rate limited, use for validation |
| context7 | Library docs, API reference | Needs library ID resolution first |
| ref | API documentation | Good for specific method signatures |
| firecrawl | Custom docs, non-standard sources | Use as fallback |

---

## Error Handling

### MCP Server Unavailable

```markdown
## Research Phase Status

**Status**: Partial
**Available**: microsoft-learn, context7
**Unavailable**: perplexity, ref

**Impact**: Version validation incomplete. Findings without perplexity
cross-validation should be treated as lower confidence.

**Recommendation**: Manual verification required for:
- Version recommendations
- Security pattern validation
- Breaking change detection
```

### No Technologies Detected

If no external frameworks/libraries detected:

```markdown
## Research Phase Status

**Status**: Not applicable
**Reason**: No external library/framework usage detected

This review focuses on internal/proprietary code patterns that do not
require external MCP validation. Standard code quality checks apply.
```

---

## Integration with Analysis Phase

The Technology Profile and Current Truth Context from this phase inform all subsequent analysis:

1. **Step 4 (Universal Checks)**: Compare code against OWASP baseline from Step 0c
2. **Step 5 (Repo Checks)**: Validate patterns against detected framework versions
3. **Step 6 (Report)**: Include MCP validation status for every finding
4. **Step 7 (Fixes)**: Recommend fixes based on current best practices from Step 0c

### Every Finding Must Reference Research

```markdown
### [Issue Title]

**File**: `path/to/file.ext:line`
**Severity**: CRITICAL

**Problem**: [Description]

**Validation**: MCP-Validated - Yes
**Source**: [Specific source from research phase] [mcp-server]
**Research Reference**: See "Current Best Practices" table, row X
```

---

## Quick Reference

### Mandatory Queries

| Detected Technology | Required Queries | Perplexity Required |
| --- | --- | --- |
| Any .NET | microsoft-learn + perplexity | YES (ALWAYS) |
| Any Azure | microsoft-learn + perplexity | YES (ALWAYS) |
| Security patterns | perplexity (OWASP) | YES (ALWAYS) |
| Version claims | perplexity | YES (ALWAYS) |
| npm packages | context7 | Recommended |
| Python packages | context7 | Recommended |
| Internal code | None | No |

### Token Budget

| Phase Component | Est. Tokens |
| --- | --- |
| Technology detection | ~200 |
| MCP query overhead | ~300 |
| Technology Profile storage | ~500 |
| Current Truth Context | ~800 |
| **Total** | **~1,800** |

---

**Last Updated:** 2025-12-29
