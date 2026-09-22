# MVP local foundation

This is the runnable starting point for the Kidney Care Analytics Platform MVP. It provides a local, AWS-shaped environment for learning with **Floci** before streaming and analytics services are added.

## What this milestone includes

- Floci, running locally through Docker Compose at `http://localhost:4567`
- The AWS CLI configured with safe local-only credentials inside project scripts
- A simulated vendor bucket: `sharesource-simulated`
- An internal immutable landing bucket: `kidney-raw-landing`
- A single-shard Kinesis stream: `therapy-events`
- A Lambda event-source mapping: `therapy-events` → `raw-event-writer` → `kidney-raw-landing`
- One-command fresh runs through `make start`

It intentionally does **not** add DuckDB or dbt yet. Each is introduced in its own learning milestone so the system stays understandable.

## Prerequisites

- Docker Desktop running
- Docker Compose available
- AWS CLI available

No AWS account or real AWS credentials are used. Floci accepts the local placeholder credentials configured by the scripts.

## Commands

```bash
make start
make status
make stop
make reset
```

`make start` always creates a clean local run. `make stop` pauses the current environment. `make reset` removes the local Floci volume; it is destructive only to locally emulated data.

The project uses host port `4567` by default to avoid colliding with another local AWS emulator. If you need a different port, run `make FLOCI_PORT=4568 start`.

## Current architecture

```text
Floci
├── s3://sharesource-simulated  (future simulated external source)
├── s3://kidney-raw-landing     (future platform landing zone)
└── Kinesis: therapy-events     (one shard; future APD device events)
```

`therapy-events` carries ordered events for each device. The simulator uses `device_id` as the Kinesis partition key so one device's therapy lifecycle remains ordered within a shard. The `raw-event-writer` Lambda receives those records and writes validated plain JSON to the landing bucket.

The next milestone adds DuckDB Bronze ingestion from the raw landing bucket.
