---
title: Issuing Internal Tokens
source_url: https://docs.duendesoftware.com/issuing-internal-tokens/
source_type: llms-full-txt
content_hash: sha256:21e6058b2f0e1fa40e50745fdd08f827e6fb6ce135e3e6a4bd130016914aa3d0
doc_id: issuing-internal-tokens
---

> A guide to using the IIdentityServerTools interface for creating JWT tokens internally within IdentityServer's extensibility code, without going through the protocol endpoints.

Sometimes, extensibility code running on your IdentityServer needs access tokens to call other APIs. In this case it is not necessary to use the protocol endpoints. The tokens can be issued internally.

`IIdentityServerTools` is a collection of useful internal tools that you might need when writing extensibility code for IdentityServer. To use it, inject it into your code, e.g. an endpoint:

```csharp
app.MapGet("/myAction", async (IIdentityServerTools tools) =>
{
    var token = await tools.IssueClientJwtAsync(
        clientId: "client_id",
        lifetime: 3600,
        audiences: new[] { "backend.api" });


    // more code
});
```

The `IIdentityServerTools` interface was added in v7 to allow mocking. Previous versions referenced the `IdentityServerTools` implementation class directly.
