---
title: Authorize Interaction Response Generator
source_url: https://docs.duendesoftware.com/identityserver/reference/response-handling/authorize-interaction-response-generator/
source_type: llms-full-txt
content_hash: sha256:5ee6c1ae29604418592b2976e8faba4c1f78146017b1aee6a9873e4eb40bf8d7
doc_id: identityserver/reference/response-handling/authorize-interaction-response-generator
---

> Documentation for the IAuthorizeInteractionResponseGenerator interface which determines if a user must log in or consent when making requests to the authorization endpoint.

#### Duende.IdentityServer.ResponseHandling.IAuthorizeInteractionResponseGenerator

[Section titled "Duende.IdentityServer.ResponseHandling.IAuthorizeInteractionResponseGenerator"](#duendeidentityserverresponsehandlingiauthorizeinteractionresponsegenerator)

The `IAuthorizeInteractionResponseGenerator` interface models the logic for determining if user must log in or consent when making requests to the authorization endpoint.

Note

If a custom implementation of `IAuthorizeInteractionResponseGenerator` is desired, then it's [recommended](/identityserver/ui/custom/#built-in-authorizeinteractionresponsegenerator) to derive from the built-in `AuthorizeInteractionResponseGenerator` to inherit all the default logic pertaining to log in and consent semantics.

## IAuthorizeInteractionResponseGenerator APIs

[Section titled "IAuthorizeInteractionResponseGenerator APIs"](#iauthorizeinteractionresponsegenerator-apis)

* **`ProcessInteractionAsync`**

  Returns the `InteractionResponse` based on the `ValidatedAuthorizeRequest` an and optional `ConsentResponse` if the user was shown a consent page.

## InteractionResponse

[Section titled "InteractionResponse"](#interactionresponse)

* **`IsLogin`**

  Specifies if the user must log in.

* **`IsConsent`**

  Specifies if the user must consent.

* **`IsCreateAccount`**

  Added in `v6.3`.

  Specifies if the user must create an account.

* **`IsError`**

  Specifies if the user must be shown an error page.

* **`Error`**

  The error to display on the error page.

* **`ErrorDescription`**

  The description of the error to display on the error page.

* **`IsRedirect`**

  Specifies if the user must be redirected to a custom page for custom processing.

* **`RedirectUrl`**

  The URL for the redirect to the page for custom processing.
