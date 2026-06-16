---
title: Error
source_url: https://docs.duendesoftware.com/identityserver/ui/error/
source_type: llms-full-txt
content_hash: sha256:12880b63a4194deb2a3e040c97d7f4acb38075d49d458816fadf9d668eaa94db
category: identityserver
doc_id: identityserver/error
---

> Documentation for implementing the error page in IdentityServer, which displays information to users when errors occur during the authorization process.

The error page is used to display to the end user that an error has occurred during a request to the [authorize endpoint](/identityserver/reference/endpoints/authorize/).

When an error occurs, IdentityServer will redirect the user to a configurable `ErrorUrl`.

Program.cs

```csharp
builder.Services.AddIdentityServer(opt => {
    opt.UserInteraction.ErrorUrl = "/path/to/error";
})
```

The default `ErrorUrl` is "/home/error". The quickstart UI includes a basic implementation of an error page at that route.

Errors are commonly due to misconfiguration, and there's not much an end user can do about that. But this allows the user to understand that something went wrong and that they are not in the middle of a successful workflow.

## Error Context

[Section titled "Error Context"](#error-context)

Details of the error are provided to the error page via a query string parameter. That parameter's name is configurable using the `ErrorId` option.

Program.cs

```csharp
builder.Services.AddIdentityServer(opt => {
    opt.UserInteraction.ErrorId = "ErrorQueryStringParamName";
})
```

By default, the `ErrorId` is the string "errorId".

The [interaction service](/identityserver/reference/services/interaction-service/#iidentityserverinteractionservice-apis) provides a `GetErrorContextAsync` API that will load error details for an `ErrorId`. The returned [ErrorMessage](/identityserver/reference/services/interaction-service/#errormessage) object contains these details.
