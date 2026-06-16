---
title: DPoP Proof Validator
source_url: https://docs.duendesoftware.com/identityserver/reference/validators/dpop-proof-validator/
source_type: llms-full-txt
content_hash: sha256:8416c6ef803394d6524775f24c48a9423e7eda34ca69000f57250fa0600b1540
category: identityserver
doc_id: identityserver/reference/validators/dpop-proof-validator
---

> Documentation for the IDPoPProofValidator interface which validates Demonstrating Proof of Possession (DPoP) tokens to ensure secure binding between access tokens and client key pairs.

#### Duende.IdentityServer.Validation.IDPoPProofValidator

[Section titled "Duende.IdentityServer.Validation.IDPoPProofValidator"](#duendeidentityservervalidationidpopproofvalidator)

The `IDPoPProofValidator` interface is used to validate [DPoP](/identityserver/tokens/pop/) proof tokens submitted to IdentityServer. A default implementation is provided and can be overridden as necessary.

## IDPoPProofValidator APIs

[Section titled "IDPoPProofValidator APIs"](#idpopproofvalidator-apis)

* **`ValidateAsync`**

  Validates a DPoP proof token with the provided `DPoPProofValidatonContext` for the current request. Returns a `DPoPProofValidatonResult` object.

```csharp
Task<DPoPProofValidatonResult> ValidateAsync(DPoPProofValidatonContext context, CancellationToken ct);
```

### DPoPProofValidatonContext

[Section titled "DPoPProofValidatonContext"](#dpopproofvalidatoncontext)

Models the information used to validate a DPoP proof token.

* **`ExpirationValidationMode`**

  Enum setting to control validation for the DPoP proof token expiration. Supports both the client-generated `iat` value and/or the server-generated `nonce` value. Defaults to `DPoPTokenExpirationValidationMode.Iat`.

* **`ClientClockSkew`**

  Clock skew used in validating the DPoP proof token `iat` claim value. Defaults to *5 minutes*.

* **`Url`**

  The HTTP URL to validate in the DPoP proof.

* **`Method`**

  The HTTP method to validate in the DPoP proof.

* **`ProofToken`**

  The DPoP proof token string to validate.

* **`ValidateAccessToken`**

  If `true`, the access token will also be validated against the proof.

* **`AccessToken`**

  The access token string to validate when `ValidateAccessToken` is `true`.

* **`AccessTokenClaims`**

  The claims associated with the access token, used when `ValidateAccessToken` is `true`. Provided separately from `AccessToken` because resolving claims from a reference token may be expensive.

### DPoPProofValidationResult

[Section titled "DPoPProofValidationResult"](#dpopproofvalidationresult)

Models the result of a DPoP proof token validation.

* **`IsError`**

  Flag to indicate if validation failed.

* **`Error`**

  The error code if the validation failed.

* **`ErrorDescription`**

  The error description if the validation failed.

* **`JsonWebKey`**

  The serialized JWK from the validated DPoP proof token.

* **`JsonWebKeyThumbprint`**

  The JWK thumbprint from the validated DPoP proof token.

* **`Confirmation`**

  The 'cnf' value for the DPoP proof token.

* **`Payload`**

  The payload values of the DPoP proof token.

* **`TokenId`**

  The 'jti' value read from the payload.

* **`Nonce`**

  The 'nonce' value read from the payload.

* **`IssuedAt`**

  The 'iat' value read from the payload.

* **`ServerIssuedNonce`**

  The 'nonce' value issued by the server that should be emitted on the response.
