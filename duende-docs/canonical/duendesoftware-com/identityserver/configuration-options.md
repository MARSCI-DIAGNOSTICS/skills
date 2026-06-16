---
title: Configuration Options
source_url: https://docs.duendesoftware.com/identityserver/configuration-options/
source_type: llms-full-txt
content_hash: sha256:6fb1df05f3516989e6a5fc95cf0e5b2b6bbf0b510ded34be22f00b5dd711e7ec
category: identityserver
doc_id: identityserver/configuration-options
---

> Configuration options available when using Entity Framework Core as the configuration store in IdentityServer

## Duende.IdentityServer.EntityFramework.Options.ConfigurationStoreOptions

[Section titled "Duende.IdentityServer.EntityFramework.Options.ConfigurationStoreOptions"](#duendeidentityserverentityframeworkoptionsconfigurationstoreoptions)

These options are configurable when using the Entity Framework Core for the [configuration store](/identityserver/data/configuration/):

You set the options at startup time in your `AddConfigurationStore` method:

Program.cs

```csharp
var builder = services.AddIdentityServer()
    .AddConfigurationStore(options =>
    {
        // configure options here..
    })
```

### Pooling

[Section titled "Pooling"](#pooling)

Settings that affect the DbContext pooling feature of Entity Framework Core.

* **`EnablePooling`**

  Gets or set if EF DbContext pooling is enabled. Defaults to `false`.

* **`PoolSize`**

  Gets or set the pool size to use when DbContext pooling is enabled. If not set, the EF default is used.

### Schema

[Section titled "Schema"](#schema)

Settings that affect the database schema and table names.

* **`DefaultSchema`**

  Gets or sets the default schema. Defaults to `null`.

`TableConfiguration` settings for each individual table (schema and name) managed by this feature:

Identity Resource related tables:

* **`IdentityResource`**
* **`IdentityResourceClaim`**
* **`IdentityResourceProperty`**

API Resource related tables:

* **`ApiResource`**
* **`ApiResourceSecret`**
* **`ApiResourceScope`**
* **`ApiResourceClaim`**
* **`ApiResourceProperty`**

Client related tables:

* **`Client`**
* **`ClientGrantType`**
* **`ClientRedirectUri`**
* **`ClientPostLogoutRedirectUri`**
* **`ClientScopes`**
* **`ClientSecret`**
* **`ClientClaim`**
* **`ClientIdPRestriction`**
* **`ClientCorsOrigin`**
* **`ClientProperty`**

API Scope related tables:

* **`ApiScope`**
* **`ApiScopeClaim`**
* **`ApiScopeProperty`**

Identity provider related tables:

* **`IdentityProvider`**
