---
title: Issuing Tokens Based On User Passwords
source_url: https://docs.duendesoftware.com/issuing-tokens-based-on-user-passwords/
source_type: llms-full-txt
content_hash: sha256:c3bdbc03165e34f42ae4d773ec74fd94803d240cdf4a601f70ad40362ce8fd0b
doc_id: issuing-tokens-based-on-user-passwords
---

> A guide to implementing the deprecated password grant type in IdentityServer for legacy applications, covering token requests, client library usage, and custom validation of user credentials.

The `password` grant type is an OAuth 2.0 [protocol flow](https://tools.ietf.org/html/rfc6749#section-4.3) for authenticating end-users at the token endpoint. It is designed for legacy applications, and it is generally recommended to use a browser-based flow instead - but in certain situation it is not feasible to change existing applications.

Note

The `password` grant type is deprecated per [OAuth 2.1](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/).

## Requesting A Token Using Password Grant

[Section titled "Requesting A Token Using Password Grant"](#requesting-a-token-using-password-grant)

First you need to add the `GrantType.Password` to the `AllowedGrantTypes` list of the client you want to use.

Then your client application would provide some means for the end-user to enter their credentials and post them to the token endpoint:

```text
POST /token HTTP/1.1
Host: demo.duendesoftware.com
Content-Type: application/x-www-form-urlencoded


client_id=client&
client_secret=secret&
grant_type=password&
username=bob&
password=password
```

### .NET Client Library

[Section titled ".NET Client Library"](#net-client-library)

On .NET you can use the [Duende IdentityModel](/identitymodel/) client library to [request](/identitymodel/endpoints/token/) tokens using the `password` grant type, e.g.:

Program.cs

```csharp
using Duende.IdentityModel.Client;


var client = new HttpClient();


var response = await client.RequestPasswordTokenAsync(new PasswordTokenRequest
{
    Address = "https://demo.duendesoftware.com/connect/token",


    ClientId = "client",
    ClientSecret = "secret",
    Scope = "api1",


    UserName = "bob",
    Password = "password"
});
```

## Validating The Token Request

[Section titled "Validating The Token Request"](#validating-the-token-request)

Since this flow is not generally recommended, no standard implementation for validating the token request and user credentials is included. To add support for it, you need to implement and [register](/identityserver/reference/di/#additional-services) an implementation of the `IResourceOwnerPasswordValidator` interface:

IResourceOwnerPasswordValidator.cs

```csharp
public interface IResourceOwnerPasswordValidator
{
    /// <summary>
    /// Validates the resource owner password credential
    /// </summary>
    /// <param name="context">The context.</param>
    Task ValidateAsync(ResourceOwnerPasswordValidationContext context);
}
```

The context contains parsed protocol parameters like `UserName` and `Password` and the raw request.

It is the job of the validator to implement the password validation and set the `Result` property on the context accordingly (see the [Grant Validation Result](/identityserver/reference/models/grant-validation-result/) reference).
