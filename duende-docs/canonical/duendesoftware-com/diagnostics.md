---
title: Diagnostics
source_url: https://docs.duendesoftware.com/bff/diagnostics/
source_type: llms-full-txt
content_hash: sha256:745edebdec8b636dbf5f2b3eb91fc18718cbf2af229ef42262d4df3956a41162
doc_id: diagnostics
---

> Samples demonstrating IdentityServer's diagnostic capabilities with OpenTelemetry integration, including metrics, traces, and logs visualization with .NET Aspire and console tracing.

This section contains a collection of samples demonstrating various diagnostics options in Duende IdentityServer.

### OpenTelemetry With .NET Aspire

[Section titled "OpenTelemetry With .NET Aspire"](#opentelemetry-with-net-aspire)

Duende IdentityServer emits [OpenTelemetry metrics, traces and logs](/identityserver/diagnostics/otel/). This sample uses .NET Aspire to display OpenTelemetry data. The solution contains an IdentityServer host, an API and a web client. The access token lifetime is set to a tiny value to force frequent refresh token flows.

Running the sample requires the dotnet aspire workload to be installed with `dotnet workload install aspire`. Run the `Aspire.AppHost` project, it will automatically launch the other projects.

This sample is not intended to be a full Aspire sample, it simply uses Aspire as a local standalone tool for displaying traces, logs and metrics.

[OpenTelemetry With .NET Aspire Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Diagnostics/Aspire)GitHub Repository for the OpenTelemetry With .NET Aspire Sample

### OpenTelemetry Tracing

[Section titled "OpenTelemetry Tracing"](#opentelemetry-tracing)

Duende IdentityServer emits [OpenTelemetry traces for input validators, stores and response generators](/identityserver/diagnostics/otel/).

The sample shows how to set up OpenTelemetry for console tracing.

[OpenTelemetry Tracing Sample ](https://github.com/DuendeSoftware/Samples/tree/main/IdentityServer/v7/Diagnostics/Otel)GitHub Repository for the OpenTelemetry Tracing Sample
