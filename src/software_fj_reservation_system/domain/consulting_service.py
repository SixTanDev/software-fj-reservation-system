"""Consulting service domain model."""

from dataclasses import dataclass

from software_fj_reservation_system.domain.service import Service


@dataclass
class ConsultingService(Service):
    """Represent a specialized consulting service."""

    consultant_name: str = "Assigned consultant"

    def __post_init__(self) -> None:
        """Validate consulting service data after initialization."""
        super().__post_init__()
        if not self.consultant_name or not self.consultant_name.strip():
            raise ValueError("Consultant name cannot be empty.")

    def calculate_cost(self, duration: int) -> float:
        """Calculate consulting service cost."""
        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")

        consulting_fee = 1.2
        return self.base_price * duration * consulting_fee

    def describe(self) -> str:
        """Return a consulting service description."""
        return f"{self.name} consulting service with {self.consultant_name}."