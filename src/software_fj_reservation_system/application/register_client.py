"""Use case for client registration."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from software_fj_reservation_system.application.schemas import (
    ClientInput,
    raise_logged_validation_error,
    summarize_validation_error,
)
from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.exceptions import InvalidDataError, ManagementSystemError
from software_fj_reservation_system.infrastructure.client_repository import (
    ClientRepositoryInMemory,
)
from software_fj_reservation_system.infrastructure.file_logger import FileLogger


def register_client(
    repository: ClientRepositoryInMemory,
    logger: FileLogger,
    payload: dict[str, Any],
) -> Client:
    """Create and store a client, logging both success and controlled failures."""

    state = {"payload": payload}

    try:
        validated_input = ClientInput.model_validate(payload)
        client = Client(
            id=validated_input.id or Client.create_id(),
            name=validated_input.name,
            email=str(validated_input.email),
            phone=validated_input.phone,
        )
        repository.add(client)
    except ValidationError as error:
        raise_logged_validation_error(
            logger,
            "register_client",
            state,
            InvalidDataError(
                "Client input validation failed: "
                f"{summarize_validation_error(error)}"
            ),
            error,
        )
    except ManagementSystemError as error:
        logger.log_error("register_client", str(error), error, state=state)
        raise

    logger.log_event(
        "register_client",
        "Client created successfully.",
        state={"client_id": client.id, "active": client.active},
    )
    return client
