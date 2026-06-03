#!/usr/bin/env bash
# Verify repo-local git identity before commit/push (Qapitol only, no personal email).
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${ROOT}" ]]; then
  echo "FAIL: not inside a git repository"
  exit 1
fi
cd "${ROOT}"

NAME="$(git config --local user.name || true)"
EMAIL="$(git config --local user.email || true)"

if [[ -z "${NAME}" || -z "${EMAIL}" ]]; then
  echo "FAIL: missing local git user.name or user.email"
  echo "  Set: git config --local user.name \"Qapitol\""
  echo "       git config --local user.email \"you@qapitol.com\""
  exit 1
fi

if [[ "${NAME}" != "Qapitol" ]]; then
  echo "FAIL: local user.name is '${NAME}', expected 'Qapitol'"
  exit 1
fi

if [[ "${EMAIL}" != *@qapitol.com ]]; then
  echo "FAIL: local user.email is '${EMAIL}', expected *@qapitol.com"
  exit 1
fi

GLOBAL_EMAIL="$(git config --global user.email || true)"
if [[ -n "${GLOBAL_EMAIL}" && "${GLOBAL_EMAIL}" == *@gmail.com* ]]; then
  echo "NOTE: global email is personal (${GLOBAL_EMAIL}); local overrides apply for commits in this repo."
fi

# Block push if HEAD has Cursor co-author (IDE-injected trailer)
if git rev-parse HEAD >/dev/null 2>&1; then
  BODY="$(git log -1 --format=%B)"
  if echo "${BODY}" | grep -qi 'Co-authored-by: Cursor'; then
    echo "FAIL: HEAD commit contains 'Co-authored-by: Cursor'"
    echo "  Fix: ./scripts/install-git-hooks.sh then: git commit --amend -F .git/COMMIT_EDITMSG_CLEAN --no-verify"
    echo "  Or amend in terminal (not Cursor agent) and remove the Co-authored-by line."
    echo "  Cursor: disable agent commit co-author / attribution in Cursor Settings if available."
    exit 1
  fi
fi

echo "OK: git identity ${NAME} <${EMAIL}>"
