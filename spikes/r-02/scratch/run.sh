#!/usr/bin/env bash
# Entry point for one spike run on the scratch machine. Results go to results/<run>/ on the "results" branch,
# published after every stage so a run that stops early still leaves its evidence.
set -uo pipefail
chmod 700 "$PWD"                       # this clone holds the scratch repository's token; keep other users out
export RUN_ID="${GITHUB_RUN_ID:-local}-${GITHUB_RUN_ATTEMPT:-0}"
export OUT="$PWD/out/$RUN_ID"; mkdir -p "$OUT"
export PUBLISH="$PWD/publish.sh"
{
  echo "run: $RUN_ID  commit: $(git rev-parse HEAD)  date: $(date -u +%FT%TZ)"
  echo "runner: $(uname -srm)  cpus: $(nproc)  mem: $(free -g | awk '/Mem:/{print $2}')G"
  echo "model key present: $([ -n "${SPIKE_MODEL_KEY:-}" ] && echo yes || echo no)"
} > "$OUT/environment.txt" 2>&1
git clone -q --depth 1 --branch results "$(git remote get-url origin)" /tmp/results-repo 2>/dev/null \
  || { git init -q /tmp/results-repo && git -C /tmp/results-repo remote add origin "$(git remote get-url origin)" && git -C /tmp/results-repo checkout -q --orphan results; }
chmod 700 /tmp/results-repo
git -C /tmp/results-repo config user.name "spike-runner"; git -C /tmp/results-repo config user.email "spike-runner@users.noreply.github.com"
bash "$PUBLISH" "started"
bash stages/all.sh "$OUT" > "$OUT/stages.log" 2>&1
echo "stages exit: $?" >> "$OUT/environment.txt"
bash "$PUBLISH" "finished"
