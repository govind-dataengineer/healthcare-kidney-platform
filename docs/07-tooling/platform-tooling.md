# Platform Tooling Requirements

## Status

| Field | Value |
|-------|-------|
| **Document owner** | Platform team |
| **Status** | Draft — living document |
| **Review cadence** | Daily, ~1 hour stand-up to advance decisions and implementation |
| **Last updated** | 2026-08-03 |
| **Related docs** | [Architecture Principles](../02-architecture/principles.md), [Dimensional Model](../02-architecture/dimensional-model.md), [PD Domain Model](../06-implementation/pd-domain-model.md), [Phased Implementation](../06-implementation/phased-approach.md) |

---

## Purpose

This document defines the **Phase 1 data platform tooling** for the Kidney Care Analytics Platform: how raw data lands, how it is ingested into the warehouse, how dbt transforms and validates it, and how CI/CD enforces quality.

It is a **living requirements document**. Open decisions are tracked explicitly and resolved during daily review sessions.

---

## Architecture Overview

```text
┌─────────────────────┐
│  Mock Source        │  External system — we do not control it
│  (Python producer)  │
└──────────┬──────────┘
           │ files (Parquet)
           ▼
┌─────────────────────┐
│  MinIO              │  S3-compatible landing zone (dev)
│  (landing bucket)   │  → AWS S3 in QA/PROD (future)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Ingest Script      │  Platform-owned Python loader
│  (Python)           │  MinIO → PostgreSQL raw schema
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  PostgreSQL         │  Warehouse (Docker for dev)
│  raw → staging →    │
│  marts              │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  dbt                │  Transform, DQ tests, docs, lineage
│  (orchestrator for  │  Runs after ingest completes
│   warehouse layer)  │
└─────────────────────┘
```

### Responsibility boundaries

| Component | Owns | Does not own |
|-----------|------|--------------|
| **Mock source** | Generating and delivering files to landing zone | Warehouse schema, business rules, DQ |
| **MinIO / S3** | Durable raw file storage | Transformations, relational modeling |
| **Ingest script** | Reading landing files, loading `raw.*` tables, ingest logging | Cleansing, joins, dims/facts |
| **dbt** | `raw` → `staging` → `marts`, DQ tests, documentation | S3 → Postgres load, mock data generation |
| **GitHub Actions** | CI/CD pipeline orchestration across all steps | Runtime business logic |

### Orchestration model

**End-to-end pipeline** (full path):

```text
mock producer  →  MinIO  →  Python ingest  →  PostgreSQL (raw)  →  dbt build  →  marts + tests
```

**dbt scope:** dbt orchestrates everything **inside PostgreSQL** after raw data is loaded — model DAG, incremental runs, DQ tests, and docs. A thin runner (shell script, Makefile, Docker Compose, or GitHub Actions) chains ingest → dbt for full end-to-end execution.

---

## 1. Landing Zone — MinIO (S3-compatible)

### Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| LZ-01 | Use MinIO for local/dev landing zone with S3-compatible API | **Decided** |
| LZ-02 | Use same path conventions as future AWS S3 (swap endpoint via config) | **Decided** |
| LZ-03 | Landing files are immutable and append-only | **Decided** |
| LZ-04 | Preferred file format is **Parquet** (typed, compressed) | **Proposed** |
| LZ-05 | Separate buckets or prefixes per environment (`dev`, `qa`, `prod`) | **Open** |

### Path convention

```text
s3://{bucket}/landing/{source_system}/{entity}/dt=YYYY-MM-DD/part-0001.parquet
```

**Example:**

```text
s3://kidney-landing/landing/pd_clinic/pd_exchange/dt=2026-08-03/part-0001.parquet
s3://kidney-landing/landing/lab_system/lab_result/dt=2026-08-03/part-0001.parquet
s3://kidney-landing/landing/ehr/patient/dt=2026-08-03/part-0001.parquet
```

### Access model

| Actor | Permission |
|-------|------------|
| Mock producer | Write to `landing/` prefix only |
| Ingest script | Read from `landing/` prefix only |
| dbt | No direct S3 access (reads Postgres only) |

---

## 2. Mock Source System (External)

### Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| MS-01 | Python application simulates external EHR / lab / clinic feeds | **Decided** |
| MS-02 | Treated as a **black box** — platform has no control over its logic | **Decided** |
| MS-03 | Delivers files to MinIO landing zone per data contract | **Decided** |
| MS-04 | May run locally or in Docker (decision deferred) | **Open** |
| MS-05 | Each feed has a documented **data contract** (schema, cadence, naming) | **Open** |

### Phase 1 source systems (proposed)

| Source system | Entities | Aligns to CDM |
|---------------|----------|---------------|
| `ehr` | `patient`, `provider`, `facility` | Core dimensions |
| `pd_clinic` | `pd_exchange`, `peritonitis_event` | PD domain model |
| `lab_system` | `lab_result` | `fct_lab_result` |

### Data contract template (per entity)

Each entity contract must define:

- Entity name and source system
- File format (Parquet) and compression
- Column names, types, nullability
- Primary / natural keys
- Delivery cadence (batch daily, hourly, etc.)
- Partition key (`dt=YYYY-MM-DD`)
- Sample file location for dev/CI

**Contracts to write:** see [Open decisions](#open-decisions) below.

---

## 3. Ingest Script (Python)

### Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| IN-01 | Custom Python script loads landing files into PostgreSQL `raw` schema | **Decided** |
| IN-02 | Uses `boto3` against MinIO (S3-compatible endpoint) | **Decided** |
| IN-03 | Reads Parquet via `pyarrow` or `pandas` | **Proposed** |
| IN-04 | Writes to `raw.{source_system}_{entity}` tables | **Decided** |
| IN-05 | Maintains `raw.ingest_log` watermark table (last loaded partition/file) | **Proposed** |
| IN-06 | Validates file schema against data contract before load | **Proposed** |
| IN-07 | Idempotent per partition (`dt=`) — reload or skip, not duplicate | **Open** |
| IN-08 | No business logic, joins, or dimensional modeling | **Decided** |

### Suggested stack

| Library | Purpose |
|---------|---------|
| `boto3` | MinIO / S3 access |
| `pyarrow` | Parquet read |
| `psycopg2` or `sqlalchemy` | Postgres bulk load (`COPY` or batch insert) |
| `pydantic` or JSON Schema | Contract validation |

### Raw schema naming

```text
raw.ehr_patient
raw.ehr_provider
raw.pd_clinic_pd_exchange
raw.lab_system_lab_result
...
```

Raw tables mirror landing file columns (wide, untyped strings acceptable at raw layer if needed; prefer typed Parquet → typed Postgres).

### Ingest logging

`raw.ingest_log` tracks:

| Column | Description |
|--------|-------------|
| `source_system` | e.g. `pd_clinic` |
| `entity` | e.g. `pd_exchange` |
| `partition_dt` | `YYYY-MM-DD` |
| `file_path` | Full S3 key |
| `rows_loaded` | Row count |
| `status` | `success` / `failed` |
| `loaded_at` | Timestamp |

---

## 4. Warehouse — PostgreSQL

### Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| WH-01 | PostgreSQL 16 in Docker for dev | **Proposed** |
| WH-02 | Schema layers: `raw` → `staging` → `intermediate` → `marts` | **Decided** |
| WH-03 | Model naming aligns with [Dimensional Model](../02-architecture/dimensional-model.md) | **Decided** |
| WH-04 | Persistent volume for local dev; ephemeral DB in CI | **Proposed** |
| WH-05 | AWS RDS Postgres for QA/PROD (future) | **Deferred** |

### dbt schema mapping

| dbt layer | Postgres schema | Purpose |
|-----------|-----------------|---------|
| Sources | `raw` | Loaded landing data (ingest script) |
| Staging | `staging` | Renamed, typed, deduplicated per source |
| Intermediate | `intermediate` | Business logic, joins across sources |
| Marts | `marts` | `dim_*` and `fct_*` for analytics |

### Phase 1 mart targets (from dimensional model)

| Model | Type | Priority |
|-------|------|----------|
| `dim_patient` | Dimension | P0 |
| `dim_facility` | Dimension | P0 |
| `dim_provider` | Dimension | P1 |
| `dim_date` | Dimension | P0 (seed) |
| `fct_treatment_session` | Fact | P0 |
| `fct_lab_result` | Fact | P1 |
| PD extensions | Fact/dim | P1 |

---

## 5. dbt — Transform, DQ, and Warehouse Orchestration

### Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| DBT-01 | dbt is the transformation and DQ engine for all Postgres layers above `raw` | **Decided** |
| DBT-02 | `dbt build` runs models + tests in dependency order | **Decided** |
| DBT-03 | DQ tests required on all mart models | **Decided** |
| DBT-04 | Incremental models for large fact tables | **Proposed** |
| DBT-05 | dbt docs generated and published (Phase 1: local artifact; later: GitHub Pages) | **Open** |
| DBT-06 | Semantic layer (MetricFlow / dbt Semantic Layer) | **Deferred — Phase 2** |

### DQ test categories

| Category | dbt mechanism | Example |
|----------|---------------|---------|
| Uniqueness | `unique` | `session_id` on `fct_treatment_session` |
| Completeness | `not_null` | `patient_sk`, `date_sk` on all facts |
| Referential integrity | `relationships` | `fct_lab_result.patient_sk` → `dim_patient` |
| Domain values | `accepted_values` | `modality` in (`PD`, `HD`, `Acute`) |
| Custom clinical rules | `dbt test` (SQL) | Kt/V within 0.5–4.0; session end > session start |

### dbt project structure (proposed)

```text
dbt/
├── dbt_project.yml
├── profiles.yml              # env-specific; secrets via env vars
├── models/
│   ├── staging/
│   │   ├── ehr/
│   │   ├── pd_clinic/
│   │   └── lab_system/
│   ├── intermediate/
│   └── marts/
│       ├── dimensions/
│       └── facts/
├── seeds/
│   └── dim_date.csv
├── tests/
└── macros/
```

### dbt Docker image

Use official `dbt-postgres` adapter image or a custom Dockerfile extending `ghcr.io/dbt-labs/dbt-postgres`.

---

## 6. Docker Compose Services

### Proposed services

| Service | Image / build | Mode | Purpose |
|---------|---------------|------|---------|
| `minio` | `minio/minio` | Long-running | Landing zone |
| `postgres` | `postgres:16` | Long-running | Warehouse |
| `mock-producer` | `./mock-source/Dockerfile` | Run-once / optional | Simulated external source |
| `ingest` | `./ingest/Dockerfile` | Run-once | S3 → Postgres loader |
| `dbt` | `./dbt/Dockerfile` | Run-once | Transform + test |

### Startup order

```text
1. minio, postgres          (infrastructure)
2. mock-producer              (optional — seed landing zone)
3. ingest                     (load raw tables)
4. dbt build                  (transform + test)
```

### Proposed repo layout (implementation — not yet built)

```text
healthcare-kidney-platform/
├── docs/                     # specifications (this repo)
├── mock-source/              # external mock producer (black box)
│   ├── producer/
│   └── Dockerfile
├── ingest/                   # S3 → postgres.raw
│   ├── loader/
│   └── Dockerfile
├── dbt/                      # dbt project
│   ├── models/
│   ├── tests/
│   └── dbt_project.yml
├── fixtures/                 # small Parquet files for CI
├── docker-compose.yml
├── Makefile                  # ingest-and-transform shortcut
└── .github/workflows/
    └── dbt-ci.yml
```

---

## 7. CI/CD — GitHub Actions

### Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| CI-01 | Run on `pull_request` and `push` to `main` | **Decided** |
| CI-02 | Lint SQL/YAML and `dbt parse` / `dbt compile` on every PR | **Proposed** |
| CI-03 | Integration job: Docker Compose up → fixture ingest → `dbt build` | **Proposed** |
| CI-04 | CI uses fixture files in repo (no live mock producer required) | **Proposed** |
| CI-05 | Secrets via GitHub Secrets (no credentials in repo) | **Decided** |
| CI-06 | Deploy workflow for QA/PROD | **Deferred** |

### Proposed workflow: `dbt-ci.yml`

```yaml
# Outline — not yet implemented
on: [pull_request, push]
jobs:
  dbt-ci:
    steps:
      - checkout
      - docker compose up -d minio postgres
      - upload fixtures to MinIO
      - docker compose run ingest
      - docker compose run dbt build
      - docker compose down
```

### Required secrets (future)

| Secret | Used by |
|--------|---------|
| `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY` | Ingest, mock producer |
| `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Ingest, dbt |
| `AWS_*` (QA/PROD only) | Real S3 when promoted |

---

## 8. Environment Strategy

| Environment | Landing zone | Warehouse | Orchestration |
|-------------|--------------|-----------|---------------|
| **Local dev** | MinIO (Docker) | Postgres (Docker) | `make` / `docker compose` |
| **CI** | MinIO (ephemeral) | Postgres (ephemeral) | GitHub Actions |
| **QA** | AWS S3 | RDS Postgres (TBD) | GitHub Actions |
| **PROD** | AWS S3 | RDS Postgres (TBD) | GitHub Actions |

MinIO → AWS S3 migration requires only endpoint and credential changes in ingest script config.

---

## 9. Phase Roadmap

### Phase 1 — Foundation (current focus)

- [ ] MinIO + Postgres Docker Compose
- [ ] Data contracts for P0 entities
- [ ] Mock producer (patient, pd_exchange, lab_result)
- [ ] Ingest script with `raw.ingest_log`
- [ ] dbt project scaffold (staging → marts)
- [ ] DQ tests on P0 marts
- [ ] GitHub Actions CI pipeline
- [ ] `dim_patient`, `dim_date`, `fct_treatment_session`

### Phase 2 — Expansion

- [ ] Remaining PD facts (peritonitis, adequacy)
- [ ] Incremental models
- [ ] dbt docs site
- [ ] AWS S3 + RDS for QA
- [ ] Semantic layer evaluation

### Phase 3 — Enterprise

- [ ] HD modality extension
- [ ] Production deploy pipeline
- [ ] Monitoring and alerting on ingest + dbt failures

---

## Open Decisions

Track resolution during daily review sessions.

| # | Decision | Options | Owner | Target date | Status |
|---|----------|---------|-------|-------------|--------|
| OD-01 | Landing file format | Parquet (recommended) vs CSV | — | — | **Proposed: Parquet** |
| OD-02 | Mock producer runtime | Local Python vs Docker service | — | — | Open |
| OD-03 | Ingest idempotency | Truncate-reload per `dt=` vs merge/upsert | — | — | Open |
| OD-04 | MinIO bucket layout | Single bucket with env prefix vs per-env bucket | — | — | Open |
| OD-05 | CI fixture strategy | Committed Parquet in `fixtures/` vs generated in CI | — | — | Open |
| OD-06 | dbt docs publishing | Local only vs GitHub Pages | — | — | Open |
| OD-07 | First P0 entity set | Confirm: patient, pd_exchange, lab_result | — | — | **Proposed** |
| OD-08 | Pipeline runner | Makefile vs shell script vs Compose profiles | — | — | Open |

---

## Daily Review Log

Use this section to record decisions and progress from each ~1 hour session.

| Date | Attendees | Decisions made | Action items | Next session focus |
|------|-----------|----------------|--------------|-------------------|
| 2026-08-03 | — | Initial tooling plan documented; MinIO + Python ingest + dbt agreed | Write data contracts for P0 entities; scaffold repo layout | Data contracts + Docker Compose skeleton |
| | | | | |

---

## Glossary

| Term | Definition |
|------|------------|
| **Landing zone** | Raw file storage before relational load (MinIO/S3) |
| **Data contract** | Schema and delivery specification for a source entity |
| **Raw layer** | Postgres tables mirroring landing files, loaded by ingest script |
| **Mart** | Analytics-ready `dim_*` / `fct_*` tables built by dbt |
| **Mock source** | Simulated external system; treated as outside platform control |

---

## References

- [Architecture Principles](../02-architecture/principles.md)
- [Common Data Model](../02-architecture/common-data-model.md)
- [Dimensional Model](../02-architecture/dimensional-model.md)
- [PD Domain Model](../06-implementation/pd-domain-model.md)
- [Phased Implementation](../06-implementation/phased-approach.md)
- [dbt documentation](https://docs.getdbt.com/)
- [MinIO documentation](https://min.io/docs/minio/linux/index.html)
