"""In-memory repository for clients."""

from __future__ import annotations

from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.infrastructure._base_repository import (
    BaseInMemoryRepository,
)


class ClientRepositoryInMemory(BaseInMemoryRepository[Client]):
    """Store clients in memory without using files or databases."""

    def __init__(self) -> None:
        super().__init__("client")
