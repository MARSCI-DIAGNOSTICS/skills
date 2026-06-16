---
title: Glossary
source_url: https://docs.duendesoftware.com/general/glossary/
source_type: llms-full-txt
content_hash: sha256:98ddbbcd8006f3c5056c9a1bd9369f85994fd740b3bd7cdd31ee03e2efa0cffc
doc_id: glossary
---

> A comprehensive glossary of security and identity management terms, including features and concepts used in Duende IdentityServer

The glossary below provides definitions and explanations of commonly used terms and features within the security and identity management domain. Explore each term to gain a deeper understanding of its functionality and relevance.

## Client

[Section titled "Client"](#client)

A client is a piece of software that requests tokens from your IdentityServer - either for authenticating a user ( requesting an identity token) or for accessing a resource (requesting an access token). A client must be first registered with your IdentityServer before it can request tokens and is identified by a unique client ID.

There are many different client types, e.g. web applications, native mobile or desktop applications, SPAs, server processes, etc.

[Documentation ](/identityserver/fundamentals/clients)Learn more about clients

## Automatic Key Management

[Section titled "Automatic Key Management"](#automatic-key-management)

**License: Business**

The automatic key management feature creates and manages key material for signing tokens and follows best practices for handling this key material, including storage and rotation.

[More Details ](https://duendesoftware.com/blog/20201028-key-management)Automatic Key Management post

[Documentation ](/identityserver/fundamentals/key-management/#automatic-key-management)Learn more about key rotation

## Server-side Session Management

[Section titled "Server-side Session Management"](#server-side-session-management)

**License: Business**

The server-side session management feature extends the ASP.NET Core cookie authentication handler to maintain a user's authentication session state in a server-side store, rather than putting it all into a self-contained cookie. Using server-side sessions enables more architectural features in your IdentityServer, such as:

* query and manage active user sessions (e.g. from an administrative app).
* detect session expiration and perform cleanup, both in IdentityServer and in client apps.
* centralize and monitor session activity in order to achieve a system-wide inactivity timeout.

[More Details ](https://duendesoftware.com/blog/20220406-session-management)Server-side Session Management post

[Documentation ](/identityserver/ui/server-side-sessions/)Learn more about Server-side Session Management

## BFF Security Framework

[Section titled "BFF Security Framework"](#bff-security-framework)

The Duende Backend For Frontend (BFF) security framework packages up guidance and the necessary components to secure browser-based frontends (e.g. SPAs or Blazor WASM applications) with ASP.NET Core backends.

[More Details ](https://duendesoftware.com/blog/20210326-bff)BFF Security Framework post

[Documentation ](/bff/)Learn more about BFF

## Dynamic Client Registration

[Section titled "Dynamic Client Registration"](#dynamic-client-registration)

**License: Business**

Implementation of [RFC 8707](https://tools.ietf.org/html/rfc8707). Provides a standards-based endpoint to register clients and their configuration.

[Documentation ](/identityserver/configuration)Learn more about Dynamic Client Registration

## Pushed Authorization Requests

[Section titled "Pushed Authorization Requests"](#pushed-authorization-requests)

**License: Business**

Implementation of [RFC 9126](https://www.rfc-editor.org/rfc/rfc9126.html). Provides a more secure way to start a browser-based token/authentication request.

[Documentation ](/identityserver/tokens/par)Learn more about Pushed Authorization Requests

## Dynamic Authentication Providers

[Section titled "Dynamic Authentication Providers"](#dynamic-authentication-providers)

**License: Enterprise**

The dynamic configuration feature allows dynamic loading of configuration for OpenID Connect providers from a store. This is designed to address the performance concern and allowing changes to the configuration to a running server.

[More Details ](https://duendesoftware.com/blog/20210517-dynamic-providers)Dynamic Authentication Providers post

[Documentation ](/identityserver/fundamentals/key-management/#automatic-key-management)Learn more about Dynamic Authentication Providers

## Resource Isolation

[Section titled "Resource Isolation"](#resource-isolation)

**License: Enterprise**

The resource isolation feature allows a client to request access tokens for an individual resource server. This allows API-specific features such as access token encryption and isolation of APIs that are not in the same trust boundary.

[More Details ](https://duendesoftware.com/blog/20201230-resource-isolation)Resource Isolation post

[Documentation ](/identityserver/fundamentals/resources/isolation/)Learn more about Resource Isolation

## Client-Initiated Backchannel Authentication (CIBA)

[Section titled "Client-Initiated Backchannel Authentication (CIBA)"](#client-initiated-backchannel-authentication-ciba)

**License: Enterprise**

Duende IdentityServer supports the Client-Initiated Backchannel Authentication Flow (also known as CIBA). This allows a user to log in with a higher security device (e.g. their mobile phone) than the device on which they are using an application (e.g. a public kiosk). CIBA is one of the requirements to support the Financal-grade API compliance.

[More Details ](https://duendesoftware.com/blog/20220107-ciba)Client-Initiated Backchannel Authentication post

[Documentation ](/identityserver/ui/ciba/)Learn more about CIBA

## Proof-of-Possession At The Application Layer / DPoP

[Section titled "Proof-of-Possession At The Application Layer / DPoP"](#proof-of-possession-at-the-application-layer--dpop)

**License: Enterprise**

A mechanism for sender-constraining OAuth 2.0 tokens via a proof-of-possession mechanism on the application level. This mechanism allows for the detection of replay attacks with access and refresh tokens.

[Documentation ](/identityserver/tokens/pop)Learn more about Proof-of-Possession

## Single Deployment

[Section titled "Single Deployment"](#single-deployment)

A single deployment acts as a single OpenID Connect / OAuth authority hosted at a single URL. It can consist of multiple physical or virtual nodes for load-balancing or fail-over purposes.

## Multiple Deployments

[Section titled "Multiple Deployments"](#multiple-deployments)

Can be either completely independent single deployments, or a single deployment that acts as multiple authorities.

## Multiple Authorities

[Section titled "Multiple Authorities"](#multiple-authorities)

A single logical deployment that acts as multiple logical token services on multiple URLs or host names (e.g. for branding, isolation or multi-tenancy reasons).

## Standard Developer Support

[Section titled "Standard Developer Support"](#standard-developer-support)

Online [developer community forum](https://github.com/DuendeSoftware/community/discussions) for Duende Software product issues and bugs.

[Duende Developer Community ](https://github.com/DuendeSoftware/community/discussions)Learn more about the Duende Developer Community

## Priority Developer Support

[Section titled "Priority Developer Support"](#priority-developer-support)

**License: Enterprise**

Helpdesk system with guaranteed response time for Duende Software product issues and bugs.

[More Details ](https://duendesoftware.com/license/PrioritySupportLicense.pdf)Download the Priority Support License PDF
