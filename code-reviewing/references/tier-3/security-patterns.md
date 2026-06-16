# Security Patterns - Deep Dive Code Review

This reference provides comprehensive security code review checks based on OWASP Top 10 and industry best practices. Load this file when reviewing code containing authentication, authorization, cryptography, or sensitive data handling.

## OWASP Top 10 Coverage

### A01:2021 - Broken Access Control

- [ ] **Authorization checks on all endpoints** - Every protected resource must verify user permissions before access
- [ ] **Deny by default** - Access should be explicitly granted, not implicitly allowed
- [ ] **No direct object references without authorization** - Validate user has permission for specific resource ID
- [ ] **Consistent authorization model** - Use same authorization pattern across codebase (RBAC, ABAC, claims-based)
- [ ] **Elevation of privilege prevention** - Users cannot escalate their own permissions or access admin functions
- [ ] **No client-side authorization checks only** - Always validate permissions server-side
- [ ] **Context-aware access control** - Consider user role, resource owner, temporal constraints, IP restrictions

### A02:2021 - Cryptographic Failures

- [ ] **No hardcoded secrets** - Keys, passwords, tokens must not be in source code
- [ ] **Strong encryption algorithms** - Use AES-256, RSA-2048+, avoid DES, MD5, SHA1 for security
- [ ] **Proper key management** - Keys stored in secure vaults (HSM, Key Vault, Secrets Manager), rotated regularly
- [ ] **Encrypt data at rest** - Databases, files, backups must use encryption
- [ ] **Encrypt data in transit** - TLS 1.2+ for all network communication, no sensitive data over HTTP
- [ ] **No encryption of already-hashed data** - Don't encrypt passwords, hash them properly
- [ ] **Proper IV/nonce handling** - Use unique, random initialization vectors for each encryption operation

### A03:2021 - Injection

- [ ] **Parameterized queries only** - Never concatenate user input into SQL, use prepared statements
- [ ] **ORM/query builder usage** - Leverage frameworks that prevent injection by design
- [ ] **Input validation** - Whitelist allowed characters, reject invalid input early
- [ ] **Context-specific output encoding** - HTML encode for HTML context, SQL escape for SQL, shell escape for shell
- [ ] **No eval() or dynamic code execution** - Avoid evaluating user input as code
- [ ] **Command injection prevention** - Validate/sanitize arguments before shell execution, use safe APIs
- [ ] **LDAP/NoSQL injection prevention** - Sanitize inputs for non-SQL data stores
- [ ] **Template injection prevention** - Use safe template engines with auto-escaping

### A04:2021 - Insecure Design

- [ ] **Threat modeling performed** - Security considered during design phase
- [ ] **Secure by default configuration** - Default settings are secure, users must opt-in to less secure options
- [ ] **Defense in depth** - Multiple layers of security controls
- [ ] **Fail securely** - Errors default to deny access, not grant access
- [ ] **Separation of duties** - Critical operations require multiple authorizations
- [ ] **Rate limiting on sensitive operations** - Login, password reset, API calls have rate limits

### A05:2021 - Security Misconfiguration

- [ ] **No default credentials** - Passwords, keys, tokens are unique per deployment
- [ ] **Unnecessary features disabled** - Debug mode, sample apps, unused endpoints removed in production
- [ ] **Security headers configured** - CSP, HSTS, X-Content-Type-Options, X-Frame-Options set
- [ ] **Error messages sanitized** - Stack traces, internal paths not exposed to users
- [ ] **Dependency versions up to date** - Regular patching of libraries and frameworks
- [ ] **Secure CORS policy** - Restrictive origin allowlist, not wildcard

### A06:2021 - Vulnerable and Outdated Components

- [ ] **Dependency scanning** - Automated checks for known vulnerabilities (Dependabot, Snyk, OWASP Dependency-Check)
- [ ] **Regular updates** - Security patches applied promptly
- [ ] **Minimal dependencies** - Only use necessary libraries, avoid bloat
- [ ] **Trusted sources only** - Dependencies from official registries, verify signatures/checksums

### A07:2021 - Identification and Authentication Failures

- [ ] **Multi-factor authentication** - MFA required for admin/privileged accounts
- [ ] **Strong password policy** - Length, complexity, no common passwords enforced
- [ ] **Secure password storage** - bcrypt/argon2/PBKDF2 with high work factor, never plaintext or reversible encryption
- [ ] **Account lockout on brute force** - Temporary lockout after N failed attempts, CAPTCHA, rate limiting
- [ ] **Session management** - Secure, HttpOnly, SameSite cookies; session timeout; regenerate session ID on login
- [ ] **No credentials in URLs** - Tokens/passwords not in query strings or logs
- [ ] **Password reset security** - Token-based, time-limited, single-use reset links
- [ ] **Account enumeration prevention** - Generic error messages, timing-attack mitigation

### A08:2021 - Software and Data Integrity Failures

- [ ] **Code signing** - Binaries, packages, deployments are signed and verified
- [ ] **Integrity checks on dependencies** - Subresource Integrity (SRI), package lock files
- [ ] **Secure CI/CD pipeline** - Build artifacts verified, secrets not in logs
- [ ] **Serialization safety** - Avoid deserializing untrusted data, use safe formats (JSON over pickle/Java serialization)

### A09:2021 - Security Logging and Monitoring Failures

- [ ] **Security events logged** - Login attempts, authorization failures, input validation failures
- [ ] **No sensitive data in logs** - Passwords, tokens, PII redacted
- [ ] **Tamper-proof logs** - Centralized logging, write-only access, integrity checks
- [ ] **Alerting on anomalies** - Automated detection of suspicious patterns
- [ ] **Audit trail for critical operations** - Who did what when for compliance

### A10:2021 - Server-Side Request Forgery (SSRF)

- [ ] **URL allowlist validation** - Restrict outbound requests to known safe domains
- [ ] **No user-controlled URLs** - Avoid letting users specify arbitrary URLs for server to fetch
- [ ] **Network segmentation** - Internal services not accessible from web-facing servers
- [ ] **Disable unused URL schemes** - Block file://, gopher://, etc. if not needed

## Authentication Patterns

### Session-Based Authentication

- [ ] **Secure session ID generation** - Cryptographically random, sufficient entropy (128+ bits)
- [ ] **HttpOnly, Secure, SameSite flags** - Prevent XSS/CSRF attacks on session cookies
- [ ] **Session expiration** - Idle timeout and absolute timeout enforced
- [ ] **Session invalidation on logout** - Server-side session destroyed
- [ ] **Session fixation prevention** - Regenerate session ID on privilege change

### JWT (JSON Web Tokens)

- [ ] **Strong signing algorithm** - HS256/RS256, never "none" algorithm
- [ ] **Secret key strength** - 256+ bits for HMAC, 2048+ bits for RSA
- [ ] **Token expiration** - Short-lived access tokens, refresh token rotation
- [ ] **Signature verification** - Always verify signature before trusting claims
- [ ] **No sensitive data in payload** - JWT payload is base64-encoded, not encrypted

### OAuth 2.0 / OpenID Connect

- [ ] **PKCE for public clients** - Proof Key for Code Exchange prevents authorization code interception
- [ ] **State parameter** - CSRF protection for authorization flow
- [ ] **Redirect URI validation** - Exact match, no wildcard allowed
- [ ] **Token storage security** - Access tokens in memory, refresh tokens in secure storage
- [ ] **Scope validation** - Verify token has required scopes for operation

## Cryptography Best Practices

- [ ] **Use established libraries** - Leverage vetted crypto libraries (OpenSSL, libsodium, .NET Crypto), never roll your own
- [ ] **Random number generation** - Use cryptographically secure PRNG (crypto.randomBytes, SecureRandom, RNGCryptoServiceProvider)
- [ ] **Password hashing work factor** - bcrypt cost 12+, argon2 memory/iterations tuned to ~1 second
- [ ] **Salt uniqueness** - Unique salt per password, stored with hash
- [ ] **Key derivation for encryption** - Use KDF (PBKDF2, scrypt, argon2) to derive keys from passwords
- [ ] **Proper padding** - PKCS7/OAEP for encryption, avoid ECB mode
- [ ] **Certificate validation** - Verify TLS certificates, check revocation, pin certificates for high-security scenarios

## Secret Management

- [ ] **Secrets in environment variables or vaults** - AWS Secrets Manager, Azure Key Vault, HashiCorp Vault
- [ ] **No secrets in version control** - Use .gitignore, scan history for leaked secrets
- [ ] **Secrets rotation** - Regular rotation schedule, support for zero-downtime rotation
- [ ] **Least privilege access to secrets** - Only services that need secrets can access them
- [ ] **Audit secret access** - Log who accessed which secrets when

## Input Validation and Output Encoding

- [ ] **Validate early** - Reject invalid input at entry point, not deep in business logic
- [ ] **Whitelist over blacklist** - Define allowed characters/patterns, not forbidden ones
- [ ] **Length limits** - Prevent DoS via oversized inputs
- [ ] **Type safety** - Strongly typed languages/frameworks reduce injection risk
- [ ] **Context-specific encoding** - HTML encode for HTML, URL encode for URLs, SQL escape for SQL
- [ ] **Content Security Policy** - CSP headers to mitigate XSS

## CSRF, XSS, SQL Injection Prevention

- [ ] **CSRF tokens** - Unique, unpredictable tokens for state-changing operations
- [ ] **SameSite cookies** - Lax or Strict to prevent cross-site cookie sending
- [ ] **Output encoding everywhere** - Never trust user input, always encode on output
- [ ] **Content-Type headers** - Prevent MIME sniffing (X-Content-Type-Options: nosniff)
- [ ] **Parameterized queries** - Only safe way to prevent SQL injection
- [ ] **Stored XSS prevention** - Encode data when rendering, use auto-escaping templates

## Security Headers

- [ ] **Strict-Transport-Security** - Force HTTPS for domain and subdomains
- [ ] **Content-Security-Policy** - Restrict resource loading, prevent inline scripts
- [ ] **X-Frame-Options** - Prevent clickjacking (DENY or SAMEORIGIN)
- [ ] **X-Content-Type-Options** - Prevent MIME sniffing (nosniff)
- [ ] **Referrer-Policy** - Control referrer information leakage
- [ ] **Permissions-Policy** - Restrict browser features (camera, geolocation, etc.)

## Rate Limiting and Brute Force Protection

- [ ] **Rate limits on authentication endpoints** - Limit login attempts per IP/account
- [ ] **Distributed rate limiting** - Use Redis/shared cache for multi-instance deployments
- [ ] **CAPTCHA after threshold** - Human verification after N failed attempts
- [ ] **Progressive delays** - Exponential backoff for repeated failures
- [ ] **IP-based and account-based limits** - Protect against distributed and targeted attacks

## Secure Communication

- [ ] **TLS 1.2+ only** - Disable SSLv3, TLS 1.0, TLS 1.1
- [ ] **Strong cipher suites** - Forward secrecy (ECDHE), authenticated encryption (GCM)
- [ ] **Certificate pinning** - For high-security mobile/desktop apps
- [ ] **HSTS preload** - Submit domain to HSTS preload list
- [ ] **Mutual TLS for internal services** - Client certificates for service-to-service auth

## Security Logging and Monitoring

- [ ] **Log security events** - Authentication, authorization, validation failures
- [ ] **Redact sensitive data** - No passwords, tokens, credit cards in logs
- [ ] **Structured logging** - Machine-parseable formats (JSON) for analysis
- [ ] **Centralized log aggregation** - ELK, Splunk, CloudWatch for correlation
- [ ] **Alerts on anomalies** - Failed login spikes, unusual access patterns
- [ ] **Immutable logs** - Write-once storage, prevent attacker tampering

---

## Suggested Fixes for Common Security Issues

When reviewing code and finding security issues, use these suggested fix patterns. These are HIGH confidence fixes backed by OWASP guidelines.

### SQL Injection (A03:2021)

**Detection Pattern:** String concatenation in SQL queries

```csharp
// Before (vulnerable)
var query = "SELECT * FROM Users WHERE Id = " + userId;
var cmd = new SqlCommand(query, connection);

// After (fixed) - Parameterized query
var query = "SELECT * FROM Users WHERE Id = @userId";
var cmd = new SqlCommand(query, connection);
cmd.Parameters.AddWithValue("@userId", userId);
```

```javascript
// Before (vulnerable)
const query = `SELECT * FROM users WHERE id = ${userId}`;
await db.query(query);

// After (fixed) - Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);
```

```python
# Before (vulnerable)
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# After (fixed) - Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**Source**: [perplexity] - OWASP SQL Injection Prevention Cheat Sheet

### Cross-Site Scripting / XSS (A03:2021)

**Detection Pattern:** Unescaped user input in HTML output

```csharp
// Before (vulnerable)
<div>@Html.Raw(Model.UserComment)</div>

// After (fixed) - Encoded output
<div>@Model.UserComment</div>  // Razor auto-encodes by default
// Or explicitly: @Html.Encode(Model.UserComment)
```

```javascript
// Before (vulnerable)
element.innerHTML = userInput;

// After (fixed) - Use textContent or sanitize
element.textContent = userInput;  // Safe - escapes HTML
// Or for HTML content, use DOMPurify:
element.innerHTML = DOMPurify.sanitize(userInput);
```

```jsx
// Before (vulnerable)
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// After (fixed) - Avoid dangerouslySetInnerHTML, or sanitize
<div>{userInput}</div>  // React auto-escapes
// If HTML needed:
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

**Source**: [perplexity] - OWASP XSS Prevention Cheat Sheet

### Hardcoded Secrets (A02:2021)

**Detection Pattern:** Credentials, API keys, connection strings in source code

```csharp
// Before (vulnerable)
var connectionString = "Server=db.example.com;User=admin;Password=P@ssw0rd123";
var apiKey = "sk-1234567890abcdef";

// After (fixed) - Use configuration/secrets management
var connectionString = configuration.GetConnectionString("DefaultConnection");
var apiKey = configuration["ApiKeys:ExternalService"];

// Or Azure Key Vault
var apiKey = await keyVaultClient.GetSecretAsync("ExternalServiceApiKey");
```

```javascript
// Before (vulnerable)
const apiKey = 'sk-1234567890abcdef';
const dbPassword = 'P@ssw0rd123';

// After (fixed) - Use environment variables
const apiKey = process.env.API_KEY;
const dbPassword = process.env.DB_PASSWORD;

// Or secrets manager
const apiKey = await secretsManager.getSecretValue('api-key');
```

**Source**: [microsoft-learn] - ASP.NET Core Configuration and Secrets Management

### Insecure Password Storage (A07:2021)

**Detection Pattern:** Plaintext passwords, weak hashing (MD5/SHA1), missing salt

```csharp
// Before (vulnerable)
var hashedPassword = SHA256.HashData(Encoding.UTF8.GetBytes(password));  // No salt, weak

// After (fixed) - Use bcrypt or Argon2
using BCrypt.Net;
var hashedPassword = BCrypt.Net.BCrypt.HashPassword(password, workFactor: 12);

// Verification
bool isValid = BCrypt.Net.BCrypt.Verify(inputPassword, storedHash);
```

```javascript
// Before (vulnerable)
const hash = crypto.createHash('md5').update(password).digest('hex');

// After (fixed) - Use bcrypt
const bcrypt = require('bcrypt');
const saltRounds = 12;
const hashedPassword = await bcrypt.hash(password, saltRounds);

// Verification
const isValid = await bcrypt.compare(inputPassword, storedHash);
```

```python
# Before (vulnerable)
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()

# After (fixed) - Use bcrypt or argon2
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Verification
is_valid = bcrypt.checkpw(input_password.encode(), stored_hash)
```

**Source**: [perplexity] - OWASP Password Storage Cheat Sheet (bcrypt cost 12+ recommended)

### Missing Authorization Checks (A01:2021)

**Detection Pattern:** Endpoint/action without authorization attribute or check

```csharp
// Before (vulnerable)
[HttpGet("users/{id}")]
public async Task<User> GetUser(int id)
{
    return await _userService.GetById(id);  // No auth check!
}

// After (fixed) - Add authorization
[Authorize]
[HttpGet("users/{id}")]
public async Task<User> GetUser(int id)
{
    var currentUserId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

    // Check user can access this resource (resource-based auth)
    if (id.ToString() != currentUserId && !User.IsInRole("Admin"))
    {
        throw new UnauthorizedAccessException();
    }

    return await _userService.GetById(id);
}
```

```javascript
// Before (vulnerable)
app.get('/api/orders/:id', async (req, res) => {
    const order = await Order.findById(req.params.id);
    res.json(order);  // No auth check!
});

// After (fixed) - Add authorization middleware + resource check
app.get('/api/orders/:id', authenticate, async (req, res) => {
    const order = await Order.findById(req.params.id);

    // Verify user owns this order
    if (order.userId !== req.user.id && !req.user.isAdmin) {
        return res.status(403).json({ error: 'Forbidden' });
    }

    res.json(order);
});
```

**Source**: [microsoft-learn] - ASP.NET Core Authorization

### CSRF Protection Missing (A01:2021)

**Detection Pattern:** State-changing POST without anti-forgery token

```csharp
// Before (vulnerable)
[HttpPost]
public IActionResult DeleteAccount()
{
    // No CSRF protection!
    _userService.DeleteCurrentUser();
    return Ok();
}

// After (fixed) - Add ValidateAntiForgeryToken
[HttpPost]
[ValidateAntiForgeryToken]  // Requires @Html.AntiForgeryToken() in form
public IActionResult DeleteAccount()
{
    _userService.DeleteCurrentUser();
    return Ok();
}

// For APIs, use [AutoValidateAntiforgeryToken] at controller level
// or configure SameSite=Strict cookies
```

**Source**: [microsoft-learn] - ASP.NET Core Anti-Forgery

### JWT Algorithm Confusion (A07:2021)

**Detection Pattern:** JWT validation without algorithm specification

```csharp
// Before (vulnerable)
var token = handler.ReadJwtToken(tokenString);
// Token might use "none" algorithm!

// After (fixed) - Specify allowed algorithms
var validationParameters = new TokenValidationParameters
{
    ValidateIssuerSigningKey = true,
    IssuerSigningKey = signingKey,
    ValidateIssuer = true,
    ValidIssuer = "your-issuer",
    ValidateAudience = true,
    ValidAudience = "your-audience",
    ValidAlgorithms = new[] { SecurityAlgorithms.HmacSha256 },  // Explicit!
    RequireExpirationTime = true,
    ClockSkew = TimeSpan.Zero
};

var principal = handler.ValidateToken(tokenString, validationParameters, out _);
```

**Source**: [perplexity] - JWT Security Best Practices (algorithm confusion attacks)

### Insecure Direct Object Reference (A01:2021)

**Detection Pattern:** User-supplied ID used without ownership check

```csharp
// Before (vulnerable)
[HttpGet("documents/{id}")]
public async Task<Document> GetDocument(int id)
{
    return await _context.Documents.FindAsync(id);  // No ownership check!
}

// After (fixed) - Filter by current user
[Authorize]
[HttpGet("documents/{id}")]
public async Task<ActionResult<Document>> GetDocument(int id)
{
    var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

    var document = await _context.Documents
        .Where(d => d.Id == id && d.OwnerId == userId)
        .FirstOrDefaultAsync();

    if (document == null)
    {
        return NotFound();  // Don't reveal if doc exists for other user
    }

    return document;
}
```

**Source**: [perplexity] - OWASP Insecure Direct Object References

---

**Usage Pattern:** Load this file when reviewing authentication, authorization, cryptography, session management, or any code handling sensitive data. Cross-reference with OWASP Top 10 and CWE/SANS Top 25 for comprehensive coverage.

**Last Updated:** 2025-12-29
