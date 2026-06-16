---
title: BFF Login Endpoint
source_url: https://docs.duendesoftware.com/bff/bff-login-endpoint/
source_type: llms-full-txt
content_hash: sha256:bfc107cebc06838e8c0353ee6644fd40d6b84d36de6263e7d1443113b32a1914
category: bff
doc_id: bff/bff-login-endpoint
---

> Learn how to initiate authentication and handle return URLs using the BFF login endpoint in your frontend applications

The */bff/login* endpoint begins the authentication process. To use it, typically javascript code will navigate away from the frontend application to the login endpoint:

```js
window.location = "/login";
```

In Blazor, instead use the *NavigationManager* to navigate to the login endpoint:

```csharp
Navigation.NavigateTo($"bff/login", forceLoad: true);
```

The login endpoint triggers an authentication challenge using the default challenge scheme, which will typically use the OpenID Connect [handler](/bff/fundamentals/session/handlers/).

## Return Url

[Section titled "Return Url"](#return-url)

After authentication is complete, the login endpoint will redirect back to your front end application. By default, this redirect goes to the root of the application. You can use a different URL instead by including a local URL as the *returnUrl* query parameter.

```js
window.location = "/login?returnUrl=/logged-in";
```
