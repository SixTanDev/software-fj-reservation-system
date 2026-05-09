"""Pydantic schemas for validating external application inputs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError
from pydantic import field_validator, model_validator

from software_fj_reservation_system.exceptions import ManagementSystemError
from software_fj_reservation_system.infrastructure.file_logger import FileLogger


class ClientInput(BaseModel):
    """Validated payload for client registration."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str | None = Field(default=None, min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=30)


class ServiceInput(BaseModel):
    """Validated payload for service creation."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str | None = Field(default=None, min_length=1, max_length=64)
    service_type: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=100)
    base_price: float = Field(gt=0)
    capacity: int | None = Field(default=None, gt=0)
    equipment_type: str | None = Field(default=None, min_length=1, max_length=80)
    consultant_name: str | None = Field(default=None, min_length=1, max_length=80)

    @field_validator("service_type")
    @classmethod
    def validate_service_type(cls, value: str) -> str:
        """Normalize and validate the supported service types."""

        normalized = value.strip().lower()
        if normalized not in {"room", "equipment", "consulting"}:
            raise ValueError(f"Unknown service type '{value}'.")
        return normalized

    @model_validator(mode="after")
    def validate_type_specific_fields(self) -> "ServiceInput":
        """Validate the fields that depend on the service type."""

        if self.service_type == "room":
            if self.capacity is None:
                raise ValueError("Room services require a capacity.")
            if self.equipment_type is not None or self.consultant_name is not None:
                raise ValueError("Room services only accept the capacity field.")
            return self

        if self.service_type == "equipment":
            if self.equipment_type is None:
                raise ValueError("Equipment services require an equipment type.")
            if self.capacity is not None or self.consultant_name is not None:
                raise ValueError(
                    "Equipment services only accept the equipment_type field."
                )
            return self

        if self.consultant_name is None:
            raise ValueError("Consulting services require a consultant name.")
        if self.capacity is not None or self.equipment_type is not None:
            raise ValueError("Consulting services only accept the consultant_name field.")
        return self


class ReservationInput(BaseModel):
    """Validated payload for reservation creation."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str | None = Field(default=None, min_length=1, max_length=64)
    client_id: str = Field(min_length=1, max_length=64)
    service_id: str = Field(min_length=1, max_length=64)
    duration: int = Field(gt=0)


class ProcessReservationInput(BaseModel):
    """Validated payload for reservation processing."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    reservation_id: str = Field(min_length=1, max_length=64)
    tax_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    discount_rate: float = Field(default=0.0, ge=0.0, le=1.0)

    @field_validator("discount_rate")
    @classmethod
    def validate_discount_rate(cls, value: float) -> float:
        """Keep discounts within the academic scope of the exercise."""

        if value > 0.95:
            raise ValueError(
                "Discount rate is too high for this academic reservation system."
            )
        return value


def summarize_validation_error(error: ValidationError) -> str:
    """Return a compact human-readable validation summary."""

    summary_parts: list[str] = []
    for issue in error.errors():
        location = ".".join(str(part) for part in issue.get("loc", ())) or "input"
        message = str(issue.get("msg", "Invalid value."))
        if message.startswith("Value error, "):
            message = message.removeprefix("Value error, ")
        summary_parts.append(f"{location}: {message}")
    return "; ".join(summary_parts)


def raise_logged_validation_error(
    logger: FileLogger,
    operation: str,
    state: dict[str, Any],
    wrapped_error: ManagementSystemError,
    error: ValidationError,
) -> None:
    """Log a wrapped validation error and raise the project exception with chaining."""

    logger.log_error(operation, str(wrapped_error), wrapped_error, state=state)
    raise wrapped_error from error
