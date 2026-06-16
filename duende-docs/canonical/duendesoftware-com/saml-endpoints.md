---
title: SAML Endpoints
source_url: https://docs.duendesoftware.com/saml-endpoints/
source_type: llms-full-txt
content_hash: sha256:f3747efdb1fd3b43b361d12043cf0a82c631aab047819c81f45e53a7651e9c3a
doc_id: saml-endpoints
---

> Details of the SAML 2.0 protocol endpoints registered by IdentityServer, including metadata, sign-in, logout, and IdP-initiated SSO.

Added in 8.0 (prerelease)

When SAML 2.0 support is enabled via `AddSaml()`, IdentityServer registers the following SAML protocol endpoints under the `/saml` path prefix.

## Endpoint Summary

[Section titled âEndpoint Summaryâ](#endpoint-summary)

| Endpoint          | Path                    | HTTP Methods | Enabled by Default |
| ----------------- | ----------------------- | ------------ | ------------------ |
| Metadata          | `/saml/metadata`        | GET          | â
 Yes              |
| Sign-in           | `/saml/signin`          | GET, POST    | â
 Yes              |
| Sign-in Callback  | `/saml/signin_callback` | GET, POST    | â
 Yes              |
| IdP-initiated SSO | `/saml/idp-initiated`   | GET, POST    | â No (opt-in)      |
| Logout            | `/saml/logout`          | GET, POST    | â
 Yes              |
| Logout Callback   | `/saml/logout_callback` | GET, POST    | â
 Yes              |

## Metadata Endpoint

[Section titled âMetadata Endpointâ](#metadata-endpoint)

**Path**: `/saml/metadata`\
**Methods**: GET

Returns the IdentityServer SAML 2.0 Identity Provider metadata document (an XML document). Service Providers use this document to discover the IdPâs signing certificates, supported NameID formats, and endpoint locations.

Share this URL with Service Providers during SP configuration so they can automatically import IdP settings.

## Sign-in Endpoint

[Section titled âSign-in Endpointâ](#sign-in-endpoint)

**Path**: `/saml/signin`\
**Methods**: GET, POST

The entry point for SP-initiated SSO. The Service Provider redirects the user to this endpoint with a SAML `AuthnRequest` message (encoded using the HTTP-Redirect or HTTP-POST binding).

IdentityServer validates the `AuthnRequest`, authenticates the user (redirecting to the login page if needed), and then continues to the Sign-in Callback endpoint.

## Sign-in Callback Endpoint

[Section titled âSign-in Callback Endpointâ](#sign-in-callback-endpoint)

**Path**: `/saml/signin_callback`\
**Methods**: GET, POST

Processes the outcome of user authentication during SP-initiated SSO. After the user authenticates, this endpoint builds the SAML `Response` (containing the `Assertion`) and delivers it to the Service Providerâs Assertion Consumer Service (ACS) URL using the configured binding.

## IdP-Initiated SSO Endpoint

[Section titled âIdP-Initiated SSO Endpointâ](#idp-initiated-sso-endpoint)

**Path**: `/saml/idp-initiated`\
**Methods**: GET, POST\
**Enabled by default**: No â requires explicit opt-in

Supports IdP-initiated SSO flows, where the IdP starts the authentication without receiving an `AuthnRequest` from the SP. The SP must have `AllowIdpInitiated = true` set in its `SamlServiceProvider` configuration.

To enable this endpoint:

Program.cs

```csharp
builder.Services.AddIdentityServer(options =>
{
    options.Endpoints.EnableSamlIdpInitiatedEndpoint = true;
});
```

Caution

IdP-initiated SSO carries additional security risks because there is no `AuthnRequest` to validate. Enable it only for Service Providers that explicitly require it.

## Logout Endpoint

[Section titled âLogout Endpointâ](#logout-endpoint)

**Path**: `/saml/logout`\
**Methods**: GET, POST

Handles incoming SAML Single Logout (SLO) requests from Service Providers. The SP sends a SAML `LogoutRequest` message to this endpoint. IdentityServer processes the request, terminates the userâs IdentityServer session, and sends front-channel logout notifications to other registered SPs.

## Logout Callback Endpoint

[Section titled âLogout Callback Endpointâ](#logout-callback-endpoint)

**Path**: `/saml/logout_callback`\
**Methods**: GET, POST

Processes SAML `LogoutResponse` messages returned by Service Providers after they have processed a logout notification from IdentityServer. This endpoint completes the SAML SLO round-trip.

## Customizing Endpoint Paths

[Section titled âCustomizing Endpoint Pathsâ](#customizing-endpoint-paths)

Endpoint paths can be customized via `SamlOptions.UserInteraction`:

Program.cs

```csharp
builder.Services.AddIdentityServer(options =>
{
    options.Saml.UserInteraction.Route = "/saml";
    options.Saml.UserInteraction.Metadata = "/metadata";
    options.Saml.UserInteraction.SignInPath = "/signin";
    options.Saml.UserInteraction.SignInCallbackPath = "/signin_callback";
    options.Saml.UserInteraction.IdpInitiatedPath = "/idp-initiated";
    options.Saml.UserInteraction.SingleLogoutPath = "/logout";
    options.Saml.UserInteraction.SingleLogoutCallbackPath = "/logout_callback";
});
```

See [SAML Configuration](/identityserver/saml/configuration/) for full path option documentation.
