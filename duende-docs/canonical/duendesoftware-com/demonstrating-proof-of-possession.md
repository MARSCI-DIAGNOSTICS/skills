---
title: Demonstrating Proof-of-Possession (DPoP)
source_url: https://docs.duendesoftware.com/demonstrating-proof-of-possession/
source_type: llms-full-txt
content_hash: sha256:b7bb2c438793bd3b6f859da59a75ffe755ed4456c3edc904130b39e28d1770c8
doc_id: demonstrating-proof-of-possession
---

> Demonstrating Proof-of-Possession is a security mechanism that binds access tokens to specific cryptographic keys to prevent token theft and misuse.

[DPoP](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-dpop) specifies how to bind an asymmetric key stored within a JSON Web Key (JWK) to an access token. This will make the access token bound to the key such that if the access token were to leak, it cannot be used without also having access to the private key of the corresponding JWK.

The Duende.AccessTokenManagement library supports DPoP.

## DPoP Key

[Section titled "DPoP Key"](#dpop-key)

The main piece that your hosting application needs to concern itself with is how to get (and manage) the DPoP key. This key (and signing algorithm) will be either an "RS", "PS", or "ES" style key, and needs to be in the form of a JSON Web Key (or JWK). Consult the specification for more details.

The creation and management of this DPoP key is up to the policy of the client. For example is can be dynamically created when the client starts up, and can be periodically rotated. The main constraint is that it must be stored for as long as the client uses any access tokens (and possibly refresh tokens) that they are bound to, which this library will manage for you.

Creating a JWK in .NET is simple:

Program.cs

```csharp
using System.Security.Cryptography;
using System.Text.Json;
using Microsoft.IdentityModel.Tokens;


var rsaKey = new RsaSecurityKey(RSA.Create(2048));
var jwkKey = JsonWebKeyConverter.ConvertFromSecurityKey(rsaKey);
jwkKey.Alg = "PS256";
var jwk = JsonSerializer.Serialize(jwkKey);


Console.WriteLine(jwk);
```

## Key Configuration

[Section titled "Key Configuration"](#key-configuration)

Once you have a JWK you wish to use, then it must be configured or made available to this library. That can be done in one of two ways:

* Configure the key at startup by setting the `DPoPJsonWebKey` property on either the `ClientCredentialsTokenManagementOptions` or `UserTokenManagementOptions` (depending on which of the two styles you are using from this library).
* Implement the `IDPoPKeyStore` interface to produce the key at runtime.

Here's a sample configuring the key in an application using `AddOpenIdConnectAccessTokenManagement` in the startup code:

Program.cs

```csharp
services.AddOpenIdConnectAccessTokenManagement(options =>
{
    options.DPoPJsonWebKey = jwk;
});
```

Similarly, for an application using `AddClientCredentialsTokenManagement`, it would look like this:

Program.cs

```csharp
services.AddClientCredentialsTokenManagement()
   .AddClient("client_name", options =>
   {
       options.DPoPJsonWebKey = jwk;
   });
```

## Proof Tokens At The Token Server's Token Endpoint

[Section titled "Proof Tokens At The Token Server's Token Endpoint"](#proof-tokens-at-the-token-servers-token-endpoint)

Once the key has been configured for the client, then the library will use it to produce a DPoP proof token when calling the token server (including token renewals if relevant). There is nothing explicit needed on behalf of the developer using this library.

### `dpop_jkt` At The Token Server's Authorize Endpoint

[Section titled "dpop\_jkt At The Token Server's Authorize Endpoint"](#dpop_jkt-at-the-token-servers-authorize-endpoint)

When using DPoP and `AddOpenIdConnectAccessTokenManagement`, this library will also automatically include the `dpop_jkt` parameter to the authorize endpoint.

## Proof Tokens At The API

[Section titled "Proof Tokens At The API"](#proof-tokens-at-the-api)

Once the library has gotten a DPoP bound access token for the client, then if your application is using any of the `HttpClient` client factory helpers (e.g. `AddClientCredentialsHttpClient` or `AddUserAccessTokenHttpClient`) then those outbound HTTP requests will automatically include a DPoP proof token for the associated DPoP access token.

## Considerations

[Section titled "Considerations"](#considerations)

A point to keep in mind when using DPoP and `AddOpenIdConnectAccessTokenManagement` is that the DPoP proof key is created per user session. This proof key must be store somewhere, and the `AuthenticationProperties` used by both the OIDC and cookie handlers is what is used to store this key. This implies that the OIDC `state` parameter will increase in size, as well the resultant cookie that represents the user's session. The storage for each of these can be customized with the properties on the options `StateDataFormat` and `SessionStore` respectively.
