# AGENTS.md

Guidance for cloud agents and developers working in this repository.

## Repository overview

This is a **documentation-only** repository for the Kidney Care Analytics Platform. It contains architecture specifications, domain models, KPIs, and implementation roadmaps in Markdown under `docs/`. There is no application code, database, or runtime services to deploy from this repo.

## Cursor Cloud specific instructions

### Services

| Service | Required | Port | Notes |
|---------|----------|------|-------|
| Docs preview server (`npm run serve`) | Optional | 8080 | Static file server for browsing Markdown locally. No backend or database. |

There are no ETL pipelines, warehouses, or BI dashboards implemented in this repository. End-to-end platform testing requires separate implementation repos.

### Development commands

All commands run from the repository root after `npm install`:

| Command | Purpose |
|---------|---------|
| `npm run lint` | Markdown lint on `README.md` and `docs/**/*.md` |
| `npm run check-links` | Verify internal Markdown links resolve to existing files |
| `npm run validate` | Run lint + link checks (use as the pre-commit sanity check) |
| `npm run serve` | Start static docs preview at http://localhost:8080 |

### Lint configuration

Markdown linting uses `.markdownlint.json` with relaxed stylistic rules so existing documentation passes without reformatting. The lint scope intentionally excludes `node_modules/`.

### Gotchas

- The `serve` package exposes a directory listing at `/` and serves raw `.md` files (not rendered HTML). This is expected for a lightweight preview.
- `scripts/check-links.mjs` uses Node's experimental `globSync`; a warning on stderr is harmless.
- No `.env` file or secrets are required for documentation work.
