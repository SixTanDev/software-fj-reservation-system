# Comprehensive System for Managing Clients, Services, and Reservations

## Purpose

This repository contains the academic Software FJ system for managing clients, services,
and reservations with object-oriented Python. The implementation focuses on the Phase 4
requirements defined in `docs/mvp/`, including custom exceptions, robust error handling,
file-based logging, in-memory repositories, simulation of valid and invalid operations,
and pytest coverage.

## Implemented Scope

- `Client`, `Service`, and `Reservation` domain entities
- `RoomService`, `EquipmentService`, and `ConsultingService`
- Centralized custom exception hierarchy
- In-memory repositories only
- Centralized `FileLogger` with:
  - `RotatingFileHandler`
  - `QueueHandler`
  - `QueueListener`
  - safe shutdown
- Application use cases for:
  - client registration
  - service creation
  - reservation creation
  - reservation confirmation, cancellation, and processing
- Simulation with valid and invalid operations that proves continuity after controlled
  failures
- Tests for domain rules, exception chaining, repositories, logger rotation, and
  simulation continuity

## Requirements

- Python 3.10
- `uv` 0.11.7 or newer

## Setup

```bash
uv sync
```

Optional Git hooks:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

## Run the Simulation

```bash
uv run python -m software_fj_reservation_system.simulation.operations_simulator
```

The simulation writes logs to `logs/system.log` by default.

## Run the Tests

```bash
uv run pytest
```

## Run Pylint

```bash
uv run pylint src tests
```

## Run Pre-Commit

```bash
uv run pre-commit run --all-files
```

## Project Structure

```text
src/software_fj_reservation_system/
├── application/
├── domain/
├── exceptions/
├── infrastructure/
└── simulation/
tests/
docs/
└── mvp/
```

## Documentation

Authoritative scope:

- `AGENTS.md`
- `docs/mvp/Annex 3 – Problem to Develop Phase 4.md`
- `docs/mvp/Tasks assigned to Emmanuel Palacio Gaviria.md`
- `docs/mvp/software_fj_selected_architecture.md`

Implementation notes:

- `docs/logging-and-exception-handling.md`
- `summary_report.md`

## Logging Notes

- Business data stays in memory.
- Files are used only for logs.
- The logger centralizes writes through a queue/listener pair so the application threads
  enqueue records while a single listener writes to the rotating file.

## Validation Commands Used in This Repository

```bash
uv run pytest
uv run pylint src tests
uv run pre-commit run --all-files
uv run python -m software_fj_reservation_system.simulation.operations_simulator
```
