---
title: Base64 URL Encoding
source_url: https://docs.duendesoftware.com/base64-url-encoding/
source_type: llms-full-txt
content_hash: sha256:72f00940b2b31b9fe5cdbd96497329c23b6607db702cd77d55592d22978d0c6b
doc_id: base64-url-encoding
---

> Documentation for Base64 URL encoding and decoding utilities in Duende IdentityModel, used for JWT token serialization

JWT serialization involves transforming the three core components of a JWT (Header, Payload, Signature) into a single, compact, URL-safe string. [Base64 URL encoding](https://tools.ietf.org/html/rfc4648#section-5) is used instead of standard Base64 because it doesn't include characters like `+`, `/`, or `=`, making it safe to use directly in URLs and HTTP headers without requiring further encoding.

In newer .NET versions, you can use the `Base64Url` class found in the `System.Buffers.Text` namespace to decode Base64 payloads using the `DecodeFromChars` method:

```csharp
using System.Buffers.Text;


var jsonString = Base64Url.DecodeFromChars(payload);
```

Encoding can be done using the `EncodeToString` method:

```csharp
using System.Buffers.Text;


var bytes = Encoding.UTF8.GetBytes("some string");
var encodedString = Base64Url.EncodeToString(bytes);
```

Alternatively, ASP.NET Core has built-in support for Base64 encoding and decoding via [WebEncoders.Base64UrlEncode](https://docs.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.webutilities.webencoders.base64urlencode) and [WebEncoders.Base64UrlDecode](https://docs.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.webutilities.webencoders.base64urldecode).

To use these methods, ensure you have the following package installed:

```bash
dotnet add package Microsoft.AspNetCore.WebUtilities
```

Then use the following code:

```csharp
using System.Text;
using Microsoft.AspNetCore.WebUtilities;


var bytes = "hello"u8.ToArray();
var b64url = WebEncoders.Base64UrlEncode(bytes);


bytes = WebEncoders.Base64UrlDecode(b64url);


var text = Encoding.UTF8.GetString(bytes);
Console.WriteLine(text);
```
