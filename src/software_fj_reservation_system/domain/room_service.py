"""Room service domain model.

This module defines the RoomService class.
RoomService represents the reservation of a physical room.
"""

from dataclasses import dataclass

from software_fj_reservation_system.domain.service import Service
from software_fj_reservation_system.exceptions import InvalidDataError


@dataclass
class RoomService(Service):
    """Represent a room reservation service.

    This class inherits from Service, so it demonstrates inheritance.

    It also implements calculate_cost and describe in its own way,
    which demonstrates polymorphism.
    """

    # Number of people that can use the room.
    capacity: int = 1

    def __post_init__(self) -> None:
        """Validate room service data after initialization.

        First, it validates the common service data using the parent class.
        Then, it validates the specific room capacity.
        """
        super().__post_init__()
        try:
            if self.capacity <= 0:
                raise ValueError("Room capacity must be greater than zero.")
        except ValueError as error:
            raise InvalidDataError(str(error)) from error

    def calculate_cost(
        self,
        duration: int,
        tax_rate: float = 0.0,
        discount_rate: float = 0.0,
    ) -> float:
        """Calculate room service cost.

        For rooms, the cost is calculated by multiplying the base price
        by the reservation duration.
        """
        return self._calculate_total_cost(
            duration=duration,
            tax_rate=tax_rate,
            discount_rate=discount_rate,
        )

    def describe(self) -> str:
        """Return a room service description.

        This description includes the name of the service and the room capacity.
        """
        return f"{self.name} room service for {self.capacity} people."
