"""System operations simulator for the Software FJ academic project."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from software_fj_reservation_system.application.create_reservation import (
    create_reservation,
)
from software_fj_reservation_system.application.create_service import create_service
from software_fj_reservation_system.application.manage_reservation import (
    cancel_reservation,
    confirm_reservation,
    process_reservation,
)
from software_fj_reservation_system.application.register_client import register_client
from software_fj_reservation_system.exceptions import ManagementSystemError
from software_fj_reservation_system.infrastructure.client_repository import (
    ClientRepositoryInMemory,
)
from software_fj_reservation_system.infrastructure.file_logger import FileLogger
from software_fj_reservation_system.infrastructure.reservation_repository import (
    ReservationRepositoryInMemory,
)
from software_fj_reservation_system.infrastructure.service_repository import (
    ServiceRepositoryInMemory,
)


def execute_simulation(
    log_path: str | Path = "logs/system.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 3,
) -> list[dict[str, Any]]:
    """Execute controlled valid and invalid operations and return the evidence."""

    results: list[dict[str, Any]] = []
    logger = FileLogger(
        log_path=log_path,
        max_bytes=max_bytes,
        backup_count=backup_count,
    )
    client_repository = ClientRepositoryInMemory()
    service_repository = ServiceRepositoryInMemory()
    reservation_repository = ReservationRepositoryInMemory()

    try:
        try:
            client = register_client(
                client_repository,
                logger,
                {
                    "id": "client-001",
                    "name": "Laura Torres",
                    "email": "laura@softwarefj.com",
                    "phone": "3001234567",
                },
            )
            _record_success(
                results,
                "register_client_valid",
                f"Client created: {client.name}",
            )
        except ManagementSystemError as error:
            _record_controlled_error(results, logger, "register_client_valid", error)

        try:
            register_client(
                client_repository,
                logger,
                {
                    "id": "client-002",
                    "name": "   ",
                    "email": "empty-name@softwarefj.com",
                    "phone": "3001230000",
                },
            )
        except ManagementSystemError as error:
            _record_controlled_error(results, logger, "register_client_empty_name", error)

        _run_operation(
            results,
            logger,
            "register_client_invalid_email",
            lambda: _register_invalid_email(client_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "create_service_room",
            lambda: _create_room_service(service_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "create_service_unknown_type",
            lambda: _create_unknown_service(service_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "create_service_equipment",
            lambda: _create_equipment_service(service_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "create_service_consulting",
            lambda: _create_consulting_service(service_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "create_reservation_valid",
            lambda: _create_primary_reservation(
                reservation_repository,
                client_repository,
                service_repository,
                logger,
            ),
        )
        _run_operation(
            results,
            logger,
            "create_reservation_invalid_duration",
            lambda: _create_invalid_duration_reservation(
                reservation_repository,
                client_repository,
                service_repository,
                logger,
            ),
        )
        _run_operation(
            results,
            logger,
            "confirm_reservation_valid",
            lambda: _confirm_primary_reservation(reservation_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "process_reservation_valid",
            lambda: _process_primary_reservation(reservation_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "create_reservation_for_cancellation",
            lambda: _create_secondary_reservation(
                reservation_repository,
                client_repository,
                service_repository,
                logger,
            ),
        )
        _run_operation(
            results,
            logger,
            "cancel_reservation_valid",
            lambda: _cancel_secondary_reservation(reservation_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "cancel_reservation_invalid",
            lambda: _cancel_secondary_reservation(reservation_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "create_reservation_for_inconsistent_cost",
            lambda: _create_consulting_reservation(
                reservation_repository,
                client_repository,
                service_repository,
                logger,
            ),
        )
        _run_operation(
            results,
            logger,
            "confirm_consulting_reservation",
            lambda: _confirm_consulting_reservation(reservation_repository, logger),
        )
        _run_operation(
            results,
            logger,
            "process_reservation_inconsistent_cost",
            lambda: _process_inconsistent_reservation(reservation_repository, logger),
        )
    except Exception as error:
        logger.log_error(
            "unexpected_simulation_error",
            "Unexpected error interrupted the simulation.",
            error,
            state={"completed_entries": len(results)},
        )
        raise
    finally:
        logger.log_event(
            "simulation_shutdown",
            "Simulation finished and logger will be closed.",
            state={"completed_entries": len(results)},
        )
        logger.close()

    return results


def _run_operation(
    results: list[dict[str, Any]],
    logger: FileLogger,
    operation: str,
    action: Callable[[], str],
) -> None:
    """Execute an operation using try/except/else to prove controlled flow."""

    try:
        message = action()
    except ManagementSystemError as error:
        _record_controlled_error(results, logger, operation, error)
    else:
        _record_success(results, operation, message)


def _record_success(
    results: list[dict[str, Any]],
    operation: str,
    message: str,
) -> None:
    """Store and print a successful simulation result."""

    results.append({"operation": operation, "status": "ok", "message": message})
    print(f"[OK] {operation}: {message}")


def _record_controlled_error(
    results: list[dict[str, Any]],
    logger: FileLogger,
    operation: str,
    error: ManagementSystemError,
) -> None:
    """Store and print a controlled failure and prove the simulation continues."""

    results.append({"operation": operation, "status": "error", "message": str(error)})
    print(f"[ERROR] {operation}: {error}")
    logger.log_event(
        "system_continues_after_error",
        "Simulation continues after controlled error.",
        state={"operation": operation, "error_type": type(error).__name__},
    )
    results.append(
        {
            "operation": "system_continues_after_error",
            "status": "continue",
            "message": f"Continuation confirmed after {operation}.",
        }
    )
    print("[CONTINUE] Simulation continues after controlled error")


def _register_invalid_email(
    client_repository: ClientRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Register a client with invalid email to trigger controlled validation."""

    register_client(
        client_repository,
        logger,
        {
            "id": "client-003",
            "name": "Carlos Diaz",
            "email": "invalid-email",
            "phone": "3001239999",
        },
    )
    return "This message should not be returned."


def _create_room_service(
    service_repository: ServiceRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Create the main room service used by the reservation flow."""

    service = create_service(
        service_repository,
        logger,
        {
            "id": "service-room-001",
            "service_type": "room",
            "name": "Main Training Room",
            "base_price": 50000,
            "capacity": 12,
        },
    )
    return f"Service created: {service.describe()}"


def _create_unknown_service(
    service_repository: ServiceRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Trigger an error by asking for an unknown service type."""

    create_service(
        service_repository,
        logger,
        {
            "id": "service-unknown-001",
            "service_type": "mystery",
            "name": "Unknown Service",
            "base_price": 1000,
        },
    )
    return "This message should not be returned."


def _create_equipment_service(
    service_repository: ServiceRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Create the equipment service used in later reservation tests."""

    service = create_service(
        service_repository,
        logger,
        {
            "id": "service-equipment-001",
            "service_type": "equipment",
            "name": "Projector Rental",
            "base_price": 30000,
            "equipment_type": "Projector",
        },
    )
    return f"Service created: {service.describe()}"


def _create_consulting_service(
    service_repository: ServiceRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Create the consulting service used in later reservation tests."""

    service = create_service(
        service_repository,
        logger,
        {
            "id": "service-consulting-001",
            "service_type": "consulting",
            "name": "Architecture Review",
            "base_price": 90000,
            "consultant_name": "Maria Perez",
        },
    )
    return f"Service created: {service.describe()}"


def _create_primary_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    client_repository: ClientRepositoryInMemory,
    service_repository: ServiceRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Create the main reservation used by confirm and process operations."""

    reservation = create_reservation(
        reservation_repository,
        client_repository,
        service_repository,
        logger,
        {
            "id": "reservation-001",
            "client_id": "client-001",
            "service_id": "service-room-001",
            "duration": 2,
        },
    )
    return f"Reservation created with status {reservation.status}"


def _create_invalid_duration_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    client_repository: ClientRepositoryInMemory,
    service_repository: ServiceRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Trigger chained conversion failure for invalid reservation duration."""

    create_reservation(
        reservation_repository,
        client_repository,
        service_repository,
        logger,
        {
            "id": "reservation-002",
            "client_id": "client-001",
            "service_id": "service-room-001",
            "duration": "two",
        },
    )
    return "This message should not be returned."


def _confirm_primary_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Confirm the main reservation."""

    reservation = confirm_reservation(reservation_repository, logger, "reservation-001")
    return f"Reservation confirmed with status {reservation.status}"


def _process_primary_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Process the main reservation with optional tax and discount values."""

    total_cost = process_reservation(
        reservation_repository,
        logger,
        {
            "reservation_id": "reservation-001",
            "tax_rate": 0.19,
            "discount_rate": 0.05,
        },
    )
    return f"Reservation processed with total cost {total_cost:.2f}"


def _create_secondary_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    client_repository: ClientRepositoryInMemory,
    service_repository: ServiceRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Create a second reservation to exercise cancellation rules."""

    reservation = create_reservation(
        reservation_repository,
        client_repository,
        service_repository,
        logger,
        {
            "id": "reservation-003",
            "client_id": "client-001",
            "service_id": "service-equipment-001",
            "duration": 1,
        },
    )
    return f"Reservation created with status {reservation.status}"


def _cancel_secondary_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Cancel the secondary reservation."""

    reservation = cancel_reservation(reservation_repository, logger, "reservation-003")
    return f"Reservation cancelled with status {reservation.status}"


def _create_consulting_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    client_repository: ClientRepositoryInMemory,
    service_repository: ServiceRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Create a consulting reservation for inconsistent pricing validation."""

    reservation = create_reservation(
        reservation_repository,
        client_repository,
        service_repository,
        logger,
        {
            "id": "reservation-004",
            "client_id": "client-001",
            "service_id": "service-consulting-001",
            "duration": 1,
        },
    )
    return f"Reservation created with status {reservation.status}"


def _confirm_consulting_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Confirm the consulting reservation."""

    reservation = confirm_reservation(reservation_repository, logger, "reservation-004")
    return f"Reservation confirmed with status {reservation.status}"


def _process_inconsistent_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    logger: FileLogger,
) -> str:
    """Trigger an inconsistent pricing calculation for a confirmed reservation."""

    process_reservation(
        reservation_repository,
        logger,
        {
            "reservation_id": "reservation-004",
            "tax_rate": 0.0,
            "discount_rate": 1.5,
        },
    )
    return "This message should not be returned."


if __name__ == "__main__":
    execute_simulation()
