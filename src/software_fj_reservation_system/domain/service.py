"""Service abstraction module.

This module defines the abstract Service class.
The Service class is the base class for all service types in the system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from software_fj_reservation_system.domain.entity import Entity


@dataclass
class Service(Entity, ABC):
    """Represent an abstract service.

    This class demonstrates abstraction because it defines the common
    structure and required behavior for all services.

    It is abstract, so it should not be used directly.
    Instead, specific services should inherit from it.
    """

    # Common information shared by all services.
    name: str
    base_price: float
    available: bool = True

    def __post_init__(self) -> None:
        """Validate service data after initialization.

        Every service must have a valid name and a valid base price.
        """
        self._validate_name()
        self._validate_base_price()

    def _validate_name(self) -> None:
        """Validate the service name.

        The service name cannot be empty.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Service name cannot be empty.")

    def _validate_base_price(self) -> None:
        """Validate the service base price.

        The base price must be greater than zero because services
        must have a valid cost.
        """
        if self.base_price <= 0:
            raise ValueError("Service base price must be greater than zero.")

    @abstractmethod
    def calculate_cost(self, duration: int) -> float:
        """Calculate the service cost.

        This method is abstract because each type of service calculates
        its cost differently.

        This supports polymorphism.
        """

    @abstractmethod
    def describe(self) -> str:
        """Return a service description.

        Each derived service must provide its own description.
        """

    def mark_unavailable(self) -> None:
        """Mark the service as unavailable.

        An unavailable service should not be used in new reservations.
        """
        self.available = False

    def mark_available(self) -> None:
        """Mark the service as available.

        This allows the service to be used again.
        """
        self.available = True
