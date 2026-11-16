#!/bin/bash
# Run a command in the spike jail. Usage: jail.sh <command...>
# Boundary: new network namespace (loopback only, so the session's credential
# proxy and the internet are unreachable), new PID, IPC, UTS and mount
# namespaces, empty tmpfs mounted over the session's home, root's home and /tmp,
# an empty environment, an unprivileged user, and no-new-privs.
set -euo pipefail
JAIL_HOME=${JAIL_HOME:-/srv/spike}
exec unshare --net --pid --fork --ipc --uts --mount --mount-proc --propagation private \
  /bin/bash -c '
    set -e
    ip link set lo up 2>/dev/null || true
    mount -t tmpfs -o mode=0700 tmpfs /home/claude
    mount -t tmpfs -o mode=0700 tmpfs /root
    mount -t tmpfs -o mode=1777 tmpfs /tmp
    mount -t sysfs sysfs /sys 2>/dev/null || true
    cd "$0"
    exec setpriv --reuid=2000 --regid=2000 --clear-groups --no-new-privs \
      env -i PATH=/srv/spike/node/bin:/usr/local/bin:/usr/bin:/bin HOME="$0" USER=spike LANG=C.UTF-8 \
      "$@"
  ' "$JAIL_HOME" "$@"
