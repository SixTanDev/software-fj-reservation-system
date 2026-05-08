"""Use case for service creation."""

from __future__ import annotations

from typing import Any

from software_fj_reservation_system.domain.consulting_service import ConsultingService
from software_fj_reservation_system.domain.equipment_service import EquipmentService
from software_fj_reservation_system.domain.room_service import RoomService
from software_fj_reservation_system.domain.service import Service
from software_fj_reservation_system.exceptions import InvalidDataError, ManagementSystemError
from software_fj_reservation_system.infrastructure.file_logger import FileLogger
from software_fj_reservation_system.infrastructure.service_repository import (
    ServiceRepositoryInMemory,
)


def create_service(
    repository: ServiceRepositoryInMemory,
    logger: FileLogger,
    payload: dict[str, Any],
) -> Service:
    """Create a concrete service from the requested service type."""

    state = {"payload": payload}

    try:
        service = _build_service(payload)
        repository.add(service)
    except ManagementSystemError as error:
        logger.log_error("create_service", str(error), error, state=state)
        raise

    logger.log_event(
        "create_service",
        "Service created successfully.",
        state={"service_id": service.id, "service_type": type(service).__name__},
    )
    return service


def _build_service(payload: dict[str, Any]) -> Service:
    """Build a concrete service using a small factory method."""

    service_type = _require_text(payload, "service_type").lower()
    service_id = _require_text(payload, "id")
    name = _require_text(payload, "name")
    base_price = _parse_float(payload, "base_price", "Service base price must be numeric.")

    if service_type == "room":
        capacity = _parse_int(payload, "capacity", "Room capacity must be numeric.")
        return RoomService(
            id=service_id,
            name=name,
            base_price=base_price,
            capacity=capacity,
        )

    if service_type == "equipment":
        equipment_type = _require_text(payload, "equipment_type")
        return EquipmentService(
            id=service_id,
            name=name,
            base_price=base_price,
            equipment_type=equipment_type,
        )

    if service_type == "consulting":
        consultant_name = _require_text(payload, "consultant_name")
        return ConsultingService(
            id=service_id,
            name=name,
            base_price=base_price,
            consultant_name=consultant_name,
        )

    raise InvalidDataError(f"Unknown service type '{service_type}'.")


def _require_text(payload: dict[str, Any], field_name: str) -> str:
    """Return a required text field or raise a controlled error."""

    try:
        value = str(payload[field_name]).strip()
    except KeyError as error:
        raise InvalidDataError(f"Service field '{field_name}' is required.") from error

    if not value:
        raise InvalidDataError(f"Service field '{field_name}' cannot be empty.")
    return value


def _parse_float(payload: dict[str, Any], field_name: str, message: str) -> float:
    """Parse a numeric field and chain low-level parsing failures."""

    try:
        return float(payload[field_name])
    except KeyError as error:
        raise InvalidDataError(f"Service field '{field_name}' is required.") from error
    except (TypeError, ValueError) as error:
        raise InvalidDataError(message) from error


def _parse_int(payload: dict[str, Any], field_name: str, message: str) -> int:
    """Parse an integer field and chain low-level parsing failures."""

    try:
        return int(payload[field_name])
    except KeyError as error:
        raise InvalidDataError(f"Service field '{field_name}' is required.") from error
    except (TypeError, ValueError) as error:
        raise InvalidDataError(message) from error
