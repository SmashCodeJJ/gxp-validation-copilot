# GxP Validation Copilot

GxP Validation Copilot is a FastAPI backend for analyzing validation coverage in a regulated, GxP-style system. It parses validation documents, stores structured requirements and test cases, builds traceability reports, retrieves semantically related evidence with vector search, and uses LLM workflows with conservative validation guardrails.

The sample package is based on the synthetic ABFS-100 Automated Bottle Filling System.

## What The System Does

- Parses User Requirements Specification and validation protocol Markdown files.
- Stores requirements and test cases in PostgreSQL.
- Stores text embeddings in pgvector for semantic search.
- Shows explicit traceability between requirements and tests.
- Finds semantically similar test cases for a requirement.
- Uses an LLM to assess whether candidate tests provide validation evidence.
- Answers validation questions from retrieved requirement/test evidence.
- Routes user questions to the right capability instead of sending every
  request through RAG.
- Evaluates retrieval, RAG, and coverage behavior against ground-truth datasets.

## Simple Architecture

```text
Validation Markdown
        |
        v
Ingestion Parsers
        |
        v
PostgreSQL + pgvector
        |
        v
Service Layer  -------->  OpenAI structured outputs
        |
        v
FastAPI /api/v1
        |
        v
API clients, scripts, docs UI

Evaluation scripts read from data/evaluation and measure system quality.
```

The key idea is separation of responsibility:

- `src/ingestion/` turns source documents into structured objects.
- `src/database/` stores and queries persistent records.
- `src/semantic/` builds embeddings and similarity scores.
- `src/services/` coordinates multi-step workflows.
- `src/LLM/` contains OpenAI-backed reasoning components.
- `src/api/` exposes the system through FastAPI routes.
- `src/evaluation/` measures whether retrieval and AI behavior are reliable.

## Development Milestones

| Milestone | Focus | Result |
| --- | --- | --- |
| 1. Synthetic validation package | Created the ABFS-100 sample documents. | The project has realistic URS, validation tests, risk, and system context files under `data/synthetic/abfs100/`. |
| 2. Document parsing | Added Markdown parsers for requirements and protocol tests. | The system can convert URS and test specs into Pydantic models. |
| 3. Traceability API | Built the first FastAPI endpoints and explicit traceability report. | The API can return requirements, tests, and requirement-to-test coverage. |
| 4. Database persistence | Added SQLAlchemy, PostgreSQL models, ingestion, repository functions, and isolated API tests. | Data is parsed once, stored in the database, and served through repository-backed endpoints. |
| 5. Semantic retrieval | Added embeddings, pgvector columns, text builders, and vector similarity search. | Requirements and tests can be compared by meaning, not only by explicit IDs. |
| 6. LLM coverage analysis | Added structured coverage assessment and review-priority logic. | Candidate tests can be classified as `full`, `partial`, `none`, or `uncertain` evidence for a requirement. |
| 7. RAG question answering | Added retrieval over requirements/tests and grounded answer generation. | The system can answer validation questions using retrieved source evidence. |
| 8. Evaluation framework | Added ground-truth CSVs and metric evaluators. | Retrieval, citation precision, abstention behavior, and coverage judgments can be measured. |
| 9. Production readiness | Added Docker, Docker Compose, typed settings, logging, error handling, health/readiness checks, API versioning, and CI. | The application can run as a cleaner service with `/api/v1` routes and reproducible local infrastructure. |
| 10. Agent/tool routing | Added an agent router, deterministic tools, an agent orchestration service, routing evaluation data, and an agent API endpoint. | User questions can be routed to traceability, semantic search, coverage analysis, or RAG based on intent. |
| 11. Production observability | Added request IDs, request lifecycle logs, runtime metadata, LLM/RAG/agent logging hooks, and log-focused tests. | Production issues can be traced with `X-Request-ID`, endpoint, status, and duration details. |
| 12. Deployment and portfolio polish | Added deployment configuration, Docker hardening, a runbook, architecture summary, interview guide, and readiness tests. | The project is ready to explain, verify, containerize, and present as a portfolio backend project. |

## Main Components

| Path | Responsibility |
| --- | --- |
| `src/api/` | FastAPI app, route modules, dependency wiring, and error handlers. |
| `src/config/` | Environment-based settings and logging configuration. |
| `src/database/` | SQLAlchemy models, sessions, ingestion persistence, and repository queries. |
| `src/ingestion/` | Markdown readers and parsers for requirements and validation protocols. |
| `src/semantic/` | Embedding service, embedding text builders, cosine similarity, and semantic matching. |
| `src/services/` | RAG retrieval, source validation, coverage analysis, and application workflows. |
| `src/LLM/` | OpenAI-backed RAG answerer and coverage evaluator. |
| `src/evaluation/` | Metric models, evaluators, thresholds, and report helpers. |
| `scripts/` | Setup, ingestion, semantic matching, and evaluation scripts. |
| `tests/` | Unit and API tests. |
| `data/` | Synthetic validation documents and ground-truth evaluation data. |
| `docs/ARCHITECTURE.md` | Interview-ready architecture summary. |
| `docs/DEPLOYMENT_RUNBOOK.md` | Deployment, verification, and operations checklist. |
| `docs/PORTFOLIO_INTERVIEW_GUIDE.md` | Portfolio pitch, resume bullets, and interview talking points. |

## API Surface

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Basic service health check. |
| `GET` | `/ready` | Readiness check including database connectivity. |
| `GET` | `/version` | Runtime app name, version, and environment. |
| `GET` | `/api/v1/requirements` | List parsed user requirements. |
| `GET` | `/api/v1/tests` | List parsed validation test cases. |
| `GET` | `/api/v1/traceability` | Show explicit requirement-to-test coverage. |
| `GET` | `/api/v1/requirements/{requirement_id}/semantic-matches` | Rank semantically similar tests for one requirement. |
| `GET` | `/api/v1/requirements/{requirement_id}/coverage-analysis` | Assess candidate test evidence for a requirement. |
| `POST` | `/api/v1/rag/query` | Answer validation questions from retrieved evidence. |
| `POST` | `/api/v1/agent/query` | Route a user question to the appropriate validation tool. |

## Guardrails

The AI components are advisory. The system is designed to support validation review, not replace final approval.

- RAG answers must come from retrieved validation context.
- Responses cite requirement IDs and test IDs.
- Semantic similarity is treated as candidate evidence, not proof of coverage.
- Coverage assessment stays conservative for GxP validation.
- Final validation decisions require human review.

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

Interactive API docs:

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

## Deployment Readiness

Milestone 12 documentation is under `docs/`:

- `docs/ARCHITECTURE.md`
- `docs/DEPLOYMENT_RUNBOOK.md`
- `docs/PORTFOLIO_INTERVIEW_GUIDE.md`

Before a release, verify:

```bash
pytest -q
docker build -t gxp-validation-copilot:test .
docker compose up --build
```

Then check:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/version
```

## Run Evaluation

```bash
python -m scripts.evaluate_retrieval
```

Local retrieval evaluation over the included ABFS-100 ground truth produced:

- Top-1 accuracy: `75.00%`
- Recall@3: `100.00%`

Additional evaluation scripts are available under `scripts/`.

## Tech Stack

| Layer | Tools |
| --- | --- |
| API | FastAPI, Pydantic |
| Persistence | SQLAlchemy, PostgreSQL |
| Vector search | pgvector, SentenceTransformers |
| LLM workflows | OpenAI API structured outputs |
| Testing and evaluation | Pytest, custom evaluators |
| Runtime | Docker, Docker Compose |
| CI | GitHub Actions |

## Author

Built by [SmashCodeJJ](https://github.com/SmashCodeJJ).
