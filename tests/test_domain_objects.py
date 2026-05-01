"""Basic domain object tests.

These tests verify that the main domain objects can be created correctly
and that their basic validations work.
"""

import pytest

from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.domain.consulting_service import ConsultingService
from software_fj_reservation_system.domain.equipment_service import EquipmentService
from software_fj_reservation_system.domain.reservation import Reservation
from software_fj_reservation_system.domain.room_service import RoomService


def test_create_valid_client() -> None:
    """Verify that a valid client can be created."""
    client = Client(
        id=1,
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )

    assert client.id == 1
    assert client.name == "Juan"
    assert client.email == "juan@email.com"
    assert client.phone == "3001234567"
    assert client.active is True


def test_client_name_cannot_be_empty() -> None:
    """Verify that an empty client name raises an error."""
    with pytest.raises(ValueError):
        Client(
            id=1,
            name="",
            email="juan@email.com",
            phone="3001234567",
        )


def test_client_email_must_be_valid() -> None:
    """Verify that an invalid email raises an error."""
    with pytest.raises(ValueError):
        Client(
            id=1,
            name="Juan",
            email="correo-invalido",
            phone="3001234567",
        )


def test_client_phone_cannot_be_empty() -> None:
    """Verify that an empty phone raises an error."""
    with pytest.raises(ValueError):
        Client(
            id=1,
            name="Juan",
            email="juan@email.com",
            phone="",
        )


def test_client_can_be_deactivated_and_activated() -> None:
    """Verify that a client can be deactivated and activated again."""
    client = Client(
        id=1,
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )

    client.deactivate()
    assert client.active is False

    client.activate()
    assert client.active is True


def test_create_room_service() -> None:
    """Verify that a room service can be created."""
    service = RoomService(
        id=1,
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    assert service.id == 1
    assert service.name == "Sala principal"
    assert service.base_price == 50000
    assert service.capacity == 10
    assert service.available is True


def test_room_service_calculates_cost() -> None:
    """Verify that room service cost is calculated correctly."""
    service = RoomService(
        id=1,
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    assert service.calculate_cost(2) == 100000


def test_room_service_capacity_must_be_greater_than_zero() -> None:
    """Verify that room capacity must be greater than zero."""
    with pytest.raises(ValueError):
        RoomService(
            id=1,
            name="Sala inválida",
            base_price=50000,
            capacity=0,
        )


def test_create_equipment_service() -> None:
    """Verify that an equipment service can be created."""
    service = EquipmentService(
        id=2,
        name="Alquiler de portátil",
        base_price=30000,
        equipment_type="Laptop",
    )

    assert service.id == 2
    assert service.name == "Alquiler de portátil"
    assert service.base_price == 30000
    assert service.equipment_type == "Laptop"
    assert service.available is True


def test_equipment_service_calculates_cost() -> None:
    """Verify that equipment service cost is calculated correctly."""
    service = EquipmentService(
        id=2,
        name="Alquiler de portátil",
        base_price=30000,
        equipment_type="Laptop",
    )

    assert service.calculate_cost(3) == 90000


def test_equipment_type_cannot_be_empty() -> None:
    """Verify that equipment type cannot be empty."""
    with pytest.raises(ValueError):
        EquipmentService(
            id=2,
            name="Alquiler de portátil",
            base_price=30000,
            equipment_type="",
        )


def test_create_consulting_service() -> None:
    """Verify that a consulting service can be created."""
    service = ConsultingService(
        id=3,
        name="Asesoría en Python",
        base_price=80000,
        consultant_name="Karen",
    )

    assert service.id == 3
    assert service.name == "Asesoría en Python"
    assert service.base_price == 80000
    assert service.consultant_name == "Karen"
    assert service.available is True


def test_consulting_service_calculates_cost_with_extra_fee() -> None:
    """Verify that consulting service applies the 20 percent extra fee."""
    service = ConsultingService(
        id=3,
        name="Asesoría en Python",
        base_price=80000,
        consultant_name="Karen",
    )

    assert service.calculate_cost(2) == 192000


def test_consultant_name_cannot_be_empty() -> None:
    """Verify that consultant name cannot be empty."""
    with pytest.raises(ValueError):
        ConsultingService(
            id=3,
            name="Asesoría en Python",
            base_price=80000,
            consultant_name="",
        )


def test_create_valid_reservation() -> None:
    """Verify that a valid reservation can be created."""
    client = Client(
        id=1,
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )

    service = RoomService(
        id=1,
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    reservation = Reservation(
        id=1,
        client=client,
        service=service,
        duration=2,
    )

    assert reservation.id == 1
    assert reservation.client == client
    assert reservation.service == service
    assert reservation.duration == 2
    assert reservation.status == "pending"


def test_reservation_duration_must_be_greater_than_zero() -> None:
    """Verify that reservation duration must be greater than zero."""
    client = Client(
        id=1,
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )

    service = RoomService(
        id=1,
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    with pytest.raises(ValueError):
        Reservation(
            id=1,
            client=client,
            service=service,
            duration=0,
        )


def test_reservation_cannot_be_created_for_inactive_client() -> None:
    """Verify that inactive clients cannot make reservations."""
    client = Client(
        id=1,
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )
    client.deactivate()

    service = RoomService(
        id=1,
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    with pytest.raises(ValueError):
        Reservation(
            id=1,
            client=client,
            service=service,
            duration=2,
        )


def test_reservation_can_be_confirmed_and_processed() -> None:
    """Verify reservation lifecycle from pending to processed."""
    client = Client(
        id=1,
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )

    service = RoomService(
        id=1,
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    reservation = Reservation(
        id=1,
        client=client,
        service=service,
        duration=2,
    )

    reservation.confirm()
    assert reservation.status == "confirmed"

    total_cost = reservation.process()
    assert total_cost == 100000
    assert reservation.status == "processed"


def test_pending_reservation_cannot_be_processed() -> None:
    """Verify that only confirmed reservations can be processed."""
    client = Client(
        id=1,
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )

    service = RoomService(
        id=1,
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    reservation = Reservation(
        id=1,
        client=client,
        service=service,
        duration=2,
    )

    with pytest.raises(ValueError):
        reservation.process()


def test_reservation_can_be_cancelled() -> None:
    """Verify that a reservation can be cancelled."""
    client = Client(
        id=1,
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )

    service = RoomService(
        id=1,
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    reservation = Reservation(
        id=1,
        client=client,
        service=service,
        duration=2,
    )

    reservation.cancel()
    assert reservation.status == "cancelled"


def test_cancelled_reservation_cannot_be_cancelled_again() -> None:
    """Verify that a cancelled reservation cannot be cancelled twice."""
    client = Client(
        id=1,
        name="Juan",
        email="juan@email.com",
        phone="3001234567",
    )

    service = RoomService(
        id=1,
        name="Sala principal",
        base_price=50000,
        capacity=10,
    )

    reservation = Reservation(
        id=1,
        client=client,
        service=service,
        duration=2,
    )

    reservation.cancel()

    with pytest.raises(ValueError):
        reservation.cancel()
