---
title: Secrets
source_url: https://docs.duendesoftware.com/identityserver/reference/models/secrets/
source_type: llms-full-txt
content_hash: sha256:5ed12c9dbfe96fdd2375c65c1ebf84eb58379e8c535c39b6e6ee798ee6b8f08b
doc_id: identityserver/reference/models/secrets
---

> Reference documentation for secret handling in Duende IdentityServer, including the ISecretParser interface for extracting secrets from HTTP requests, the ParsedSecret class, and the ISecretValidator interface.

## Duende.IdentityServer.Validation.ISecretParser

[Section titled "Duende.IdentityServer.Validation.ISecretParser"](#duendeidentityservervalidationisecretparser)

Parses a secret from the raw HTTP request.

```csharp
public interface ISecretParser
{
    /// <summary>
    /// Tries to find a secret on the context that can be used for authentication
    /// </summary>
    /// <param name="context">The HTTP context.</param>
    /// <returns>A parsed secret</returns>
    Task<ParsedSecret> ParseAsync(HttpContext context);


    /// <summary>
    /// Returns the authentication method name that this parser implements
    /// </summary>
    /// <value>The authentication method.</value>
    string AuthenticationMethod { get; }
}
```

* **`AuthenticationMethod`**

  The name of the authentication method that this parser registers for. This value must be unique and will be displayed in the discovery document.

* **`ParseAsync`**

  The job of this method is to extract the secret from the HTTP request and parse it into a `ParsedSecret`

#### Duende.IdentityServer.Model.ParsedSecret

[Section titled "Duende.IdentityServer.Model.ParsedSecret"](#duendeidentityservermodelparsedsecret)

Represents a parsed secret.

```csharp
/// <summary>
/// Represents a secret extracted from the HttpContext
/// </summary>
public class ParsedSecret
{
    /// <summary>
    /// Gets or sets the identifier associated with this secret
    /// </summary>
    /// <value>
    /// The identifier.
    /// </value>
    public string Id { get; set; }


    /// <summary>
    /// Gets or sets the credential to verify the secret
    /// </summary>
    /// <value>
    /// The credential.
    /// </value>
    public object Credential { get; set; }


    /// <summary>
    /// Gets or sets the type of the secret
    /// </summary>
    /// <value>
    /// The type.
    /// </value>
    public string Type { get; set; }


    /// <summary>
    /// Gets or sets additional properties.
    /// </summary>
    /// <value>
    /// The properties.
    /// </value>
    public Dictionary<string, string> Properties { get; set; } = new Dictionary<string, string>();
}
```

The parsed secret is forwarded to the registered secret validator. The validator will typically inspect the `Type` property to determine if this secret is something that can be validated by that validator instance. If yes, it will know how to cast the `Credential` object into a format that is understood.

#### Duende.IdentityServer.Validation.ISecretParser

[Section titled "Duende.IdentityServer.Validation.ISecretParser"](#duendeidentityservervalidationisecretparser-1)

Validates a parsed secret.

```csharp
public interface ISecretValidator
{
    /// <summary>Validates a secret</summary>
    /// <param name="secrets">The stored secrets.</param>
    /// <param name="parsedSecret">The received secret.</param>
    /// <returns>A validation result</returns>
    Task<SecretValidationResult> ValidateAsync(
      IEnumerable<Secret> secrets,
      ParsedSecret parsedSecret);
}
```
