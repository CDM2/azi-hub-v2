#!/bin/bash
# Runs OUTSIDE the jail, as root. Copies the spike's own code in, then starts one long-lived jail session.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); R02=$(dirname "$HERE")
mkdir -p /srv/spike/work && rm -rf /srv/spike/work/{service,tests,qa,mapper,jail}
cp -r "$R02"/{service,tests,qa,mapper,jail} /srv/spike/work/ 2>/dev/null || true
chown -R spike:spike /srv/spike/work
rm -f /srv/spike/run/ready
nohup "$HERE/jail.sh" bash /srv/spike/work/jail/session.sh > /tmp/jail-session.log 2>&1 &
echo $! > /tmp/jail-session.pid
for i in $(seq 1 60); do [ -f /srv/spike/run/ready ] && break; sleep 1; done
cat /srv/spike/run/ready 2>/dev/null || { echo "jail session did not come up"; tail -n 5 /tmp/jail-session.log /srv/spike/logs/*.log; exit 1; }
