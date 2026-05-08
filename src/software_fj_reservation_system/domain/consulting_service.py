"""Consulting service domain model.

This module defines the ConsultingService class.
ConsultingService represents a specialized consulting service.
"""

from dataclasses import dataclass

from software_fj_reservation_system.domain.service import Service
from software_fj_reservation_system.exceptions import InvalidDataError


@dataclass
class ConsultingService(Service):
    """Represent a specialized consulting service.

    This class inherits from Service.

    Its cost calculation is different from the other services,
    which demonstrates polymorphism.
    """

    # Name of the consultant assigned to the service.
    consultant_name: str = "Assigned consultant"

    def __post_init__(self) -> None:
        """Validate consulting service data after initialization.

        First, it validates the common service data.
        Then, it validates the consultant name.
        """
        super().__post_init__()
        try:
            if not self.consultant_name or not self.consultant_name.strip():
                raise ValueError("Consultant name cannot be empty.")
        except ValueError as error:
            raise InvalidDataError(str(error)) from error

    def calculate_cost(
        self,
        duration: int,
        tax_rate: float = 0.0,
        discount_rate: float = 0.0,
    ) -> float:
        """Calculate consulting service cost.

        Consulting services have an additional fee because they require
        specialized knowledge.
        """
        return self._calculate_total_cost(
            duration=duration,
            multiplier=1.2,
            tax_rate=tax_rate,
            discount_rate=discount_rate,
        )

    def describe(self) -> str:
        """Return a consulting service description.

        This description includes the service name and consultant name.
        """
        return f"{self.name} consulting service with {self.consultant_name}."
