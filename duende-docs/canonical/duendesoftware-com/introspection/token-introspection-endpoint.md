---
title: Token Introspection Endpoint
source_url: https://docs.duendesoftware.com/introspection/token-introspection-endpoint/
source_type: llms-full-txt
content_hash: sha256:24973d0955d50254d5026ad9e974be9b7e944dc718fde393811a9bbf4c3202ce
category: introspection
doc_id: introspection/token-introspection-endpoint
---

> Learn how to use the OAuth 2.0 token introspection endpoint to validate and inspect access tokens using HttpClient extensions.

The client library for [OAuth 2.0 token introspection (RFC 7662)](https://tools.ietf.org/html/rfc7662) is provided by the `IntrospectionClient` class, and as an extension method for `HttpClient`.

## Token Introspection Request

[Section titled "Token Introspection Request"](#token-introspection-request)

The following code sends a reference token to an introspection endpoint:

* Using IntrospectionClient

  ```csharp
  var clientOptions = new IntrospectionClientOptions
  {
    Address = Endpoint,
    ClientId = "client",
    ClientSecret = "secret",
    ResponseFormat = ResponseFormat.Json
  };


  var httpClient = new HttpClient();


  var introspectionClient = new IntrospectionClient(httpClient, clientOptions);
  var introspectionResponse = await introspectionClient.Introspect("token");
  ```

* Using HttpClient extension

  ```csharp
  var client = new HttpClient();
  var introspectionResponse = await client.IntrospectTokenAsync(new TokenIntrospectionRequest
  {
    Address = Endpoint,
    Token = "token",
    ResponseFormat = ResponseFormat.Json
  });
  ```

## Token Introspection Response

[Section titled "Token Introspection Response"](#token-introspection-response)

The response of a token introspection request is an object of type `TokenIntrospectionResponse`. Before using the response, you should always check the `IsError` property to make sure the request was successful:

```csharp
if (introspectionResponse.IsError) throw new Exception(introspectionResponse.Error);


var isActive = introspectionResponse.IsActive;
var claims = introspectionResponse.Claims;
```

The `TokenIntrospectionResponse` class exposes the raw response through its `Raw` property, and to the parsed JSON document through its `Json` property. In addition, it provides access to the following standard response parameters:

| Property     | Value                                                                                                                                                                               |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Scopes`     | The list of scopes associated to the token or an empty array if no `scope` claim is present.                                                                                        |
| `ClientId`   | The client identifier for the OAuth 2.0 client that requested the token or `null` if the `client_id` claim is missing.                                                              |
| `UserName`   | The human-readable identifier for the resource owner who authorized the token or `null` if the `username` claim is missing.                                                         |
| `TokenType`  | The type of the token as defined in [section 5.1 of OAuth 2.0 (RFC6749)](https://datatracker.ietf.org/doc/html/rfc6749#section-5.1) or `null` if the `token_type` claim is missing. |
| `Expiration` | The expiration time of the token or `null` if the `exp` claim is missing.                                                                                                           |
| `IssuedAt`   | The issuance time of the token or `null` if the `iat` claim is missing.                                                                                                             |
| `NotBefore`  | The validity start time of the token or `null` if the `nbf` claim is missing.                                                                                                       |
| `Subject`    | The subject of the token or `null` if the `sub` claim is missing.                                                                                                                   |
| `Audiences`  | The service-specific list of string identifiers representing the intended audience for the token or an empty array if no `aud` claim is present.                                    |
| `Issuer`     | The string representing the issuer of the token or `null` if the `iss` claim is missing.                                                                                            |
| `JwtId`      | The string identifier for the token or `null` if the `jti` claim is missing.                                                                                                        |

## JWT Response Format v7.1

[Section titled "JWT Response Format "v7.1](#jwt-response-format)

Introspection requests can optionally pass a parameter to indicate that a signed JWT rather than JSON payload is desired. Such a JWT response is most often useful for non-repudiation. For example, an API might rely on the claims from introspection to produce digitally signed documents or issue certificates, with the Authorization Server assuming legal liability for the introspected data. A JWT introspection response can be stored and its signature independently verified as part of an audit.

### Requesting JWT Response Format

[Section titled "Requesting JWT Response Format"](#requesting-jwt-response-format)

To request the JWT response format, set the `ResponseFormat` option to `ResponseFormat.Jwt`.

```csharp
var client = new HttpClient();
var introspectionResponse = await client.IntrospectTokenAsync(
    new TokenIntrospectionRequest
    {
        Address = Endpoint,
        Token = "token",
        ResponseFormat = ResponseFormat.Jwt
    });
```

### Validating JWT Signature

[Section titled "Validating JWT Signature"](#validating-jwt-signature)

By default, when the introspection endpoint returns a JWT, the system performs only a basic format check on the response. Full cryptographic validation of the JWT's signature and claims is not performed.

This approach is generally appropriate because the introspection request is made over a direct back-channel connection from the application to the introspection endpoint. This connection is secured by TLS, which guarantees the authenticity and integrity of the response in transit. The introspected claims can safely be used immediately without an additional cryptographic validation.

An extensibility point is available to provide your own implementation of `ITokenIntrospectionJwtResponseValidator`.

ITokenIntrospectionJwtResponseValidator.cs

```csharp
public interface ITokenIntrospectionJwtResponseValidator
{
    void Validate(string rawJwtResponse);
}
```

A custom validator can be applied using the `TokenIntrospectionRequest.JwtResponseValidator` property or using `IntrospectionClientOptions`:

```csharp
var client = new HttpClient();
var introspectionResponse = await client.IntrospectTokenAsync(
    new TokenIntrospectionRequest
    {
        Address = Endpoint,
        Token = "token",
        ResponseFormat = ResponseFormat.Jwt,
        JwtResponseValidator = new CustomIntrospectionJwtResponseValidator()
    });
```
