# Contributing to onec-bitrix-observability-pack

We welcome contributions! Please follow these guidelines to ensure a smooth process.

## Development Workflow

1.  **Fork and Clone**: Fork the repository and clone it locally.
2.  **Branching**: Create a feature branch (`git checkout -b feature/my-new-feature`).
3.  **Testing**:
    *   We practice TDD (Test Driven Development).
    *   **Before** committing, run the full test suite:
        ```bash
        ./scripts/dev_run_all_tests.sh
        ```
    *   Ensure all tests pass and linters are happy.
4.  **Commit**: Make atomic commits with clear messages.
5.  **Push and PR**: Push to your fork and submit a Pull Request.

## Code Standards

*   **Python**: Follow PEP 8. We use `flake8`, `black`, and `mypy`.
*   **PHP**: Follow PSR-12.
*   **General**:
    *   No hardcoded secrets.
    *   No proprietary code from 1C or Bitrix.
    *   No real customer data in tests/examples.

## CI/CD

Our CI pipeline runs on every PR and checks:
1.  Linting and Unit Tests.
2.  Integration Tests (Docker Compose).
3.  Security Scans.

PRs cannot be merged if the CI fails.
