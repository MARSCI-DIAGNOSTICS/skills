---
title: "Solving the Distributed Cache Invalidation Problem with Redis and HybridCache"
slug: solving-the-distributed-cache-invalidation-problem-with-redis-and-hybridcache
date: 2026-01-17
author: Milan Jovanovic
description: "When running multiple application instances with HybridCache, stale data across nodes becomes a consistency problem. This article shows how to use Redis Pub/Sub as a backplane to synchronize cache invalidation across all instances."
tags:
  - aspnet-core
  - caching
  - distributed-systems
  - redis
source_url: https://www.milanjovanovic.tech/blog/solving-the-distributed-cache-invalidation-problem-with-redis-and-hybridcache
doc_id: milanjovanovic-tech-blog-solving-the-distributed-cache-invalidation-problem-with-redis-and-hybridcache
---

# Solving the Distributed Cache Invalidation Problem with Redis and HybridCache

## The Distributed Caching Dilemma

When running multiple application instances behind a load balancer with HybridCache, a consistency problem emerges. If data is updated on Server 1, Server 2 continues serving stale data from its local cache until that entry expires.

Simply reducing cache duration (TTL) doesn't solve this - it only masks the problem while introducing increased latency and lost efficiency by forcing more frequent requests to Redis or the database.

## The Solution: Redis Pub/Sub Backplane

The solution uses Redis Pub/Sub as a backplane - a communication channel connecting all application nodes. When a cache entry is removed on one node, that node publishes a message. All subscribing nodes receive this notification and call `HybridCache.RemoveAsync(key)` to evict the stale entry locally.

## Implementation Details

The solution involves three components:

**1. Cache Invalidator Service**: Publishes invalidation messages to Redis when data changes.

**2. Background Listener**: A `BackgroundService` subscribing to Redis invalidation messages and removing keys from the local L1 cache.

**3. Dependency Injection Setup**: Registering `IConnectionMultiplexer`, `HybridCache`, the invalidator service, and background service.

When developers update entities in command handlers, they call `ICacheInvalidator.InvalidateAsync(cacheKey)`. This triggers Redis to broadcast the invalidation message to all nodes, ensuring consistent cache state across the distributed system.

## Alternative: FusionCache

FusionCache provides a mature, battle-tested alternative with built-in backplane support and a HybridCache implementation, allowing seamless integration without extensive custom code.
