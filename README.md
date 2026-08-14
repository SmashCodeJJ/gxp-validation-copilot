# GxP Validation Copilot

GxP Validation Copilot is a FastAPI backend that helps validation engineers analyze requirement coverage for a regulated, GxP-style system. It parses validation documents, stores structured requirements and test cases, builds traceability views, retrieves semantically related evidence with vector search, and uses LLM-based review flows that keep human approval in the loop.

This project is built as a portfolio-grade example of applied backend engineering, AI retrieval, and quality evaluation for a high-accountability domain.

## What It Demonstrates

- Backend API design with FastAPI, dependency injection, structured error handling, and versioned routes
- Data modeling with Pydantic and SQLAlchemy 2.0
- PostgreSQL plus pgvector for semantic retrieval
- SentenceTransformers embeddings for requirement-to-test matching
- OpenAI structured outputs for RAG answers and coverage assessments
- GxP-aware guardrails: citation validation, conservative coverage labels, and required human review
- Evaluation workflows for retrieval quality, RAG citation behavior, and coverage classification
- Dockerized local runtime and GitHub Actions CI

## Domain Scenario

The synthetic sample package models an ABFS-100 Automated Bottle Filling System. The data includes:

- User Requirements Specification
- Validation test specification
- Functional specification
- Risk assessment
- System overview
- Evaluation ground-truth CSV files

The system can answer questions such as:

- Which tests explicitly cover a requirement?
- Which requirements have no explicit validation coverage?
- Which tests are semantically similar to an uncovered requirement?
- Does a test provide full, partial, uncertain, or no evidence for a requirement?
- Can the assistant answer from retrieved validation evidence without inventing unsupported claims?

## Architecture

```text
Markdown validation docs
        |
        v
Ingestion parsers
        |
        v
SQLAlchemy models in PostgreSQL + pgvector
        |
        +--> Traceability API
        +--> Semantic matching API
        +--> RAG retrieval service
        +--> LLM coverage analysis
        |
        v
Evaluation scripts and tests
```

## API Surface

Health:

- `GET /health`
- `GET /ready`

Validation:

- `GET /api/v1/requirements`
- `GET /api/v1/tests`
- `GET /api/v1/traceability`
- `GET /api/v1/requirements/{requirement_id}/semantic-matches`
- `GET /api/v1/requirements/{requirement_id}/coverage-analysis`

RAG:

- `POST /api/v1/rag/query`

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- pgvector
- SentenceTransformers
- OpenAI API
- Pytest
- Docker and Docker Compose
- GitHub Actions

## Local Setup

Create a local environment file:

```bash
cp .env.example .env
```

Start Postgres and the API:

```bash
docker compose up --build
```

The API runs at:

```text
http://localhost:8000
```

The interactive API docs are available at:

```text
http://localhost:8000/docs
```

## Load Sample Data

After the database is running, ingest the synthetic validation package:

```bash
python -m scripts.ingest_documents
```

This loads requirements, validation tests, and embeddings for semantic retrieval.

## Run Tests

```bash
pytest -q
```

The test suite covers document parsing, traceability reporting, repository behavior, API endpoints, semantic similarity, retrieval evaluation, RAG evaluation helpers, and quality threshold logic.

## Evaluation Snapshot

A local retrieval evaluation over the included ABFS-100 ground truth produced:

- Top-1 accuracy: 75.00%
- Recall@3: 100.00%

That result is intentionally visible because regulated AI systems need measurable behavior, not just demos. The project includes evaluation code so retrieval and answer quality can be improved and tracked over time.

## Safety Posture

This copilot is designed for validation support, not autonomous approval. The LLM prompts and response models require conservative reasoning, source citations, and human review flags. Semantic similarity is treated as candidate evidence, not proof of validation coverage.

## Repository Structure

```text
src/api/          FastAPI app, routes, dependencies, error handlers
src/database/     SQLAlchemy models, sessions, ingestion, repositories
src/ingestion/    Markdown parsers and traceability report builders
src/semantic/     Embeddings, similarity scoring, semantic matching
src/services/     RAG, source validation, coverage analysis services
src/LLM/          OpenAI-backed coverage and RAG answerers
src/evaluation/   Retrieval, RAG, coverage, and quality evaluation logic
scripts/          Operational scripts for setup, ingestion, and evaluation
tests/            Unit and API tests
data/             Synthetic validation documents and evaluation data
```

## Author

Built by [SmashCodeJJ](https://github.com/SmashCodeJJ) as a recruiter-facing project showing backend engineering, applied AI, validation-domain thinking, and production-minded evaluation.
