# GxP Validation Copilot

GxP Validation Copilot is a backend AI project for reviewing software validation evidence in a regulated life-sciences style workflow.

In plain English: the system reads requirements and validation test cases, builds a traceability map, finds possible missing coverage, retrieves relevant evidence, and uses carefully controlled LLM workflows to help a validation engineer review whether a requirement is actually tested.

The project is built around a synthetic validation package for an **ABFS-100 Automated Bottle Filling System**. The sample data is not real company data, but it is structured like the documents used in regulated software validation.

## Why This Project Exists

In GxP environments, teams must prove that software requirements are tested before a system can be released. This usually involves documents such as:

- User Requirements Specification, or URS
- Functional/system specifications
- Validation protocols
- Test cases
- Traceability matrices
- Evidence review

Manual review is slow and error-prone. A reviewer has to answer questions like:

- Which requirements have tests?
- Which requirements are missing tests?
- Does this test really verify the requirement, or is it only loosely related?
- Where is the evidence for this answer?
- Can an AI assistant help without inventing validation conclusions?

This project demonstrates one possible backend architecture for that problem.

## What It Can Do

| Capability | What It Means |
| --- | --- |
| Document parsing | Reads Markdown validation documents and extracts structured requirements and test cases. |
| Traceability | Maps requirements to validation tests using explicit requirement IDs. |
| PostgreSQL persistence | Stores requirements and tests in a database instead of only keeping them in files. |
| Semantic search | Uses embeddings and pgvector to find tests that are meaningfully similar to a requirement. |
| LLM coverage review | Uses structured AI output to classify whether a test provides `full`, `partial`, `none`, or `uncertain` evidence. |
| RAG question answering | Answers validation questions from retrieved requirement and test evidence. |
| Agent routing | Sends user questions to the right tool: traceability, semantic search, coverage analysis, or RAG. |
| Evaluation | Measures retrieval, RAG, coverage analysis, and routing behavior against ground-truth datasets. |
| Observability | Adds request IDs, request lifecycle logs, runtime metadata, and health/readiness checks. |
| Deployment readiness | Includes Docker, Docker Compose, CI, runbook documentation, and portfolio/interview notes. |

## Example Questions The System Supports

A validation engineer could ask:

```text
Which requirements are not explicitly traced to a test?
```

```text
Find tests that may provide evidence for URS-003.
```

```text
Does TEST-002 fully verify URS-002?
```

```text
What evidence exists that only approved recipes can be selected?
```

```text
Route this question to the safest validation tool.
```

The important design choice is that the system does **not** send every question directly to a general chatbot. It uses deterministic tools when possible and AI only where it adds value.

## High-Level Workflow

```text
Validation documents
        |
        v
Markdown parsers
        |
        v
Structured requirements and test cases
        |
        v
PostgreSQL + pgvector
        |
        v
Traceability, semantic search, RAG, coverage analysis
        |
        v
FastAPI endpoints
        |
        v
Validation engineer or API client
```

## Simple Architecture

```text
                  +----------------------+
                  |  Validation Markdown |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |  Ingestion Parsers   |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  | PostgreSQL + pgvector|
                  +----------+-----------+
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
 +----------------+  +----------------+  +----------------+
 | Traceability   |  | Semantic Search|  | RAG / LLM Review|
 +----------------+  +----------------+  +----------------+
          |                  |                  |
          +------------------+------------------+
                             |
                             v
                  +----------------------+
                  | FastAPI /api/v1      |
                  +----------------------+
```

The code is intentionally separated by responsibility:

| Path | Responsibility |
| --- | --- |
| `src/ingestion/` | Turns source documents into structured Python models. |
| `src/database/` | Defines SQLAlchemy models, sessions, ingestion, and repository queries. |
| `src/semantic/` | Builds embedding text, generates embeddings, and ranks similarity. |
| `src/services/` | Coordinates multi-step validation workflows. |
| `src/LLM/` | Contains OpenAI-backed structured-output components. |
| `src/agent/` | Routes user intent to the correct validation tool. |
| `src/evaluation/` | Measures whether retrieval and AI behavior are reliable. |
| `src/api/` | Exposes the system through FastAPI routes, middleware, and error handlers. |
| `data/` | Contains synthetic validation documents and evaluation data. |
| `docs/` | Contains architecture, deployment, and interview-ready documentation. |

## GxP And AI Guardrails

This project treats AI as an assistant, not as the final validation authority.

Key guardrails:

- Explicit traceability is kept separate from semantic similarity.
- Semantic similarity suggests candidate evidence, but does not prove coverage.
- RAG answers must be grounded in retrieved validation context.
- LLM responses use structured outputs where possible.
- Coverage analysis is conservative by design.
- Final validation decisions require human review.
- Evaluation datasets are used to measure system behavior repeatedly.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Basic service health check. |
| `GET` | `/ready` | Readiness check, including database connectivity. |
| `GET` | `/version` | Runtime app name, version, and environment. |
| `GET` | `/api/v1/requirements` | List parsed user requirements. |
| `GET` | `/api/v1/tests` | List parsed validation test cases. |
| `GET` | `/api/v1/traceability` | Show explicit requirement-to-test coverage. |
| `GET` | `/api/v1/requirements/{requirement_id}/semantic-matches` | Rank semantically similar tests for one requirement. |
| `GET` | `/api/v1/requirements/{requirement_id}/coverage-analysis` | Assess candidate test evidence for one requirement. |
| `POST` | `/api/v1/rag/query` | Answer validation questions from retrieved evidence. |
| `POST` | `/api/v1/agent/query` | Route a user question to the best validation tool. |

## Tech Stack

| Layer | Tools |
| --- | --- |
| API | FastAPI, Pydantic |
| Persistence | SQLAlchemy, PostgreSQL |
| Vector search | pgvector, SentenceTransformers |
| LLM workflows | OpenAI API structured outputs |
| Testing | Pytest |
| Evaluation | Custom retrieval, RAG, coverage, and routing evaluators |
| Runtime | Docker, Docker Compose |
| CI | GitHub Actions |

## Quick Start

Create a local environment file:

```bash
cp .env.example .env
```

Add your OpenAI API key to `.env`, then start the database and API:

```bash
docker compose up --build
```

The API runs at:

```text
http://localhost:8000
```

Interactive API docs:

```text
http://localhost:8000/docs
```

## Load Sample Data

After the database is running, load the synthetic ABFS-100 validation package:

```bash
python -m scripts.ingest_documents
```

This loads requirements, validation tests, and embeddings for semantic retrieval.

## Run Tests

```bash
pytest -q
```

The Docker/Python 3.11 verification for the latest milestone passed with:

```text
41 passed
```

## Run Evaluation

Example retrieval evaluation:

```bash
python -m scripts.evaluate_retrieval
```

Local retrieval evaluation over the included ABFS-100 ground truth produced:

- Top-1 accuracy: `75.00%`
- Recall@3: `100.00%`

Additional evaluation scripts are available under `scripts/`.

## Development Milestones

| Milestone | Focus | Result |
| --- | --- | --- |
| 1 | Synthetic validation package | Created realistic sample URS, system, risk, and validation test documents. |
| 2 | Document parsing | Converted Markdown requirements and test protocols into structured models. |
| 3 | Traceability API | Added FastAPI endpoints for requirements, tests, and traceability. |
| 4 | Database persistence | Added PostgreSQL, SQLAlchemy models, repositories, and ingestion persistence. |
| 5 | Semantic retrieval | Added embeddings and pgvector similarity search. |
| 6 | LLM coverage analysis | Added structured coverage review for requirement-test evidence. |
| 7 | RAG question answering | Added grounded answers over retrieved validation context. |
| 8 | Evaluation framework | Added ground-truth datasets and quality metrics. |
| 9 | Production readiness | Added Docker, Compose, settings, logging, error handling, health/readiness checks, API versioning, and CI. |
| 10 | Agent/tool routing | Added a router that chooses deterministic tools or AI workflows based on user intent. |
| 11 | Production observability | Added request IDs, request lifecycle logs, runtime metadata, and observability tests. |
| 12 | Deployment and portfolio polish | Added deployment configuration, Docker hardening, runbook docs, architecture docs, and interview guide. |

## Portfolio Notes

This project is useful for interviews because it shows more than a basic chatbot:

- Backend API design with FastAPI
- Database modeling and repository patterns
- Vector search with pgvector
- RAG with source-grounding rules
- Structured LLM outputs
- Agent/tool routing
- Evaluation-driven AI development
- Docker-based deployment readiness
- Production observability basics
- GxP-aware thinking around evidence, traceability, and human review

More detailed portfolio and interview material:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/DEPLOYMENT_RUNBOOK.md`](docs/DEPLOYMENT_RUNBOOK.md)
- [`docs/PORTFOLIO_INTERVIEW_GUIDE.md`](docs/PORTFOLIO_INTERVIEW_GUIDE.md)

## Author

Built by [SmashCodeJJ](https://github.com/SmashCodeJJ).
