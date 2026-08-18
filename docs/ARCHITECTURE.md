# Architecture Summary

## Purpose

GxP Validation Copilot is a FastAPI backend that demonstrates how regulated software validation work can combine deterministic traceability, semantic retrieval, LLM-assisted review, and evaluation controls without treating AI output as final approval.

The project uses the synthetic ABFS-100 validation package as a realistic example domain.

## Request Flow

```text
Client
  |
  v
FastAPI routes
  |
  v
Service layer
  |
  +--> deterministic traceability
  +--> semantic retrieval
  +--> LLM coverage assessment
  +--> grounded RAG answering
  +--> agent/tool routing
  |
  v
PostgreSQL + pgvector
```

## Main Boundaries

| Area | Responsibility |
| --- | --- |
| `src/ingestion/` | Parse URS and validation protocol Markdown into structured models. |
| `src/database/` | Persist requirements and tests, including vector embeddings. |
| `src/semantic/` | Build embedding text and rank semantic similarity. |
| `src/services/` | Coordinate traceability, retrieval, RAG, and coverage workflows. |
| `src/LLM/` | OpenAI structured-output components for coverage, RAG, and routing. |
| `src/agent/` | Route user questions to deterministic tools or AI-backed workflows. |
| `src/evaluation/` | Measure retrieval quality, RAG citation behavior, and coverage judgments. |
| `src/api/` | Expose versioned HTTP endpoints, health probes, request IDs, and errors. |

## GxP Guardrails

- Explicit traceability is kept separate from semantic similarity.
- LLM output is structured and conservative.
- RAG answers must cite retrieved validation evidence.
- Human review remains required for final validation conclusions.
- Evaluation datasets provide repeatable evidence of system behavior.

## Production Surface

- `/health` confirms the API process is responsive.
- `/ready` confirms the database dependency is reachable.
- `/version` exposes runtime metadata for deployment verification.
- `X-Request-ID` is accepted or generated for every request.
- Request start, completion, status code, and duration are logged.
- Docker Compose provides reproducible local PostgreSQL and API startup.
