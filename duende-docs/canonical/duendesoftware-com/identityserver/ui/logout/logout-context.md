---
title: Logout Context
source_url: https://docs.duendesoftware.com/identityserver/ui/logout/logout-context/
source_type: llms-full-txt
content_hash: sha256:eb6b3af16b38e9f5a64156442e648d8d457b611fdaaee9e35db7b6f45053c5bb
category: identityserver
doc_id: identityserver/ui/logout/logout-context
---

> Guide to accessing and using the LogoutRequest context in IdentityServer, which provides essential information for implementing proper logout workflows across different initiation scenarios.

To correctly perform all the steps for logout, your logout page needs contextual information about the user's session and the client that initiated logout request. This information is provided by the [LogoutRequest](/identityserver/reference/services/interaction-service/#logoutrequest) class and will provide your logout page data needed for the logout workflow.

## Accessing The LogoutRequest And The `logoutId`

[Section titled "Accessing The LogoutRequest And The logoutId"](#accessing-the-logoutrequest-and-the-logoutid)

The logout page can be triggered in different ways:

* Client Initiated Logout (protocol)
* External Provider Logout Notification (protocol)
* Direct User Access (non-protocol)

If the logout page is being triggered by a protocol workflow, then this means Duende IdentityServer has redirected the user's browser to the logout page. In these scenarios, a `logoutId` parameter will be passed that represents the logout context. The `logoutId` value can be exchanged with the `GetLogoutContextAsync` API on the [interaction service](/identityserver/reference/services/interaction-service/) to obtain a `LogoutRequest` object.

If the page is directly accessed by the user then there will be no `logoutId` parameter, but the context can still be accessed by calling `GetLogoutContextAsync` just without passing any parameters.

In either case, the `LogoutRequest` contains the data to perform client notification, and redirect the user back to the client after logout.
