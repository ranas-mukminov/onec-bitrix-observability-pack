#!/bin/bash
set -e

echo "Running all tests..."

# 1. Run Linters
./scripts/lint.sh

# 2. Run Python Unit Tests
echo "Running Python tests..."
export PYTHONPATH=$PYTHONPATH:$(pwd)/exporters/onec/src:$(pwd)/ai/src:$(pwd)/tests/mocks
python3 -m pytest tests/exporters/onec tests/ai

# 3. Run PHP Tests (if available)
if command -v php >/dev/null 2>&1; then
    echo "Running PHP tests..."
    php tests/exporters/bitrix/test_bitrix_metrics.php
else
    echo "PHP not found, skipping PHP tests."
fi

echo "All tests passed!"
