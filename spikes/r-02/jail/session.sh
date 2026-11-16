#!/bin/bash
# Runs INSIDE the jail as the unprivileged user. Starts Postgres and the permission service, then waits.
set -euo pipefail
PG=/srv/spike/pgpkg/node_modules/@embedded-postgres/linux-x64
PGBIN=$PG/native/bin
mkdir -p /srv/spike/logs /srv/spike/run
( cd "$PG" && node scripts/hydrate-symlinks.js ) > /srv/spike/logs/hydrate.log 2>&1 || true
if [ ! -s /srv/spike/pgdata/PG_VERSION ]; then
  "$PGBIN/initdb" -D /srv/spike/pgdata -U postgres -A trust --locale=C -E UTF8 > /srv/spike/logs/initdb.log 2>&1
fi
"$PGBIN/pg_ctl" -D /srv/spike/pgdata -o "-p 5433 -c listen_addresses=127.0.0.1 -c unix_socket_directories=/tmp" -l /srv/spike/logs/pg.log -w start > /srv/spike/logs/pg_ctl.log 2>&1
export PGHOST=127.0.0.1 PGPORT=5433
psql -U postgres -X -q -c "select 1 from pg_database where datname='brain'" -A -t | grep -q 1 || psql -U postgres -X -q -c "create database brain"
psql -U postgres -d brain -X -q -v ON_ERROR_STOP=1 -v owner_pw=owner-local -v app_pw=app-local -f /srv/spike/work/service/schema.sql > /srv/spike/logs/schema.log 2>&1
export BRAIN_ADMIN_TOKEN=test-admin-token-local
export BRAIN_OWNER_DSN=postgres://brain_owner:owner-local@127.0.0.1:5433/brain
export BRAIN_APP_DSN=postgres://brain_app:app-local@127.0.0.1:5433/brain
export PORT=8900 LISTEN_SOCKET=/srv/spike/run/brain.sock NODE_PATH=/srv/spike/app/node_modules
cd /srv/spike/app && cp /srv/spike/work/service/server.mjs . && node server.mjs > /srv/spike/logs/service.log 2>&1 &
echo "session up" > /srv/spike/run/ready
exec sleep infinity
