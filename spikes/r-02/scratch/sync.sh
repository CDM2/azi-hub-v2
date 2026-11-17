#!/bin/bash
# Copy the spike's own code into a clone of the scratch repository. Nothing from Toveli is copied.
set -euo pipefail
R02=$(cd "$(dirname "$0")/.." && pwd); DEST="${1:?path to the scratch repository clone}"
mkdir -p "$DEST/.github/workflows" "$DEST/stages"
cp "$R02/scratch/workflow-spike.yml" "$DEST/.github/workflows/spike.yml"
cp "$R02/scratch/run.sh" "$DEST/run.sh"; cp "$R02/scratch/publish.sh" "$DEST/publish.sh"; cp "$R02/scratch/stages/all.sh" "$DEST/stages/all.sh"
rm -rf "$DEST/service" "$DEST/tests" "$DEST/paperclip"
cp -r "$R02/service" "$R02/tests" "$R02/paperclip" "$DEST/"
find "$DEST" -name __pycache__ -prune -exec rm -rf {} \; ; rm -rf "$DEST/service/node_modules"
