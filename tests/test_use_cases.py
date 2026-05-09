"""Application use case tests."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from software_fj_reservation_system.application.create_reservation import (
    create_reservation,
)
from software_fj_reservation_system.application.create_service import create_service
from software_fj_reservation_system.application.manage_reservation import (
    confirm_reservation,
    process_reservation,
)
from software_fj_reservation_system.application.register_client import register_client
from software_fj_reservation_system.exceptions import (
    InvalidDataError,
    InvalidReservationError,
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


def test_successful_use_case_flow_logs_events(tmp_path: Path) -> None:
    """A valid end-to-end flow should succeed and leave event evidence in the log."""

    log_path = tmp_path / "logs" / "system.log"
    logger = FileLogger(log_path=log_path)
    client_repository = ClientRepositoryInMemory()
    service_repository = ServiceRepositoryInMemory()
    reservation_repository = ReservationRepositoryInMemory()
    repositories = (
        reservation_repository,
        client_repository,
        service_repository,
    )

    client = register_client(
        client_repository,
        logger,
        _client_payload(),
    )
    service = create_service(
        service_repository,
        logger,
        _room_service_payload(),
    )
    reservation = create_reservation(
        *repositories,
        logger,
        _reservation_payload(client.id, service.id, duration=2),
    )
    confirm_reservation(reservation_repository, logger, reservation.id)
    total_cost = process_reservation(
        reservation_repository,
        logger,
        {"reservation_id": reservation.id, "tax_rate": 0.19, "discount_rate": 0.05},
    )
    logger.close()

    assert total_cost == pytest.approx(114000)
    content = log_path.read_text(encoding="utf-8")
    assert "Client created successfully." in content
    assert "Service created successfully." in content
    assert "Reservation processed successfully." in content


def test_controlled_error_is_logged_by_use_case(tmp_path: Path) -> None:
    """A controlled use case failure should be persisted in the log."""

    log_path = tmp_path / "logs" / "system.log"
    logger = FileLogger(log_path=log_path)
    service_repository = ServiceRepositoryInMemory()

    with pytest.raises(InvalidDataError):
        create_service(
            service_repository,
            logger,
            {
                **_room_service_payload(),
                "id": "service-unknown-001",
                "service_type": "unknown",
                "name": "Service",
                "base_price": 1000,
            },
        )

    logger.close()
    content = log_path.read_text(encoding="utf-8")
    assert "Service input validation failed" in content
    assert "Unknown service type 'unknown'." in content


def test_create_service_preserves_exception_chaining(tmp_path: Path) -> None:
    """Pydantic validation failures should be chained to the application error."""

    logger = FileLogger(log_path=tmp_path / "logs" / "system.log")
    service_repository = ServiceRepositoryInMemory()

    with pytest.raises(InvalidDataError) as error_info:
        create_service(
            service_repository,
            logger,
            {
                **_room_service_payload(),
                "base_price": "not-a-number",
                "capacity": 10,
            },
        )

    logger.close()
    assert isinstance(error_info.value.__cause__, ValidationError)


def test_create_reservation_preserves_exception_chaining(tmp_path: Path) -> None:
    """Pydantic failures should be chained to the controlled reservation error."""

    logger = FileLogger(log_path=tmp_path / "logs" / "system.log")
    client_repository = ClientRepositoryInMemory()
    service_repository = ServiceRepositoryInMemory()
    reservation_repository = ReservationRepositoryInMemory()
    repositories = (
        reservation_repository,
        client_repository,
        service_repository,
    )

    register_client(
        client_repository,
        logger,
        _client_payload(),
    )
    create_service(
        service_repository,
        logger,
        _room_service_payload(),
    )

    with pytest.raises(InvalidReservationError) as error_info:
        create_reservation(
            *repositories,
            logger,
            _reservation_payload("client-001", "service-room-001", duration="two"),
        )

    logger.close()
    assert isinstance(error_info.value.__cause__, ValidationError)


def _client_payload() -> dict[str, str]:
    """Return a reusable client payload."""

    return {
        "id": "client-001",
        "name": "Laura Torres",
        "email": "laura@softwarefj.com",
        "phone": "3001234567",
    }


def _room_service_payload() -> dict[str, object]:
    """Return a reusable room service payload."""

    return {
        "id": "service-room-001",
        "service_type": "room",
        "name": "Sala principal",
        "base_price": 50000,
        "capacity": 12,
    }


def _reservation_payload(
    client_id: str,
    service_id: str,
    duration: object,
) -> dict[str, object]:
    """Return a reusable reservation payload."""

    return {
        "id": "reservation-001",
        "client_id": client_id,
        "service_id": service_id,
        "duration": duration,
    }
