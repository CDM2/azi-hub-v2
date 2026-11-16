#!/bin/bash
# Runs INSIDE the jail. Every probe must fail for the jail to count as holding.
fail=0
probe() { name="$1"; shift; if "$@" >/dev/null 2>&1; then echo "LEAK  $name"; fail=1; else echo "held  $name"; fi; }
echo "whoami: $(id -un) uid=$(id -u) cwd=$(pwd)"
echo "env names: $(env | cut -d= -f1 | sort | tr '\n' ' ')"
probe "session credential in the environment (GH_TOKEN, GITHUB_*, AWS_*, ANTHROPIC_*, CLAUDE_*, CLOUDSDK_*)" sh -c 'env | cut -d= -f1 | grep -qE "^(GH_|GITHUB_|AWS_|ANTHROPIC|CLAUDE|CLOUDSDK_)|SECRET"'
probe "session home has content" sh -c 'test -n "$(ls -A /home/claude 2>/dev/null)"'
probe "read Toveli clone" cat /home/claude/toveli/README.md
probe "read azi-hub clone" cat /home/claude/azi-hub/README.md
probe "read azi-hub-v2 clone" cat /home/claude/azi-hub-v2/README.md
probe "read signing key dir" sh -c 'test -n "$(ls -A /home/claude/.ssh 2>/dev/null)"'
probe "root home has content" sh -c 'test -n "$(ls -A /root 2>/dev/null)"'
probe "host /tmp visible (marker file written outside the jail)" test -e /tmp/HOST_TMP_MARKER
probe "see a root-owned process" sh -c 'ps -eo uid= | grep -qw 0'
probe "reach credential proxy on loopback:35165" bash -c 'exec 3<>/dev/tcp/127.0.0.1/35165'
probe "reach github.com by address" bash -c 'exec 3<>/dev/tcp/140.82.112.3/443'
probe "reach api.anthropic.com by address" bash -c 'exec 3<>/dev/tcp/160.79.104.10/443'
probe "resolve a hostname" getent hosts github.com
probe "running as root" sh -c 'test "$(id -u)" = 0'
probe "write outside jail home (/srv, /etc, /usr/local)" sh -c 'touch /srv/x || touch /etc/x || touch /usr/local/x'
echo "interfaces in this namespace: $(awk -F: 'NR>2{gsub(/ /,"",$1); printf "%s ", $1}' /proc/net/dev)"
echo "processes visible: $(ls -d /proc/[0-9]* | wc -l)"
exit $fail
