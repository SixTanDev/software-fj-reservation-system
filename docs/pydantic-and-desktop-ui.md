# Pydantic Validation and Desktop UI

## Purpose

This document explains the Pydantic validation layer and the Tkinter/ttk desktop
interface added to the Software FJ academic project.

## Why Pydantic Is Used in the Application Layer

Pydantic is used only at the application boundary, where external payloads enter the
system from the simulator, tests, or desktop UI.

That keeps the architecture proportional to the assignment:

- domain entities remain dataclasses focused on business rules;
- repositories remain in memory only;
- the application layer validates and normalizes external inputs before domain objects
  are created;
- low-level validation details do not leak directly to the presentation layer.

Implemented input schemas:

- `ClientInput`
- `ServiceInput`
- `ReservationInput`
- `ProcessReservationInput`

Location:

```text
src/software_fj_reservation_system/application/schemas.py
```

## Custom Exception Translation

The system does not expose raw `pydantic.ValidationError` instances to the rest of the
application flow.

Instead, use cases:

1. validate external payloads with Pydantic;
2. catch `ValidationError`;
3. build a clear system-level message;
4. translate the error into the existing custom exception layer;
5. log the controlled failure;
6. re-raise it with `raise ... from` so the original cause is preserved.

Examples of translated exceptions:

- `InvalidDataError`
- `InvalidReservationError`
- `InconsistentCalculationError`

This preserves the academic exception-handling requirements while improving validation
quality and keeping the existing exception package intact.

## Desktop UI Scope

The desktop interface lives in:

```text
src/software_fj_reservation_system/presentation/
```

Main files:

- `controller.py`
- `desktop_app.py`
- `styles.py`

The UI uses:

- `tkinter`
- `tkinter.ttk`
- `ttk.Style`
- `ttk.Notebook`
- `ttk.Treeview`
- `ttk.LabelFrame`
- `ttk.Combobox`
- `ttk.Entry`
- `ttk.Button`

## UI Architecture

The desktop UI does not duplicate business rules.

It creates and uses:

- `ClientRepositoryInMemory`
- `ServiceRepositoryInMemory`
- `ReservationRepositoryInMemory`
- `FileLogger`
- existing application use cases through `ReservationSystemController`

The controller delegates operations to the application layer for:

- client registration
- service creation
- reservation creation
- reservation confirmation
- reservation cancellation
- reservation processing

## UI Features

The desktop application supports:

- dashboard counters for clients, services, and reservations;
- latest operation status;
- client registration form;
- service creation form for room, equipment, and consulting services;
- reservation creation with client/service selection;
- reservation confirmation, cancellation, and processing;
- log viewing with refresh support for `logs/system.log`.

## Visual Design

The UI uses a restrained dark palette aligned with a professional academic tool:

- main background: `#071224`
- primary surface: `#0E1A2B`
- secondary surface: `#132238`
- table/header background: `#1E2B3F`
- border: `#2A3A55`
- main text: `#F8FAFC`
- muted text: `#B6C2D1`
- primary action: `#3B82F6`
- primary action hover: `#2563EB`
- success: `#22C55E`
- error: `#EF4444`
- warning: `#F59E0B`

The interface is styled through centralized `ttk.Style` configuration in:

```text
src/software_fj_reservation_system/presentation/styles.py
```

## Run Commands

Install and sync dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

Run Pylint:

```bash
uv run pylint src tests
```

Run the simulator:

```bash
uv run python -m software_fj_reservation_system.simulation.operations_simulator
```

Run the desktop UI:

```bash
uv run python -m software_fj_reservation_system.presentation.desktop_app
```

If the environment does not include Tk support or there is no display available, use the
import check instead:

```bash
uv run python -c "from software_fj_reservation_system.presentation.desktop_app import ReservationDesktopApp; print('UI import OK')"
```

## Limitations

- clients, services, and reservations are stored only in memory;
- logs are the only file-based persistence;
- the UI depends on Tk availability in the active Python runtime;
- headless environments may only support import-level validation instead of a real window.
