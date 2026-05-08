"""In-memory repository for services."""

from __future__ import annotations

from software_fj_reservation_system.domain.service import Service
from software_fj_reservation_system.infrastructure._base_repository import (
    BaseInMemoryRepository,
)


class ServiceRepositoryInMemory(BaseInMemoryRepository[Service]):
    """Store services in memory without using files or databases."""

    def __init__(self) -> None:
        super().__init__("service")
