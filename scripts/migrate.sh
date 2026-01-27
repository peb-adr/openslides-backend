#!/bin/bash

# DON'T MERGE ME INTO MAIN
# I AM ONLY DOING UGLY THINGS

export DATABASE_HOST=${DATABASE_HOST:-postgres}
export DATABASE_PORT=${DATABASE_PORT:-5432}
export DATABASE_USER=${DATABASE_USER:-openslides}
export DATABASE_NAME=${DATABASE_NAME:-openslides}
export DATABASE_PASSWORD_FILE=${DATABASE_PASSWORD_FILE:-/run/secrets/postgres_password}
export PGPASSWORD="$(cat "$DATABASE_PASSWORD_FILE")"

python3 /app/openslides_backend/migrations/migrate.py "$@"
