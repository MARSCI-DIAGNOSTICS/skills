---
name: ml-pipeline
description: Design an ML system for a problem
argument-hint: <problem>
allowed-tools: Read, Glob, Grep, Skill, Task
---

# Design ML Pipeline

Design an end-to-end ML system architecture for a given problem.

## Arguments

`$ARGUMENTS` - The ML problem to design for (e.g., "recommendation system", "fraud detection", "search ranking", "content moderation")

## Workflow

1. **Clarify requirements** by understanding:
   - What predictions are being made?
   - What is the latency requirement? (real-time vs batch)
   - What is the scale? (QPS, data volume)
   - Who are the consumers of predictions?

2. **Load relevant skills** based on the problem:
   - Core ML architecture → `ml-system-design`
   - LLM-based systems → `llm-serving-patterns`
   - RAG systems → `rag-architecture`
   - Inference optimization → `ml-inference-optimization`
   - Vector search → `vector-databases`

3. **Spawn the ml-systems-designer agent** for comprehensive design:
   - Use Task tool with subagent_type="ml-systems-designer"
   - Provide full problem context and requirements
   - Request end-to-end architecture

4. **Design the complete pipeline**:
   - Data ingestion and processing
   - Feature engineering and feature store
   - Model training infrastructure
   - Model serving and inference
   - Monitoring and observability
   - A/B testing and experimentation

5. **Address cross-cutting concerns**:
   - Training-serving skew prevention
   - Feature consistency
   - Model versioning and rollback
   - Cost optimization

## Example Usage

```bash
/sd:ml-pipeline recommendation system for 100M users
/sd:ml-pipeline real-time fraud detection for payments
/sd:ml-pipeline search ranking for e-commerce with 10M products
/sd:ml-pipeline content moderation for social media
/sd:ml-pipeline ad click prediction at 1M QPS
/sd:ml-pipeline customer churn prediction
/sd:ml-pipeline demand forecasting for inventory
```

## Problem Categories

| Category | Key Considerations |
| -------- | ------------------ |
| Recommendations | Cold start, real-time signals, A/B testing |
| Fraud/Risk | Low latency (<100ms), rules + ML hybrid, feedback loops |
| Search/Ranking | Multi-stage ranking, personalization, position bias |
| NLP/LLM | Inference cost, caching, streaming responses |
| Computer Vision | GPU inference, batching, edge deployment |
| Time Series | Feature freshness, windowing, seasonal patterns |

## Output

A comprehensive ML system architecture including:

- High-level architecture diagram (component-based)
- Data flow from sources to predictions
- Technology stack recommendations
- Trade-offs and alternatives considered
- Phased implementation approach
- Cost and scale considerations
