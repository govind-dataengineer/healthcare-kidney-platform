# Raw event writer Lambda

This Lambda is triggered by Kinesis stream records from `therapy-events`.

For each record it:

1. Decodes the Base64 transport value supplied by Kinesis.
2. Parses and validates the project's plain JSON event envelope.
3. Writes an immutable JSON file to `s3://kidney-raw-landing`.

The stored object path is partitioned by `run_id`, date, and `device_id`:

```text
raw/run_id={run_id}/dt=YYYY-MM-DD/device_id={device_id}/{timestamp}_{event_id}.json
```

No clinical transformation happens here. DuckDB and dbt will own typing, deduplication, and metrics in later milestones.
