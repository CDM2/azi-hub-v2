#!/usr/bin/env bash
# REV-01 fix pass: run every test and measurement against the fixed permission service in ./service.
#
# Needs: a local PostgreSQL you may create a database in (a superuser DSN), psql, Node 22 or newer, Python 3.
# Nothing third-party runs except PostgreSQL and the service's one dependency (the `pg` driver, 8.23.1).
# The service's files are copied to a scratch directory and run from there. Made-up data only.
#
#   SUPER_DSN=postgres://postgres:...@127.0.0.1:5432/brain  ./run.sh [results-directory]
#
# The database named in SUPER_DSN must exist and is wiped: the schema "brain" is dropped and recreated several times.
# SKIP_SWEEP=1 leaves out the mutation sweep, which takes about 35 minutes; everything else takes about 5.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); OUT="${1:-$HERE/results}"; mkdir -p "$OUT"
: "${SUPER_DSN:?set SUPER_DSN to a superuser connection string for a throwaway database}"
HOSTPORT=$(python3 -c "import sys,urllib.parse as u; p=u.urlparse(sys.argv[1]); print(f'{p.hostname}:{p.port or 5432}{p.path}')" "$SUPER_DSN")
export SUPER_DSN OWNER_PW="${OWNER_PW:-rev01-owner-pw}" APP_PW="${APP_PW:-rev01-app-pw}"
export BRAIN_URL="http://127.0.0.1:${PORT:-8900}" BRAIN_ADMIN_TOKEN="${BRAIN_ADMIN_TOKEN:-rev01-admin-token-0123456789abcdef}"
export BRAIN_APP_DSN="postgres://brain_app:$APP_PW@$HOSTPORT" BRAIN_OWNER_DSN="postgres://brain_owner:$OWNER_PW@$HOSTPORT" PYTHONDONTWRITEBYTECODE=1
WORK=$(mktemp -d); SVC=""
trap '[ -n "$SVC" ] && kill $SVC 2>/dev/null; psql "$SUPER_DSN" -X -q -c "alter role brain_app reset plan_cache_mode" >/dev/null 2>&1; rm -rf "$WORK"' EXIT
start() {   # (re)start the service from the scratch directory; a restart gives it new database connections
  [ -n "$SVC" ] && { kill $SVC 2>/dev/null; wait $SVC 2>/dev/null; }
  (cd "$WORK" && PORT="${PORT:-8900}" exec node server.mjs >> "$OUT/service.log" 2>&1) & SVC=$!
  for i in $(seq 1 50); do curl -fsS -m 2 "$BRAIN_URL/healthz" >/dev/null 2>&1 && return 0; sleep 0.2; done; echo "the service did not start"; exit 13
}
load() { psql "$SUPER_DSN" -X -q -v ON_ERROR_STOP=1 -v owner_pw="$OWNER_PW" -v app_pw="$APP_PW" -f "$HERE/service/schema.sql" >/dev/null 2>"$WORK/load.err" || { cat "$WORK/load.err"; exit 11; }; }

# 1. The comparison figure first, on R-02's own schema, before the fixed schema replaces it.
cd "$HERE" && python3 measure.py baseline-db > "$OUT/timing-in-database.txt" 2>&1 || { echo "baseline measurement failed"; tail -n 3 "$OUT/timing-in-database.txt"; }

# 2. The fixed schema and service.
load
cp "$HERE/service/server.mjs" "$HERE/service/package.json" "$WORK/" && (cd "$WORK" && npm install --no-audit --no-fund >/dev/null 2>&1) || exit 12
: > "$OUT/service.log"; start
{ echo "# $(date -u +%FT%TZ)  $(psql "$SUPER_DSN" -X -q -A -t -c 'show server_version')  node $(node -v)  python $(python3 -V 2>&1 | cut -d' ' -f2)"
  echo "# service files: $(cd "$HERE/service" && sha256sum server.mjs schema.sql | tr '\n' ' ')"; } > "$OUT/environment.txt"

# 3. The tests. A line "OK (expected failures=N)" counts the known limits, which are tests kept failing on purpose.
cd "$HERE/tests"
python3 -m unittest -v test_criteria_1_3        > "$OUT/tests-r02-original-35.txt" 2>&1;   echo "R-02's 35 tests:        $(tail -n 1 "$OUT/tests-r02-original-35.txt")"
python3 -m unittest -v test_rev01_attacks       > "$OUT/tests-review-attacks.txt" 2>&1;    echo "review, attacks:        $(tail -n 1 "$OUT/tests-review-attacks.txt")"
python3 -m unittest -v test_rev01_second_person > "$OUT/tests-review-second-person.txt" 2>&1; echo "review, second person:  $(tail -n 1 "$OUT/tests-review-second-person.txt")"
python3 -m unittest -v test_fix_new_rules       > "$OUT/tests-new-rules.txt" 2>&1;         echo "new rules:              $(tail -n 1 "$OUT/tests-new-rules.txt")"

# 3b. The same tests twice more, with PostgreSQL forced into each of its two ways of planning a statement. Left alone it plans a
# statement afresh the first five times a connection runs it and may then keep one plan, and the two behave differently for the
# timing and scale findings. A run that passes only in one mode would be a finding.
for mode in force_generic_plan force_custom_plan; do
  psql "$SUPER_DSN" -X -q -c "alter role brain_app set plan_cache_mode = $mode" && start
  python3 -m unittest test_criteria_1_3 test_rev01_attacks test_rev01_second_person test_fix_new_rules > "$OUT/tests-all-$mode.txt" 2>&1
  echo "all tests, $mode: $(tail -n 1 "$OUT/tests-all-$mode.txt")"
done
psql "$SUPER_DSN" -X -q -c "alter role brain_app reset plan_cache_mode" && start

# 4. The measurements.
cd "$HERE"
python3 measure.py matrix > "$OUT/second-person-matrix.txt" 2>&1
python3 measure.py timing > "$OUT/timing.txt" 2>&1
{ echo; python3 measure.py timing-db; } >> "$OUT/timing-in-database.txt" 2>&1
python3 measure.py scale  > "$OUT/scale.txt" 2>&1

# 5. How the database runs a search: the read rule first (the inner scan), the search text after (the outer filter).
psql "$SUPER_DSN" -X -q -A -t > "$OUT/plan-of-a-search.txt" 2>&1 <<'SQL'
set enable_seqscan = off;
explain (costs off) select count(*) from (select * from brain.visible_pages_(row(1, 1, 'toveli', 'sub', 'agent', null, '{toveli}', '{}', '{mgmt}', true, '{}')::brain.sessions) offset 0) p
 where p.title ilike '%x%' or p.body ilike '%x%' or p.path ilike '%x%';
SQL

# 6. The log's chain, checked over every row the tests and measurements above wrote.
curl -fsS -m 60 -H "Authorization: Bearer $BRAIN_ADMIN_TOKEN" "$BRAIN_URL/admin/audit_verify" > "$OUT/log-chain.txt" 2>&1; echo "log chain:              $(cat "$OUT/log-chain.txt")"

# 7. The mutation sweep, on its own copy of the service. It loads the fixed schema again when it is done.
if [ "${SKIP_SWEEP:-0}" = "1" ]; then echo "mutation sweep:         SKIPPED (SKIP_SWEEP=1), so NOT RUN in this run"
else SERVICE_DIR="$WORK" SWEEP_PORT=$(( ${PORT:-8900} + 11 )) python3 mutation_sweep.py > "$OUT/mutation-sweep.txt" 2>&1; echo "mutation sweep:         $(tail -n 1 "$OUT/mutation-sweep.txt")"; fi
echo "results in $OUT"
