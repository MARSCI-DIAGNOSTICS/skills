---
title: Revocation Endpoint
source_url: https://docs.duendesoftware.com/revocation-endpoint/
source_type: llms-full-txt
content_hash: sha256:b4dbc0c1ab11d9df4be8443ae32a0f20f6e3a4f4bf8124d9c72ccc2414bccc7a
doc_id: revocation-endpoint
---

> Learn about the revocation endpoint that allows invalidating access and refresh tokens according to RFC 7009 specification.

This endpoint allows revoking access tokens (reference tokens only) and refresh token. It implements the token revocation specification [(RFC 7009)](https://tools.ietf.org/html/rfc7009).

* **`token`**

  the token to revoke (required)

* **`token_type_hint`**

  either `access_token` or `refresh_token` (optional)

```text
POST /connect/revocation HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW


token=...&token_type_hint=refresh_token
```

## .NET Client Library

[Section titled ".NET Client Library"](#net-client-library)

You can use the [Duende IdentityModel](/identitymodel/) client library to programmatically interact with the protocol endpoint from .NET code.

```csharp
using Duende.IdentityModel.Client;


var client = new HttpClient();


var result = await client.RevokeTokenAsync(new TokenRevocationRequest
{
    Address = "https://demo.duendesoftware.com/connect/revocation",
    ClientId = "client",
    ClientSecret = "secret",


    Token = token
});
```
