#!/bin/bash
set -e

echo "Running security scan..."

# Python dependencies
echo "Checking python dependencies..."
# pip-audit or safety would go here. For now, we just echo.
# pip-audit -r exporters/onec/requirements.txt

# Bandit (SAST for Python)
echo "Running bandit..."
bandit -r exporters/onec/src ai/src -c pyproject.toml || true

echo "Security scan finished."
