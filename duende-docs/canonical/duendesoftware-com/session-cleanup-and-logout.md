---
title: Session Cleanup and Logout
source_url: https://docs.duendesoftware.com/session-cleanup-and-logout/
source_type: llms-full-txt
content_hash: sha256:2589c6637ccd323d28a60ed113af3c79359719478bffdc2187a89eb92e5fd53b
doc_id: session-cleanup-and-logout
---

> Guide to correctly ending a session in IdentityServer, including removing authentication cookies, handling external logins, and revoking client tokens during logout.

Learn how to correctly end a session in ASP.NET Core, including handling cookies and token revocation.

## Removing The Authentication Cookie

[Section titled "Removing The Authentication Cookie"](#removing-the-authentication-cookie)

To remove the authentication cookie, use the ASP.NET Core `SignOutAsync` extension method on the `HttpContext`. You will need to pass the scheme used (which is provided by `IdentityServerConstants.DefaultCookieAuthenticationScheme` unless you have changed it):

LogOut.cshtml.cs

```csharp
await HttpContext.SignOutAsync(
    Duende
        .IdentityServer
        .IdentityServerConstants
        .DefaultCookieAuthenticationScheme
);
```

Or you can use the overload that will sign out of the default authentication scheme:

LogOut.cshtml.cs

```csharp
await HttpContext.SignOutAsync();
```

If you are integrating with ASP.NET Identity, sign out using its `SignInManager` instead:

LogOut.cshtml.cs

```csharp
await _signInManager.SignOutAsync();
```

### Prompting The User To Logout

[Section titled "Prompting The User To Logout"](#prompting-the-user-to-logout)

Typically, you should prompt the user to logout which requires a POST to remove the cookie. Otherwise, an attacker could hotlink to your logout page causing the user to be automatically logged out. This means you will need a page to prompt the user to logout.

If a `logoutId` is passed to the logout page and the returned `LogoutRequest`'s `ShowSignoutPrompt` is `false` then it is safe to skip the prompt. This would occur when the logout page is requested due to a validated client initiated logout via the [end session endpoint](/identityserver/reference/endpoints/end-session/). Your logout page process can continue as if the user submitted the post back to log out, in essence calling `SignOutAsync`.

### External Logins

[Section titled "External Logins"](#external-logins)

If your user has signed in with an external login, then it's likely that they should perform an [external logout](/identityserver/ui/logout/external/) of the external provider as well.

### Revoking Client Tokens At Logout

[Section titled "Revoking Client Tokens At Logout"](#revoking-client-tokens-at-logout)

During a user's session, long-lived tokens (e.g. refresh tokens) might have been created for client applications. If at logout time you would like to have those tokens revoked, then this can be done automatically by setting the `CoordinateLifetimeWithUserSession` property on the [client configuration](/identityserver/reference/models/client/#authentication--session-management), or globally on the [IdentityServer Authentication Options](/identityserver/reference/options/#authentication).
