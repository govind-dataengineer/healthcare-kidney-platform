#!/usr/bin/env bash
set -euo pipefail

export AWS_ACCESS_KEY_ID=local
export AWS_SECRET_ACCESS_KEY=local
export AWS_DEFAULT_REGION=us-east-1

endpoint_url="${FLOCI_ENDPOINT_URL:-http://localhost:4567}"
max_attempts=30

for attempt in $(seq 1 "$max_attempts"); do
  if aws --endpoint-url "$endpoint_url" s3api list-buckets >/dev/null 2>&1; then
    echo "Floci is ready."
    exit 0
  fi
  sleep 1
done

echo "Floci did not become ready within ${max_attempts} seconds." >&2
echo "Start Docker Desktop, then run 'make start' again." >&2
exit 1
