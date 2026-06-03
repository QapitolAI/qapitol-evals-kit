#!/usr/bin/env bash
# Install repo git hooks (removes Cursor co-author from commit messages).
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="${ROOT}/.git/hooks"
mkdir -p "${HOOKS_DIR}"
install -m 755 "${ROOT}/scripts/git-hooks/prepare-commit-msg" "${HOOKS_DIR}/prepare-commit-msg"
echo "Installed ${HOOKS_DIR}/prepare-commit-msg"
