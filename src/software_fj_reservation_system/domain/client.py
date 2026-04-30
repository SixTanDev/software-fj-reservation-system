"""Client domain model.

This module defines the Client class.
The Client class represents a person or customer who can make reservations.
"""

from dataclasses import dataclass, field

from software_fj_reservation_system.domain.entity import Entity


@dataclass
class Client(Entity):
    """Represent a client registered in the system.

    This class demonstrates encapsulation because the client's data is
    validated inside the class before the object is considered valid.
    """

    # Basic client information.
    name: str
    email: str
    phone: str

    # By default, a new client is active.
    active: bool = field(default=True)

    def __post_init__(self) -> None:
        """Validate client data after initialization.

        This method runs automatically after the dataclass object is created.
        It checks that the client has valid information.
        """
        self._validate_name()
        self._validate_email()
        self._validate_phone()

    def _validate_name(self) -> None:
        """Validate the client name.

        The name cannot be empty because every client must be identifiable.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Client name cannot be empty.")

    def _validate_email(self) -> None:
        """Validate the client email.

        This is a basic email validation.
        The system checks that the email contains the @ symbol.
        """
        if not self.email or "@" not in self.email:
            raise ValueError("Client email must be valid.")

    def _validate_phone(self) -> None:
        """Validate the client phone.

        The phone cannot be empty because it is part of the client's data.
        """
        if not self.phone or not self.phone.strip():
            raise ValueError("Client phone cannot be empty.")

    def deactivate(self) -> None:
        """Deactivate the client.

        A deactivated client should not be able to make new reservations.
        """
        self.active = False

    def activate(self) -> None:
        """Activate the client.

        This allows a previously deactivated client to use the system again.
        """
        self.active = True
