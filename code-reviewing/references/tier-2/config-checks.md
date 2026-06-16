# Configuration Management Code Review Checks

**Tier 2 Reference - Loaded for:** `.yaml`, `.yml`, `.json`, `.env`, `.toml`, `.ini`, `.xml`, `.config`, `.properties`

## Overview

Configuration files are critical security and operational boundaries. Review them with heightened scrutiny for secrets, validation, environment handling, and operational safety.

## 1. Secret Management

### 1.1 No Hardcoded Secrets

- [ ] **No credentials in config** - No passwords, API keys, tokens, or secrets hardcoded in config files
- [ ] **No connection strings with credentials** - Database URLs, service endpoints use environment variables or secret stores
- [ ] **No private keys** - No SSH keys, TLS certificates, or cryptographic keys in configuration
- [ ] **No service account credentials** - OAuth tokens, service principals stored in secure vaults
- [ ] **Placeholder values for secrets** - Use `<SECRET>`, `${ENV_VAR}`, or similar for sensitive values

### 1.2 Secret Detection Prevention

- [ ] **Secret scanning in CI/CD** - Automated secret detection (gitleaks, TruffleHog, detect-secrets)
- [ ] **Pre-commit hooks** - Local secret detection before commits
- [ ] **Clear documentation** - Instructions for developers on how to provide secrets securely
- [ ] **Example config files** - Provide `.example` files with placeholders, never real secrets

## 2. Environment-Specific Configuration

### 2.1 Environment Isolation

- [ ] **Separate configs per environment** - `dev.yaml`, `staging.yaml`, `prod.yaml` with clear isolation
- [ ] **Environment detection** - Runtime environment determined correctly (ENV variable, deployment context)
- [ ] **No production secrets in non-prod** - Lower environments use separate, non-production credentials
- [ ] **Clear environment naming** - Unambiguous environment identifiers (`production`, not `prod1`, `prod-new`)

### 2.2 Configuration Overrides

- [ ] **Layered configuration** - Base config + environment overrides pattern
- [ ] **Override precedence documented** - Clear hierarchy (file < env var < CLI arg)
- [ ] **No unexpected merging** - Deep merge behavior is explicit and predictable
- [ ] **Override validation** - Environment-specific overrides validated against schema

## 3. Configuration Validation

### 3.1 Schema and Type Safety

- [ ] **Schema defined** - JSON Schema, YAML schema, or language-specific validation
- [ ] **Type checking** - Config values validated for correct types (string, int, bool, array)
- [ ] **Required fields enforced** - Missing required config fails fast at startup
- [ ] **Unknown fields rejected** - Typos and deprecated fields cause errors, not silent failures

### 3.2 Constraint Validation

- [ ] **Range validation** - Numeric values within acceptable bounds (ports 1-65535, percentages 0-100)
- [ ] **Format validation** - URLs, emails, UUIDs validated with regex or parsers
- [ ] **Enum validation** - Only allowed values accepted (log levels, feature flags)
- [ ] **Dependency validation** - If feature X enabled, config Y is required

### 3.3 Startup Validation

- [ ] **Fail-fast on invalid config** - Application refuses to start with bad configuration
- [ ] **Clear error messages** - Validation failures explain what is wrong and how to fix it
- [ ] **Pre-deployment validation** - Config validated in CI/CD before deployment

## 4. Feature Flags and Toggles

### 4.1 Feature Flag Design

- [ ] **Boolean flags** - Simple on/off toggles use `true`/`false`, not magic strings
- [ ] **Rollout percentages** - Gradual rollouts use 0-100 percentages, not arbitrary values
- [ ] **User/group targeting** - Feature flags support targeting by user ID, group, or tenant
- [ ] **Flag naming conventions** - Clear, consistent naming (`enable_new_checkout`, not `flag1`)

### 4.2 Feature Flag Lifecycle

- [ ] **Documented flag purpose** - Each flag has description and removal plan
- [ ] **Removal timeline** - Temporary flags have expiration dates or cleanup tickets
- [ ] **No permanent flags** - Feature flags are for experiments/rollouts, not configuration
- [ ] **Default values** - Flag defaults are safe (usually `false` for new features)

## 5. 12-Factor App Compliance

### 5.1 Config in Environment

- [ ] **Config from environment** - All environment-specific values from env vars, not files
- [ ] **No code changes for environments** - Same codebase runs in all environments
- [ ] **Strict separation** - Config never checked into version control with code

### 5.2 Backing Services

- [ ] **URLs for services** - Databases, caches, queues treated as attached resources (URLs in config)
- [ ] **No hardcoded hostnames** - Service endpoints configurable, not compiled
- [ ] **Connection pooling config** - Max connections, timeouts, retries configurable

## 6. Default Values and Fallbacks

### 6.1 Safe Defaults

- [ ] **Secure defaults** - Conservative settings (e.g., TLS enabled, short timeouts, low limits)
- [ ] **Explicit over implicit** - Defaults documented and visible, not hidden in code
- [ ] **Override-able defaults** - All defaults can be overridden when needed
- [ ] **No dangerous defaults** - Defaults never bypass security (auth enabled, logging on)

### 6.2 Fallback Behavior

- [ ] **Graceful degradation** - Missing optional config degrades functionality, does not crash
- [ ] **Logged fallbacks** - When defaults are used, log this fact for operators
- [ ] **Required vs optional** - Clear distinction between must-have and optional config

## 7. Configuration File Organization

### 7.1 File Structure

- [ ] **Logical grouping** - Related config grouped (database, cache, messaging sections)
- [ ] **Flat over nested** - Avoid excessive nesting (max 3 levels deep)
- [ ] **Consistent formatting** - Indentation, key ordering, and style consistent
- [ ] **Comments for complex values** - Non-obvious settings explained inline

### 7.2 Naming Conventions

- [ ] **Consistent key naming** - `snake_case`, `camelCase`, or `kebab-case` used consistently
- [ ] **Hierarchical keys** - Namespacing for clarity (`database.host`, `cache.ttl`)
- [ ] **No abbreviations** - Prefer `timeout_seconds` over `timeout_s` or `to`

## 8. Documentation of Configuration

### 8.1 Inline Documentation

- [ ] **Comments for all sections** - Each config section has explanatory comment
- [ ] **Units specified** - Timeouts, sizes include units (seconds, MB, etc.)
- [ ] **Valid ranges documented** - Min/max values, allowed options listed
- [ ] **Examples provided** - Non-trivial config has example values

### 8.2 External Documentation

- [ ] **README or wiki** - Central reference for all config options
- [ ] **Migration guides** - When config changes, provide migration instructions
- [ ] **Environment setup docs** - How to configure each environment documented
- [ ] **Troubleshooting section** - Common config errors and solutions

## 9. Configuration Change Auditing

### 9.1 Change Tracking

- [ ] **Version control for config** - Config files in git (excluding secrets)
- [ ] **Config change reviews** - PRs for config changes, not direct edits
- [ ] **Audit logs for runtime changes** - Changes via admin UI or API logged
- [ ] **Rollback capability** - Easy to revert config changes

### 9.2 Change Validation

- [ ] **Dry-run mode** - Test config changes before applying
- [ ] **Staging validation** - Config changes tested in non-production first
- [ ] **Automated testing** - Config changes trigger relevant tests

## 10. Sensitive Data Handling

### 10.1 Data Classification

- [ ] **Config classified** - Public, internal, confidential, secret clearly marked
- [ ] **Encryption at rest** - Sensitive config encrypted on disk
- [ ] **Encryption in transit** - Config fetched from remote sources over TLS
- [ ] **Access controls** - Only authorized users/services can read sensitive config

### 10.2 Logging and Exposure

- [ ] **No secrets in logs** - Config values sanitized before logging
- [ ] **No secrets in error messages** - Stack traces and errors redact sensitive values
- [ ] **No secrets in metrics** - Tags and labels do not contain credentials
- [ ] **Health checks safe** - Diagnostic endpoints do not expose config

## 11. Advanced Configuration Patterns

### 11.1 Dynamic Configuration

- [ ] **Hot reload support** - Config changes without restart (where appropriate)
- [ ] **Change notification** - Applications detect config updates and react
- [ ] **Gradual rollout** - Config changes can be rolled out incrementally

### 11.2 Remote Configuration

- [ ] **Config from remote stores** - etcd, Consul, AWS Parameter Store integration
- [ ] **Caching strategy** - Remote config cached locally with TTL
- [ ] **Fallback to local** - If remote unavailable, use last-known-good local cache
- [ ] **Retry logic** - Transient failures fetching config handled gracefully

## 12. Platform-Specific Considerations

### 12.1 JSON Configuration

- [ ] **Valid JSON syntax** - No trailing commas, proper quoting
- [ ] **Schema validation** - JSON Schema defined and enforced
- [ ] **No comments** - JSON does not support comments; use separate docs or JSONC where supported

### 12.2 YAML Configuration

- [ ] **Consistent indentation** - Spaces, not tabs (2 or 4 spaces consistently)
- [ ] **Quoted strings** - Ambiguous values quoted (`"true"`, `"123"`, `"yes"`)
- [ ] **No complex anchors** - YAML anchors/aliases used sparingly, clearly documented
- [ ] **Version pinned** - YAML parser version pinned to avoid breaking changes

### 12.3 Environment Variables (.env)

- [ ] **KEY=VALUE format** - No spaces around `=`, no quotes unless needed
- [ ] **UPPERCASE keys** - Conventional to use `UPPERCASE_WITH_UNDERSCORES`
- [ ] **No interpolation** - Environment variable files do not support `${VAR}` by default
- [ ] **Not committed** - `.env` files gitignored, `.env.example` provided

### 12.4 TOML Configuration

- [ ] **Section headers** - Clear `[section]` organization
- [ ] **Type safety** - Leverage TOML's type system (dates, integers, arrays)
- [ ] **Comments** - Use `#` for inline and block comments

## 13. Dependency Update Safety

**Profile**: `thorough`, `strict`

When dependency manifest files change (`package.json`, `*.csproj`, `requirements.txt`, `Cargo.toml`, `go.mod`), verify updates are safe.

### 13.1 Dependency Change Detection

- [ ] **Detect manifest changes** - Track changes to dependency files in changeset
- [ ] **Parse version changes** - Extract old and new version numbers
- [ ] **Classify risk level** - Major (1.x→2.x), Minor (1.1→1.2), Patch (1.1.1→1.1.2)

### 13.2 Breaking Change Validation

For major version bumps or known-risky packages:

- [ ] **Query MCP for breaking changes** - `perplexity: "{package} {old} to {new} breaking changes"`
- [ ] **Check changelogs** - `context7: query package changelog/migration guide`
- [ ] **Verify migration steps** - Code addresses breaking changes mentioned in MCP results
- [ ] **Document known issues** - Major bumps with no migration notes flagged as MAJOR

### 13.3 Risk Classification

| Version Change | Risk Level | Severity if Unaddressed |
|----------------|------------|-------------------------|
| Major bump (1.x → 2.x) | HIGH | MAJOR (breaking changes likely) |
| Minor bump (1.1 → 1.2) | MEDIUM | MINOR (new features, possible deprecations) |
| Patch bump (1.1.1 → 1.1.2) | LOW | Info only (bug fixes) |
| Pre-release to stable | MEDIUM | MINOR (API may have changed) |
| Wildcard versions (`*`, `latest`) | HIGH | CRITICAL (unpredictable builds) |

### 13.4 Manifest-Specific Checks

**package.json / package-lock.json:**

- [ ] **Lock file updated** - Changes to `package.json` include corresponding lock file updates
- [ ] **No floating versions** - Avoid `^` or `~` for critical dependencies
- [ ] **Peer dependencies satisfied** - New packages don't break peer requirements

**\*.csproj / Directory.Packages.props:**

- [ ] **Central package management** - If using CPM, changes go to `Directory.Packages.props`
- [ ] **Framework compatibility** - Package supports target framework version
- [ ] **Transitive dependencies** - Major transitive updates detected

**requirements.txt / pyproject.toml:**

- [ ] **Pinned versions** - Production dependencies pinned to exact versions
- [ ] **Python version compatibility** - Packages support declared Python version

**Cargo.toml:**

- [ ] **Semver followed** - Rust ecosystem relies heavily on semver
- [ ] **Feature flags documented** - New feature flags explicitly enabled

### 13.5 MCP Query Templates

```text
# For major version bumps
perplexity: "{package_name} version {old} to {new} breaking changes migration guide"

# For known-risky packages
perplexity: "{package_name} {new_version} known issues December 2025"

# For framework-specific
context7: query "{framework} {package_name} upgrade guide"
```

### 13.6 Output Format

When dependency issues detected:

```markdown
### Dependency Update Risk

**File**: `package.json:15`
**Severity**: MAJOR
**Confidence**: HIGH

**Problem**: Major version bump without migration verification.

**Details**:
- Package: `axios` (1.7.2 → 2.0.0)
- Risk: HIGH (major version)
- Breaking Changes: [MCP result summary]

**Fix**: Review migration guide and address breaking changes.

**Source**: [perplexity] - axios 2.0 migration guide
```

## Anti-Patterns to Avoid

- Hardcoding production credentials in any config file
- Mixing environment-specific values in shared config files
- Using config as a feature flag graveyard (flags never removed)
- Overly complex nested structures (more than 3 levels deep)
- Undocumented magic numbers or cryptic abbreviations
- Silently ignoring unknown config keys (typos go undetected)
- Storing secrets in config files (even encrypted files in version control)
- Using default credentials (`admin/admin`) even in dev environments

## Quick Reference

**Before Approving Config Changes:**

1. Scan for hardcoded secrets (keys, passwords, tokens)
2. Verify environment-specific values use environment variables
3. Check schema validation exists and fails on bad input
4. Confirm sensitive data is properly protected
5. Ensure documentation is updated for new config options
6. Validate default values are secure and sensible

**Config Review Priority:**

- **P0 (Block merge):** Hardcoded secrets, production credentials, missing validation
- **P1 (Must fix):** No schema, unclear environment handling, dangerous defaults
- **P2 (Should fix):** Poor documentation, inconsistent naming, no examples
- **P3 (Nice to have):** Better comments, improved organization, refactoring

---

**Last Updated:** 2025-12-31
