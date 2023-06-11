#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

POSTGRES_DB_VAR=$(<$POSTGRES_DB)
POSTGRES_USER_VAR=$(<POSTGRES_USER)
POSTGRES_PASSWORD_VAR=$(<POSTGRES_PASSWORD)

if [ -z "${POSTGRES_USER_VAR}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER_VAR="${base_postgres_image_default_user}"
fi

postgres_ready() {
python << END
import psycopg2
import sys

try:
    psycopg2.connect(
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
        dbname="${POSTGRES_DB_VAR}",
        user="${POSTGRES_USER_VAR}",
        password="${POSTGRES_PASSWORD}"
    )
except psycopg2.OperationalError:
    sys.exit(-1)

sys.exit(0)

END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

exec "$@"
