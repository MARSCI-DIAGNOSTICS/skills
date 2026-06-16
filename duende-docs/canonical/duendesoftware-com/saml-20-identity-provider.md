---
title: SAML 2.0 Identity Provider
source_url: https://docs.duendesoftware.com/saml-20-identity-provider/
source_type: llms-full-txt
content_hash: sha256:3a7bc97a96a1937c6dbe54adf40567abdbb2b95f89d42fd2e78cdaf0844ba5f9
doc_id: saml-20-identity-provider
---

> Overview of IdentityServer's SAML 2.0 Identity Provider support for issuing SAML assertions to enterprise Service Providers.

Added in 8.0 (prerelease)

<!--
:::note
SAML 2.0 Identity Provider support requires a **Duende IdentityServer Enterprise Edition** license.
:::
-->

IdentityServer can act as a **SAML 2.0 Identity Provider (IdP)**, issuing SAML assertions to Service Providers (SPs). This enables integration with enterprise applications and legacy systems that use the SAML 2.0 protocol rather than OAuth 2.0 / OpenID Connect.

## When to Use SAML 2.0

[Section titled "When to Use SAML 2.0"](#when-to-use-saml-20)

SAML 2.0 support is useful when:

* You need to integrate with enterprise SaaS applications that require SAML (e.g., Salesforce, Workday, ServiceNow)
* You are migrating from a legacy SSO system that uses SAML
* Your organization has compliance or procurement requirements for SAML-based federation

For new integrations, OpenID Connect is recommended. SAML 2.0 support is provided for interoperability with existing SAML-based systems.

## Quick Setup

[Section titled "Quick Setup"](#quick-setup)

### 1. Register SAML Services

[Section titled "1. Register SAML Services"](#1-register-saml-services)

Call `AddSaml()` on the IdentityServer builder:

Program.cs

```csharp
builder.Services.AddIdentityServer()
    .AddSaml();
```

This enables all SAML endpoints except IdP-initiated SSO (which requires explicit opt-in).

### 2. Register Service Providers

[Section titled "2. Register Service Providers"](#2-register-service-providers)

Register your SAML Service Providers using the in-memory store (for development/testing) or a custom `ISamlServiceProviderStore` implementation (for production):

Program.cs

```csharp
builder.Services.AddIdentityServer()
    .AddSaml()
    .AddInMemorySamlServiceProviders(new[]
    {
        new SamlServiceProvider
        {
            EntityId = "https://sp.example.com",
            DisplayName = "Example SP",
            AssertionConsumerServiceUrls = new[] { new Uri("https://sp.example.com/acs") },
            AssertionConsumerServiceBinding = SamlBinding.HttpPost,
        }
    });
```

### 3. Configure Protocol Type (Optional)

[Section titled "3. Configure Protocol Type (Optional)"](#3-configure-protocol-type-optional)

SAML 2.0 uses the protocol type constant `IdentityServerConstants.ProtocolTypes.Saml2p` (`"saml2p"`). This is used in logging, discovery, and extensibility hooks.

## Protocol Endpoints

[Section titled "Protocol Endpoints"](#protocol-endpoints)

SAML 2.0 endpoints are registered under the `/saml` path prefix:

| Endpoint          | Path                    |
| ----------------- | ----------------------- |
| Metadata          | `/saml/metadata`        |
| Sign-in           | `/saml/signin`          |
| Sign-in Callback  | `/saml/signin_callback` |
| IdP-initiated SSO | `/saml/idp-initiated`   |
| Logout            | `/saml/logout`          |
| Logout Callback   | `/saml/logout_callback` |

See [SAML Endpoints](/identityserver/saml/endpoints/) for full details.
