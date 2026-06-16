---
title: Data Stores and Persistence
source_url: https://docs.duendesoftware.com/identityserver/data-stores-and-persistence/
source_type: llms-full-txt
content_hash: sha256:fd98532b0d0573cd531e8950ac1bbb9a3e4bf49c95ef40e10858c68306de3d81
last_fetched: '2025-12-16T19:17:25Z'
category: identityserver
doc_id: identityserver/data-stores-and-persistence
---

> Overview of IdentityServer data stores types, including configuration and operational data, and their implementation options

Duende IdentityServer is backed by two kinds of data:

* [Configuration Data](/identityserver/data/configuration/)
* [Operational Data](/identityserver/data/operational/)

Data access is abstracted by store interfaces that are registered in the ASP.NET Core service provider. These store interfaces allow IdentityServer to access the data it needs at runtime when processing requests. You can implement these interfaces yourself and thus can use any database you wish. If you prefer a relational database for this data, then we provide [EntityFramework Core](/identityserver/data/ef/) implementations.

Note

Given that data stores abstract the details of the data stored, strictly speaking, IdentityServer does not know or understand where the data is actually being stored. As such, there is no built-in administrative tool to populate or manage this data. There are third-party options (both commercial and FOSS) that provide an administrative UI for managing the data when using the EntityFramework Core implementations.
