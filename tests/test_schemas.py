"""Tests for Pydantic schemas and validation error translation."""

# pylint: disable=duplicate-code

from pathlib import Path

import pytest
from pydantic import ValidationError

from software_fj_reservation_system.application.create_reservation import (
    create_reservation,
)
from software_fj_reservation_system.application.manage_reservation import (
    process_reservation,
)
from software_fj_reservation_system.application.register_client import register_client
from software_fj_reservation_system.application.schemas import (
    ClientInput,
    ProcessReservationInput,
    ReservationInput,
    ServiceInput,
)
from software_fj_reservation_system.exceptions import (
    InconsistentCalculationError,
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


def test_client_schema_accepts_valid_payload() -> None:
    """A valid client payload should be accepted by the Pydantic schema."""

    validated = ClientInput.model_validate(
        {
            "name": "Laura Torres",
            "email": "laura@softwarefj.com",
            "phone": "3001234567",
        }
    )

    assert validated.name == "Laura Torres"
    assert str(validated.email) == "laura@softwarefj.com"


def test_client_schema_rejects_empty_name() -> None:
    """Client names must not be empty after whitespace stripping."""

    with pytest.raises(ValidationError):
        ClientInput.model_validate(
            {
                "name": "   ",
                "email": "laura@softwarefj.com",
                "phone": "3001234567",
            }
        )


def test_client_schema_rejects_invalid_email() -> None:
    """Client email addresses must be valid."""

    with pytest.raises(ValidationError):
        ClientInput.model_validate(
            {
                "name": "Laura Torres",
                "email": "invalid-email",
                "phone": "3001234567",
            }
        )


def test_service_schema_rejects_unknown_service_type() -> None:
    """Unknown service types must be rejected before the domain layer runs."""

    with pytest.raises(ValidationError):
        ServiceInput.model_validate(
            {
                "service_type": "unknown",
                "name": "Unsupported",
                "base_price": 1000,
            }
        )


def test_service_schema_rejects_negative_price() -> None:
    """Services must have a positive base price."""

    with pytest.raises(ValidationError):
        ServiceInput.model_validate(
            {
                "service_type": "room",
                "name": "Main room",
                "base_price": -10,
                "capacity": 12,
            }
        )


def test_reservation_schema_rejects_invalid_duration() -> None:
    """Reservation durations must be positive integers."""

    with pytest.raises(ValidationError):
        ReservationInput.model_validate(
            {
                "client_id": "client-001",
                "service_id": "service-001",
                "duration": 0,
            }
        )


def test_process_reservation_schema_rejects_invalid_rates() -> None:
    """Tax and discount rates must stay within the supported range."""

    with pytest.raises(ValidationError):
        ProcessReservationInput.model_validate(
            {
                "reservation_id": "reservation-001",
                "tax_rate": -0.1,
                "discount_rate": 0.97,
            }
        )


def test_register_client_wraps_pydantic_validation_error(tmp_path: Path) -> None:
    """Use cases must translate Pydantic validation failures into custom exceptions."""

    logger = FileLogger(log_path=tmp_path / "logs" / "system.log")
    repository = ClientRepositoryInMemory()

    with pytest.raises(InvalidDataError) as error_info:
        register_client(
            repository,
            logger,
            {
                "name": "",
                "email": "invalid-email",
                "phone": "123",
            },
        )

    logger.close()
    assert isinstance(error_info.value.__cause__, ValidationError)


def test_create_reservation_wraps_pydantic_validation_error(tmp_path: Path) -> None:
    """Reservation creation must chain the Pydantic failure into the custom error."""

    logger = FileLogger(log_path=tmp_path / "logs" / "system.log")
    reservation_repository = ReservationRepositoryInMemory()
    client_repository = ClientRepositoryInMemory()
    service_repository = ServiceRepositoryInMemory()

    with pytest.raises(InvalidReservationError) as error_info:
        create_reservation(
            reservation_repository,
            client_repository,
            service_repository,
            logger,
            {
                "client_id": "client-001",
                "service_id": "service-001",
                "duration": "two",
            },
        )

    logger.close()
    assert isinstance(error_info.value.__cause__, ValidationError)


def test_process_reservation_wraps_pydantic_validation_error(tmp_path: Path) -> None:
    """Reservation processing must expose a custom calculation error with chaining."""

    logger = FileLogger(log_path=tmp_path / "logs" / "system.log")
    repository = ReservationRepositoryInMemory()

    with pytest.raises(InconsistentCalculationError) as error_info:
        process_reservation(
            repository,
            logger,
            {"reservation_id": "", "tax_rate": 0.1, "discount_rate": 0.1},
        )

    logger.close()
    assert isinstance(error_info.value.__cause__, ValidationError)
