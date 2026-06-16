---
title: Securing and Accessing API Endpoints
source_url: https://docs.duendesoftware.com/securing-and-accessing-api-endpoints/
source_type: llms-full-txt
content_hash: sha256:8e509fcffab1b5527cf7e28e8001a393d5d5987395fabf047f5a82ee8b2ab8bc
doc_id: securing-and-accessing-api-endpoints
---

> Learn about the different types of APIs in a BFF architecture and how to secure and access them properly

A frontend application using the BFF pattern can call two types of APIs:

#### Embedded (Local) APIs

[Section titled "Embedded (Local) APIs"](#embedded-local-apis)

These APIs embedded inside the BFF and typically exist to support the BFF's frontend; they are not shared with other frontends or services.

See [Embedded APIs](local/) for more information.

#### Proxying Remote APIs

[Section titled "Proxying Remote APIs"](#proxying-remote-apis)

These APIs are deployed on a different host than the BFF, which allows them to be shared between multiple frontends or (more generally speaking) multiple clients. These APIs can only be called via the BFF host acting as a proxy.

You can use [Direct Forwarding](remote/) for most scenarios. If you have more complex requirements, you can also directly interact with [YARP](yarp/)
