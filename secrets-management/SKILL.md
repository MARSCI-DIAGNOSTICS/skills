---
name: secrets-management
description: Comprehensive guidance for secure secrets management including storage solutions (Vault, AWS Secrets Manager, Azure Key Vault), environment variables, secret rotation, scanning tools, and CI/CD pipeline security. Use when implementing secrets storage, configuring secret rotation, preventing secret leaks, or reviewing credentials handling.
allowed-tools: Read, Glob, Grep, Task, Bash
---

# Secrets Management

Comprehensive guidance for securely storing, accessing, rotating, and protecting secrets.

## When to Use This Skill

Use this skill when:

- Choosing a secrets management solution
- Implementing secret rotation
- Preventing secrets in source code
- Configuring CI/CD pipeline secrets
- Setting up secrets scanning
- Reviewing credentials handling
- Migrating from insecure secret storage

## Secrets Management Solutions

### Comparison Matrix

| Solution | Self-Hosted | Cloud | Dynamic Secrets | Rotation | Cost |
|----------|-------------|-------|-----------------|----------|------|
| HashiCorp Vault | ✅ | ✅ | ✅ | ✅ | Free (OSS) / $$ |
| AWS Secrets Manager | ❌ | ✅ | ❌ | ✅ | $ |
| Azure Key Vault | ❌ | ✅ | ❌ | ✅ | $ |
| Google Secret Manager | ❌ | ✅ | ❌ | ✅ | $ |
| Doppler | ❌ | ✅ | ❌ | ❌ | $$ |
| Environment Variables | ✅ | ✅ | ❌ | Manual | Free |

### When to Use What

| Use Case | Recommended Solution |
|----------|---------------------|
| Enterprise, multi-cloud | HashiCorp Vault |
| AWS-native applications | AWS Secrets Manager |
| Azure-native applications | Azure Key Vault |
| GCP-native applications | Google Secret Manager |
| Simple applications | Environment variables |
| Development | .env files (never commit!) |

## HashiCorp Vault

### Basic Usage

```bash
# Enable secrets engine
vault secrets enable -path=secret kv-v2

# Store a secret
vault kv put secret/myapp/database \
    username="dbuser" \
    password="supersecret"

# Read a secret
vault kv get secret/myapp/database

# Get specific field
vault kv get -field=password secret/myapp/database
```

### Application Integration (C#)

```csharp
using System.Text.Json;
using VaultSharp;
using VaultSharp.V1.AuthMethods.Token;

/// <summary>
/// HashiCorp Vault client for secrets retrieval.
/// </summary>
public sealed class VaultClient
{
    private readonly IVaultClient _client;

    public VaultClient(string url, string token)
    {
        var authMethod = new TokenAuthMethodInfo(token);
        var settings = new VaultClientSettings(url, authMethod);
        _client = new VaultSharp.VaultClient(settings);
    }

    /// <summary>
    /// Get a secret from Vault KV v2.
    /// </summary>
    public async Task<string> GetSecretAsync(string path, string key, CancellationToken cancellationToken = default)
    {
        var secret = await _client.V1.Secrets.KeyValue.V2.ReadSecretAsync(path: path);
        return secret.Data.Data[key].ToString()!;
    }

    /// <summary>
    /// Get database credentials.
    /// </summary>
    public async Task<DatabaseCredentials> GetDatabaseCredentialsAsync(CancellationToken cancellationToken = default)
    {
        return new DatabaseCredentials(
            Username: await GetSecretAsync("myapp/database", "username", cancellationToken),
            Password: await GetSecretAsync("myapp/database", "password", cancellationToken)
        );
    }
}

public sealed record DatabaseCredentials(string Username, string Password);

// Usage
var vault = new VaultClient(
    url: Environment.GetEnvironmentVariable("VAULT_ADDR")!,
    token: Environment.GetEnvironmentVariable("VAULT_TOKEN")!
);
var dbCreds = await vault.GetDatabaseCredentialsAsync();
```

### Dynamic Database Credentials

```bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL connection
vault write database/config/mydb \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb" \
    allowed_roles="readonly,readwrite" \
    username="vault" \
    password="vault-password"

# Create a role
vault write database/roles/readonly \
    db_name=mydb \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# Get dynamic credentials
vault read database/creds/readonly
# Returns: username=v-token-readonly-xxx, password=xxx, lease_id=xxx
```

**For detailed Vault patterns:** See [Vault Patterns Reference](references/vault-patterns.md)

## AWS Secrets Manager

### Store and Retrieve Secrets

```csharp
using Amazon.SecretsManager;
using Amazon.SecretsManager.Model;
using System.Text.Json;

/// <summary>
/// AWS Secrets Manager client.
/// </summary>
public sealed class AwsSecretsClient(IAmazonSecretsManager client)
{
    /// <summary>
    /// Retrieve secret from AWS Secrets Manager.
    /// </summary>
    public async Task<T> GetSecretAsync<T>(string secretName, CancellationToken cancellationToken = default)
    {
        var response = await client.GetSecretValueAsync(
            new GetSecretValueRequest { SecretId = secretName },
            cancellationToken
        );

        return JsonSerializer.Deserialize<T>(response.SecretString)!;
    }
}

// Usage with DI
public sealed record DbCredentials(string Username, string Password);

// In Startup/Program.cs
services.AddAWSService<IAmazonSecretsManager>();
services.AddSingleton<AwsSecretsClient>();

// In application code
var dbCreds = await secretsClient.GetSecretAsync<DbCredentials>("prod/myapp/database");
// Returns: DbCredentials { Username = "dbuser", Password = "secret" }
```

### Automatic Rotation

```csharp
using Amazon.SecretsManager;
using Amazon.SecretsManager.Model;
using System.Text.Json;

/// <summary>
/// Create secret with automatic rotation enabled.
/// </summary>
public static async Task CreateSecretWithRotationAsync(
    IAmazonSecretsManager client,
    string secretName,
    object secretValue,
    string rotationLambdaArn,
    int rotationDays = 30,
    CancellationToken cancellationToken = default)
{
    // Create the secret
    await client.CreateSecretAsync(new CreateSecretRequest
    {
        Name = secretName,
        SecretString = JsonSerializer.Serialize(secretValue)
    }, cancellationToken);

    // Enable rotation (requires Lambda function)
    await client.RotateSecretAsync(new RotateSecretRequest
    {
        SecretId = secretName,
        RotationLambdaARN = rotationLambdaArn,
        RotationRules = new RotationRulesType
        {
            AutomaticallyAfterDays = rotationDays
        }
    }, cancellationToken);
}
```

## Environment Variables

### Best Practices

```bash
# Set environment variables (not in code!)
export DATABASE_URL="postgresql://user:pass@localhost/db"
export API_KEY="sk_live_xxx"

# In systemd service file
[Service]
Environment="DATABASE_URL=postgresql://user:pass@localhost/db"
EnvironmentFile=/etc/myapp/secrets.env

# In Docker
docker run -e DATABASE_URL="postgresql://..." myapp
# Or from file
docker run --env-file ./secrets.env myapp

# In Kubernetes
kubectl create secret generic myapp-secrets \
    --from-literal=DATABASE_URL="postgresql://..." \
    --from-literal=API_KEY="sk_live_xxx"
```

### Loading in Application

```csharp
using Microsoft.Extensions.Configuration;

/// <summary>
/// Application configuration loaded from environment variables.
/// </summary>
public sealed class AppConfig
{
    public required string DatabaseUrl { get; init; }
    public required string ApiKey { get; init; }
    public bool Debug { get; init; }
}

// In Program.cs or Startup.cs
var configuration = new ConfigurationBuilder()
    .AddEnvironmentVariables()
    .AddUserSecrets<Program>(optional: true)  // For development
    .Build();

// Bind to strongly-typed config
services.Configure<AppConfig>(options =>
{
    options.DatabaseUrl = configuration["DATABASE_URL"]
        ?? throw new InvalidOperationException("DATABASE_URL is required");
    options.ApiKey = configuration["API_KEY"]
        ?? throw new InvalidOperationException("API_KEY is required");
    options.Debug = bool.TryParse(configuration["DEBUG"], out var debug) && debug;
});

// Or use options pattern
services.AddOptions<AppConfig>()
    .Bind(configuration.GetSection("App"))
    .ValidateDataAnnotations()
    .ValidateOnStart();

// In application code
public class MyService(IOptions<AppConfig> config)
{
    private readonly AppConfig _config = config.Value;
}
```

### .env File Security

```bash
# .env (NEVER commit this!)
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=sk_live_xxx

# .env.example (commit this as template)
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=your-api-key-here
```

```gitignore
# .gitignore - ALWAYS include
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
```

## Secret Rotation

### Rotation Strategy

```csharp
using System.Security.Cryptography;

/// <summary>
/// Secret rotation with overlap period for zero-downtime rotation.
/// </summary>
public sealed class SecretRotator(ISecretsStore secrets, INotificationClient notifications)
{
    private static readonly TimeSpan GracePeriod = TimeSpan.FromHours(24);

    /// <summary>
    /// Rotate an API key with overlap period.
    /// </summary>
    public async Task<string> RotateApiKeyAsync(string keyName, CancellationToken cancellationToken = default)
    {
        // 1. Generate new key
        var newKey = Convert.ToBase64String(RandomNumberGenerator.GetBytes(32))
            .Replace('+', '-').Replace('/', '_').TrimEnd('=');

        // 2. Store new key as pending
        await secrets.StoreAsync($"{keyName}_pending", newKey, cancellationToken);

        // 3. Update primary key (old key still valid)
        var oldKey = await secrets.GetAsync(keyName, cancellationToken);
        await secrets.StoreAsync($"{keyName}_old", oldKey, cancellationToken);
        await secrets.StoreAsync(keyName, newKey, cancellationToken);

        // 4. Notify dependent services
        await notifications.SendAsync(
            $"API key {keyName} rotated. Update your configuration.",
            cancellationToken
        );

        // 5. Schedule old key deletion (grace period)
        await secrets.ScheduleDeletionAsync($"{keyName}_old", GracePeriod, cancellationToken);

        return newKey;
    }

    /// <summary>
    /// Accept both old and new keys during rotation.
    /// </summary>
    public async Task<bool> ValidateDuringRotationAsync(string keyName, string providedKey, CancellationToken cancellationToken = default)
    {
        var current = await secrets.GetAsync(keyName, cancellationToken);
        if (CryptographicOperations.FixedTimeEquals(
            System.Text.Encoding.UTF8.GetBytes(providedKey),
            System.Text.Encoding.UTF8.GetBytes(current)))
        {
            return true;
        }

        var old = await secrets.GetOrDefaultAsync($"{keyName}_old", cancellationToken);
        if (old is not null && CryptographicOperations.FixedTimeEquals(
            System.Text.Encoding.UTF8.GetBytes(providedKey),
            System.Text.Encoding.UTF8.GetBytes(old)))
        {
            return true;
        }

        return false;
    }
}

// Interfaces for secrets and notifications
public interface ISecretsStore
{
    Task<string> GetAsync(string key, CancellationToken cancellationToken);
    Task<string?> GetOrDefaultAsync(string key, CancellationToken cancellationToken);
    Task StoreAsync(string key, string value, CancellationToken cancellationToken);
    Task ScheduleDeletionAsync(string key, TimeSpan delay, CancellationToken cancellationToken);
}

public interface INotificationClient
{
    Task SendAsync(string message, CancellationToken cancellationToken);
}
```

### Rotation Timeline

```text
Day 0:  Generate new key, deploy to secrets manager
        ├── Old key: ACTIVE
        └── New key: PENDING

Day 1:  Update applications to use new key
        ├── Old key: ACTIVE (grace period)
        └── New key: ACTIVE

Day 7:  Revoke old key
        ├── Old key: REVOKED
        └── New key: ACTIVE
```

## Secrets Scanning

### Pre-commit Scanning

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### CI/CD Scanning

```yaml
# GitHub Actions
name: Security Scan
on: [push, pull_request]

jobs:
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0  # Full history for scanning

      - name: Gitleaks scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: TruffleHog scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          extra_args: --only-verified
```

### Scanning Tools Comparison

| Tool | Strengths | Weaknesses |
|------|-----------|------------|
| gitleaks | Fast, good regex patterns | May miss custom formats |
| TruffleHog | Verifies secrets are live | Slower, network calls |
| detect-secrets | Baseline support, plugins | More false positives |
| git-secrets | AWS patterns built-in | AWS-focused |

**For detailed scanning setup:** See [Secrets Scanning Reference](references/secrets-scanning.md)

## CI/CD Pipeline Secrets

### GitHub Actions

```yaml
# Store secrets in repository settings
# Access via ${{ secrets.SECRET_NAME }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          # Secrets available as environment variables
          ./deploy.sh

      # For OIDC authentication (preferred for cloud)
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
          aws-region: us-east-1
```

### GitLab CI

```yaml
# Store in Settings > CI/CD > Variables
# Mark as "Masked" and "Protected"

deploy:
  script:
    - echo "Deploying with DB_PASSWORD=$DB_PASSWORD"  # Never do this!
    - ./deploy.sh
  variables:
    # Override for this job only
    ENVIRONMENT: production
```

### Best Practices for CI/CD Secrets

1. **Use OIDC when possible** - No long-lived credentials
2. **Mask secrets in logs** - CI systems should auto-mask
3. **Limit secret scope** - Per-environment, per-branch
4. **Audit secret access** - Who accessed what when
5. **Rotate regularly** - Especially after team changes

## Quick Decision Tree

**Where should I store this secret?**

1. **Production database credentials** → Secrets Manager + rotation
2. **API keys for third-party services** → Secrets Manager
3. **Encryption keys** → HSM or Vault
4. **Development credentials** → .env file (gitignored)
5. **CI/CD deployment credentials** → CI/CD secrets + OIDC
6. **Inter-service authentication** → Vault dynamic secrets
7. **User-submitted API keys** → Encrypted database column

## Anti-Patterns to Avoid

### Never Do This

```csharp
// WRONG: Hardcoded secrets
const string ApiKey = "sk_live_abc123";
const string DatabaseUrl = "postgresql://admin:password123@prod.db.example.com/app";

// WRONG: Secrets in appsettings.json (committed to git)
// {
//   "Database": {
//     "Password": "supersecret"
//   }
// }

// WRONG: Secrets in Docker images
// COPY secrets.env /app/secrets.env

// WRONG: Logging secrets
_logger.LogInformation("Connecting with password: {Password}", password);

// WRONG: Secrets in error messages
throw new Exception($"Failed to connect: {connectionString}");

// WRONG: Secrets in URLs
await httpClient.GetAsync($"https://api.example.com?api_key={apiKey}");
```

### Do This Instead

```csharp
// RIGHT: Environment variables
var apiKey = Environment.GetEnvironmentVariable("API_KEY")
    ?? throw new InvalidOperationException("API_KEY not configured");

// RIGHT: Secrets manager
var apiKey = await secretsManager.GetSecretAsync("api-key");

// RIGHT: Configuration with User Secrets (dev) or Azure Key Vault (prod)
var apiKey = configuration["ApiKey"];

// RIGHT: Masked logging (use structured logging)
_logger.LogInformation("Connecting to database...");  // No credentials

// RIGHT: Generic error messages
throw new InvalidOperationException("Database connection failed");  // No details

// RIGHT: Secrets in headers (for APIs)
httpClient.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Bearer", apiKey);
await httpClient.GetAsync("https://api.example.com");
```

## Security Checklist

### Storage

- [ ] No hardcoded secrets in source code
- [ ] Secrets stored in dedicated secrets manager
- [ ] Environment variables for configuration
- [ ] .env files gitignored

### Access Control

- [ ] Least privilege access to secrets
- [ ] Audit logging enabled
- [ ] Secrets scoped to environments
- [ ] Regular access reviews

### Rotation

- [ ] Rotation policy defined
- [ ] Automated rotation where possible
- [ ] Grace period for old secrets
- [ ] Notification on rotation

### Detection

- [ ] Pre-commit hooks for secret scanning
- [ ] CI/CD pipeline scanning
- [ ] Git history scanning
- [ ] Regular repository audits

### CI/CD

- [ ] Using CI platform's secrets management
- [ ] OIDC for cloud authentication
- [ ] Secrets masked in logs
- [ ] Limited secret scope

## References

- [Vault Patterns Reference](references/vault-patterns.md) - HashiCorp Vault deep dive
- [Secrets Scanning Reference](references/secrets-scanning.md) - Scanning tools setup

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `cryptography` | Encryption for secrets at rest |
| `devsecops-practices` | CI/CD security integration |
| `authentication-patterns` | API key and token management |

## Version History

- v1.0.0 (2025-12-26): Initial release with Vault, cloud providers, rotation, scanning

---

**Last Updated:** 2025-12-26
