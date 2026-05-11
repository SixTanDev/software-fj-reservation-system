"""Use case for reservation creation."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from software_fj_reservation_system.application.schemas import (
    ReservationInput,
    raise_logged_validation_error,
    summarize_validation_error,
)
from software_fj_reservation_system.domain.reservation import Reservation
from software_fj_reservation_system.exceptions import (
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
        validated_input = ReservationInput.model_validate(payload)
        reservation = Reservation(
            id=validated_input.id or Reservation.create_id(),
            client=client_repository.get_by_id(validated_input.client_id),
            service=service_repository.get_by_id(validated_input.service_id),
            duration=validated_input.duration,
        )
        reservation_repository.add(reservation)
    except ValidationError as error:
        raise_logged_validation_error(
            logger,
            "create_reservation",
            state,
            InvalidReservationError(
                "Reservation input validation failed: "
                f"{summarize_validation_error(error)}"
            ),
            error,
        )
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
