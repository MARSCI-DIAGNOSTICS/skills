---
title: OIDC Client Manual Mode
source_url: https://docs.duendesoftware.com/identitymodel-oidcclient/oidc-client-manual-mode/
source_type: llms-full-txt
content_hash: sha256:ce4f9975cc013537b34ef998329db83704c97ea44a21fd1ed687cf3f6e398a22
category: identitymodel-oidcclient
doc_id: identitymodel-oidcclient/oidc-client-manual-mode
---

> Guide for implementing manual mode in OidcClient to handle browser interactions and token processing

OpenID Connect is a protocol that allows you to authenticate users using a browser and involves browser-based interactions. When using this library you can choose between two modes: [automatic](/identitymodel-oidcclient/automatic/) and manual.

We recommend using automatic mode when possible, but sometimes you need to use manual mode when you want to handle browser interactions yourself.

With manual mode, `OidcClient` is still useful, as it helps with creating the necessary start URL and state parameters needed to complete an OIDC flow. You'll need to handle all browser interactions yourself with custom code. This is beneficial for scenarios where you want to customize the browser experience or when you want to integrate with other platform-specific browser libraries.

```csharp
var options = new OidcClientOptions
{
    Authority = "https://demo.duendesoftware.com",
    ClientId = "native",
    RedirectUri = redirectUri,
    Scope = "openid profile api"
};


var client = new OidcClient(options);


// generate start URL, state, nonce, code challenge
var state = await client.PrepareLoginAsync();
```

When the browser work is done, `OidcClient` can take over to process the response, get the access/refresh tokens, contact userinfo endpoint etc.:

```csharp
var result = await client.ProcessResponseAsync(data, state);
```

When using this manual mode, and processing the response, the `ProcessResponseAsync` method will return a [`LoginResult`](https://github.com/DuendeSoftware/foss/blob/19370c6d4820a684d41d1d40b8192ee8b873b8f0/identity-model-oidc-client/src/IdentityModel.OidcClient/LoginResult.cs) which will contain a `ClaimsPrincipal` with the user's claims along with the `IdentityToken` and `AccessToken`.
