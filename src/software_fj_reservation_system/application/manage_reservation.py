"""Use cases for reservation lifecycle management."""

from __future__ import annotations

from typing import Any

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
        reservation_id = str(payload["reservation_id"]).strip()
        reservation = repository.get_by_id(reservation_id)
        state["current_status"] = reservation.status
        total_cost = reservation.process(
            tax_rate=_parse_rate(payload, "tax_rate"),
            discount_rate=_parse_rate(payload, "discount_rate"),
        )
    except KeyError as error:
        wrapped_error = InconsistentCalculationError(
            "Reservation field 'reservation_id' is required."
        )
        logger.log_error(
            "process_reservation",
            str(wrapped_error),
            wrapped_error,
            state=state,
        )
        raise wrapped_error from error
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


def _parse_rate(payload: dict[str, Any], field_name: str) -> float:
    """Parse optional pricing modifiers and chain conversion failures."""

    raw_value = payload.get(field_name, 0.0)
    try:
        return float(raw_value)
    except (TypeError, ValueError) as error:
        raise InconsistentCalculationError(
            f"Reservation field '{field_name}' must be numeric."
        ) from error
