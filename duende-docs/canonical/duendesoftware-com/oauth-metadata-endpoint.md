---
title: OAuth Metadata Endpoint
source_url: https://docs.duendesoftware.com/oauth-metadata-endpoint/
source_type: llms-full-txt
content_hash: sha256:0b9d33f0aaaacaf3a4c0ae7f4b7b083c6f87c1b5392db119604b79b61da802df
doc_id: oauth-metadata-endpoint
---

> Learn about the OAuth metadata endpoint that provides information about your IdentityServer configuration, including issuer name, key material, and supported scopes.

The [OAuth Metadata Endpoint](https://www.rfc-editor.org/rfc/rfc8414.html) is a standardized way to retrieve metadata about your IdentityServer.

The discovery endpoint is available via `/.well-known/oauth-authorization-server` relative to the base address, e.g.:

```text
https://demo.duendesoftware.com/.well-known/oauth-authorization-server
```

## Issuer Name and Path Base

[Section titled "Issuer Name and Path Base"](#issuer-name-and-path-base)

When hosting IdentityServer in an application that uses [ASP.NET Core's `PathBaseMiddleware`](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.builder.extensions.usepathbasemiddleware), the base path will be included in the issuer name and discovery document URLs.

Refer the [Discovery Endpoint](/identityserver/reference/endpoints/discovery/#issuer-name-and-path-base) for more information.
