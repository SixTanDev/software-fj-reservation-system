# Logging and Exception Handling

## Purpose

This document describes the robustness section assigned to Emmanuel Palacio Gaviria for
the Software FJ academic project.

## Custom Exception Hierarchy

The centralized exception package lives in:

```text
src/software_fj_reservation_system/exceptions/__init__.py
```

Implemented hierarchy:

- `ManagementSystemError`
- `InvalidDataError`
- `ServiceUnavailableError`
- `InvalidReservationError`
- `OperationNotAllowedError`
- `InconsistentCalculationError`
- `LoggingError`

The domain and application layers use these exceptions to expose controlled failures
instead of leaking low-level validation errors to the simulator.

## Exception Handling Patterns Demonstrated

The project explicitly demonstrates:

- `try/except`: direct handling of controlled failures in the simulator.
- `try/except/else`: successful and failed application operations in the simulator and
  use cases.
- `try/except/finally`: safe shutdown of the queue listener in the simulator.
- exception chaining with `raise ... from`: low-level `ValueError`, `TypeError`,
  `KeyError`, and repository lookup failures are converted into controlled domain or
  application errors while preserving the original cause.

## Logging Design

The centralized logger lives in:

```text
src/software_fj_reservation_system/infrastructure/file_logger.py
```

Key decisions:

- Standard library `logging` only.
- `RotatingFileHandler` for bounded log growth.
- `QueueHandler` plus `QueueListener` for a single physical file writer inside the
  process.
- explicit `close()` / `shutdown()` to stop the listener safely.
- no `logging.basicConfig`.
- logger reuse per physical log path to avoid duplicate handlers.

Default location:

```text
logs/system.log
```

Format includes:

- timestamp
- level
- operation
- message
- error type
- state/context

## Why Rotation Is Used

`RotatingFileHandler` is used to keep the academic log output bounded and reviewable.
This prevents uncontrolled file growth while preserving backup files as evidence of
events and controlled failures.

## Why QueueHandler and QueueListener Are Used

The simulator and application code enqueue records through `QueueHandler`. A single
`QueueListener` thread drains the queue and writes to the rotating file handler. In this
single-process academic application, that design reduces the risk of interleaved writes
and avoids attaching multiple direct file handlers across the execution flow.

## Repositories and Persistence Rule

- Clients, services, and reservations are stored only in memory.
- Repositories use dictionaries and lists derived from those dictionaries.
- No database engine is used.
- No domain data is written to files.
- Files are used only for logs.

## Simulation Evidence

The simulator lives in:

```text
src/software_fj_reservation_system/simulation/operations_simulator.py
```

It executes valid and invalid operations, including:

- valid client registration
- invalid client registration
- valid and invalid service creation
- valid and invalid reservation creation
- confirmation, cancellation, and processing
- inconsistent calculation attempts
- explicit continuity evidence after controlled errors

The simulator prints controlled console output such as:

- `[OK] ...`
- `[ERROR] ...`
- `[CONTINUE] ...`

## How to Run

Simulation:

```bash
uv run python -m software_fj_reservation_system.simulation.operations_simulator
```

Tests:

```bash
uv run pytest
```

Lint:

```bash
uv run pylint src tests
```

## Evidence Expected for Emmanuel's Section

- custom exceptions module
- centralized log generation
- recorded successful events and controlled errors
- simulation with more than 10 operations
- proof that the system continues running after controlled failures
- pytest coverage for exceptions, logger, repositories, use cases, and simulation

## APA References

- Python Software Foundation. (2026). *logging.handlers — Logging handlers*. Python
  3.10.20 documentation. https://docs.python.org/3.10/library/logging.handlers.html
- Python Software Foundation. (2026). *logging — Logging facility for Python*. Python
  3.10.20 documentation. https://docs.python.org/3.10/library/logging.html
- Python Software Foundation. (2026). *Logging Cookbook*. Python 3.10.20 documentation.
  https://docs.python.org/3.10/howto/logging-cookbook.html
- Python Software Foundation. (2026). *Errors and Exceptions*. Python 3.10.20
  documentation. https://docs.python.org/3.10/tutorial/errors.html
