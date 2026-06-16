# Latency Numbers Every Programmer Should Know

These numbers help you understand the relative cost of operations when designing systems.

## Core Latency Reference (2024 estimates)

| Operation | Latency | Notes |
| --------- | ------- | ----- |
| L1 cache reference | 0.5 ns | Fastest possible memory access |
| Branch mispredict | 5 ns | CPU pipeline flush |
| L2 cache reference | 7 ns | ~14x slower than L1 |
| Mutex lock/unlock | 25 ns | Thread synchronization cost |
| Main memory reference | 100 ns | RAM access |
| Compress 1KB with Snappy | 3 us | Fast compression |
| Send 1KB over 1 Gbps network | 10 us | Network is expensive |
| Read 4KB randomly from SSD | 16 us | ~160x slower than RAM |
| Read 1MB sequentially from memory | 3 us | Memory is fast for sequential |
| Read 1MB sequentially from SSD | 49 us | SSD sequential is good |
| Round trip within same datacenter | 500 us | 0.5 ms |
| Read 1MB sequentially from disk | 825 us | HDD is slow |
| Disk seek | 2 ms | Random HDD access is very slow |
| Send packet CA to Netherlands and back | 150 ms | Cross-continent latency |

## Relative Comparisons

If L1 cache access = 1 second (for human intuition):

| Operation | Relative Time |
| --------- | ------------- |
| L1 cache reference | 1 second |
| L2 cache reference | 14 seconds |
| Main memory reference | 3 minutes |
| SSD random read | 9 hours |
| HDD seek | 46 days |
| Cross-continent round trip | 9.5 years |

## Implications for System Design

### Memory vs Disk

```text
RAM: 100 ns
SSD: 16 us (160x slower)
HDD: 2 ms (20,000x slower)

Takeaway: Keep hot data in memory. Every disk access is expensive.
```

### Local vs Network

```text
Local memory: 100 ns
Same datacenter: 500 us (5,000x slower)
Cross-region: 150 ms (1,500,000x slower)

Takeaway: Minimize network calls. Colocate services that talk frequently.
```

### Sequential vs Random

```text
Sequential SSD read (1MB): 49 us
Random SSD read (4KB): 16 us
Ratio: ~3x faster per byte for sequential

Sequential HDD read (1MB): 825 us
Random HDD seek: 2 ms
Ratio: ~100x faster for sequential

Takeaway: Design for sequential access patterns when possible.
```

## Database Operation Estimates

| Operation | Typical Latency |
| --------- | --------------- |
| Simple key-value lookup (cached) | 1 ms |
| Simple query (indexed) | 1-10 ms |
| Complex query (joins) | 10-100 ms |
| Full table scan | 100ms - 10s |
| Cross-shard query | 10-100 ms |

## Network Latencies

| Route | Typical RTT |
| ----- | ----------- |
| Same rack | 0.1 ms |
| Same datacenter | 0.5 ms |
| Same region (e.g., US-East) | 1-5 ms |
| Cross-region (US-East to US-West) | 40-60 ms |
| Cross-continent (US to Europe) | 70-100 ms |
| Cross-Pacific (US to Asia) | 150-200 ms |

## Cache Performance

| Cache Type | Access Time | Capacity |
| ---------- | ----------- | -------- |
| L1 cache | 0.5 ns | 32-64 KB |
| L2 cache | 7 ns | 256 KB - 1 MB |
| L3 cache | 20-40 ns | 8-64 MB |
| RAM | 100 ns | 64-512 GB |
| Redis (local) | 0.5 ms | TB+ |
| Redis (remote) | 1-5 ms | TB+ |

## Throughput Numbers

| System | Throughput |
| ------ | ---------- |
| Single HDD | 100-200 MB/s sequential |
| Single SSD | 500 MB/s - 3 GB/s |
| NVMe SSD | 3-7 GB/s |
| RAM | 20-100 GB/s |
| 10 Gbps network | 1.25 GB/s theoretical |
| 100 Gbps network | 12.5 GB/s theoretical |

## Cost Implications

| Storage Type | $/GB/month (approx) |
| ------------ | ------------------- |
| RAM | $10-20 |
| SSD | $0.10-0.20 |
| HDD | $0.02-0.05 |
| S3/Blob storage | $0.02-0.03 |
| Archive storage | $0.004 |

**Rule of thumb:**

- RAM is 100x more expensive than SSD
- SSD is 5x more expensive than HDD
- Choose based on access patterns

## Design Guidelines from These Numbers

### 1. Cache Everything Expensive

If you're doing it more than once:

- Cache database queries (1ms+ -> sub-ms)
- Cache API responses (100ms+ -> 1ms)
- Cache computed results

### 2. Minimize Network Hops

Each hop adds latency:

- Microservice call: +1-5ms
- External API: +50-200ms
- Cross-region: +50-100ms

### 3. Batch Operations

```text
10 individual reads: 10 * 2ms = 20ms
1 batch read of 10: 5ms

Takeaway: Batch when possible.
```

### 4. Use Async for Slow Operations

If operation > 100ms:

- Move to background job
- Use message queue
- Return immediately, notify when done

### 5. Replicate for Read Performance

```text
Single database: 1000 QPS max
With 5 read replicas: 5000 QPS

Takeaway: Scale reads with replicas.
```

## Sources and Updates

These numbers are approximations that change over time as hardware improves:

- Original: Jeff Dean's "Numbers Every Programmer Should Know" (2009)
- Updated estimates for modern hardware (2024)
- Your mileage may vary based on specific hardware/cloud provider

**Rule of thumb for interviews:** Memorize the order of magnitude, not exact numbers.

---

**Last Updated:** 2025-12-26
