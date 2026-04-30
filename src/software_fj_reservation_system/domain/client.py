"""Client domain model."""

from dataclasses import dataclass, field

from software_fj_reservation_system.domain.entity import Entity


@dataclass
class Client(Entity):
    """Represent a system client."""

    name: str
    email: str
    phone: str
    active: bool = field(default=True)

    def __post_init__(self) -> None:
        """Validate client data after initialization."""
        self._validate_name()
        self._validate_email()
        self._validate_phone()

    def _validate_name(self) -> None:
        """Validate the client name."""
        if not self.name or not self.name.strip():
            raise ValueError("Client name cannot be empty.")

    def _validate_email(self) -> None:
        """Validate the client email."""
        if not self.email or "@" not in self.email:
            raise ValueError("Client email must be valid.")

    def _validate_phone(self) -> None:
        """Validate the client phone."""
        if not self.phone or not self.phone.strip():
            raise ValueError("Client phone cannot be empty.")

    def deactivate(self) -> None:
        """Deactivate the client."""
        self.active = False

    def activate(self) -> None:
        """Activate the client."""
        self.active = True