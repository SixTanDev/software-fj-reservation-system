"""Room service domain model."""

from dataclasses import dataclass

from software_fj_reservation_system.domain.service import Service


@dataclass
class RoomService(Service):
    """Represent a room reservation service."""

    capacity: int = 1

    def __post_init__(self) -> None:
        """Validate room service data after initialization."""
        super().__post_init__()
        if self.capacity <= 0:
            raise ValueError("Room capacity must be greater than zero.")

    def calculate_cost(self, duration: int) -> float:
        """Calculate room service cost."""
        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")

        return self.base_price * duration

    def describe(self) -> str:
        """Return a room service description."""
        return f"{self.name} room service for {self.capacity} people."
