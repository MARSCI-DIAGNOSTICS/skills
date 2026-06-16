---
title: Custom Token Request Validator
source_url: https://docs.duendesoftware.com/identityserver/reference/validators/custom-token-request-validator/
source_type: llms-full-txt
content_hash: sha256:8596a7a59252f1aa558e2ee1c9f48ec49a83e723f3f239a72836d4c0f35db260
doc_id: custom-token-request-validator
---

> Documentation for the ICustomTokenRequestValidator interface which allows inserting custom validation logic into token requests with the ability to modify request parameters and response fields.

#### Duende.IdentityServer.Validation.ICustomTokenRequestValidator

[Section titled "Duende.IdentityServer.Validation.ICustomTokenRequestValidator"](#duendeidentityservervalidationicustomtokenrequestvalidator)

Allows running custom code as part of the token issuance pipeline at the token endpoint.

```csharp
/// <summary>
/// Allows inserting custom validation logic into token requests
/// </summary>
public interface ICustomTokenRequestValidator
{
    /// <summary>
    /// Custom validation logic for a token request.
    /// </summary>
    /// <param name="context">The context.</param>
    /// <returns>
    /// The validation result
    /// </returns>
    Task ValidateAsync(CustomTokenRequestValidationContext context);
}
```

* **`ValidateAsync`**

  This method gets called during token request processing. The context gives you access to request and response parameters.

  You can also change certain parameters on the validated request object, e.g. the token lifetime, token type, confirmation method and client claims.

  The `CustomResponse` dictionary allows emitting additional response fields.

  To fail the request, set the `IsError`, the `Error`, and optionally the `ErrorDescription` properties on the `Result` object on the `CustomTokenRequestValidationContext`.
