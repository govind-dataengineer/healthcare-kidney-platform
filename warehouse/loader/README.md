# Bronze loader

The Bronze loader polls `s3://kidney-raw-landing/raw/` every five seconds and loads each immutable JSON object exactly once into DuckDB.

## Tables

- `bronze.raw_therapy_event` — one row per raw APD lifecycle event
- `bronze.ingest_log` — one row per S3 object successfully loaded

Business payloads remain JSON in Bronze. Silver and Gold dbt models will own typing, session reconstruction, and KPI logic.

## Validate

```bash
make bronze-status
```
