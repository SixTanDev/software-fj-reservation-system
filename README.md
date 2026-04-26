# Comprehensive System for Managing Clients, Services, and Reservations

## Purpose

This repository hosts the Programming course project for **Software FJ**. The final system
must manage clients, services, and reservations with object-oriented Python, custom
exceptions, file-based logging, controlled error handling, and a simulation that continues
running after failures.

## Current Baseline Status

The repository currently provides the technical baseline needed for future implementation:

- UV-based dependency management
- pytest configuration with a minimal honest baseline test
- pylint configuration for the current `src/` and `tests/` layout
- pre-commit hooks for repository hygiene, Conventional Commits, and linting
- GitHub Actions workflows for pytest and pull request quality checks

The business system itself is **not implemented yet** in this baseline.

## Requirements

- Python 3.10
- [uv](https://docs.astral.sh/uv/) 0.11.7 or newer

## Setup with UV

Create the virtual environment and install the development dependencies:

```bash
uv sync
```

Install the local Git hooks when you want automated commit and push checks:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

## Running Tests

Run the current baseline test suite:

```bash
uv run pytest
```

## Running Pylint

Lint the scaffolded package and tests:

```bash
uv run pylint src tests
```

## Running Pre-Commit

Run the configured repository checks manually:

```bash
uv run pre-commit run --all-files
```

Because `pre-commit run --all-files` only checks tracked content, new local files may also
need explicit targeting until they are added to Git:

```bash
uv run pre-commit run --files pyproject.toml .pre-commit-config.yaml README.md tests/test_baseline.py
```

## CI Workflows

- `pytest.yml`: runs `uv sync --locked` and `uv run pytest` on pushes to `develop`.
- `pr-ci-fast.yml`: validates the pull request title and runs pre-commit for quick PR feedback.
- `pr-ci-deep.yml`: validates commit messages, then runs pytest and pylint for deeper PR review.

## Project Documentation

The academic scope for this repository is defined in:

- `docs/mvp/Annex 3 – Problem to Develop Phase 4.md`
- `docs/mvp/Tasks assigned to Emmanuel Palacio Gaviria.md`

The prompt execution contract for this baseline lives in:

- `AGENTS.md`
- `prompt-master.md`
- `subprompts/01-diagnosis.md`
- `subprompts/02-baseline-tooling-uv.md`
- `subprompts/03-ci-precommit-pylint.md`
- `subprompts/04-tests-readme-documentation.md`
- `subprompts/05-validation-commits-pr.md`

## Future Implementation Scope

The future domain implementation must add:

- clients with validations and encapsulation
- abstract and specialized services
- reservations with controlled state transitions
- custom exceptions and exception chaining
- centralized file logging for events and errors
- a simulation with at least 10 valid and invalid operations
- pytest coverage for valid flows, controlled failures, and continuity after errors

## Conventional Commits and Pull Requests

Use Conventional Commits for every commit and PR title. Examples:

- `chore(tooling): configure uv project baseline`
- `chore(lint): add pre-commit and pylint quality gates`
- `ci(pr): add pull request validation workflows`

The pull request template is available at `.github/PULL_REQUEST_TEMPLATE.md`.
