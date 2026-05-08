"""Reservation domain model.

This module defines the Reservation class.
A reservation connects a client with a service for a specific duration.
"""

from dataclasses import dataclass

from software_fj_reservation_system.domain.client import Client
from software_fj_reservation_system.domain.entity import Entity
from software_fj_reservation_system.domain.service import Service
from software_fj_reservation_system.exceptions import (
    InvalidReservationError,
    OperationNotAllowedError,
    ServiceUnavailableError,
)


@dataclass
class Reservation(Entity):
    """Represent a reservation in the system.

    This class connects the main domain objects:

    - Client
    - Service
    - Duration
    - Reservation status

    It controls the reservation lifecycle using methods such as
    confirm, cancel, and process.
    """

    # Client who makes the reservation.
    client: Client

    # Service being reserved.
    service: Service

    # Duration of the reservation.
    duration: int

    # Initial reservation status.
    status: str = "pending"

    def __post_init__(self) -> None:
        """Validate reservation data after initialization.

        A reservation is valid only if:

        - The client is active.
        - The service is available.
        - The duration is greater than zero.
        """
        self._validate_client()
        self._validate_service()
        self._validate_duration()

    def _validate_client(self) -> None:
        """Validate the reservation client.

        A reservation cannot be created for an inactive client.
        """
        if not self.client.active:
            raise InvalidReservationError("Reservation client must be active.")

    def _validate_service(self) -> None:
        """Validate the reservation service.

        A reservation cannot be created for an unavailable service.
        """
        if not self.service.available:
            raise ServiceUnavailableError("Reservation service must be available.")

    def _validate_duration(self) -> None:
        """Validate the reservation duration.

        The reservation duration must be greater than zero.
        """
        if self.duration <= 0:
            raise InvalidReservationError(
                "Reservation duration must be greater than zero."
            )

    def confirm(self) -> None:
        """Confirm the reservation.

        Only pending reservations can be confirmed.
        """
        if self.status != "pending":
            raise OperationNotAllowedError(
                "Only pending reservations can be confirmed."
            )

        self.status = "confirmed"

    def cancel(self) -> None:
        """Cancel the reservation.

        A reservation cannot be cancelled twice.
        """
        if self.status == "cancelled":
            raise OperationNotAllowedError("Reservation is already cancelled.")
        if self.status == "processed":
            raise OperationNotAllowedError(
                "Processed reservations cannot be cancelled."
            )

        self.status = "cancelled"

    def process(self, tax_rate: float = 0.0, discount_rate: float = 0.0) -> float:
        """Process the reservation and return its total cost.

        Only confirmed reservations can be processed.

        This method also demonstrates polymorphism because it calls
        calculate_cost on the service. The result depends on the actual
        service type: room, equipment, or consulting.
        """
        if self.status != "confirmed":
            raise OperationNotAllowedError(
                "Only confirmed reservations can be processed."
            )

        total_cost = self.service.calculate_cost(
            self.duration,
            tax_rate=tax_rate,
            discount_rate=discount_rate,
        )
        self.status = "processed"
        return total_cost
