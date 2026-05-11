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

## Execution and Validation Guide

The following commands are the main entry points used to validate the project from an
academic and technical perspective. They allow the evaluator to verify automated
correctness, controlled execution of valid and invalid scenarios, and the availability
of the desktop graphical interface.

Before running any command in this section:

1. Ensure that `uv` is installed on the machine.
2. Synchronize the environment and dependencies:

   ```bash
   uv sync
   ```

3. Execute the selected command from the repository root.

## Running Automated Tests

To execute the automated validation suite, run:

```bash
uv run pytest
```

This command starts the project's tests with `pytest` inside the virtual environment
managed by `uv`. Its purpose is to verify that the object-oriented reservation system
behaves correctly across its main layers and responsibilities. In practical terms, the
suite validates:

- domain entities such as clients, services, and reservations;
- application use cases that coordinate business operations;
- in-memory repositories used instead of a database;
- custom exception handling and controlled validation failures;
- logging-related behavior and simulation continuity;
- the expected functional behavior of the system as a whole.

A successful execution may produce an output similar to the following:

```text
36 passed, 1 skipped
```

That result is acceptable for this project. The skipped test may correspond to the
graphical interface when the execution environment does not provide GUI support or when
the current Python installation does not include Tkinter support. In that situation, the
test suite still confirms the core academic requirements of the system, and the skipped
GUI check does not necessarily mean that the project is incorrect.

In environments where Tkinter is fully available, the final result may show all tests as
passed instead of reporting a skipped GUI test.

## Running the System Simulation

To execute the console-based simulation, run:

```bash
uv run python -m software_fj_reservation_system.simulation.operations_simulator
```

This command runs the academic simulation of the reservation system from the command
line. The simulation is intentionally designed to demonstrate the behavior of the
application without requiring a database engine or a graphical user interface. All core
data is managed in memory, while relevant events and controlled failures are recorded in
the log file `logs/system.log`.

The purpose of this execution is not only to show successful flows, but also to prove
that the system remains stable when controlled errors occur. For that reason, the
simulation includes both valid and invalid operations, and it continues running after
exceptions are detected and handled through the corresponding `try/except` logic.

The current `operations_simulator` demonstrates a sequence of operations such as the
following:

1. Registering a valid client with correct name, email, and phone data.
2. Attempting to register a client with an empty name.
3. Attempting to register a client with an invalid email address.
4. Creating valid services, including room, equipment, and consulting services.
5. Attempting to execute an invalid service-related operation. In the current simulator,
   the explicit negative case is the creation of a service with an unknown type. More
   generally, the same controlled exception approach also applies to attempts to use or
   search for a non-existing or unavailable service.
6. Creating a valid reservation using an existing client and an existing service.
7. Attempting to create a reservation with an invalid duration.
8. Confirming a valid reservation.
9. Processing a valid reservation with tax and discount parameters.
10. Creating a second valid reservation in order to exercise cancellation behavior.
11. Cancelling a valid reservation.
12. Attempting to cancel a reservation that has already been cancelled or is otherwise in
    an invalid state for that operation.
13. Creating and confirming an additional reservation for a controlled processing failure.
14. Attempting to process a reservation with inconsistent cost data.
15. Registering the corresponding errors in `logs/system.log`.
16. Continuing execution after controlled errors by using structured exception handling
    blocks.

From an academic viewpoint, this simulation also serves as evidence that the project
applies the required object-oriented programming concepts:

- encapsulation in the handling of client and reservation data;
- abstraction through shared entity and service contracts;
- inheritance through specialized service classes;
- polymorphism through service-specific behavior such as description and cost handling;
- custom exception handling through a centralized exception hierarchy;
- layered architecture across presentation/simulation, application, domain,
  infrastructure, and test responsibilities.

During execution, the console output should clearly distinguish successful operations,
controlled failures, and continuity after errors. A representative example is shown
below:

```text
[OK] register_client_valid
[ERROR] register_client_empty_name
[CONTINUE] Simulation continues after controlled error
[OK] process_reservation_valid
```

Additional lines may include more detailed messages, such as the reason for the
validation failure or the final processed reservation cost. The important academic
criterion is that the simulation does not terminate when a controlled error appears.

## Running the Desktop Graphical Interface

To start the desktop graphical interface, run:

```bash
uv run python -m software_fj_reservation_system.presentation.desktop_app
```

This command starts the desktop application developed with Tkinter. The graphical
interface provides a visual way to work with the reservation system and is intended to
support the management of clients, services, and reservations through a desktop window
instead of the console simulation. In the current project structure, the interface is
part of the presentation layer and acts as a user-facing entry point over the same
business and application logic validated by the automated tests.

Python must include Tkinter support in order to open the graphical window successfully.
If the active Python runtime does not provide Tkinter, the desktop interface cannot be
displayed even if the rest of the project is correct.

### Troubleshooting on macOS/Homebrew

If the following error appears:

```text
No module named '_tkinter'
```

install Tkinter support for the Homebrew-managed Python runtime:

```bash
brew install python-tk@3.10
```

Then, if necessary, recreate the virtual environment and verify the Tkinter import before
starting the GUI again:

```bash
rm -rf .venv
uv sync
uv run python -c "import tkinter; print('Tkinter OK')"
uv run python -m software_fj_reservation_system.presentation.desktop_app
```

## Important Notes

- `uv run` executes commands inside the virtual environment managed by `uv`.
- Before running the commands, `uv` must be installed and the project dependencies must
  be synchronized with `uv sync`.
- The system does not require a database because the academic requirement is based on
  object-oriented design with in-memory data management.
- During execution, clients, services, and reservations are handled in memory.
- Files are used only for logging and execution evidence, especially in
  `logs/system.log`.
- The expected errors shown in the simulation are intentional. They are part of the
  evidence that demonstrates robust exception handling and controlled validation.
- A controlled error in the simulation should not stop the rest of the execution.
- When the environment provides GUI support, the desktop command opens the Tkinter
  application window; when it does not, the rest of the project can still be validated
  through `pytest` and the console simulation.

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
