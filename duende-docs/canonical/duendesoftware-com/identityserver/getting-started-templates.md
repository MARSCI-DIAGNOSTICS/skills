---
title: Getting Started - Templates
source_url: https://docs.duendesoftware.com/identityserver/getting-started-templates/
source_type: llms-full-txt
content_hash: sha256:327129dcca7eb75b083a64a658fd3e8e7d94b985c5649d136525e818edf265f1
category: identityserver
doc_id: identityserver/getting-started-templates
---

> A guide on how to install the BFF project templates.

Project templates for Duende BFF are shipped as part of the Duende .NET project templates. Refer the [templates documentation](/identityserver/overview/packaging/#templates) for more information on how to install the templates.

## Available templates

[Section titled "Available templates"](#available-templates)

### BFF Remote API

[Section titled "BFF Remote API"](#bff-remote-api)

```shell
dotnet new duende-bff-remoteapi
```

Creates a basic JavaScript-based BFF host that configures and invokes a [remote API via the BFF proxy](/bff/fundamentals/apis/remote/).

### BFF Local API

[Section titled "BFF Local API"](#bff-local-api)

```shell
dotnet new duende-bff-localapi
```

Creates a basic JavaScript-based BFF host that invokes a [local API](/bff/fundamentals/apis/local/) co-hosted with the BFF.

### BFF Blazor

[Section titled "BFF Blazor"](#bff-blazor)

```shell
dotnet new duende-bff-blazor
```

Creates a Blazor application that [uses the interactive auto render mode](/bff/fundamentals/blazor/), and secures the application across all render modes consistently using Duende.BFF.Blazor.
