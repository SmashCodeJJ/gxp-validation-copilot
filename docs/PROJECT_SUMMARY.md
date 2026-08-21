# Project Summary

## Project Overview

GxP Validation Copilot is a backend project that shows how AI can support regulated validation work without replacing human approval. It parses requirements and test protocols, builds traceability, retrieves semantically related evidence, runs conservative LLM coverage analysis, answers grounded RAG questions, routes user requests to the right tool, and evaluates the system against ground-truth datasets.

## Core Design Points

- Deterministic traceability is the source of truth.
- Semantic search finds candidate evidence but does not prove coverage.
- LLM outputs are structured, conservative, and advisory.
- RAG answers are constrained to retrieved validation context.
- Evaluation data makes AI behavior measurable instead of purely subjective.
- Deployment readiness includes Docker, health probes, readiness checks, request IDs, logs, and CI.

## Architecture Notes

- FastAPI provides a clean API layer with `/api/v1` routes.
- PostgreSQL stores requirements and tests.
- pgvector supports semantic retrieval over validation evidence.
- SQLAlchemy keeps persistence separate from service logic.
- OpenAI structured outputs make coverage, RAG, and routing responses easier to validate.
- Pytest covers parsers, services, API behavior, evaluation metrics, routing, and observability.
- Docker Compose gives a repeatable local production-like environment.

## Key Technical Decisions

| Question | Strong Answer Direction |
| --- | --- |
| Why not send every question to RAG? | Deterministic tools are safer and cheaper when the answer is explicit traceability or known structured data. |
| How do you reduce hallucination risk? | Restrict context, use structured outputs, validate cited sources, keep conservative prompts, and require human review. |
| How do you know retrieval works? | Use ground-truth evaluation data and metrics such as top-1 accuracy and recall@k. |
| What makes this GxP-aware? | The system separates evidence from interpretation, preserves traceability, logs behavior, and treats AI as advisory. |
| What would be improved next? | Add migrations, authentication, role-based access, production metrics storage, audit trails, and cloud deployment automation. |

## Project Highlights

- Built a FastAPI-based GxP Validation Copilot that parses validation documents, stores requirements/tests in PostgreSQL, and generates traceability reports.
- Implemented pgvector-backed semantic retrieval and grounded RAG workflows with source validation and human-review guardrails.
- Added structured LLM coverage analysis to classify requirement-test evidence as full, partial, none, or uncertain.
- Built an agent router that chooses deterministic traceability, semantic search, coverage analysis, or RAG based on user intent.
- Created evaluation datasets and pytest coverage for parsing, API behavior, retrieval quality, RAG behavior, routing, and observability.
- Containerized the application with Docker Compose, health/readiness probes, request IDs, structured logs, CI, and deployment runbook documentation.
