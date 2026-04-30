"""Service abstraction module."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from software_fj_reservation_system.domain.entity import Entity


@dataclass
class Service(Entity, ABC):
    """Represent an abstract service."""

    name: str
    base_price: float
    available: bool = True

    def __post_init__(self) -> None:
        """Validate service data after initialization."""
        self._validate_name()
        self._validate_base_price()

    def _validate_name(self) -> None:
        """Validate the service name."""
        if not self.name or not self.name.strip():
            raise ValueError("Service name cannot be empty.")

    def _validate_base_price(self) -> None:
        """Validate the service base price."""
        if self.base_price <= 0:
            raise ValueError("Service base price must be greater than zero.")

    @abstractmethod
    def calculate_cost(self, duration: int) -> float:
        """Calculate the service cost."""

    @abstractmethod
    def describe(self) -> str:
        """Return a service description."""

    def mark_unavailable(self) -> None:
        """Mark the service as unavailable."""
        self.available = False

    def mark_available(self) -> None:
        """Mark the service as available."""
        self.available = True