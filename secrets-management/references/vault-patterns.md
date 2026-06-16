# HashiCorp Vault Patterns Reference

This reference provides advanced HashiCorp Vault patterns and configurations.

## Architecture Overview

### Vault Components

```text
┌─────────────────────────────────────────────────────────────┐
│                    Vault Server                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Auth Methods│  │Secret Engines│  │   Audit Devices    │  │
│  │ - Token     │  │ - KV        │  │   - File           │  │
│  │ - AppRole   │  │ - Database  │  │   - Syslog         │  │
│  │ - OIDC      │  │ - Transit   │  │   - Socket         │  │
│  │ - AWS       │  │ - PKI       │  │                    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    Storage Backend                           │
│  (Consul, Raft, S3, etc.)                                   │
└─────────────────────────────────────────────────────────────┘
```

## Authentication Methods

### AppRole (Recommended for Applications)

AppRole is designed for machine authentication with minimal human interaction.

```bash
# Enable AppRole auth
vault auth enable approle

# Create a policy for the application
vault policy write myapp-policy - <<EOF
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}
path "database/creds/myapp-readonly" {
  capabilities = ["read"]
}
EOF

# Create an AppRole
vault write auth/approle/role/myapp \
    token_policies="myapp-policy" \
    token_ttl=1h \
    token_max_ttl=4h \
    secret_id_ttl=24h \
    secret_id_num_uses=100

# Get Role ID (static, can be baked into app)
vault read auth/approle/role/myapp/role-id
# role_id: abc123...

# Generate Secret ID (dynamic, delivered securely)
vault write -f auth/approle/role/myapp/secret-id
# secret_id: xyz789...
```

#### AppRole Authentication in C\#

```csharp
using VaultSharp;
using VaultSharp.V1.AuthMethods.AppRole;

/// <summary>
/// Vault client using AppRole authentication.
/// </summary>
public sealed class VaultAppRoleClient : IAsyncDisposable
{
    private readonly IVaultClient _client;
    private readonly string _mountPoint;

    public VaultAppRoleClient(string vaultAddress, string roleId, string secretId, string mountPoint = "approle")
    {
        _mountPoint = mountPoint;

        var authMethod = new AppRoleAuthMethodInfo(
            mountPoint: mountPoint,
            roleId: roleId,
            secretId: secretId);

        var settings = new VaultClientSettings(vaultAddress, authMethod)
        {
            UseVaultTokenHeaderInsteadOfAuthorizationHeader = true
        };

        _client = new VaultClient(settings);
    }

    /// <summary>
    /// Create client from environment variables.
    /// </summary>
    public static VaultAppRoleClient FromEnvironment() => new(
        vaultAddress: Environment.GetEnvironmentVariable("VAULT_ADDR")
            ?? throw new InvalidOperationException("VAULT_ADDR not set"),
        roleId: Environment.GetEnvironmentVariable("VAULT_ROLE_ID")
            ?? throw new InvalidOperationException("VAULT_ROLE_ID not set"),
        secretId: Environment.GetEnvironmentVariable("VAULT_SECRET_ID")
            ?? throw new InvalidOperationException("VAULT_SECRET_ID not set"));

    /// <summary>
    /// Read a secret from KV v2.
    /// </summary>
    public async Task<IDictionary<string, object>> GetSecretAsync(string path, CancellationToken ct = default)
    {
        var secret = await _client.V1.Secrets.KeyValue.V2.ReadSecretAsync(
            path: path,
            mountPoint: "secret");

        return secret.Data.Data;
    }

    /// <summary>
    /// Renew the current token.
    /// </summary>
    public async Task RenewTokenAsync(CancellationToken ct = default)
    {
        await _client.V1.Auth.Token.RenewSelfAsync();
    }

    public ValueTask DisposeAsync() => ValueTask.CompletedTask;
}
```

### Kubernetes Authentication

For applications running in Kubernetes:

```bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure the auth method
vault write auth/kubernetes/config \
    kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

# Create a role for the application
vault write auth/kubernetes/role/myapp \
    bound_service_account_names=myapp-sa \
    bound_service_account_namespaces=production \
    policies=myapp-policy \
    ttl=1h
```

#### Kubernetes Sidecar Injection

```yaml
# Pod with Vault Agent sidecar
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  annotations:
    vault.hashicorp.com/agent-inject: "true"
    vault.hashicorp.com/role: "myapp"
    vault.hashicorp.com/agent-inject-secret-config: "secret/data/myapp/config"
    vault.hashicorp.com/agent-inject-template-config: |
      {{- with secret "secret/data/myapp/config" -}}
      DATABASE_URL={{ .Data.data.database_url }}
      API_KEY={{ .Data.data.api_key }}
      {{- end }}
spec:
  serviceAccountName: myapp-sa
  containers:
    - name: myapp
      image: myapp:latest
      volumeMounts:
        - name: vault-secrets
          mountPath: /vault/secrets
          readOnly: true
```

## Secret Engines

### KV v2 (Versioned Key-Value)

```bash
# Enable KV v2
vault secrets enable -version=2 -path=secret kv

# Store a secret
vault kv put secret/myapp/database \
    username="dbuser" \
    password="supersecret" \
    host="db.example.com"

# Read current version
vault kv get secret/myapp/database

# Read specific version
vault kv get -version=2 secret/myapp/database

# List secret versions
vault kv metadata get secret/myapp/database

# Delete specific version (soft delete)
vault kv delete -versions=1 secret/myapp/database

# Destroy version (permanent)
vault kv destroy -versions=1 secret/myapp/database

# Undelete (recover soft-deleted)
vault kv undelete -versions=1 secret/myapp/database
```

### Database Secrets Engine

Dynamic database credentials with automatic rotation:

```bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL
vault write database/config/mydb \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb?sslmode=require" \
    allowed_roles="readonly,readwrite" \
    username="vault" \
    password="vault-password"

# Create readonly role
vault write database/roles/readonly \
    db_name=mydb \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    revocation_statements="DROP ROLE IF EXISTS \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# Create readwrite role
vault write database/roles/readwrite \
    db_name=mydb \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    revocation_statements="DROP ROLE IF EXISTS \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="8h"

# Get dynamic credentials
vault read database/creds/readonly
# username: v-approle-readonly-abc123
# password: A1b2C3d4E5f6G7h8
# lease_id: database/creds/readonly/abc123
# lease_duration: 1h
```

#### Dynamic Credentials in Application

```csharp
using Npgsql;
using VaultSharp;

/// <summary>
/// Database client with Vault-managed dynamic credentials.
/// </summary>
public sealed class DynamicDatabaseClient(IVaultClient vault, string role = "readonly") : IAsyncDisposable
{
    private string? _leaseId;

    /// <summary>
    /// Get dynamic database credentials from Vault.
    /// </summary>
    private async Task<(string Username, string Password)> GetCredentialsAsync(CancellationToken ct = default)
    {
        var response = await vault.V1.Secrets.Database.GetCredentialsAsync(role);

        _leaseId = response.LeaseId;

        return (response.Data.Username, response.Data.Password);
    }

    /// <summary>
    /// Revoke current credentials.
    /// </summary>
    public async Task RevokeCredentialsAsync(CancellationToken ct = default)
    {
        if (_leaseId is not null)
        {
            await vault.V1.System.RevokeLeaseAsync(_leaseId);
            _leaseId = null;
        }
    }

    /// <summary>
    /// Get a database connection with dynamic credentials.
    /// </summary>
    public async Task<NpgsqlConnection> GetConnectionAsync(
        string database,
        string host,
        int port = 5432,
        CancellationToken ct = default)
    {
        var (username, password) = await GetCredentialsAsync(ct);

        var connectionString = new NpgsqlConnectionStringBuilder
        {
            Host = host,
            Port = port,
            Database = database,
            Username = username,
            Password = password,
            SslMode = SslMode.Require
        }.ConnectionString;

        var connection = new NpgsqlConnection(connectionString);
        await connection.OpenAsync(ct);
        return connection;
    }

    /// <summary>
    /// Execute work with an automatically managed connection.
    /// </summary>
    public async Task<T> UseConnectionAsync<T>(
        string database,
        string host,
        Func<NpgsqlConnection, Task<T>> work,
        CancellationToken ct = default)
    {
        await using var connection = await GetConnectionAsync(database, host, ct: ct);
        return await work(connection);
    }

    public async ValueTask DisposeAsync()
    {
        // Optionally revoke immediately, or let TTL expire
        // await RevokeCredentialsAsync();
    }
}
```

### Transit Secrets Engine (Encryption as a Service)

```bash
# Enable transit engine
vault secrets enable transit

# Create an encryption key
vault write -f transit/keys/myapp-key \
    type=aes256-gcm96 \
    exportable=false \
    allow_plaintext_backup=false

# Encrypt data
vault write transit/encrypt/myapp-key \
    plaintext=$(echo -n "my secret data" | base64)
# ciphertext: vault:v1:abc123...

# Decrypt data
vault write transit/decrypt/myapp-key \
    ciphertext="vault:v1:abc123..."
# plaintext: bXkgc2VjcmV0IGRhdGE= (base64)

# Rotate key
vault write -f transit/keys/myapp-key/rotate

# Rewrap data with new key version
vault write transit/rewrap/myapp-key \
    ciphertext="vault:v1:abc123..."
# ciphertext: vault:v2:xyz789... (encrypted with v2)
```

#### Transit in Application

```csharp
using System.Text;
using VaultSharp;
using VaultSharp.V1.SecretsEngines.Transit;

/// <summary>
/// Encryption as a service using Vault Transit.
/// </summary>
public sealed class VaultTransitClient(IVaultClient vault, string keyName, string mountPoint = "transit")
{
    /// <summary>
    /// Encrypt plaintext using Vault Transit.
    /// </summary>
    public async Task<string> EncryptAsync(string plaintext, CancellationToken ct = default)
    {
        var encoded = Convert.ToBase64String(Encoding.UTF8.GetBytes(plaintext));

        var response = await vault.V1.Secrets.Transit.EncryptAsync(
            keyName: keyName,
            encryptRequestOptions: new EncryptRequestOptions { Base64EncodedPlainText = encoded },
            mountPoint: mountPoint);

        return response.Data.CipherText;
    }

    /// <summary>
    /// Decrypt ciphertext using Vault Transit.
    /// </summary>
    public async Task<string> DecryptAsync(string ciphertext, CancellationToken ct = default)
    {
        var response = await vault.V1.Secrets.Transit.DecryptAsync(
            keyName: keyName,
            decryptRequestOptions: new DecryptRequestOptions { CipherText = ciphertext },
            mountPoint: mountPoint);

        var decoded = Convert.FromBase64String(response.Data.Base64EncodedPlainText);
        return Encoding.UTF8.GetString(decoded);
    }

    /// <summary>
    /// Encrypt multiple items in a single request.
    /// </summary>
    public async Task<List<string>> EncryptBatchAsync(IEnumerable<string> items, CancellationToken ct = default)
    {
        var batchInput = items
            .Select(item => new EncryptionItem
            {
                Base64EncodedPlainText = Convert.ToBase64String(Encoding.UTF8.GetBytes(item))
            })
            .ToList();

        var response = await vault.V1.Secrets.Transit.EncryptAsync(
            keyName: keyName,
            encryptRequestOptions: new EncryptRequestOptions { BatchedEncryptionItems = batchInput },
            mountPoint: mountPoint);

        return response.Data.BatchedResults
            .Select(r => r.CipherText)
            .ToList();
    }

    /// <summary>
    /// Decrypt multiple items in a single request.
    /// </summary>
    public async Task<List<string>> DecryptBatchAsync(IEnumerable<string> ciphertexts, CancellationToken ct = default)
    {
        var batchInput = ciphertexts
            .Select(ct => new DecryptionItem { CipherText = ct })
            .ToList();

        var response = await vault.V1.Secrets.Transit.DecryptAsync(
            keyName: keyName,
            decryptRequestOptions: new DecryptRequestOptions { BatchedDecryptionItems = batchInput },
            mountPoint: mountPoint);

        return response.Data.BatchedResults
            .Select(r => Encoding.UTF8.GetString(Convert.FromBase64String(r.Base64EncodedPlainText)))
            .ToList();
    }
}
```

## Policy Patterns

### Least Privilege Policies

```hcl
# Application policy - minimal access
path "secret/data/myapp/*" {
  capabilities = ["read"]
}

path "database/creds/myapp-readonly" {
  capabilities = ["read"]
}

# Deny access to metadata (prevents enumeration)
path "secret/metadata/*" {
  capabilities = ["deny"]
}
```

### Environment-Based Policies

```hcl
# Production policy - strict access
path "secret/data/production/*" {
  capabilities = ["read"]
  # Require MFA for production secrets
  required_parameters = ["mfa_token"]
}

# Development policy - more permissive
path "secret/data/development/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Staging can read from development
path "secret/data/development/*" {
  capabilities = ["read"]
}
path "secret/data/staging/*" {
  capabilities = ["read"]
}
```

### Admin Policies

```hcl
# Full admin (use sparingly)
path "*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Secrets admin (manage secrets, not auth/audit)
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Auth admin
path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Policy admin
path "sys/policies/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
```

## High Availability Patterns

### Raft Storage (Integrated HA)

```hcl
# vault-config.hcl
storage "raft" {
  path    = "/vault/data"
  node_id = "node1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "/vault/certs/vault.crt"
  tls_key_file  = "/vault/certs/vault.key"
}

cluster_addr = "https://node1.vault.example.com:8201"
api_addr     = "https://node1.vault.example.com:8200"
```

### Joining Raft Cluster

```bash
# Initialize first node
vault operator init -key-shares=5 -key-threshold=3

# Unseal first node
vault operator unseal <key1>
vault operator unseal <key2>
vault operator unseal <key3>

# Join additional nodes to cluster
vault operator raft join https://node1.vault.example.com:8200

# Unseal joined node
vault operator unseal <key1>
vault operator unseal <key2>
vault operator unseal <key3>

# Check cluster status
vault operator raft list-peers
```

## Disaster Recovery

### Snapshots

```bash
# Create snapshot
vault operator raft snapshot save backup.snap

# Restore snapshot (on fresh cluster)
vault operator raft snapshot restore backup.snap
```

### Auto-Unseal with Cloud KMS

```hcl
# AWS KMS auto-unseal
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "alias/vault-unseal-key"
}

# Azure Key Vault auto-unseal
seal "azurekeyvault" {
  tenant_id     = "tenant-id"
  vault_name    = "vault-unseal"
  key_name      = "vault-unseal-key"
}

# GCP Cloud KMS auto-unseal
seal "gcpckms" {
  project     = "my-project"
  region      = "global"
  key_ring    = "vault-keyring"
  crypto_key  = "vault-unseal-key"
}
```

## Security Best Practices

### Audit Logging

```bash
# Enable file audit device
vault audit enable file file_path=/var/log/vault/audit.log

# Enable syslog audit device
vault audit enable syslog tag="vault" facility="AUTH"

# Audit logs capture all operations
# NEVER disable all audit devices in production
```

### TLS Configuration

```hcl
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/vault/certs/vault.crt"
  tls_key_file  = "/vault/certs/vault.key"

  # Strong TLS configuration
  tls_min_version = "tls12"
  tls_cipher_suites = "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"
}
```

### Token Management

```bash
# Use short TTLs
vault token create -ttl=1h -policy=myapp

# Revoke tokens when no longer needed
vault token revoke <token>

# Revoke all tokens for a user
vault token revoke -accessor <accessor>

# Use token roles for consistency
vault write auth/token/roles/myapp \
    allowed_policies="myapp-policy" \
    orphan=true \
    renewable=true \
    token_ttl="1h" \
    token_max_ttl="4h"
```

## Security Checklist

### Infrastructure

- [ ] TLS enabled and enforced
- [ ] Auto-unseal configured (no manual key management)
- [ ] Audit logging enabled (multiple devices)
- [ ] High availability configured
- [ ] Network segmentation (Vault isolated)
- [ ] Regular snapshots and backup testing

### Authentication

- [ ] Root token revoked after setup
- [ ] AppRole for applications, OIDC for humans
- [ ] Short token TTLs (1h or less)
- [ ] MFA required for sensitive operations

### Authorization

- [ ] Least privilege policies
- [ ] No wildcard paths in production policies
- [ ] Regular policy audits
- [ ] Environment separation enforced

### Operations

- [ ] Secret rotation scheduled
- [ ] Lease management implemented
- [ ] Monitoring and alerting configured
- [ ] Incident response plan documented
