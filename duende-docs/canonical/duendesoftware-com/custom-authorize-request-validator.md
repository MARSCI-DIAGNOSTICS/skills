---
title: Custom Authorize Request Validator
source_url: https://docs.duendesoftware.com/identityserver/reference/validators/custom-authorize-request-validator/
source_type: llms-full-txt
content_hash: sha256:997e6a3e1c2f61377af583e993edc18c34d8755aa8a01c29e1947ab5163ac2a1
doc_id: custom-authorize-request-validator
---

> Documentation for the ICustomAuthorizeRequestValidator interface which allows inserting custom validation logic into the authorization request pipeline.

#### Duende.IdentityServer.Validation.ICustomAuthorizeRequestValidator

[Section titled "Duende.IdentityServer.Validation.ICustomAuthorizeRequestValidator"](#duendeidentityservervalidationicustomauthorizerequestvalidator)

Allows running custom code as part of the authorization issuance pipeline at the authorization endpoint.

```csharp
/// <summary>
/// Allows inserting custom validation logic into authorize requests
/// </summary>
public interface ICustomAuthorizeRequestValidator
{
    /// <summary>
    /// Custom validation logic for the authorize request.
    /// </summary>
    /// <param name="context">The context.</param>
    Task ValidateAsync(CustomAuthorizeRequestValidationContext context);
}
```

* **`ValidateAsync`**

  This method gets called during authorize request processing. The context gives you access to request and response parameters.

  To fail the request, set the `IsError`, the `Error`, and optionally the `ErrorDescription` properties on the `Result` object on the `CustomAuthorizeRequestValidationContext`.
