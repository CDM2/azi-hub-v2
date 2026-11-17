#!/usr/bin/env bash
# REV-01: run the review's tests and measurements against the unmodified permission service.
#
# Needs: a local PostgreSQL you may create a database in (a superuser DSN), psql, Node 22 or newer, Python 3.
# Nothing third-party runs except PostgreSQL and the service's one dependency (the `pg` driver, 8.23.1).
# The service's files are copied to a scratch directory and run from there; nothing under ../service changes.
#
#   SUPER_DSN=postgres://postgres:...@127.0.0.1:5432/brain  ./run.sh [results-directory]
#
# The database named in SUPER_DSN must exist and is wiped: schema.sql drops and recreates the schema "brain".
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); SPIKE=$(dirname "$HERE"); OUT="${1:-$HERE/results}"; mkdir -p "$OUT"
: "${SUPER_DSN:?set SUPER_DSN to a superuser connection string for a throwaway database}"
HOSTPORT=$(python3 -c "import sys,urllib.parse as u; p=u.urlparse(sys.argv[1]); print(f'{p.hostname}:{p.port or 5432}{p.path}')" "$SUPER_DSN")
export OWNER_PW="${OWNER_PW:-rev01-owner-pw}" APP_PW="${APP_PW:-rev01-app-pw}"
export BRAIN_URL="http://127.0.0.1:${PORT:-8900}" BRAIN_ADMIN_TOKEN="${BRAIN_ADMIN_TOKEN:-rev01-admin-token-0123456789abcdef}"
export BRAIN_APP_DSN="postgres://brain_app:$APP_PW@$HOSTPORT" BRAIN_OWNER_DSN="postgres://brain_owner:$OWNER_PW@$HOSTPORT" PYTHONDONTWRITEBYTECODE=1
WORK=$(mktemp -d); trap 'kill $SVC 2>/dev/null; rm -rf "$WORK"' EXIT
psql "$SUPER_DSN" -X -q -v ON_ERROR_STOP=1 -v owner_pw="$OWNER_PW" -v app_pw="$APP_PW" -f "$SPIKE/service/schema.sql" >/dev/null || exit 11
cp "$SPIKE/service/server.mjs" "$SPIKE/service/package.json" "$WORK/" && (cd "$WORK" && npm install --no-audit --no-fund >/dev/null 2>&1) || exit 12
(cd "$WORK" && PORT="${PORT:-8900}" node server.mjs > "$OUT/service.log" 2>&1) & SVC=$!
for i in $(seq 1 50); do curl -fsS -m 2 "$BRAIN_URL/healthz" >/dev/null 2>&1 && break; sleep 0.2; done
{ echo "# $(date -u +%FT%TZ)  $(psql "$SUPER_DSN" -X -q -A -t -c 'show server_version')  node $(node -v)  python $(python3 -V 2>&1 | cut -d' ' -f2)"
  echo "# service files: $(cd "$SPIKE/service" && sha256sum server.mjs schema.sql | tr '\n' ' ')"; } > "$OUT/environment.txt"
cd "$SPIKE/tests" && python3 -m unittest test_criteria_1_3 > "$OUT/existing-35-tests.txt" 2>&1; echo "existing tests: $(tail -n 1 "$OUT/existing-35-tests.txt")"
cd "$HERE"
python3 -m unittest -v test_rev01_attacks > "$OUT/review-attacks.txt" 2>&1;             echo "attack tests:   $(tail -n 1 "$OUT/review-attacks.txt")"
python3 -m unittest -v test_rev01_second_person > "$OUT/review-second-person.txt" 2>&1; echo "second person:  $(tail -n 1 "$OUT/review-second-person.txt")"
python3 measure.py matrix > "$OUT/second-person-matrix.txt" 2>&1
python3 measure.py timing > "$OUT/timing.txt" 2>&1
python3 measure.py scale  > "$OUT/scale.txt" 2>&1
python3 mutation_sweep.py > "$OUT/mutation-sweep.txt" 2>&1;                            echo "mutation sweep: $(tail -n 1 "$OUT/mutation-sweep.txt")"
psql "$SUPER_DSN" -X -q -v ON_ERROR_STOP=1 -v owner_pw="$OWNER_PW" -v app_pw="$APP_PW" -f "$SPIKE/service/schema.sql" >/dev/null
echo "results in $OUT"
