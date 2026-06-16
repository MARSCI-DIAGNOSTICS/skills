---
title: Basics
source_url: https://docs.duendesoftware.com/identityserver/samples/basics/
source_type: llms-full-txt
content_hash: sha256:cbfc7e5741c0891eddfb418bda4e9a62c91a4d275c331c1290a63739a912067b
doc_id: identityserver/samples/basics
---

> A collection of common IdentityServer scenarios including client credentials, JWT-based authentication, reference tokens, MVC clients, token management, and back-channel logout notifications.

This section contains a collection of common scenarios when building a Duende IdentityServer solution.

### Client Credentials

[Section titled "Client Credentials"](#client-credentials)

This sample shows how to use the `client_credentials` grant type. This is typically used for machine to machine communication.

Key takeaways:

* how to request a token using client credentials
* how to use a shared secret
* how to use an access token

[Client Credentials Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Basics/ClientCredentials)GitHub Repository for the Client Credentials Sample

### JWT-based Client Authentication

[Section titled "JWT-based Client Authentication"](#jwt-based-client-authentication)

This sample shows how to use the `client_credentials` grant type with JWT-based client authentication. This authentication method is more recommended than shared secrets.

Key takeaways:

* create a JWT for client authentication
* use a JWT as a client secret replacement
* configure IdentityServer to accept a JWT as a client secret

[JWT-based Client Authentication Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Basics/ClientCredentials)GitHub Repository for the JWT-based Client Authentication Sample

### Introspection & Reference Tokens

[Section titled "Introspection & Reference Tokens"](#introspection--reference-tokens)

This sample shows how to use the reference tokens instead of JWTs.

Things of interest:

* the client registration uses `AccessTokenType` of value `Reference`
* the client requests `scope2` - this scope is part of an API resource.
  * API resources allow defining API secrets, which can then be used to access the introspection endpoint
* The API supports both JWT and reference tokens, this is achieved by forwarding the token to the right handler at runtime

Key takeaways:

* configuring a client to receive reference tokens
* set up an API resource with an API secret
* configure an API to accept and validate reference tokens

[Introspection & Reference Tokens Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Basics/Introspection)GitHub Repository for the Introspection & Reference Tokens Sample

### MVC Client

[Section titled "MVC Client"](#mvc-client)

This sample shows how to use the `authorization_code` grant type. This is typically used for interactive applications like web applications.

Key takeaways:

* configure an MVC client to use IdentityServer
* access tokens in ASP.NET Core's authentication session
* call an API
* manually refresh tokens

[MVC Client Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Basics/MvcBasic)GitHub Repository for the MVC Client Sample

### MVC Client with automatic Access Token Management

[Section titled "MVC Client with automatic Access Token Management"](#mvc-client-with-automatic-access-token-management)

This sample shows how to use [Duende.AccessTokenManagement](/accesstokenmanagement) to automatically manage access tokens.

The sample uses a special client in the sample IdentityServer with a short token lifetime (75 seconds). When repeating the API call, make sure you inspect the returned `iat` and `exp` claims to observer how the token is slides.

You can also turn on debug tracing to get more insights in the token management library.

Key takeaways:

* use [Duende.AccessTokenManagement](/accesstokenmanagement) to automate refreshing tokens

[MVC Client with automatic Access Token Management Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Basics/MvcTokenManagement)GitHub Repository for the MVC Client with automatic Access Token Management Sample

### MVC Client with JAR and JWT-based Authentication

[Section titled "MVC Client with JAR and JWT-based Authentication"](#mvc-client-with-jar-and-jwt-based-authentication)

This sample shows how to use signed authorize requests, and JWT-based authentication for clients in MVC. It also shows how to integrate that technique with automatic token management.

Key takeaways:

* use the ASP.NET Core extensibility points to add signed authorize requests and JWT-based authentication
* use JWT-based authentication for automatic token management
* configure a client in IdentityServer to share key material for both front- and back-channel

[MVC Client with JAR and JWT-based Authentication Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Basics/MvcJarJwt)GitHub Repository for the MVC Client with JAR and JWT-based Authentication Sample

### MVC Client with Back-Channel Logout Notifications

[Section titled "MVC Client with Back-Channel Logout Notifications"](#mvc-client-with-back-channel-logout-notifications)

This sample shows how to use back-channel logout notifications.

Key takeaways:

* how to implement the back-channel notification endpoint
* how to leverage events on the cookie handler to invalidate the user session

[MVC Client with Back-Channel Logout Notifications Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Basics/MvcBackChannelLogout)GitHub Repository for the MVC Client with Back-Channel Logout Notifications Sample

### MVC Client with Pushed Authorization Requests

[Section titled "MVC Client with Pushed Authorization Requests"](#mvc-client-with-pushed-authorization-requests)

This sample shows how to use [Pushed Authorization Requests](/identityserver/tokens/par/) (PAR).

Key takeaways:

* how to enable PAR in the client configuration
* how to add support for PAR to the ASP.NET OIDC authentication handler. The main idea is to use the events in the handler to push the parameters before redirecting to the authorize endpoint, and then replace the parameters that would normally be sent in that redirect with the resulting request uri. See the `ParOidcEvents.cs` file for more details.

Note

This sample is only relevant if you're using .NET 8 or lower.

[.NET 9 has support for PAR built-in](https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-9.0?view=aspnetcore-9.0#openidconnecthandler-adds-support-for-pushed-authorization-requests-par), and the ASP.NET Core OIDC authentication handler will automatically use PAR when the authority supports it, based on the discovery metadata.

[MVC Client with Pushed Authorization Requests Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Basics/MvcPar)GitHub Repository for the MVC Client with Pushed Authorization Requests Sample
