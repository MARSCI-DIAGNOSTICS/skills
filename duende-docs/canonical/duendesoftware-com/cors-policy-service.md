---
title: CORS Policy Service
source_url: https://docs.duendesoftware.com/identityserver/reference/stores/cors-policy-service/
source_type: llms-full-txt
content_hash: sha256:e1c4cf3c7c2e1c3cb16ae484c71194ddfca15fd3a7c00de8d0826c9e23f7b0a0
doc_id: cors-policy-service
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
    /// <returns></returns>
    Task<bool> IsOriginAllowedAsync(string origin);
}
```
