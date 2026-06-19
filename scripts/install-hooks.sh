#!/usr/bin/env bash
#
# Install the Maxalding QA gate as a git pre-commit hook.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SRC="$REPO_ROOT/hooks/pre-commit"
DEST="$REPO_ROOT/.git/hooks/pre-commit"

if [ ! -f "$SRC" ]; then
  echo "Cannot find hooks/pre-commit at $SRC"
  exit 1
fi

cp "$SRC" "$DEST"
chmod +x "$DEST"
echo "Installed pre-commit hook to $DEST"
