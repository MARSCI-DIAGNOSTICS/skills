---
title: Client Application Portal
source_url: https://docs.duendesoftware.com/client-application-portal/
source_type: llms-full-txt
content_hash: sha256:b2df9f8b34ec0479d74bd8a1dd33431a4bd48434640de67685c0a279186a4f44
doc_id: client-application-portal
---

> Documentation for creating a client application portal within IdentityServer that provides links to applications configured with InitiateLoginUri, enabling a seamless single sign-on experience for users.

You can create a client application portal within your IdentityServer host that contains links to client applications that are configured with an `InitiateLoginUri`. The `InitiateLoginUri` URI property is optional, and can be used to [enable identity-provider initiated sign-in](https://openid.net/specs/openid-connect-core-1_0.html#ThirdPartyInitiatedLogin).

Your IdentityServer host can check for clients with this property, and render links to those applications for the currently authenticated user. Doing so gives the user a client application portal that lets them start using each application, where navigating to an application link starts an OpenID Connect challenge with the application.

This creates a curious pattern, where the user follows a link from the portal page in the IdentityServer host to an external application only to have that application immediately redirect back to the IdentityServer host's `/connect/authorize` endpoint. However, if the user has logged in and created a session at the IdentityServer host, they will get a single sign on experience as they navigate to the various applications in the portal.

Tip

The [Entity Framework Core project template](/identityserver/overview/packaging/#templates) comes with an example `~/Portal.cshtml` Razor Page that implements this functionality.

## Third-Party Initiated Login

[Section titled "Third-Party Initiated Login"](#third-party-initiated-login)

The [OpenID Connect Core 1.0 specification](https://openid.net/specs/openid-connect-core-1_0.html#ThirdPartyInitiatedLogin) describes several query string parameters that can be passed from the identity provider to the client application:

* `iss` - a URL (using the https scheme) that identifies the issuer
* `login_hint` - a hint about the end user to be authenticated
* `target_link_uri` - URL that the client application is requested to redirect to after authentication

These query string parameters are not included in the template IdentityServer client application portal, but you can add them to your implementation when desired.

## Implement Identity-Provider Initiated Sign-In

[Section titled "Implement Identity-Provider Initiated Sign-In"](#implement-identity-provider-initiated-sign-in)

To support identity-provider initiated sign-in, client applications must:

1. Be registered in IdentityServer with the `InitiateLoginUri` property set to a URL in the client application.
2. Implement an endpoint at that URL which triggers an OpenID Connect authentication challenge.

### Configuring The Client In IdentityServer

[Section titled "Configuring The Client In IdentityServer"](#configuring-the-client-in-identityserver)

In your IdentityServer client configuration, set the `InitiateLoginUri` property:

```csharp
// IdentityServer Configuration
// ...
new Client
{
    ClientId = "myclient",
    // ... existing config ...
    InitiateLoginUri = "https://example.com/signin-idp"
}
```

### Implementing The Endpoint In The Client Application

[Section titled "Implementing The Endpoint In The Client Application"](#implementing-the-endpoint-in-the-client-application)

In your ASP.NET Core client application, implement the endpoint referenced by `InitiateLoginUri`. This endpoint should trigger the OpenID Connect authentication challenge.

Here's an example ASP.NET Core endpoint that redirects the user to IdentityServer for authorization. When the user is already authenticated, the user is redirected to the application root.

Program.cs

```csharp
app.MapGet("/signin-idp", async (HttpContext http) =>
{
    if (http.User.Identity is { IsAuthenticated: false })
    {
        var returnUrl = "https://example.com/";


        return Results.Challenge(
            new AuthenticationProperties { RedirectUri = returnUrl });
    }


    return Results.Redirect("/");
});
```

For the challenge to work, an OpenID Connect schema must be configured in your client application. When multiple OpenID Connect schemas are registered, you can also use the `Results.Challenge()` overload that allows you to target a specific scheme.
