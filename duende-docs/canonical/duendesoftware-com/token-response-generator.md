---
title: Token Response Generator
source_url: https://docs.duendesoftware.com/token-response-generator/
source_type: llms-full-txt
content_hash: sha256:d98b474ad84f7425e9b95ca43a32a5318638f3765218e035fee9f478fa4d4e11
doc_id: token-response-generator
---

> Documentation for the ITokenResponseGenerator interface and its implementation, which generates responses to valid token endpoint requests with customization options for different token flows.

## Duende.IdentityServer.ResponseHandling.ITokenResponseGenerator

[Section titled "Duende.IdentityServer.ResponseHandling.ITokenResponseGenerator"](#duendeidentityserverresponsehandlingitokenresponsegenerator)

The `ITokenResponseGenerator` interface is the contract for the service that generates responses to valid requests to the token endpoint. A response in this context refers to an object model that describes the content that will be serialized and transmitted in the HTTP response.

The default implementation is the `TokenResponseGenerator` class. You can customize the behavior of the token endpoint by providing your own implementation of the `ITokenResponseGenerator` to the ASP.NET Core service provider.

To create a customized implementation of `ITokenResponseGenerator`, we recommend that you create a class that derives from the default implementation. Your custom implementation should override the appropriate virtual methods of the default implementation and add your custom behavior to those overrides, possibly calling the base methods first and then manipulating their results.

## ITokenResponseGenerator

[Section titled "ITokenResponseGenerator"](#itokenresponsegenerator)

The `ITokenResponseGenerator` contains a single method to process validated token requests and return token responses.

* **`ProcessInteractionAsync`**

  Returns the `TokenResponse` based on the `ValidatedTokenRequest`.

## TokenResponseGenerator

[Section titled "TokenResponseGenerator"](#tokenresponsegenerator)

The default implementation of the `ITokenResponseGenerator` contains virtual methods that can be overridden to customize particular behavior for particular token requests.

* **`ProcessAsync`**

  Returns the `TokenResponse` for any `TokenRequestValidationResult`.

* **`ProcessClientCredentialsRequestAsync`**

  Returns the `TokenResponse` for a `TokenRequestValidationResult` from the client credentials flow.

* **`ProcessPasswordRequestAsync`**

  Returns the `TokenResponse` for a `TokenRequestValidationResult` from the resource owner password flow.

* **`ProcessAuthorizationCodeRequestAsync`**

  Returns the `TokenResponse` for a `TokenRequestValidationResult` from the authorization code flow.

* **`ProcessRefreshTokenRequestAsync`**

  Returns the `TokenResponse` for a `TokenRequestValidationResult` from the refresh token flow.

* **`ProcessDeviceCodeRequestAsync`**

  Returns the `TokenResponse` for a `TokenRequestValidationResult` from the device code flow.

* **`ProcessCibaRequestAsync`**

  Returns the `TokenResponse` for a `TokenRequestValidationResult` from the CIBA flow.

* **`ProcessExtensionGrantRequestAsync`**

  Returns the `TokenResponse` for a `TokenRequestValidationResult` from an extension grant.

* **`CreateAccessTokenAsync`**

  Creates an access token and optionally a refresh token.

* **`CreateIdTokenFromRefreshTokenRequestAsync`**

  Creates an ID token in a refresh token request.

## TokenResponse

[Section titled "TokenResponse"](#tokenresponse)

The `TokenResponse` class represents the data that will be included in the body of the response returned from the token endpoint. It contains properties for the various tokens that can be returned, the scope and expiration of the access token, and a mechanism for adding custom properties to the result. Omitting property values will cause the entire property to be absent from the response.

* **`IdentityToken`**

  The identity token.

* **`AccessToken`**

  The access token.

* **`RefreshToken`**

  The refresh token.

* **`AccessTokenLifetime`**

  The access token lifetime in seconds.

* **`Scope`**

  The scope.

* **`Custom`**

  A dictionary of strings to objects that will be serialized to json and added to the token response.
