"""Reservation domain model."""

from dataclasses import dataclass

from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.domain.entity import Entity
from software_fj_reservation_system.domain.service import Service


@dataclass
class Reservation(Entity):
    """Represent a reservation in the system."""

    client: Client
    service: Service
    duration: int
    status: str = "pending"

    def __post_init__(self) -> None:
        """Validate reservation data after initialization."""
        self._validate_client()
        self._validate_service()
        self._validate_duration()

    def _validate_client(self) -> None:
        """Validate the reservation client."""
        if not self.client.active:
            raise ValueError("Reservation client must be active.")

    def _validate_service(self) -> None:
        """Validate the reservation service."""
        if not self.service.available:
            raise ValueError("Reservation service must be available.")

    def _validate_duration(self) -> None:
        """Validate the reservation duration."""
        if self.duration <= 0:
            raise ValueError("Reservation duration must be greater than zero.")

    def confirm(self) -> None:
        """Confirm the reservation."""
        if self.status != "pending":
            raise ValueError("Only pending reservations can be confirmed.")

        self.status = "confirmed"

    def cancel(self) -> None:
        """Cancel the reservation."""
        if self.status == "cancelled":
            raise ValueError("Reservation is already cancelled.")

        self.status = "cancelled"

    def process(self) -> float:
        """Process the reservation and return its total cost."""
        if self.status != "confirmed":
            raise ValueError("Only confirmed reservations can be processed.")

        self.status = "processed"
        return self.service.calculate_cost(self.duration)
