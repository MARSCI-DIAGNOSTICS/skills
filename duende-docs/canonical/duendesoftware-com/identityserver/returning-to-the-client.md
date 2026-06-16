---
title: Returning to the Client
source_url: https://docs.duendesoftware.com/identityserver/returning-to-the-client/
source_type: llms-full-txt
content_hash: sha256:5a42da459b563453e4e1bac1006e054fa8ee2c94d652997e68c6028ec71efffc
category: identityserver
doc_id: identityserver/returning-to-the-client
---

> Guide to properly redirecting users back to client applications after logout in IdentityServer, ensuring front-channel notifications are processed correctly.

If sign-out was initiated by a client application, then the client first redirected the user to the [end session endpoint](/identityserver/reference/endpoints/end-session/). This can be determined if a `logoutId` is passed to the login page and the returned `LogoutRequest`'s `PostLogoutRedirectUri` is set.

## How To Redirect

[Section titled "How To Redirect"](#how-to-redirect)

If there is a `PostLogoutRedirectUri` value, then it's important how this URL is used to redirect the user. The logout page typically should not directly redirect the user to this URL. Doing so would skip the necessary [front-channel notifications](/identityserver/ui/logout/notification/#front-channel-server-side-clients) to clients.

Instead, the typical approach is to render the `PostLogoutRedirectUri` as a link on the "logged out" page. This will allow the page to render, the front-channel iframes will load and perform their duty. It's possible to add JavaScript to the page to enhance this experience even more.
