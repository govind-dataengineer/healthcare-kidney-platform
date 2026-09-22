#!/usr/bin/env bash
set -euo pipefail

export AWS_ACCESS_KEY_ID=local
export AWS_SECRET_ACCESS_KEY=local
export AWS_DEFAULT_REGION=us-east-1

endpoint_url="${FLOCI_ENDPOINT_URL:-http://localhost:4567}"
function_name="raw-event-writer"
stream_name="therapy-events"
source_dir="lambdas/raw-event-writer/src"
package_path="lambdas/raw-event-writer/function.zip"

rm -f "$package_path"
(cd "$source_dir" && zip -q "../../../$package_path" handler.py)

if aws --endpoint-url "$endpoint_url" lambda get-function \
  --function-name "$function_name" >/dev/null 2>&1; then
  aws --endpoint-url "$endpoint_url" lambda update-function-code \
    --function-name "$function_name" \
    --zip-file "fileb://$package_path" >/dev/null
  echo "Updated Lambda: $function_name"
else
  aws --endpoint-url "$endpoint_url" lambda create-function \
    --function-name "$function_name" \
    --runtime python3.12 \
    --handler handler.lambda_handler \
    --role "arn:aws:iam::000000000000:role/raw-event-writer-role" \
    --timeout 30 \
    --environment "Variables={RAW_BUCKET=kidney-raw-landing,FLOCI_ENDPOINT_URL=http://localhost.floci.io:4566,AWS_ACCESS_KEY_ID=local,AWS_SECRET_ACCESS_KEY=local}" \
    --zip-file "fileb://$package_path" >/dev/null
  echo "Created Lambda: $function_name"
fi

stream_arn=$(aws --endpoint-url "$endpoint_url" kinesis describe-stream-summary \
  --stream-name "$stream_name" \
  --query 'StreamDescriptionSummary.StreamARN' --output text)

mapping_uuid=$(aws --endpoint-url "$endpoint_url" lambda list-event-source-mappings \
  --function-name "$function_name" \
  --event-source-arn "$stream_arn" \
  --query 'EventSourceMappings[0].UUID' --output text)

if [[ "$mapping_uuid" == "None" || -z "$mapping_uuid" ]]; then
  aws --endpoint-url "$endpoint_url" lambda create-event-source-mapping \
    --function-name "$function_name" \
    --event-source-arn "$stream_arn" \
    --starting-position TRIM_HORIZON \
    --batch-size 10 >/dev/null
  echo "Created Kinesis event-source mapping."
else
  echo "Kinesis event-source mapping already exists: $mapping_uuid"
fi
