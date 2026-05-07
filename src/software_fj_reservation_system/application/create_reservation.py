"""Use case for reservation creation."""

from __future__ import annotations

from typing import Any

from software_fj_reservation_system.domain.reservation import Reservation
from software_fj_reservation_system.exceptions import (
    InvalidDataError,
    InvalidReservationError,
    ManagementSystemError,
)
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


def create_reservation(
    reservation_repository: ReservationRepositoryInMemory,
    client_repository: ClientRepositoryInMemory,
    service_repository: ServiceRepositoryInMemory,
    logger: FileLogger,
    payload: dict[str, Any],
) -> Reservation:
    """Create and store a reservation from existing client and service data."""

    state = {"payload": payload}

    try:
        reservation_id = _require_text(payload, "id", "Reservation field")
        client_id = _require_text(payload, "client_id", "Reservation field")
        service_id = _require_text(payload, "service_id", "Reservation field")
        duration = _parse_duration(payload)

        reservation = Reservation(
            id=reservation_id,
            client=client_repository.get_by_id(client_id),
            service=service_repository.get_by_id(service_id),
            duration=duration,
        )
        reservation_repository.add(reservation)
    except ManagementSystemError as error:
        logger.log_error("create_reservation", str(error), error, state=state)
        raise

    logger.log_event(
        "create_reservation",
        "Reservation created successfully.",
        state={
            "reservation_id": reservation.id,
            "client_id": reservation.client.id,
            "service_id": reservation.service.id,
            "status": reservation.status,
        },
    )
    return reservation


def _parse_duration(payload: dict[str, Any]) -> int:
    """Parse reservation duration and chain low-level conversion failures."""

    try:
        return int(payload["duration"])
    except KeyError as error:
        raise InvalidReservationError("Reservation field 'duration' is required.") from error
    except (TypeError, ValueError) as error:
        raise InvalidReservationError(
            "Reservation duration must be a valid integer."
        ) from error


def _require_text(payload: dict[str, Any], field_name: str, prefix: str) -> str:
    """Return a required text field or raise a controlled error."""

    try:
        value = str(payload[field_name]).strip()
    except KeyError as error:
        raise InvalidDataError(f"{prefix} '{field_name}' is required.") from error

    if not value:
        raise InvalidDataError(f"{prefix} '{field_name}' cannot be empty.")
    return value
