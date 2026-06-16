---
title: Session Expiration
source_url: https://docs.duendesoftware.com/identityserver/ui/server-side-sessions/session-expiration/
source_type: llms-full-txt
content_hash: sha256:20e25bfbe664c69592efb484ee65ff950e9b924bdb6f8df4780f7b43bd123318
doc_id: identityserver/ui/server-side-sessions/session-expiration
---

> Documentation on IdentityServer's session expiration feature, which automatically cleans up expired server-side sessions and can notify client applications via back-channel logout.

If the user session ends when the session cookie expires without explicitly triggering logout, there is most likely a need to clean up the server-side session data. To remove these expired records, there is an automatic cleanup mechanism that periodically scans for expired sessions. When these records are cleaned up, you can optionally notify the client that the session has ended via back-channel logout.

## Expiration Configuration

[Section titled "Expiration Configuration"](#expiration-configuration)

The expiration configuration features can be configured with the [server-side session options](/identityserver/reference/options/#server-side-sessions). It is enabled by default, but if you wish to disable it or change how often IdentityServer will check for expired sessions, you can.

For example, to change the interval:

Program.cs

```csharp
builder.Services.AddIdentityServer(options => {
    options.ServerSideSessions.RemoveExpiredSessionsFrequency = TimeSpan.FromSeconds(60);
})
    .AddServerSideSessions();
```

To disable:

Program.cs

```csharp
builder.Services.AddIdentityServer(options => {
    options.ServerSideSessions.RemoveExpiredSessions = false;
})
    .AddServerSideSessions();
```

### Back-channel Logout

[Section titled "Back-channel Logout"](#back-channel-logout)

When the session cleanup job removes expired records, it will by default also trigger [back-channel logout notifications](/identityserver/ui/logout/notification/#back-channel-server-side-clients) to client applications participating in the session. You can use this mechanism to create an [inactivity timeout](/identityserver/ui/server-side-sessions/inactivity-timeout/) that applies across all your client applications.

The `ServerSideSessions.ExpiredSessionsTriggerBackchannelLogout` flag enables this behavior, and it is on by default.

### Configuring Server-Side Session Lifetime

[Section titled "Configuring Server-Side Session Lifetime"](#configuring-server-side-session-lifetime)

If you need to change the default lifetime of server-side sessions, there are two ways to do so, depending on whether you're using ASP.NET Core Identity or not.

* Default behavior

  The default session lifetime of 10 hours is inherited from the [`IdentityServerOptions.Authentication.CookieLifetime`](/identityserver/reference/options/#authentication) property. When configuring IdentityServer, you can override this default:

  Program.cs

  ```csharp
  builder.Services.AddIdentityServer(options => {
    options.Authentication.CookieLifetime = TimeSpan.FromMinutes(42);
  });
  ```

* ASP.NET Core Identity

  When using ASP.NET Core Identity, the server-side session follows the lifetime of ASP.NET Core Identity's session cookie, which is 14 days by default. To change the lifetime, you need to reconfigure the application cookie using the `ConfigureApplicationCookie` extension method:

  Program.cs

  ```csharp
  builder.Services.ConfigureApplicationCookie(options => {
    options.ExpireTimeSpan = TimeSpan.FromMinutes(42);
  });
  ```
