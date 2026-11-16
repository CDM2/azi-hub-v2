#!/usr/bin/env bash
# Copy the run's output (text only, size-capped) to the results branch and push it.
set -uo pipefail
R=/tmp/results-repo; D="$R/results/$RUN_ID"
rm -rf "$D"; mkdir -p "$D"; cp -r "$OUT/." "$D/" 2>/dev/null
find "$D" -type f -size +700k -exec sh -c 'tail -c 700000 "$1" > "$1.cut" && mv "$1.cut" "$1"' _ {} \;
cd "$R" && git add -A "results/$RUN_ID" >/dev/null 2>&1 && git commit -qm "results: run $RUN_ID ($1)" >/dev/null 2>&1
for i in 1 2 3; do
  git push -q origin results 2>/dev/null && exit 0
  git pull -q --rebase origin results 2>/dev/null || true
done
exit 0
