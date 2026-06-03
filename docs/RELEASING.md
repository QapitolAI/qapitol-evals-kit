# Releasing qapitol-evals-kit (Phase 3 — PyPI)

This repo publishes to **TestPyPI** (manual) and **PyPI** (on `v*` tags) via [Trusted Publishing](https://docs.pypi.org/trusted-publishers/). No API tokens are stored in GitHub secrets.

## One-time setup (maintainer)

### 1. Register the project on PyPI

1. Create accounts on [pypi.org](https://pypi.org) and [test.pypi.org](https://test.pypi.org) if needed.
2. Register the project name **`qapitol-evals-kit`** on production PyPI (claim early if the name is free).

### 2. Add Trusted Publishers

For **each** index (TestPyPI and PyPI), open the project → **Publishing** → **Add a new trusted publisher**:

| Field | Value |
|-------|--------|
| Owner | `QapitolAI` |
| Repository | `qapitol-evals-kit` |
| Workflow name | `release.yml` |
| Environment name | `testpypi` (TestPyPI) or `pypi` (production) |

Use the exact environment names — they must match [`.github/workflows/release.yml`](../.github/workflows/release.yml).

### 3. GitHub environments (optional but recommended)

In **Settings → Environments**, create:

- **`testpypi`** — no protection rules required for dry runs.
- **`pypi`** — add required reviewers if you want a manual gate before production publish.

The workflow binds publish jobs to these environment names.

## Publish flow

### TestPyPI (recommended first)

1. Merge release workflow to `main`.
2. **Actions → Release → Run workflow** → target **testpypi**.
3. Install and smoke-test:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ qapitol-evals-kit==0.1.0
qapitol-evals doctor
```

### Production PyPI

1. Ensure `version` in `pyproject.toml` matches the tag (e.g. `0.1.0` ↔ tag `v0.1.0`).
2. Tag on `main` after CI is green:

```bash
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0
```

3. The **Release** workflow builds, verifies tag ↔ version, and publishes to PyPI.

Re-publishing the same version will fail on PyPI (immutable). Bump `pyproject.toml` for fixes (`0.1.1`, etc.).

### Manual production publish (emergency)

**Actions → Release → Run workflow** → target **pypi** (uses the `pypi` environment; same Trusted Publisher rules apply).

## Version checklist

- [ ] `pyproject.toml` `version` bumped
- [ ] `ruff check` + `pytest` pass locally
- [ ] CI green on `main`
- [ ] Tag `vX.Y.Z` matches version
- [ ] TestPyPI install smoke (first time or after packaging changes)
- [ ] GitHub Release notes updated (optional)

## Install URLs after publish

```bash
pip install qapitol-evals-kit==0.1.0
pip install "qapitol-evals-kit[all]==0.1.0"
```

Git install remains documented in README as a fallback.
