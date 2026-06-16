---
title: Backchannel Authentication User Validator
source_url: https://docs.duendesoftware.com/backchannel-authentication-user-validator/
source_type: llms-full-txt
content_hash: sha256:209fadd389a261fcfd137bcefb5fdd152a62ebed0d380b23b5d75a98b150b8cb
doc_id: backchannel-authentication-user-validator
---

> Documentation for the IBackchannelAuthenticationUserValidator interface which is used to validate request hints and identify the user for CIBA authentication requests.

#### Duende.IdentityServer.Validation.IBackchannelAuthenticationUserValidator

[Section titled "Duende.IdentityServer.Validation.IBackchannelAuthenticationUserValidator"](#duendeidentityservervalidationibackchannelauthenticationuservalidator)

The `IBackchannelAuthenticationUserValidator` interface is used to validate request hints and identify the user for whom the [CIBA](/identityserver/ui/ciba/) request is intended. To use CIBA, you are expected to implement this interface and register it in the ASP.NET Core service provider.

## IBackchannelAuthenticationUserValidator APIs

[Section titled "IBackchannelAuthenticationUserValidator APIs"](#ibackchannelauthenticationuservalidator-apis)

* **`ValidateRequestAsync`**

  Validates the backchannel login request with the provided `BackchannelAuthenticationUserValidatorContext` for the current request. Returns a `BackchannelAuthenticationUserValidationResult` object.

### BackchannelAuthenticationUserValidatorContext

[Section titled "BackchannelAuthenticationUserValidatorContext"](#backchannelauthenticationuservalidatorcontext)

Models the information to validate and identity the user for a CIBA login request.

* **`Client`**

  The `Client` making the request.

* **`LoginHintToken`**

  The login hint request parameter from the request.

* **`IdTokenHint`**

  The id token hint request parameter from the request.

* **`IdTokenHintClaims`**

  The claims contained in the validated id token hint from the request.

* **`LoginHint`**

  The login hint request parameter from the request.

* **`UserCode`**

  The user code request parameter from the request.

* **`BindingMessage`**

  The binding request parameter from the request.

### BackchannelAuthenticationUserValidationResult

[Section titled "BackchannelAuthenticationUserValidationResult"](#backchannelauthenticationuservalidationresult)

Models the result of a CIBA login request.

* **`Subject`**

  The `ClaimsPrincipal` that represents the user that was successfully identified for the login request. This must contain the user's `"sub"` claim.

* **`Error`**

  The error if the user validation failed.

* **`ErrorDescription`**

  The error description if the user validation failed.
