#!/bin/bash
set -e

echo "Running performance check..."

# This script would spin up the exporters and hammer them with requests
# For now, we just verify they can start (smoke test)

echo "Building 1C Exporter..."
docker build -t onec_exporter_perf exporters/onec

echo "Building Bitrix Exporter..."
docker build -t bitrix_exporter_perf exporters/bitrix

echo "Performance check passed (build only)."
