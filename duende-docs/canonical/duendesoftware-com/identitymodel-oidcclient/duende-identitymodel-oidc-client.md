---
title: Duende IdentityModel OIDC Client
source_url: https://docs.duendesoftware.com/identitymodel-oidcclient/duende-identitymodel-oidc-client/
source_type: llms-full-txt
content_hash: sha256:305d688c2b18e4ec5dc849b93a5f460ad9b9b42ca8e4995138d1234f0c2a9f92
category: identitymodel-oidcclient
doc_id: identitymodel-oidcclient/duende-identitymodel-oidc-client
---

> A certified OpenID Connect relying party library for building native clients with .NET, supporting various UI frameworks and authentication flows

Tip

**`Duende.IdentityModel.OidcClient` is a [certified](https://openid.net/certification/) OpenID Connect relying party implementation.**

The `Duende.IdentityModel.OidcClient` library is a certified OpenID Connect relying party and implements [RFC 8252](https://tools.ietf.org/html/rfc8252/), "OAuth 2.0 for native Applications". The `Duende.IdentityModel.OidcClient.Extensions` library provides support for [DPoP](https://datatracker.ietf.org/doc/html/rfc9449) extensions to Duende.IdentityModel.OidcClient for sender-constraining tokens.

## Use Cases

[Section titled "Use Cases"](#use-cases)

OidcClient targets .NET Standard, making it suitable for .NET and .NET Framework. It can be used to build OIDC native clients with a variety of .NET UI tools.

* .NET MAUI
* WPF with the system browser
* WPF with an embedded browser
* WinForms with an embedded browser
* Cross-platform Console Applications (relies on kestrel for processing the callback)
* Windows Console Applications (relies on an HttpListener - a wrapper around the windows HTTP.sys driver)
* Windows Console Applications using custom uri schemes

## License and Feedback

[Section titled "License and Feedback"](#license-and-feedback)

`Duende.IdentityModel.OidcClient` is released as open source under the [Apache 2.0 license](https://github.com/DuendeSoftware/foss/blob/main/LICENSE). Bug reports and contributions are welcome at [the GitHub repository](https://github.com/DuendeSoftware/foss).

[GitHub Repository ](https://github.com/DuendeSoftware/foss/tree/main/identity-model-oidc-client)View the source code for this library on GitHub.

[NuGet Package ](https://www.nuget.org/packages/Duende.IdentityModel.OidcClient/)View the package on NuGet.org.
