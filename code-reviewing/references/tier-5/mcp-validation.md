# MCP Validation Reference (MANDATORY)

**Token Budget:** ~2,000 tokens | **Load Type:** Context-dependent (integrated with Research Phase)

**CRITICAL:** MCP validation is MANDATORY for all code reviews. Use this reference in conjunction with the Research Phase (Tier 0). Every finding MUST include validation status.

## Core Rules (NON-NEGOTIABLE)

1. **Research BEFORE analysis** - Query MCP servers to understand current patterns before reviewing code
2. **Perplexity is ALWAYS required** - Training data is stale; always cross-validate with perplexity
3. **Dual validation for Microsoft tech** - ALWAYS pair microsoft-learn with perplexity
4. **Every claim needs a source** - No finding without authoritative validation
5. **Exhaustive detection** - Scan ALL changed files for technology indicators

## Validation Requirements Matrix

| Code Pattern | Perplexity Required | Why |
| --- | --- | --- |
| Any .NET/Azure code | YES (ALWAYS) | Dual validation with microsoft-learn |
| Security patterns | YES (ALWAYS) | OWASP changes, evolving best practices |
| Version claims | YES (ALWAYS) | Training data cutoff makes versions stale |
| Deprecation warnings | YES (ALWAYS) | APIs sunset frequently |
| OWASP references | YES (ALWAYS) | Security guidance evolves |
| npm/PyPI packages | Recommended | Frequent version updates |
| Internal/proprietary code | No | No public documentation exists |

## Technology Detection Matrix

Detect technologies from file patterns and route to appropriate MCP:

| File Pattern | Technology | Primary MCP | Secondary MCP |
| --- | --- | --- | --- |
| *.cs,*.csproj, *.sln | .NET/C# | microsoft-learn | **perplexity (ALWAYS)** |
| *.fs,*.fsproj | F# | microsoft-learn | **perplexity (ALWAYS)** |
| Program.cs with Azure.* | Azure SDK | microsoft-learn | **perplexity (ALWAYS)** |
| *.py, requirements.txt, pyproject.toml | Python | context7 + ref | perplexity |
| *.ts,*.tsx, package.json | TypeScript | context7 + ref | perplexity |
| *.js,*.jsx, package.json | JavaScript | context7 + ref | perplexity |
| *.go, go.mod | Go | context7 + ref | perplexity |
| *.rs, Cargo.toml | Rust | context7 + ref | perplexity |
| *.java, pom.xml, build.gradle | Java | context7 + ref | perplexity |
| *.rb, Gemfile | Ruby | context7 + ref | perplexity |
| Dockerfile, docker-compose.yml | Docker | perplexity | firecrawl |
| *.tf,*.tfvars | Terraform | perplexity | firecrawl |
| azure-pipelines.yml | Azure DevOps | microsoft-learn | perplexity |
| .github/workflows/** | GitHub Actions | context7 | perplexity |

## CRITICAL: microsoft-learn Staleness Warning

The microsoft-learn MCP server caches documentation and may return **outdated information** - not just version numbers, but also API patterns, configuration examples, and best practices.

**Mandatory Dual-Validation Protocol for ALL Microsoft Technology Findings:**

1. Query microsoft-learn for API patterns and code examples
2. **IMMEDIATELY query perplexity**: `"{technology} latest version patterns December 2025"`
3. If ANY discrepancy:
   - Trust perplexity for version numbers and release dates
   - Cross-reference API patterns - perplexity may have more current info
   - Document which source was used for which information
4. When information matches, proceed with confidence

**High-Risk Technologies (Extra Scrutiny Required):**

| Technology | Risk Level | Why |
| --- | --- | --- |
| .NET 10 | HIGH | Very new, docs evolving rapidly |
| .NET Aspire | HIGH | Major version jumps, fast-moving |
| Azure AI Foundry | HIGH | New platform, frequent changes |
| Hybrid Cache | HIGH | New in .NET 9/10, patterns evolving |

## Content Pattern Detection

Detect patterns in code content for specialized validation:

| Content Pattern | Validation Focus | Query Template |
| --- | --- | --- |
| password, bcrypt, argon2, hash | Password hashing | perplexity: "password hashing best practices 2025" |
| jwt, token, oauth, auth | Authentication | perplexity: "{framework} authentication best practices 2025" |
| sql, query, DbContext | SQL/ORM | perplexity: "{framework} SQL injection prevention" |
| async, await, Task, Promise | Async patterns | context7: {library} async patterns |
| cache, redis, IDistributedCache | Caching | perplexity: "{technology} caching best practices" |
| rate limit, throttle | Rate limiting | perplexity: "rate limiting patterns {technology}" |

## MCP Query Templates

### Microsoft Technologies

```text
# Primary query
microsoft_docs_search: ".NET 10 {topic} best practices"

# Code samples (optional)
microsoft_code_sample_search: "{API} example" + language="csharp"

# MANDATORY validation
perplexity_search: ".NET 10 {topic} December 2025 latest"
```

### Library/Package Validation

```text
# Step 1: Resolve library ID
context7_resolve-library-id: "{package-name}"

# Step 2: Get docs with topic
context7_query-docs:
  context7CompatibleLibraryID: "{resolved-id}"
  topic: "{specific-topic}"
  mode: "code"

# Optional: Cross-reference
ref_search_documentation: "{package} {API} documentation"
```

### Security Validation

```text
perplexity_search: "OWASP {vulnerability} prevention 2025"
perplexity_reason: "Compare {implementation} against OWASP guidelines for {category}"
```

### Version Validation

```text
perplexity_search: "{package} latest stable version December 2025"
perplexity_search: "{framework} version {X} deprecated features"
```

## Validation Status Format (REQUIRED)

Every finding MUST include one of these validation statuses:

```markdown
**Validated**: MCP-Validated - Yes - [Source description] [mcp-server-name]
**Validated**: MCP-Validated - No (internal pattern, no external reference needed)
**Validated**: MCP-Validated - Unable (MCP unavailable, manual verification recommended)
```

**Examples:**

```markdown
**Validated**: MCP-Validated - Yes - OWASP Password Storage Cheat Sheet recommends bcrypt cost 12+ [perplexity]
**Validated**: MCP-Validated - Yes - .NET 10 HybridCache patterns confirmed [microsoft-learn + perplexity]
**Validated**: MCP-Validated - No (project-internal naming convention)
```

## Validation Categories

### What to Validate (Priority Order - ALL are mandatory when applicable)

| Category | Priority | MCP Strategy | Skip Allowed? |
| --- | --- | --- | --- |
| Security findings | CRITICAL | perplexity (OWASP) + technology-specific | NO |
| API usage patterns | HIGH | context7 + ref + microsoft-learn | NO |
| Version recommendations | HIGH | perplexity (primary source) | NO |
| Deprecated pattern warnings | HIGH | perplexity + official docs | NO |
| Framework best practices | HIGH | context7 + perplexity | NO |
| Performance recommendations | MEDIUM | perplexity + technology-specific | Only if time-critical |

### What NOT to Validate (Mark as "No external reference needed")

- Code style/formatting (project-specific rules)
- Naming conventions (project-specific patterns)
- File organization (project-specific structure)
- Comment quality (subjective judgment)
- Internal/proprietary APIs (no public documentation exists)

## Citation Format

### Inline Citation (Add to Each Validated Finding)

```markdown
**Validated**: Yes - OWASP Password Storage Cheat Sheet recommends bcrypt cost 12+ [perplexity]
```

### Source List Entry (Add to MCP Validation Summary)

```markdown
- [perplexity]: OWASP Password Storage Cheat Sheet, queried December 2024
- [microsoft-learn]: "EF Core 10 Migrations", https://learn.microsoft.com/...
- [context7]: React v19 documentation, hooks section
- [ref]: Express.js 5.x API reference
```

## Correction Format

When MCP shows different best practice than original finding:

```markdown
### [Original Issue Title] - CORRECTED

**File**: `path/to/file.ext:line`
**Severity**: [Adjusted if needed]
**Category**: [Category]

**Original Finding**: [What the review initially found]
**MCP Correction**: [What MCP sources indicate]

**Updated Recommendation**: [Revised guidance based on MCP]

**Source**: [Specific source] [mcp-server-name]
```

## Error Handling

### MCP Server Unavailable

```markdown
## MCP Validation Summary
**Status**: Partial
**Available Sources**: microsoft-learn, context7
**Unavailable Sources**: perplexity, ref

Note: Some validations could not be completed. Findings without MCP
validation should be verified manually against current documentation.
```

### No Findings to Validate

```markdown
## MCP Validation Summary
**Status**: Not applicable
**Reason**: No external library/framework usage detected

This review focused on project-internal code patterns that do not
require external documentation validation.
```

## Parallel Query Strategy

Run independent MCP queries in parallel for efficiency:

```text
Parallel batch 1 (technology detection complete):
- microsoft-learn: .NET patterns (if applicable)
- context7: library docs (if applicable)
- perplexity: security validation (if security findings)

Parallel batch 2 (after batch 1):
- ref: API reference (for specific methods)
- perplexity: version validation (always for .NET)
```

## Quick Reference

| Finding Type | Primary MCP | Always Pair With | Query Pattern |
| --- | --- | --- | --- |
| .NET API | microsoft-learn | perplexity | Docs + version check |
| npm package | context7 | - | Library docs |
| Security | perplexity | - | OWASP + best practices |
| Performance | perplexity | technology-specific | Benchmarks + patterns |
| Deprecation | perplexity | official docs | Latest version info |

---

**Last Updated:** 2025-12-29
