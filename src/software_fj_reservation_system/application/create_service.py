"""Use case for service creation."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from software_fj_reservation_system.application.schemas import (
    ServiceInput,
    raise_logged_validation_error,
    summarize_validation_error,
)
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
        validated_input = ServiceInput.model_validate(payload)
        service = _build_service(validated_input)
        repository.add(service)
    except ValidationError as error:
        raise_logged_validation_error(
            logger,
            "create_service",
            state,
            InvalidDataError(
                "Service input validation failed: "
                f"{summarize_validation_error(error)}"
            ),
            error,
        )
    except ManagementSystemError as error:
        logger.log_error("create_service", str(error), error, state=state)
        raise

    logger.log_event(
        "create_service",
        "Service created successfully.",
        state={"service_id": service.id, "service_type": type(service).__name__},
    )
    return service


def _build_service(validated_input: ServiceInput) -> Service:
    """Build a concrete service using a small factory method."""

    service_type = validated_input.service_type
    service_id = validated_input.id or Service.create_id()
    name = validated_input.name
    base_price = validated_input.base_price

    if service_type == "room":
        return RoomService(
            id=service_id,
            name=name,
            base_price=base_price,
            capacity=validated_input.capacity or 1,
        )

    if service_type == "equipment":
        return EquipmentService(
            id=service_id,
            name=name,
            base_price=base_price,
            equipment_type=validated_input.equipment_type or "",
        )

    if service_type == "consulting":
        return ConsultingService(
            id=service_id,
            name=name,
            base_price=base_price,
            consultant_name=validated_input.consultant_name or "",
        )

    raise InvalidDataError(f"Unknown service type '{service_type}'.")
