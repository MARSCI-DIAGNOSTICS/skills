---
title: Device Flow Interaction Service
source_url: https://docs.duendesoftware.com/identityserver/reference/services/device-flow-interaction-service/
source_type: llms-full-txt
content_hash: sha256:71c3a452931dd1432511ce3d84c8f234883e24084b740f311cac75c611d7c908
doc_id: identityserver/reference/services/device-flow-interaction-service
---

> Documentation for the IDeviceFlowInteractionService interface which provides services for user interfaces to communicate with IdentityServer during device flow authorization.

#### Duende.IdentityServer.Services.IDeviceFlowInteractionService

[Section titled "Duende.IdentityServer.Services.IDeviceFlowInteractionService"](#duendeidentityserverservicesideviceflowinteractionservice)

The `IDeviceFlowInteractionService` interface is intended to provide services to be used by the user interface to communicate with Duende IdentityServer during device flow authorization. It is available from the dependency injection system and would normally be injected as a constructor parameter into your MVC controllers for the user interface of IdentityServer.

## IDeviceFlowInteractionService APIs

[Section titled "IDeviceFlowInteractionService APIs"](#ideviceflowinteractionservice-apis)

* **`GetAuthorizationContextAsync`**

  Returns the `DeviceFlowAuthorizationRequest` based on the `userCode` passed to the login or consent pages.

* **`DeviceFlowInteractionResult`**

  Completes device authorization for the given `userCode`.

## DeviceFlowAuthorizationRequest

[Section titled "DeviceFlowAuthorizationRequest"](#deviceflowauthorizationrequest)

* **`ClientId`**

  The client identifier that initiated the request.

* **`ScopesRequested`**

  The scopes requested from the authorization request.

## DeviceFlowInteractionResult

[Section titled "DeviceFlowInteractionResult"](#deviceflowinteractionresult)

* **`IsError`**

  Specifies if the authorization request errored.

* **`ErrorDescription`**

  Error description upon failure.
