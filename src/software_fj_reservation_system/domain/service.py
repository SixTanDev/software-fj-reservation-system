"""Service abstraction module.

This module defines the abstract Service class.
The Service class is the base class for all service types in the system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from software_fj_reservation_system.domain.entity import Entity
from software_fj_reservation_system.exceptions import (
    InconsistentCalculationError,
    InvalidDataError,
)


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
        try:
            self._validate_name()
            self._validate_base_price()
        except ValueError as error:
            raise InvalidDataError(str(error)) from error

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
    def calculate_cost(
        self,
        duration: int,
        tax_rate: float = 0.0,
        discount_rate: float = 0.0,
    ) -> float:
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

    def _calculate_total_cost(
        self,
        duration: int,
        multiplier: float = 1.0,
        tax_rate: float = 0.0,
        discount_rate: float = 0.0,
    ) -> float:
        """Calculate the total cost with optional taxes and discounts.

        Subclasses delegate to this helper so every service validates pricing
        modifiers in a consistent way.
        """
        try:
            if duration <= 0:
                raise ValueError("Duration must be greater than zero.")
            if tax_rate < 0:
                raise ValueError("Tax rate cannot be negative.")
            if discount_rate < 0:
                raise ValueError("Discount rate cannot be negative.")
            if multiplier <= 0:
                raise ValueError("Service multiplier must be greater than zero.")
        except ValueError as error:
            raise InconsistentCalculationError(str(error)) from error

        subtotal = self.base_price * duration * multiplier
        total = subtotal * (1 + tax_rate - discount_rate)

        if total < 0:
            raise InconsistentCalculationError(
                "Calculated total cost cannot be negative."
            )

        return total
