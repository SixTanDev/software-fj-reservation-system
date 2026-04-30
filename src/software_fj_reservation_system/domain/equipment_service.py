"""Equipment service domain model.

This module defines the EquipmentService class.
EquipmentService represents the rental of equipment.
"""

from dataclasses import dataclass

from software_fj_reservation_system.domain.service import Service


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

        if not self.equipment_type or not self.equipment_type.strip():
            raise ValueError("Equipment type cannot be empty.")

    def calculate_cost(self, duration: int) -> float:
        """Calculate equipment service cost.

        For equipment rental, the cost is calculated using the base price
        and the rental duration.
        """
        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")

        return self.base_price * duration

    def describe(self) -> str:
        """Return an equipment service description.

        This description includes the service name and the equipment type.
        """
        return f"{self.name} rental for {self.equipment_type}."