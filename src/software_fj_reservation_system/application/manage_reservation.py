"""Use cases for reservation lifecycle management."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from software_fj_reservation_system.application.schemas import (
    ProcessReservationInput,
    raise_logged_validation_error,
    summarize_validation_error,
)
from software_fj_reservation_system.domain.reservation import Reservation
from software_fj_reservation_system.exceptions import (
    InconsistentCalculationError,
    ManagementSystemError,
)
from software_fj_reservation_system.infrastructure.file_logger import FileLogger
from software_fj_reservation_system.infrastructure.reservation_repository import (
    ReservationRepositoryInMemory,
)


def confirm_reservation(
    repository: ReservationRepositoryInMemory,
    logger: FileLogger,
    reservation_id: object,
) -> Reservation:
    """Confirm a reservation and log the resulting state transition."""

    state = {"reservation_id": str(reservation_id)}

    try:
        reservation = repository.get_by_id(reservation_id)
        state["current_status"] = reservation.status
        reservation.confirm()
    except ManagementSystemError as error:
        logger.log_error("confirm_reservation", str(error), error, state=state)
        raise

    logger.log_event(
        "confirm_reservation",
        "Reservation confirmed successfully.",
        state={"reservation_id": reservation.id, "status": reservation.status},
    )
    return reservation


def cancel_reservation(
    repository: ReservationRepositoryInMemory,
    logger: FileLogger,
    reservation_id: object,
) -> Reservation:
    """Cancel a reservation and log the resulting state transition."""

    state = {"reservation_id": str(reservation_id)}

    try:
        reservation = repository.get_by_id(reservation_id)
        state["current_status"] = reservation.status
        reservation.cancel()
    except ManagementSystemError as error:
        logger.log_error("cancel_reservation", str(error), error, state=state)
        raise

    logger.log_event(
        "cancel_reservation",
        "Reservation cancelled successfully.",
        state={"reservation_id": reservation.id, "status": reservation.status},
    )
    return reservation


def process_reservation(
    repository: ReservationRepositoryInMemory,
    logger: FileLogger,
    payload: dict[str, Any],
) -> float:
    """Process a confirmed reservation and return the calculated total."""

    state = {"payload": payload}

    try:
        validated_input = ProcessReservationInput.model_validate(payload)
        reservation = repository.get_by_id(validated_input.reservation_id)
        state["current_status"] = reservation.status
        total_cost = reservation.process(
            tax_rate=validated_input.tax_rate,
            discount_rate=validated_input.discount_rate,
        )
    except ValidationError as error:
        raise_logged_validation_error(
            logger,
            "process_reservation",
            state,
            InconsistentCalculationError(
                "Reservation processing input validation failed: "
                f"{summarize_validation_error(error)}"
            ),
            error,
        )
    except ManagementSystemError as error:
        logger.log_error("process_reservation", str(error), error, state=state)
        raise

    logger.log_event(
        "process_reservation",
        "Reservation processed successfully.",
        state={
            "reservation_id": reservation.id,
            "status": reservation.status,
            "total_cost": total_cost,
        },
    )
    return total_cost
