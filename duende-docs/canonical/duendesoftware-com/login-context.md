---
title: Login Context
source_url: https://docs.duendesoftware.com/login-context/
source_type: llms-full-txt
content_hash: sha256:b4e55fac92062fc68f0ce890caf975b94ff73cc4706aee550d65e9236108e5e7
doc_id: login-context
---

> Guide to accessing and using authorization request parameters from the returnUrl to customize the login workflow in IdentityServer.

The `returnUrl` query parameter passed to the login page refers to the URL the prior request came from. This URL typically refers to the IdentityServer authorization endpoint and contains the original request parameters sent from the client. These parameters might contain information your login page needs to customize its workflow. Some examples would be for branding, dynamic page customization (e.g. which external login providers to use), or controlling what credentials the client application expects (e.g. perhaps MFA is required).

## Authorization Request Context

[Section titled "Authorization Request Context"](#authorization-request-context)

In order to read the original authorize request parameter values, you can use the [interaction service](/identityserver/reference/services/interaction-service/#iidentityserverinteractionservice-apis). It provides a `GetAuthorizationContextAsync` API that will extract that information from the `returnUrl` and return an [AuthorizationRequest](/identityserver/reference/services/interaction-service/#authorizationrequest) object which contains these values.

Note

It is unnecessary (and discouraged) for your login page logic to parse the `returnUrl` itself.
