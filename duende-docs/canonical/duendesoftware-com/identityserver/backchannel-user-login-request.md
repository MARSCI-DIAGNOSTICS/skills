---
title: Backchannel User Login Request
source_url: https://docs.duendesoftware.com/identityserver/backchannel-user-login-request/
source_type: llms-full-txt
content_hash: sha256:22e2d4ab078be86e017e7daf6ba961661d0b97479c43f0530c56fa5ebb0261b0
category: identityserver
doc_id: identityserver/backchannel-user-login-request
---

> Reference documentation for the BackchannelUserLoginRequest class which models the information needed to initiate a user login request for Client Initiated Backchannel Authentication (CIBA).

## Duende.IdentityServer.Models.BackchannelUserLoginRequest

[Section titled "Duende.IdentityServer.Models.BackchannelUserLoginRequest"](#duendeidentityservermodelsbackchanneluserloginrequest)

Models the information to initiate a user login request for [CIBA](/identityserver/ui/ciba/).

* **`InternalId`**

  Ihe identifier of the request in the store.

* **`Subject`**

  The subject for whom the login request is intended.

* **`BindingMessage`**

  The binding message used in the request.

* **`AuthenticationContextReferenceClasses`**

  The acr\_values used in the request.

* **`Tenant`**

  The tenant value from the acr\_values used the request.

* **`IdP`**

  The idp value from the acr\_values used in the request.

* **`RequestedResourceIndicators`**

  The resource indicator values used in the request.

* **`Client`**

  The client that initiated the request.

* **`ValidatedResources`**

  The validated resources (i.e. scopes) used in the request.
