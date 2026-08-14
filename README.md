# GxP Validation Copilot

GxP Validation Copilot is a FastAPI backend for analyzing validation coverage in a regulated, GxP-style system. It parses validation documents, stores structured requirements and test cases, builds traceability reports, finds semantically related evidence with vector search, and uses LLM-based review flows with conservative guardrails.

The sample domain is the ABFS-100 Automated Bottle Filling System, a synthetic validation package with user requirements, validation tests, system context, risk notes, and evaluation ground truth.

## Core Capabilities

| Area | What the system does |
| --- | --- |
| Document ingestion | Parses Markdown validation documents into structured requirement and test-case records. |
| Traceability | Maps requirements to explicitly linked validation tests and highlights uncovered requirements. |
| Semantic matching | Uses embeddings and pgvector search to find test cases that are semantically similar to a requirement. |
| RAG question answering | Retrieves relevant requirements/tests and answers only from supplied validation context. |
| Coverage analysis | Uses an LLM to classify whether a test provides full, partial, uncertain, or no evidence for a requirement. |
| Evaluation | Measures retrieval, citation, abstention, and coverage quality against ground-truth datasets. |

## Architecture Overview

```mermaid
flowchart LR
    docs["Validation Documents<br/>URS, tests, risk, system overview"]
    ingest["Ingestion Layer<br/>Markdown parsers"]
    db[("PostgreSQL<br/>requirements, tests")]
    vector[("pgvector<br/>384-d embeddings")]
    api["FastAPI Application<br/>/health, /api/v1"]
    services["Service Layer<br/>traceability, retrieval, RAG, coverage"]
    llm["OpenAI API<br/>structured outputs"]
    eval["Evaluation Suite<br/>ground truth + metrics"]
    clients["API Clients<br/>docs UI, scripts, external tools"]

    docs --> ingest
    ingest --> db
    ingest --> vector
    clients --> api
    api --> services
    services --> db
    services --> vector
    services --> llm
    eval --> db
    eval --> vector
    eval --> services
```

The project is intentionally split into small layers. Parsers do not know about API routes, API routes do not perform database queries directly unless the operation is simple, and LLM calls sit behind service/evaluator classes so they can be tested or replaced.

## Runtime Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI Route
    participant Service
    participant Repo as Repository
    participant DB as PostgreSQL/pgvector
    participant LLM as OpenAI

    Client->>API: HTTP request
    API->>Service: Validate request + inject dependencies
    Service->>Repo: Query structured records or vector matches
    Repo->>DB: SQLAlchemy select / pgvector distance
    DB-->>Repo: Requirements, tests, similarity scores
    Repo-->>Service: Domain records
    opt LLM-assisted route
        Service->>LLM: Prompt with retrieved validation evidence
        LLM-->>Service: Structured Pydantic response
    end
    Service-->>API: Response model
    API-->>Client: JSON response
```

## Data And AI Pipeline

```mermaid
flowchart TD
    urs["URS Markdown"]
    protocol["Validation Test Markdown"]
    req_parser["Requirement Parser"]
    test_parser["Protocol Parser"]
    req_model["Requirement DTO"]
    test_model["TestCase DTO"]
    embedder["SentenceTransformer<br/>all-MiniLM-L6-v2"]
    req_record["RequirementRecord<br/>text + embedding"]
    test_record["TestCaseRecord<br/>objective, steps, expected result + embedding"]
    trace["Traceability Report<br/>explicit links"]
    semantic["Semantic Matches<br/>cosine distance search"]
    rag["RAG Context<br/>requirements + tests"]
    coverage["Coverage Assessment<br/>full / partial / none / uncertain"]

    urs --> req_parser --> req_model
    protocol --> test_parser --> test_model
    req_model --> embedder --> req_record
    test_model --> embedder --> test_record
    req_record --> trace
    test_record --> trace
    req_record --> semantic
    test_record --> semantic
    req_record --> rag
    test_record --> rag
    req_record --> coverage
    test_record --> coverage
```

## Main Components

| Path | Responsibility |
| --- | --- |
| `src/api/` | FastAPI application, routes, dependency wiring, error handlers. |
| `src/config/` | Environment-driven settings and logging configuration. |
| `src/database/` | SQLAlchemy models, session factory, ingestion persistence, query helpers. |
| `src/ingestion/` | Markdown readers and parsers for requirements and validation protocols. |
| `src/semantic/` | Embedding service, cosine similarity helper, semantic matcher. |
| `src/services/` | Application workflows for RAG, retrieval, source validation, and coverage analysis. |
| `src/LLM/` | OpenAI-backed RAG answer generation and coverage evaluation. |
| `src/evaluation/` | Ground-truth loaders, evaluation models, metrics, thresholds, report generation. |
| `scripts/` | Operational scripts for setup, ingestion, semantic matching, and evaluation. |
| `tests/` | Unit and API tests for parsers, routes, repositories, retrieval metrics, and RAG helpers. |
| `data/` | Synthetic ABFS-100 validation documents and evaluation CSV files. |

## API Surface

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Basic service health check. |
| `GET` | `/ready` | Readiness check including database connectivity. |
| `GET` | `/api/v1/requirements` | List parsed user requirements. |
| `GET` | `/api/v1/tests` | List parsed validation test cases. |
| `GET` | `/api/v1/traceability` | Show explicit requirement-to-test coverage. |
| `GET` | `/api/v1/requirements/{requirement_id}/semantic-matches` | Rank semantically similar tests for one requirement. |
| `GET` | `/api/v1/requirements/{requirement_id}/coverage-analysis` | Ask the LLM to assess candidate test evidence for a requirement. |
| `POST` | `/api/v1/rag/query` | Answer validation questions from retrieved requirement/test evidence. |

## RAG And Coverage Guardrails

```mermaid
flowchart LR
    question["User question"]
    retrieve["Retrieve evidence<br/>requirements + tests"]
    context["Build bounded context"]
    answer["LLM structured answer"]
    citations["Validate cited sources"]
    review["Human review required"]

    question --> retrieve --> context --> answer --> citations --> review
```

The assistant is designed for validation support, not autonomous approval. The prompts and response models enforce conservative behavior:

- Answer only from retrieved validation context.
- Cite requirement IDs and test IDs.
- Separate explicit traceability from semantic similarity.
- Refuse to invent missing validation evidence.
- Mark final decisions as requiring human review.

## Data Model

```mermaid
erDiagram
    REQUIREMENT {
        int id PK
        string requirement_id UK
        text requirement_text
        string source_document
        vector embedding
    }

    TEST_CASE {
        int id PK
        string test_id UK
        text objective
        json related_requirements
        json test_steps
        text expected_result
        string source_document
        vector embedding
    }

    REQUIREMENT ||--o{ TEST_CASE : related_requirements
```

The explicit traceability relationship is stored inside each test case as `related_requirements`. Semantic similarity is stored separately as embeddings so the system can recommend possible evidence without treating it as approved coverage.

## Evaluation Flow

```mermaid
flowchart TD
    gt["Ground-truth CSV files"]
    retrieval_eval["Retrieval evaluation<br/>Top-1, Recall@3"]
    rag_eval["RAG evaluation<br/>source recall, citation precision, abstention"]
    coverage_eval["Coverage evaluation<br/>accuracy, dangerous false positives"]
    thresholds["Quality thresholds"]
    report["Evaluation report"]

    gt --> retrieval_eval
    gt --> rag_eval
    gt --> coverage_eval
    retrieval_eval --> thresholds
    rag_eval --> thresholds
    coverage_eval --> thresholds
    thresholds --> report
```

A local retrieval evaluation over the included ABFS-100 ground truth produced:

- Top-1 accuracy: `75.00%`
- Recall@3: `100.00%`

These metrics help track whether retrieval changes improve evidence discovery without hiding misses that still require review.

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

The test suite covers document parsing, traceability reporting, repository behavior, API endpoints, semantic similarity, retrieval evaluation, RAG evaluation helpers, and quality threshold logic.

## Run Evaluation

```bash
python -m scripts.evaluate_retrieval
```

Additional evaluation scripts are available under `scripts/` for coverage, RAG behavior, vector search, and system-level reporting.

## Tech Stack

| Layer | Tools |
| --- | --- |
| API | FastAPI, Pydantic |
| Persistence | SQLAlchemy, PostgreSQL |
| Vector search | pgvector, SentenceTransformers |
| LLM workflows | OpenAI API structured outputs |
| Testing and evaluation | Pytest, custom metric evaluators |
| Runtime | Docker, Docker Compose |
| CI | GitHub Actions |

## Author

Built by [SmashCodeJJ](https://github.com/SmashCodeJJ).
