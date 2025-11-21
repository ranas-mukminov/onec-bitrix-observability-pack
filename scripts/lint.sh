#!/bin/bash
set -e

echo "Running linters..."

# Python
echo "Running flake8..."
flake8 exporters/onec/src ai/src tests

echo "Running black..."
black --check exporters/onec/src ai/src tests

echo "Running mypy..."
mypy exporters/onec/src ai/src

# PHP (if installed)
if command -v php >/dev/null 2>&1; then
    echo "Running PHP lint..."
    find exporters/bitrix/src -name "*.php" -print0 | xargs -0 -n1 php -l
else
    echo "PHP not found, skipping PHP lint."
fi

echo "Linting passed!"
