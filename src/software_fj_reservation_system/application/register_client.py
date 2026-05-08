"""Use case for client registration."""

from __future__ import annotations

from typing import Any

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
        client = Client(
            id=_require_text(payload, "id"),
            name=_require_text(payload, "name"),
            email=_require_text(payload, "email"),
            phone=_require_text(payload, "phone"),
        )
        repository.add(client)
    except ManagementSystemError as error:
        logger.log_error("register_client", str(error), error, state=state)
        raise

    logger.log_event(
        "register_client",
        "Client created successfully.",
        state={"client_id": client.id, "active": client.active},
    )
    return client


def _require_text(payload: dict[str, Any], field_name: str) -> str:
    """Return a required text field or raise a controlled error."""

    try:
        value = str(payload[field_name]).strip()
    except KeyError as error:
        raise InvalidDataError(f"Client field '{field_name}' is required.") from error

    if not value:
        raise InvalidDataError(f"Client field '{field_name}' cannot be empty.")
    return value
