---
title: BFF Silent Login Endpoint
source_url: https://docs.duendesoftware.com/bff/bff-silent-login-endpoint/
source_type: llms-full-txt
content_hash: sha256:241b5684f818bdfb7a39ce696d8fa9e0c169d9e377855e73d5da68c897dec35d
last_fetched: '2025-12-16T19:17:20Z'
category: bff
doc_id: bff/bff-silent-login-endpoint
---

> Endpoint for non-interactive authentication using an existing session at the remote identity provider

Note

Deprecated. See [OIDC Prompt support](/bff/fundamentals/session/oidc-prompts/) instead.

**Added in v1.2.0.**

The */bff/silent-login* endpoint triggers authentication similarly to the login endpoint, but in a non-interactive way.

The expected usage pattern is that the application code loads in the browser and triggers a request to the *User Endpoint*. If that indicates that there is no BFF session, then the *Silent Login Endpoint* can be requested to attempt to automatically log the user in, using an existing session at the remote identity provider.

This non-interactive design relies upon the use of an *iframe* to make the silent login request. The result of the silent login request in the *iframe* will then use *postMessage* to notify the parent window of the outcome. If the result is that a session has been established, then the application logic can either re-trigger a call to the *User Endpoint*, or reload the entire page (depending on the preferred design). If the result is that a session has not been established, then the application redirects to the login endpoint to log the user in interactively.

To trigger the silent login, the application code must have an *iframe* and then set its *src* to the silent login endpoint. For example in your HTML:

```html
<iframe id="bff-silent-login"></iframe>
```

And then in JavaScript:

```javascript
document.querySelector('#bff-silent-login').src = '/bff/silent-login';
```

To receive the result, the application should handle the *message* event in the browser and look for the *data.isLoggedIn* property on the event object:

```javascript
window.addEventListener("message", e => {
  if (e.data && e.data.source === 'bff-silent-login' && e.data.isLoggedIn) {
      // we now have a user logged in silently, so reload this window
      window.location.reload();
  }
});
```
