"""Shared helpers for in-memory repositories."""

from __future__ import annotations

from typing import Generic, TypeVar

from software_fj_reservation_system.exceptions import InvalidDataError

T = TypeVar("T")


class BaseInMemoryRepository(Generic[T]):
    """Store entities in memory using a dictionary keyed by identifier."""

    def __init__(self, entity_name: str) -> None:
        self._entity_name = entity_name
        self._items: dict[str, T] = {}

    def add(self, entity: T) -> T:
        """Store an entity if its identifier is unique."""

        entity_id = self._normalize_id(getattr(entity, "id", None))
        if entity_id in self._items:
            raise InvalidDataError(
                f"{self._entity_name.capitalize()} with id '{entity_id}' already exists."
            )

        self._items[entity_id] = entity
        return entity

    def list_all(self) -> list[T]:
        """Return every stored entity."""

        return list(self._items.values())

    def get_by_id(self, entity_id: object) -> T:
        """Return a stored entity by identifier."""

        normalized_id = self._normalize_id(entity_id)
        try:
            return self._items[normalized_id]
        except KeyError as error:
            raise InvalidDataError(
                f"{self._entity_name.capitalize()} with id '{normalized_id}' was not found."
            ) from error

    def _normalize_id(self, entity_id: object) -> str:
        """Validate and normalize repository identifiers."""

        normalized_id = str(entity_id).strip()
        if not normalized_id:
            raise InvalidDataError(f"{self._entity_name.capitalize()} id cannot be empty.")
        return normalized_id
