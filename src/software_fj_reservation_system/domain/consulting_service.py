"""Consulting service domain model.

This module defines the ConsultingService class.
ConsultingService represents a specialized consulting service.
"""

from dataclasses import dataclass

from software_fj_reservation_system.domain.service import Service


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

        if not self.consultant_name or not self.consultant_name.strip():
            raise ValueError("Consultant name cannot be empty.")

    def calculate_cost(self, duration: int) -> float:
        """Calculate consulting service cost.

        Consulting services have an additional fee because they require
        specialized knowledge.
        """
        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")

        # Consulting services are 20% more expensive than the base calculation.
        consulting_fee = 1.2

        return self.base_price * duration * consulting_fee

    def describe(self) -> str:
        """Return a consulting service description.

        This description includes the service name and consultant name.
        """
        return f"{self.name} consulting service with {self.consultant_name}."