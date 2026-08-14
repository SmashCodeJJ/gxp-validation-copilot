#!/bin/sh

set -e

echo "Creating database tables..."

python -m scripts.create_tables

echo "Starting FastAPI..."

exec uvicorn \
    src.api.main:app \
    --host 0.0.0.0 \
    --port 8000