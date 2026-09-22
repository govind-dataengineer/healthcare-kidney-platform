# APD device simulator

This Python program emits a synthetic, de-identified APD therapy session into the local `therapy-events` Kinesis stream. It is an educational simulator, not a clinical device model and not a source of clinical guidance.

## Event lifecycle

```text
therapy_started
  → initial_drain
  → cycle_fill → cycle_dwell_completed → cycle_drain  (repeated)
  → last_fill
  → therapy_completed
```

Every record includes `run_id`, `session_id`, `device_id`, and a synthetic `patient_id`. The Kinesis partition key is `device_id`, which keeps the events for one device ordered within a shard.

## Run it

From the repository root, after `make start`:

```bash
make setup-python
make simulate
```

The default replay uses a two-second interval between events. Use a faster or slower replay directly when learning:

```bash
.venv/bin/python services/device-simulator/src/simulator.py \
  --endpoint-url http://localhost:4567 \
  --interval-seconds 0.5
```

## Event payloads

The simulator uses simple synthetic values to make the event sequence easy to follow:

- Initial drain: drained volume and duration
- Cycles: prescribed and actual fill, dwell, and drain values
- Last fill: final fill volume
- Completion: total therapy time and total ultrafiltration

The next milestone reads these Kinesis records with Lambda and stores immutable raw JSON in `kidney-raw-landing`.
