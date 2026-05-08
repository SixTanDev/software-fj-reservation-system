# feat(simulation): implement Emmanuel robustness scope

## Summary

Implemented Emmanuel Palacio Gaviria's robustness scope for the Software FJ academic reservation system.

This local PR adds centralized custom exceptions, robust error handling, queue-based rotating file logging, in-memory repositories, application use cases, a multi-operation simulator, tests, and documentation evidence.

## Why

The academic assignment requires the system to continue operating after controlled failures while recording relevant events and errors in log files. Emmanuel's assigned scope specifically covers custom exceptions, robust error handling, logging, tests, simulation, and evidence of system continuity.

## What Changed

### Exceptions and error handling

- Added a centralized custom exception hierarchy for controlled system errors.
- Converted low-level validation failures into domain-specific exceptions where appropriate.
- Preserved original causes through exception chaining with `raise ... from`.
- Demonstrated `try/except`, `try/except/else`, and `try/except/finally`.

### Logging

- Added a centralized file logger.
- Used the Python standard library `logging` module.
- Added rotating log files with `RotatingFileHandler`.
- Added queue-based logging with `QueueHandler` and `QueueListener` to reduce concurrent write risk.
- Added safe logger shutdown through `close()` / `shutdown()`.
- Ensured logging failures do not stop the main simulation flow.

### Repositories and application layer

- Added in-memory repositories for clients, services, and reservations.
- Added application use cases to coordinate domain objects, repositories, and logging.
- Kept domain data in memory only.
- Avoided database usage and avoided file persistence for business data.

### Simulation

- Added a simulator that executes more than 10 operations.
- Included valid and invalid client registration.
- Included valid and invalid service creation.
- Included valid and invalid reservation flows.
- Demonstrated controlled error handling.
- Demonstrated system continuity after failures.
- Generated log evidence for successful events and errors.

### Tests

- Added tests for custom exceptions.
- Added tests for logger behavior and log rotation.
- Added tests for repositories.
- Added tests for application use cases.
- Added tests for simulation continuity.
- Updated domain tests where necessary.

### Documentation

- Added documentation for logging and exception handling.
- Updated project usage documentation where applicable.
- Added evidence of Emmanuel's implementation scope.

## Files Changed

### Source

- `src/software_fj_reservation_system/__init__.py`
- `src/software_fj_reservation_system/application/__init__.py`
- `src/software_fj_reservation_system/application/create_reservation.py`
- `src/software_fj_reservation_system/application/create_service.py`
- `src/software_fj_reservation_system/application/manage_reservation.py`
- `src/software_fj_reservation_system/application/register_client.py`
- `src/software_fj_reservation_system/domain/client.py`
- `src/software_fj_reservation_system/domain/consulting_service.py`
- `src/software_fj_reservation_system/domain/equipment_service.py`
- `src/software_fj_reservation_system/domain/reservation.py`
- `src/software_fj_reservation_system/domain/room_service.py`
- `src/software_fj_reservation_system/domain/service.py`
- `src/software_fj_reservation_system/exceptions/__init__.py`
- `src/software_fj_reservation_system/infrastructure/__init__.py`
- `src/software_fj_reservation_system/infrastructure/_base_repository.py`
- `src/software_fj_reservation_system/infrastructure/client_repository.py`
- `src/software_fj_reservation_system/infrastructure/file_logger.py`
- `src/software_fj_reservation_system/infrastructure/reservation_repository.py`
- `src/software_fj_reservation_system/infrastructure/service_repository.py`
- `src/software_fj_reservation_system/simulation/__init__.py`
- `src/software_fj_reservation_system/simulation/operations_simulator.py`

### Tests

- `tests/test_domain_objects.py`
- `tests/test_exceptions.py`
- `tests/test_file_logger.py`
- `tests/test_repositories.py`
- `tests/test_simulation.py`
- `tests/test_use_cases.py`

### Documentation

- `docs/logging-and-exception-handling.md`
- `README.md`

### Configuration

- `pyproject.toml` to update the package description so it reflects the implemented system instead of the earlier baseline.
- `.gitignore` to exclude local delivery artifacts from the branch workflow.

## Validation

- [x] `uv run pytest` - Passed, `24 passed in 0.18s`
- [x] `uv run pylint src tests` - Passed, `10.00/10`
- [x] `uv run python -m software_fj_reservation_system.simulation.operations_simulator` - Passed, simulator completed with controlled `[OK]`, `[ERROR]`, and `[CONTINUE]` output
- [x] `uv run pre-commit run --all-files` - Passed

## Evidence

- The simulator executes more than 10 operations.
- Controlled failures are captured and logged.
- The program continues after errors.
- Logs are generated in `logs/system.log`.
- Tests cover exceptions, logging, repositories, use cases, and simulation continuity.

## Excluded from this local PR

The following files must not be included in the final branch commit if they appear modified:

- `docs/mvp/Annex 3 – Problem to Develop Phase 4.md`
- `docs/mvp/software_fj_selected_architecture.md`
- `docs/mvp/Tasks assigned to Emmanuel Palacio Gaviria.md`

These are original assignment/context documents and should be restored before committing unless the team explicitly approves changes to them.

Also exclude:

- `summary_report.md`,
- generated log files,
- `.zip` files,
- screenshots,
- cache folders,
- temporary local notes.

## Reviewer Notes

This PR is focused on Emmanuel Palacio Gaviria's assigned robustness section only. It should not introduce database persistence or unrelated architecture changes.

The working tree was clean before creating this local PR note. `summary_report.md` is a local artifact and should stay outside the final PR even if it exists on disk for personal reference.

## Local Status

`git status --short` returned no output. The working tree is clean and there are no staged changes.

## Commit Plan

Recommended commits, if the maintainer decides to commit later:

1. `feat(exceptions): add controlled management system errors`
2. `feat(logging): add queue-based rotating file logger`
3. `feat(application): add in-memory repositories and reservation use cases`
4. `feat(simulation): demonstrate continuity after controlled failures`
5. `test(robustness): cover logging exceptions and simulation flow`
6. `docs(mvp): document Emmanuel robustness evidence`
