---
title: Options
source_url: https://docs.duendesoftware.com/bff/fundamentals/options/
source_type: llms-full-txt
content_hash: sha256:43a6cb3db191ebd32561e0c8a64fb3264fa4f97348112190759ac3816fe8c8aa
doc_id: bff/fundamentals/options
---

> Reference documentation for the IdentityServer configuration options related to dynamic client registration and secret lifetimes.

The page describes the `IdentityServerConfigurationOptions` class, which provides top-level configuration options for IdentityServer, including the `DynamicClientRegistrationOptions` class for managing dynamic client registration and secret lifetimes.

## IdentityServerConfigurationOptions

[Section titled "IdentityServerConfigurationOptions"](#identityserverconfigurationoptions)

Top-level options for IdentityServer.Configuration.

```csharp
public class IdentityServerConfigurationOptions
```

### Public Members

[Section titled "Public Members"](#public-members)

| name                                                                         | description                             |
| ---------------------------------------------------------------------------- | --------------------------------------- |
| [DynamicClientRegistration](#dynamicclientregistrationoptions) { get; set; } | Options for Dynamic Client Registration |

## DynamicClientRegistrationOptions

[Section titled "DynamicClientRegistrationOptions"](#dynamicclientregistrationoptions)

Options for dynamic client registration.

```csharp
public class DynamicClientRegistrationOptions
```

### Public Members

[Section titled "Public Members"](#public-members-1)

| name                         | description                                                                                                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SecretLifetime { get; set; } | Gets or sets the lifetime of secrets generated for clients. If unset, generated secrets will have no expiration. Defaults to null (secrets never expire). |
