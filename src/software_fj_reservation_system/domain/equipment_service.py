"""Equipment service domain model.

This module defines the EquipmentService class.
EquipmentService represents the rental of equipment.
"""

# pylint: disable=duplicate-code

from dataclasses import dataclass

from software_fj_reservation_system.domain.service import Service
from software_fj_reservation_system.exceptions import InvalidDataError


@dataclass
class EquipmentService(Service):
    """Represent an equipment rental service.

    This class inherits from Service, so it uses the common service structure.

    It also defines its own cost calculation and description,
    demonstrating polymorphism.
    """

    # Type of equipment being rented.
    equipment_type: str = "General equipment"

    def __post_init__(self) -> None:
        """Validate equipment service data after initialization.

        First, it validates the common service data.
        Then, it validates the specific equipment type.
        """
        super().__post_init__()
        try:
            if not self.equipment_type or not self.equipment_type.strip():
                raise ValueError("Equipment type cannot be empty.")
        except ValueError as error:
            raise InvalidDataError(str(error)) from error

    def calculate_cost(
        self,
        duration: int,
        tax_rate: float = 0.0,
        discount_rate: float = 0.0,
    ) -> float:
        """Calculate equipment service cost.

        For equipment rental, the cost is calculated using the base price
        and the rental duration.
        """
        return self._calculate_total_cost(
            duration=duration,
            tax_rate=tax_rate,
            discount_rate=discount_rate,
        )

    def describe(self) -> str:
        """Return an equipment service description.

        This description includes the service name and the equipment type.
        """
        return f"{self.name} rental for {self.equipment_type}."
