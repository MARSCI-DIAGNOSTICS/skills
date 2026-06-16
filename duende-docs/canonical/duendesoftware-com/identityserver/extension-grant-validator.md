---
title: Extension Grant Validator
source_url: https://docs.duendesoftware.com/identityserver/reference/validators/extension-grant-validator/
source_type: llms-full-txt
content_hash: sha256:9cb2faf27c1639a2d503e209886e883a1a4d4e65d16b6ee635d91bb43a6298ca
category: identityserver
doc_id: identityserver/extension-grant-validator
---

> Documentation for the IExtensionGrantValidator interface which enables custom OAuth grant types by handling validation of extension grant requests.

#### Duende.IdentityServer.Validation.IExtensionGrantValidator

[Section titled "Duende.IdentityServer.Validation.IExtensionGrantValidator"](#duendeidentityservervalidationiextensiongrantvalidator)

Use an implementation of this interface to handle [extension grants](/identityserver/tokens/extension-grants/).

```csharp
public interface IExtensionGrantValidator
{
    /// <summary>
    /// Handles the custom grant request.
    /// </summary>
    /// <param name="request">The validation context.</param>
    Task ValidateAsync(ExtensionGrantValidationContext context);


    /// <summary>
    /// Returns the grant type this validator can deal with
    /// </summary>
    /// <value>
    /// The type of the grant.
    /// </value>
    string GrantType { get; }
}
```

* **`GrantType`**

  Specifies the name of the extension grant that the implementation wants to register for.

* **`ValidateAsync`**

  This method gets called at runtime, when a request comes in that is using the registered extension grant. The job of this method is to validate the request and to populate `ExtensionGrantValidationContext.Result` with a [grant validation result](/identityserver/reference/models/grant-validation-result/)

The instance of the extension grant validator gets registered with:

Program.cs

```csharp
builder.AddExtensionGrantValidator<MyValidator>();
```
