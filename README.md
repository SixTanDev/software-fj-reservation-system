# Comprehensive System for Managing Clients, Services, and Reservations

## Purpose

This repository contains the academic Software FJ system for managing clients, services,
and reservations with object-oriented Python. The implementation focuses on the Phase 4
requirements defined in `docs/mvp/`, including custom exceptions, robust error handling,
file-based logging, in-memory repositories, Pydantic input validation, a Tkinter/ttk
desktop interface, simulation of valid and invalid operations, and pytest coverage.

## Implemented Scope

- `Client`, `Service`, and `Reservation` domain entities
- `RoomService`, `EquipmentService`, and `ConsultingService`
- Centralized custom exception hierarchy
- Pydantic validation in the application/input layer
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
- Tkinter/ttk desktop UI for:
  - dashboard counters and status
  - client registration
  - service creation
  - reservation creation, confirmation, cancellation, and processing
  - log inspection
- Simulation with valid and invalid operations that proves continuity after controlled
  failures
- Tests for domain rules, Pydantic translation, repositories, logger rotation, desktop
  controller delegation, and simulation continuity

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

## Run the Desktop UI

```bash
uv run python -m software_fj_reservation_system.presentation.desktop_app
```

If the current Python runtime does not include Tk support or the environment is headless,
validate the import path instead:

```bash
uv run python -c "from software_fj_reservation_system.presentation.desktop_app import ReservationDesktopApp; print('UI import OK')"
```

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
├── presentation/
└── simulation/
tests/
docs/
├── mvp/
└── pydantic-and-desktop-ui.md
```

## Documentation

Authoritative scope:

- `AGENTS.md`
- `docs/mvp/Annex 3 – Problem to Develop Phase 4.md`
- `docs/mvp/Tasks assigned to Emmanuel Palacio Gaviria.md`
- `docs/mvp/software_fj_selected_architecture.md`

Implementation notes:

- `docs/logging-and-exception-handling.md`
- `docs/pydantic-and-desktop-ui.md`
- `summary_report.md` (local-only)

## Logging Notes

- Business data stays in memory.
- Files are used only for logs.
- The logger centralizes writes through a queue/listener pair so the application threads
  enqueue records while a single listener writes to the rotating file.

## Validation Commands Used in This Repository

```bash
uv sync
uv run pytest
uv run pylint src tests
uv run pre-commit run --all-files
uv run python -m software_fj_reservation_system.simulation.operations_simulator
uv run python -m software_fj_reservation_system.presentation.desktop_app
```
