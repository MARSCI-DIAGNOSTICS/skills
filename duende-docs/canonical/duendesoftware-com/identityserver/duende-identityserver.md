---
title: Duende IdentityServer
source_url: https://docs.duendesoftware.com/identityserver/duende-identityserver/
source_type: llms-full-txt
content_hash: sha256:bdeb5a0d69e4f66238b7f3f145f679d56edb1288a2443d02419ec0d5181e2322
category: identityserver
doc_id: identityserver/duende-identityserver
---

> Overview of Duende IdentityServer framework for OpenID Connect and OAuth 2.x protocols, covering extensibility, security scenarios, licensing, and support.

Duende IdentityServer is a highly extensible, standards-compliant framework for implementing the OpenID Connect and OAuth 2.x protocols in ASP.NET Core. It offers deep flexibility for handling authentication, authorization, and token issuance and can be adapted to fit complex custom security scenarios.

[GitHub Repository ](https://github.com/DuendeSoftware/products/tree/main/identity-server/)View the source code for this library on GitHub.

[NuGet Package ](https://www.nuget.org/packages/Duende.IdentityServer/)View the package on NuGet.org.

## Extensibility Points

[Section titled "Extensibility Points"](#extensibility-points)

* **Customizable User Experience**: Go beyond simple branding to fully customizable user interfaces.
* **Core Engine Customization**: The engine itself is modular and built from services that can be extended or overridden.

## Advanced Security Scenarios

[Section titled "Advanced Security Scenarios"](#advanced-security-scenarios)

Duende IdentityServer supports a wide range of security scenarios for modern applications:

* **Federation**: Easily integrate with external identity providers or other authentication services using [federation](/identityserver/ui/federation/).
* **Token Exchange**: Enable secure token exchange between clients and services with [Token Exchange](/identityserver/tokens/extension-grants/#token-exchange).
* **Audience Constrained Tokens**: Restrict tokens to specific audiences, increasing security in multi-service architectures. Learn more about [audience-constrained tokens](/identityserver/fundamentals/resources/isolation/).
* **Sender Constrained Tokens**: Implement Proof of Possession (PoP) tokens with [DPoP or mTLS](/identityserver/tokens/pop/), which bind tokens to the client, adding another layer of protection.
* **Pushed Authorization Requests (PAR)**: Support [Pushed Authorization Requests](/identityserver/tokens/par/) to enhance the security of the authorization flow.
* **FAPI 2.0**: protect APIs in high-value scenarios with the[FAPI 2.0 Security profile](/identityserver/tokens/fapi-2-0-specification/).

## Licensing

[Section titled "Licensing"](#licensing)

Duende IdentityServer is source-available, but **requires a paid [license](https://duendesoftware.com/products/identityserver) for production use.**

* **Development and Testing**: You are free to use and explore the code for development, testing, or personal projects without a license.
* **Production**: A license is required for production environments.
* **Free Community Edition**: A free Community Edition license is available for qualifying companies and non-profit organizations. Learn more [here](https://duendesoftware.com/products/communityedition).

## Reporting Issues and Getting Support

[Section titled "Reporting Issues and Getting Support"](#reporting-issues-and-getting-support)

* For bug reports or feature requests, [use our developer community forum](https://github.com/DuendeSoftware/community).
* For security-related concerns, please contact us privately at: **<security@duendesoftware.com>**.
