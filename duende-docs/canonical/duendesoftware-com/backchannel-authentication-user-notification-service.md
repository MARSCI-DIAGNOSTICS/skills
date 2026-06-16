---
title: Backchannel Authentication User Notification Service
source_url: https://docs.duendesoftware.com/backchannel-authentication-user-notification-service/
source_type: llms-full-txt
content_hash: sha256:ec0aab1304e4d914a38351792648087e91f9d380934b4cfba0fa004021da1212
doc_id: backchannel-authentication-user-notification-service
---

> Documentation for the IBackchannelAuthenticationUserNotificationService interface which is used to notify users when a CIBA login request has been made.

#### Duende.IdentityServer.Services.IBackchannelAuthenticationUserNotificationService

[Section titled "Duende.IdentityServer.Services.IBackchannelAuthenticationUserNotificationService"](#duendeidentityserverservicesibackchannelauthenticationusernotificationservice)

The `IBackchannelAuthenticationUserNotificationService` interface is used to contact users when a [CIBA](/identityserver/ui/ciba/) login request has been made. To use CIBA, you are expected to implement this interface and register it in the ASP.NET Core service provider.

## IBackchannelAuthenticationUserNotificationService APIs

[Section titled "IBackchannelAuthenticationUserNotificationService APIs"](#ibackchannelauthenticationusernotificationservice-apis)

* **`SendLoginRequestAsync`**

  Sends a notification for the user to login via the [BackchannelUserLoginRequest](/identityserver/reference/models/ciba-login-request/) parameter.
