---
title: CORS Policy Service
source_url: https://docs.duendesoftware.com/identityserver/reference/stores/cors-policy-service/
source_type: llms-full-txt
content_hash: sha256:0e3d5dfe0485912c17df68baee4235ac43ac0d0b2d459c39e95e1e992c8abe51
doc_id: identityserver/reference/stores/cors-policy-service
---

> Documentation for the ICorsPolicyService interface which determines if CORS requests from specific origins are allowed to access protocol endpoints.

#### Duende.IdentityServer.Stores.ICorsPolicyService

[Section titled "Duende.IdentityServer.Stores.ICorsPolicyService"](#duendeidentityserverstoresicorspolicyservice)

Used to determine if CORS requests are allowed to certain protocol endpoints.

```csharp
/// <summary>
/// Service that determines if CORS is allowed.
/// </summary>
public interface ICorsPolicyService
{
    /// <summary>
    /// Determines whether origin is allowed.
    /// </summary>
    /// <param name="origin">The origin.</param>
    /// <param name="ct">The cancellation token.</param>
    /// <returns></returns>
    Task<bool> IsOriginAllowedAsync(string origin, CancellationToken ct);
}
```
