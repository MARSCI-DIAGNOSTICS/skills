---
title: SAML Extensibility
source_url: https://docs.duendesoftware.com/saml-extensibility/
source_type: llms-full-txt
content_hash: sha256:45308a020dec64b4fa518e8519af7e4a0aef79a68c85dcfa8629c956b0e0a013
doc_id: saml-extensibility
---

> Extensibility interfaces for customizing SAML 2.0 Identity Provider behavior, including claims mapping, interaction, and response generation.

Added in 8.0 (prerelease)

IdentityServer's SAML 2.0 Identity Provider feature exposes several extensibility interfaces that you can implement to customize SAML behavior. All interfaces are registered in the DI container and can be replaced with custom implementations.

## ISamlClaimsMapper

[Section titled "ISamlClaimsMapper"](#isamlclaimsmapper)

Customizes how user claims are mapped to SAML attributes in the assertion.

```csharp
public interface ISamlClaimsMapper
{
    Task<IEnumerable<SamlAttribute>> MapClaimsAsync(SamlClaimsMappingContext context);
}
```

### When to Use

[Section titled "When to Use"](#when-to-use)

Override this interface when the built-in claim mapping (configured via `SamlOptions.DefaultClaimMappings` and `SamlServiceProvider.ClaimMappings`) is not flexible enough. Registering a custom `ISamlClaimsMapper` **completely replaces** the default mapping logic.

### Context

[Section titled "Context"](#context)

`SamlClaimsMappingContext` provides:

* `UserClaims` -- the user's claims to be mapped to SAML attributes
* `ServiceProvider` -- the `SamlServiceProvider` that initiated the request

### Registration

[Section titled "Registration"](#registration)

Register via DI by replacing the default:

Program.cs

```csharp
builder.Services.AddScoped<ISamlClaimsMapper, MyClaimsMapper>();
```

### Example

[Section titled "Example"](#example)

MyClaimsMapper.cs

```csharp
public class MyClaimsMapper : ISamlClaimsMapper
{
    public Task<IEnumerable<SamlAttribute>> MapClaimsAsync(SamlClaimsMappingContext context)
    {
        var attributes = context.UserClaims
            .Where(c => c.Type == "email")
            .Select(c => new SamlAttribute
            {
                Name = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
                Values = new[] { c.Value }
            });


        return Task.FromResult(attributes);
    }
}
```

***

## ISamlInteractionService

[Section titled "ISamlInteractionService"](#isamlinteractionservice)

Provides services for the login UI to communicate with IdentityServer during SAML authentication flows.

```csharp
public interface ISamlInteractionService
{
    Task<SamlAuthenticationRequest?> GetAuthenticationRequestContextAsync(
        CancellationToken ct = default);


    Task StoreRequestedAuthnContextResultAsync(
        bool requestedAuthnContextRequirementsWereMet,
        CancellationToken ct = default);
}
```

### When to Use

[Section titled "When to Use"](#when-to-use-1)

Inject `ISamlInteractionService` into your login UI pages to:

* Retrieve the current SAML authentication request context (SP name, requested AuthnContext, etc.)
* Report back to IdentityServer whether the user's authentication met the SP's `RequestedAuthnContext` requirements

If `StoreRequestedAuthnContextResultAsync` is called with `false`, IdentityServer will include a SAML `NoAuthnContext` status code in the response, as per SAML Core spec section 3.3.2.2.1.

***

## ISamlSigninInteractionResponseGenerator

[Section titled "ISamlSigninInteractionResponseGenerator"](#isamlsignininteractionresponsegenerator)

Determines what interaction (login, consent, error) is required during a SAML sign-in flow.

```csharp
public interface ISamlSigninInteractionResponseGenerator
{
    Task<SamlInteractionResponse> ProcessInteractionAsync(
        SamlServiceProvider sp,
        AuthNRequest request,
        CancellationToken ct = default);
}
```

### When to Use

[Section titled "When to Use"](#when-to-use-2)

Override this interface to customize the interaction flow for SAML sign-in requests -- for example, to implement custom step-up authentication logic, or to enforce per-SP consent requirements.

The default implementation (`DefaultSamlSigninInteractionResponseGenerator`) handles standard login and consent flows.

### Registration

[Section titled "Registration"](#registration-1)

Program.cs

```csharp
builder.Services.AddScoped<ISamlSigninInteractionResponseGenerator, MySamlSigninInteractionGenerator>();
```

***

## ISamlLogoutNotificationService

[Section titled "ISamlLogoutNotificationService"](#isamllogoutnotificationservice)

Builds the front-channel logout notifications that IdentityServer sends to SAML Service Providers when a user logs out.

```csharp
public interface ISamlLogoutNotificationService
{
    Task<IEnumerable<ISamlFrontChannelLogout>> GetSamlFrontChannelLogoutsAsync(
        LogoutNotificationContext context,
        CancellationToken ct);
}
```

### When to Use

[Section titled "When to Use"](#when-to-use-3)

Override this interface to customize which Service Providers receive logout notifications, or to modify the logout messages sent. The default implementation sends a SAML `LogoutRequest` to each SP that has a configured `SingleLogoutServiceUrl`.

### Registration

[Section titled "Registration"](#registration-2)

Program.cs

```csharp
builder.Services.AddScoped<ISamlLogoutNotificationService, MySamlLogoutNotificationService>();
```

***

## ISamlFrontChannelLogout

[Section titled "ISamlFrontChannelLogout"](#isamlfrontchannellogout)

Represents a single front-channel logout notification to be sent to a Service Provider. This is a data interface returned by `ISamlLogoutNotificationService`; you typically do not need to implement it directly.

```csharp
public interface ISamlFrontChannelLogout
{
    SamlBinding SamlBinding { get; }
    Uri Destination { get; }
    string EncodedContent { get; }
    string? RelayState { get; }
}
```

Each instance represents a SAML `LogoutRequest` (or response) message encoded for delivery to a specific SP via the specified binding and destination URL.
