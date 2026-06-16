---
title: UserInfo Endpoint
source_url: https://docs.duendesoftware.com/userinfo-endpoint/
source_type: llms-full-txt
content_hash: sha256:a19690033047dbdf645d70684953cba5110e21044bf2c86957362983cede280a
doc_id: userinfo-endpoint
---

The client library for the [OpenID Connect UserInfo](https://openid.net/specs/openid-connect-core-1_0.html#userinfo) endpoint is provided as an extension method for `HttpClient`.

The following code sends an access token to the UserInfo endpoint:

```csharp
var client = new HttpClient();


var response = await client.GetUserInfoAsync(new UserInfoRequest
{
    Address = disco.UserInfoEndpoint,
    Token = token
});
```

The response is of type `UserInfoResponse` and has properties for the standard response parameters. You also have access to the raw response and to a parsed JSON document (via the `Raw` and `Json` properties).

Before using the response, you should always check the `IsError` property to make sure the request was successful:

```csharp
if (response.IsError) throw new Exception(response.Error);


var claims = response.Claims;
```
