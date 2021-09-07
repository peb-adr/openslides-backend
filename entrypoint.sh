#!/bin/bash

export DATASTORE_DATABASE_HOST=${DATASTORE_DATABASE_HOST:-postgresql}
export DATASTORE_DATABASE_PORT=${DATASTORE_DATABASE_PORT:-5432}
export DATASTORE_DATABASE_USER=${DATASTORE_DATABASE_USER:-openslides}
export DATASTORE_DATABASE_NAME=${DATASTORE_DATABASE_NAME:-openslides}
export DATASTORE_DATABASE_PASSWORD=${DATASTORE_DATABASE_PASSWORD:-openslides}

./wait.sh $DATASTORE_WRITER_HOST $DATASTORE_WRITER_PORT

max_retries=10
sleep_time=10

marker=/tmp/migration-in-progress

# Test if migrations are necessary and refuse to start until they have been
# applied.
while true; do
  # Detect if migrations have been started in this particular container.  If so,
  # don't do anything until they have finished.
  #
  # TODO: This is a workaround.  Ideally, migrate.py could be used to detect
  # in-progress migrations in the future.
  if [[ -e "$marker" ]]; then
    echo "INFO: Migrations in progress (${marker} exists). Waiting indefinitely."
    count=
  else
    python migrations/migrate.py stats
    python migrations/migrate.py status && break
    err_code=$?
    if [[ $err_code -eq 1 ]]; then
      echo "WARN: Migrations necessary."
    elif [[ $err_code -eq 2 ]]; then
      echo "ERROR: Migrations impossible."
    else
      echo "ERROR: Unknown error: $err_code"
      exit $err_code
    fi
    [[ $(( ++count )) -lt $max_retries ]] || exit $err_code
  fi
  sleep $sleep_time
done

exec "$@"
