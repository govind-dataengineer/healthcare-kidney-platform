.DEFAULT_GOAL := help

FLOCI_PORT ?= 4567
FLOCI_ENDPOINT_URL ?= http://localhost:$(FLOCI_PORT)
PYTHON ?= python3
VENV ?= .venv
export FLOCI_PORT
export FLOCI_ENDPOINT_URL

.PHONY: help start stop reset status bootstrap deploy-lambda setup-python simulate test-simulator test-lambda bronze-status

help:
	@echo "Kidney Care Analytics Platform — local learning environment"
	@echo ""
	@echo "  make start   Start a fresh local Floci environment and create S3 + Kinesis resources"
	@echo "  make stop    Stop the environment without deleting its current state"
	@echo "  make reset   Delete local emulator state (the next start is completely fresh)"
	@echo "  make status  Show the local services and S3 buckets"
	@echo "  make deploy-lambda    Package and deploy the Kinesis-to-S3 Lambda"
	@echo "  make bronze-status    Show the DuckDB Bronze event and ingest counts"
	@echo "  make setup-python     Create the local Python environment for the simulator"
	@echo "  make simulate         Send one accelerated synthetic APD session to Kinesis"
	@echo "  make test-simulator   Run the simulator's unit tests"
	@echo "  make test-lambda      Run the Lambda's unit tests"

start: reset
	@docker compose up -d --build floci bronze-loader
	@./scripts/wait-for-floci.sh
	@$(MAKE) bootstrap
	@echo ""
	@echo "Environment is ready at $(FLOCI_ENDPOINT_URL)"

stop:
	@docker compose stop
	@echo "Environment stopped. Run 'make start' for a new clean run."

reset:
	@docker compose down --volumes --remove-orphans
	@echo "Local Floci state removed."

bootstrap:
	@./infra/bootstrap.sh

deploy-lambda:
	@./infra/deploy-lambda.sh

status:
	@docker compose ps
	@AWS_ACCESS_KEY_ID=local AWS_SECRET_ACCESS_KEY=local AWS_DEFAULT_REGION=us-east-1 \
		aws --endpoint-url $(FLOCI_ENDPOINT_URL) s3api list-buckets \
		--query 'Buckets[].Name' --output table
	@AWS_ACCESS_KEY_ID=local AWS_SECRET_ACCESS_KEY=local AWS_DEFAULT_REGION=us-east-1 \
		aws --endpoint-url $(FLOCI_ENDPOINT_URL) kinesis list-streams \
		--query 'StreamNames' --output table

setup-python:
	@$(PYTHON) -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install -r services/device-simulator/requirements.txt

simulate:
	@test -x $(VENV)/bin/python || (echo "Python environment missing. Run 'make setup-python' first." >&2; exit 1)
	@$(VENV)/bin/python services/device-simulator/src/simulator.py \
		--endpoint-url $(FLOCI_ENDPOINT_URL)

test-simulator:
	@test -x $(VENV)/bin/python || (echo "Python environment missing. Run 'make setup-python' first." >&2; exit 1)
	@$(VENV)/bin/python -m unittest discover -s tests -p 'test_*.py' -v

test-lambda: test-simulator

bronze-status:
	@docker compose exec -T bronze-loader python inspect_bronze.py
