---
name: optimize-llm
description: Get LLM optimization recommendations for serving latency, inference costs, and throughput improvements
allowed-tools: Read, Glob, Grep, Task
argument-hint: "[focus: latency|cost|throughput]"
---

# Optimize LLM Command

Get quick, actionable recommendations for LLM serving optimization.

## Usage

```text
/sd:optimize-llm [focus]
```

## Arguments

- `focus` (optional): Optimization priority
  - `latency` - Focus on reducing response time
  - `cost` - Focus on reducing inference costs
  - `throughput` - Focus on maximizing requests/second
  - If omitted: Provide balanced recommendations

## Examples

```text
/sd:optimize-llm
/sd:optimize-llm latency
/sd:optimize-llm cost
```

## Workflow

1. **Gather Context**
   - Search for LLM-related configuration files
   - Look for: model configs, serving configs, inference scripts
   - Identify current serving stack (vLLM, TGI, TensorRT-LLM, etc.)

2. **Spawn LLM Optimization Advisor Agent**
   Use the `llm-optimization-advisor` agent to analyze and provide recommendations. The agent specializes in:
   - Quantization strategies (INT8, INT4, FP16)
   - Batching optimization (continuous, dynamic)
   - KV cache optimization (PagedAttention)
   - Serving framework selection
   - Cost reduction strategies

3. **Present Recommendations**
   Display optimization opportunities organized by:
   - **Quick Wins** - Low effort, high impact changes
   - **Medium Effort** - Moderate changes with significant benefits
   - **Advanced** - Architectural changes for maximum performance

## Output Format

```text
## LLM Optimization Report

### Current Setup
- Model: [detected or ask]
- Framework: [detected or unknown]
- Hardware: [detected or ask]

### Quick Wins
1. [Optimization] - [Expected impact]
2. ...

### Medium Effort Optimizations
1. [Optimization] - [Expected impact]
2. ...

### Advanced Optimizations
1. [Optimization] - [Expected impact]
2. ...

### Estimated Total Impact
- Latency: [X]% improvement
- Cost: [X]% reduction
- Throughput: [X]x increase
```
