---
name: rag-design
description: Design a RAG architecture for a use case
argument-hint: <use-case>
allowed-tools: Read, Glob, Grep, Skill, Task
---

# Design RAG Architecture

Design a Retrieval-Augmented Generation system for a given use case.

## Arguments

`$ARGUMENTS` - The RAG use case to design for (e.g., "customer support chatbot", "documentation Q&A", "legal document search", "code assistant")

## Workflow

1. **Clarify requirements** by understanding:
   - What type of questions will be asked?
   - What is the document corpus size and type?
   - What is the required accuracy/faithfulness?
   - What is the latency budget?
   - Are there multi-turn conversation requirements?

2. **Load relevant skills** based on the use case:
   - RAG patterns → `rag-architecture`
   - Vector store selection → `vector-databases`
   - LLM serving → `llm-serving-patterns`
   - Inference optimization → `ml-inference-optimization`

3. **Spawn the rag-architect agent** for comprehensive design:
   - Use Task tool with subagent_type="rag-architect"
   - Provide full use case context and requirements
   - Request end-to-end RAG architecture

4. **Design the ingestion pipeline**:
   - Document extraction (PDF, HTML, code)
   - Chunking strategy selection
   - Embedding model selection
   - Vector database configuration
   - Metadata extraction and indexing

5. **Design the retrieval pipeline**:
   - Query processing (expansion, HyDE)
   - Retrieval strategy (dense, sparse, hybrid)
   - Reranking approach
   - Context assembly
   - Prompt engineering

6. **Address quality and scale**:
   - Retrieval accuracy (recall@k, MRR)
   - Answer faithfulness (grounding)
   - Latency budget allocation
   - Cost optimization
   - Scaling strategy

## Example Usage

```bash
/sd:rag-design customer support chatbot with 10K FAQ documents
/sd:rag-design internal documentation Q&A for engineering team
/sd:rag-design legal document search for contract review
/sd:rag-design code assistant for enterprise codebase
/sd:rag-design research paper Q&A with 100K papers
/sd:rag-design product catalog search with structured data
/sd:rag-design multi-lingual knowledge base
```

## Use Case Categories

| Category | Key Considerations |
| -------- | ------------------ |
| Customer Support | FAQ coverage, escalation, tone consistency |
| Documentation | Technical accuracy, code examples, versioning |
| Legal/Compliance | Citation accuracy, audit trails, access control |
| Code Assistance | AST-aware chunking, context relevance, IDE integration |
| Research/Academic | Multi-document reasoning, citation, long-form answers |
| E-commerce | Product attributes, inventory awareness, personalization |

## RAG Pattern Selection Guide

| Complexity | Pattern | When to Use |
| ---------- | ------- | ----------- |
| Low | Basic RAG | Simple Q&A, small corpus |
| Medium | RAG + Reranking | Higher accuracy needed |
| Medium | Hybrid Search | Mixed keyword + semantic queries |
| High | Query-Transformed | Vague or complex queries |
| High | Agentic RAG | Multi-hop reasoning, tool use |

## Output

A comprehensive RAG system architecture including:

- Ingestion pipeline (documents → vectors)
- Retrieval pipeline (query → context)
- Technology stack (embedding model, vector DB, LLM)
- Quality targets (recall, faithfulness, latency)
- Trade-offs and alternatives
- Cost estimate (per-query and monthly)
