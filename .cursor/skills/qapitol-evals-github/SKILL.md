---
name: qapitol-evals-github
description: Push qapitol-evals-kit to QapitolAI via branch and PR with CI green. Use when publishing changes to GitHub.
disable-model-invocation: true
---

# qapitol-evals-github

## When to use

When pushing to `QapitolAI/qapitol-evals-kit` or opening a PR.

## Steps

1. Run `./scripts/verify-git-identity.sh` — must print `OK: git identity Qapitol <*@qapitol.com>`.
2. Run **qapitol-evals-test** first.
3. Confirm remote: `git@github.com:QapitolAI/qapitol-evals-kit.git`
4. `git status` — ensure `.plan/` is not listed (gitignored).
5. Branch: `feat/...`, `fix/...`, `chore/...`; no direct commits to protected `main` if configured.
6. Commit with **local** author only (`Qapitol` / `@qapitol.com`). **No** `Co-authored-by: Cursor` in message.
7. Before push: `git log -1 --format='%an <%ae>%n%B'` — verify author and no Cursor co-author line.
8. Push; open PR; wait for CI green.
9. Tags/releases on `main` only after merge (`v0.1.0` semver).
10. Never force-push `main`; never commit secrets.
