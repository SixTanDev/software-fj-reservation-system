"""Base entity module.

This module defines the base class used by the domain entities.
A domain entity is an object that has its own identity.
"""

from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Entity:
    """Base entity for domain objects.

    This class is used as a parent class for other domain classes,
    such as Client, Service, and Reservation.

    The goal is to avoid repeating the `id` attribute in every class.
    """

    # Unique identifier for each entity.
    id: str

    @classmethod
    def create_id(cls) -> str:
        """Create a unique entity identifier.

        This method generates a new unique ID using UUID.
        It can be used when creating clients, services, or reservations.
        """
        return str(uuid4())