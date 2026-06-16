---
title: SAML Configuration
source_url: https://docs.duendesoftware.com/saml-configuration/
source_type: llms-full-txt
content_hash: sha256:4d3b557ba5f3560a96a4b8490c8e44ca31d9b2e9b91af604084e7dec6efcc743
doc_id: saml-configuration
---

> Configuration options and models for the SAML 2.0 Identity Provider feature, including SamlOptions and SamlServiceProvider settings.

Added in 8.0 (prerelease)

This page documents the configuration options and models for the SAML 2.0 Identity Provider feature.

## Setup

[Section titled "Setup"](#setup)

Call `AddSaml()` on the IdentityServer builder to enable SAML 2.0 support:

Program.cs

```csharp
builder.Services.AddIdentityServer()
    .AddSaml();
```

`AddSaml()` registers all SAML services and enables the five standard SAML endpoints. The IdP-initiated SSO endpoint is **not** enabled by default and requires explicit opt-in (see [Enabling IdP-Initiated SSO](#enabling-idp-initiated-sso) below).

## SamlOptions

[Section titled "SamlOptions"](#samloptions)

`SamlOptions` controls the global behavior of the SAML 2.0 Identity Provider. Access it via `IdentityServerOptions.Saml`:

Program.cs

```csharp
builder.Services.AddIdentityServer(options =>
{
    options.Saml.DefaultSigningBehavior = SamlSigningBehavior.SignAssertion;
    options.Saml.DefaultClockSkew = TimeSpan.FromMinutes(5);
    options.Saml.WantAuthnRequestsSigned = false;
});
```

Available options:

* **`MetadataValidityDuration`** If set, the metadata document includes a `validUntil` attribute. Defaults to 7 days.

* **`WantAuthnRequestsSigned`** When `true`, the IdP requires all AuthnRequests to be signed. Defaults to `false`.

* **`DefaultAttributeNameFormat`** Default SAML attribute name format URI for attributes in assertions. Defaults to `uri`.

* **`DefaultPersistentNameIdentifierClaimType`** Claim type used to resolve a persistent NameID value. Defaults to `ClaimTypes.NameIdentifier`.

* **`DefaultClaimMappings`** Maps OIDC claim types to SAML attribute names. See below.

* **`SupportedNameIdFormats`** Supported NameID formats for the IdP. Defaults to `[ Email, Persistent, Transient, Unspecified ]`.

* **`DefaultClockSkew`** Clock skew tolerance for validating SAML message timestamps. Defaults to 5 minutes.

* **`DefaultRequestMaxAge`** Maximum age for SAML AuthnRequests. Defaults to 5 minutes.

* **`DefaultSigningBehavior`** Default signing behavior for SAML responses. Defaults to `SignAssertion`.

* **`MaxRelayStateLength`** Maximum length (in UTF-8 bytes) of the RelayState parameter. Defaults to 80.

* **`UserInteraction`** Configures SAML endpoint paths. See below.

### Default Claim Mappings

[Section titled "Default Claim Mappings"](#default-claim-mappings)

The default `DefaultClaimMappings` dictionary maps common OIDC claim types to SAML 2.0 attribute names:

| Claim type | SAML attribute name                                                  |
| ---------- | -------------------------------------------------------------------- |
| `name`     | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name`         |
| `email`    | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` |
| `role`     | `http://schemas.xmlsoap.org/ws/2005/05/identity/role`                |

Claims not present in this mapping are excluded from the SAML assertion. Override mappings globally via `SamlOptions.DefaultClaimMappings` or per Service Provider via `SamlServiceProvider.ClaimMappings`.

## SamlUserInteractionOptions

[Section titled "SamlUserInteractionOptions"](#samluserinteractionoptions)

`SamlUserInteractionOptions` configures the URL paths for all SAML endpoints. All paths are relative to the application root.

* **`Route`** Base route prefix for all SAML endpoints. Defaults to `/saml`.

* **`Metadata`** Path suffix for the metadata endpoint. Defaults to `/metadata`.

* **`SignInPath`** Path suffix for the SP-initiated sign-in endpoint. Defaults to `/signin`.

* **`SignInCallbackPath`** Path suffix for the sign-in callback endpoint. Defaults to `/signin_callback`.

* **`IdpInitiatedPath`** Path suffix for the IdP-initiated SSO endpoint. Defaults to `/idp-initiated`.

* **`SingleLogoutPath`** Path suffix for the single logout endpoint. Defaults to `/logout`.

* **`SingleLogoutCallbackPath`** Path suffix for the logout callback endpoint. Defaults to `/logout_callback`.

The full URL for each endpoint is formed by combining the base URL of the IdentityServer host with the `Route` prefix and the individual path suffix. For example, the metadata endpoint is available at `https://your-idp.example.com/saml/metadata` by default.

## SamlServiceProvider Model

[Section titled "SamlServiceProvider Model"](#samlserviceprovider-model)

`SamlServiceProvider` represents a registered SAML 2.0 Service Provider configuration.

Available options:

* **`EntityId`** The SP's entity identifier URI, as declared in its SAML metadata. Required.

* **`DisplayName`** Human-readable name shown in logs and consent screens. Required.

* **`Description`** Optional description. Defaults to `null`.

* **`Enabled`** When `false`, all SAML requests from this SP are rejected. Defaults to `true`.

* **`ClockSkew`** Per-SP clock skew override. Uses `SamlOptions.DefaultClockSkew` when `null`. Defaults to `null`.

* **`RequestMaxAge`** Per-SP request maximum age. Uses `SamlOptions.DefaultRequestMaxAge` when `null`. Defaults to `null`.

* **`AssertionConsumerServiceUrls`** ACS URLs where SAML responses will be delivered. At least one is required.

* **`AssertionConsumerServiceBinding`** SAML binding for the ACS (`HttpPost` or `HttpRedirect`).

* **`SingleLogoutServiceUrl`** SP's Single Logout Service endpoint. Required for SLO support. Defaults to `null`.

* **`RequireSignedAuthnRequests`** When `true`, unsigned AuthnRequests from this SP are rejected. Defaults to `false`.

* **`SigningCertificates`** Certificates used to verify SP-signed messages. Defaults to `null`.

* **`EncryptionCertificates`** Certificates used to encrypt assertions for this SP. Defaults to `null`.

* **`EncryptAssertions`** When `true`, assertions are encrypted using `EncryptionCertificates`. Defaults to `false`.

* **`RequireConsent`** When `true`, the user is always shown a consent screen. Defaults to `false`.

* **`AllowIdpInitiated`** When `true`, IdP-initiated SSO is allowed for this SP. Defaults to `false`.

* **`ClaimMappings`** Per-SP claim-to-attribute mappings that override `SamlOptions.DefaultClaimMappings`. Defaults to `{}`.

* **`DefaultNameIdFormat`** Default NameID format to use when the SP does not specify one. Defaults to `urn:...unspecified`.

* **`DefaultPersistentNameIdentifierClaimType`** Per-SP override for the claim type used to resolve a persistent NameID. Defaults to `null`.

* **`SigningBehavior`** Per-SP signing behavior. Uses `SamlOptions.DefaultSigningBehavior` when `null`. Defaults to `null`.

## Enums

[Section titled "Enums"](#enums)

### SamlBinding

[Section titled "SamlBinding"](#samlbinding)

Defines the SAML protocol binding used for message transport:

| Value          | Description                                                                           |
| -------------- | ------------------------------------------------------------------------------------- |
| `HttpRedirect` | HTTP-Redirect binding. The SAML message is URL-encoded and sent as a query parameter. |
| `HttpPost`     | HTTP-POST binding. The SAML message is Base64-encoded and sent in an HTML form.       |

### SamlSigningBehavior

[Section titled "SamlSigningBehavior"](#samlsigningbehavior)

Controls what elements are signed in SAML responses:

| Value           | Description                                                                           |
| --------------- | ------------------------------------------------------------------------------------- |
| `DoNotSign`     | No signing. For testing only -- do not use in production.                              |
| `SignResponse`  | Signs the entire SAML `<Response>` element.                                           |
| `SignAssertion` | Signs the `<Assertion>` element inside the response. **Recommended.**                 |
| `SignBoth`      | Signs both the `<Response>` and the `<Assertion>`. Maximum security, larger messages. |

### SamlEndpointType

[Section titled "SamlEndpointType"](#samlendpointtype)

`SamlEndpointType` is a class (not an enum) that represents a SAML endpoint with a location and binding. Used for `SamlServiceProvider.SingleLogoutServiceUrl`:

```csharp
new SamlServiceProvider
{
    // ...
    SingleLogoutServiceUrl = new SamlEndpointType
    {
        Location = new Uri("https://sp.example.com/saml/slo"),
        Binding = SamlBinding.HttpPost,
    }
}
```

## Enabling IdP-Initiated SSO

[Section titled "Enabling IdP-Initiated SSO"](#enabling-idp-initiated-sso)

IdP-initiated SSO is disabled by default. To enable it, set the endpoint option and configure `AllowIdpInitiated = true` on each SP that should permit IdP-initiated flows:

Program.cs

```csharp
builder.Services.AddIdentityServer(options =>
{
    options.Endpoints.EnableSamlIdpInitiatedEndpoint = true;
});
```

```csharp
new SamlServiceProvider
{
    EntityId = "https://sp.example.com",
    AllowIdpInitiated = true,
    // ...
}
```

Caution

IdP-initiated SSO is disabled by default because it is not protected by the usual SAML request binding (there is no AuthnRequest to validate). Only enable it for SPs that you explicitly trust and that require IdP-initiated flows.

## Endpoint Enable/Disable Options

[Section titled "Endpoint Enable/Disable Options"](#endpoint-enabledisable-options)

Individual SAML endpoints can be enabled or disabled via `IdentityServerOptions.Endpoints`:

Program.cs

```csharp
builder.Services.AddIdentityServer(options =>
{
    options.Endpoints.EnableSamlMetadataEndpoint = true;
    options.Endpoints.EnableSamlSigninEndpoint = true;
    options.Endpoints.EnableSamlSigninCallbackEndpoint = true;
    options.Endpoints.EnableSamlIdpInitiatedEndpoint = false; // must opt in
    options.Endpoints.EnableSamlLogoutEndpoint = true;
    options.Endpoints.EnableSamlLogoutCallbackEndpoint = true;
});
```

`AddSaml()` sets all of the above to `true` except `EnableSamlIdpInitiatedEndpoint`.
