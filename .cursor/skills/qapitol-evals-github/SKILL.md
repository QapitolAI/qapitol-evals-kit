---
name: qapitol-evals-github
description: Push qapitol-evals-kit to QapitolAI via branch and PR with CI green. Use when publishing changes to GitHub.
disable-model-invocation: true
---

# qapitol-evals-github

## When to use

When pushing to `QapitolAI/qapitol-evals-kit` or opening a PR.

## Steps

1. Run **qapitol-evals-test** first.
2. Confirm remote: `git@github.com:QapitolAI/qapitol-evals-kit.git`
3. `git status` — ensure `.plan/` is not listed (gitignored).
4. Branch: `feat/...`, `fix/...`, `chore/...`; no direct commits to protected `main` if configured.
5. Conventional commit message; push; open PR; wait for CI green.
6. Tags/releases on `main` only after merge (`v0.1.0` semver).
7. Never force-push `main`; never commit secrets.
