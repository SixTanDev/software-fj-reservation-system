"""Base entity module."""

from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Entity:
    """Base entity for domain objects."""

    id: str

    @classmethod
    def create_id(cls) -> str:
        """Create a unique entity identifier."""
        return str(uuid4())