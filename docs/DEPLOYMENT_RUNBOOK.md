# Deployment Runbook

## Required Configuration

Set these environment variables in every deployed environment:

| Variable | Purpose |
| --- | --- |
| `ENVIRONMENT` | Runtime label, such as `development`, `staging`, or `production`. |
| `APP_VERSION` | Version shown by `/version`. |
| `DATABASE_URL` | PostgreSQL connection string. |
| `OPENAI_API_KEY` | API key for LLM-backed workflows. |
| `OPENAI_MODEL` | Model used for structured LLM calls. |
| `EMBEDDING_MODEL` | SentenceTransformer model for local embeddings. |
| `LOG_LEVEL` | Logging level, usually `INFO` in production. |
| `API_HOST` | Bind host, usually `0.0.0.0` in containers. |
| `API_PORT` | API port, usually `8000`. |
| `API_WORKERS` | Uvicorn worker count. Start with `1`; increase after load testing. |

Never commit real `.env` secrets.

## Local Deployment Check

```bash
cp .env.example .env
docker compose up --build
```

Then check:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/version
```

Expected result:

- `/health` returns `{"status":"ok"}`.
- `/ready` returns `{"status":"ready","database":"ok"}` when PostgreSQL is reachable.
- `/version` returns app name, version, and environment.

## Data Initialization

Create tables:

```bash
python -m scripts.create_tables
```

Load the synthetic validation package:

```bash
python -m scripts.ingest_documents
```

Run evaluation after ingestion:

```bash
python -m scripts.evaluate_retrieval
python -m scripts.evaluate_rag
python -m scripts.evaluate_llm_coverage
python -m scripts.evaluate_agent_routing
python -m scripts.evaluate_system
```

## Pre-Release Checklist

- Tests pass with Python 3.11.
- Docker image builds successfully.
- `/health`, `/ready`, and `/version` return expected values.
- Synthetic ABFS-100 data has been ingested.
- Evaluation scripts meet the quality thresholds in `src/evaluation/thresholds.py`.
- Logs include request ID, method, path, status code, and duration.
- `OPENAI_MODEL` and `APP_VERSION` are recorded for the release.

## Operational Checks

For a reported production issue:

1. Ask for the `X-Request-ID` response header.
2. Search logs for the same request ID.
3. Confirm endpoint, status code, duration, and error stack if present.
4. Check `/ready` to verify database connectivity.
5. Re-run the relevant evaluation script if the issue involves retrieval, RAG, coverage, or routing quality.

## Rollback

Redeploy the previous known-good image and keep the same database unless a migration changed schema. This project currently creates tables from SQLAlchemy models and does not include a migration system, so schema-changing releases should be handled cautiously.
