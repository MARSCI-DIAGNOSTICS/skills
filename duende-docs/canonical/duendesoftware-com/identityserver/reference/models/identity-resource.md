---
title: Identity Resource
source_url: https://docs.duendesoftware.com/identityserver/reference/models/identity-resource/
source_type: llms-full-txt
content_hash: sha256:009715d4a94a58c9327c2e9544ed92c08b139481abf15097627c413809af8c6b
doc_id: identityserver/reference/models/identity-resource
---

> Reference documentation for the IdentityResource class which models an identity resource in Duende IdentityServer, including standard and custom identity resources and their properties.

## Duende.IdentityServer.Models.IdentityResource

[Section titled "Duende.IdentityServer.Models.IdentityResource"](#duendeidentityservermodelsidentityresource)

This class models an identity resource.

```csharp
public static readonly IEnumerable<IdentityResource> IdentityResources =
    new[]
    {
        // some standard scopes from the OIDC spec
        new IdentityResources.OpenId(),
        new IdentityResources.Profile(),
        new IdentityResources.Email(),


        // custom identity resource with some associated claims
        new IdentityResource("custom.profile",
            userClaims: new[] { JwtClaimTypes.Name, JwtClaimTypes.Email, "location", JwtClaimTypes.Address })
    };
```

* **`Enabled`**

  Indicates if this resource is enabled and can be requested. Defaults to true.

* **`Name`**

  The unique name of the identity resource. This is the value a client will use for the scope parameter in the authorize request.

* **`DisplayName`**

  This value will be used e.g. on the consent screen.

* **`Description`**

  This value will be used e.g. on the consent screen.

* **`Required`**

  Specifies whether the user can de-select the scope on the consent screen (if the consent screen wants to implement such a feature). Defaults to false.

* **`Emphasize`**

  Specifies whether the consent screen will emphasize this scope (if the consent screen wants to implement such a feature). Use this setting for sensitive or important scopes. Defaults to false.

* **`ShowInDiscoveryDocument`**

  Specifies whether this scope is shown in the discovery document. Defaults to `true`.

* **`UserClaims`**

  List of associated user claim types that should be included in the identity token.
