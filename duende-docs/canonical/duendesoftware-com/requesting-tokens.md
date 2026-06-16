---
title: Requesting tokens
source_url: https://docs.duendesoftware.com/requesting-tokens/
source_type: llms-full-txt
content_hash: sha256:b85d3a39eea17f89552850cd625b89d30f7d1d0cd0ef263adff1376b98e47d69
doc_id: requesting-tokens
---

> Samples demonstrating token-related features in IdentityServer, including extension grants for Token Exchange implementation and Personal Access Tokens (PAT) for API integrations without full OAuth clients.

This section contains a collection of samples demonstrating Duende IdentityServer token-related features..

### Extension grants And Token Exchange

[Section titled "Extension grants And Token Exchange"](#extension-grants-and-token-exchange)

This sample shows an implementation of the Token Exchange specification [RFC 8693](https://tools.ietf.org/html/rfc8693) via the [Duende IdentityServer extension grant mechanism](/identityserver/tokens/extension-grants/).

[Extension grants And Token Exchange Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/TokenExchange)GitHub Repository for the Extension grants And Token Exchange Sample

### Personal Access Tokens (PAT)

[Section titled "Personal Access Tokens (PAT)"](#personal-access-tokens-pat)

This sample shows how to provide a self-service UI to create access tokens. This is a common approach to enable integrations with APIs without having to create full-blown OAuth clients.

When combining PATs with the [reference token](/identityserver/tokens/reference/) feature, you also get automatic validation and revocation support. This is very similar to API keys, but does not require custom infrastructure. The sample also contains an API that accepts both JWT and reference tokens.

[Personal Access Tokens (PAT) Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/PAT)GitHub Repository for the Personal Access Tokens (PAT) Sample
