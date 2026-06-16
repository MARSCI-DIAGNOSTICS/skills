---
title: IdentityServer Quickstarts
source_url: https://docs.duendesoftware.com/identityserver/identityserver-quickstarts/
source_type: llms-full-txt
content_hash: sha256:fc5ca8a3c836bd69e1c15275848d45c0c3855af7055a2552becec09425647ca9
category: identityserver
doc_id: identityserver/identityserver-quickstarts
---

> Step-by-step tutorials for implementing common Duende IdentityServer scenarios, from basic setup to advanced features.

The quickstarts provide step-by-step instructions for various common Duende IdentityServer scenarios. They start with the absolute basics and become more complex - it is recommended you do them in order.

* adding Duende IdentityServer to an ASP.NET Core application
* configuring Duende IdentityServer
* issuing tokens for various clients
* securing web applications and APIs
* adding support for EntityFramework based configuration
* adding support for ASP.NET Identity

Every quickstart has a reference solution - you can find the code in the [samples](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Quickstarts) folder.

## Preparation

[Section titled "Preparation"](#preparation)

The first thing you should do is install our templates:

Terminal

```bash
dotnet new install Duende.Templates
```

They will be used as a starting point for the various tutorials.

Note

You may have a previous version of Duende templates (`Duende.Templates`) installed on your machine. To uninstall the previous template package, and install the latest version, use the following command:

Terminal

```bash
dotnet new uninstall Duende.Templates
dotnet new install Duende.Templates
```

[YouTube video player](https://www.youtube.com/embed/cxYmODQHErM)
