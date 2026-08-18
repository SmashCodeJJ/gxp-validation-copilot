#!/bin/sh

set -e

echo "Creating database tables..."

python -m scripts.create_tables

echo "Starting FastAPI..."

exec uvicorn \
    src.api.main:app \
    --host "${API_HOST:-0.0.0.0}" \
    --port "${API_PORT:-8000}" \
    --workers "${API_WORKERS:-1}"
