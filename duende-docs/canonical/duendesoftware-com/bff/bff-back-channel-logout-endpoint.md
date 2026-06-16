---
title: BFF Back-Channel Logout Endpoint
source_url: https://docs.duendesoftware.com/bff/bff-back-channel-logout-endpoint/
source_type: llms-full-txt
content_hash: sha256:12d5820d9f7e72350e30f69a824edcbd9651929766f5b264c1a1d39ef93eeb1b
category: bff
doc_id: bff/bff-back-channel-logout-endpoint
---

> Documentation for the OpenID Connect Back-Channel Logout endpoint implementation in BFF, enabling server-to-server session termination without browser involvement.

The */bff/backchannel* endpoint is an implementation of the [OpenID Connect Back-Channel Logout](https://openid.net/specs/openid-connect-backchannel-1_0.html) specification. The remote identity provider can use this endpoint to end the BFF's session via a server to server call, without involving the user's browser. This design avoids problems with 3rd party cookies associated with front-channel logout.

## Typical Usage

[Section titled "Typical Usage"](#typical-usage)

The back-channel logout endpoint is invoked by the remote identity provider when it determines that sessions should be ended. IdentityServer will send back-channel logout requests if you [configure](/identityserver/reference/models/client/#authentication--session-management) your client's *BackChannelLogoutUri*. When a session ends at IdentityServer, any client that was participating in that session that has a back-channel logout URI configured will be sent a back-channel logout request. This typically happens when another application signs out. [Expiration](/identityserver/ui/server-side-sessions/session-expiration/) of [IdentityServer server side sessions](/identityserver/ui/server-side-sessions/) can also be configured to send back-channel logout requests, though this is disabled by default.

## Dependencies

[Section titled "Dependencies"](#dependencies)

The back-channel logout endpoint depends on [server-side sessions in the BFF](/bff/fundamentals/session/server-side-sessions/), which must be enabled to use this endpoint. Note that such server-side sessions are distinct from server-side sessions in IdentityServer.

## Revoke All Sessions

[Section titled "Revoke All Sessions"](#revoke-all-sessions)

Back-channel logout tokens include a sub (subject ID) and sid (session ID) claim to describe which session should be revoked. By default, the back-channel logout endpoint will only revoke the specific session for the given subject ID and session ID. Alternatively, you can configure the endpoint to revoke every session that belongs to the given subject ID by setting the *BackchannelLogoutAllUserSessions* [option](/bff/fundamentals/options/#session-management) to true.
