#!/usr/bin/env bash
set -euo pipefail

# These are deliberately non-production credentials. Floci accepts them locally;
# never use real AWS credentials for this learning environment.
export AWS_ACCESS_KEY_ID=local
export AWS_SECRET_ACCESS_KEY=local
export AWS_DEFAULT_REGION=us-east-1

endpoint_url="${FLOCI_ENDPOINT_URL:-http://localhost:4567}"

create_bucket_if_missing() {
  local bucket_name="$1"
  if aws --endpoint-url "$endpoint_url" s3api head-bucket --bucket "$bucket_name" 2>/dev/null; then
    echo "Bucket already exists: $bucket_name"
    return
  fi

  aws --endpoint-url "$endpoint_url" s3api create-bucket --bucket "$bucket_name" >/dev/null
  echo "Created bucket: $bucket_name"
}

# The simulated vendor bucket mirrors Sharesource ownership. The internal bucket
# is the platform's immutable landing zone.
create_bucket_if_missing "sharesource-simulated"
create_bucket_if_missing "kidney-raw-landing"

create_stream_if_missing() {
  local stream_name="$1"
  if aws --endpoint-url "$endpoint_url" kinesis describe-stream-summary \
    --stream-name "$stream_name" >/dev/null 2>&1; then
    echo "Kinesis stream already exists: $stream_name"
    return
  fi

  aws --endpoint-url "$endpoint_url" kinesis create-stream \
    --stream-name "$stream_name" \
    --shard-count 1 >/dev/null
  echo "Created Kinesis stream: $stream_name (1 shard)"
}

# One shard is enough for an MVP. It preserves event order for records sent with
# the same device_id partition key and is easy to inspect while learning.
create_stream_if_missing "therapy-events"

"$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/deploy-lambda.sh"
