"""Centralized custom exceptions for the Software FJ reservation system."""


class ManagementSystemError(Exception):
    """Base exception for controlled Software FJ system errors."""


class InvalidDataError(ManagementSystemError):
    """Raised when client, service, or reservation data is invalid."""


class ServiceUnavailableError(ManagementSystemError):
    """Raised when a service cannot be reserved or used."""


class InvalidReservationError(ManagementSystemError):
    """Raised when a reservation violates business rules."""


class OperationNotAllowedError(ManagementSystemError):
    """Raised when the current object state does not allow the operation."""


class InconsistentCalculationError(ManagementSystemError):
    """Raised when a cost calculation produces an inconsistent result."""


class LoggingError(ManagementSystemError):
    """Raised when a logging failure must be surfaced in a controlled manner."""


__all__ = [
    "ManagementSystemError",
    "InvalidDataError",
    "ServiceUnavailableError",
    "InvalidReservationError",
    "OperationNotAllowedError",
    "InconsistentCalculationError",
    "LoggingError",
]
