---
title: Logging
source_url: https://docs.duendesoftware.com/accesstokenmanagement/advanced/logging/
source_type: llms-full-txt
content_hash: sha256:0fd939fd4d85f3eb8c8bf6b4cf5107bc48a746bbb04fc16c613a6d658d6f52b7
doc_id: accesstokenmanagement/advanced/logging
---

> Documentation for logging configuration and usage in Duende Access Token Management, including log levels and Serilog setup

Duende Access Token Management uses the standard logging facilities provided by ASP.NET Core. You generally do not need to perform any extra configuration, as it will use the logging provider you have already configured for your application.

For general information on how to configure logging, setting up Serilog, and understanding log levels in Duende products, see our [Logging Fundamentals](/general/logging/) guide.

The Microsoft [documentation](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/logging) has a good introduction and description of the built-in logging providers.

## Log Levels

[Section titled "Log Levels"](#log-levels)

You can control the log output for Duende Access Token Management specifically by configuring the `Duende.AccessTokenManagement` namespace in your logging configuration. For example, to enable debug logging for Access Token Management while keeping other logs at a higher level, you can modify your `appsettings.json`:

appsettings.json

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Duende.AccessTokenManagement": "Debug"
    }
  }
}
```
