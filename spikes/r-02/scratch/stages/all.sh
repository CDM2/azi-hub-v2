#!/usr/bin/env bash
# All spike stages on the scratch machine. Paperclip runs as its own unprivileged user with an empty environment.
set -uo pipefail
OUT="$1"; ROOT=$(cd "$(dirname "$0")/.." && pwd); cd "$ROOT"
PC_OLD="${PC_OLD:-2026.1023.0}"; PC_NEW="${PC_NEW:-2026.1106.0}"; NODE_V=v24.22.3
log() { echo "[$(date -u +%T)] $*"; }
keep_logs() { for f in /srv/pcwork/*.log; do [ -f "$f" ] && tail -c 60000 "$f" > "$OUT/$(basename "$f")" 2>/dev/null; done; cp /srv/pcwork/state.json "$OUT/state.json" 2>/dev/null; true; }
pub() { keep_logs 2>/dev/null; bash "$PUBLISH" "$1" || true; }
export BRAIN_URL=http://127.0.0.1:8900 BRAIN_ADMIN_TOKEN=test-admin-token-scratch
export BRAIN_OWNER_DSN=postgres://brain_owner:owner-local@127.0.0.1:5433/brain BRAIN_APP_DSN=postgres://brain_app:app-local@127.0.0.1:5433/brain
export SPIKE_WORK=/srv/pcwork PAPERCLIP_URL=http://127.0.0.1:3100
# The whole environment Paperclip and its agents get. Nothing of the runner's is passed on.
PCENV="env -i PATH=/opt/node24/bin:/usr/local/bin:/usr/bin:/bin HOME=/home/pclip USER=pclip LANG=C.UTF-8 PAPERCLIP_TELEMETRY_DISABLED=1 DO_NOT_TRACK=1 PAPERCLIP_MIGRATION_AUTO_APPLY=true"
# umask 022: Paperclip 2026.1106.0 refuses to install when its helper binary is group-writable, which a umask of 0002
# (the default for a newly created Ubuntu user) produces. Run 43795703101 recorded that failure; see results/.
PC_UMASK="${PC_UMASK:-022}"
as_pc() { sudo -u pclip -H $PCENV bash -c "cd /home/pclip; umask $PC_UMASK; $1"; }

log "stage 0: Node $NODE_V"
( cd /tmp && curl -fsSLO "https://nodejs.org/dist/$NODE_V/node-$NODE_V-linux-x64.tar.xz" && curl -fsSLO "https://nodejs.org/dist/$NODE_V/SHASUMS256.txt" \
  && grep " node-$NODE_V-linux-x64.tar.xz\$" SHASUMS256.txt | sha256sum -c - && sudo mkdir -p /opt/node24 \
  && sudo tar -xJf "node-$NODE_V-linux-x64.tar.xz" -C /opt/node24 --strip-components=1 ) || { log "node install failed"; exit 10; }
export PATH=/opt/node24/bin:$PATH; node -v

log "stage 1: permission service"
docker run -d --name brainpg -e POSTGRES_PASSWORD=pg-local -p 127.0.0.1:5433:5432 postgres:17 >/dev/null
for i in $(seq 1 60); do PGPASSWORD=pg-local psql -h 127.0.0.1 -p 5433 -U postgres -X -q -c "select 1" >/dev/null 2>&1 && break; sleep 1; done
PGPASSWORD=pg-local psql -h 127.0.0.1 -p 5433 -U postgres -X -q -c "create database brain"
PGPASSWORD=pg-local psql -h 127.0.0.1 -p 5433 -U postgres -d brain -X -q -v ON_ERROR_STOP=1 -v owner_pw=owner-local -v app_pw=app-local -f service/schema.sql || exit 11
( cd service && npm install --no-audit --no-fund >/dev/null 2>&1 && nohup node server.mjs > "$OUT/service.log" 2>&1 & )
for i in $(seq 1 30); do curl -fsS -m 2 $BRAIN_URL/healthz >/dev/null 2>&1 && break; sleep 1; done
( cd tests && python3 -m unittest test_criteria_1_3 > "$OUT/direct-tests.txt" 2>&1 ); log "direct tests: $(tail -n 1 "$OUT/direct-tests.txt") ($(grep -c -E '^Ran|ok$' "$OUT/direct-tests.txt") lines; $(grep -E '^Ran ' "$OUT/direct-tests.txt"))"; pub "stage 1"

log "stage 2: Paperclip $PC_OLD as user pclip"
sudo useradd -m -s /bin/bash pclip
sudo mkdir -p /srv/pcwork && sudo chmod 0777 /srv/pcwork && cp paperclip/agent_probe.py /srv/pcwork/ && chmod 755 /srv/pcwork/agent_probe.py
[ -f paperclip/task_agent.py ] && cp paperclip/task_agent.py /srv/pcwork/ && chmod 755 /srv/pcwork/task_agent.py
install_pc() {  # $1 = version, $2 = directory
  local tag="$1-$(basename "$2")"
  as_pc "mkdir -p $2 && cd $2 && { [ -f package.json ] || npm init -y >/dev/null; } && npm install --no-audit --no-fund paperclipai@$1" > "$OUT/install-$tag.log" 2>&1
  local rc=$?
  { echo "requested: paperclipai@$1 in $2  npm exit: $rc"
    as_pc "cd $2 && node -p \"var p=require('./node_modules/paperclipai/package.json'); 'installed ' + p.name + ' ' + p.version\""
    npm view "paperclipai@$1" dist.integrity dist.shasum gitHead 2>/dev/null
  } > "$OUT/version-$tag.txt" 2>&1
  return $rc
}
start_pc() {  # $1 = label for the log, $2 = command ("onboard --yes --no-install-service" on first start, "run" afterwards), $3 = directory
  as_pc "cd $3 && nohup npx paperclipai $2 --data-dir /home/pclip/data > /srv/pcwork/paperclip-$1.log 2>&1 < /dev/null &"
  for i in $(seq 1 180); do curl -fsS -m 2 $PAPERCLIP_URL/api/health >/dev/null 2>&1 && return 0; sleep 2; done
  return 1
}
stop_pc() { sudo pkill -u pclip -f paperclipai || true; sudo pkill -u pclip node || true; sleep 5; sudo pkill -9 -u pclip || true; sleep 2; }

PCDIR=/home/pclip/pc
install_pc "$PC_OLD" $PCDIR || { log "install failed"; keep_logs; exit 20; }
log "installed: $(tr '\n' ' ' < "$OUT/version-$PC_OLD-pc.txt" | cut -c1-400)"; pub "installed"
start_pc old "onboard --yes --no-install-service" $PCDIR || { log "Paperclip did not start"; keep_logs; exit 21; }
curl -fsS $PAPERCLIP_URL/api/health > "$OUT/health-old.json" 2>&1; log "Paperclip up: $(head -c 300 "$OUT/health-old.json")"; pub "stage 2"

log "stage 3: criteria 1 to 4 through Paperclip $PC_OLD"
python3 paperclip/harness.py setup "$OUT/old"; log "setup exit: $?"; pub "setup"
python3 paperclip/harness.py checks "$OUT/old"; RC_OLD=$?; log "checks ($PC_OLD) exit: $RC_OLD"; pub "checks old"
GOV_KEY=gov-old python3 paperclip/harness.py governance "$OUT/governance-old"; log "governance ($PC_OLD) exit: $?"; pub "governance old"

log "stage 4: upgrade Paperclip $PC_OLD -> $PC_NEW; the permission service is not touched"
SERVICE_BEFORE=$(sha256sum service/server.mjs service/schema.sql | sha256sum | cut -c1-16); SERVICE_PID_BEFORE=$(pgrep -f "node server.mjs" | head -1)
stop_pc
{ echo "umask used for the Paperclip user: $(as_pc umask)"
  as_pc "find $PCDIR/node_modules -maxdepth 4 -name copilot -type f -exec stat -c '%a %U %s %n' {} +" 2>&1 | head -5
} > "$OUT/upgrade-diagnostics.txt" 2>&1
install_pc "$PC_NEW" $PCDIR; RC_INPLACE=$?
log "in-place upgrade (npm install paperclipai@$PC_NEW over the old install): npm exit $RC_INPLACE"
if [ $RC_INPLACE -ne 0 ]; then
  PCDIR=/home/pclip/pc-new
  install_pc "$PC_NEW" $PCDIR || { log "fresh install of $PC_NEW failed too"; keep_logs; exit 30; }
  log "installed $PC_NEW into a fresh directory, keeping the data directory: $(tr '\n' ' ' < "$OUT/version-$PC_NEW-pc-new.txt" | cut -c1-300)"
fi
pub "upgrade installed"
start_pc new "run" $PCDIR || { log "Paperclip $PC_NEW did not start"; keep_logs; exit 31; }
curl -fsS $PAPERCLIP_URL/api/health > "$OUT/health-new.json" 2>&1; log "Paperclip up after upgrade: $(head -c 300 "$OUT/health-new.json")"
python3 paperclip/harness.py checks "$OUT/new"; RC_NEW=$?; log "checks ($PC_NEW) exit: $RC_NEW"; pub "checks new"
SERVICE_AFTER=$(sha256sum service/server.mjs service/schema.sql | sha256sum | cut -c1-16); SERVICE_PID_AFTER=$(pgrep -f "node server.mjs" | head -1)
{ echo "in-place npm upgrade exit: $RC_INPLACE; final install directory: $PCDIR"
  echo "service files digest before/after: $SERVICE_BEFORE / $SERVICE_AFTER; service process before/after: $SERVICE_PID_BEFORE / $SERVICE_PID_AFTER (same process means it was never restarted)"
} > "$OUT/upgrade.txt"
GOV_KEY=gov-new python3 paperclip/harness.py governance "$OUT/governance-new"; log "governance ($PC_NEW) exit: $?"; pub "governance new"

log "stage 5: criterion 5 (one model-driven task through the stack, and the same task on one plain agent)"
if [ -f paperclip/task_run.py ]; then python3 paperclip/task_run.py "$OUT/task"; log "criterion 5 exit: $?"; else log "criterion 5: no task runner in this revision"; fi
keep_logs
log "done: old=$RC_OLD new=$RC_NEW"
