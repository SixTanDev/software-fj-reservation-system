"""Equipment service domain model."""

from dataclasses import dataclass

from software_fj_reservation_system.domain.service import Service


@dataclass
class EquipmentService(Service):
    """Represent an equipment rental service."""

    equipment_type: str = "General equipment"

    def __post_init__(self) -> None:
        """Validate equipment service data after initialization."""
        super().__post_init__()
        if not self.equipment_type or not self.equipment_type.strip():
            raise ValueError("Equipment type cannot be empty.")

    def calculate_cost(self, duration: int) -> float:
        """Calculate equipment service cost."""
        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")

        return self.base_price * duration

    def describe(self) -> str:
        """Return an equipment service description."""
        return f"{self.name} rental for {self.equipment_type}."