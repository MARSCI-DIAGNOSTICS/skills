---
title: Epoch Time Conversion
source_url: https://docs.duendesoftware.com/epoch-time-conversion/
source_type: llms-full-txt
content_hash: sha256:ec87e962f43654893562f1274733aa4317f14fdb4ecd9e8640ba28ce9cbefd29
last_fetched: '2025-12-16T19:17:23Z'
doc_id: epoch-time-conversion
---

> Learn about converting between DateTime and Unix/Epoch time formats in Duende IdentityModel for JWT tokens

JSON Web Token (JWT) tokens use so-called [Epoch or Unix time](https://en.wikipedia.org/wiki/Unix_time) to represent date/times, which is the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT).

In .NET, you can convert `DateTimeOffset` to Unix/Epoch time via the two methods of `ToUnixTimeSeconds` and `ToUnixTimeMilliseconds`:

EpochTimeExamples.cs

```csharp
var seconds = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
var milliseconds = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
```
