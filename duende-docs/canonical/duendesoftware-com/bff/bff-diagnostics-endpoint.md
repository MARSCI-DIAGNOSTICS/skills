---
title: BFF Diagnostics Endpoint
source_url: https://docs.duendesoftware.com/bff/bff-diagnostics-endpoint/
source_type: llms-full-txt
content_hash: sha256:1e58ab6f8687bc3d30a735fbb45ea9070d9d00ab8b6ee5cd33d43484c18e19fe
last_fetched: '2025-12-16T19:17:19Z'
category: bff
doc_id: bff/bff-diagnostics-endpoint
---

> Learn about the BFF diagnostics endpoint that provides access to user and client access tokens for development testing purposes.

Note

This endpoint is only enabled in *Development* mode.

The `/bff/diagnostics` endpoint returns the current user and client access token for testing purposes. The endpoint tries to retrieve and show current tokens. It may invoke both a refresh token flow for the user access token and a client credential flow for the client access token.

To use the diagnostics endpoint, make a `GET` request to `/bff/diagnostics`. Typically, this is done in a browser to diagnose a problem during development.
