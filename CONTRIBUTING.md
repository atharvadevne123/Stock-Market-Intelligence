# Contributing to Stock Market Intelligence

Thank you for considering contributing!

## Getting Started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
make install
```

3. Create a feature branch:

```bash
git checkout -b feat/your-feature-name
```

## Development Workflow

### Running tests

```bash
make test
```

### Linting and formatting

```bash
make lint        # Check for issues
make format      # Auto-format code
make lint-fix    # Fix auto-fixable lint errors
```

### Type checking

```bash
make type-check
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat(scope): add new feature`
- `fix(scope): fix a bug`
- `test(scope): add or update tests`
- `docs(scope): update documentation`
- `refactor(scope): refactor code`
- `chore(scope): maintenance tasks`

## Pull Request Process

1. Ensure all tests pass (`make test`).
2. Add or update tests for your changes.
3. Update `CHANGELOG.md` with a summary of your changes.
4. Open a PR against `main` with a clear description.

## Code Style

- All code is linted with [ruff](https://github.com/astral-sh/ruff).
- Type annotations are required for all public functions.
- Google-style docstrings are preferred.

## Reporting Issues

Please use the GitHub Issues tracker. Include:
- Python version and OS
- Steps to reproduce
- Expected vs actual behaviour
- Relevant stack trace

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feat/<short-desc>` | `feat/portfolio-risk-endpoint` |
| Bug fix | `fix/<short-desc>` | `fix/ticker-validation-edge-case` |
| Docs | `docs/<short-desc>` | `docs/api-portfolio-section` |
| Chore | `chore/<short-desc>` | `chore/update-deps` |

## Testing Guidelines

- Aim for ≥ 80% line coverage on new modules.
- Use `pytest.mark.parametrize` for data-driven tests.
- Mock external HTTP calls and database I/O in unit tests.
- Integration tests live in `tests/test_integration.py` and may use a real SQLite in-memory database.

## Review Checklist

Before requesting a review, verify:
- [ ] All tests pass locally (`make test`)
- [ ] No new ruff lint errors (`make lint`)
- [ ] Type annotations present on public functions
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] No secrets or credentials committed

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
