---
title: Stores
source_url: https://docs.duendesoftware.com/stores/
source_type: llms-full-txt
content_hash: sha256:b235cb9b34afaa1ae46fd5be91c4e1ed660b3eda2827dad4cc0aef3769bdffa4
last_fetched: '2025-12-16T19:17:39Z'
doc_id: stores
---

> An overview of IdentityServer's persistence layer abstractions that manage configuration and operational data for authentication and authorization processes.

Stores in IdentityServer are the persistence layer abstractions responsible for managing various types of data needed for the authentication and authorization processes. They provide interfaces to store and retrieve configuration and operational data.

Common types of stores include:

* Client store - manages client application registrations
* Resource store - handles API resources and scopes
* Persisted grant store - maintains operational data like authorization codes and refresh tokens
* User store - manages user authentication data (typically integrated with ASP.NET Identity)

IdentityServer provides default in-memory implementations of these stores for development scenarios, and extensibility points to implement custom stores using various database technologies for production environments.
