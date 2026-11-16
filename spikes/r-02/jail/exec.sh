#!/bin/bash
# Runs OUTSIDE the jail, as root: run a command inside the already-running jail session, as the unprivileged user.
set -euo pipefail
OUTER=$(cat /tmp/jail-session.pid)
INNER=$(pgrep -P "$OUTER" | head -1)   # the first process inside the jail's namespaces
exec nsenter -t "$INNER" --net --pid --ipc --uts --mount -- \
  setpriv --reuid=2000 --regid=2000 --clear-groups --no-new-privs \
  env -i PATH=/opt/node22/bin:/usr/local/bin:/usr/bin:/bin HOME=/srv/spike USER=spike LANG=C.UTF-8 \
      PGHOST=127.0.0.1 PGPORT=5433 BRAIN_URL=http://127.0.0.1:8900 BRAIN_ADMIN_TOKEN=test-admin-token-local \
      BRAIN_APP_DSN=postgres://brain_app:app-local@127.0.0.1:5433/brain "$@"
