"""Tests for the centralized exception hierarchy."""

from software_fj_reservation_system.exceptions import (
    InconsistentCalculationError,
    InvalidDataError,
    InvalidReservationError,
    LoggingError,
    ManagementSystemError,
    OperationNotAllowedError,
    ServiceUnavailableError,
)


def test_all_custom_exceptions_inherit_from_management_system_error() -> None:
    """Every specialized exception should inherit from the base system error."""

    exception_classes = [
        InvalidDataError,
        ServiceUnavailableError,
        InvalidReservationError,
        OperationNotAllowedError,
        InconsistentCalculationError,
        LoggingError,
    ]

    for exception_class in exception_classes:
        assert issubclass(exception_class, ManagementSystemError)
