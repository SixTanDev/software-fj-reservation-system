"""In-memory repository for reservations."""

from __future__ import annotations

from software_fj_reservation_system.domain.reservation import Reservation
from software_fj_reservation_system.infrastructure._base_repository import (
    BaseInMemoryRepository,
)


class ReservationRepositoryInMemory(BaseInMemoryRepository[Reservation]):
    """Store reservations in memory without using files or databases."""

    def __init__(self) -> None:
        super().__init__("reservation")
