"""Domain object tests for the Software FJ reservation system."""

import pytest

from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.domain.consulting_service import ConsultingService
from software_fj_reservation_system.domain.equipment_service import EquipmentService
from software_fj_reservation_system.domain.reservation import Reservation
from software_fj_reservation_system.domain.room_service import RoomService
from software_fj_reservation_system.exceptions import (
    InconsistentCalculationError,
    InvalidDataError,
    InvalidReservationError,
    OperationNotAllowedError,
    ServiceUnavailableError,
)


def test_create_valid_client() -> None:
    """A valid client should be created with the expected state."""

    client = Client(
        id="client-001",
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )

    assert client.id == "client-001"
    assert client.name == "Juan"
    assert client.active is True


def test_client_validation_is_wrapped_in_invalid_data_error() -> None:
    """Client validation should expose a controlled exception with chaining."""

    with pytest.raises(InvalidDataError) as error_info:
        Client(
            id="client-001",
            name="Juan",
            email="correo-invalido",
            phone="3001234567",
        )

    assert str(error_info.value) == "Client email must be valid."
    assert isinstance(error_info.value.__cause__, ValueError)


def test_room_service_cost_supports_optional_tax_and_discount() -> None:
    """Room services should support cost calculation variants."""

    service = RoomService(
        id="service-room-001",
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    assert service.calculate_cost(2, tax_rate=0.19, discount_rate=0.05) == pytest.approx(
        114000
    )


def test_equipment_service_requires_non_empty_type() -> None:
    """Equipment services should validate their specific payload."""

    with pytest.raises(InvalidDataError):
        EquipmentService(
            id="service-equipment-001",
            name="Portatil",
            base_price=30000,
            equipment_type="",
        )


def test_consulting_service_applies_multiplier() -> None:
    """Consulting services should apply the consulting multiplier."""

    service = ConsultingService(
        id="service-consulting-001",
        name="Asesoria",
        base_price=80000,
        consultant_name="Karen",
    )

    assert service.calculate_cost(2) == pytest.approx(192000)


def test_negative_cost_result_raises_inconsistent_calculation_error() -> None:
    """Inconsistent discounts should be rejected with a controlled exception."""

    service = RoomService(
        id="service-room-001",
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    with pytest.raises(InconsistentCalculationError):
        service.calculate_cost(2, discount_rate=2.0)


def test_reservation_requires_active_client() -> None:
    """Inactive clients should not be able to create reservations."""

    client = Client(
        id="client-001",
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )
    client.deactivate()
    service = RoomService(
        id="service-room-001",
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    with pytest.raises(InvalidReservationError):
        Reservation(
            id="reservation-001",
            client=client,
            service=service,
            duration=2,
        )


def test_reservation_requires_available_service() -> None:
    """Unavailable services should raise the correct reservation error."""

    client = Client(
        id="client-001",
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )
    service = RoomService(
        id="service-room-001",
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )
    service.mark_unavailable()

    with pytest.raises(ServiceUnavailableError):
        Reservation(
            id="reservation-001",
            client=client,
            service=service,
            duration=2,
        )


def test_reservation_can_be_confirmed_and_processed() -> None:
    """Confirmed reservations should process successfully."""

    client = Client(
        id="client-001",
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )
    service = RoomService(
        id="service-room-001",
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )
    reservation = Reservation(
        id="reservation-001",
        client=client,
        service=service,
        duration=2,
    )

    reservation.confirm()
    total_cost = reservation.process()

    assert reservation.status == "processed"
    assert total_cost == pytest.approx(100000)


def test_pending_reservation_cannot_be_processed() -> None:
    """Only confirmed reservations should be processed."""

    client = Client(
        id="client-001",
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )
    service = RoomService(
        id="service-room-001",
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )
    reservation = Reservation(
        id="reservation-001",
        client=client,
        service=service,
        duration=2,
    )

    with pytest.raises(OperationNotAllowedError):
        reservation.process()


def test_processed_reservation_cannot_be_cancelled() -> None:
    """Processed reservations should reject cancellation."""

    client = Client(
        id="client-001",
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )
    service = RoomService(
        id="service-room-001",
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )
    reservation = Reservation(
        id="reservation-001",
        client=client,
        service=service,
        duration=2,
    )
    reservation.confirm()
    reservation.process()

    with pytest.raises(OperationNotAllowedError):
        reservation.cancel()
