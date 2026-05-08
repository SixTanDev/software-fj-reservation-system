"""Tests for the in-memory repositories."""

from __future__ import annotations

import builtins

import pytest

from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.domain.reservation import Reservation
from software_fj_reservation_system.domain.room_service import RoomService
from software_fj_reservation_system.exceptions import InvalidDataError
from software_fj_reservation_system.infrastructure.client_repository import (
    ClientRepositoryInMemory,
)
from software_fj_reservation_system.infrastructure.reservation_repository import (
    ReservationRepositoryInMemory,
)
from software_fj_reservation_system.infrastructure.service_repository import (
    ServiceRepositoryInMemory,
)


def test_client_repository_stores_data_in_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    """Repository operations should succeed without opening files."""

    monkeypatch.setattr(
        builtins,
        "open",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("open() not allowed")),
    )
    repository = ClientRepositoryInMemory()
    client = _build_client()

    repository.add(client)

    assert repository.get_by_id("client-001") is client
    assert repository.list_all() == [client]


def test_service_repository_rejects_duplicate_ids() -> None:
    """Duplicate service identifiers should be rejected."""

    repository = ServiceRepositoryInMemory()
    service = _build_service()
    repository.add(service)

    with pytest.raises(InvalidDataError):
        repository.add(service)


def test_reservation_repository_returns_stored_reservation() -> None:
    """Reservations should remain available in the in-memory store."""

    repository = ReservationRepositoryInMemory()
    reservation = _build_reservation()
    repository.add(reservation)

    assert repository.get_by_id("reservation-001") is reservation


def _build_client() -> Client:
    """Create a valid reusable client fixture."""

    return Client(
        id="client-001",
        name="Ana",
        email="ana@softwarefj.com",
        phone="3001234567",
    )


def _build_service() -> RoomService:
    """Create a valid reusable service fixture."""

    return RoomService(
        id="service-room-001",
        name="Sala principal",
        base_price=50000,
        capacity=12,
    )


def _build_reservation() -> Reservation:
    """Create a valid reusable reservation fixture."""

    return Reservation(
        id="reservation-001",
        client=_build_client(),
        service=_build_service(),
        duration=2,
    )
